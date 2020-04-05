from meme_generator.common import Rect, Point, Line, Color
from meme_generator.text import Font, Text
from meme_generator.constants import TextStyle
from meme_generator.render import Render


def test_text_style(image_regression):
    r = Render(400, 200)
    r.fill_bg()

    for i, style in enumerate([TextStyle.NORMAL, TextStyle.OBLIQUE, TextStyle.ITALIC]):
        font = Font(size=16, style=style)

        text = Text(f"{style}: test 🌚 🍆", font=font)
        r.draw_text(
            text,
            pos=Point(20, (30 * i) + 30))

    image_regression(r.save_to_stream())


def test_text_border(image_regression):
    r = Render(400, 200)
    r.fill_bg()
    font = Font("Impact", size=25)

    text = Text(f"TEST з̴̢̺̤̦̬̩̱̺̭̠͚̀̒͛̈̏͌̂̔̎̑́̇͜͝͝а̶̢̟̦̝͎̖̘̯̦͚͚͉̖̒̊̄̅͌̈́̈ͅл̷̢̧̨͉̩͉͚̭͎̗̤̤̓̉̀̔̈́̓г̵̨̙̯̖͖̠͈̙͇̼̟̮̦̍о̷̻̖̮͉̜̰̲̪̅͋̃̃͒͜",
                font=font,
                color=Color.from_str("#FFF"),
                border=Line(width=1, color=Color.from_str("#F00"))
                )
    r.draw_text(
        text,
        pos=Point(20, 50))

    image_regression(r.save_to_stream())
