from typing import List

from ..base_image_text_meme import BaseImageTextMeme
from ...constants import TextAlignment
from ...text import Font, Text


class PoohMeme(BaseImageTextMeme):
    name = 'pooh'

    font = [
        Font(size=14),
        Font("Marck Script", size=14)
    ]

    def get_texts(self, texts: List[str]) -> List[Text]:
        for i, text in enumerate(texts):
            font = self.font[0]
            if i >= len(texts) - 1:
                font = self.font[1]
            yield Text(
                text,
                font=font,
                alignment=TextAlignment.CENTER
            )
