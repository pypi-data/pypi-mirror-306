from typer import Typer

from ..config.load import load_config
from ..utils.cmd import get_runner
from ..utils.register import get_commands

app = Typer(help="CLI utilities for personal use", no_args_is_help=True, add_completion=False)


# load other commands

for sub_app in get_commands():
    if sub_app.info.name:
        app.add_typer(sub_app)
    else:
        app.registered_commands.extend(sub_app.registered_commands)


# load aliases

config = load_config()

for alias, command in config["aliases"].items():
    app.command(
        name=alias,
        help=f"alias of {command!r}",
        context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
        add_help_option=False,
    )(get_runner(command))
