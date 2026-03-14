#!/usr/bin/env python3
"""OpenClaw Workflow Engine - YAML-based Workflow Definition and Execution"""

import yaml
import click
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime
import subprocess
import json


class WorkflowStep:
    """Represents a single step in a workflow"""
    
    def __init__(self, name: str, action: str, params: Dict[str, Any]):
        self.name = name
        self.action = action
        self.params = params
        self.status = "pending"  # pending, running, success, failed
        self.result = None
        self.error = None
    
    def execute(self, verbose: bool = False) -> bool:
        """Execute this step"""
        self.status = "running"
        
        try:
            # Build command based on action
            if self.action.startswith("openclaw "):
                # OpenClaw CLI command
                cmd_parts = self.action.split()
                cmd = cmd_parts  # ['openclaw', 'doc', 'read', ...]
                
                # Add parameters as flags
                for key, value in self.params.items():
                    if isinstance(value, bool):
                        if value:
                            cmd.append(f"--{key}")
                    elif isinstance(value, list):
                        for item in value:
                            cmd.append(f"--{key}")
                            cmd.append(str(item))
                    else:
                        cmd.append(f"--{key}")
                        cmd.append(str(value))
                
                if verbose:
                    click.echo(f"  → Running: {' '.join(cmd)}")
                
                # Execute command
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=300  # 5 minute timeout per step
                )
                
                self.result = {
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "returncode": result.returncode
                }
                
                if result.returncode == 0:
                    self.status = "success"
                    return True
                else:
                    self.status = "failed"
                    self.error = result.stderr
                    return False
            
            elif self.action == "shell":
                # Shell command
                cmd = self.params.get("command", "")
                if verbose:
                    click.echo(f"  → Shell: {cmd}")
                
                result = subprocess.run(
                    cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                
                self.result = {
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "returncode": result.returncode
                }
                
                if result.returncode == 0:
                    self.status = "success"
                    return True
                else:
                    self.status = "failed"
                    self.error = result.stderr
                    return False
            
            else:
                # Unknown action
                self.status = "failed"
                self.error = f"Unknown action: {self.action}"
                return False
                
        except subprocess.TimeoutExpired:
            self.status = "failed"
            self.error = "Timeout expired (5 minutes)"
            return False
        except Exception as e:
            self.status = "failed"
            self.error = str(e)
            return False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON output"""
        return {
            "name": self.name,
            "action": self.action,
            "params": self.params,
            "status": self.status,
            "result": self.result,
            "error": self.error
        }


class Workflow:
    """Represents a complete workflow"""
    
    def __init__(self, name: str, description: str = "", steps: List[WorkflowStep] = None):
        self.name = name
        self.description = description
        self.steps = steps or []
        self.created_at = datetime.now().isoformat()
        self.status = "pending"  # pending, running, success, failed, partial
    
    def add_step(self, step: WorkflowStep):
        """Add a step to the workflow"""
        self.steps.append(step)
    
    def execute(self, verbose: bool = False, stop_on_failure: bool = True) -> bool:
        """Execute all steps in the workflow"""
        self.status = "running"
        total_steps = len(self.steps)
        success_count = 0
        failed_count = 0
        
        if verbose:
            click.echo(f"\n🚀 Starting workflow: {self.name}")
            if self.description:
                click.echo(f"   {self.description}")
            click.echo(f"   Steps: {total_steps}\n")
        
        for i, step in enumerate(self.steps, 1):
            if verbose:
                click.echo(f"[{i}/{total_steps}] {step.name}")
            
            success = step.execute(verbose)
            
            if success:
                success_count += 1
            else:
                failed_count += 1
                if stop_on_failure:
                    click.echo(f"  ✗ Step failed: {step.error}", err=True)
                    self.status = "failed"
                    return False
        
        # Determine final status
        if failed_count == 0:
            self.status = "success"
        elif success_count > 0:
            self.status = "partial"
        else:
            self.status = "failed"
        
        if verbose:
            click.echo(f"\n✓ Workflow complete: {success_count}/{total_steps} steps succeeded")
        
        return failed_count == 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON output"""
        return {
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
            "status": self.status,
            "steps": [step.to_dict() for step in self.steps],
            "summary": {
                "total": len(self.steps),
                "success": sum(1 for s in self.steps if s.status == "success"),
                "failed": sum(1 for s in self.steps if s.status == "failed")
            }
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Workflow':
        """Create Workflow from dictionary"""
        workflow = cls(
            name=data.get("name", "Untitled Workflow"),
            description=data.get("description", "")
        )
        
        for step_data in data.get("steps", []):
            step = WorkflowStep(
                name=step_data.get("name", "Unnamed Step"),
                action=step_data.get("action", ""),
                params=step_data.get("params", {})
            )
            workflow.add_step(step)
        
        return workflow
    
    @classmethod
    def from_yaml(cls, yaml_path: str) -> 'Workflow':
        """Load workflow from YAML file"""
        with open(yaml_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return cls.from_dict(data)
    
    def to_yaml(self, output_path: str):
        """Save workflow to YAML file"""
        data = {
            "name": self.name,
            "description": self.description,
            "steps": [
                {
                    "name": step.name,
                    "action": step.action,
                    "params": step.params
                }
                for step in self.steps
            ]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)


@click.group()
def workflow():
    """Workflow management commands"""
    pass


@workflow.command()
@click.option('--file', '-f', 'workflow_file', required=True, help='YAML workflow file')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.option('--continue-on-failure', is_flag=True, help='Continue even if a step fails')
@click.option('--json', 'output_json', is_flag=True, help='Output results as JSON')
def run(workflow_file: str, verbose: bool, continue_on_failure: bool, output_json: bool):
    """Run a workflow from YAML file"""
    
    # Load workflow
    try:
        workflow = Workflow.from_yaml(workflow_file)
    except Exception as e:
        click.echo(f"Error loading workflow: {e}", err=True)
        if output_json:
            click.echo(json.dumps({"success": False, "error": str(e)}))
        return
    
    # Execute workflow
    success = workflow.execute(
        verbose=verbose,
        stop_on_failure=not continue_on_failure
    )
    
    # Output results
    if output_json:
        click.echo(json.dumps(workflow.to_dict(), indent=2))
    else:
        if success or workflow.status == "partial":
            click.echo(f"\n✓ Workflow '{workflow.name}' completed")
            if workflow.status == "partial":
                click.echo(f"  (Partial: {workflow.to_dict()['summary']['success']}/{workflow.to_dict()['summary']['total']} steps)")
        else:
            click.echo(f"\n✗ Workflow '{workflow.name}' failed", err=True)


@workflow.command()
@click.option('--name', '-n', required=True, help='Workflow name')
@click.option('--description', '-d', default='', help='Workflow description')
@click.option('--output', '-o', default='workflow.yml', help='Output YAML file')
def create(name: str, description: str, output: str):
    """Create a new workflow interactively"""
    
    workflow = Workflow(name=name, description=description)
    
    click.echo(f"Creating workflow: {name}")
    click.echo("Add steps (empty action to finish):\n")
    
    step_num = 1
    while True:
        click.echo(f"\n[Step {step_num}]")
        action = click.prompt("Action (e.g., 'openclaw doc read' or 'shell')", default="")
        
        if not action:
            break
        
        name = click.prompt("Step name", default=f"Step {step_num}")
        
        # Parse parameters
        params = {}
        click.echo("Enter parameters (key=value, empty to finish):")
        while True:
            param = click.prompt("  Param", default="")
            if not param:
                break
            if '=' in param:
                key, value = param.split('=', 1)
                # Try to parse as JSON for complex values
                try:
                    params[key.strip()] = json.loads(value.strip())
                except json.JSONDecodeError:
                    params[key.strip()] = value.strip()
        
        workflow.add_step(WorkflowStep(name=name, action=action, params=params))
        step_num += 1
    
    # Save workflow
    workflow.to_yaml(output)
    click.echo(f"\n✓ Workflow saved to: {output}")


@workflow.command()
@click.option('--file', '-f', 'workflow_file', required=True, help='YAML workflow file')
@click.option('--json', 'output_json', is_flag=True, help='Output as JSON')
def validate(workflow_file: str, output_json: bool):
    """Validate a workflow YAML file"""
    
    try:
        workflow = Workflow.from_yaml(workflow_file)
        
        # Basic validation
        errors = []
        if not workflow.name:
            errors.append("Workflow name is required")
        if not workflow.steps:
            errors.append("At least one step is required")
        
        for i, step in enumerate(workflow.steps):
            if not step.action:
                errors.append(f"Step {i+1} ({step.name}): action is required")
        
        if output_json:
            result = {
                "valid": len(errors) == 0,
                "errors": errors,
                "workflow": {
                    "name": workflow.name,
                    "steps": len(workflow.steps)
                }
            }
            click.echo(json.dumps(result, indent=2))
        else:
            if errors:
                click.echo("✗ Validation failed:")
                for error in errors:
                    click.echo(f"  - {error}")
            else:
                click.echo("✓ Workflow is valid")
                click.echo(f"  Name: {workflow.name}")
                click.echo(f"  Steps: {len(workflow.steps)}")
        
    except Exception as e:
        if output_json:
            click.echo(json.dumps({"valid": False, "error": str(e)}))
        else:
            click.echo(f"✗ Validation error: {e}", err=True)


@workflow.command()
@click.option('--json', 'output_json', is_flag=True, help='Output as JSON')
def list_templates(output_json: bool):
    """List available workflow templates"""
    
    templates = [
        {
            "name": "document-conversion",
            "description": "Convert documents between formats",
            "steps": 3
        },
        {
            "name": "batch-process",
            "description": "Process multiple documents in parallel",
            "steps": 5
        },
        {
            "name": "content-pipeline",
            "description": "Extract, transform, and publish content",
            "steps": 7
        }
    ]
    
    if output_json:
        click.echo(json.dumps({"templates": templates}, indent=2))
    else:
        click.echo("\nAvailable Workflow Templates:\n")
        for tpl in templates:
            click.echo(f"  • {tpl['name']}")
            click.echo(f"    {tpl['description']}")
            click.echo(f"    Steps: {tpl['steps']}\n")


@workflow.command()
@click.option('--name', '-n', required=True, help='Template name')
@click.option('--output', '-o', default='workflow.yml', help='Output file')
def init(name: str, output: str):
    """Initialize a workflow from template"""
    
    templates = {
        "document-conversion": {
            "name": "Document Conversion Pipeline",
            "description": "Convert documents through multiple formats",
            "steps": [
                {
                    "name": "Read source document",
                    "action": "openclaw doc read",
                    "params": {"file": "input.docx", "json": True}
                },
                {
                    "name": "Convert to Markdown",
                    "action": "openclaw doc convert",
                    "params": {"input": "docx", "output": "markdown", "file": "input.docx", "output-file": "output.md"}
                },
                {
                    "name": "Verify output",
                    "action": "shell",
                    "params": {"command": "cat output.md"}
                }
            ]
        },
        "batch-process": {
            "name": "Batch Document Processing",
            "description": "Process multiple documents",
            "steps": [
                {
                    "name": "List files",
                    "action": "shell",
                    "params": {"command": "ls *.md"}
                },
                {
                    "name": "Process each file",
                    "action": "openclaw agent batch-process",
                    "params": {"files": "*.md", "map": "process.py", "reduce": "merge.py"}
                },
                {
                    "name": "Verify output",
                    "action": "shell",
                    "params": {"command": "wc -l output.md"}
                }
            ]
        }
    }
    
    if name not in templates:
        click.echo(f"Unknown template: {name}", err=True)
        click.echo("Available templates:", err=True)
        for tpl_name in templates.keys():
            click.echo(f"  - {tpl_name}", err=True)
        return
    
    tpl = templates[name]
    workflow = Workflow.from_dict({
        "name": tpl["name"],
        "description": tpl["description"],
        "steps": tpl["steps"]
    })
    
    workflow.to_yaml(output)
    click.echo(f"✓ Workflow initialized from template '{name}'")
    click.echo(f"  Saved to: {output}")
