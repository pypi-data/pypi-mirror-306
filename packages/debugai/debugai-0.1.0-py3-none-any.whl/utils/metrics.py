from typing import Dict, Any
import ast
import os

def calculate_metrics(content: str) -> Dict[str, Any]:
    """Calculate code metrics"""
    metrics = {
        'lines': {
            'total': 0,
            'code': 0,
            'comment': 0,
            'blank': 0,
            'docstring': 0
        },
        'complexity': {
            'cyclomatic': 0,
            'cognitive': 0,
            'maintainability': 0
        },
        'functions': {
            'count': 0,
            'async_count': 0,
            'avg_length': 0,
            'max_length': 0
        },
        'classes': {
            'count': 0,
            'avg_methods': 0,
            'max_methods': 0
        }
    }
    
    try:
        tree = ast.parse(content)
        
        # Count lines
        lines = content.splitlines()
        metrics['lines']['total'] = len(lines)
        metrics['lines']['blank'] = len([l for l in lines if not l.strip()])
        
        # Analyze AST
        analyzer = CodeMetricsVisitor()
        analyzer.visit(tree)
        
        metrics['complexity']['cyclomatic'] = analyzer.complexity
        metrics['functions']['count'] = analyzer.function_count
        metrics['functions']['async_count'] = analyzer.async_function_count
        metrics['classes']['count'] = analyzer.class_count
        
        if analyzer.function_lengths:
            metrics['functions']['avg_length'] = sum(analyzer.function_lengths) / len(analyzer.function_lengths)
            metrics['functions']['max_length'] = max(analyzer.function_lengths)
            
        if analyzer.class_methods:
            metrics['classes']['avg_methods'] = sum(analyzer.class_methods) / len(analyzer.class_methods)
            metrics['classes']['max_methods'] = max(analyzer.class_methods)
            
        return metrics
    except Exception:
        return metrics

class CodeMetricsVisitor(ast.NodeVisitor):
    def __init__(self):
        self.complexity = 0
        self.function_count = 0
        self.async_function_count = 0
        self.class_count = 0
        self.function_lengths = []
        self.class_methods = []
        
    def visit_FunctionDef(self, node):
        self.function_count += 1
        self.function_lengths.append(node.end_lineno - node.lineno if hasattr(node, 'end_lineno') else 1)
        self.generic_visit(node)
        
    def visit_AsyncFunctionDef(self, node):
        self.async_function_count += 1
        self.function_lengths.append(node.end_lineno - node.lineno if hasattr(node, 'end_lineno') else 1)
        self.generic_visit(node)
        
    def visit_ClassDef(self, node):
        self.class_count += 1
        method_count = len([n for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))])
        self.class_methods.append(method_count)
        self.generic_visit(node)
        
    def visit_If(self, node):
        self.complexity += 1
        self.generic_visit(node)
        
    def visit_While(self, node):
        self.complexity += 1
        self.generic_visit(node)
        
    def visit_For(self, node):
        self.complexity += 1
        self.generic_visit(node)
        
    def visit_Try(self, node):
        self.complexity += len(node.handlers) + len(node.finalbody)
        self.generic_visit(node) 