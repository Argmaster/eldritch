from __future__ import annotations

from eldritch.api.license import LicenseAPI
from eldritch.core.use_context import UseContextOnce


class EldritchAPI(UseContextOnce):
    """This class is a container for eldritch APIs instantiated with specific
    context."""

    license: LicenseAPI
