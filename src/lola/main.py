"""
main:
    is the main script execution module for commands and flags
"""

import click
from lola.layout import console
from . import __version__
from .mod import mod


def ver():
    """
    Show version
    """
    console.print(__version__)

@click.group(invoke_without_command=True, no_args_is_help=True)
@click.option('-v','--version', is_flag=True, help="Show version")
@click.pass_context
def main(ctx, version):
    """
    lola:
    is a simple CLI script that aims to manage Lazy Context Modules for LLMs
    tied to Agents that has basic IO Read support and bash script execution,
    usually found on AI code assitants
    """
    ctx.ensure_object(dict)
    if version:
        ver()


# Register commands
main.add_command(mod)
