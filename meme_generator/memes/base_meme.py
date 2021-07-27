from typing import List

from meme_generator.cairo_draw.common import Size
from meme_generator.cairo_draw.draw.base import BaseDraw
from meme_generator.cairo_draw.helpers import find_max_bound
from meme_generator.cairo_draw.render import Render


class BaseMeme:
    name: str

    def get_drawers(self, *args, **kwargs) -> List[BaseDraw]:
        raise NotImplementedError()

    def render(self, *args, **kwargs):
        drawers = list(self.get_drawers(*args, **kwargs))

        p1, p2 = find_max_bound([d.get_rect() for d in drawers])
        canvas_size = Size(p1.x + p2.x, p1.y + p2.y)

        render = Render(int(canvas_size.w), int(canvas_size.h))
        render.fill_bg()
        for d in drawers:
            render.draw(d)
        return render.save_to_stream()
