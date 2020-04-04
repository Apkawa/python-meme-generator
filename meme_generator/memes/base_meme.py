from typing import List

from meme_generator.draw.base import AbstractDraw


class BaseMeme:
    name: str

    def get_drawers(self, *args, **kwargs) -> List[AbstractDraw]:
        raise NotImplementedError()

    def render(self, *args, **kwargs):
        raise NotImplementedError()