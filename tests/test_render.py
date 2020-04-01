from io import BytesIO

from meme_generator.common import Rect, Font, Color
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
    r = Render(300, 200)
    r.fill_bg()


    r.draw_text(
        'top-right',
        bound=Rect(230, 0), font=Font(size=10))

    r.draw_text(
        'top-left',
        bound=Rect(0, 0), font=Font(size=10))

    fp = BytesIO()
    r.save(fp)
    fp.seek(0)

    image_regression(fp)



def test_draw_line(image_regression):
    r = Render(300, 200)
    r.fill_bg()
    r.draw_line(Rect(0, 0, 300, 200))
    r.draw_line(Rect(0, 200, 300, 0), line_width=3, color=Color.from_str("#F00"))
    fp = BytesIO()
    r.save(fp)
    fp.seek(0)

    image_regression(fp)


def test_draw_image(image_regression):
    r = Render(300, 1000)
    r.fill_bg()
    r.draw_image("/home/apkawa/code/python-meme-generator/meme_generator/memes/supermind/img/0.jpg")

    fp = BytesIO()
    r.save(fp)
    fp.seek(0)

    image_regression(fp)
