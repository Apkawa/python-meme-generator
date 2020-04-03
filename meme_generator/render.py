# -*- coding: utf-8 -*-
import os
import sys
from io import BytesIO
from typing import Union, BinaryIO, List

import cairo
from PIL import Image
from gi.repository import Pango as pango
from gi.repository import PangoCairo as pangocairo

from meme_generator.common import Color, Rect, Point
from .text import Font, Text
from meme_generator.constants import TextAlignment

from . import fontconfig as fc

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

    def draw_text(self, text: Text, bound: Rect):
        context = self.ctx
        context.move_to(bound.x, bound.y)
        layout = pangocairo.create_layout(context)

        context.set_antialias(cairo.ANTIALIAS_SUBPIXEL)

        layout.set_font_description(text.font.font_desc)

        if bound.w:
            text_width = bound.w
            if bound.x + bound.w > self.width:
                text_width = bound.w - ((bound.x + bound.w) - self.width)
            layout.set_width(text_width * pango.SCALE)
            layout.set_wrap(pango.WrapMode.WORD)
        if bound.h:
            layout.set_height(bound.h * pango.SCALE)

        if text.alignment:
            layout.set_alignment(text.alignment.value)

        layout.set_text(text.text)
        context.set_source_rgb(*text.color.rgb)
        pangocairo.update_layout(context, layout)
        pangocairo.show_layout(context, layout)

    def draw_image(self, image: Union[Image.Image, BinaryIO, str], rect: Rect = Rect(0,0,0,0)):
        if isinstance(image, Image.Image):
            im = image
        else:
            im = Image.open(image)
        buffer = BytesIO()
        if rect.h or rect.w:
            _w, _h = im.size
            im.thumbnail([rect.w or _w, rect.h or _h], Image.ANTIALIAS)
        im.save(buffer, format="PNG")
        buffer.seek(0)

        s = cairo.ImageSurface.create_from_png(buffer)
        self.ctx.set_source_surface(s, rect.x, rect.y)
        self.ctx.paint()

    def draw_line(self, points: List[Point], color: Color = Color.from_str('#000'), line_width=0.5):
        self.ctx.set_source_rgb(*color.rgb)
        self.ctx.set_line_width(line_width)
        self.ctx.move_to(points[0].x, points[0].y)
        for p in points[1:]:
            self.ctx.line_to(p.x, p.y)
        self.ctx.stroke()

    def save(self, fp: Union[BinaryIO, str]):
        self.surf.write_to_png(fp)

    def save_to_stream(self):
        fp = BytesIO()
        self.save(fp)
        fp.seek(0)
        return fp
