"""Document Handlers"""

from .markdown import MarkdownHandler
from .text import TextHandler
from .docx import DocxHandler
from .html import HtmlHandler
from .pdf import PdfHandler

__all__ = [
    "MarkdownHandler",
    "TextHandler",
    "DocxHandler",
    "HtmlHandler",
    "PdfHandler"
]
