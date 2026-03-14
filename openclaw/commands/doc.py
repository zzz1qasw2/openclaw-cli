#!/usr/bin/env python3
"""Document CLI Commands"""

import click
from pathlib import Path
from typing import List, Optional

from ..utils.output import format_output
from ..core.document import Document, DocumentConverter
from ..handlers import (
    MarkdownHandler, TextHandler, DocxHandler, 
    HtmlHandler, PdfHandler
)


@click.group()
@click.option('--json', 'output_json', is_flag=True, help='Output in JSON format')
@click.pass_context
def doc(ctx, output_json):
    """Universal Document Operations.
    
    Read, write, convert, merge, and search documents across multiple formats.
    
    Supported formats: Markdown, Plain Text, Word (.docx), HTML, PDF (read-only)
    
    Examples:
    
        openclaw doc read --file report.md
        
        openclaw doc write --file output.md --content "Hello"
        
        openclaw doc convert --input docx --output markdown --file report.docx
        
        openclaw doc merge --files a.md b.md --output combined.md
    """
    ctx.ensure_object(dict)
    if output_json:
        ctx.obj['json'] = True


@doc.command()
@click.option('--file', 'filepath', required=True, help='Document file path')
@click.option('--format', 'fmt', type=click.Choice(['markdown', 'text', 'auto']), default='auto',
              help='Document format (default: auto-detect)')
@click.option('--json', 'json_mode', is_flag=True, help='Output in JSON format')
@click.pass_context
def read(ctx, filepath, fmt, json_mode):
    """Read a document.
    
    Reads document content and metadata.
    
    Examples:
    
        openclaw doc read --file report.md
        
        openclaw doc read --file readme.txt --json
    """
    try:
        # Auto-detect format from extension
        if fmt == 'auto':
            ext = Path(filepath).suffix.lower()
            if ext in ['.md', '.markdown']:
                fmt = 'markdown'
            elif ext in ['.txt', '.text']:
                fmt = 'text'
            elif ext == '.docx':
                fmt = 'docx'
            elif ext in ['.html', '.htm']:
                fmt = 'html'
            elif ext == '.pdf':
                fmt = 'pdf'
            else:
                format_output({
                    "success": False,
                    "error": f"Unknown format for extension '{ext}'. Use --format to specify.",
                    "command": "doc read"
                }, json_mode=json_mode or ctx.obj.get('json', False))
                return
        
        # Get appropriate handler
        handlers = {
            'markdown': MarkdownHandler,
            'md': MarkdownHandler,
            'text': TextHandler,
            'txt': TextHandler,
            'plain': TextHandler,
            'docx': DocxHandler,
            'word': DocxHandler,
            'html': HtmlHandler,
            'htm': HtmlHandler,
            'pdf': PdfHandler,
        }
        
        handler_class = handlers.get(fmt.lower())
        if not handler_class:
            format_output({
                "success": False,
                "error": f"Unsupported format: {fmt}",
                "command": "doc read"
            }, json_mode=json_mode or ctx.obj.get('json', False))
            return
        
        handler = handler_class()
        
        # Read document
        document = handler.read(filepath)
        
        format_output({
            "success": True,
            "data": document.to_dict(),
            "command": "doc read"
        }, json_mode=json_mode or ctx.obj.get('json', False))
        
    except FileNotFoundError as e:
        format_output({
            "success": False,
            "error": str(e),
            "command": "doc read"
        }, json_mode=json_mode or ctx.obj.get('json', False))
    except Exception as e:
        format_output({
            "success": False,
            "error": str(e),
            "command": "doc read"
        }, json_mode=json_mode or ctx.obj.get('json', False))


@doc.command()
@click.option('--file', 'filepath', required=True, help='Output file path')
@click.option('--content', required=True, help='Document content')
@click.option('--format', 'fmt', type=click.Choice(['markdown', 'text', 'docx', 'html']), default='markdown',
              help='Document format (default: markdown)')
@click.option('--json', 'json_mode', is_flag=True, help='Output in JSON format')
@click.pass_context
def write(ctx, filepath, content, fmt, json_mode):
    """Write a document.
    
    Creates or overwrites a document with provided content.
    
    Examples:
    
        openclaw doc write --file output.md --content "# Hello"
        
        openclaw doc write --file readme.txt --content "Plain text" --format text
    """
    try:
        # Support reading content from file if starts with @
        if content.startswith('@'):
            filename = content[1:]
            content = Path(filename).read_text(encoding='utf-8')
        else:
            # Decode escape sequences like \n
            content = content.encode().decode('unicode_escape')
        
        # Create document
        document = Document(
            content=content,
            metadata={"format": fmt},
            format=fmt
        )
        
        # Get handler
        handlers = {
            'markdown': MarkdownHandler,
            'md': MarkdownHandler,
            'text': TextHandler,
            'txt': TextHandler,
            'docx': DocxHandler,
            'word': DocxHandler,
            'html': HtmlHandler,
            'htm': HtmlHandler,
        }
        
        handler_class = handlers.get(fmt.lower())
        if not handler_class:
            format_output({
                "success": False,
                "error": f"Unsupported format for writing: {fmt}",
                "command": "doc write"
            }, json_mode=json_mode or ctx.obj.get('json', False))
            return
        
        handler = handler_class()
        
        # Write document
        result = handler.write(filepath, document)
        result["command"] = "doc write"
        
        format_output(result, json_mode=json_mode or ctx.obj.get('json', False))
        
    except Exception as e:
        format_output({
            "success": False,
            "error": str(e),
            "command": "doc write"
        }, json_mode=json_mode or ctx.obj.get('json', False))


@doc.command()
@click.option('--input', 'input_fmt', required=True, 
              type=click.Choice(['markdown', 'text', 'docx', 'html', 'pdf']),
              help='Input format')
@click.option('--output', 'output_fmt', required=True, 
              type=click.Choice(['markdown', 'text', 'docx', 'html']),
              help='Output format')
@click.option('--file', 'filepath', required=True, help='Input file path')
@click.option('--output-file', 'output_file', help='Output file path (optional, prints to stdout if omitted)')
@click.option('--json', 'json_mode', is_flag=True, help='Output in JSON format')
@click.pass_context
def convert(ctx, input_fmt, output_fmt, filepath, output_file, json_mode):
    """Convert document format.
    
    Converts a document from one format to another.
    
    Examples:
    
        openclaw doc convert --input markdown --output html --file readme.md
        
        openclaw doc convert --input docx --output markdown --file report.docx --output-file report.md
    """
    try:
        # Handler mapping
        handlers = {
            'markdown': MarkdownHandler,
            'md': MarkdownHandler,
            'text': TextHandler,
            'txt': TextHandler,
            'docx': DocxHandler,
            'word': DocxHandler,
            'html': HtmlHandler,
            'htm': HtmlHandler,
            'pdf': PdfHandler,
        }
        
        # Read input document
        input_handler_class = handlers.get(input_fmt.lower())
        if not input_handler_class:
            format_output({
                "success": False,
                "error": f"Input format '{input_fmt}' not supported",
                "command": "doc convert"
            }, json_mode=json_mode or ctx.obj.get('json', False))
            return
        
        input_handler = input_handler_class()
        document = input_handler.read(filepath)
        
        # Convert
        converter = DocumentConverter()
        converted = converter.convert(document, output_fmt)
        
        # Write or output
        if output_file:
            output_handler_class = handlers.get(output_fmt.lower())
            if not output_handler_class:
                format_output({
                    "success": False,
                    "error": f"Output format '{output_fmt}' not supported for writing",
                    "command": "doc convert"
                }, json_mode=json_mode or ctx.obj.get('json', False))
                return
            
            out_handler = output_handler_class()
            
            result = out_handler.write(output_file, converted)
            result["command"] = "doc convert"
            format_output(result, json_mode=json_mode or ctx.obj.get('json', False))
        else:
            # Output to stdout
            format_output({
                "success": True,
                "data": {
                    "content": converted.content,
                    "format": converted.format
                },
                "command": "doc convert"
            }, json_mode=json_mode or ctx.obj.get('json', False))
        
    except Exception as e:
        format_output({
            "success": False,
            "error": str(e),
            "command": "doc convert"
        }, json_mode=json_mode or ctx.obj.get('json', False))


@doc.command()
@click.option('--file', 'filepaths', required=True, multiple=True, help='Input files to merge (can specify multiple times)')
@click.option('--output', 'output_file', required=True, help='Output file path')
@click.option('--separator', default='\n\n---\n\n', help='Separator between merged documents')
@click.option('--json', 'json_mode', is_flag=True, help='Output in JSON format')
@click.pass_context
def merge(ctx, filepaths, output_file, separator, json_mode):
    """Merge multiple documents.
    
    Combines multiple documents into one.
    
    Examples:
    
        openclaw doc merge --files intro.md body.md conclusion.md --output book.md
    """
    try:
        if len(filepaths) < 2:
            format_output({
                "success": False,
                "error": "At least 2 files required for merge",
                "command": "doc merge"
            }, json_mode=json_mode or ctx.obj.get('json', False))
            return
        
        # Read all documents
        contents = []
        for filepath in filepaths:
            path = Path(filepath)
            if not path.exists():
                format_output({
                    "success": False,
                    "error": f"File not found: {filepath}",
                    "command": "doc merge"
                }, json_mode=json_mode or ctx.obj.get('json', False))
                return
            contents.append(path.read_text(encoding='utf-8'))
        
        # Merge
        merged_content = separator.join(contents)
        
        # Write output
        document = Document(
            content=merged_content,
            metadata={"merged_from": list(filepaths)},
            format="markdown"
        )
        
        handler = MarkdownHandler()
        result = handler.write(output_file, document)
        result["command"] = "doc merge"
        
        format_output(result, json_mode=json_mode or ctx.obj.get('json', False))
        
    except Exception as e:
        format_output({
            "success": False,
            "error": str(e),
            "command": "doc merge"
        }, json_mode=json_mode or ctx.obj.get('json', False))


@doc.command()
@click.option('--file', 'filepath', required=True, help='Document file path')
@click.option('--pattern', required=True, help='Search pattern (regex supported)')
@click.option('--ignore-case', '-i', is_flag=True, help='Case-insensitive search')
@click.option('--json', 'json_mode', is_flag=True, help='Output in JSON format')
@click.pass_context
def search(ctx, filepath, pattern, ignore_case, json_mode):
    """Search within a document.
    
    Searches for pattern in document content.
    
    Examples:
    
        openclaw doc search --file report.md --pattern "TODO"
        
        openclaw doc search --file code.py --pattern "def.*test" --json
    """
    try:
        import re
        
        # Read document
        path = Path(filepath)
        if not path.exists():
            format_output({
                "success": False,
                "error": f"File not found: {filepath}",
                "command": "doc search"
            }, json_mode=json_mode or ctx.obj.get('json', False))
            return
        
        content = path.read_text(encoding='utf-8')
        
        # Search
        flags = re.IGNORECASE if ignore_case else 0
        matches = re.finditer(pattern, content, flags)
        
        results = []
        lines = content.splitlines()
        
        for match in matches:
            # Find line number
            start_pos = match.start()
            line_num = content[:start_pos].count('\n') + 1
            
            results.append({
                "line": line_num,
                "match": match.group(),
                "context": lines[line_num - 1] if line_num <= len(lines) else ""
            })
        
        format_output({
            "success": True,
            "data": {
                "pattern": pattern,
                "total_matches": len(results),
                "matches": results[:50]  # Limit to 50 results
            },
            "command": "doc search"
        }, json_mode=json_mode or ctx.obj.get('json', False))
        
    except Exception as e:
        format_output({
            "success": False,
            "error": str(e),
            "command": "doc search"
        }, json_mode=json_mode or ctx.obj.get('json', False))
