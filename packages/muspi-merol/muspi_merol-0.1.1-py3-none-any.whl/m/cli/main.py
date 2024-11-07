from sys import argv

from typer import Typer

from ..config.load import load_config
from ..utils.console import console, print_version
from ..utils.register import get_commands

app = Typer(help="CLI utilities for personal use", no_args_is_help=True, add_completion=False)


@app.command()
def version():
    """Print the version of `m` and Python and quit."""

    print_version()


# load other commands

for sub_app in get_commands():
    if sub_app.info.name:
        app.add_typer(sub_app)
    else:
        app.registered_commands.extend(sub_app.registered_commands)


# load aliases

config = load_config()

for alias, command in config["aliases"].items():

    @app.command(name=alias, help=f"alias of {command!r}", context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
    def _(cmd=command):
        from shlex import split
        from subprocess import Popen

        console.print("\n [d]>>", *split(cmd), end=" ", style="violet")
        console.print(" ".join(argv[2:]), style="yellow", end="\n\n")

        code = Popen(split(cmd) + argv[2:]).wait()
        exit(code)
