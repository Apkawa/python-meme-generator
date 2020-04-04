import pytest

from meme_generator.common import Rect, Point
from meme_generator.text import Font, Text
from meme_generator.constants import Align
from meme_generator.helpers import get_text_bound, calculate_align
from meme_generator.render import Render

ALIGNS = [
    Align.TOP | Align.LEFT,
    Align.TOP | Align.CENTER,
    Align.TOP | Align.RIGHT,
    Align.CENTER | Align.LEFT,
    Align.CENTER,
    Align.CENTER | Align.RIGHT,
    Align.BOTTOM | Align.LEFT,
    Align.BOTTOM | Align.CENTER,
    Align.BOTTOM | Align.RIGHT,
]


def test_draw_multiple_texts(image_regression):
    r = Render(800, 400)
    r.fill_bg()
    r.draw_line([Point(400, 0), Point(400, 400)], line_width=3)
    r.draw_line([Point(400, 200), Point(800, 200)], line_width=.5)
    r.draw_line([Point(400 + 200, 0), Point(400 + 200, 400)], line_width=.5)

    text_container = Rect(400, 0, 400, 400)

    font = Font(size=10)
    for align in ALIGNS:
        text = Text(str(align), font=font)
        text_bound = text.get_bound()
        align_text_bound = calculate_align(text_container, text_bound, align=align)

        r.draw_text(
            text,
            pos=align_text_bound.point)

    image_regression(r.save_to_stream())


@pytest.mark.parametrize('align', ALIGNS)
def test_draw_align_multiline_text(align, image_regression):
    r = Render(800, 400)
    r.fill_bg()
    r.draw_line([Point(400, 0), Point(400, 400)], line_width=3)
    r.draw_line([Point(400, 200), Point(800, 200)], line_width=.5)
    r.draw_line([Point(400 + 200, 0), Point(400 + 200, 400)], line_width=.5)

    text_container = Rect(400, 0, 400, 400)

    font = Font(size=16)

    text = Text("Мир: сгорает в огне инфекции\n"
            "Экономика: кончается в муках", font=font, width=400)
    text_bound = text.get_bound()
    align_text_bound = calculate_align(text_container, text_bound, align=align)

    r.draw_text(
        text,
        pos=align_text_bound.point)

    image_regression(r.save_to_stream())
