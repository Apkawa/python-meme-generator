from dataclasses import dataclass

from webcolors import hex_to_rgb

from meme_generator.constants import Align


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
    x: int
    y: int
    w: int
    h: int

    def align_box(self, box: Size, align: Align) -> "Rect":
        from .helpers import calculate_align
        return calculate_align(self, box, align)


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


