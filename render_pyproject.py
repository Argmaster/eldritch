from pathlib import Path

import jinja2
import tomlkit

dotproject = Path.cwd() / ".project"

with open(dotproject / "metadata.toml", encoding="utf-8") as file:
    metadata = tomlkit.load(file)

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(dotproject), autoescape=jinja2.select_autoescape()
)

template = env.get_template("templates/pyproject.toml.jinja2")
out = template.render(metadata=metadata.unwrap())

(dotproject / "out.toml").write_text(out)
