from __future__ import annotations

import sys

from eldritch.core.context import EldritchContext


def main() -> None:
    """This function is the main entry point of the eldritch library."""
    ctx = EldritchContext()
    ctx.command_line(sys.argv[1:])
