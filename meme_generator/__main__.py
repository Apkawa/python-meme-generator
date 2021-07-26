import shutil
from typing import List, BinaryIO

import click

from meme_generator.memes.supermind import SupermindMeme


@click.group("memes")
@click.option('-o', '--output', type=click.File('wb'))
@click.pass_context
def cli(ctx: click.Context, output: BinaryIO) -> None:
    ctx.ensure_object(dict)
    ctx.obj['output'] = output


@cli.command()
@click.pass_context
@click.argument("texts", nargs=-1)
def supermind(ctx: click.Context, texts: List[str]) -> None:
    meme = SupermindMeme()
    fp = meme.render(texts)
    shutil.copyfileobj(fp, ctx.obj['output'])


cli()
