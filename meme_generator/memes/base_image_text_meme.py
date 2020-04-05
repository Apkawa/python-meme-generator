import os
from typing import List, Iterator

from meme_generator.common import Size, Point, Image, Container, Line
from meme_generator.constants import TextAlignment, Align
from meme_generator.draw.image import DrawImage
from meme_generator.draw.line import DrawLine
from meme_generator.draw.text import DrawText
from meme_generator.memes.base_meme import BaseMeme
from meme_generator.text import Font, Text


class BaseImageTextMeme(BaseMeme):
    name = None
    line = Line(width=5)
    image_width: int = 400
    font: Font = Font(size=14)
    text_position: Align.LEFT or Align.RIGHT = Align.RIGHT
    text_margin: int = 5

    def get_image_root(self):
        import inspect
        cls_file = inspect.getfile(self.__class__)
        return os.path.join(os.path.dirname(cls_file), 'img')

    def get_images(self) -> Iterator[Image]:
        root = self.get_image_root()
        for name in sorted(os.listdir(root)):
            f = os.path.join(root, name)
            if not os.path.isfile(f):
                continue
            yield Image(f, size=Size(self.image_width, 0))

    def get_texts(self, texts: List[str]) -> List[Text]:
        for text in texts:
            yield Text(text,
                       font=self.font,
                       alignment=TextAlignment.CENTER
                       )

    def get_drawers(self, texts: List[str]):
        offset_x, offset_y = 0, 0
        total_w = self.image_width * 2

        prev_line = None
        texts = self.get_texts(texts)
        for i, (img, text) in enumerate(zip(self.get_images(), texts)):
            d_im = DrawImage(img, Point(offset_x, offset_y))
            im_box = d_im.get_box()
            yield d_im
            text_container = Container(
                x=(total_w / 2),
                y=offset_y,
                w=(total_w / 2) - self.text_margin,
                h=im_box.h - self.text_margin,
                align=Align.CENTER
            )
            yield DrawText(text, pos=text_container, fit_text=True)
            offset_y += im_box.h
            if prev_line:
                yield prev_line
            prev_line = DrawLine(self.line, Point(0, offset_y), [Point(total_w, offset_y)])
