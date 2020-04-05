from dataclasses import dataclass, replace
from functools import lru_cache
from typing import Union, List

import cairo

from gi.repository import Pango as pango
from gi.repository import PangoCairo as pangocairo

from meme_generator.common import Point, Size, Container
from meme_generator.draw.base import BaseDraw
from meme_generator.render import Render
from meme_generator.text import Text


@dataclass
class DrawText(BaseDraw):
    obj: Text

    fit_text: bool = False

    def __post_init__(self):
        if isinstance(self.pos, Container):
            self.obj.width = self.obj.width or self.pos.w
            self.obj.height = self.obj.height or self.pos.h

    def get_box(self) -> Size:
        return self.obj.get_bound()

    def render(self, render: Render):
        text = self.obj
        ctx = render.ctx

        layout = pangocairo.create_layout(ctx)

        ctx.set_antialias(cairo.ANTIALIAS_SUBPIXEL)

        if self.fit_text:
            # Begin large font
            text.font = replace(text.font, size=text.width * .07)

        pos = self.get_pos()
        box = self.get_box()
        while text.font.size > 4:
            text_width = box.w + text.font.size
            if text.width and text_width > text.width:
                text_width = text_width - (text_width - text.width)
            layout.set_width(text_width * pango.SCALE)
            layout.set_wrap(pango.WrapMode.WORD)

            text_height = box.h
            if text.height and text_height > text.height:
                text_height = text_height - (text_height - text.height)
            layout.set_height(text_height * pango.SCALE)

            if not self.fit_text:
                break

            if box.h > text.height or box.w > text.width:
                text.font = replace(text.font, size=text.font.size - 1)
                pos = self.get_pos()
                box = self.get_box()
            else:
                break

        layout.set_font_description(text.font.font_desc)
        ctx.move_to(pos.x, pos.y)
        if text.alignment:
            layout.set_alignment(text.alignment.value)

        layout.set_text(text.text)
        ctx.set_source_rgb(*text.color.rgb)
        pangocairo.update_layout(ctx, layout)
        pangocairo.show_layout(ctx, layout)
