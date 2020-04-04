# -*- coding: utf-8 -*-
import os
from io import BytesIO
from typing import Union, BinaryIO, List

import cairo

from meme_generator.common import Color, Rect, Point, Line, Image
from . import fontconfig as fc
from .text import Text
from .types import ImageType

FONTS_ROOT = os.path.join(os.path.dirname(__file__), 'fonts')


def load_fonts():
    conf = fc.Config.get_current()
    for name in os.listdir(FONTS_ROOT):
        path = os.path.join(FONTS_ROOT, name)
        if not os.path.isfile(path):
            continue

        conf.app_font_add_file(path)


load_fonts()


class Render:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        self.ctx: cairo.Context = cairo.Context(self.surf)

    def fill_bg(self, color: Color = Color.from_str('#fff')):
        self.ctx.rectangle(0, 0, self.width, self.height)
        self.ctx.set_source_rgb(*color.rgb)
        self.ctx.fill()

    def draw(self, obj: "meme_generator.draw.base.AbstractDraw"):
        obj.render(self)

    def draw_text(self, text: Text, pos: Point):
        from .draw.text import DrawText
        self.draw(DrawText(text, pos))

    def draw_image(self, image: Image, pos: Point = Point(0, 0)):
        from meme_generator.draw.image import DrawImage
        self.draw(DrawImage(image, pos))

    def draw_line(self, points: List[Point], color: Color = Color.from_str('#000'), line_width=0.5):
        from meme_generator.draw.line import DrawLine
        self.draw(DrawLine(Line(width=line_width, color=color), pos=None, points=points))

    def save(self, fp: Union[BinaryIO, str]):
        self.surf.write_to_png(fp)

    def save_to_stream(self):
        fp = BytesIO()
        self.save(fp)
        fp.seek(0)
        return fp
