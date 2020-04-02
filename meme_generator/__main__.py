import shutil

import click

from meme_generator.memes.supermind import SupermindMeme


@click.group("memes")
@click.option('-o', '--output', type=click.File('wb'))
@click.pass_context
def cli(ctx, output):
    ctx.ensure_object(dict)
    ctx.obj['output'] = output



@cli.command()
@click.pass_context
@click.argument("texts", nargs=-1)
def supermind(ctx, texts):
    meme = SupermindMeme()
    fp = meme.render(texts)
    shutil.copyfileobj(fp, ctx.obj['output'])


cli()

