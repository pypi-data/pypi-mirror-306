# Need to add
def test_memory_management():
    """Test memory management and cleanup"""
    mapper = CodeMapper(max_memory_percent=90.0)
    
    # Create large test file
    with TemporaryDirectory() as tmpdir:
        test_file = Path(tmpdir) / "large.py"
        test_file.write_text("x = 'a' * 1000000")  # 1MB string
        
        result = mapper.analyze_file(str(test_file))
        assert result['success']
        assert 'memory_usage' in result
        assert result['memory_usage'] < 90.0

def test_concurrent_analysis():
    """Test concurrent file analysis"""
    mapper = CodeMapper()
    
    with TemporaryDirectory() as tmpdir:
        files = []
        for i in range(5):
            f = Path(tmpdir) / f"test{i}.py"
            f.write_text(f"def test{i}(): pass")
            files.append(f)
            
        with ThreadPoolExecutor(max_workers=3) as executor:
            results = list(executor.map(
                mapper.analyze_file,
                [str(f) for f in files]
            ))
            
        assert all(r['success'] for r in results)
        assert len(results) == 5

def test_large_file_handling():
    """Test handling of large files"""
    mapper = CodeMapper(max_file_size=1024)  # 1KB limit
    
    with TemporaryDirectory() as tmpdir:
        large_file = Path(tmpdir) / "large.py"
        large_file.write_text("x = 'a' * 2048")  # 2KB file
        
        result = mapper.analyze_file(str(large_file))
        assert not result['success']
        assert 'error' in result
        assert 'file size' in result['error'].lower() 