from meme_generator.cairo_draw.common import Point, Line, Color
from meme_generator.cairo_draw.text import Font, Text
from meme_generator.cairo_draw.constants import TextStyle
from meme_generator.cairo_draw.render import Render


def test_text_style(image_regression):
    r = Render(400, 200)
    r.fill_bg()

    for i, style in enumerate(
        [
            TextStyle.OBLIQUE,
            TextStyle.ITALIC,
            TextStyle.SMALL_CAPS,
            TextStyle.UPPER_CAPS,
            TextStyle.UPPER_CAPS | TextStyle.ITALIC,
        ]
    ):
        font = Font(size=13, style=style)

        text = Text(f"{style}: test 🌚 🍆", font=font)
        r.draw_text(text, pos=Point(20, (30 * i) + 30))

    image_regression(r.save_to_stream())


def test_text_border(image_regression):
    r = Render(400, 200)
    r.fill_bg()
    font = Font("Impact", size=25)

    text = Text(
        f"TEST з̴̢̺̤̦̬̩̱̺̭̠͚̀̒͛̈̏͌̂̔̎̑́̇͜͝͝а̶̢̟̦̝͎̖̘̯̦͚͚͉̖̒̊̄̅͌̈́̈ͅл̷̢̧̨͉̩͉͚̭͎̗̤̤̓̉̀̔̈́̓г̵̨̙̯̖͖̠͈̙͇̼̟̮̦̍о̷̻̖̮͉̜̰̲̪̅͋̃̃͒͜",
        font=font,
        color=Color.from_str("#FFF"),
        border=Line(width=1, color=Color.from_str("#F00")),
    )
    r.draw_text(text, pos=Point(20, 50))

    image_regression(r.save_to_stream())
