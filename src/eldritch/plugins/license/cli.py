from __future__ import annotations

from enum import IntEnum
from typing import Dict, Optional, cast

import inquirer

from eldritch.core.use_context import UseContext
from eldritch.plugins.license.api import LicenseAPI


class ExitCode(IntEnum):
    """This enum contains possible exit codes of license cli."""

    SUCCESS = 0


class LicenseCLI(UseContext):
    """This class is a namespace for Eldritch license plugin CLI."""

    def __init__(self) -> None:
        super().__init__()
        self.api = LicenseAPI()

    def list(self) -> ExitCode:
        """This method can be used to list all available licenses."""
        self.ctx.console.print()
        self.ctx.console.print("[green]Available licenses:")

        for license_ob in self.api.licenses:
            self.ctx.console.print(f"- {license_ob}")

        self.ctx.console.print()

        return ExitCode.SUCCESS

    def use(self, license_name: Optional[str]) -> ExitCode:
        """Add source file license notice to files without it."""
        if license_name is None:
            alias = "name"

            questions = [
                inquirer.List(
                    alias,
                    message="Which license?",
                    choices=self.api.license_names,
                ),
            ]
            answers = cast(Dict[str, str], inquirer.prompt(questions))
            license_name = answers.get(alias)

            assert license_name is not None

        self.api.use_license(license_name)

        return ExitCode.SUCCESS
