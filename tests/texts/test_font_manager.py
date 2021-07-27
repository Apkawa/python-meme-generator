import os

import pytest

from meme_generator.cairo_draw.common import Point
from meme_generator.cairo_draw.font_manager import font_manager, FONTS_ROOT, FontManager
from meme_generator.cairo_draw.render import Render
from meme_generator.cairo_draw.text import Text, Font


def test_reinitialize():
    font_manager = FontManager()
    font_manager.init()
    own_files = [f for f in font_manager.conf.config_files if f.startswith("/tmp")]
    assert len(own_files) == 1
    assert len(font_manager._conf_files) == 1
    font_manager.init(default_emoji="Noto Color Emoji")
    own_files = [f for f in font_manager.conf.config_files if f.startswith("/tmp")]
    assert len(own_files) == 1

    assert len(font_manager._conf_files) == 2
    c_f = font_manager._conf_files
    font_manager.__del__()
    assert not [c for c in c_f if os.path.exists(c)]


def test_default_emoji_font(image_regression, fixture_path):
    font_manager.init(
        fonts=[fixture_path, FONTS_ROOT], default_emoji="Noto Color Emoji"
    )

    r = Render(300, 200)
    r.fill_bg()

    text = Text(
        "Noto Color Emoji\n" "😀😁😂😃😄😅😆😇😈😉😊😋😌😍😡😴", font=Font(size=11), width=300 - 10
    )
    r.draw_text(text, pos=Point(10, 10))

    image_regression(r.save_to_stream(), 0.005)


@pytest.mark.skip("No worked")
def test_change_default_emoji_font(image_regression, fixture_path):
    # FIXME
    # В общем, нельзя заменить FcConfig в рантайме, только во время рестарта
    # No work https://gitlab.gnome.org/GNOME/pango/-/issues/443
    # https://gitlab.gnome.org/GNOME/librsvg/-/issues/536#note_668610
    r = Render(300, 200)
    r.fill_bg()

    text = Text(
        "Apple Color Emoji\n" "😀😁😂😃😄😅😆😇😈😉😊😋😌😍😡😴\n", font=Font(size=11), width=300 - 10
    )
    r.draw_text(text, pos=Point(10, 0))

    font_manager.init(
        fonts=[fixture_path, FONTS_ROOT], default_emoji="Noto Color Emoji"
    )

    text = Text(
        "Noto Color Emoji\n" "😀😁😂😃😄😅😆😇😈😉😊😋😌😍😡😴", font=Font(size=11), width=300 - 10
    )
    r.draw_text(text, pos=Point(10, 50))

    image_regression(r.save_to_stream(), 0.001)
