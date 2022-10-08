"""This module defines objects used for typing among Eldritch codebase."""

from __future__ import annotations

from pathlib import Path
from typing import Callable, Dict, List, TypeVar, Union

from typing_extensions import ParamSpec, TypeAlias

PathLike: TypeAlias = Union[Path, str]
PathOrGetterT: TypeAlias = Union[Callable[[], PathLike], PathLike]

ParamT = ParamSpec("ParamT")
ReturnT = TypeVar("ReturnT")
AnyFunctionT = Callable[ParamT, ReturnT]  # type: ignore

DepsDictT: TypeAlias = Dict[str, Union[str, Dict[str, str]]]
ScriptDefT: TypeAlias = Union[str, Dict[str, Union[str, List[str]]]]
IncludeDefT: TypeAlias = List[
    Union[str, Dict[str, str], Dict[str, Union[str, List[str]]]]
]
