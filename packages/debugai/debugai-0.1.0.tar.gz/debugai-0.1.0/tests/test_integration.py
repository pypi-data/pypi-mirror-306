import pytest
from debugai import CodeMapper, CodeAnalyzer
from tempfile import TemporaryDirectory
from pathlib import Path
from debugai.cli.commands import AiderRunner
from debugai.config.config_manager import ConfigManager
from debugai.config.config_validator import ConfigValidator

def test_full_analysis(sample_file):
    mapper = CodeMapper(show_components=True)
    analyzer = CodeAnalyzer()
    
    mapper_result = mapper.analyze_file(sample_file)
    analyzer_result = analyzer.analyze_file(sample_file)
    
    assert mapper_result['success'] is True
    assert analyzer_result['success'] is True
    assert 'components' in mapper_result
    assert 'streamlit' in mapper_result['components'] 

# Add integration test suite
def test_full_pipeline():
    """Test complete analysis pipeline"""
    with TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "test.py"
        test_file.write_text("def test(): pass")
        
        # Test full pipeline
        mapper = CodeMapper(show_components=True)
        analyzer = CodeAnalyzer()
        profiler = CodeProfiler()
        
        with profiler.profile("full_analysis"):
            mapper_result = mapper.analyze_file(str(test_file))
            analyzer_result = analyzer.analyze_file(str(test_file))
            
        assert mapper_result['success']
        assert analyzer_result['success']
        assert profiler.get_report()

def test_aider_integration():
    """Test aider integration"""
    with TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "test.py"
        test_file.write_text("def buggy(): reutrn None")  # Intentional typo
        
        runner = AiderRunner(
            file_path=str(test_file),
            iterations=1,
            mode='debug',
            auto_accept=True
        )
        
        runner.run()
        assert test_file.read_text() == "def buggy(): return None"

def test_config_integration():
    """Test configuration system"""
    config = ConfigManager()
    config.register_setting('max_file_size', 1024 * 1024)
    
    validator = ConfigValidator()
    validator.register_schema('analysis', {
        'max_file_size': {'type': 'integer', 'min': 0}
    })
    
    assert validator.validate_config({'analysis': {'max_file_size': 1024}}) == []