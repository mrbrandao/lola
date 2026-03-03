"""
prompts:
    Interactive terminal prompt helpers using InquirerPy.

Provides keyboard-navigable selection prompts for:
- Checking whether stdin is a real terminal (is_interactive)
- Selecting one or more AI assistants (multi-select checkbox)
- Selecting a single module from a list (single-select)
- Selecting a marketplace by name from a list (single-select)
- Selecting a marketplace when a module name conflicts across several (single-select)

All functions return None / [] when the user cancels, so callers can raise
SystemExit(130) to signal a user-initiated cancellation.
"""

import sys

from InquirerPy import inquirer
from InquirerPy.base.control import Choice


def is_interactive() -> bool:
    """Return True when stdin is connected to a real TTY (not piped or CI)."""
    return sys.stdin.isatty()


def select_assistants(available: list[str]) -> list[str]:
    """
    Show a multi-select checkbox for AI assistants.

    If only one assistant is available it is returned immediately without
    prompting.  Returns a (possibly empty) list of selected assistant names;
    an empty list means the user cancelled or deselected everything.
    """
    if len(available) == 1:
        return list(available)

    result = inquirer.checkbox(  # type: ignore[attr-defined]
        message="Select assistants to install to (Space to toggle, Enter to confirm):",
        choices=available,
    ).execute()
    return result if result is not None else []


def select_module(modules: list[str]) -> str | None:
    """
    Show a single-select list for choosing a module.

    If only one module is available it is returned immediately without
    prompting.  Returns the selected module name, or None if cancelled.
    """
    if len(modules) == 1:
        return modules[0]

    result = inquirer.select(  # type: ignore[attr-defined]
        message="Select module:",
        choices=modules,
    ).execute()
    return str(result) if result is not None else None


def select_marketplace_name(names: list[str]) -> str | None:
    """
    Show a single-select list for choosing a marketplace by name.

    Always prompts, even when only one marketplace is registered, so the user
    must explicitly confirm before a destructive action proceeds.
    Returns the selected marketplace name, or None if cancelled.
    """
    result = inquirer.select(  # type: ignore[attr-defined]
        message="Select marketplace:",
        choices=names,
    ).execute()
    return str(result) if result is not None else None


def select_installations(
    installations: list[tuple[str, str, str]],
) -> list[tuple[str, str, str]]:
    """
    Show a multi-select checkbox for (project_path, assistant, label) tuples.

    Returns the selected installations; an empty list means the user cancelled
    or deselected everything.
    """
    choices = [
        Choice(value=(project, assistant, label), name=label)
        for project, assistant, label in installations
    ]
    result = inquirer.checkbox(  # type: ignore[attr-defined]
        message="Select installations to uninstall (Space to toggle, Enter to confirm):",
        choices=choices,
    ).execute()
    return result if result is not None else []


def select_marketplace(matches: list[tuple[dict, str]]) -> str | None:
    """
    Show a single-select list for marketplace conflict resolution.

    matches: list of (module_dict, marketplace_name) tuples.
    Returns the chosen marketplace name, or None if cancelled.
    """
    choices = [
        Choice(
            value=marketplace_name,
            name=(
                f"@{marketplace_name}/{module.get('name', '?')} "
                f"v{module.get('version', '?')} \u2014 {module.get('description', '')}"
            ),
        )
        for module, marketplace_name in matches
    ]
    result = inquirer.select(  # type: ignore[attr-defined]
        message="Module found in multiple marketplaces. Select one:",
        choices=choices,
    ).execute()
    return str(result) if result is not None else None
