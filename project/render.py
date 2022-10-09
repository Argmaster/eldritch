from __future__ import annotations

from typing import List

from eldritch.render import File, Template

ENTRIES: List[File] = [
    File(template=Template("pyproject.toml.jinja2"), destination="pyproject.toml"),
]
