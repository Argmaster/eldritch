"""This module contain generic decorators which can be used across code base and are not
tight to any specific component."""
from __future__ import annotations

from pathlib import Path
from typing import Callable, TypeVar

from typing_extensions import ParamSpec

ParamT = ParamSpec("ParamT")
ReturnT = TypeVar("ReturnT")


class on_return_mkdir:  # pylint: disable=invalid-name
    """This is a decorator which will create directory which path is returned by
    function."""

    def __call__(self, function: Callable[ParamT, Path]) -> Callable[ParamT, Path]:
        def wrapper(*args: ParamT.args, **kwargs: ParamT.kwargs) -> Path:
            value = function(*args, **kwargs)
            assert isinstance(value, Path), value
            value.mkdir(0o777, True, True)
            return value

        return wrapper


class on_return_mkfile:  # pylint: disable=invalid-name
    """This is a decorator which will create file which path is returned by function."""

    def __init__(self, default_content: bytes = b"", /) -> None:
        self.default_content = default_content

    def __call__(self, function: Callable[ParamT, Path]) -> Callable[ParamT, Path]:
        def wrapper(*args: ParamT.args, **kwargs: ParamT.kwargs) -> Path:
            value = function(*args, **kwargs)
            assert isinstance(value, Path), value

            value.parent.mkdir(0o777, True, True)
            if not value.exists():
                value.write_bytes(self.default_content)

            return value

        return wrapper
