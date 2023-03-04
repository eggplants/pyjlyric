"""Abstract classes."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Self

    from .model import LyricPage


class BaseLyricPageParserError(Exception):
    ...


class BaseLyricPageParser(ABC):
    _test: str

    def __init__(self: Self, url: str) -> None:
        if self.is_valid_url(url):
            self.data = self.parse(url)
            self.url = url

    @staticmethod
    @abstractmethod
    def is_valid_url(url: str) -> bool:
        """Check if the url is valid."""
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def parse(url: str) -> LyricPage:
        """Parse the url page and return the result as LyricPage instance."""
        raise NotImplementedError
