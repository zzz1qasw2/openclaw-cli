#!/usr/bin/env python3
"""OpenClaw CLI - Main Entry Point"""

import click
import sys
from . import __version__

# Import command groups
from .commands import doc, agent, workflow


@click.group()
@click.version_option(version=__version__, prog_name="openclaw")
@click.option('--json', 'output_json', is_flag=True, help='Output in JSON format')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.option('--debug', is_flag=True, help='Debug mode')
@click.pass_context
def cli(ctx, output_json, verbose, debug):
    """OpenClaw CLI - Agent-Native Interface for AI Assistants.
    
    Make any software agent-ready with standardized CLI commands.
    
    Examples:
    
        openclaw doc read --file report.md
        
        openclaw doc convert --input docx --output markdown --file report.docx
        
        openclaw doc merge --files a.md b.md --output combined.md
    """
    ctx.ensure_object(dict)
    ctx.obj['json'] = output_json
    ctx.obj['verbose'] = verbose
    ctx.obj['debug'] = debug


# Register command groups
cli.add_command(doc.doc)
cli.add_command(agent.agent)
cli.add_command(workflow.workflow)


def main():
    """Main entry point"""
    try:
        cli(obj={})
    except KeyboardInterrupt:
        click.echo("\nInterrupted by user", err=True)
        sys.exit(130)
    except Exception as e:
        if '--debug' in sys.argv:
            import traceback
            traceback.print_exc()
        else:
            click.echo(f"Error: {e}", err=True)
            click.echo("Use --debug for full traceback", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
