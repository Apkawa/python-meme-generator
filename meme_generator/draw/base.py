from dataclasses import dataclass
from typing import Optional, Union, Any

from meme_generator.common import Container, Point
from meme_generator.render import Render


@dataclass
class AbstractDraw:
    obj: Any
    pos: Union[Point, Container]

    def get_box(self):
        raise NotImplementedError()

    def get_pos(self):
        if isinstance(self.pos, Point):
            return self.pos
        raise NotImplementedError

    def render(self, render: Render):
        raise NotImplementedError()
