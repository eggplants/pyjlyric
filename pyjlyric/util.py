"""Utility functions."""
from __future__ import annotations

from typing import TYPE_CHECKING, Literal
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag
from pydantic import HttpUrl, TypeAdapter

from pyjlyric.model import WithUrlText

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


def get_source(
    url: str,
    *,
    data: dict[str, str | int] | None = None,
    method: Literal["get", "post"] | None = "get",
    headers: dict[str, str] | None = None,
    parser: str | None = "lxml",
) -> BeautifulSoup | None:
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
    headers = _REQUESTS_HEADERS if headers is None else dict(_REQUESTS_HEADERS, **headers)

    if method is None or method == "get":
        res = requests.get(url, data=data, timeout=_REQUESTS_TIMEOUT, headers=headers)
    elif method == "post":
        res = requests.post(url, data=data, timeout=_REQUESTS_TIMEOUT, headers=headers)
    else:
        raise ValueError(method)

    if not res.ok:
        return None
    return BeautifulSoup(
        markup=res.content if res.content != b"" else res.text,
        features="lxml" if parser is None else parser,
    )


def select_one_tag(bs: BeautifulSoup | Tag, selector: str) -> Tag:
    """WIP."""
    res = bs.select_one(selector)

    if res is None:
        raise ValueError(res)

    return res


def parse_obj_as_url(url: str, *, base: str | None = None) -> HttpUrl:
    """WIP."""
    if base is not None:
        url = urljoin(base, url)
    return TypeAdapter(HttpUrl).validate_python(url)


def parse_text_with_optional_link(text: str, link: HttpUrl | None) -> WithUrlText | str:
    if link is None:
        return text
    return WithUrlText(text=text, link=link)


def convert_lines_into_sections(lines: list[str]) -> list[list[str]]:
    lyric_sections = []
    now: list[str] = []
    for line in [*lines, ""]:
        if not line:
            if len(now) > 0:
                lyric_sections.append(now)
            now = []
        else:
            now.append(line)
    return lyric_sections
