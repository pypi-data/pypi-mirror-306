from typing import Dict, Optional, Type, Callable
from datetime import datetime

class RecoveryManager:
    """Handles error recovery and state management"""
    
    def __init__(self):
        self.checkpoints = {}
        self.state_history = []
        
    def save_checkpoint(self, name: str, state: Dict):
        self.checkpoints[name] = {
            'state': state,
            'timestamp': datetime.now()
        }
        
    def restore_checkpoint(self, name: str) -> Optional[Dict]:
        checkpoint = self.checkpoints.get(name, {})
        if not checkpoint:
            return None
            
        # Add validation
        if (datetime.now() - checkpoint['timestamp']).total_seconds() > 3600:
            return None  # Checkpoint too old
            
        return checkpoint.get('state')

# Add global error handler
class GlobalErrorHandler:
    def __init__(self):
        self.handlers = {}
        self.fallback = None

    def register_handler(self, error_type: Type[Exception], handler: Callable):
        self.handlers[error_type] = handler

    def handle_error(self, error: Exception) -> bool:
        handler = self.handlers.get(type(error))
        if handler:
            return handler(error)
        return self.fallback(error) if self.fallback else False