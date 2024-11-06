from typing import Annotated

import typer

from furious.cli.commands.run import run_app
from furious.cli.commands.shell import embed as embed_shell
from furious.cli.config import Config
from furious.cli.setup import set_up_furious

tpr = typer.Typer(callback=set_up_furious)


# TODO: Try to  implement as a type
def FromConfig(name):
    """
    Constructs annotation based on cli.config.Config pydantic model.
    Sets the correct type and the default value.
    """
    field = Config.model_fields[name]
    return Annotated[
        field.annotation, typer.Option(default_factory=lambda: field.default)
    ]


@tpr.command()
def shell(type: FromConfig("shell")):
    embed_shell(type)


@tpr.command()
def run(host: FromConfig("host"), port: FromConfig("port")):
    run_app(host, port)


if __name__ == "__main__":
    tpr()
