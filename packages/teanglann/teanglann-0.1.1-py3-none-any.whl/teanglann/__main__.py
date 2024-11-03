"""Command-line interface."""

import click

from . import words


@click.group(invoke_without_command=True)
@click.pass_context
@click.version_option()
def cli(ctx) -> None:
    """Teanglann."""
    if ctx.invoked_subcommand is None:
        random_word()


@cli.command()
def random_word():
    """Retrieve a word randomly from teanglann.ie"""
    word = words.get_random_definition()
    click.echo(word)


@cli.command()
@click.argument("word_to_translate", nargs=1)
def translate(word_to_translate: str):
    """Search a word in Irish and get an English definition"""
    click.echo(f"Searching for translation: {word_to_translate}")
    translation = words.get_translation(word_to_translate)

    if translation:
        click.echo(translation)
    else:
        click.echo("No translation found", err=True)


if __name__ == "__main__":
    cli(prog_name="teanglann")  # pragma: no cover
