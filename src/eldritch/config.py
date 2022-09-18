from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, List, Optional, Type, cast

import tomlkit
from filelock import FileLock
from pydantic import BaseModel
from pydantic.main import ModelMetaclass

__all__ = ["EldritchConfig"]


class _EldritchConfigMeta(ModelMetaclass):

    __instance__: Optional[EldritchConfig] = None

    def __new__(
        cls: Type[_EldritchConfigMeta],
        name: str,
        bases: tuple[type, ...],
        attrs: dict[str, Any],
        **kwargs: Any,
    ) -> Type[_EldritchConfigMeta]:
        # We want to create single instance of environment object
        assert _EldritchConfigMeta.__instance__ is None

        new_cls = super().__new__(cls, name, bases, attrs, **kwargs)

        return cast(Type[_EldritchConfigMeta], new_cls)

    def __post_init__(cls) -> None:
        pass

    def __call__(cls, *args: Any, **kwargs: Any) -> EldritchConfig:
        assert not args, args
        assert not kwargs, kwargs
        # Lazy instantiation is necessary as we end up with circular imports otherwise
        if _EldritchConfigMeta.__instance__ is None:
            _EldritchConfigMeta.__instance__ = super().__call__()

        assert _EldritchConfigMeta.__instance__ is not None

        return _EldritchConfigMeta.__instance__


class EldritchConfig(BaseModel, metaclass=_EldritchConfigMeta):
    """This class holds configuration of Eldritch package.
    This class is a singleton."""

    plugins: List[str]

    def __init__(self) -> None:  # pylint: disable=super-init-not-called
        self.reload()

    @property
    def config_path(self) -> Path:
        """This property contains path to configuration file.

        Returns
        -------
        Path
            Path to file.
        """
        return Path.cwd() / "pyproject.toml"

    def reload(self) -> EldritchConfig:
        """This method loads again EldritchConfig from pyproject.toml
        Because EldritchConfig is a singleton, reloading is done in-place.

        Returns
        -------
        EldritchConfig
            Loaded config object.
        """

        document = self._load_content()
        configuration = document.value
        print(configuration)
        super().__init__(**configuration)

        return self

    def _load_content(self) -> tomlkit.TOMLDocument:
        file_path = self.config_path
        lock_file = file_path.parent / f"{file_path.name}.lock"

        with FileLock(lock_file), file_path.open(
            "r", encoding="utf-8"
        ) as file:
            document = tomlkit.load(file)

        logging.debug(
            "Eldritch config was loaded from {0}",
            file_path.absolute(),
        )

        return document
