""".. include:: ../README.md"""

from __future__ import annotations

import importlib.metadata

from .parse import Parsers, parse

try:
    __version__ = importlib.metadata.version(__name__)
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.0.0"

__all__ = (
    "Parsers",
    "__version__",
    "parse",
)
