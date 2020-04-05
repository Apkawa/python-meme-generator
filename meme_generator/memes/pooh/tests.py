from . import PoohMeme


def test_pooh(image_regression):
    meme = PoohMeme()
    fp = meme.render([
        "Работать",
        "Делать генератор мемов  🐻",
    ])
    image_regression(fp)

def test_long_text(image_regression):
    meme = PoohMeme()
    fp = meme.render([
        "Писать короткий текст",
        "Ввести налог на каждого "
        "ребёнка из которого будут "
        "покрываться расходы на "
        "удовлетворение ущерба копрорациям и другим шарагам",
    ])
    image_regression(fp)
