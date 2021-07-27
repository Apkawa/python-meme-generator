from typing import List, Generator

from ..base_image_text_meme import BaseImageTextMeme
from meme_generator.cairo_draw.constants import TextAlignment
from meme_generator.cairo_draw.text import Font, Text


class PoohMeme(BaseImageTextMeme):
    name = "pooh"

    font: List[Font] = [Font(size=14), Font("Marck Script", size=14)]

    def get_texts(self, texts: List[str]) -> Generator[Text, None, None]:
        for i, text in enumerate(texts):
            font = self.font[0]
            if i >= len(texts) - 1:
                font = self.font[1]
            yield Text(text, font=font, alignment=TextAlignment.CENTER)
