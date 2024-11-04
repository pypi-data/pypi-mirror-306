import click
import os
import glob
from typing import List, Optional, Dict, Any
from pathlib import Path
import logging
import fcntl
import time
import traceback
import subprocess
import sys
import json
import asyncio
from ..core.mapper import CodeMapper
from ..utils.formatters import format_output
from ..utils.metrics import calculate_metrics
from ..workflows.manager import WorkflowManager
from collections import defaultdict
from datetime import datetime

@click.group()
def cli():
    """DebugAI - Python Code Structure Analysis Tool"""
    pass

@cli.command()
@click.argument('paths', nargs=-1, type=click.Path(exists=True))
@click.option('--folder', is_flag=True, help='Analyze entire folder recursively')
@click.option('--output', '-o', type=click.Path(), help='Output file path')
@click.option('--format', '-f', 
              type=click.Choice(['text', 'json', 'md', 'tree']), 
              default='text',
              help='Output format')
@click.option('--show-lines', is_flag=True, help='Show line numbers')
@click.option('--components', is_flag=True, help='Show framework components (st, gr, etc.)')
@click.option('--verbose', '-v', is_flag=True, help='Show detailed output')
def analyze(paths: tuple, 
           folder: bool, 
           output: Optional[str], 
           format: str,
           show_lines: bool,
           components: bool,
           verbose: bool):
    """
    Analyze Python files and generate structure map.
    
    Examples:
        debugai analyze app.py
        debugai analyze app1.py app2.py
        debugai analyze *.py
        debugai analyze . --folder
        debugai analyze src/ --folder -o analysis.md
    """
    try:
        files_to_analyze = _get_files_to_analyze(paths, folder)
        
        if not files_to_analyze:
            raise click.UsageError("No Python files found to analyze")
            
        logging.basicConfig(
            level=logging.INFO if verbose else logging.WARNING,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        mapper = CodeMapper(
            show_line_numbers=show_lines,
            show_components=components,
            verbose=verbose
        )
        
        results = {}
        failed_files = []
        
        with click.progressbar(files_to_analyze, 
                             label='Analyzing files',
                             item_show_func=lambda x: x if x else '') as files:
            for file_path in files:
                try:
                    if not os.path.exists(file_path):
                        raise FileNotFoundError(f"File not found: {file_path}")
                        
                    if os.path.getsize(file_path) > mapper.max_file_size:
                        raise ValueError(f"File too large: {file_path}")
                        
                    result = mapper.analyze_file(file_path)
                    if 'error' in result:
                        failed_files.append((file_path, result['error']))
                    else:
                        results[file_path] = result
                        
                except Exception as e:
                    failed_files.append((file_path, str(e)))
                    if verbose:
                        click.echo(f"\nError analyzing {file_path}: {e}", err=True)
                        
        if failed_files:
            click.echo("\nFailed to analyze the following files:", err=True)
            for file_path, error in failed_files:
                click.echo(f"  {file_path}: {error}", err=True)
                
        formatted_output = format_output(results, format_type=format)
        
        if output:
            try:
                with open(output, 'w') as f:
                    f.write(formatted_output)
                click.echo(f"Analysis saved to {output}")
            except IOError as e:
                raise click.FileError(output, hint=str(e))
        else:
            click.echo(formatted_output)
            
    except Exception as e:
        click.echo(f"Fatal error: {str(e)}", err=True)
        sys.exit(1)

def _get_files_to_analyze(paths: tuple, is_folder: bool) -> List[str]:
    """Get list of Python files to analyze"""
    files_to_analyze = []
    
    if is_folder:
        for path in paths:
            if os.path.isdir(path):
                files_to_analyze.extend(glob.glob(f"{path}/**/*.py", recursive=True))
            else:
                click.echo(f"Warning: {path} is not a directory", err=True)
    else:
        for path in paths:
            if os.path.isfile(path):
                files_to_analyze.append(path)
            else:
                # Handle glob patterns
                matched_files = glob.glob(path)
                if matched_files:
                    files_to_analyze.extend(
                        [f for f in matched_files if f.endswith('.py')]
                    )
                else:
                    click.echo(f"Warning: No files match pattern {path}", err=True)
    
    return sorted(set(files_to_analyze)) 

def check_file_size(file_path: str) -> bool:
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    size = os.path.getsize(file_path)
    if size > MAX_FILE_SIZE:
        click.echo(f"Error: File {file_path} exceeds size limit of 10MB")
        return False
    return True 

def analyze_with_lock(file_path: str, timeout: int = 10):
    """Analyze file with timeout-based lock"""
    lock_path = f"{file_path}.lock"
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            with open(lock_path, 'x') as lock_file:
                try:
                    # Perform analysis
                    result = analyze_file(file_path)
                    return result
                finally:
                    os.unlink(lock_path)
            break
        except FileExistsError:
            time.sleep(0.1)
            continue
            
    raise TimeoutError(f"Could not acquire lock for {file_path}")

class AnalysisProgress:
    def __init__(self, total_files: int):
        self.total = total_files
        self.current = 0
        self.failed = []
        self.start_time = time.time()
        
    def update(self, file_path: str, success: bool):
        self.current += 1
        if not success:
            self.failed.append(file_path)

class ErrorCollector:
    def __init__(self):
        self.errors = defaultdict(list)
        
    def add_error(self, error_type: str, file_path: str, message: str):
        self.errors[error_type].append({
            'file': file_path,
            'message': message,
            'timestamp': datetime.now()
        })

class ErrorReporter:
    def __init__(self):
        self.errors = []
        
    def report_error(self, error: Dict[str, Any]):
        self.errors.append({
            **error,
            'timestamp': datetime.now(),
            'stack_trace': traceback.format_exc()
        })

class AnalysisSession:
    """Manages analysis session state and recovery"""
    
    def __init__(self, paths: tuple, options: Dict[str, Any]):
        self.paths = paths
        self.options = options
        self.results = {}
        self.failed = []
        self.progress = AnalysisProgress(0)
        self.error_collector = ErrorCollector()
        self._setup_logging()
        self._resources = []

    def _setup_logging(self):
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        if self.options.get('verbose'):
            logging.basicConfig(level=logging.DEBUG, format=log_format)
        else:
            logging.basicConfig(level=logging.INFO, format=log_format)

    def run(self):
        """Run analysis session with error handling"""
        try:
            files = self._get_files()
            self.progress = AnalysisProgress(len(files))
            
            with click.progressbar(files, label='Analyzing files') as progress_files:
                for file_path in progress_files:
                    try:
                        self._analyze_single_file(file_path)
                    except Exception as e:
                        self.error_collector.add_error('analysis_error', file_path, str(e))
                        
            return self._format_results()
            
        except Exception as e:
            click.echo(f"Fatal error: {str(e)}", err=True)
            return 1

    def _analyze_single_file(self, file_path: str):
        """Analyze single file with proper error handling"""
        try:
            with open(file_path, 'r') as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                
            if os.path.getsize(file_path) > self.options.get('max_file_size', 10*1024*1024):
                raise ValueError(f"File too large: {file_path}")
                
            mapper = CodeMapper(**self.options)
            result = mapper.analyze_file(file_path)
            
            if 'error' in result:
                self.failed.append((file_path, result['error']))
            else:
                self.results[file_path] = result
                
        except BlockingIOError:
            self.error_collector.add_error('lock_error', file_path, "File locked by another process")
        except Exception as e:
            self.error_collector.add_error('analysis_error', file_path, str(e))
        finally:
            self.progress.update(file_path, 'error' not in result)

    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._cleanup_resources()
        
    def _cleanup_resources(self):
        for resource in self._resources:
            try:
                resource.close()
            except Exception as e:
                self.logger.error(f"Failed to clean up resource: {e}")

@cli.command()
@click.argument('paths', nargs=-1, type=click.Path(exists=True))
@click.option('--iterations', '-i', default=1, help='Number of improvement iterations')
@click.option('--mode', type=click.Choice(['debug', 'optimize', 'security', 'complete', 'lint', 
                                         'refactor', 'type_hints', 'docstrings', 'tests', 'async']),
              default='debug', help='Improvement mode')
@click.option('--parallel/--sequential', default=False, help='Process files in parallel')
@click.option('--timeout', default=300, help='Timeout per file in seconds')
@click.option('--yes', is_flag=True, help='Auto-accept all changes')
@click.option('--report', type=click.Path(), help='Save detailed report')
def loop(paths: tuple, iterations: int, mode: str, parallel: bool, 
         timeout: int, yes: bool, report: Optional[str]):
    """
    Continuously improve code using AI.
    
    Examples:
        debugai loop app.py --mode=optimize
        debugai loop *.py --iterations=3 --parallel
        debugai loop src/ --mode=security --report=security.json
    """
    try:
        files = _get_files_to_analyze(paths, True)
        if not files:
            raise click.UsageError("No Python files found")
            
        runner = AiderRunner(
            file_path=files,
            iterations=iterations,
            mode=mode,
            auto_accept=yes,
            parallel=parallel,
            timeout=timeout
        )
        
        with click.progressbar(length=len(files) * iterations,
                             label=f'Running {mode} improvements') as bar:
            def progress_callback(file: str, iteration: int):
                bar.update(1)
                if not yes:
                    click.echo(f"\nCompleted {file} (iteration {iteration})")
                    
            results = runner.run_with_progress(progress_callback)
            
        if report:
            with open(report, 'w') as f:
                json.dump(results, f, indent=2)
                click.echo(f"Report saved to {report}")
                
        summary = runner.get_session_summary()
        click.echo("\nImprovement Summary:")
        click.echo(f"Files processed: {len(files)}")
        click.echo(f"Improvements made: {summary['improvements']}")
        click.echo(f"Failed attempts: {summary['failures']}")
        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.argument('workflow', type=click.Choice(['code_quality', 'security', 'performance']))
@click.option('--auto-fix', is_flag=True, help='Automatically fix issues')
@click.option('--report', type=click.Path(), help='Save detailed report')
def workflow(workflow: str, auto_fix: bool, report: Optional[str]):
    """
    Run automated improvement workflows.
    
    Examples:
        debugai workflow code_quality --auto-fix
        debugai workflow security --report security.json
    """
    try:
        manager = WorkflowManager(Path.cwd())
        results = asyncio.run(manager.run_workflow(workflow))
        
        if report:
            with open(report, 'w') as f:
                json.dump(results, f, indent=2)
                click.echo(f"Report saved to {report}")
                
        if results['success']:
            click.echo(f"Workflow {workflow} completed successfully")
        else:
            click.echo(f"Workflow {workflow} completed with issues")
            sys.exit(1)
            
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.option('--gui', is_flag=True, help='Launch the GUI interface')
def loop(gui: bool):
    """Run in continuous improvement mode"""
    if gui:
        try:
            import streamlit
            streamlit_script = Path(__file__).parent.parent / 'gui' / 'app.py'
            subprocess.run([
                'streamlit', 'run',
                str(streamlit_script),
                '--server.address=localhost',
                '--server.port=8501'
            ])
        except ImportError:
            click.echo("Streamlit not found. Install with: pip install streamlit")
            sys.exit(1)
    else:
        # Existing loop command implementation
        ...