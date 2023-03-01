"""Utility functions."""
from __future__ import annotations

from typing import TYPE_CHECKING

import requests
from bs4 import BeautifulSoup, Tag
from pydantic import HttpUrl, parse_obj_as

if TYPE_CHECKING:
    from re import Match

_UA = """
Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)
Chrome/110.0.0.0 Safari/537.36
""".strip().replace(
    "\n",
    " ",
)

_REQUESTS_TIMEOUT = 10
_REQUESTS_HEADERS = {
    "User-Agent": _UA,
}


def get_captured_value(m: Match[str] | None, group_name: str) -> str | None:
    """Get the captured value with the group name from the match object.

    Parameters
    ----------
    m : Match | None
        matched result
    group_name : str | int
        group name

    Returns
    -------
    str | None
        return matched string if exists, otherwise None
    """
    if m is None or group_name not in (d := m.groupdict()):
        return None

    return str(d[group_name])


def get_source(url: str) -> BeautifulSoup | None:
    """Get the source as a BeautifulSoup object.

    Parameters
    ----------
    url : str
        Web Page URL

    Returns
    -------
    BeautifulSoup | None
        parsed source data of web page
    """
    res = requests.get(url, timeout=_REQUESTS_TIMEOUT, headers=_REQUESTS_HEADERS)
    if not res.ok:
        return None
    return BeautifulSoup(markup=res.content, features="lxml")


def select_one_tag(bs: BeautifulSoup | Tag, selector: str) -> Tag:
    """WIP."""
    res = bs.select_one(selector)

    if res is None:
        raise ValueError(res)

    return res


def parse_obj_as_url(url: str) -> HttpUrl:
    """WIP."""
    return parse_obj_as(HttpUrl, url)  # type: ignore[no-any-return]
