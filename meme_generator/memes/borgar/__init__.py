import os
from typing import List, Iterator

from meme_generator.common import Size, Point, Image, Container, Line, Color
from meme_generator.constants import TextAlignment, Align, TextStyle
from meme_generator.draw.image import DrawImage
from meme_generator.draw.line import DrawLine
from meme_generator.draw.text import DrawText
from meme_generator.memes.base_meme import BaseMeme
from meme_generator.text import Font, Text


class BorgarMeme(BaseMeme):
    name = None
    image_width: int = 400
    font: Font = Font("Impact", size=14, style=TextStyle.UPPER_CAPS)
    text_border = Line(width=3, color=Color.from_str("#000"))
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
                       alignment=TextAlignment.CENTER,
                       color=Color.from_str("#FFF"),
                       border=self.text_border
                       )

    def get_drawers(self, texts: List[str]):
        offset_x, offset_y = 0, 0
        total_w = self.image_width
        texts = self.get_texts(texts)

        img = list(self.get_images())[0]
        d_im = DrawImage(img, Point(0, 0))
        im_box = d_im.get_box()
        yield d_im

        for i, text in enumerate(texts):
            align = Align.CENTER
            if i == 0:
                align |= Align.TOP
            elif i == 1:
                align |= Align.BOTTOM
            else:
                break
            text_container = Container(
                x=0,
                y=offset_y,
                w=total_w - self.text_margin,
                h=im_box.h / 2,
                align=align
            )
            yield DrawText(text, pos=text_container, fit_text=True)
            offset_y += im_box.h / 2
