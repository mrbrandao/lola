"""
mod:
    Module management commands for lola modules
"""

from pathlib import Path
from datetime import datetime
import shutil
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
@click.option(
    '-p', '--path',
    'modules_dir',
    default='./modules',
    type=click.Path(exists=False, path_type=Path),
    help='Directory containing lola modules'
)
@click.pass_context
def mod(ctx, modules_dir):
    """
    Manage lola modules
    """
    ctx.ensure_object(dict)
    ctx.obj['modules_dir'] = modules_dir


@mod.command(name='ls')
@click.pass_context
def list_modules(ctx):
    """
    List available lola modules
    """
    modules_dir = ctx.obj['modules_dir']

    if not modules_dir.exists():
        console.print(f"[yellow]Modules directory not found: {modules_dir}[/yellow]")
        return

    modules = load_modules(modules_dir)

    if not modules:
        console.print("[yellow]No modules found[/yellow]")
        return

    console.print(f"[bold]Found {len(modules)} module(s):[/bold]")
    console.print()

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


@mod.command(name='install')
@click.argument('module_name')
@click.option(
    '-d', '--dest',
    'dest_dir',
    default='.',
    type=click.Path(path_type=Path),
    help='Destination directory'
)
@click.pass_context
def install_module(ctx, module_name, dest_dir):
    """
    Install a lola module
    """
    modules_dir = ctx.obj['modules_dir']

    if not modules_dir.exists():
        console.print(f"[red]Modules directory not found: {modules_dir}[/red]")
        return

    # Find module
    modules = load_modules(modules_dir)
    module = None
    for m in modules:
        if m.get('name') == module_name:
            module = m
            break

    if not module:
        console.print(f"[red]Module '{module_name}' not found[/red]")
        return

    # Get module source directory
    module_path = module.get('path', f'./{module_name}')
    source_dir = modules_dir / module_path.replace('./', '')

    if not source_dir.exists():
        console.print(f"[red]Module directory not found: {source_dir}[/red]")
        return

    # Check destination directory
    if dest_dir.exists() and not dest_dir.is_dir():
        console.print(f"[red]Destination is not a directory: {dest_dir}[/red]")
        return

    # Create destination and .lolas directory
    dest_dir.mkdir(parents=True, exist_ok=True)
    lolas_dir = dest_dir / '.lolas' / module_name
    lolas_dir.mkdir(parents=True, exist_ok=True)

    console.print(f"[bold]Installing {module_name}...[/bold]")
    console.print()

    # Copy assets
    assets = module.get('assets', [])
    for asset in assets:
        source_asset = source_dir / asset
        dest_asset = lolas_dir / asset

        if not source_asset.exists():
            console.print(f"[yellow]Asset not found: {asset}[/yellow]")
            continue

        shutil.copytree(source_asset, dest_asset, dirs_exist_ok=True)
        console.print(f"[green]✓ {asset}[/green]")

    # Copy main file if exists
    main_file = module.get('main')
    if main_file:
        source_main = source_dir / main_file
        dest_main = dest_dir / main_file

        if source_main.exists():
            if dest_main.exists():
                backup = dest_dir / f"{dest_main.stem}-{datetime.now().strftime('%Y%m%d')}.bkp"
                shutil.copy2(dest_main, backup)
                console.print(f"[yellow]Backup: {backup.name}[/yellow]")

            shutil.copy2(source_main, dest_main)
            console.print(f"[green]✓ {main_file}[/green]")

    console.print()
    console.print("[bold green]Done![/bold green]")
