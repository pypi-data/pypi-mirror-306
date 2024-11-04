from collections import defaultdict
from typing import Dict, Any, List, ContextManager
import time
import statistics
from contextlib import contextmanager

class PerformanceProfiler:
    """Monitors and reports performance metrics"""
    
    def __init__(self):
        self.metrics = defaultdict(list)
        self.start_times = {}
        
    @contextmanager
    def profile(self, operation: str):
        start = time.time()
        try:
            yield
        finally:
            duration = time.time() - start
            self.metrics[operation].append(duration)
            
    def get_report(self) -> Dict[str, Any]:
        return {
            op: {
                'avg': statistics.mean(times),
                'max': max(times),
                'min': min(times),
                'count': len(times)
            }
            for op, times in self.metrics.items()
        } 