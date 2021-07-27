from dataclasses import asdict
from typing import Union, List, Tuple, Optional

import PIL.Image
import cairo
from gi.repository import Pango as pango
from gi.repository import PangoCairo as pangocairo

from meme_generator.cairo_draw.common import Rect, Size, Point
from meme_generator.cairo_draw.constants import Align
from meme_generator.cairo_draw.text import Font


def get_text_bound(
    text: str,
    width: Optional[int] = None,
    height: Optional[int] = None,
    font: Font = Font(),
) -> Size:
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1000, 1000)
    ctx = cairo.Context(surf)
    layout = pangocairo.create_layout(ctx)
    layout.set_markup(text)
    layout.set_font_description(font.font_desc)
    if width:
        layout.set_width(width * pango.SCALE)
        layout.set_wrap(pango.WrapMode.WORD)
    if height:
        layout.set_height(width * pango.SCALE)
    size = layout.get_pixel_size()
    return Size(w=size.width, h=size.height)


def calculate_align(rect: Rect, box: Size, align: Align) -> Rect:
    new_rect = Rect(x=0, y=0, w=box.w, h=box.h)

    if Align.CENTER & align:
        new_rect.x = (rect.w / 2) - (new_rect.w / 2)
        new_rect.y = (rect.h / 2) - (new_rect.h / 2)
    if Align.LEFT & align:
        new_rect.x = 0
    if Align.RIGHT & align:
        new_rect.x = rect.w - new_rect.w

    if Align.TOP & align:
        new_rect.y = 0

    if Align.BOTTOM & align:
        new_rect.y = rect.h - new_rect.h

    new_rect.x += rect.x
    new_rect.y += rect.y
    return new_rect


def find_max_bound(pos_list: List[Union[Point, Rect]]) -> Tuple[Point, Point]:
    p1, p2 = None, None
    for pos in pos_list:
        _p = [pos]
        if isinstance(pos, Rect):
            _p = pos.points
        for p in _p:
            if p1 is None:
                p1 = Point(**asdict(p))
                p2 = Point(**asdict(p))
                continue
            if p.x < p1.x:
                p1.x = p.x
            if p.y < p1.y:
                p1.y = p.y

            if p.x > p2.x:
                p2.x = p.x
            if p.y > p2.y:
                p2.y = p.y
    return p1, p2


def resize_image(
    im: PIL.Image.Image, width: Optional[int] = None, height: Optional[int] = None
) -> PIL.Image.Image:
    a_ratio = []
    if width:
        a_ratio.append(width / im.size[0])
    if height:
        a_ratio.append(height / im.size[1])
    aspect_ratio = min(a_ratio)
    result_size = list([width, height])
    if width:
        result_size[1] = im.size[1] * aspect_ratio
    if height:
        result_size[0] = im.size[0] * aspect_ratio
    return im.resize(map(int, result_size), resample=PIL.Image.ANTIALIAS)
