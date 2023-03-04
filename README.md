# pyjlyric: Japanese Lyric Aggregator

[![PyPI](
  <https://img.shields.io/pypi/v/pyjlyric?color=blue>
  )](
  <https://pypi.org/project/pyjlyric/>
) [![Release Package](
  <https://github.com/eggplants/pyjlyric/actions/workflows/release.yml/badge.svg>
  )](
  <https://github.com/eggplants/pyjlyric/actions/workflows/release.yml>
) [![Ghcr](
  <https://ghcr-badge.deta.dev/eggplants/pyjlyric/size>
  )](
  <https://github.com/eggplants/pyjlyric/pkgs/container/pyjlyric/74193340?tag=latest>
)

[![pre-commit.ci status](
  <https://results.pre-commit.ci/badge/github/eggplants/pyjlyric/master.svg>
  )](
  <https://results.pre-commit.ci/latest/github/eggplants/pyjlyric/master>
) [![Maintainability](
  <https://api.codeclimate.com/v1/badges/efdc16e97af8b8914ce9/maintainability>
  )](
  <https://codeclimate.com/github/eggplants/pyjlyric/maintainability>
) [![Test Coverage](
  <https://api.codeclimate.com/v1/badges/efdc16e97af8b8914ce9/test_coverage>
  )](
  <https://codeclimate.com/github/eggplants/pyjlyric/test_coverage>
)

## Supported sites

<https://github.com/eggplants/pyjlyric/issues/4>

## Installation

```sh
pip install git+https://github.com/eggplants/pyjlyric
# or
pip install pyjlyric
```

## Usage

### CLI

```shellsession
$ jrc -h
usage: jrc [-h] [-V] url

get lyric data by URL.

positional arguments:
  url

options:
  -h, --help     show this help message and exit
  -V, --version  show program's version number and exit

supported sites:
  - ...
```

### Library

```python
import pyjlyric

pyjlyric.parse("https://kashinavi.com/song_view.html?155779")
```

Returns:

```python
KashinaviLyricPage(
    title='Life goes on',
    page_url=HttpUrl('https://kashinavi.com/song_view.html?155779', ),
    pageid='155779',
    artist=WithUrlText(
        link=HttpUrl('https://kashinavi.com/artist.html?artist=104498&kashu=King+%26+Prince&start=1', ),
        text='King & Prince'
    ),
    composer='Joacim Persson・Johan Alkenas・SQVARE・Sean Michael Alexander',
    lyricist='木村友威',
    arranger=None,
    lyric_sections=[['Keep it up, keep it up yup'], [...], [..., "Let's live it up"]]
)
```
