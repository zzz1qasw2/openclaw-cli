#!/usr/bin/env python3
"""Output Formatting Utilities"""

import json
import sys
from datetime import datetime
from typing import Any, Dict, Optional

# Try to import rich for beautiful output, fall back to plain text
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.json import JSON
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

if RICH_AVAILABLE:
    console = Console()


def format_output(result: Dict[str, Any], json_mode: bool = False) -> None:
    """Format and print output based on mode.
    
    Args:
        result: Result dictionary from backend
        json_mode: If True, output JSON; otherwise human-readable
    """
    if json_mode:
        _output_json(result)
    else:
        _output_human(result)


def _output_json(result: Dict[str, Any]) -> None:
    """Output in JSON format"""
    output = {
        "success": result.get("success", True),
        "data": result.get("data"),
        "meta": {
            "command": result.get("command", "unknown"),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "version": "0.1.0"
        }
    }
    
    if result.get("error"):
        output["error"] = result["error"]
    
    # Use standard json for compatibility
    print(json.dumps(output, indent=2, ensure_ascii=False))


def _output_human(result: Dict[str, Any]) -> None:
    """Output in human-readable format"""
    success = result.get("success", True)
    error = result.get("error")
    data = result.get("data", {})
    command = result.get("command", "unknown")
    
    if RICH_AVAILABLE:
        _output_human_rich(success, error, data, command)
    else:
        _output_human_plain(success, error, data, command)


def _output_human_rich(success: bool, error: Optional[str], data: Dict, command: str) -> None:
    """Human-readable output with Rich"""
    if success:
        # Status indicator
        console.print("[green]✓[/green] Success", style="bold")
        console.print()
        
        # Format data based on type
        _format_data_rich(data)
    else:
        console.print(f"[red]✗ Error:[/red] {error}", style="bold red")
        if command:
            console.print(f"Command: {command}", style="dim")


def _output_human_plain(success: bool, error: Optional[str], data: Dict, command: str) -> None:
    """Human-readable output without Rich"""
    if success:
        print("✓ Success")
        print()
        _format_data_plain(data)
    else:
        print(f"✗ Error: {error}")
        if command:
            print(f"Command: {command}")


def _format_data_rich(data: Dict) -> None:
    """Format data for human reading with Rich"""
    if not data:
        return
    
    # Check if it's a document-like structure
    if "title" in data or "content" in data:
        if "title" in data:
            console.print(Panel(
                f"[bold]{data['title']}[/bold]",
                title="Document",
                border_style="blue"
            ))
        
        if "content" in data:
            console.print()
            console.print("[bold]Content:[/bold]")
            console.print(data["content"])
        
        if "doc_token" in data:
            console.print()
            console.print(f"[dim]Token: {data['doc_token']}[/dim]")
    
    # Generic key-value display
    else:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")
        
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                value = json.dumps(value, indent=2, ensure_ascii=False)
            table.add_row(str(key), str(value))
        
        console.print(table)


def _format_data_plain(data: Dict) -> None:
    """Format data for human reading without Rich"""
    if not data:
        return
    
    # Document-like structure
    if "title" in data or "content" in data:
        if "title" in data:
            print(f"Title: {data['title']}")
        
        if "content" in data:
            print()
            print("Content:")
            print(data["content"])
        
        if "doc_token" in data:
            print()
            print(f"Token: {data['doc_token']}")
    
    # Generic key-value display
    else:
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                value = json.dumps(value, indent=2, ensure_ascii=False)
            print(f"{key}: {value}")
