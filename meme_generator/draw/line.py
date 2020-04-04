from dataclasses import dataclass
from typing import List

from meme_generator.common import Point, Line
from meme_generator.draw.base import AbstractDraw
from meme_generator.render import Render


@dataclass
class DrawLine(AbstractDraw):
    obj: Line
    points: List[Point]

    def render(self, render: Render):
        line = self.obj
        points = self.points
        ctx = render.ctx
        ctx.set_source_rgb(*line.color.rgb)
        ctx.set_line_width(line.width)
        ctx.move_to(points[0].x, points[0].y)
        for p in points[1:]:
            ctx.line_to(p.x, p.y)
        ctx.stroke()
