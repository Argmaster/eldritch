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
from pathlib import Path
from typing import Any, Optional, Type, TypeVar

from .decorators import on_return_mkdir

__all__ = ["SingletonMixin"]


class _SingletonMeta(ABCMeta):

    __instance__: Optional[_SingletonMeta]

    def __new__(
        cls: Type[_SingletonMeta],
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, Any],
        **kwargs: Any,
    ) -> _SingletonMeta:
        # Set placeholder for singleton instance, otherwise can not be assigned
        namespace["__instance__"] = None
        # Instantiate class object
        new_class = super().__new__(cls, name, bases, namespace, **kwargs)
        # Ensure instance container was correctly set
        assert hasattr(new_class, "__instance__")
        return new_class

    def __call__(
        cls: _SingletonMeta,
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
    """This class can be used as mixin class to create singleton design pattern
    compliant subclasses.

    You must be a ware that clas ses inhe riti ng from Sing leto nMix in must not have
    cust om m etac lass .

    """

    __instance__: _SingletonMeta


NoInstanceAllowedMixinT = TypeVar(
    "NoInstanceAllowedMixinT", bound="NoInstanceAllowedMixin"
)


class _NoInstanceAllowedMeta(ABCMeta):
    def __call__(
        cls: _NoInstanceAllowedMeta, *_: Any, **__: Any
    ) -> _NoInstanceAllowedMeta:
        raise AssertionError("No instances allowed.")


class NoInstanceAllowedMixin(  # pylint: disable=too-few-public-methods
    metaclass=_SingletonMeta
):
    """This class can be used to forbid creation of instances of class which inherits
    from this.

    It m akes clas s work only as a name spac e.

    """

    def __init__(self, *_: Any, **__: Any) -> None:
        raise AssertionError("No instances allowed.")

    def __new__(
        cls: Type[NoInstanceAllowedMixinT], *_: Any, **__: Any
    ) -> NoInstanceAllowedMixinT:
        raise AssertionError("No instances allowed.")


class DirsMixin:
    """This mixin provides getters for commonly referenced paths in project."""

    python_project_dir: Path

    @property
    def local(self) -> LocalDirs:
        """This property contains LocalDirs object using path to this project."""
        return LocalDirs(self.python_project_dir)


class LocalDirs:
    """This mixin provides getters for commonly referenced local paths in project."""

    def __init__(self, python_project_dir: Path) -> None:
        self._python_project_dir = python_project_dir

    @property
    @on_return_mkdir
    def dot_project(self) -> Path:
        """This property contains path to `.project` folder of Python project."""
        return self._python_project_dir / ".project"

    @property
    @on_return_mkdir
    def scripts(self) -> Path:
        """This property contains path to `scripts` folder of Python project."""
        return self._python_project_dir / "scripts"

    @property
    @on_return_mkdir
    def docs(self) -> Path:
        """This property contains path to `docs` folder of Python project."""
        return self._python_project_dir / "docs"

    @property
    @on_return_mkdir
    def test(self) -> Path:
        """This property contains path to `test` folder of Python project."""
        return self._python_project_dir / "test"

    @property
    @on_return_mkdir
    def test_unit_subdir(self) -> Path:
        """This property contains path to `test/unit` folder of Python project."""
        return self._python_project_dir / "test" / "unit"

    @property
    @on_return_mkdir
    def test_integration_subdir(self) -> Path:
        """This property contains path to `test/integration` folder of Python
        project."""
        return self._python_project_dir / "test" / "integration"

    @property
    @on_return_mkdir
    def test_e2e_subdir(self) -> Path:
        """This property contains path to `test/e2e` folder of Python project."""
        return self._python_project_dir / "test" / "e2e"

    @property
    @on_return_mkdir
    def src(self) -> Path:
        """This property contains path to `src` folder of Python project."""
        return self._python_project_dir / "src"
