import ast
from ast import NodeVisitor
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from ..utils.code_parser import parse_code
import logging
import re
from ..core.analyzer import CodeAnalyzer
from ..utils.metrics import calculate_metrics
import time
import psutil
import resource
import os
from contextlib import contextmanager

@dataclass
class Component:
    type: str
    name: str
    line: int
    args: Optional[List[str]] = None
    
@dataclass
class Function:
    name: str
    line: int
    args: List[str]
    decorators: List[str]
    
@dataclass
class Class:
    name: str
    line: int
    methods: List[Function]
    decorators: List[str]

class MemoryTracker:
    """Tracks memory usage during code analysis"""
    
    def __init__(self):
        self.start_usage = 0
        self.peak_usage = 0
        self._tracking = False

    @contextmanager
    def monitor(self):
        """Context manager for tracking memory usage"""
        try:
            self.start_tracking()
            yield
        finally:
            self.stop_tracking()

    def start_tracking(self):
        """Start memory tracking"""
        self.start_usage = psutil.Process().memory_info().rss
        self.peak_usage = self.start_usage
        self._tracking = True

    def stop_tracking(self):
        """Stop memory tracking and return stats"""
        self._tracking = False
        current = psutil.Process().memory_info().rss
        return {
            'start': self.start_usage,
            'peak': self.peak_usage,
            'end': current,
            'diff': current - self.start_usage
        }

    def update(self):
        """Update peak memory usage"""
        if self._tracking:
            current = psutil.Process().memory_info().rss
            self.peak_usage = max(self.peak_usage, current)

class CodeMapper:
    """Maps Python code structure and framework components"""
    
    def __init__(self, show_line_numbers: bool = True, 
                 show_components: bool = True,
                 verbose: bool = False,
                 max_memory_percent: float = 80.0,
                 max_file_size: int = 10 * 1024 * 1024):  # 10MB
        self.show_line_numbers = show_line_numbers
        self.show_components = show_components
        self.verbose = verbose
        self.analyzer = CodeAnalyzer(verbose=verbose)
        self.logger = logging.getLogger(__name__)
        
        # Framework component patterns
        self.PATTERNS = {
            'streamlit': [
                r'st\.[a-zA-Z_]+\s*\(',  # Function calls
                r'streamlit\.[a-zA-Z_]+\s*\(',
                r'import\s+streamlit\s+as\s+st'  # Imports
            ],
            'gradio': [r'gr\.\w+', r'gradio\.\w+'],
            'flask': [r'@app\.\w+', r'flask\.\w+'],
            'fastapi': [r'@app\.\w+', r'fastapi\.\w+'],
            'django': [r'@\w+\.route', r'django\.\w+'],
            'pytest': [r'@pytest\.\w+', r'pytest\.\w+']
        }

        # Add cache size limit
        self.ast_cache = {}
        self.cache_size = 100  # Maximum number of ASTs to cache
        self.cache_timestamps = {}
        self.cache_max_age = 300  # 5 minutes

        self.max_memory_percent = max_memory_percent
        self.max_file_size = max_file_size
        self._setup_resource_limits()

        # Add memory tracking
        self._memory_tracker = MemoryTracker()

    def _setup_resource_limits(self):
        """Setup system resource limits"""
        try:
            # Set memory limit (1GB)
            resource.setrlimit(resource.RLIMIT_AS, (1024 * 1024 * 1024, -1))
            # Set CPU time limit (30 seconds)
            resource.setrlimit(resource.RLIMIT_CPU, (30, 30))
        except (ValueError, resource.error) as e:
            self.logger.warning(f"Failed to set resource limits: {e}")

    def _check_resources(self) -> Optional[str]:
        """Check system resources before analysis"""
        try:
            memory_percent = psutil.Process().memory_percent()
            if memory_percent > self.max_memory_percent:
                return f"Memory usage too high: {memory_percent:.1f}%"
            return None
        except Exception as e:
            self.logger.error(f"Resource check failed: {e}")
            return str(e)

    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze a Python file and return its structure"""
        with self._memory_tracker.monitor():
            if not file_path.endswith('.py'):
                self.logger.warning(f"File {file_path} is not a Python file")
                return self._empty_analysis()
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Get initial parse results
                parse_results = parse_code(content)
                if not parse_results['success']:
                    self.logger.error(f"Failed to parse {file_path}: {parse_results['error']}")
                    return self._empty_analysis(error=parse_results['error'])

                tree = parse_results['ast']
                lines = content.splitlines()
                
                # Combine analyzer results with mapper analysis
                analyzer_results = self.analyzer.analyze_file(file_path)
                
                analysis = {
                    'classes': self._extract_classes(tree),
                    'functions': self._extract_functions(tree),
                    'imports': self._extract_imports(tree),
                    'metrics': calculate_metrics(content),
                    'complexity': analyzer_results.get('complexity', {}),
                    'issues': analyzer_results.get('issues', [])
                }
                
                if self.show_components:
                    analysis['components'] = self._extract_components(lines)
                    
                # Add memory check
                if psutil.Process().memory_percent() > 80:
                    raise MemoryError("System memory usage too high")
                
                return analysis
            except Exception as e:
                self.logger.error(f"Failed to analyze {file_path}: {str(e)}")
                return self._empty_analysis(error=str(e))

    def _empty_analysis(self, error: str = None) -> Dict[str, Any]:
        """Return empty analysis structure"""
        return {
            'error': error,
            'classes': [],
            'functions': [],
            'imports': [],
            'components': {} if self.show_components else None,
            'metrics': {
                'total_lines': 0,
                'code_lines': 0,
                'comment_lines': 0,
                'blank_lines': 0,
                'docstring_lines': 0
            }
        }

    def _extract_classes(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Extract class definitions with methods"""
        classes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                methods = []
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        methods.append({
                            'name': item.name,
                            'line': item.lineno if self.show_line_numbers else None,
                            'args': [arg.arg for arg in item.args.args],
                            'decorators': [ast.unparse(d) for d in item.decorator_list]
                        })
                
                classes.append({
                    'name': node.name,
                    'line': node.lineno if self.show_line_numbers else None,
                    'methods': methods,
                    'decorators': [ast.unparse(d) for d in node.decorator_list]
                })
        return classes

    def _extract_functions(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Extract function definitions"""
        # Add parent references to AST nodes
        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                setattr(child, 'parent', node)
                
        functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and not hasattr(node, 'parent'):
                # Handle top-level functions
                functions.append({
                    'name': node.name,
                    'line': node.lineno if self.show_line_numbers else None,
                    'args': [arg.arg for arg in node.args.args],
                    'decorators': [ast.unparse(d) for d in node.decorator_list]
                })
        return functions

    def _extract_components(self, lines: List[str]) -> Dict[str, List[Dict[str, Any]]]:
        """Extract framework-specific components"""
        try:
            components = {framework: [] for framework in self.PATTERNS}
            
            for i, line in enumerate(lines, 1):
                for framework, pattern in self.PATTERNS.items():
                    try:
                        matches = re.finditer(pattern, line)
                        for match in matches:
                            component = match.group()
                            components[framework].append({
                                'type': component,
                                'line': i if self.show_line_numbers else None,
                                'content': line.strip()
                            })
                    except re.error as e:
                        self.logger.error(f"Regex error for {framework}: {str(e)}")
                        continue
            
            return {k: v for k, v in components.items() if v}
        except Exception as e:
            self.logger.error(f"Component extraction failed: {str(e)}")
            return {}

    def _extract_imports(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Extract import statements"""
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                if isinstance(node, ast.Import):
                    for name in node.names:
                        imports.append({
                            'module': name.name,
                            'line': node.lineno if self.show_line_numbers else None,
                            'type': 'import'
                        })
                else:
                    for name in node.names:
                        imports.append({
                            'module': f"{node.module}.{name.name}",
                            'line': node.lineno if self.show_line_numbers else None,
                            'type': 'from'
                        })
        return imports 

    def _cache_ast(self, file_path: str, ast: Any):
        if len(self.ast_cache) >= self.cache_size:
            # Remove oldest entry
            self.ast_cache.pop(next(iter(self.ast_cache)))
        self.ast_cache[file_path] = ast

    def _cleanup_cache(self):
        """Enhanced cache cleanup with memory management"""
        current_time = time.time()
        memory_usage = psutil.Process().memory_percent()
        
        # Force cleanup if memory usage is too high
        if memory_usage > self.max_memory_percent:
            self.ast_cache.clear()
            self.cache_timestamps.clear()
            return
        
        # Normal expiration-based cleanup
        expired = [k for k, v in self.cache_timestamps.items() 
                  if current_time - v > self.cache_max_age]
        for k in expired:
            del self.ast_cache[k]
            del self.cache_timestamps[k]

    def validate_input(self, file_path: str) -> Optional[str]:
        """Validate input file"""
        if not os.path.exists(file_path):
            return "File does not exist"
        if not os.access(file_path, os.R_OK):
            return "File is not readable"
        if os.path.getsize(file_path) == 0:
            return "File is empty"
        return None

def set_resource_limits():
    # Set CPU time limit
    resource.setrlimit(resource.RLIMIT_CPU, (30, 30))
    # Set memory limit (1GB)
    resource.setrlimit(resource.RLIMIT_AS, (1024 * 1024 * 1024, -1))