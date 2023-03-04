from pyjlyric.model import LyricPage, WithUrlText


class JtotalLyricPage(LyricPage):
    artist: WithUrlText
    composer: str
    lyricist: str
    arranger: None
