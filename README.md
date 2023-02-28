# pyjlyric: Japanese Lyric Extractor

<!--
[![PyPI](
  <https://img.shields.io/pypi/v/my-best-python-project?color=blue>
  )](
  <https://pypi.org/project/my-best-python-project/>
) [![Maintainability](
  <https://api.codeclimate.com/v1/badges/e6d94059d1dc7f08d2a4/maintainability>
  )](
  <https://codeclimate.com/github/eggplants/my-best-python-project/maintainability>
) [![Release Package](
  <https://github.com/eggplants/my-best-python-project/actions/workflows/release.yml/badge.svg>
  )](
  <https://github.com/eggplants/my-best-python-project/actions/workflows/release.yml>
)

[![pre-commit.ci status](
  <https://results.pre-commit.ci/badge/github/eggplants/my-best-python-project/master.svg>
  )](
  <https://results.pre-commit.ci/latest/github/eggplants/my-best-python-project/master>
) [![pages-build-deployment](
  <https://github.com/eggplants/my-best-python-project/actions/workflows/pages/pages-build-deployment/badge.svg>
  )](
  <https://github.com/eggplants/my-best-python-project/actions/workflows/pages/pages-build-deployment>
)
-->

## Installation

```sh
pip install git+https://github.com/eggplants/pyjlyric
# or,
pip install pyjlyric
```

## Usage

### CLI

```shellsession
jrc -h
```

### Library

```python
import pyjlyric

pyjlyric.parse("https://kashinavi.com/song_view.html?155779")
```

Returns:

```python
LyricPage(
  title='Life goes on',
  page_url=HttpUrl('https://kashinavi.com/song_view.html?155779', ),
  pageid='155779',
  artist=WithUrlText(
    link=HttpUrl('https://kashinavi.com/artist.html?artist=104498&kashu=King+%26+Prince&start=1', ),
    text='King & Prince'
  ),
  composer=[
    WithUrlText(link=None, text='Joacim Persson・Johan Alkenas・SQVARE・Sean Michael Alexander')
  ],
  lyricist=[WithUrlText(link=None, text='木村友威')],
  arranger=None,
  lyric=[
    ['Keep it up, keep it up yup'],
    ['...'],
    ['Everything will be alright いつだって', "...", "Let's live it up"]
  ]
)
```
