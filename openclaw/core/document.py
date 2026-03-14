#!/usr/bin/env python3
"""Core Document Abstraction"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod
from pathlib import Path
import json


@dataclass
class Document:
    """Unified document representation.
    
    Attributes:
        content: Document content as string
        metadata: Document metadata (path, size, format, etc.)
        format: Document format (markdown, docx, pdf, etc.)
        source: Original source (file path, URL, feishu token, etc.)
    """
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    format: str = "text"
    source: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "content": self.content,
            "metadata": self.metadata,
            "format": self.format,
            "source": self.source
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Document":
        """Create from dictionary"""
        return cls(
            content=data.get("content", ""),
            metadata=data.get("metadata", {}),
            format=data.get("format", "text"),
            source=data.get("source")
        )


class DocumentHandler(ABC):
    """Base class for format-specific document handlers.
    
    Each document format (markdown, docx, pdf, etc.) has its own handler
    that implements read/write operations.
    """
    
    @abstractmethod
    def read(self, source: str) -> Document:
        """Read document from file/path/source.
        
        Args:
            source: File path, URL, or format-specific identifier
            
        Returns:
            Document object with content and metadata
        """
        pass
    
    @abstractmethod
    def write(self, destination: str, document: Document) -> Dict[str, Any]:
        """Write document to file/destination.
        
        Args:
            destination: File path or destination identifier
            document: Document object to write
            
        Returns:
            Result dictionary with success status and metadata
        """
        pass
    
    @abstractmethod
    def supports_format(self, format_name: str) -> bool:
        """Check if this handler supports the given format.
        
        Args:
            format_name: Format name (e.g., 'markdown', 'docx', 'pdf')
            
        Returns:
            True if supported, False otherwise
        """
        pass
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported format names.
        
        Returns:
            List of format strings
        """
        # Extract from class name or override in subclass
        return []


class DocumentConverter:
    """Document format converter.
    
    Converts documents between different formats using
    registered handlers.
    """
    
    def __init__(self):
        self.handlers: Dict[str, DocumentHandler] = {}
    
    def register_handler(self, handler: DocumentHandler) -> None:
        """Register a document handler.
        
        Args:
            handler: DocumentHandler instance to register
        """
        for fmt in handler.get_supported_formats():
            self.handlers[fmt.lower()] = handler
    
    def get_handler(self, format_name: str) -> Optional[DocumentHandler]:
        """Get handler for a specific format.
        
        Args:
            format_name: Format name
            
        Returns:
            DocumentHandler or None if not found
        """
        return self.handlers.get(format_name.lower())
    
    def convert(self, document: Document, target_format: str) -> Document:
        """Convert document to target format.
        
        Args:
            document: Source document
            target_format: Target format name
            
        Returns:
            Converted document
            
        Raises:
            ValueError: If conversion is not supported
        """
        if document.format == target_format:
            return document
        
        # Simple text-based conversion (can be enhanced)
        if target_format == "markdown":
            return self._convert_to_markdown(document)
        elif target_format == "text":
            return self._convert_to_text(document)
        elif target_format == "html":
            return self._convert_to_html(document)
        else:
            raise ValueError(f"Conversion from {document.format} to {target_format} not supported")
    
    def _convert_to_markdown(self, document: Document) -> Document:
        """Convert to markdown"""
        # For now, just copy content (most formats are close to markdown)
        return Document(
            content=document.content,
            metadata=document.metadata,
            format="markdown",
            source=document.source
        )
    
    def _convert_to_text(self, document: Document) -> Document:
        """Convert to plain text"""
        # Remove markdown formatting
        content = document.content
        # Simple markdown stripping (can be enhanced)
        import re
        content = re.sub(r'#+\s*', '', content)  # Headers
        content = re.sub(r'\*\*(.*?)\*\*', r'\1', content)  # Bold
        content = re.sub(r'\*(.*?)\*', r'\1', content)  # Italic
        content = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', content)  # Links
        
        return Document(
            content=content,
            metadata=document.metadata,
            format="text",
            source=document.source
        )
    
    def _convert_to_html(self, document: Document) -> Document:
        """Convert to HTML"""
        if document.format == "markdown":
            # Simple markdown to HTML (can use markdown library)
            try:
                import markdown
                html_content = markdown.markdown(document.content)
            except ImportError:
                # Fallback: simple conversion
                html_content = f"<p>{document.content.replace(chr(10), '<br>')}</p>"
            
            return Document(
                content=html_content,
                metadata=document.metadata,
                format="html",
                source=document.source
            )
        
        # For other formats, wrap in basic HTML
        return Document(
            content=f"<p>{document.content}</p>",
            metadata=document.metadata,
            format="html",
            source=document.source
        )
