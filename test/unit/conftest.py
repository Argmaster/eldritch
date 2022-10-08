from __future__ import annotations

import pytest

from eldritch.core.context import EldritchContext


@pytest.fixture()
def ctx() -> EldritchContext:
    """Fixture which provides context object."""
    return EldritchContext()
