import pytest

from meme_generator.cairo_draw.common import Rect, Size
from meme_generator.cairo_draw.text import Font
from meme_generator.cairo_draw.constants import Align
from meme_generator.cairo_draw.helpers import get_text_bound, calculate_align


def test_get_text_bound(image_regression):
    bound = get_text_bound("top-left", font=Font(size=10))
    # TODO pixel perfect for CI and local
    assert bound.w in [48, 47]
    assert bound.h in [17, 16]


@pytest.mark.parametrize(
    "kw,expect",
    [
        [
            dict(
                rect=Rect(0, 0, w=100, h=100), box=Size(w=50, h=50), align=Align.CENTER
            ),
            Rect(x=25, y=25, w=50, h=50),
        ]
    ],
)
def test_calculate_align(kw, expect):
    assert calculate_align(**kw) == expect
