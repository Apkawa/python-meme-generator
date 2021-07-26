from dataclasses import dataclass, field, asdict, replace
from io import BytesIO
from typing import Optional, Tuple, Union

import PIL.Image
from webcolors import hex_to_rgb

from meme_generator.constants import Align
from meme_generator.types import ImageType, CoordType


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

    @property
    def point(self) -> Point:
        return Point(self.x, self.y)

    @property
    def points(self) -> Tuple[Point, Point]:
        return Point(self.x, self.y), Point(self.x + self.w, self.y + self.h)

    @property
    def size(self) -> Size:
        return Size(self.w, self.h)

    def reduce_size(self, size: Union[CoordType, Size]) -> 'Rect':
        if not isinstance(size, Size):
            size = Size(w=round(size * 2), h=round(size * 2))

        return replace(
            self,
            x=round(self.x + size.w / 2),
            y=round(self.y + size.h / 2),
            w=round(self.w - size.w / 2),
            h=round(self.h - size.h / 2),
        )


@dataclass
class Container(Rect):
    align: Align

    def align_box(self, box: Size) -> Rect:
        from .helpers import calculate_align
        return calculate_align(self, box, self.align)

    @property
    def rect(self) -> Rect:
        kw = asdict(self)
        kw.pop('align', None)
        return Rect(**kw)


def value_to_double(value: int) -> float:
    """
    Convert 0-255 to 0-1.0

    >>> value_to_double(255)
    1.0
    >>> value_to_double(0)
    0.0
    >>> value_to_double(128)
    0.5019607843137255

    :param value:
    :return:
    """
    return value / 0xff


@dataclass
class Color:
    red: int
    green: int
    blue: int
    alpha: int = 0

    @classmethod
    def from_str(self, color: str) -> "Color":
        # TODO rgba
        rgb = hex_to_rgb(color)
        return Color(*rgb)

    @property
    def rgba(self) -> Tuple[float, float, float, float]:
        return (
            value_to_double(self.red),
            value_to_double(self.green),
            value_to_double(self.blue),
            value_to_double(self.alpha)
        )

    @property
    def rgb(self) -> Tuple[float, float, float]:
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

    _image: Optional[PIL.Image.Image] = field(init=False, default=None)

    def get_image(self) -> PIL.Image.Image:
        from meme_generator.helpers import resize_image
        if self._image:
            return self._image

        if isinstance(self.image, PIL.Image.Image):
            im = self.image
        else:
            im = PIL.Image.open(self.image)
        size = self.size
        if size:
            _w, _h = im.size
            im = resize_image(im, width=size.w, height=size.h)
        self._image = im
        return im

    def get_buffer(self) -> BytesIO:
        im = self.get_image()
        buffer = BytesIO()
        im.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer
