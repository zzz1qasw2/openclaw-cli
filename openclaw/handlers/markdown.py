#!/usr/bin/env python3
"""Markdown Document Handler"""

from pathlib import Path
from typing import Dict, Any, List
from ..core.document import Document, DocumentHandler


class MarkdownHandler(DocumentHandler):
    """Handler for Markdown documents.
    
    Supports .md and .markdown files.
    """
    
    def get_supported_formats(self) -> List[str]:
        return ["markdown", "md"]
    
    def supports_format(self, format_name: str) -> bool:
        return format_name.lower() in ["markdown", "md"]
    
    def read(self, source: str) -> Document:
        """Read markdown file.
        
        Args:
            source: File path to markdown file
            
        Returns:
            Document object
            
        Raises:
            FileNotFoundError: If file doesn't exist
        """
        path = Path(source)
        
        if not path.exists():
            raise FileNotFoundError(f"Markdown file not found: {source}")
        
        # Read content
        content = path.read_text(encoding='utf-8')
        
        # Gather metadata
        stat = path.stat()
        metadata = {
            "path": str(path.absolute()),
            "size": stat.st_size,
            "lines": len(content.splitlines()),
            "format": "markdown"
        }
        
        return Document(
            content=content,
            metadata=metadata,
            format="markdown",
            source=source
        )
    
    def write(self, destination: str, document: Document) -> Dict[str, Any]:
        """Write markdown file.
        
        Args:
            destination: File path to write
            document: Document object
            
        Returns:
            Result dictionary
        """
        try:
            path = Path(destination)
            
            # Create parent directories if needed
            path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write content
            path.write_text(document.content, encoding='utf-8')
            
            return {
                "success": True,
                "data": {
                    "path": str(path.absolute()),
                    "size": path.stat().st_size,
                    "written": True
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
