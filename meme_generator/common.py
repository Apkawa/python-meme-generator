from dataclasses import dataclass
from enum import Enum, auto, Flag

from webcolors import hex_to_rgb

from gi.repository import Pango as pango


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

    class Style:
        NORMAL = pango.Style.NORMAL
        ITALIC = pango.Style.ITALIC
        OBLIQUE = pango.Style.OBLIQUE

    style: Style = Style.NORMAL

    @property
    def font_desc(self):
        # https://lazka.github.io/pgi-docs/Pango-1.0/classes/FontDescription.html#Pango.FontDescription
        font = pango.FontDescription.from_string(f'{self.name} {self.size}')
        font.set_style(self.style)
        return font


class Align(Flag):
    LEFT = auto()
    RIGHT = auto()
    TOP = auto()
    CENTER = auto()
    BOTTOM = auto()

    VERTICAL = TOP | BOTTOM
    HORIZONTAL = LEFT | RIGHT

    # def __init__(self, *args):
    #     cls = self.__class__
    #     if self.value in [cls.VERTICAL, cls.HORIZONTAL]:
    #         raise ValueError("Invalid combination")
