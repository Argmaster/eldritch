"""Copyright 2022 Krzysztof Wiśniewski <argmaster.world@gmail.com>

This file is part of Eldritch.
https://github.com/Argmaster/Eldritch

Eldritch is free software: you can redistribute it and/or modify it under
the terms of the GNU Lesser General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option)
any later version.

Eldritch is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
details.

You should have received a copy of the GNU Lesser General Public License
along with Eldritch. If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import annotations

from pluggy import HookspecMarker

from eldritch.core import EldritchCLI

hookspec = HookspecMarker("eldritch")


@hookspec
def extend_command_line(
    cli: EldritchCLI,  # pylint: disable=unused-argument
) -> None:
    """This hook is used to collect command line commands. Implementing it
    allows you to extend command line interface of Eldritch.

    Parameters
    ----------
    cli : EldritchCLI
        Eldritch command line app object.
    """
