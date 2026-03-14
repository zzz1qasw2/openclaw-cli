#!/usr/bin/env python3
"""Plain Text Document Handler"""

from pathlib import Path
from typing import Dict, Any, List
from ..core.document import Document, DocumentHandler


class TextHandler(DocumentHandler):
    """Handler for plain text documents.
    
    Supports .txt and .text files.
    """
    
    def get_supported_formats(self) -> List[str]:
        return ["text", "txt", "plain"]
    
    def supports_format(self, format_name: str) -> bool:
        return format_name.lower() in ["text", "txt", "plain"]
    
    def read(self, source: str) -> Document:
        """Read text file.
        
        Args:
            source: File path to text file
            
        Returns:
            Document object
            
        Raises:
            FileNotFoundError: If file doesn't exist
        """
        path = Path(source)
        
        if not path.exists():
            raise FileNotFoundError(f"Text file not found: {source}")
        
        # Read content
        content = path.read_text(encoding='utf-8')
        
        # Gather metadata
        stat = path.stat()
        metadata = {
            "path": str(path.absolute()),
            "size": stat.st_size,
            "lines": len(content.splitlines()),
            "format": "text"
        }
        
        return Document(
            content=content,
            metadata=metadata,
            format="text",
            source=source
        )
    
    def write(self, destination: str, document: Document) -> Dict[str, Any]:
        """Write text file.
        
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
