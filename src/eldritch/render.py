"""This module contains classes used for template based file creation."""
from __future__ import annotations

from pathlib import Path
from typing import List, Optional, TypeVar

import jinja2

from eldritch import context

TemplateT = TypeVar("TemplateT", bound="Template")

ENTRIES: List[File] = []

class Template:
    """Represents template object which can be rendered."""

    def __init__(self, name: str) -> None:
        self._name = name
        self._env: Optional[jinja2.Environment] = None
        self._template: Optional[jinja2.Template] = None
        self._content: Optional[str] = None

    def bind(self: TemplateT, env: jinja2.Environment) -> TemplateT:
        """Bind template to specific environment.

        Parameters
        ----------
        env : jinja2.Environment
            Environment to bind to.

        """
        self._env = env
        self._template = env.get_template(self._name)
        return self

    def render(self: TemplateT, ctx: context.Context) -> TemplateT:
        """Render template content.

        Parameters
        ----------
        context : context.Context
            Context to use.

        Returns
        -------
        str
            Rendered template.

        """
        assert self._template is not None
        self._content = self._template.render(**ctx.asdict())
        return self

    def get_content(self) -> str:
        """Acquire rendered content.

        Returns
        -------
        str
            Rendered content.

        """
        assert self._content is not None
        return self._content


FileT = TypeVar("FileT", bound="File")


class File:
    """Represents file which can be recreated by rendering template."""

    def __init__(self, *, template: Template, destination: str | Path) -> None:
        self._template = template
        self._destination = Path(destination)

    def render(self: FileT, env: jinja2.Environment, ctx: context.Context) -> FileT:
        """Render file template content.

        Parameters
        ----------
        env : jinja2.Environment
            Environment from which template should be loaded.
        ctx : context.Context
            Template rendering context.

        Returns
        -------
        File
            This file object.

        """
        self._template.bind(env)
        self._template.render(ctx)
        return self

    def write(self) -> None:
        """Write rendered file content to destination."""
        self._destination.write_text(self._template.get_content(), encoding="utf-8")
