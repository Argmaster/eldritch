"""This module contains utilities connected with `project` directory."""
from __future__ import annotations

from pathlib import Path

from eldritch import assets

from .decorators import on_return_mkdir, on_return_mkfile


@on_return_mkfile(assets.get_asset("metadata.toml"))
def get_metadata_path() -> Path:
    """Return path to `metadata.toml` in `.project` in current working directory."""
    return get_dot_project_path() / "metadata.toml"


@on_return_mkdir()
def get_dot_project_path() -> Path:
    """Return path to `.project` dir in current working directory."""
    return Path.cwd() / ".project"
