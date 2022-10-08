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

import importlib
from inspect import isclass

import pluggy

import eldritch.core.plugin


class EldritchPluginManager(pluggy.PluginManager):
    """This class is used by Eldritch to load plug-ins at runtime and use them
    afterwards."""

    def __init__(self) -> None:
        super().__init__(eldritch.api.plugin.NAMESPACE)
        self.add_hookspecs(eldritch.api.plugin.EldritchPluginSpec)

    def register_module(self, module_name: str) -> None:
        """Register plugin defined in module.

        Parameters
        ----------
        module_name : str
            Name of module containing plugin implementation.

        """
        loaded_module = importlib.import_module(module_name)

        for member in loaded_module.__dict__.values():
            if isclass(member) and issubclass(
                member, eldritch.api.plugin.EldritchPluginImpl
            ):
                name = f"{module_name}.{member.__qualname__}"

                self.register(member(), name)
