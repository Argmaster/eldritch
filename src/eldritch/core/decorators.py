"""This module contain generic decorators which can be used across code base and are not
tight to any specific component."""
from __future__ import annotations

from pathlib import Path
from typing import Callable, TypeVar

from typing_extensions import ParamSpec

ParamT = ParamSpec("ParamT")
ReturnT = TypeVar("ReturnT")


def on_return_mkdir(function: Callable[ParamT, Path]) -> Callable[ParamT, Path]:
    """This is a decorator which will create directory which path is returned by
    function.

    Parameters
    ----------
    function : Callable[ParamT, ReturnT]
        Function which returns Path.

    Returns
    -------
    Callable[ParamT, ReturnT]
        Transparent function wrapper.

    """

    def wrapper(*args: ParamT.args, **kwargs: ParamT.kwargs) -> Path:
        value = function(*args, **kwargs)
        assert isinstance(value, Path), value
        value.mkdir(0o777, True, True)
        return value

    return wrapper


def on_return_mkfile(function: Callable[ParamT, Path]) -> Callable[ParamT, Path]:
    """This is a decorator which will create file which path is returned by function.

    Parameters
    ----------
    function : Callable[ParamT, ReturnT]
        Function which returns Path.

    Returns
    -------
    Callable[ParamT, ReturnT]
        Transparent function wrapper.

    """

    def wrapper(*args: ParamT.args, **kwargs: ParamT.kwargs) -> Path:
        value = function(*args, **kwargs)
        assert isinstance(value, Path), value
        value.parent.mkdir(0o777, True, True)
        value.touch(0o777, True)
        return value

    return wrapper
