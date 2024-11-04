from typing import Any, List

class IntegrationManager:
    """Manages integration between components"""
    
    def __init__(self):
        self.components = {}
        self.dependencies = {}
        self.error_handlers = {}
        
    def register_component(self, name: str, component: Any,
                          dependencies: List[str] = None):
        self.components[name] = component
        if dependencies:
            self.dependencies[name] = dependencies
            
    def validate_dependencies(self):
        """Check for circular dependencies"""
        graph = {k: set(v) for k, v in self.dependencies.items()}
        visited = set()
        
        def has_cycle(node, path):
            if node in path:
                return True
            path.add(node)
            for dep in graph.get(node, []):
                if dep not in visited and has_cycle(dep, path):
                    return True
            path.remove(node)
            visited.add(node)
            return False
            
        for node in graph:
            if node not in visited and has_cycle(node, set()):
                raise ValueError(f"Circular dependency detected at {node}") 