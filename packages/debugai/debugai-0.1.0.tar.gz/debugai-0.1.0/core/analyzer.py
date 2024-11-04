import ast
import logging
from typing import Dict, List, Any, Optional, TYPE_CHECKING
from ..utils.code_parser import parse_code
from ..utils.metrics import calculate_metrics
import os
import signal
from contextlib import contextmanager
from ratelimit import limits, sleep_and_retry
import time
from collections import defaultdict
import traceback
from datetime import datetime
import resource

# Add import guard
if TYPE_CHECKING:
    from .mapper import CodeMapper

@contextmanager
def timeout(seconds: int):
    def timeout_handler(signum, frame):
        raise TimeoutError(f"Analysis timed out after {seconds} seconds")
    
    original_handler = signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, original_handler)

class AnalysisError(Exception):
    """Base class for analysis errors"""
    pass

class AnalyzerBase:
    """Base class for analysis components"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.logger = logging.getLogger(self.__class__.__name__)
        
    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Base analyze method"""
        raise NotImplementedError
        
    def cleanup(self):
        """Resource cleanup"""
        pass

class CodeAnalyzer(AnalyzerBase):
    """Main code analysis engine"""
    
    def __init__(self, verbose: bool = False, max_memory_mb: int = 1024):
        super().__init__(verbose)
        self._temp_files = []
        self._file_handles = []
        self._memory_limit = max_memory_mb * 1024 * 1024  # Convert to bytes
        self._setup_resource_limits()
        
    def _setup_resource_limits(self):
        """Set up resource limits"""
        try:
            resource.setrlimit(resource.RLIMIT_AS, (self._memory_limit, -1))
        except (ValueError, resource.error) as e:
            self.logger.warning(f"Failed to set memory limit: {e}")
            
    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze a Python file and return structured information"""
        if not os.path.exists(file_path):
            raise AnalysisError(f"File not found: {file_path}")
            
        try:
            with self._timeout(30):  # 30 second timeout
                return self._analyze_file_internal(file_path)
        except TimeoutError:
            return self._error_result("Analysis timed out")
        except MemoryError:
            return self._error_result("Out of memory")
        except Exception as e:
            return self._error_result(str(e))

    def _error_result(self, error_msg: str) -> Dict[str, Any]:
        """Create standardized error result"""
        return {
            'error': error_msg,
            'success': False,
            'timestamp': datetime.now().isoformat(),
            'traceback': traceback.format_exc()
        }

    def _analyze_file_internal(self, file_path: str) -> Dict[str, Any]:
        """Analyze a Python file and return structured information"""
        try:
            # Current: Analyzer and Mapper call each other recursively
            # Fix: Add recursion depth limit
            self._recursion_depth = getattr(self, '_recursion_depth', 0) + 1
            if self._recursion_depth > 3:
                raise RecursionError("Maximum analysis depth exceeded")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Use code_parser for initial parsing
            parse_results = parse_code(content)
            if not parse_results['success']:
                self.logger.error(f"Parser error: {parse_results['error']}")
                return {'error': parse_results['error']}

            tree = parse_results['ast']
            
            analysis = {
                'structure': self._analyze_structure(tree),
                'metrics': calculate_metrics(content),
                'imports': self._analyze_imports(tree),
                'complexity': self._analyze_complexity(tree),
                'issues': self._detect_issues(tree),
                'security': self._security_check(tree)
            }
            
            if self.verbose:
                self.logger.info(f"Analysis complete for {file_path}")
                
            return analysis
            
        except Exception as e:
            self.logger.error(f"Analysis failed: {str(e)}")
            return {'error': str(e)}
        finally:
            self._recursion_depth -= 1

    def _analyze_structure(self, tree: ast.AST) -> Dict[str, Any]:
        """Analyze code structure (classes, functions, etc.)"""
        return {
            'classes': self._extract_classes(tree),
            'functions': self._extract_functions(tree),
            'globals': self._extract_globals(tree)
        }
        
    def _analyze_imports(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Analyze imports and their usage"""
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                imports.append({
                    'module': node.names[0].name,
                    'alias': node.names[0].asname,
                    'line': node.lineno,
                    'type': 'import' if isinstance(node, ast.Import) else 'from'
                })
        return imports

    def _analyze_complexity(self, tree: ast.AST) -> Dict[str, Any]:
        """Calculate code complexity metrics"""
        complexity = {
            'cyclomatic': 0,
            'cognitive': 0,
            'maintainability': 0
        }
        # Add complexity calculation logic
        return complexity

    def _detect_issues(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Detect potential code issues"""
        issues = []
        # Add issue detection logic
        return issues

    def _security_check(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Perform security analysis"""
        vulnerabilities = []
        # Add security check logic
        return vulnerabilities

    def _extract_classes(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Extract class definitions and their structure"""
        classes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                classes.append({
                    'name': node.name,
                    'methods': [m.name for m in node.body if isinstance(m, ast.FunctionDef)],
                    'line': node.lineno,
                    'decorators': [d.id for d in node.decorator_list if isinstance(d, ast.Name)]
                })
        return classes

    def _extract_functions(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Extract function definitions and their properties"""
        functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append({
                    'name': node.name,
                    'args': [arg.arg for arg in node.args.args],
                    'line': node.lineno,
                    'decorators': [d.id for d in node.decorator_list if isinstance(d, ast.Name)],
                    'returns': self._get_return_annotation(node)
                })
        return functions

    def _extract_globals(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Extract global variables and constants"""
        globals_list = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) for t in node.targets):
                globals_list.append({
                    'name': node.targets[0].id,
                    'line': node.lineno,
                    'type': self._get_value_type(node.value)
                })
        return globals_list

    @staticmethod
    def _get_return_annotation(node: ast.FunctionDef) -> str:
        """Get function return type annotation"""
        if node.returns:
            return ast.unparse(node.returns)
        return 'Any'

    @staticmethod
    def _get_value_type(node: ast.AST) -> str:
        """Get the type of a value node"""
        if isinstance(node, ast.Num):
            return type(node.n).__name__
        elif isinstance(node, ast.Str):
            return 'str'
        elif isinstance(node, ast.List):
            return 'list'
        elif isinstance(node, ast.Dict):
            return 'dict'
        return 'unknown' 

    def cleanup(self):
        """Enhanced cleanup with proper error handling"""
        for handle in self._file_handles:
            try:
                handle.close()
            except Exception as e:
                self.logger.error(f"Failed to close handle: {e}")
                
        for temp_file in self._temp_files:
            try:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
            except Exception as e:
                self.logger.error(f"Failed to remove temp file: {e}")
                
    def __del__(self):
        self.cleanup()

    @sleep_and_retry
    @limits(calls=10, period=1)  # 10 calls per second
    def analyze_with_rate_limit(self, file_path: str):
        return self.analyze_file(file_path)

class PerformanceMonitor:
    def __init__(self):
        self.start_time = time.time()
        self.operations = defaultdict(list)
        
    def record_operation(self, operation: str, duration: float):
        self.operations[operation].append(duration)