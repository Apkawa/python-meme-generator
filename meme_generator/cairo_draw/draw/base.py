from dataclasses import dataclass, asdict
from typing import Union, Any

from meme_generator.cairo_draw.common import Container, Point, Size, Rect
from meme_generator.cairo_draw.render import Render


@dataclass
class BaseDraw:
    obj: Any
    pos: Union[Point, Container]

    def get_rect(self) -> Rect:
        if isinstance(self.pos, Container):
            return self.pos.rect

        if isinstance(self.pos, Point):
            kw = asdict(self.pos)
            kw.update(asdict(self.get_box()))
            return Rect(**kw)
        raise NotImplementedError()

    def get_box(self) -> Size:
        raise NotImplementedError()

    def get_pos(self) -> Point:
        if isinstance(self.pos, Point):
            return self.pos
        if isinstance(self.pos, Container):
            return self.pos.align_box(self.get_box()).point
        raise NotImplementedError

    def render(self, render: Render):
        raise NotImplementedError()
