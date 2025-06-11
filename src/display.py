"""
Simple utilities for displaying CS2 GSI data cleanly.
"""

from datetime import datetime
from typing import Dict, Any


def display_gsi_data(json_data: Dict[str, Any]) -> None:
    """Display CS2 GSI data in a clean, organized format."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"\n{'='*60}")
    print(f"CS2 GSI DATA RECEIVED - {timestamp}")
    print(f"{'='*60}")
    
    # Display all sections
    for section_name, section_data in json_data.items():
        _display_section(section_name, section_data)
        print()  # Add spacing between sections
    
    print(f"{'='*60}\n")


def _display_section(name: str, data: Any, indent: int = 0) -> None:
    """Recursively display a data section with proper indentation."""
    prefix = "  " * indent
    
    if isinstance(data, dict):
        print(f"{prefix}{name}:")
        for key, value in data.items():
            if isinstance(value, dict):
                _display_section(key, value, indent + 1)
            elif isinstance(value, list):
                print(f"{prefix}  {key}: [{len(value)} items]")
            else:
                print(f"{prefix}  {key}: {value}")
    else:
        print(f"{prefix}{name}: {data}")