from . import SupermindMeme


def test_supermind(image_regression):
    meme = SupermindMeme()
    fp = meme.render([
        "Работать",
        "Читать пикабу",
        "Деградировать",
        "Делать генератор мемов",
        "Р̷̨̡͔̣͉̜̳͙̪̹̘͕̩̳͚͑а̸̯̬̹̪̹̹̗̜̣͋̄̓̇̕б̶̧̧̟̟̗̣̟͇̗͍̥̺̇̓̌̓̍̂͗̈͂̇̇̕͝ͅо̵͇͔̣̥̠̳͚̼͇̱̩̗̣̃́̓͋̊̊̀̅̾̊̌͝͝т̵͔̻͙̋́̈̓͛̚ӓ̵̡̲̮͉̳̂̍̋̏͌̏͛͋̒̊͛͝ё̷̨͈̤̰̍͝т̶̡̨̺̺̫̳̻̙̦̟͖̬̻̗͋̇̕",
        "🍆🍆🍆🍆🍆🍆",
    ])
    image_regression(fp)
