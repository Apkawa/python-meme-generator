from dataclasses import dataclass
from io import BytesIO

import PIL.Image
import cairo

from meme_generator.common import Point, Image
from meme_generator.draw.base import AbstractDraw
from meme_generator.render import Render


@dataclass
class DrawImage(AbstractDraw):
    obj: Image

    def render(self, render: Render):
        pos = self.get_pos()
        im = self.obj.get_image()
        buffer = BytesIO()
        size = self.obj.size
        if size:
            _w, _h = im.size
            im.thumbnail([size.w or _w, size.h or _h], PIL.Image.ANTIALIAS)
        im.save(buffer, format="PNG")
        buffer.seek(0)

        s = cairo.ImageSurface.create_from_png(buffer)
        render.ctx.set_source_surface(s, pos.x, pos.y)
        render.ctx.paint()
