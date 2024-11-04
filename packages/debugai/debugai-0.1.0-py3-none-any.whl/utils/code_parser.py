import ast
import logging
from typing import Dict, Any, Optional
import tokenize
from io import StringIO
import traceback

logger = logging.getLogger(__name__)

def parse_code(content: str) -> Dict[str, Any]:
    """
    Parse Python code content and return AST with metadata
    
    Args:
        content: String containing Python code
        
    Returns:
        Dict containing:
            - success: Boolean indicating parse success
            - ast: AST object if successful
            - error: Error message if failed
            - stats: Basic code statistics
    """
    try:
        tree = ast.parse(content)
        stats = _collect_stats(content)
        return {
            'success': True,
            'ast': tree,
            'stats': stats,
            'error': None
        }
    except SyntaxError as e:
        logger.error(f"Syntax error: {str(e)}")
        return {
            'success': False,
            'ast': None,
            'error': str(e),
            'line': e.lineno,
            'offset': e.offset,
            'text': e.text
        }
    except Exception as e:
        logger.error(f"Parse error: {str(e)}\n{traceback.format_exc()}")
        return {
            'success': False,
            'ast': None,
            'error': str(e)
        }

def _collect_stats(content: str) -> Dict[str, int]:
    """Collect basic code statistics"""
    stats = {
        'total_lines': 0,
        'code_lines': 0,
        'comment_lines': 0,
        'blank_lines': 0,
        'docstring_lines': 0
    }
    
    try:
        # Count lines
        lines = content.splitlines()
        stats['total_lines'] = len(lines)
        
        # Parse tokens
        tokens = tokenize.generate_tokens(StringIO(content).readline)
        for token in tokens:
            if token.type == tokenize.COMMENT:
                stats['comment_lines'] += 1
            elif token.type == tokenize.STRING and _is_docstring(token, tokens):
                stats['docstring_lines'] += len(token.string.splitlines())
            elif token.type == tokenize.NL:
                stats['blank_lines'] += 1
                
        stats['code_lines'] = stats['total_lines'] - (
            stats['comment_lines'] + 
            stats['blank_lines'] + 
            stats['docstring_lines']
        )
        
        return stats
    except Exception as e:
        logger.error(f"Error collecting stats: {e}")
        return stats

def _is_docstring(token: tokenize.TokenInfo, tokens: tokenize.TokenInfo) -> bool:
    """Check if a string token is a docstring"""
    try:
        return (
            token.type == tokenize.STRING and
            token.start[1] == 0 and  # Must start at column 0
            any(t.type == tokenize.INDENT for t in tokens)  # Must be at module/class/function level
        )
    except Exception:
        return False

def analyze_imports(tree: ast.AST) -> Dict[str, Any]:
    """Analyze imports in the code"""
    imports = {
        'standard_lib': [],
        'third_party': [],
        'local': []
    }
    
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            module = node.names[0].name
            if module.split('.')[0] in STANDARD_MODULES:
                imports['standard_lib'].append(module)
            elif '.' in module:
                imports['local'].append(module)
            else:
                imports['third_party'].append(module)
                
    return imports

# Standard library modules
STANDARD_MODULES = {
    'abc', 'argparse', 'ast', 'asyncio', 'collections', 'concurrent',
    'contextlib', 'copy', 'datetime', 'functools', 'glob', 'io',
    'json', 'logging', 'os', 'pathlib', 'random', 're', 'sys',
    'time', 'typing', 'unittest', 'warnings'
}

def get_complexity_score(node: ast.AST) -> int:
    """Calculate cognitive complexity score for code"""
    score = 0
    
    for child in ast.walk(node):
        # Control flow adds complexity
        if isinstance(child, (ast.If, ast.While, ast.For)):
            score += 1
        # Nested functions/classes add complexity    
        elif isinstance(child, (ast.FunctionDef, ast.ClassDef)):
            score += 1
        # Exception handling adds complexity
        elif isinstance(child, ast.Try):
            score += len(child.handlers) + len(child.finalbody)
            
    return score