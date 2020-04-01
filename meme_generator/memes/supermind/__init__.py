import os
from typing import List

from PIL import Image

from ..base_meme import BaseMeme
from ...common import Rect
from ...render import Render

IMAGE_ROOT = os.path.join(os.path.dirname(__file__), 'img')


class SupermindMeme(BaseMeme):
    name = 'supermind'

    def get_images(self):
        images = []
        for name in sorted(os.listdir(IMAGE_ROOT)):
            f = os.path.join(IMAGE_ROOT, name)
            if not os.path.isfile(f):
                continue

            images.append(Image.open(f))
        return images

    def render(self, text_minds: List[str]):
        line_width = 3
        images = self.get_images()[:len(text_minds)]
        total_w, total_h = 0, 0
        for img in images:
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

            r.draw_image(img, Rect(offset_x, offset_y))
            offset_y += img.size[1]
            r.draw_line(Rect(0, offset_y, total_w, offset_y), line_width=line_width)

        return r.save_to_stream()

