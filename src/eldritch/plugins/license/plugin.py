"""This module contains implementation of license plugin for eldritch.

This plugin allows you to create license files, replace license and fill missing license
notices in code files.

"""
from __future__ import annotations

from typing import Optional

import click

from eldritch.core.context import EldritchContext
from eldritch.core.plugin import EldritchPluginImpl
from eldritch.plugins.license.cli import LicenseCLI

from .api import LicenseAPI


class LicensePlugin(EldritchPluginImpl):
    """This class implements."""

    @EldritchPluginImpl.hookimpl
    def on_cli_create_hook(self, ctx: EldritchContext) -> None:
        @ctx.command_line.group(name="license")
        def _license() -> int:
            """Groups license related operations."""

            return 0

        @_license.command("list")
        def _list() -> int:
            """List all available licenses."""
            return LicenseCLI().list()

        @_license.command("use")
        @click.option(
            "--name",
            "-n",
            required=False,
            type=click.Choice(LicenseAPI().license_names),
        )
        def _use(name: Optional[str]) -> int:
            """Select license and copy its files to your project."""
            return LicenseCLI().use(name)
