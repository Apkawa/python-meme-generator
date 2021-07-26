from . import BorgarMeme


def test_borgar(image_regression):
    meme = BorgarMeme()
    fp = meme.render(["Как же хочется", "боргар"])
    image_regression(fp)
