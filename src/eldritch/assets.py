from __future__ import annotations

from pathlib import Path

ASSETS_DIR = Path(__file__).parent / 'assets'


def get_asset(name: str) -> bytes:
    """Get content of asset as bytes.

    Parameters
    ----------
    name : str
        Asset name.

    Returns
    -------
    bytes
        Asset content (raw).

    """
    return (ASSETS_DIR / name).read_bytes()
