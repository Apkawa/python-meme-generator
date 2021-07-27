# -*- coding: utf-8 -*-
from io import BytesIO
from typing import Union, BinaryIO, List

import cairo

from meme_generator.cairo_draw.common import Color, Point, Line, Image
from .font_manager import font_manager
from .text import Text


class Render:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        self.ctx: cairo.Context = cairo.Context(self.surf)
        self.font_manager = font_manager
        self.font_manager.init()

    def fill_bg(self, color: Color = Color.from_str("#fff")):
        self.ctx.rectangle(0, 0, self.width, self.height)
        self.ctx.set_source_rgb(*color.rgb)
        self.ctx.fill()

    def draw(self, obj: "meme_generator.draw.base.BaseDraw"):
        obj.render(self)

    def draw_text(self, text: Text, pos: Point):
        from meme_generator.cairo_draw.draw.text import DrawText

        self.draw(DrawText(text, pos))

    def draw_image(self, image: Image, pos: Point = Point(0, 0)):
        from meme_generator.cairo_draw.draw.image import DrawImage

        self.draw(DrawImage(image, pos))

    def draw_line(
        self, points: List[Point], color: Color = Color.from_str("#000"), line_width=0.5
    ):
        from meme_generator.cairo_draw.draw.line import DrawLine

        self.draw(
            DrawLine(
                Line(width=line_width, color=color), pos=points[0], points=points[1:]
            )
        )

    def save(self, fp: Union[BinaryIO, str]):
        self.surf.write_to_png(fp)

    def save_to_stream(self):
        fp = BytesIO()
        self.save(fp)
        fp.seek(0)
        return fp
