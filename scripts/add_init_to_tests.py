from pathlib import Path

TEST = Path.cwd() / "test"

for path in TEST.rglob("**"):
    init_file = path / "__init__.py"
    if not init_file.exists():
        init_file.touch(0o777, True)
