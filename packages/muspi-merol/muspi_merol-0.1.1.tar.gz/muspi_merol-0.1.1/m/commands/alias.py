from rich import print, print_json
from typer import Typer
from typer.params import Argument, Option

from ..config.load import read_json_config, write_json_config
from ..config.types import Config
from ..utils.helpers import wrap_raw_config
from ..utils.path import global_store, local_store

app = Typer()


@app.command(help="Manage command aliases.")
def alias(
    alias: str = Argument("", help="The alias to create or retrieve."),
    command: str = Argument("", help="The command to alias."),
    local: bool = Option(True, "--global", "-g", flag_value=False, help="Persistent alias in User's home directory instead of this python venv."),
):
    store = local_store if local else global_store

    config = wrap_raw_config(read_json_config(store))

    match (alias, command):
        case ("", ""):
            if aliases := config["aliases"]:
                print_json(data=aliases)

        case (alias, ""):
            if command := config["aliases"][alias]:
                print(command)

        case (alias, command):
            new_config: Config = dict(config) if isinstance(config, dict) else {}  # type: ignore
            if config["aliases"]:
                new_config["aliases"][alias] = command
            else:
                new_config["aliases"] = {alias: command}
            write_json_config(store, new_config)
