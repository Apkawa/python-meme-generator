import cairo
from gi.repository import Pango as pango
from gi.repository import PangoCairo as pangocairo

from meme_generator.common import Rect, Size
from meme_generator.text import Font
from meme_generator.constants import Align


def get_text_bound(text: str, width=None, height=None, font: Font = Font()) -> Size:
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


