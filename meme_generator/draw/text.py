from dataclasses import dataclass, replace

import cairo
from gi.repository import Pango as pango
from gi.repository import PangoCairo as pangocairo

from meme_generator.common import Size, Container
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

        if self.fit_text:
            # Begin large font
            text.font = replace(text.font, size=round(text.width * 0.07))

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

        if text.alignment:
            layout.set_alignment(text.alignment.value)

        ctx.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
        ctx.move_to(pos.x, pos.y)
        layout.set_font_description(text.font.font_desc)
        layout.set_text(text.text)

        sub_surf_size = Size(box.w + 40, box.h + 150)
        sub_offset = Size(int(20), int(sub_surf_size.h / 4))

        if text.border:
            b_width = text.border.width
            surf = cairo.ImageSurface(
                cairo.FORMAT_ARGB32, sub_surf_size.w, sub_surf_size.h
            )
            b_ctx = cairo.Context(surf)
            b_ctx.move_to(sub_offset.w, sub_offset.h)
            # b_ctx.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
            b_ctx.set_source_rgb(*text.border.color.rgb)
            pangocairo.update_layout(b_ctx, layout)
            pangocairo.layout_path(b_ctx, layout)
            b_ctx.set_line_width(b_width)
            b_ctx.stroke()
            ctx.set_source_surface(surf, (pos.x - sub_offset.w), (pos.y - sub_offset.h))
            ctx.paint()

        text_surf = cairo.ImageSurface(
            cairo.FORMAT_ARGB32, sub_surf_size.w, sub_surf_size.h
        )
        t_ctx = cairo.Context(text_surf)
        t_ctx.move_to(sub_offset.w, sub_offset.h)
        t_ctx.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
        t_ctx.set_source_rgb(*text.color.rgb)
        pangocairo.update_layout(t_ctx, layout)
        pangocairo.show_layout(t_ctx, layout)
        ctx.set_source_surface(text_surf, pos.x - sub_offset.w, pos.y - sub_offset.h)
        ctx.paint()
