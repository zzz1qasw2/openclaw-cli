#!/usr/bin/env python3
"""Agent/Subagent CLI Commands"""

import click
import json
import sys
from pathlib import Path
from typing import List, Optional

from ..utils.output import format_output


@click.group()
@click.option('--json', 'output_json', is_flag=True, help='Output in JSON format')
@click.pass_context
def agent(ctx, output_json):
    """Agent Management Commands.
    
    Spawn, manage, and coordinate multiple AI agents for complex tasks.
    
    Examples:
    
        openclaw agent spawn --role analyst --task "analyze codebase"
        
        openclaw agent list
        
        openclaw agent batch-process --files *.md --map extract.py --reduce merge.py
    """
    ctx.ensure_object(dict)
    if output_json:
        ctx.obj['json'] = True


@agent.command()
@click.option('--role', 'role', required=True, help='Agent role (analyst, writer, reviewer, etc.)')
@click.option('--task', 'task', required=True, help='Task description')
@click.option('--label', 'label', help='Optional label for the agent')
@click.option('--model', 'model', help='Model to use (default: from OpenClaw config)')
@click.option('--timeout', 'timeout', type=int, default=300, help='Timeout in seconds')
@click.option('--json', 'json_mode', is_flag=True, help='Output in JSON format')
@click.pass_context
def spawn(ctx, role, task, label, model, timeout, json_mode):
    """Spawn a sub-agent for specialized work.
    
    Creates a new sub-agent session with a specific role and task.
    
    Examples:
    
        openclaw agent spawn --role analyst --task "analyze code structure"
        
        openclaw agent spawn --role writer --task "generate documentation" --label doc-writer
    """
    try:
        # Try to import OpenClaw sessions module
        from openclaw.sessions import sessions_spawn
        
        # Build spawn parameters
        spawn_params = {
            "task": task,
            "runtime": "subagent",
            "mode": "run",
            "timeoutSeconds": timeout,
        }
        
        if label:
            spawn_params["label"] = f"{role}-{label}"
        else:
            spawn_params["label"] = f"agent-{role}"
        
        if model:
            spawn_params["model"] = model
        
        # Spawn the agent
        result = sessions_spawn(**spawn_params)
        
        format_output({
            "success": True,
            "data": {
                "agent_id": result.get("sessionKey") or result.get("id"),
                "role": role,
                "task": task,
                "label": spawn_params["label"],
                "status": "spawned"
            },
            "command": "agent spawn"
        }, json_mode=json_mode or ctx.obj.get('json', False))
        
    except ImportError:
        # OpenClaw not available, return mock result
        format_output({
            "success": False,
            "error": "OpenClaw sessions module not available. Make sure you're running within OpenClaw.",
            "command": "agent spawn"
        }, json_mode=json_mode or ctx.obj.get('json', False))
    except Exception as e:
        format_output({
            "success": False,
            "error": str(e),
            "command": "agent spawn"
        }, json_mode=json_mode or ctx.obj.get('json', False))


@agent.command()
@click.option('--active-minutes', 'active_minutes', type=int, default=60, 
              help='Show agents active in last N minutes')
@click.option('--limit', 'limit', type=int, default=20, help='Maximum agents to list')
@click.option('--json', 'json_mode', is_flag=True, help='Output in JSON format')
@click.pass_context
def list(ctx, active_minutes, limit, json_mode):
    """List active sub-agents.
    
    Shows currently running or recently active agents.
    
    Examples:
    
        openclaw agent list
        
        openclaw agent list --active-minutes 30
    """
    try:
        from openclaw.sessions import sessions_list
        
        result = sessions_list(
            activeMinutes=active_minutes,
            limit=limit
        )
        
        agents = []
        sessions = result.get("sessions", [])
        
        for session in sessions:
            agents.append({
                "session_key": session.get("sessionKey"),
                "label": session.get("label"),
                "kind": session.get("kind"),
                "active_minutes_ago": session.get("activeMinutesAgo"),
                "message_count": session.get("messageCount")
            })
        
        format_output({
            "success": True,
            "data": {
                "total_agents": len(agents),
                "agents": agents
            },
            "command": "agent list"
        }, json_mode=json_mode or ctx.obj.get('json', False))
        
    except ImportError:
        format_output({
            "success": False,
            "error": "OpenClaw sessions module not available",
            "command": "agent list"
        }, json_mode=json_mode or ctx.obj.get('json', False))
    except Exception as e:
        format_output({
            "success": False,
            "error": str(e),
            "command": "agent list"
        }, json_mode=json_mode or ctx.obj.get('json', False))


@agent.command()
@click.option('--target', 'target', required=True, help='Target agent session key or label')
@click.option('--message', 'message', required=True, help='Message to send')
@click.option('--timeout', 'timeout', type=int, default=60, help='Timeout in seconds')
@click.option('--json', 'json_mode', is_flag=True, help='Output in JSON format')
@click.pass_context
def send(ctx, target, message, timeout, json_mode):
    """Send a message to a sub-agent.
    
    Communicates with a running agent session.
    
    Examples:
    
        openclaw agent send --target agent-analyst --message "Please analyze this file"
    """
    try:
        from openclaw.sessions import sessions_send
        
        # Determine if target is a label or session key
        send_params = {
            "message": message,
            "timeoutSeconds": timeout
        }
        
        # Try to use as session key first, fall back to label
        if target.startswith("sess_") or len(target) > 20:
            send_params["sessionKey"] = target
        else:
            send_params["label"] = target
        
        result = sessions_send(**send_params)
        
        format_output({
            "success": True,
            "data": {
                "target": target,
                "message_sent": message,
                "status": "sent"
            },
            "command": "agent send"
        }, json_mode=json_mode or ctx.obj.get('json', False))
        
    except ImportError:
        format_output({
            "success": False,
            "error": "OpenClaw sessions module not available",
            "command": "agent send"
        }, json_mode=json_mode or ctx.obj.get('json', False))
    except Exception as e:
        format_output({
            "success": False,
            "error": str(e),
            "command": "agent send"
        }, json_mode=json_mode or ctx.obj.get('json', False))


@agent.command()
@click.option('--files', 'filepatterns', required=True, multiple=True, 
              help='File patterns to process (e.g., "*.md")')
@click.option('--map', 'map_cmd', required=True, help='Map command/script')
@click.option('--reduce', 'reduce_cmd', required=True, help='Reduce command/script')
@click.option('--output', 'output_file', help='Output file path')
@click.option('--parallel', 'parallel', is_flag=True, default=True, 
              help='Process files in parallel (default: true)')
@click.option('--max-workers', 'max_workers', type=int, default=5,
              help='Maximum parallel workers')
@click.option('--json', 'json_mode', is_flag=True, help='Output in JSON format')
@click.pass_context
def batch_process(ctx, filepatterns, map_cmd, reduce_cmd, output_file, parallel, max_workers, json_mode):
    """Batch process files with Map-Reduce pattern.
    
    Spawns multiple agents to process files in parallel, then combines results.
    
    Examples:
    
        openclaw agent batch-process --files "*.md" --map extract.py --reduce merge.py
        
        openclaw agent batch-process --files chapter-*.md --map summarize.py --reduce combine.py --output book.md
    """
    try:
        import glob
        from concurrent.futures import ThreadPoolExecutor, as_completed
        
        # Expand file patterns
        all_files = []
        for pattern in filepatterns:
            matches = glob.glob(pattern)
            all_files.extend(matches)
        
        if not all_files:
            format_output({
                "success": False,
                "error": f"No files found matching patterns: {filepatterns}",
                "command": "agent batch-process"
            }, json_mode=json_mode or ctx.obj.get('json', False))
            return
        
        format_output({
            "success": True,
            "data": {
                "files_found": len(all_files),
                "files": all_files[:20],  # Limit output
                "map_command": map_cmd,
                "reduce_command": reduce_cmd,
                "parallel": parallel,
                "max_workers": max_workers,
                "status": "processing_started"
            },
            "command": "agent batch-process"
        }, json_mode=json_mode or ctx.obj.get('json', False))
        
        # Note: Full implementation would spawn agents for each file
        # and collect/reduce results. This is a skeleton implementation.
        
    except Exception as e:
        format_output({
            "success": False,
            "error": str(e),
            "command": "agent batch-process"
        }, json_mode=json_mode or ctx.obj.get('json', False))


@agent.command()
@click.option('--session', 'session_key', required=True, help='Agent session key to kill')
@click.option('--force', 'force', is_flag=True, help='Force kill without confirmation')
@click.option('--json', 'json_mode', is_flag=True, help='Output in JSON format')
@click.pass_context
def kill(ctx, session_key, force, json_mode):
    """Kill a running sub-agent.
    
    Terminates a specific agent session.
    
    Examples:
    
        openclaw agent kill --session sess_abc123
    """
    try:
        from openclaw.subagents import subagents
        
        if not force:
            if not click.confirm(f"Are you sure you want to kill agent {session_key}?"):
                click.echo("Cancelled")
                return
        
        result = subagents(action="kill", target=session_key)
        
        format_output({
            "success": True,
            "data": {
                "session_key": session_key,
                "status": "killed"
            },
            "command": "agent kill"
        }, json_mode=json_mode or ctx.obj.get('json', False))
        
    except ImportError:
        format_output({
            "success": False,
            "error": "OpenClaw subagents module not available",
            "command": "agent kill"
        }, json_mode=json_mode or ctx.obj.get('json', False))
    except Exception as e:
        format_output({
            "success": False,
            "error": str(e),
            "command": "agent kill"
        }, json_mode=json_mode or ctx.obj.get('json', False))
