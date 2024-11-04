import cProfile
import pstats
import time
import tracemalloc
from typing import Any, Callable, Dict, List, Optional
from functools import wraps
import logging
from collections import defaultdict
import statistics
from datetime import datetime

class CodeProfiler:
    """Performance and resource usage profiler"""
    
    def __init__(self):
        self.logger = logging.getLogger('debugai.profiler')
        self.profiler = cProfile.Profile()
        self.memory_tracker = None
        self._start_time = None
        self._memory_snapshots = []

    def start_profiling(self):
        """Start profiling execution"""
        self.profiler.enable()
        self._start_time = time.time()
        tracemalloc.start()
        self.memory_tracker = tracemalloc.take_snapshot()

    def stop_profiling(self) -> Dict[str, Any]:
        """Stop profiling and return results"""
        self.profiler.disable()
        end_time = time.time()
        current_snapshot = tracemalloc.take_snapshot()
        
        stats = pstats.Stats(self.profiler)
        
        results = {
            'execution_time': end_time - self._start_time,
            'function_stats': self._get_function_stats(stats),
            'memory_usage': self._get_memory_stats(current_snapshot),
            'peak_memory': tracemalloc.get_traced_memory()[1],
            'call_count': stats.total_calls
        }
        
        tracemalloc.stop()
        return results

    def profile_function(self, func: Callable) -> Callable:
        """Decorator to profile a specific function"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            self.start_profiling()
            try:
                result = func(*args, **kwargs)
                profile_data = self.stop_profiling()
                self.logger.info(f"Profile data for {func.__name__}: {profile_data}")
                return result
            except Exception as e:
                self.logger.error(f"Error profiling {func.__name__}: {str(e)}")
                raise
        return wrapper

    def memory_snapshot(self, label: str = None):
        """Take a memory snapshot for comparison"""
        snapshot = tracemalloc.take_snapshot()
        self._memory_snapshots.append((label or f"Snapshot_{len(self._memory_snapshots)}", snapshot))

    def compare_snapshots(self, snapshot1_idx: int = -2, snapshot2_idx: int = -1) -> List[Dict[str, Any]]:
        """Compare two memory snapshots"""
        if len(self._memory_snapshots) < 2:
            raise ValueError("Need at least two snapshots to compare")
            
        snapshot1_label, snapshot1 = self._memory_snapshots[snapshot1_idx]
        snapshot2_label, snapshot2 = self._memory_snapshots[snapshot2_idx]
        
        diff = snapshot2.compare_to(snapshot1, 'lineno')
        return [{
            'file': stat.traceback[0].filename,
            'line': stat.traceback[0].lineno,
            'size_diff': stat.size_diff,
            'count_diff': stat.count_diff
        } for stat in diff]

    def _get_function_stats(self, stats: pstats.Stats) -> List[Dict[str, Any]]:
        """Extract function-level statistics"""
        function_stats = []
        for func, (cc, nc, tt, ct, callers) in stats.stats.items():
            function_stats.append({
                'function': f"{func[2]}({func[0]}:{func[1]})",
                'calls': cc,
                'cumulative_time': ct,
                'total_time': tt,
                'per_call': ct/cc if cc > 0 else 0
            })
        return sorted(function_stats, key=lambda x: x['cumulative_time'], reverse=True)

    def _get_memory_stats(self, snapshot: tracemalloc.Snapshot) -> List[Dict[str, Any]]:
        """Extract memory usage statistics"""
        memory_stats = []
        for stat in snapshot.statistics('lineno'):
            memory_stats.append({
                'file': stat.traceback[0].filename,
                'line': stat.traceback[0].lineno,
                'size': stat.size,
                'count': stat.count
            })
        return sorted(memory_stats, key=lambda x: x['size'], reverse=True)

    @staticmethod
    def format_size(size: int) -> str:
        """Format size in bytes to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f}{unit}"
            size /= 1024
        return f"{size:.1f}TB" 

class PerformanceMonitor:
    def __init__(self):
        self.metrics = defaultdict(list)
        self.thresholds = {}
        self.alerts = []

    def set_threshold(self, operation: str, max_time: float):
        self.thresholds[operation] = max_time

    def check_performance(self) -> List[Dict[str, Any]]:
        issues = super().check_performance()
        for issue in issues:
            if issue['avg_time'] > issue['threshold'] * 2:
                self.alerts.append({
                    'level': 'critical',
                    'message': f"Operation {issue['operation']} is severely delayed",
                    'timestamp': datetime.now()
                })
        return issues