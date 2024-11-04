import subprocess
import time
import logging
from typing import Optional, List, Dict, Union, Any
from datetime import datetime
import os
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from functools import wraps
import asyncio
import chardet
import difflib
import traceback
import sys
import psutil
import concurrent.futures

class TimeoutError(Exception):
    """Exception raised when a function call times out."""
    pass

def timeout(seconds):
    """Decorator to enforce a timeout on a function."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(func, *args, **kwargs)
                try:
                    return future.result(timeout=seconds)
                except concurrent.futures.TimeoutError:
                    raise TimeoutError(f"Function call timed out after {seconds} seconds")
                except Exception as e:
                    raise TimeoutError(f"Function call failed: {e}")
        return wrapper
    return decorator

class AiderRunner:
    """Enhanced Aider integration for continuous code improvement"""
    
    PRESET_MESSAGES = {
        'debug': "DEBUG without talking (EDIT ONLY WRONG FATAL THINGS IF ANY) Analyze the current logic and UI, and identify and fix any critical errors or bugs.",
        'optimize': "OPTIMIZE without talking (EDIT ONLY) Analyze and optimize the code for better performance and efficiency.",
        'security': "SECURITY without talking (EDIT ONLY) Analyze and fix any security vulnerabilities in the code.",
        'complete': "COMPLETE without talking (EDIT ONLY) Complete any missing or incomplete functionality in the code.",
        'lint': "LINT without talking (EDIT ONLY) Fix any code style issues and improve code quality.",
        'refactor': "REFACTOR without talking (EDIT ONLY) Improve code structure and maintainability.",
        'type_hints': "TYPES without talking (EDIT ONLY) Add or fix type hints throughout the code.",
        'docstrings': "DOCS without talking (EDIT ONLY) Add or improve docstrings and comments.",
        'tests': "TESTS without talking (EDIT ONLY) Add or improve unit tests.",
        'async': "ASYNC without talking (EDIT ONLY) Convert suitable functions to async/await pattern."
    }
    
    def __init__(self, 
                 file_path: Union[str, List[str]],
                 model: str = "gpt-4",
                 iterations: int = 1,
                 delay: int = 3,
                 auto_accept: bool = False,
                 mode: str = 'debug',
                 save_history: bool = True,
                 max_retries: int = 3,
                 timeout: int = 300,
                 parallel: bool = False,
                 auto_commit: bool = True,
                 auto_test: bool = True,
                 auto_lint: bool = True):
        self.file_path = file_path if isinstance(file_path, list) else [file_path]
        self.model = model
        self.iterations = iterations
        self.delay = delay
        self.auto_accept = auto_accept
        self.mode = mode
        self.save_history = save_history
        self.message = self.PRESET_MESSAGES.get(mode, self.PRESET_MESSAGES['debug'])
        self.logger = logging.getLogger('debugai.aider')
        self.history: List[Dict] = []
        self.history_file = Path('.debugai_history.json')
        self.max_retries = max_retries
        self.timeout = timeout
        self.parallel = parallel
        self._improvement_cache = {}
        self._session_stats = {
            'start_time': datetime.now(),
            'improvements': 0,
            'failures': 0,
            'retries': 0
        }
        self.auto_commit = auto_commit
        self.auto_test = auto_test
        self.auto_lint = auto_lint
        self._previous_content = {}
        self._setup_workflows()
        
    def _setup_workflows(self):
        """Setup automated workflows"""
        self.workflows = {
            'test': {
                'command': 'pytest',
                'auto_fix': True,
                'priority': 1
            },
            'lint': {
                'command': 'flake8',
                'auto_fix': True,
                'priority': 2
            },
            'type_check': {
                'command': 'mypy',
                'auto_fix': True,
                'priority': 3
            },
            'security': {
                'command': 'bandit',
                'auto_fix': True,
                'priority': 4
            }
        }

    async def run_automated_workflow(self):
        """Run automated improvement workflow"""
        try:
            # Initial analysis
            analysis_result = await self._analyze_codebase()
            
            # Run improvements in priority order
            for improvement in analysis_result['improvements']:
                await self._apply_improvement(improvement)
                
            # Run verification workflows
            if self.auto_test:
                await self._run_test_suite()
            if self.auto_lint:
                await self._run_linting()
                
            # Auto commit changes
            if self.auto_commit:
                await self._commit_changes()
                
            return {
                'success': True,
                'improvements': analysis_result['improvements'],
                'metrics': self._calculate_metrics()
            }
            
        except Exception as e:
            self.logger.error(f"Workflow failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    async def _analyze_codebase(self) -> Dict[str, Any]:
        """Analyze codebase for potential improvements"""
        improvements = []
        try:
            static_issues = await self._run_static_analysis()
            improvements.extend(static_issues)
            
            security_issues = await self._run_security_scan()
            improvements.extend(security_issues)
            
            perf_issues = await self._run_performance_analysis()
            improvements.extend(perf_issues)
            
            return {
                'improvements': sorted(improvements, key=lambda x: x['priority'])
            }
        except Exception as e:
            self.logger.error(f"Analysis failed: {e}")
            return {'improvements': []}

    def run_with_recovery(self):
        """Run Aider with automatic recovery and parallel processing"""
        try:
            if self.parallel and len(self.file_path) > 1:
                with ThreadPoolExecutor(max_workers=3) as executor:
                    futures = [
                        executor.submit(self._run_with_retries, file)
                        for file in self.file_path
                    ]
                    results = [f.result() for f in futures]
            else:
                results = [self._run_with_retries(f) for f in self.file_path]
                
            self._save_session_stats()
            return results
            
        except Exception as e:
            self.logger.error(f"Fatal error in Aider runner: {e}")
            self._save_crash_report(e)
            raise

    def _run_with_retries(self, file_path: str) -> Dict:
        """Run single file analysis with retries"""
        for attempt in range(self.max_retries):
            try:
                with timeout(self.timeout):
                    result = self._run_single_iteration(file_path)
                    if result['success']:
                        self._session_stats['improvements'] += 1
                        return result
                    
                self._session_stats['retries'] += 1
                time.sleep(self.delay * (attempt + 1))
                
            except TimeoutError:
                self.logger.warning(f"Timeout on attempt {attempt + 1}")
            except Exception as e:
                self.logger.error(f"Attempt {attempt + 1} failed: {e}")
                
        self._session_stats['failures'] += 1
        return {'success': False, 'error': 'Max retries exceeded'}

    def _run_single_iteration(self, file_path: str) -> Dict:
        """Run a single aider iteration with enhanced command options"""
        cmd = [
            "aider",
            file_path,
            "--model", self.model,
            "--message", self.message,
            "--map-refresh", "always"
        ]
        
        if self.auto_accept:
            cmd.append("--yes")
            
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            return {
                'success': True,
                'output': result.stdout
            }
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Aider command failed: {e.stderr}")
            return {
                'success': False,
                'output': e.stderr
            }
            
    def _detect_changes(self, file_path: str) -> Dict:
        """Detect changes made to the file"""
        try:
            if not os.path.exists(file_path):
                return {'error': 'File not found'}
                
            current_content = self._read_file_safe(file_path)
            if self._previous_content.get(file_path) != current_content:
                diff = self._compute_diff(self._previous_content.get(file_path, ''), current_content)
                self._previous_content[file_path] = current_content
                return {'changes': diff}
            return {'changes': None}
        except Exception as e:
            self.logger.error(f"Failed to detect changes: {e}")
            return {'error': str(e)}
        
    def _save_history(self):
        """Save operation history to file"""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save history: {e}")
            
    def _run_linting(self, file_path: str):
        """Run additional linting checks"""
        try:
            subprocess.run(["aider", file_path, "--lint"], check=True)
        except subprocess.CalledProcessError:
            self.logger.warning(f"Linting failed for {file_path}")
            
    def _run_security_check(self, file_path: str):
        """Run security checks"""
        try:
            subprocess.run(["aider", file_path, "--security-check"], check=True)
        except subprocess.CalledProcessError:
            self.logger.warning(f"Security check failed for {file_path}")
            
    def _clear_aider_messages(self):
        """Clear aider message history"""
        try:
            subprocess.run(
                ["aider", "--message", "/clear"],
                capture_output=True,
                check=True
            )
        except subprocess.CalledProcessError as e:
            self.logger.warning(f"Failed to clear aider messages: {e.stderr}")
            
    def _run_with_recovery(self, func, *args, max_retries=3):
        for attempt in range(max_retries):
            try:
                return func(*args)
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                self.logger.warning(f"Attempt {attempt + 1} failed, retrying...")
                time.sleep(self.delay)

    async def _run_test_suite(self):
        """Run test suite with proper cleanup"""
        process = None
        try:
            process = await asyncio.create_subprocess_exec(
                'pytest',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            return {
                'success': process.returncode == 0,
                'output': stdout.decode(),
                'errors': stderr.decode() if stderr else None
            }
        except Exception as e:
            raise RuntimeError(f"Test suite failed: {e}")
        finally:
            if process and process.returncode is None:
                process.terminate()
                await process.wait()

    def _read_file_safe(self, file_path: str) -> str:
        """Safely read file contents with proper encoding detection"""
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read()
                encoding = chardet.detect(raw_data)['encoding'] or 'utf-8'
                return raw_data.decode(encoding)
        except Exception as e:
            self.logger.error(f"Failed to read file {file_path}: {e}")
            return ""

    def _compute_diff(self, old_content: str, new_content: str) -> Dict[str, Any]:
        """Compute the difference between old and new content"""
        diff = difflib.unified_diff(
            old_content.splitlines(keepends=True),
            new_content.splitlines(keepends=True),
            n=3
        )
        return {
            'diff': ''.join(diff),
            'lines_added': len([l for l in diff if l.startswith('+')]),
            'lines_removed': len([l for l in diff if l.startswith('-')]),
            'timestamp': datetime.now().isoformat()
        }

    def _calculate_metrics(self) -> Dict[str, Any]:
        """Calculate improvement metrics for the session"""
        duration = (datetime.now() - self._session_stats['start_time']).total_seconds()
        return {
            'duration': duration,
            'improvements': self._session_stats['improvements'],
            'failures': self._session_stats['failures'],
            'retries': self._session_stats['retries'],
            'success_rate': (self._session_stats['improvements'] / 
                            (self._session_stats['improvements'] + 
                             self._session_stats['failures'])) * 100 if 
                            (self._session_stats['improvements'] + 
                             self._session_stats['failures']) > 0 else 0,
            'files_processed': len(self.file_path)
        }

    def _save_crash_report(self, error: Exception):
        """Save detailed crash report for debugging"""
        crash_time = datetime.now()
        crash_file = f'debugai_crash_{crash_time.strftime("%Y%m%d_%H%M%S")}.json'
        
        report = {
            'timestamp': crash_time.isoformat(),
            'error': str(error),
            'traceback': traceback.format_exc(),
            'session_stats': self._session_stats,
            'files': self.file_path,
            'mode': self.mode,
            'system_info': {
                'python_version': sys.version,
                'platform': sys.platform,
                'memory_usage': psutil.Process().memory_info().rss
            }
        }
        
        try:
            with open(crash_file, 'w') as f:
                json.dump(report, f, indent=2)
            self.logger.info(f"Crash report saved to {crash_file}")
        except Exception as e:
            self.logger.error(f"Failed to save crash report: {e}")

    def _parse_flake8_output(self, output: str) -> List[Dict[str, Any]]:
        """Parse flake8 output into structured format"""
        issues = []
        for line in output.splitlines():
            try:
                file_path, line_no, col, message = line.split(':', 3)
                issues.append({
                    'type': 'style',
                    'file': file_path,
                    'line': int(line_no),
                    'column': int(col),
                    'message': message.strip(),
                    'priority': 3,
                    'auto_fix': True,
                    'fix_command': ['autopep8', '--in-place', file_path]
                })
            except ValueError:
                continue
        return issues

    def _parse_bandit_output(self, results: Dict) -> List[Dict[str, Any]]:
        """Parse bandit output into structured format"""
        issues = []
        for result in results.get('results', []):
            issues.append({
                'type': 'security',
                'file': result['filename'],
                'line': result['line_number'],
                'message': result['issue_text'],
                'severity': result['issue_severity'],
                'priority': 1 if result['issue_severity'] == 'HIGH' else 2,
                'auto_fix': False
            })
        return issues

    def _parse_profile_output(self, output: str) -> List[Dict[str, Any]]:
        """Parse cProfile output into structured format"""
        issues = []
        # Add performance issue detection logic
        return issues

    async def _run_linting(self):
        """Run linting checks"""
        process = None
        try:
            process = await asyncio.create_subprocess_exec(
                'flake8',
                *self.file_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            return {
                'success': process.returncode == 0,
                'output': stdout.decode(),
                'errors': stderr.decode() if stderr else None
            }
        except Exception as e:
            raise RuntimeError(f"Linting failed: {e}")
        finally:
            if process and process.returncode is None:
                process.terminate()
                await process.wait()

    async def _run_static_analysis(self) -> List[Dict[str, Any]]:
        """Run static code analysis"""
        issues = []
        for file_path in self.file_path:
            try:
                process = await asyncio.create_subprocess_exec(
                    'flake8',
                    file_path,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                stdout, stderr = await process.communicate()
                if stdout:
                    issues.extend(self._parse_flake8_output(stdout.decode()))
            except Exception as e:
                self.logger.error(f"Static analysis failed for {file_path}: {e}")
        return issues

    async def _run_security_scan(self) -> List[Dict[str, Any]]:
        """Run security scan"""
        issues = []
        try:
            process = await asyncio.create_subprocess_exec(
                'bandit',
                '-r',
                *self.file_path,
                '-f',
                'json',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            if stdout:
                results = json.loads(stdout.decode())
                issues.extend(self._parse_bandit_output(results))
        except Exception as e:
            self.logger.error(f"Security scan failed: {e}")
        return issues

    async def _run_performance_analysis(self) -> List[Dict[str, Any]]:
        """Run performance analysis"""
        issues = []
        for file_path in self.file_path:
            try:
                process = await asyncio.create_subprocess_exec(
                    'python',
                    '-m',
                    'cProfile',
                    file_path,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                stdout, stderr = await process.communicate()
                if stdout:
                    issues.extend(self._parse_profile_output(stdout.decode()))
            except Exception as e:
                self.logger.error(f"Performance analysis failed for {file_path}: {e}")
        return issues