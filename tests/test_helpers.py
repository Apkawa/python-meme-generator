import pytest

from meme_generator.common import Font, Rect, Align
from meme_generator.helpers import get_text_bound, calculate_align


def test_get_text_bound(image_regression):
    bound = get_text_bound("top-left", font=Font(size=10))
    assert bound.width == 48
    assert bound.height == 17


@pytest.mark.parametrize('kw,expect', [
    [dict(rect=Rect(w=100, h=100), box=Rect(w=50, h=50), align=Align.CENTER),
     Rect(x=25, y=25, w=50, h=50)]
])
def test_calculate_align(kw, expect):
    assert calculate_align(**kw) == expect
