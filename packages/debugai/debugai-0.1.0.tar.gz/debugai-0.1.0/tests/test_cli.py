from click.testing import CliRunner
from debugai.cli.commands import cli
import pytest
import os

@pytest.fixture
def runner():
    return CliRunner()

def test_analyze_command(runner, sample_file):
    result = runner.invoke(cli, ['analyze', str(sample_file)])
    assert result.exit_code == 0
    assert 'Classes: 1' in result.output
    assert 'Functions: 1' in result.output

def test_analyze_multiple_files(runner, tmp_path):
    # Create test files
    file1 = tmp_path / "test1.py"
    file2 = tmp_path / "test2.py"
    file1.write_text("def test1(): pass")
    file2.write_text("def test2(): pass")
    
    result = runner.invoke(cli, ['analyze', str(file1), str(file2)])
    assert result.exit_code == 0
    assert 'test1.py' in result.output
    assert 'test2.py' in result.output

def test_analyze_folder(runner, tmp_path):
    # Create test folder structure
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "test.py").write_text("class Test: pass")
    
    result = runner.invoke(cli, ['analyze', str(tmp_path), '--folder'])
    assert result.exit_code == 0
    assert 'Test' in result.output

def test_loop_command(runner, sample_file):
    result = runner.invoke(cli, [
        'loop', 
        str(sample_file), 
        '--iterations=1',
        '--mode=debug',
        '--yes'
    ])
    assert result.exit_code == 0

def test_invalid_file(runner):
    result = runner.invoke(cli, ['analyze', 'nonexistent.py'])
    assert result.exit_code != 0
    assert 'Error' in result.output

def test_output_formats(runner, sample_file):
    formats = ['json', 'text', 'md', 'tree']
    for fmt in formats:
        result = runner.invoke(cli, [
            'analyze', 
            str(sample_file),
            '-f', fmt
        ])
        assert result.exit_code == 0