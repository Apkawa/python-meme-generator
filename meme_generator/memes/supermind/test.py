
from . import SupermindMeme

def test_supermind(image_regression):
    meme = SupermindMeme()
    fp = meme.render(list(map(str, range(8))))
    image_regression(fp)