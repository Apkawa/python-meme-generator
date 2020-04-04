from dataclasses import dataclass
from typing import Optional

import PIL.Image
from webcolors import hex_to_rgb

from meme_generator.constants import Align
from meme_generator.types import ImageType


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

    @property
    def point(self):
        return Point(self.x, self.y)


@dataclass
class Container(Rect):
    align: Align


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
class Line:
    color: Color = Color.from_str("#000")
    width: float = .5
    # style


@dataclass
class Image:
    image: ImageType

    size: Optional[Size] = None

    def get_image(self) -> "PIL.Image.Image":
        if isinstance(self.image, PIL.Image.Image):
            im = self.image
        else:
            im = Image.open(self.image)
        return im
