# -*- coding: utf-8 -*-
import sys
from io import BytesIO
from typing import Union, BinaryIO

import cairo
from PIL import Image
from gi.repository import Pango as pango
from gi.repository import PangoCairo as pangocairo

from meme_generator.common import Color, Rect, Font
from meme_generator.constants import TextAlignment


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

    def draw_text(self, text: str, bound: Rect = Rect(0, 0),
                  color: Color = Color.from_str("#000"),
                  font: Font = Font("Sans", 25),
                  alignment: TextAlignment = TextAlignment.LEFT):
        context = self.ctx
        context.move_to(bound.x, bound.y)
        layout = pangocairo.create_layout(context)

        context.set_antialias(cairo.ANTIALIAS_SUBPIXEL)

        layout.set_font_description(font.font_desc)

        if bound.w:
            text_width = bound.w
            if bound.x + bound.w > self.width:
                text_width = bound.w - ((bound.x + bound.w) - self.width)
            layout.set_width(text_width * pango.SCALE)
            layout.set_wrap(pango.WrapMode.WORD)
        if bound.h:
            layout.set_height(bound.w)

        if alignment:
            layout.set_alignment(alignment.value)

        layout.set_text(text)
        context.set_source_rgb(*color.rgb)
        pangocairo.update_layout(context, layout)
        pangocairo.show_layout(context, layout)

    def draw_image(self, image: Union[Image.Image, BinaryIO, str], rect: Rect = Rect()):
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

    def draw_line(self, rect: Rect, color: Color = Color.from_str('#000'), line_width=0.5):
        self.ctx.set_source_rgb(*color.rgb)
        self.ctx.set_line_width(line_width)
        self.ctx.move_to(rect.x, rect.y)
        self.ctx.line_to(rect.w, rect.h)
        self.ctx.stroke()

    def save(self, fp: Union[BinaryIO, str]):
        self.surf.write_to_png(fp)

    def save_to_stream(self):
        fp = BytesIO()
        self.save(fp)
        fp.seek(0)
        return fp

