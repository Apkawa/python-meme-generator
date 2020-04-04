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


def test_supermind_long_text(image_regression):
    meme = SupermindMeme()
    fp = meme.render([
        "Писать короткий текст",
        "Ввести налог на каждого "
        "ребёнка из которого будут "
        "покрываться расходы на "
        "удовлетворение ущерба копрорациям и другим шарагам",
    ])
    image_regression(fp)
