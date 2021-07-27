from dataclasses import dataclass
from typing import Optional

from gi.repository import Pango as pango

from meme_generator.cairo_draw.common import Size, Color, Line
from meme_generator.cairo_draw.constants import TextStyle, TextAlignment


@dataclass
class Font:
    name: str = "Sans"
    size: int = 12

    style: Optional[TextStyle] = None

    @property
    def font_desc(self):
        # https://lazka.github.io/pgi-docs/Pango-1.0/classes/FontDescription.html#Pango.FontDescription
        font = pango.FontDescription.from_string(f"{self.name} {self.size}")
        if self.style:
            style = (TextStyle.ITALIC | TextStyle.OBLIQUE) & self.style
            if style:
                font.set_style(getattr(pango.Style, style.name))
            variant = TextStyle.SMALL_CAPS & self.style
            if variant:
                font.set_variant(pango.Variant.SMALL_CAPS)
        # https://valadoc.org/pango/Pango.html
        return font


@dataclass
class Text:
    _text: str
    width: Optional[int] = None
    height: Optional[int] = None
    font: Font = Font()

    alignment: TextAlignment = TextAlignment.LEFT
    color: Color = Color.from_str("#000")

    # shadow: Optional[Shadow] = None
    border: Optional[Line] = None

    @property
    def text(self) -> str:
        if self.font.style and TextStyle.UPPER_CAPS & self.font.style:
            return self._text.upper()
        return self._text

    @text.setter
    def text(self, v: str) -> None:
        self._text = v

    def get_bound(self) -> Size:
        from .helpers import get_text_bound

        return get_text_bound(
            self.text, width=self.width, height=self.height, font=self.font
        )
