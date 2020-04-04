from dataclasses import dataclass
from typing import Union, List

import cairo

from gi.repository import Pango as pango
from gi.repository import PangoCairo as pangocairo

from meme_generator.common import Point
from meme_generator.draw.base import AbstractDraw
from meme_generator.render import Render
from meme_generator.text import Text


@dataclass
class DrawText(AbstractDraw):
    obj: Text

    def render(self, render: Render):
        text = self.obj
        pos = self.pos
        ctx = render.ctx

        ctx.move_to(pos.x, pos.y)
        layout = pangocairo.create_layout(ctx)

        ctx.set_antialias(cairo.ANTIALIAS_SUBPIXEL)

        layout.set_font_description(text.font.font_desc)

        if text.width:
            text_width = text.width
            if pos.x + text_width > render.width:
                text_width = text_width - ((pos.x + text_width) - render.width)
            layout.set_width(text_width * pango.SCALE)
            layout.set_wrap(pango.WrapMode.WORD)
        if text.height:
            layout.set_height(text.height * pango.SCALE)

        if text.alignment:
            layout.set_alignment(text.alignment.value)

        layout.set_text(text.text)
        ctx.set_source_rgb(*text.color.rgb)
        pangocairo.update_layout(ctx, layout)
        pangocairo.show_layout(ctx, layout)
