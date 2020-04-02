from io import BytesIO

from PIL import ImageDraw, Image

from meme_generator.common import Rect, Font, Color
from meme_generator.constants import Align
from meme_generator.helpers import get_text_bound, calculate_align
from meme_generator.render import Render


def test_draw_text(image_regression):
    r = Render(300, 200)
    r.fill_bg()

    r.draw_text(
        u"T̴͍͔̹͈̰̘͇͉̔̍͛̀̃͝e̸̡̛̦͖̫̙̜̱̱͚̤̥̽͐̋̏̀͌̈́͂͐̊̔͋͘͠s̶̡̨̛̮͍̯̪͚̹̖͕̦͖̫̳̐̓̋̿̔̒̒͐̑̂̚͝͝͝ţ̶̝̯̪͍̹̫̔͂̌͊̉̓̔͋̔̏̊̽́͜ͅ 😂",
        bound=Rect(30, 100))

    fp = BytesIO()
    r.save(fp)
    fp.seek(0)

    image_regression(fp)


def test_draw_long_text_wrap(image_regression):
    r = Render(300, 200)
    r.fill_bg()

    r.draw_text("Росатом готов к 3D-печати клапанов для аппаратов искусственной вентиляции легких"
                "😀😁😂😃😄😅😆😇😈😉😊😋😌😍😡😴"
                "😀😁😂😃😄😅😆😇😈😉😊😋😌😍😡😴"
                "😀😁😂😃😄😅😆😇😈😉😊😋😌😍😡😴"
                "�̷̧̫̭̫̀̀̀�̸̡̡̡̢̮͓̹̗̟͈̖͙̙̀̓̉̓́͗̋̔̓̂̇͜͠�̵̣͉͔̰͙̭͋͐͒͐͗͆́ͅ�̸̡̛̺̼̞̤̈́̀̽̀̀͛͒̈̎͊̈́͌͘̚ ̵̨͈͓̲̗̳̹͋̈͑̋́͝n̶̯̖͚̬̦͇̲͕͚̪͉͖̘̖̝̍́y̵̧̙̯̘̯͙̣͔̠̬̟͎̬̔͑̋͑̉͗̕ǎ̵̪̙̤̳̳͍̼̹͓̼̿͒̏̄̿͑̿͋̉͜",
                bound=Rect(10, 0, w=300), font=Font(size=11))

    fp = BytesIO()
    r.save(fp)
    fp.seek(0)

    image_regression(fp)


def test_draw_multiple_texts(image_regression):
    r = Render(800, 400)
    r.fill_bg()
    r.draw_line(Rect(400, 0, 400, 400), line_width=3)

    text_container = Rect(400, 0, 400, 400)

    test_aligns = [
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
    font = Font(size=10)
    for align in test_aligns:
        text = str(align)
        text_bound = get_text_bound(text, font=font)
        align_text_bound = calculate_align(text_container, text_bound, align=align)

        r.draw_text(
            text,
            bound=align_text_bound, font=Font(size=10))

    image_regression(r.save_to_stream())


def _test_draw_line(image_regression):
    r = Render(300, 200)
    r.fill_bg()
    r.draw_line(Rect(0, 0, 300, 200))
    r.draw_line(Rect(0, 200, 300, 0), line_width=3, color=Color.from_str("#F00"))
    fp = BytesIO()
    r.save(fp)
    fp.seek(0)

    image_regression(fp)


def make_test_image(text="Hello world", size=(100, 30)):
    img = Image.new('RGB', size, color=(73, 109, 137))

    d = ImageDraw.Draw(img)
    d.text((10, 10), text, fill=(255, 255, 0))

    return img


def test_draw_image(image_regression):
    r = Render(300, 100)
    r.fill_bg()

    r.draw_image(make_test_image("Nya"))

    fp = BytesIO()
    r.save(fp)
    fp.seek(0)

    image_regression(fp)
