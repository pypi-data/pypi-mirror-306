from sys import argv

from rich.console import Console
from rich.highlighter import ISO8601Highlighter
from rich.text import Text
from typer import Typer

from ..config.load import load_config
from ..utils.print_version import print_version
from ..utils.register import get_commands

app = Typer(help="CLI utilities for personal use", no_args_is_help=True)


@app.command()
def version():
    """Print the version of `m` and Python and quit."""

    print_version()


for sub_app in get_commands():
    if app.info.name:
        app.add_typer(sub_app)
    else:
        app.registered_commands.extend(sub_app.registered_commands)


config = load_config()

for alias, command in config["aliases"].items():

    @app.command(name=alias, help=f"alias of {command!r}", context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
    def _(cmd=command):
        from shlex import split
        from subprocess import Popen

        console = Console()
        console.print(
            "\n [d]>>",
            *(ISO8601Highlighter()(Text(i if " " not in i else repr(i))) for i in split(cmd)),
            end=" ",
            highlight=False,
        )
        console.print(" ".join(argv[2:]), style="yellow", end="\n\n")

        p = Popen(split(cmd) + argv[2:], shell=True)
        exit(p.wait())
