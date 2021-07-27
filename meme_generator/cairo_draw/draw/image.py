from dataclasses import dataclass

import cairo

from meme_generator.cairo_draw.common import Image, Size
from meme_generator.cairo_draw.draw.base import BaseDraw
from meme_generator.cairo_draw.render import Render


@dataclass
class DrawImage(BaseDraw):
    obj: Image

    def get_box(self) -> Size:
        return Size(*self.obj.get_image().size)

    def render(self, render: Render):
        pos = self.get_pos()
        s = cairo.ImageSurface.create_from_png(self.obj.get_buffer())
        render.ctx.set_source_surface(s, pos.x, pos.y)
        render.ctx.paint()
