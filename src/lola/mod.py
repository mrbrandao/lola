"""
mod:
    Module management commands for lola modules
"""

from pathlib import Path
import yaml
import click
from lola.layout import console


def load_modules(modules_dir: Path) -> list[dict]:
    """
    Load lola modules from lolamod.yml file.

    Args:
        modules_dir: Path to the modules directory

    Returns:
        List of lola module dictionaries
    """
    lolamod_file = modules_dir / "lolamod.yml"

    if not lolamod_file.exists():
        return []

    with open(lolamod_file, 'r') as f:
        data = yaml.safe_load(f) or {}

    return data.get('lolas', [])


@click.group(name='mod')
def mod():
    """
    Manage lola modules
    """
    pass


@mod.command(name='ls')
@click.option(
    '-p', '--path',
    'modules_dir',
    default='./modules',
    type=click.Path(exists=False, path_type=Path),
    help='Directory containing lola modules'
)
def list_modules(modules_dir: Path):
    """
    List available lola modules
    """
    if not modules_dir.exists():
        console.print(f"[yellow]Modules directory not found: {modules_dir}[/yellow]")
        return

    modules = load_modules(modules_dir)

    if not modules:
        console.print("[yellow]No modules found[/yellow]")
        return

    console.print(f"[bold]Found {len(modules)} module(s):[/bold]\n")

    for idx, module in enumerate(modules, 1):
        name = module.get('name', 'Unnamed')
        description = module.get('desc') or module.get('description', 'No description')
        module_path = module.get('path', '')
        assets = module.get('assets', [])

        console.print(f"[cyan]{idx}. {name}[/cyan]")
        console.print(f"   {description}")
        if module_path:
            console.print(f"   Path: {module_path}")
        console.print(f"   Assets: {len(assets)}")
        console.print()
