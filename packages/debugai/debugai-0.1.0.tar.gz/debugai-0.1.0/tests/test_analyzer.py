import pytest
from debugai.core.analyzer import CodeAnalyzer

def test_analyzer_initialization():
    analyzer = CodeAnalyzer(verbose=True)
    assert analyzer is not None
    assert analyzer.verbose == True

def test_analyze_empty_file(tmp_path):
    analyzer = CodeAnalyzer()
    empty_file = tmp_path / "empty.py"
    empty_file.write_text("")
    result = analyzer.analyze_file(str(empty_file))
    assert result.get('error') is None
    assert result.get('metrics') is not None

def test_analyze_file():
    analyzer = CodeAnalyzer()
    result = analyzer.analyze_file("test_files/sample.py")
    assert result['success'] is True
    assert 'structure' in result
    assert 'metrics' in result

def test_analyze_invalid_file():
    analyzer = CodeAnalyzer()
    result = analyzer.analyze_file("nonexistent.py")
    assert result['success'] is False
    assert 'error' in result 