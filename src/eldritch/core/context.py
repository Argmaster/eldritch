"""This module contains Eldritch context class used for holding runtime context.

Eldritch does not have global context, instead it passes around single EldritchContext
instance which contains all important shared information like configuration or plugin
access.

"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Type, TypeVar, Union

import jinja2
import rich
import rich_click as click
import tomlkit
from pydantic import BaseModel, Field

from eldritch import __version__
from eldritch.core.config import EldritchConfig, load_pyproject
from eldritch.core.plugin_manager import EldritchPluginManager
from eldritch.typing import DepsDictT, IncludeDefT, ScriptDefT


class EldritchContext:
    """This class is used by Eldritch to hold all of its internal execution context."""

    python_project_dir: Path
    pyproject: tomlkit.TOMLDocument
    config: EldritchConfig
    log: logging.Logger
    command_line: click.Group
    plugin_manager: EldritchPluginManager
    console: rich.console.Console
    package_info: PoetryProjectInfo

    def __init__(self, python_project_dir: Optional[Path] = None) -> None:
        self.python_project_dir = python_project_dir or Path.cwd()

        self.console = self._load_console()
        self.pyproject = self._load_pyproject()
        self.package_info = self._load_package_info()
        self.config = self._load_config()
        self.command_line = self._load_command_line()
        self.plugin_manager = self._load_plugin_manager()

        self._register_plugins()
        self._create_command_line()

        self.jinja2_env = self.templates("eldritch")

    def _load_console(self) -> rich.console.Console:
        return rich.console.Console(highlight=False)

    def _load_pyproject(self) -> tomlkit.TOMLDocument:
        return load_pyproject(self.python_project_dir, "pyproject.toml")

    def _load_package_info(self) -> PoetryProjectInfo:
        return PoetryProjectInfo.from_pyproject(self.pyproject)

    def _load_config(self) -> EldritchConfig:
        return EldritchConfig.from_pyproject(self.pyproject)

    def _load_command_line(self) -> click.Group:
        @click.group(invoke_without_command=True, no_args_is_help=True)
        @click.version_option(__version__)
        @click.pass_context
        def main(_: click.Context) -> int:
            """Welcome to Eldritch!"""
            return 0

        return main

    def _load_plugin_manager(self) -> EldritchPluginManager:
        return EldritchPluginManager()

    def _register_plugins(self) -> None:
        for plugin in self.config.plugins:
            self.plugin_manager.register_module(plugin)

    def _create_command_line(self) -> None:
        self.plugin_manager.hook.on_cli_create_hook(ctx=self)  # type: ignore

    def print(self, *args: Any, **kwargs: Any) -> None:
        """Print to the console."""
        return self.console.print(*args, **kwargs)

    def templates(self, package: str) -> jinja2.Environment:
        """Get template environment for package."""
        return jinja2.Environment(
            loader=jinja2.PackageLoader(package), autoescape=jinja2.select_autoescape()
        )

    def __hash__(self) -> int:
        return id(self)


PoetryProjectInfoT = TypeVar("PoetryProjectInfoT", bound="PoetryProjectInfo")


class PoetryProjectInfo(BaseModel):
    """This class is used to wrap contents of `[tool.poetry]` configuration section
    pulled from pyproject.toml of project."""

    name: str = Field(default="")
    version: str = Field(default="")
    description: str = Field(default="")
    license: str = Field(default="")
    authors: List[str] = Field(default_factory=list)
    maintainers: List[str] = Field(default_factory=list)
    readme: Union[str, List[str]] = Field(default="")
    homepage: str = Field(default="")
    repository: str = Field(default="")
    documentation: str = Field(default="")
    keywords: List[str] = Field(default_factory=list)
    classifiers: List[str] = Field(default_factory=list)
    packages: List[Dict[str, str]] = Field(default_factory=list)
    include: IncludeDefT = Field(default_factory=list)
    dependencies: DepsDictT = Field(default_factory=dict)
    group: Dict[str, Dict[str, DepsDictT]] = Field(default_factory=dict)
    scripts: Dict[str, ScriptDefT] = Field(default_factory=dict)
    extras: Dict[str, List[str]] = Field(default_factory=dict)
    plugins: Dict[str, str] = Field(default_factory=dict)
    urls: Dict[str, str] = Field(default_factory=dict)

    class Config:
        allow_mutation: bool = False
        frozen: bool = True
        copy_on_model_validation: Literal["none", "deep", "shallow"] = "none"
        validate_all: bool = True

    @classmethod
    def from_pyproject(
        cls: Type[PoetryProjectInfoT], pyproject: tomlkit.TOMLDocument
    ) -> PoetryProjectInfoT:
        """Extract project info section from pyproject.toml file content.

        Parameters
        ----------
        pyproject : tomlkit.TOMLDocument
            Configuration content loaded with tomlkit.

        Returns
        -------
        EldritchConfig
            Project info wrapper instance.

        """
        eldritch_config_raw = pyproject.get("tool", {}).get("poetry", {})
        return cls.parse_obj(eldritch_config_raw)
