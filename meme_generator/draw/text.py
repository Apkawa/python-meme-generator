from dataclasses import dataclass
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

    def __post_init__(self):
        if isinstance(self.pos, Container):
            self.obj.width = self.obj.width or self.pos.w
            self.obj.height = self.obj.height or self.pos.h

    def get_box(self) -> Size:
        return self.obj.get_bound()

    def render(self, render: Render):
        text = self.obj
        pos = self.get_pos()
        box = self.get_box()
        ctx = render.ctx

        ctx.move_to(pos.x, pos.y)
        layout = pangocairo.create_layout(ctx)

        ctx.set_antialias(cairo.ANTIALIAS_SUBPIXEL)

        layout.set_font_description(text.font.font_desc)

        if box.w:
            text_width = box.w
            if pos.x + text_width > render.width:
                text_width = text_width - ((pos.x + text_width) - render.width)
            layout.set_width(text_width * pango.SCALE)
            layout.set_wrap(pango.WrapMode.WORD)
        if box.h:
            layout.set_height(box.h * pango.SCALE)

        if text.alignment:
            layout.set_alignment(text.alignment.value)

        layout.set_text(text.text)
        ctx.set_source_rgb(*text.color.rgb)
        pangocairo.update_layout(ctx, layout)
        pangocairo.show_layout(ctx, layout)
