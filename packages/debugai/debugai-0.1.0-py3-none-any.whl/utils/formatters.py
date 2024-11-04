from typing import Dict, Any
import json
import yaml

def format_output(results: Dict[str, Any], format_type: str = 'text') -> str:
    """Format analysis results in specified format"""
    if format_type == 'json':
        return json.dumps(results, indent=2)
    elif format_type == 'yaml':
        return yaml.dump(results, default_flow_style=False)
    elif format_type == 'md':
        return _format_markdown(results)
    else:
        return _format_text(results)

def _format_markdown(results: Dict[str, Any]) -> str:
    """Format results as markdown"""
    output = ["# Analysis Results\n"]
    for file_path, result in results.items():
        output.append(f"## {file_path}\n")
        if 'error' in result:
            output.append(f"**Error:** {result['error']}\n")
            continue
            
        if 'classes' in result:
            output.append("\n### Classes\n")
            for cls in result['classes']:
                output.append(f"- {cls['name']} (line {cls['line']})\n")
                
        if 'functions' in result:
            output.append("\n### Functions\n")
            for func in result['functions']:
                output.append(f"- {func['name']} (line {func['line']})\n")
                
    return ''.join(output)

def _format_text(results: Dict[str, Any]) -> str:
    """Format results as plain text"""
    output = ["Analysis Results\n", "=" * 50, "\n"]
    for file_path, result in results.items():
        output.append(f"\nFile: {file_path}\n{'-' * 50}\n")
        if 'error' in result:
            output.append(f"Error: {result['error']}\n")
            continue
            
        if 'classes' in result:
            output.append("\nClasses:\n")
            for cls in result['classes']:
                output.append(f"  - {cls['name']} (line {cls['line']})\n")
                
        if 'functions' in result:
            output.append("\nFunctions:\n")
            for func in result['functions']:
                output.append(f"  - {func['name']} (line {func['line']})\n")
                
    return ''.join(output)