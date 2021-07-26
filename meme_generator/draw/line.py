from dataclasses import dataclass
from typing import List

from meme_generator.common import Point, Line, Size
from meme_generator.draw.base import BaseDraw
from meme_generator.helpers import find_max_bound
from meme_generator.render import Render


@dataclass
class DrawLine(BaseDraw):
    obj: Line
    points: List[Point]

    def get_box(self) -> Size:
        p1, p2 = find_max_bound([self.pos] + self.points)

        size = Size(p2.x - p1.x, p2.y - p1.y)
        if size.w == 0:
            size.w = self.obj.width
        if size.h == 0:
            size.h = self.obj.width
        return size

    def render(self, render: Render):
        line = self.obj
        points = self.points
        ctx = render.ctx
        ctx.set_source_rgb(*line.color.rgb)
        ctx.set_line_width(line.width)
        pos = self.get_pos()
        ctx.move_to(pos.x, pos.y)
        for p in points:
            ctx.line_to(p.x, p.y)
        ctx.stroke()
