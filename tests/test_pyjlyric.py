"""Test."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from pyjlyric import Parsers
from pyjlyric.base import BaseLyricPageParserError

if TYPE_CHECKING:
    from pyjlyric.base import BaseLyricPageParser


@pytest.mark.parametrize("parser", Parsers)
def test_validate_valid_url(parser: type[BaseLyricPageParser]) -> None:
    assert parser.is_valid_url(parser._test), (type(parser), parser._test)  # noqa: SLF001


@pytest.mark.parametrize("parser", Parsers)
def test_validate_invalid_url(parser: type[BaseLyricPageParser]) -> None:
    assert not parser.is_valid_url("http://example.com"), type(parser)


@pytest.mark.parametrize("parser", Parsers)
def test_parse_valid_url(parser: type[BaseLyricPageParser]) -> None:
    assert parser.parse(parser._test), type(parser)  # noqa: SLF001


@pytest.mark.parametrize("parser", Parsers)
def test_parse_invalid_url(parser: type[BaseLyricPageParser]) -> None:
    with pytest.raises(BaseLyricPageParserError):
        assert not parser.parse("http://example.com"), type(parser)
