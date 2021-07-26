# -*- coding: utf-8 -*-
import os
import tempfile
from io import BytesIO
from typing import Union, BinaryIO, List

import cairo

from meme_generator.common import Color, Point, Line, Image
from . import fontconfig as fc

from .text import Text

FONTS_ROOT = os.path.join(os.path.dirname(__file__), 'fonts')


def load_fonts():
    conf = fc.Config.get_current()
    xml = '''
<!DOCTYPE fontconfig SYSTEM "fonts.dtd">
<fontconfig>
        <match target="pattern">
            <test name="family" qual="first" compare="contains">
                <string>emoji</string>
            </test>
            <edit name="family" mode="prepend" binding="strong">
                    <string>Apple Color Emoji</string>
            </edit>
        </match> 
</fontconfig>
        '''
    # TODO cleanup
    fd, conf_filename = tempfile.mkstemp()
    os.write(fd, xml.encode('utf-8'))
    os.close(fd)
    conf.parse_and_load(conf_filename, True)

    conf.set_current()

    font_path = []
    for name in os.listdir(FONTS_ROOT):
        path = os.path.join(FONTS_ROOT, name)
        if not os.path.isfile(path):
            continue
        font_path.append(path)

    for path in font_path:
        conf.app_font_add_file(path)


load_fonts()


class Render:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        self.ctx: cairo.Context = cairo.Context(self.surf)

    def fill_bg(self, color: Color = Color.from_str('#fff')):
        self.ctx.rectangle(0, 0, self.width, self.height)
        self.ctx.set_source_rgb(*color.rgb)
        self.ctx.fill()

    def draw(self, obj: "meme_generator.draw.base.AbstractDraw"):
        obj.render(self)

    def draw_text(self, text: Text, pos: Point):
        from .draw.text import DrawText
        self.draw(DrawText(text, pos))

    def draw_image(self, image: Image, pos: Point = Point(0, 0)):
        from meme_generator.draw.image import DrawImage
        self.draw(DrawImage(image, pos))

    def draw_line(self, points: List[Point], color: Color = Color.from_str('#000'), line_width=0.5):
        from meme_generator.draw.line import DrawLine
        self.draw(DrawLine(Line(width=line_width, color=color), pos=points[0], points=points[1:]))

    def save(self, fp: Union[BinaryIO, str]):
        self.surf.write_to_png(fp)

    def save_to_stream(self):
        fp = BytesIO()
        self.save(fp)
        fp.seek(0)
        return fp
