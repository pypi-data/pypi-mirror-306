from typing import Optional, Any, Callable
from datetime import datetime, timedelta
import sys
import time

class Progress:
    """Progress tracking utility"""
    
    def __init__(self, total: int, description: str = "", 
                 show_percentage: bool = True,
                 show_time: bool = True,
                 update_interval: float = 0.1):
        self.total = total
        self.current = 0
        self.description = description
        self.show_percentage = show_percentage
        self.show_time = show_time
        self.update_interval = update_interval
        self.start_time = datetime.now()
        self.last_update = self.start_time
        
    def update(self, amount: int = 1):
        """Update progress"""
        self.current += amount
        now = datetime.now()
        
        if (now - self.last_update).total_seconds() >= self.update_interval:
            self._display_progress()
            self.last_update = now
            
    def _display_progress(self):
        """Display progress bar"""
        bar_width = 50
        progress = min(1.0, self.current / self.total)
        filled = int(bar_width * progress)
        bar = '=' * filled + '-' * (bar_width - filled)
        
        output = [f"\r{self.description} [{bar}]"]
        
        if self.show_percentage:
            output.append(f" {progress*100:.1f}%")
            
        if self.show_time:
            elapsed = datetime.now() - self.start_time
            if progress > 0:
                eta = elapsed / progress - elapsed
                output.append(f" ETA: {str(timedelta(seconds=int(eta.total_seconds())))}")
                
        sys.stdout.write(''.join(output))
        sys.stdout.flush()
        
    def finish(self):
        """Mark progress as complete"""
        self.current = self.total
        self._display_progress()
        sys.stdout.write('\n')
        sys.stdout.flush()

class AsyncProgress(Progress):
    """Async-compatible progress tracking"""
    
    async def update(self, amount: int = 1):
        """Update progress asynchronously"""
        self.current += amount
        now = datetime.now()
        
        if (now - self.last_update).total_seconds() >= self.update_interval:
            self._display_progress()
            self.last_update = now
            
    async def finish(self):
        """Mark progress as complete asynchronously"""
        self.current = self.total
        self._display_progress()
        sys.stdout.write('\n')
        sys.stdout.flush()