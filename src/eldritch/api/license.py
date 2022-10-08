from __future__ import annotations

import shutil
from pathlib import Path
from typing import List, Optional

from eldritch.core.use_context import UseContext, UseContextOnce

THIS_DIR = Path(__file__).parent
THIS_TEMPLATES_DIR = THIS_DIR / "templates"

SCRIPTS_DIR = Path.cwd() / "scripts"
SCRIPTS_TEMPLATES_DIR = SCRIPTS_DIR / "templates"
SCRIPTS_LICENSE_DIR = SCRIPTS_TEMPLATES_DIR / "license"


class LicenseAPI(UseContextOnce):
    """This class is a namespace for Eldritch license plugin API."""

    def __init__(self) -> None:
        super().__init__()
        self.licenses = [License("LGPL-3.0-or-later")]
        self._licenses_dict = {l.name: l for l in self.licenses}

    def use_license(self, name: str) -> None:
        """Move license template file to projects template repository."""
        license_ob = self._licenses_dict[name]
        asserts_dir = THIS_TEMPLATES_DIR / license_ob.namespace

        shutil.rmtree(SCRIPTS_LICENSE_DIR, ignore_errors=True)
        SCRIPTS_LICENSE_DIR.mkdir(0o777, True, True)

        shutil.copytree(asserts_dir, str(SCRIPTS_LICENSE_DIR), dirs_exist_ok=True)

    def generate(self) -> None:
        """Generate license files from template files."""

    @property
    def license_names(self) -> List[str]:
        """This property provides list of license names available."""
        return list(self._licenses_dict.keys())


class License(UseContext):
    """This object represents license in plugin."""

    def __init__(self, name: str, namespace: Optional[str] = None) -> None:
        super().__init__()
        self.name = name
        self.namespace = namespace or name

    def render_notice(self) -> str:
        """Render source file license notice."""

        loader = self.ctx.templates(__name__)
        notice_template = loader.get_template(f"{self.namespace}/NOTICE.jinja2")

        output = notice_template.render(ctx=self.ctx)

        return output

    def render_root_files(self) -> list[str]:
        """Render files which should be in root of repository."""
        return []

    def __str__(self) -> str:
        return self.name
