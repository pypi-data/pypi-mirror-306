import gc
import psutil
from contextlib import contextmanager

class MemoryTracker:
    """Tracks memory usage and handles cleanup"""
    
    def __init__(self, threshold_mb: int = 1024):
        self.threshold = threshold_mb * 1024 * 1024
        self.peak_usage = 0
        
    @contextmanager
    def monitor(self):
        gc.collect()
        start_usage = psutil.Process().memory_info().rss
        try:
            yield
        finally:
            current_usage = psutil.Process().memory_info().rss
            self.peak_usage = max(self.peak_usage, current_usage - start_usage) 