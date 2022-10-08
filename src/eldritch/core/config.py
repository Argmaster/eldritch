from __future__ import annotations

from pathlib import Path
from typing import List, Type, TypeVar

import tomlkit
from filelock import FileLock
from pydantic import BaseModel, Extra, Field

from eldritch.typing import PathOrGetterT

EldritchConfigT = TypeVar("EldritchConfigT", bound="EldritchConfig")


class EldritchConfig(BaseModel):

    plugins: List[str] = Field(default_factory=list)

    class Config:
        """This class changes configuration of BaseModel."""

        extra: Extra = Extra.ignore
        validate_all: bool = True
        allow_mutation: bool = False
        frozen: bool = True
        copy_on_model_validation: str = "none"

    @classmethod
    def from_pyproject(
        cls: Type[EldritchConfigT], pyproject: tomlkit.TOMLDocument
    ) -> EldritchConfigT:
        """Extract configuration section from pyproject.toml file content.

        Parameters
        ----------
        pyproject : tomlkit.TOMLDocument
            Configuration content loaded with tomlkit.

        Returns
        -------
        EldritchConfig
            Configuration wrapper instance.

        """
        eldritch_config_raw = pyproject.get("tool", {}).get("eldritch", {})
        return cls.parse_obj(eldritch_config_raw)


def load_pyproject(
    directory: PathOrGetterT = Path.cwd,
    filename: str = "pyproject.toml",
    encoding: str = "utf-8",
) -> tomlkit.TOMLDocument:
    """Load pyproject file content from specified location, by default from current
    working directory (resolved dynamically, every chdir will be taken ito account).

    Parameters
    ----------
    directory : PathOrGetterT, optional
        Path or getter of directory which contains pyproject.toml, by default Path.cwd
    encoding : str, optional
        File encoding to use, by default "utf-8"

    """
    if isinstance(directory, (str, Path)):
        pyproject_directory = Path(directory)

    elif callable(directory):
        # When we allow to pass callable to call, we are make it possible to
        # defer path resolution without placing whole expression in lambda.
        # It also makes dynamic defaults simple to implement without None checks
        pyproject_directory = Path(directory())

    else:
        raise TypeError(f"Unsupported directory source {directory!r}")

    pyproject_file = pyproject_directory / filename
    # Using lock file ensures that multiple instances of eldritch wont mess
    # up pyproject.toml content
    pyproject_lock_file = pyproject_file.with_suffix(".yaml.lock")

    with FileLock(pyproject_lock_file):
        # Minimize lock time by instant loading whole content pyproject
        # file is quite small, wont be high memory overhead
        file_content = pyproject_file.read_text(encoding=encoding)

    # Toml might be expensive to parse and this library is not prioritizing
    # minimal parse times, thus loading it after pyproject.toml is unlocked.
    document = tomlkit.parse(file_content)
    return document
