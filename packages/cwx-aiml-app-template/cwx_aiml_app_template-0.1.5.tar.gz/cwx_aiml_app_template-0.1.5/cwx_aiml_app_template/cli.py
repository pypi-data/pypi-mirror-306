# File: cwx_aiml_app_template/cli.py
import click
from rich.console import Console
from rich.panel import Panel
from .generator import create_project_structure

console = Console()

@click.group()
def main():
    """CWX AIML Application Template Generator"""
    pass

@main.command()
@click.argument('project_name')
def init(project_name):
    """Initialize a new AIML project with the standard structure"""
    try:
        create_project_structure(project_name)
        console.print(
            Panel.fit(
                f"✨ Successfully created AIML project: {project_name}",
                title="Success",
                border_style="green",
            )
        )
    except Exception as e:
        console.print(f"[red]Error creating project: {str(e)}[/red]")

if __name__ == '__main__':
    main()
