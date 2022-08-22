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

from abc import ABCMeta
from typing import TYPE_CHECKING, Any, Optional, Type

if TYPE_CHECKING:
    from typing_extensions import Self


__all__ = ["SingletonMixin"]


class _SingletonMeta(ABCMeta):

    __instance__: Optional[_SingletonMeta]

    def __new__(
        cls: type[Self],  # type: ignore
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
        **kwargs: Any,
    ) -> Self:  # type: ignore
        # Set placeholder for singleton instance
        namespace["__instance__"] = None
        # Instantiate class object
        new_class = super().__new__(name, bases, namespace, **kwargs)  # type: ignore
        # Ensure instance container was correctly set
        assert hasattr(new_class, "__instance__")
        return new_class  # type: ignore

    def __call__(  # type: ignore
        cls: Type[_SingletonMeta],  # type: ignore
        *args: Any,
        **kwds: Any,
    ) -> _SingletonMeta:
        # Instantiate class only when instance was not created already
        if cls.__instance__ is None:
            cls.__instance__ = super().__call__(*args, **kwds)
        assert cls.__instance__ is not None, cls
        return cls.__instance__


class SingletonMixin(  # pylint: disable=too-few-public-methods
    metaclass=_SingletonMeta
):
    """This class can be used as mixin class to create singleton
    design pattern compliant subclasses. You must be aware that
    classes inheriting from SingletonMixin must not have custom
    metaclass.
    """
