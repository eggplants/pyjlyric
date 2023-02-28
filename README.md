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

pyjlyric.get("https://https://kashinavi.com/song_view.html?155779")
# >>> <pyjlyric.Kashinavi(
  singer="...",
  lyricist="...",
  composer="...",
  id=155779,
  title="Life goes on",
  lyrics=[["..."], ["..."
  ]])>
```
