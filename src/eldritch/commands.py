from __future__ import annotations

import rich_click as click

from eldritch import __version__


@click.command(no_args_is_help=True)
@click.version_option(__version__)
@click.pass_context
def eldritch(_: click.Context) -> int:
    """"""
    return 0


@click.command()
@click.option("--all", "-a", is_flag=True, help="Render all defined files.")
@click.option("--file", "-f", type=click.Choice(["pyproject.toml"]))
def render() -> int:
    return 1
