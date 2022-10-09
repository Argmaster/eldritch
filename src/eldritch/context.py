"""This module contains base implementation of context object.

You can extend it to provide additional fields to rendering context.

"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict

import tomlkit

from . import dotproject


@dataclass
class Context:
    """Container for variables used for rendering of templates."""

    metadata: tomlkit.TOMLDocument

    @classmethod
    def create(cls) -> Context:
        """Construct context object.

        Returns
        -------
        Context
            New context object.

        """
        return Context(metadata=cls._load_metadata())

    @classmethod
    def _load_metadata(cls) -> tomlkit.TOMLDocument:
        content = dotproject.get_metadata_path().read_text("utf-8")
        metadata = tomlkit.loads(content)
        return metadata

    def asdict(self) -> Dict[str, Any]:
        """Context variables dict for used rendering.

        Returns
        -------
        Dict[str, Any]
            Namespace dict.

        """
        return asdict(self)
