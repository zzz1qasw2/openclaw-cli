#!/usr/bin/env python3
"""PDF Document Handler (Read-Only)"""

from pathlib import Path
from typing import Dict, Any, List
from ..core.document import Document, DocumentHandler


class PdfHandler(DocumentHandler):
    """Handler for PDF documents.
    
    Read-only support using pdfplumber.
    Writing PDFs requires more complex libraries (reportlab, etc.)
    and is not supported in this basic handler.
    """
    
    def get_supported_formats(self) -> List[str]:
        return ["pdf"]
    
    def supports_format(self, format_name: str) -> bool:
        return format_name.lower() == "pdf"
    
    def read(self, source: str) -> Document:
        """Read PDF document (extract text).
        
        Args:
            source: File path to .pdf file
            
        Returns:
            Document object with extracted text
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ImportError: If pdfplumber not installed
        """
        try:
            import pdfplumber
        except ImportError:
            raise ImportError("pdfplumber not installed. Run: pip install pdfplumber")
        
        path = Path(source)
        
        if not path.exists():
            raise FileNotFoundError(f"PDF file not found: {source}")
        
        # Extract text from PDF
        pages_text = []
        metadata = {
            "path": str(path.absolute()),
            "size": path.stat().st_size,
            "format": "pdf",
            "pages": 0
        }
        
        with pdfplumber.open(str(path)) as pdf:
            metadata["pages"] = len(pdf.pages)
            
            for i, page in enumerate(pdf.pages):
                text = page.extract_text() or ""
                pages_text.append(f"--- Page {i+1} ---\n{text}")
        
        content = "\n\n".join(pages_text)
        
        # Try to extract PDF metadata
        try:
            with pdfplumber.open(str(path)) as pdf:
                pdf_metadata = pdf.metadata
                if pdf_metadata:
                    metadata.update({
                        "title": pdf_metadata.get('title', ''),
                        "author": pdf_metadata.get('author', ''),
                        "subject": pdf_metadata.get('subject', ''),
                    })
        except Exception:
            pass
        
        return Document(
            content=content,
            metadata=metadata,
            format="pdf",
            source=source
        )
    
    def write(self, destination: str, document: Document) -> Dict[str, Any]:
        """Write PDF document.
        
        Not supported in basic handler. PDF writing requires
        specialized libraries like reportlab.
        
        Returns:
            Error result indicating not supported
        """
        return {
            "success": False,
            "error": "PDF writing not supported. Use a dedicated PDF library like reportlab.",
            "command": "doc write"
        }
