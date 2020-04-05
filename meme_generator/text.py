from dataclasses import dataclass
from typing import Optional

from gi.repository import Pango as pango

from meme_generator.common import Size, Color, Line
from meme_generator.constants import TextStyle, TextAlignment


@dataclass
class Font:
    name: str = "Sans"
    size: int = 12

    style: TextStyle = TextStyle.NORMAL

    @property
    def font_desc(self):
        # https://lazka.github.io/pgi-docs/Pango-1.0/classes/FontDescription.html#Pango.FontDescription
        font = pango.FontDescription.from_string(f'{self.name} {self.size}')
        font.set_style(self.style.value)
        # https://valadoc.org/pango/Pango.html
        return font


@dataclass
class Text:
    text: str
    width: str or None = None
    height: str or None = None
    font: Font = Font()

    alignment: TextAlignment = TextAlignment.LEFT
    color: Color = Color.from_str("#000")

    # shadow: Optional[Shadow] = None
    border: Optional[Line] = None

    def get_bound(self) -> Size:
        from .helpers import get_text_bound
        return get_text_bound(
            self.text,
            width=self.width,
            height=self.height,
            font=self.font
        )
