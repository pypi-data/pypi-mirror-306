from typing import Any, Callable, Dict, List, Optional, defaultdict
import os

class ConfigManager:
    """Manages configuration and settings"""
    
    def __init__(self):
        self.settings = {}
        self.validators = {}
        self.watchers = defaultdict(list)
        
    def register_setting(self, key: str, default: Any,
                        validator: Optional[Callable] = None):
        self.settings[key] = default
        if validator:
            self.validators[key] = validator
            
    def update_setting(self, key: str, value: Any):
        if key in self.validators:
            if not self.validators[key](value):
                raise ValueError(f"Invalid value for {key}")
        self.settings[key] = value
        for callback in self.watchers[key]:
            callback(value) 

    def _load_config(self):
        """Load configuration from file"""
        config_paths = [
            os.path.expanduser('~/.debugai/config.yml'),
            os.path.join(os.getcwd(), '.debugai.yml')
        ]
        
        # Add environment variable support
        if 'DEBUGAI_CONFIG' in os.environ:
            config_paths.insert(0, os.environ['DEBUGAI_CONFIG'])