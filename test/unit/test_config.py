from __future__ import annotations

import tempfile
from pathlib import Path

from eldritch.config import EldritchConfig, _EldritchConfigMeta


class TestEldritchConfig:
    """This class groups tests of EldritchConfig."""

    example_pyproject: str = """
        [tool.eldritch] # ANCHOR: tool.eldritch
        plugins = [some_plugin]
    """

    def __init__(self) -> None:
        print("INIT")
        self.temp_dir = (
            tempfile.TemporaryDirectory()  # pylint: disable=consider-using-with
        )

        self.tmp_path = Path(self.temp_dir.name)
        self.pyproject_path = self.tmp_path / "pyproject.toml"
        self.pyproject_path.write_text(self.example_pyproject)

        _EldritchConfigMeta.__instance__ = None

    def test_config_load(self) -> None:
        """This test checks if config is correctly loaded."""
        configuration = EldritchConfig()
        print(configuration.plugins)
