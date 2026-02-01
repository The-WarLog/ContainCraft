# core/json_converter.py
"""
Bidirectional JSON ↔ YAML converter module.
Provides functions to convert between JSON and YAML formats with preview capabilities.
"""

import json
import yaml
from typing import Dict, Any, Optional
from pathlib import Path
from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel

console = Console()


def load_json(filepath: str) -> Optional[Dict[str, Any]]:
    """
    Load JSON file and return as Python dictionary.
    
    Args:
        filepath: Path to JSON file
        
    Returns:
        Dictionary containing JSON data, or None if error occurs
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        console.print(f"[bold red]Error: File not found: {filepath}[/]")
        return None
    except json.JSONDecodeError as e:
        console.print(f"[bold red]Error: Invalid JSON format: {e}[/]")
        return None
    except Exception as e:
        console.print(f"[bold red]Error loading JSON: {e}[/]")
        return None


def save_json(filepath: str, data: Dict[str, Any], indent: int = 2, sort_keys: bool = False) -> bool:
    """
    Save Python dictionary as JSON file.
    
    Args:
        filepath: Path to save JSON file
        data: Dictionary to save
        indent: Number of spaces for indentation (default: 2)
        sort_keys: Whether to sort keys alphabetically (default: False)
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, sort_keys=sort_keys, ensure_ascii=False)
        return True
    except Exception as e:
        console.print(f"[bold red]Error saving JSON: {e}[/]")
        return False


def json_to_yaml(json_path: str, yaml_path: str, indent: int = 2) -> bool:
    """
    Convert JSON file to YAML format.
    
    Args:
        json_path: Path to source JSON file
        yaml_path: Path to destination YAML file
        indent: Number of spaces for YAML indentation (default: 2)
        
    Returns:
        True if conversion successful, False otherwise
    """
    # Load JSON
    data = load_json(json_path)
    if data is None:
        return False
    
    # Save as YAML
    try:
        with open(yaml_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(data, f, sort_keys=False, default_flow_style=False, indent=indent)
        console.print(f"[bold green]✓ Successfully converted {json_path} → {yaml_path}[/]")
        return True
    except Exception as e:
        console.print(f"[bold red]Error saving YAML: {e}[/]")
        return False


def yaml_to_json(yaml_path: str, json_path: str, indent: int = 2, sort_keys: bool = False) -> bool:
    """
    Convert YAML file to JSON format.
    
    Args:
        yaml_path: Path to source YAML file
        json_path: Path to destination JSON file
        indent: Number of spaces for JSON indentation (default: 2)
        sort_keys: Whether to sort keys alphabetically (default: False)
        
    Returns:
        True if conversion successful, False otherwise
    """
    # Load YAML
    try:
        with open(yaml_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        console.print(f"[bold red]Error: File not found: {yaml_path}[/]")
        return False
    except yaml.YAMLError as e:
        console.print(f"[bold red]Error: Invalid YAML format: {e}[/]")
        return False
    except Exception as e:
        console.print(f"[bold red]Error loading YAML: {e}[/]")
        return False
    
    if data is None:
        console.print("[bold red]Error: YAML file is empty or invalid[/]")
        return False
    
    # Save as JSON
    if save_json(json_path, data, indent, sort_keys):
        console.print(f"[bold green]✓ Successfully converted {yaml_path} → {json_path}[/]")
        return True
    return False


def preview_json_to_yaml(json_path: str, indent: int = 2) -> Optional[str]:
    """
    Generate YAML preview from JSON file without saving.
    
    Args:
        json_path: Path to JSON file
        indent: Number of spaces for YAML indentation (default: 2)
        
    Returns:
        YAML string preview, or None if error occurs
    """
    data = load_json(json_path)
    if data is None:
        return None
    
    try:
        return yaml.safe_dump(data, sort_keys=False, default_flow_style=False, indent=indent)
    except Exception as e:
        console.print(f"[bold red]Error generating YAML preview: {e}[/]")
        return None


def preview_yaml_to_json(yaml_path: str, indent: int = 2, sort_keys: bool = False) -> Optional[str]:
    """
    Generate JSON preview from YAML file without saving.
    
    Args:
        yaml_path: Path to YAML file
        indent: Number of spaces for JSON indentation (default: 2)
        sort_keys: Whether to sort keys alphabetically (default: False)
        
    Returns:
        JSON string preview, or None if error occurs
    """
    try:
        with open(yaml_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except Exception as e:
        console.print(f"[bold red]Error loading YAML: {e}[/]")
        return None
    
    if data is None:
        return None
    
    try:
        return json.dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)
    except Exception as e:
        console.print(f"[bold red]Error generating JSON preview: {e}[/]")
        return None


def display_preview(content: str, format_type: str, title: str = "Preview") -> None:
    """
    Display formatted preview of converted content.
    
    Args:
        content: Content to display
        format_type: Format type ('json' or 'yaml')
        title: Panel title (default: "Preview")
    """
    syntax = Syntax(content, format_type, theme="monokai", line_numbers=True)
    console.print(Panel(syntax, title=title, border_style="cyan"))
