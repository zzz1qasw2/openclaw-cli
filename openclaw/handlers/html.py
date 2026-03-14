#!/usr/bin/env python3
"""HTML Document Handler"""

from pathlib import Path
from typing import Dict, Any, List
from ..core.document import Document, DocumentHandler


class HtmlHandler(DocumentHandler):
    """Handler for HTML documents.
    
    Uses BeautifulSoup for parsing and writing HTML.
    """
    
    def get_supported_formats(self) -> List[str]:
        return ["html", "htm"]
    
    def supports_format(self, format_name: str) -> bool:
        return format_name.lower() in ["html", "htm"]
    
    def read(self, source: str) -> Document:
        """Read HTML document.
        
        Args:
            source: File path to .html file
            
        Returns:
            Document object with extracted text
            
        Raises:
            FileNotFoundError: If file doesn't exist
        """
        try:
            from bs4 import BeautifulSoup
        except ImportError:
            raise ImportError("beautifulsoup4 not installed. Run: pip install beautifulsoup4")
        
        path = Path(source)
        
        if not path.exists():
            raise FileNotFoundError(f"HTML file not found: {source}")
        
        # Read and parse HTML
        html_content = path.read_text(encoding='utf-8')
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract text
        text_content = soup.get_text(separator='\n', strip=True)
        
        # Extract title
        title = soup.title.string if soup.title else ""
        
        # Gather metadata
        stat = path.stat()
        metadata = {
            "path": str(path.absolute()),
            "size": stat.st_size,
            "format": "html",
            "title": title,
            "links_count": len(soup.find_all('a')),
            "images_count": len(soup.find_all('img')),
            "headings_count": len(soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']))
        }
        
        return Document(
            content=text_content,
            metadata=metadata,
            format="html",
            source=source
        )
    
    def write(self, destination: str, document: Document) -> Dict[str, Any]:
        """Write HTML document.
        
        Args:
            destination: File path to write
            document: Document object
            
        Returns:
            Result dictionary
        """
        try:
            from bs4 import BeautifulSoup
        except ImportError:
            raise ImportError("beautifulsoup4 not installed. Run: pip install beautifulsoup4")
        
        path = Path(destination)
        
        # Create parent directories if needed
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create basic HTML structure
        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{document.metadata.get('title', 'Document')}</title>
</head>
<body>
{self._convert_to_html(document.content)}
</body>
</html>"""
        
        # Write file
        path.write_text(html_content, encoding='utf-8')
        
        return {
            "success": True,
            "data": {
                "path": str(path.absolute()),
                "size": path.stat().st_size,
                "written": True,
                "format": "html"
            }
        }
    
    def _convert_to_html(self, content: str) -> str:
        """Convert markdown-like content to basic HTML.
        
        Simple conversion - can be enhanced with markdown library.
        """
        lines = content.split('\n')
        html_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Headers
            if line.startswith('# '):
                html_lines.append(f'<h1>{line[2:]}</h1>')
            elif line.startswith('## '):
                html_lines.append(f'<h2>{line[3:]}</h2>')
            elif line.startswith('### '):
                html_lines.append(f'<h3>{line[4:]}</h3>')
            # List items
            elif line.startswith('- '):
                html_lines.append(f'<li>{line[2:]}</li>')
            # Paragraphs
            else:
                html_lines.append(f'<p>{line}</p>')
        
        return '\n'.join(html_lines)
