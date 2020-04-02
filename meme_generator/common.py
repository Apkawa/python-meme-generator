from dataclasses import dataclass

from webcolors import hex_to_rgb

from gi.repository import Pango as pango

from meme_generator.constants import TextStyle


@dataclass
class Size:
    w: int
    h: int


@dataclass
class Point:
    x: int
    y: int


@dataclass
class Rect:
    x: int = 0
    y: int = 0
    w: int or None = None
    h: int or None = None


def value_to_double(value):
    return value / 0xff


@dataclass
class Color:
    red: int
    green: int
    blue: int
    alpha: int = 0

    @classmethod
    def from_str(self, color: str):
        # TODO rgba
        rgb = hex_to_rgb(color)
        return Color(*rgb)

    @property
    def rgba(self):
        return list(map(value_to_double, [self.red, self.green, self.blue, self.alpha]))

    @property
    def rgb(self):
        return self.rgba[:3]


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
        return font
