import os
from typing import List

from PIL import Image

from ..base_meme import BaseMeme
from ...common import Rect, Point, Size
from ...text import Font, Text
from ...constants import Align, TextAlignment
from ...helpers import get_text_bound, calculate_align
from ...render import Render

IMAGE_ROOT = os.path.join(os.path.dirname(__file__), 'img')


class SupermindMeme(BaseMeme):
    name = 'supermind'
    line_width = 5
    resize: Size = Size(200, 200)
    font: Font = Font(size=14)

    def get_images(self):
        images = []
        for name in sorted(os.listdir(IMAGE_ROOT)):
            f = os.path.join(IMAGE_ROOT, name)
            if not os.path.isfile(f):
                continue

            images.append(Image.open(f))
        return images

    def render(self, text_minds: List[str]):
        line_width = self.line_width

        images = self.get_images()[:len(text_minds)]
        total_w, total_h = 0, 0
        for img in images:
            img.thumbnail([self.resize.w, self.resize.h], Image.ANTIALIAS)
            w, h = img.size
            total_h += h
            if total_w < w:
                total_w = w
        total_h += (len(images) - 1) * line_width
        total_w *= 2
        r = Render(total_w, total_h)
        r.fill_bg()
        offset_x, offset_y = 0, 0
        for img, text in zip(images, text_minds):
            r.draw_image(img, Rect(offset_x, offset_y, 0, 0))

            text = Text(text,
                        width=img.size[0],
                        height=img.size[1],
                        font=self.font,
                        alignment=TextAlignment.CENTER
                        )
            aligned_bound = calculate_align(
                Rect(total_w / 2, offset_y, total_w / 2, img.size[1]),
                box=text.get_bound(),
                align=Align.CENTER
            )
            r.draw_text(text, bound=aligned_bound)
            offset_y += img.size[1] + line_width / 2
            r.draw_line([Point(0, offset_y), Point(total_w, offset_y)], line_width=line_width)
            offset_y += line_width / 2

        return r.save_to_stream()
