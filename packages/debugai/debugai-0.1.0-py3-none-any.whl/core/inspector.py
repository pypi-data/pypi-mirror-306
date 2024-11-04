import inspect
import logging
from typing import Any, Dict, List, Optional
from types import ModuleType, FunctionType

class CodeInspector:
    """Runtime code inspection and introspection"""
    
    def __init__(self):
        self.logger = logging.getLogger('debugai.inspector')
        
    def inspect_object(self, obj: Any) -> Dict[str, Any]:
        """Inspect any Python object and return its properties"""
        try:
            return {
                'type': type(obj).__name__,
                'doc': inspect.getdoc(obj),
                'module': inspect.getmodule(obj).__name__,
                'file': inspect.getfile(obj) if hasattr(obj, '__file__') else None,
                'attributes': self._get_attributes(obj),
                'methods': self._get_methods(obj),
                'source': self._get_source(obj)
            }
        except Exception as e:
            self.logger.error(f"Inspection failed: {str(e)}")
            return {}

    def inspect_module(self, module: ModuleType) -> Dict[str, Any]:
        """Inspect a module and return its structure"""
        try:
            return {
                'name': module.__name__,
                'file': module.__file__,
                'doc': module.__doc__,
                'functions': self._get_module_functions(module),
                'classes': self._get_module_classes(module),
                'variables': self._get_module_variables(module)
            }
        except Exception as e:
            self.logger.error(f"Module inspection failed: {str(e)}")
            return {}

    def inspect_function(self, func: FunctionType) -> Dict[str, Any]:
        """Inspect a function and return its details"""
        try:
            signature = inspect.signature(func)
            return {
                'name': func.__name__,
                'doc': func.__doc__,
                'parameters': self._get_parameters(signature),
                'return_type': self._get_return_type(signature),
                'source': inspect.getsource(func),
                'is_async': inspect.iscoroutinefunction(func),
                'is_generator': inspect.isgeneratorfunction(func)
            }
        except Exception as e:
            self.logger.error(f"Function inspection failed: {str(e)}")
            return {}

    def _get_attributes(self, obj: Any) -> Dict[str, str]:
        """Get object attributes and their types"""
        return {
            name: type(getattr(obj, name)).__name__
            for name in dir(obj)
            if not name.startswith('_') and not callable(getattr(obj, name))
        }

    def _get_methods(self, obj: Any) -> List[Dict[str, Any]]:
        """Get object methods and their signatures"""
        methods = []
        for name in dir(obj):
            if not name.startswith('_'):
                attr = getattr(obj, name)
                if callable(attr):
                    try:
                        methods.append({
                            'name': name,
                            'signature': str(inspect.signature(attr)),
                            'doc': inspect.getdoc(attr)
                        })
                    except ValueError:
                        continue
        return methods

    def _get_source(self, obj: Any) -> Optional[str]:
        """Get source code of an object"""
        try:
            return inspect.getsource(obj)
        except Exception:
            return None

    def _get_module_functions(self, module: ModuleType) -> List[Dict[str, Any]]:
        """Get all functions defined in a module"""
        functions = []
        for name, obj in inspect.getmembers(module, inspect.isfunction):
            if obj.__module__ == module.__name__:
                functions.append({
                    'name': name,
                    'signature': str(inspect.signature(obj)),
                    'doc': inspect.getdoc(obj)
                })
        return functions

    def _get_module_classes(self, module: ModuleType) -> List[Dict[str, Any]]:
        """Get all classes defined in a module"""
        classes = []
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if obj.__module__ == module.__name__:
                classes.append({
                    'name': name,
                    'bases': [base.__name__ for base in obj.__bases__],
                    'doc': inspect.getdoc(obj)
                })
        return classes

    def _get_module_variables(self, module: ModuleType) -> Dict[str, str]:
        """Get all variables defined in a module"""
        return {
            name: type(obj).__name__
            for name, obj in module.__dict__.items()
            if not name.startswith('_') and not callable(obj)
        }

    def _get_parameters(self, signature: inspect.Signature) -> List[Dict[str, Any]]:
        """Get function parameters details"""
        return [{
            'name': name,
            'kind': str(param.kind),
            'default': str(param.default) if param.default is not inspect.Parameter.empty else None,
            'annotation': str(param.annotation) if param.annotation is not inspect.Parameter.empty else None
        } for name, param in signature.parameters.items()]

    def _get_return_type(self, signature: inspect.Signature) -> Optional[str]:
        """Get function return type annotation"""
        return str(signature.return_annotation) if signature.return_annotation is not inspect.Parameter.empty else None 