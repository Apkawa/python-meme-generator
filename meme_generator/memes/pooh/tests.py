from . import PoohMeme


def test_pooh(image_regression):
    meme = PoohMeme()
    fp = meme.render([
        "Работать",
        "Делать генератор мемов",
    ])
    image_regression(fp)
