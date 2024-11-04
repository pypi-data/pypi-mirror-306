import pytest
from debugai.integrations.aider_runner import AiderRunner

def test_aider_initialization():
    runner = AiderRunner("test.py")
    assert runner._previous_content == {}
    assert runner.history == []

def test_aider_recovery():
    runner = AiderRunner("test.py")
    with pytest.raises(Exception):
        runner._run_single_iteration("nonexistent.py") 