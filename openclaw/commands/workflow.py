#!/usr/bin/env python3
"""OpenClaw Workflow Engine v2 - Advanced Features (Phase 4)

Features:
- Conditional execution (if/else)
- Parallel step execution
- Variable system for data passing
- Rich progress bars
- Error recovery and retry
"""

import yaml
import click
from typing import Dict, List, Any, Optional, Callable
from pathlib import Path
from datetime import datetime
import subprocess
import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field


@dataclass
class ExecutionContext:
    """Execution context with variables and state"""
    variables: Dict[str, Any] = field(default_factory=dict)
    step_results: Dict[str, Any] = field(default_factory=dict)
    working_dir: str = field(default_factory=lambda: Path.cwd())
    
    def set_variable(self, name: str, value: Any):
        """Set a variable"""
        self.variables[name] = value
    
    def get_variable(self, name: str, default: Any = None) -> Any:
        """Get a variable, with optional default"""
        return self.variables.get(name, default)
    
    def interpolate(self, text: str) -> str:
        """Interpolate variables in text using ${var} or $var syntax"""
        if not isinstance(text, str):
            return text
        
        # Replace ${var} syntax
        def replace_braced(match):
            var_name = match.group(1)
            return str(self.variables.get(var_name, match.group(0)))
        
        text = re.sub(r'\$\{(\w+)\}', replace_braced, text)
        
        # Replace $var syntax (word boundary)
        def replace_simple(match):
            var_name = match.group(1)
            return str(self.variables.get(var_name, match.group(0)))
        
        text = re.sub(r'\$(\w+)', replace_simple, text)
        
        return text
    
    def interpolate_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Interpolate all parameters recursively"""
        result = {}
        for key, value in params.items():
            if isinstance(value, str):
                result[key] = self.interpolate(value)
            elif isinstance(value, list):
                result[key] = [
                    self.interpolate(v) if isinstance(v, str) else v
                    for v in value
                ]
            elif isinstance(value, dict):
                result[key] = self.interpolate_params(value)
            else:
                result[key] = value
        return result


class WorkflowStep:
    """Represents a single step in a workflow with advanced features"""
    
    def __init__(self, name: str, action: str, params: Dict[str, Any],
                 condition: Optional[str] = None,
                 retry: int = 0,
                 timeout: int = 300,
                 parallel: bool = False,
                 output_var: Optional[str] = None):
        self.name = name
        self.action = action
        self.params = params
        self.condition = condition  # Conditional execution
        self.retry = retry  # Number of retries on failure
        self.timeout = timeout  # Timeout in seconds
        self.parallel = parallel  # Can run in parallel with other steps
        self.output_var = output_var  # Store result in variable
        
        self.status = "pending"  # pending, running, success, failed, skipped
        self.result = None
        self.error = None
        self.execution_time = 0
    
    def should_execute(self, context: ExecutionContext) -> bool:
        """Check if this step should execute based on condition"""
        if not self.condition:
            return True
        
        # Interpolate condition string
        condition = context.interpolate(self.condition)
        
        # Simple condition evaluation (support basic comparisons)
        try:
            # Support: var == "value", var != "value", var, !var
            condition = condition.strip()
            
            if '==' in condition:
                parts = condition.split('==')
                left = parts[0].strip().strip('"\'')
                right = parts[1].strip().strip('"\'')
                return left == right
            elif '!=' in condition:
                parts = condition.split('!=')
                left = parts[0].strip().strip('"\'')
                right = parts[1].strip().strip('"\'')
                return left != right
            elif condition.startswith('!'):
                var_name = condition[1:].strip()
                return not bool(context.get_variable(var_name, False))
            else:
                # Just check if variable exists and is truthy
                return bool(context.get_variable(condition, False))
        except Exception as e:
            click.echo(f"  ⚠ Condition evaluation failed: {e}", err=True)
            return False
    
    def execute(self, context: ExecutionContext, verbose: bool = False) -> bool:
        """Execute this step with retry support"""
        import time
        
        # Check condition
        if not self.should_execute(context):
            self.status = "skipped"
            if verbose:
                click.echo(f"  ⊘ Skipped (condition not met)")
            return True
        
        # Interpolate parameters
        params = context.interpolate_params(self.params)
        
        attempts = 0
        max_attempts = self.retry + 1
        
        while attempts < max_attempts:
            attempts += 1
            self.status = "running"
            start_time = time.time()
            
            try:
                # Build command based on action
                if self.action.startswith("openclaw "):
                    # OpenClaw CLI command
                    cmd_parts = self.action.split()
                    cmd = cmd_parts
                    
                    # Add parameters as flags
                    for key, value in params.items():
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
                        timeout=self.timeout,
                        cwd=context.working_dir
                    )
                    
                    self.result = {
                        "stdout": result.stdout,
                        "stderr": result.stderr,
                        "returncode": result.returncode
                    }
                    
                    if result.returncode == 0:
                        self.status = "success"
                        self.execution_time = time.time() - start_time
                        
                        # Store output if requested
                        if self.output_var:
                            context.set_variable(self.output_var, result.stdout)
                            context.step_results[self.name] = result.stdout
                        
                        return True
                    else:
                        self.error = result.stderr
                        raise Exception(f"Command failed with code {result.returncode}")
                
                elif self.action == "shell":
                    # Shell command
                    cmd = params.get("command", "")
                    if verbose:
                        click.echo(f"  → Shell: {cmd}")
                    
                    result = subprocess.run(
                        cmd,
                        shell=True,
                        capture_output=True,
                        text=True,
                        timeout=self.timeout,
                        cwd=context.working_dir
                    )
                    
                    self.result = {
                        "stdout": result.stdout,
                        "stderr": result.stderr,
                        "returncode": result.returncode
                    }
                    
                    if result.returncode == 0:
                        self.status = "success"
                        self.execution_time = time.time() - start_time
                        
                        # Store output if requested
                        if self.output_var:
                            context.set_variable(self.output_var, result.stdout)
                            context.step_results[self.name] = result.stdout
                        
                        return True
                    else:
                        self.error = result.stderr
                        raise Exception(f"Shell command failed: {result.stderr}")
                
                elif self.action == "set":
                    # Set variable action
                    var_name = params.get("name", "")
                    var_value = params.get("value", "")
                    context.set_variable(var_name, var_value)
                    
                    self.status = "success"
                    self.execution_time = time.time() - start_time
                    self.result = {"variable": var_name, "value": var_value}
                    
                    if verbose:
                        click.echo(f"  → Set ${var_name} = {var_value}")
                    
                    return True
                
                else:
                    # Unknown action
                    self.status = "failed"
                    self.error = f"Unknown action: {self.action}"
                    raise Exception(self.error)
                    
            except subprocess.TimeoutExpired:
                self.error = f"Timeout expired ({self.timeout}s)"
                self.status = "failed"
            except Exception as e:
                self.error = str(e)
                self.status = "failed"
                
                if attempts < max_attempts:
                    if verbose:
                        click.echo(f"  ⚠ Retry {attempts}/{max_attempts}: {self.error}")
                    time.sleep(1)  # Wait before retry
                    continue
                else:
                    self.execution_time = time.time() - start_time
                    return False
        
        self.execution_time = time.time() - start_time
        return False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON output"""
        return {
            "name": self.name,
            "action": self.action,
            "params": self.params,
            "condition": self.condition,
            "retry": self.retry,
            "timeout": self.timeout,
            "parallel": self.parallel,
            "output_var": self.output_var,
            "status": self.status,
            "result": self.result,
            "error": self.error,
            "execution_time": round(self.execution_time, 3)
        }


class Workflow:
    """Represents a complete workflow with advanced features"""
    
    def __init__(self, name: str, description: str = "", steps: List[WorkflowStep] = None):
        self.name = name
        self.description = description
        self.steps = steps or []
        self.created_at = datetime.now().isoformat()
        self.status = "pending"
        self.execution_time = 0
    
    def add_step(self, step: WorkflowStep):
        """Add a step to the workflow"""
        self.steps.append(step)
    
    def execute(self, verbose: bool = False, stop_on_failure: bool = True,
                max_workers: int = 4) -> bool:
        """Execute all steps with parallel support"""
        import time
        from rich.console import Console
        from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
        
        console = Console()
        context = ExecutionContext()
        
        self.status = "running"
        start_time = time.time()
        
        # Separate parallel and sequential steps
        parallel_groups = []
        current_sequential = []
        
        for step in self.steps:
            if step.parallel:
                if current_sequential:
                    parallel_groups.append(("sequential", current_sequential))
                    current_sequential = []
                parallel_groups.append(("parallel", [step]))
            else:
                if parallel_groups and parallel_groups[-1][0] == "parallel":
                    parallel_groups[-1][1].append(step)
                else:
                    current_sequential.append(step)
        
        if current_sequential:
            parallel_groups.append(("sequential", current_sequential))
        
        # Execute step groups
        total_steps = len(self.steps)
        completed_steps = 0
        success_count = 0
        failed_count = 0
        skipped_count = 0
        
        if verbose:
            console.print(f"\n[bold blue]🚀 Starting workflow:[/bold blue] {self.name}")
            if self.description:
                console.print(f"   [dim]{self.description}[/dim]")
            console.print(f"   Steps: {total_steps}\n")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=console,
            disable=not verbose
        ) as progress:
            
            task = progress.add_task(f"[cyan]{self.name}", total=total_steps)
            
            for group_type, steps in parallel_groups:
                if group_type == "sequential":
                    # Execute sequential steps
                    for step in steps:
                        progress.update(task, description=f"[cyan]{step.name}")
                        
                        if verbose:
                            console.print(f"\n[{completed_steps + 1}/{total_steps}] [bold]{step.name}[/bold]")
                        
                        success = step.execute(context, verbose)
                        
                        if success:
                            if step.status == "skipped":
                                skipped_count += 1
                            else:
                                success_count += 1
                            progress.advance(task)
                        else:
                            failed_count += 1
                            progress.update(task, description=f"[red]{step.name} (failed)")
                            console.print(f"  [red]✗ Step failed:[/red] {step.error}", err=True)
                            
                            if stop_on_failure:
                                self.status = "failed"
                                self.execution_time = time.time() - start_time
                                return False
                        
                        completed_steps += 1
                
                elif group_type == "parallel":
                    # Execute parallel steps
                    if verbose:
                        console.print(f"\n[bold magenta]∥ Running {len(steps)} steps in parallel[/bold magenta]")
                    
                    with ThreadPoolExecutor(max_workers=max_workers) as executor:
                        futures = {
                            executor.submit(step.execute, context, verbose): step
                            for step in steps
                        }
                        
                        for future in as_completed(futures):
                            step = futures[future]
                            try:
                                success = future.result()
                                
                                if success:
                                    success_count += 1
                                else:
                                    failed_count += 1
                                    console.print(f"  [red]✗ {step.name} failed:[/red] {step.error}", err=True)
                                    
                                    if stop_on_failure:
                                        self.status = "failed"
                                        self.execution_time = time.time() - start_time
                                        return False
                                
                                completed_steps += 1
                                progress.advance(task)
                                
                            except Exception as e:
                                failed_count += 1
                                console.print(f"  [red]✗ {step.name} exception:[/red] {e}", err=True)
                                
                                if stop_on_failure:
                                    self.status = "failed"
                                    self.execution_time = time.time() - start_time
                                    return False
        
        # Determine final status
        self.execution_time = time.time() - start_time
        
        if failed_count == 0:
            self.status = "success"
        elif success_count > 0:
            self.status = "partial"
        else:
            self.status = "failed"
        
        if verbose:
            console.print(f"\n[bold green]✓ Workflow complete[/bold green]: "
                         f"{success_count} succeeded, {failed_count} failed, {skipped_count} skipped")
            console.print(f"   [dim]Total time: {self.execution_time:.2f}s[/dim]")
        
        return failed_count == 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON output"""
        return {
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
            "status": self.status,
            "execution_time": round(self.execution_time, 3),
            "steps": [step.to_dict() for step in self.steps],
            "summary": {
                "total": len(self.steps),
                "success": sum(1 for s in self.steps if s.status == "success"),
                "failed": sum(1 for s in self.steps if s.status == "failed"),
                "skipped": sum(1 for s in self.steps if s.status == "skipped")
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
                params=step_data.get("params", {}),
                condition=step_data.get("condition"),
                retry=step_data.get("retry", 0),
                timeout=step_data.get("timeout", 300),
                parallel=step_data.get("parallel", False),
                output_var=step_data.get("output_var")
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
                    "params": step.params,
                    **({"condition": step.condition} if step.condition else {}),
                    **({"retry": step.retry} if step.retry else {}),
                    **({"timeout": step.timeout} if step.timeout != 300 else {}),
                    **({"parallel": step.parallel} if step.parallel else {}),
                    **({"output_var": step.output_var} if step.output_var else {}),
                }
                for step in self.steps
            ]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)


# CLI Commands (Phase 4 enhanced)

@click.group()
def workflow():
    """Workflow management commands (Phase 4: Advanced Features)"""
    pass


@workflow.command()
@click.option('--file', '-f', 'workflow_file', required=True, help='YAML workflow file')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output with progress bar')
@click.option('--continue-on-failure', is_flag=True, help='Continue even if a step fails')
@click.option('--json', 'output_json', is_flag=True, help='Output results as JSON')
@click.option('--max-workers', type=int, default=4, help='Max parallel workers')
@click.option('--var', 'variables', multiple=True, help='Set variable (KEY=value)')
def run(workflow_file: str, verbose: bool, continue_on_failure: bool, 
        output_json: bool, max_workers: int, variables: tuple):
    """Run a workflow from YAML file"""
    
    # Load workflow
    try:
        workflow = Workflow.from_yaml(workflow_file)
    except Exception as e:
        click.echo(f"Error loading workflow: {e}", err=True)
        if output_json:
            click.echo(json.dumps({"success": False, "error": str(e)}))
        return
    
    # Set initial variables
    context = ExecutionContext()
    for var in variables:
        if '=' in var:
            key, value = var.split('=', 1)
            context.set_variable(key.strip(), value.strip())
    
    # Execute workflow
    success = workflow.execute(
        verbose=verbose,
        stop_on_failure=not continue_on_failure,
        max_workers=max_workers
    )
    
    # Output results
    if output_json:
        click.echo(json.dumps(workflow.to_dict(), indent=2))
    else:
        if success or workflow.status == "partial":
            click.echo(f"\n✓ Workflow '{workflow.name}' completed")
            if workflow.status == "partial":
                summary = workflow.to_dict()['summary']
                click.echo(f"  (Partial: {summary['success']} succeeded, "
                          f"{summary['failed']} failed, {summary['skipped']} skipped)")
        else:
            click.echo(f"\n✗ Workflow '{workflow.name}' failed", err=True)


@workflow.command()
@click.option('--file', '-f', 'workflow_file', required=True, help='YAML workflow file')
@click.option('--json', 'output_json', is_flag=True, help='Output as JSON')
def validate(workflow_file: str, output_json: bool):
    """Validate a workflow YAML file"""
    
    try:
        workflow = Workflow.from_yaml(workflow_file)
        
        # Basic validation
        errors = []
        warnings = []
        
        if not workflow.name:
            errors.append("Workflow name is required")
        if not workflow.steps:
            errors.append("At least one step is required")
        
        for i, step in enumerate(workflow.steps):
            if not step.action:
                errors.append(f"Step {i+1} ({step.name}): action is required")
            
            # Check for variable references without definition
            params_str = json.dumps(step.params)
            if '$' in params_str:
                warnings.append(f"Step {i+1} ({step.name}): contains variable references")
            
            # Validate retry count
            if step.retry < 0:
                errors.append(f"Step {i+1} ({step.name}): retry must be >= 0")
            
            # Validate timeout
            if step.timeout <= 0:
                errors.append(f"Step {i+1} ({step.name}): timeout must be > 0")
        
        if output_json:
            result = {
                "valid": len(errors) == 0,
                "errors": errors,
                "warnings": warnings,
                "workflow": {
                    "name": workflow.name,
                    "steps": len(workflow.steps),
                    "parallel_steps": sum(1 for s in workflow.steps if s.parallel),
                    "conditional_steps": sum(1 for s in workflow.steps if s.condition)
                }
            }
            click.echo(json.dumps(result, indent=2))
        else:
            if errors:
                click.echo("[red]✗ Validation failed:[/red]")
                for error in errors:
                    click.echo(f"  - {error}")
            else:
                click.echo("[green]✓ Workflow is valid[/green]")
                click.echo(f"  Name: {workflow.name}")
                click.echo(f"  Steps: {len(workflow.steps)}")
                
                if workflow.to_dict()['workflow'].get('parallel_steps', 0) > 0:
                    click.echo(f"  Parallel steps: {workflow.to_dict()['workflow']['parallel_steps']}")
                if workflow.to_dict()['workflow'].get('conditional_steps', 0) > 0:
                    click.echo(f"  Conditional steps: {workflow.to_dict()['workflow']['conditional_steps']}")
            
            if warnings:
                click.echo("\n[yellow]Warnings:[/yellow]")
                for warning in warnings:
                    click.echo(f"  - {warning}")
        
    except Exception as e:
        if output_json:
            click.echo(json.dumps({"valid": False, "error": str(e)}))
        else:
            click.echo(f"[red]✗ Validation error:[/red] {e}", err=True)


@workflow.command()
@click.option('--json', 'output_json', is_flag=True, help='Output as JSON')
def list_templates(output_json: bool):
    """List available workflow templates"""
    
    templates = [
        {
            "name": "document-conversion",
            "description": "Convert documents between formats",
            "steps": 3,
            "features": ["sequential"]
        },
        {
            "name": "batch-process",
            "description": "Process multiple documents in parallel",
            "steps": 5,
            "features": ["parallel", "variables"]
        },
        {
            "name": "content-pipeline",
            "description": "Extract, transform, and publish content",
            "steps": 7,
            "features": ["conditional", "variables", "retry"]
        },
        {
            "name": "ci-cd-pipeline",
            "description": "Continuous integration and deployment",
            "steps": 6,
            "features": ["parallel", "conditional", "retry"]
        }
    ]
    
    if output_json:
        click.echo(json.dumps({"templates": templates}, indent=2))
    else:
        click.echo("\n[bold]Available Workflow Templates:[/bold]\n")
        for tpl in templates:
            features = ", ".join(tpl['features'])
            click.echo(f"  • [cyan]{tpl['name']}[/cyan]")
            click.echo(f"    {tpl['description']}")
            click.echo(f"    Steps: {tpl['steps']} | Features: {features}\n")


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
                    "params": {"file": "input.docx", "json": True},
                    "output_var": "doc_content"
                },
                {
                    "name": "Convert to Markdown",
                    "action": "openclaw doc convert",
                    "params": {"input": "docx", "output": "markdown", "file": "input.docx", "output-file": "output.md"}
                },
                {
                    "name": "Verify output",
                    "action": "shell",
                    "params": {"command": "wc -l output.md"},
                    "output_var": "line_count"
                }
            ]
        },
        "batch-process": {
            "name": "Batch Document Processing",
            "description": "Process multiple documents in parallel",
            "steps": [
                {
                    "name": "List files",
                    "action": "shell",
                    "params": {"command": "ls *.md"},
                    "output_var": "file_list"
                },
                {
                    "name": "Process file 1",
                    "action": "shell",
                    "params": {"command": "cat file1.md"},
                    "parallel": True
                },
                {
                    "name": "Process file 2",
                    "action": "shell",
                    "params": {"command": "cat file2.md"},
                    "parallel": True
                },
                {
                    "name": "Merge results",
                    "action": "shell",
                    "params": {"command": "cat file1.md file2.md > combined.md"}
                }
            ]
        },
        "content-pipeline": {
            "name": "Content Pipeline with Conditions",
            "description": "Extract, transform, and publish with conditional logic",
            "steps": [
                {
                    "name": "Set environment",
                    "action": "set",
                    "params": {"name": "env", "value": "production"}
                },
                {
                    "name": "Extract content",
                    "action": "shell",
                    "params": {"command": "cat source.md"},
                    "output_var": "content"
                },
                {
                    "name": "Transform if production",
                    "action": "shell",
                    "params": {"command": "echo 'Optimizing for production...'"},
                    "condition": "${env} == production"
                },
                {
                    "name": "Publish",
                    "action": "shell",
                    "params": {"command": "cp output.md published/"},
                    "retry": 2,
                    "timeout": 60
                }
            ]
        },
        "ci-cd-pipeline": {
            "name": "CI/CD Pipeline",
            "description": "Continuous integration and deployment workflow",
            "steps": [
                {
                    "name": "Checkout code",
                    "action": "shell",
                    "params": {"command": "git pull"}
                },
                {
                    "name": "Install dependencies",
                    "action": "shell",
                    "params": {"command": "pip install -r requirements.txt"},
                    "retry": 2
                },
                {
                    "name": "Run tests",
                    "action": "shell",
                    "params": {"command": "pytest tests/"},
                    "parallel": True
                },
                {
                    "name": "Build",
                    "action": "shell",
                    "params": {"command": "python setup.py build"},
                    "condition": "${test_passed} == true"
                },
                {
                    "name": "Deploy",
                    "action": "shell",
                    "params": {"command": "deploy.sh"},
                    "condition": "${env} == production",
                    "retry": 3
                }
            ]
        }
    }
    
    if name not in templates:
        click.echo(f"[red]Unknown template:[/red] {name}", err=True)
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
    click.echo(f"[green]✓[/green] Workflow initialized from template '{name}'")
    click.echo(f"  Saved to: {output}")


@workflow.command()
@click.option('--name', '-n', required=True, help='Workflow name')
@click.option('--description', '-d', default='', help='Workflow description')
@click.option('--output', '-o', default='workflow.yml', help='Output YAML file')
def create(name: str, description: str, output: str):
    """Create a new workflow interactively"""
    
    workflow = Workflow(name=name, description=description)
    
    click.echo(f"Creating workflow: [cyan]{name}[/cyan]")
    click.echo("Add steps (empty action to finish):\n")
    
    step_num = 1
    while True:
        click.echo(f"\n[bold]Step {step_num}[/bold]")
        action = click.prompt("Action (e.g., 'openclaw doc read' or 'shell' or 'set')", default="")
        
        if not action:
            break
        
        step_name = click.prompt("Step name", default=f"Step {step_num}")
        
        # Parse parameters
        params = {}
        click.echo("Enter parameters (key=value, empty to finish):")
        while True:
            param = click.prompt("  Param", default="")
            if not param:
                break
            if '=' in param:
                key, value = param.split('=', 1)
                try:
                    params[key.strip()] = json.loads(value.strip())
                except json.JSONDecodeError:
                    params[key.strip()] = value.strip()
        
        # Advanced options
        condition = click.prompt("Condition (e.g., '\${var} == value', empty for none)", default="")
        retry = click.prompt("Retry count", default=0, type=int)
        timeout = click.prompt("Timeout (seconds)", default=300, type=int)
        parallel = click.prompt("Run in parallel? (y/n)", default="n").lower() == 'y'
        output_var = click.prompt("Output variable name (empty for none)", default="")
        
        step = WorkflowStep(
            name=step_name,
            action=action,
            params=params,
            condition=condition if condition else None,
            retry=retry,
            timeout=timeout,
            parallel=parallel,
            output_var=output_var if output_var else None
        )
        
        workflow.add_step(step)
        step_num += 1
    
    # Save workflow
    workflow.to_yaml(output)
    click.echo(f"\n[green]✓[/green] Workflow saved to: [cyan]{output}[/cyan]")


# Example workflows for demonstration

@workflow.command()
def demo():
    """Run a demo workflow to showcase features"""
    
    demo_yaml = """
name: Phase 4 Feature Demo
description: Demonstrates conditional execution, parallel steps, variables, and retry

steps:
  - name: Set environment variable
    action: set
    params:
      name: environment
      value: development
    output_var: env
  
  - name: This always runs
    action: shell
    params:
      command: echo "Starting workflow..."
  
  - name: Conditional step (only in production)
    action: shell
    params:
      command: echo "Production mode enabled!"
    condition: "${environment} == production"
  
  - name: Parallel step 1
    action: shell
    params:
      command: 'echo "Parallel task 1" && sleep 1'
    parallel: true
  
  - name: Parallel step 2
    action: shell
    params:
      command: 'echo "Parallel task 2" && sleep 1'
    parallel: true
  
  - name: Retry example
    action: shell
    params:
      command: echo "This might fail but will retry"
    retry: 2
  
  - name: Variable interpolation
    action: shell
    params:
      command: 'echo "Environment is: ${environment}"'
"""
    
    # Write demo workflow
    demo_path = "/tmp/demo-workflow.yml"
    with open(demo_path, 'w') as f:
        f.write(demo_yaml)
    
    click.echo(f"[cyan]Demo workflow created:[/cyan] {demo_path}")
    click.echo("\nRun it with:")
    click.echo(f"  openclaw workflow run -f {demo_path} -v\n")
