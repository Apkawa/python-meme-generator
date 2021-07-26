from io import BytesIO

from PIL import ImageDraw, Image

from meme_generator import common
from meme_generator.common import Rect, Color, Point
from meme_generator.text import Font, Text
from meme_generator.render import Render


def test_draw_text(image_regression):
    r = Render(300, 200)
    r.fill_bg()

    r.draw_text(
        Text(
            u"T̴͍͔̹͈̰̘͇͉̔̍͛̀̃͝e̸̡̛̦͖̫̙̜̱̱͚̤̥̽͐̋̏̀͌̈́͂͐̊̔͋͘͠s̶̡̨̛̮͍̯̪͚̹̖͕̦͖̫̳̐̓̋̿̔̒̒͐̑̂̚͝͝͝ţ̶̝̯̪͍̹̫̔͂̌͊̉̓̔͋̔̏̊̽́͜ͅ 😂",
            font=Font(size=24),
        ),
        pos=Point(30, 100),
    )

    image_regression(r.save_to_stream())


def test_draw_long_text_wrap(image_regression):
    r = Render(300, 200)
    r.fill_bg()

    text = Text(
        "Росатом готов к 3D-печати клапанов для аппаратов искусственной вентиляции легких"
        "😀😁😂😃😄😅😆😇😈😉😊😋😌😍😡😴"
        "😀😁😂😃😄😅😆😇😈😉😊😋😌😍😡😴"
        "😀😁😂😃😄😅😆😇😈😉😊😋😌😍😡😴"
        "�̷̧̫̭̫̀̀̀�̸̡̡̡̢̮͓̹̗̟͈̖͙̙̀̓̉̓́͗̋̔̓̂̇͜͠�̵̣͉͔̰͙̭͋͐͒͐͗͆́ͅ�̸̡̛̺̼̞̤̈́̀̽̀̀͛͒̈̎͊̈́͌͘̚ ̵̨͈͓̲̗̳̹͋̈͑̋́͝n̶̯̖͚̬̦͇̲͕͚̪͉͖̘̖̝̍́y̵̧̙̯̘̯͙̣͔̠̬̟͎̬̔͑̋͑̉͗̕ǎ̵̪̙̤̳̳͍̼̹͓̼̿͒̏̄̿͑̿͋̉͜",
        font=Font(size=11),
        width=300 - 10,
    )
    r.draw_text(text, pos=Point(10, 0))

    image_regression(r.save_to_stream())


def test_draw_line(image_regression):
    r = Render(300, 200)
    r.fill_bg()
    r.draw_line([Point(0, 0), Point(300, 200)])
    r.draw_line(
        [Point(0, 200), Point(300, 0)], line_width=3, color=Color.from_str("#F00")
    )

    image_regression(r.save_to_stream())


def make_test_image(text="Hello world", size=(100, 30)):
    img = Image.new("RGB", size, color=(73, 109, 137))

    d = ImageDraw.Draw(img)
    d.text((10, 10), text, fill=(255, 255, 0))

    return img


def test_draw_image(image_regression):
    r = Render(300, 100)
    r.fill_bg()

    r.draw_image(common.Image(make_test_image("Nya")))

    fp = BytesIO()
    r.save(fp)
    fp.seek(0)

    image_regression(fp)
