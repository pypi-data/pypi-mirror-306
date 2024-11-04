import pytest
from pathlib import Path
from tempfile import TemporaryDirectory
from debugai.utils.code_parser import parse_code, CodeParser
from debugai.utils.metrics import calculate_metrics
from debugai.utils.memory_tracker import MemoryTracker
from debugai.utils.profiler import PerformanceProfiler
import time

def test_parse_code():
    code = "def test(): pass"
    result = parse_code(code)
    assert result['success'] is True
    assert result['body_length'] == 1

def test_calculate_metrics():
    code = """
    def test():
        # Comment
        pass
    """
    metrics = calculate_metrics(code)
    assert metrics['total_lines'] == 4
    assert metrics['comment_lines'] == 1 

def test_memory_tracker():
    tracker = MemoryTracker(threshold_mb=100)
    with tracker.monitor():
        # Allocate some memory
        x = [0] * 1000000
    assert tracker.peak_usage > 0

def test_performance_profiler():
    profiler = PerformanceProfiler()
    with profiler.profile("test_op"):
        time.sleep(0.1)
    report = profiler.get_report()
    assert "test_op" in report
    assert report["test_op"]["avg"] >= 0.1