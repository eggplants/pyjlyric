# pyjlyric: Japanese Lyric Aggregator

[![PyPI](
  <https://img.shields.io/pypi/v/pyjlyric?color=blue>
  ) ![Python Version](
  <https://img.shields.io/pypi/pyversions/pyjlyric>
  )](
  <https://pypi.org/project/pyjlyric/>
) [![Release Package](
  <https://github.com/eggplants/pyjlyric/actions/workflows/release.yml/badge.svg>
  )](
  <https://github.com/eggplants/pyjlyric/actions/workflows/release.yml>
) [![Ghcr](
  <https://ghcr-badge.egpl.dev/eggplants/pyjlyric/size>
  )](
  <https://github.com/eggplants/pyjlyric/pkgs/container/pyjlyric/74193340?tag=latest>
)

[![pre-commit.ci status](
  <https://results.pre-commit.ci/badge/github/eggplants/pyjlyric/master.svg>
  )](
  <https://results.pre-commit.ci/latest/github/eggplants/pyjlyric/master>
) [![Maintainability](
  <https://qlty.sh/badges/1d3588fe-b2bd-4903-b301-3bfb8064ddf3/maintainability.svg>
  )](
  <https://qlty.sh/gh/eggplants/projects/pyjlyric>
) [![Code Coverage](
  <https://qlty.sh/badges/1d3588fe-b2bd-4903-b301-3bfb8064ddf3/test_coverage.svg>
  )](
  <https://qlty.sh/gh/eggplants/projects/pyjlyric>
)

## Supported sites

- <http://www.animap.jp/kasi/showkasi.php?surl=:pageid>
- <http://www.utamap.com/showtop.php?surl=:pageid>
- <https://gakufu.gakki.me/m/data/:pageid.html>
- <https://hoick.jp/mdb/detail/:pageid>
- <https://j-lyric.net/artist/:artistid/:pageid.html>
- <https://kashinavi.com/song_view.html?:pageid>
- <https://linkco.re/:albumid/songs/:songid/lyrics>
- <https://lyric.evesta.jp/:pageid.html>
- <https://music-book.jp/music/Artist/:artistid/Music/:pageid>
- <https://music.j-total.net/data/:pageid.html>
- <https://petitlyrics.com/lyrics/:pageid>
- <https://utaten.com/lyric/:pageid>
- <https://www.joysound.com/web/search/song/:pageid>
- <https://www.uta-net.com/song/:pageid>

## Installation

```sh
pip install git+https://github.com/eggplants/pyjlyric
# or
pip install pyjlyric
```

## Usage

### CLI

<!-- markdownlint-disable MD010 -->

```shellsession
$ jrc https://j-lyric.net/artist/a00126c/l013283.html
===
Title:		春よ来い
Artist:		童謡・唱歌
Lyric:		相馬 御風
Composer:	弘田 龍太郎
===
春よ来い早く来い
あるきはじめたみいちゃんが
赤い鼻緒のじょじょはいて
おんもへ出たいと待っている

春よ来い早く来い
おうちの前の桃の木の
蕾もみんなふくらんで
はよ咲きたいと待っている
```

<!-- markdownlint-enable MD010 -->

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
  - http://www.animap.jp/kasi/showkasi.php?surl=:pageid
  - http://www.utamap.com/showtop.php?surl=:pageid
  - https://gakufu.gakki.me/m/data/:pageid.html
  - https://hoick.jp/mdb/detail/:pageid
  - https://j-lyric.net/artist/:artistid/:pageid.html
  - https://kashinavi.com/song_view.html?:pageid
  - https://linkco.re/:albumid/songs/:songid/lyrics
  - https://lyric.evesta.jp/:pageid.html
  - https://music-book.jp/music/Artist/:artistid/Music/:pageid
  - https://music.j-total.net/data/:pageid.html
  - https://petitlyrics.com/lyrics/:pageid
  - https://utaten.com/lyric/:pageid
  - https://www.joysound.com/web/search/song/:pageid
  - https://www.uta-net.com/song/:pageid
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
