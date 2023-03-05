from pyjlyric.model import LyricPage, WithUrlText


class GakkiLyricPage(LyricPage):
    artist: WithUrlText
    composer: str
    lyricist: str
    arranger: None
