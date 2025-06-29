#!/home/bin/env python
import logging, logging.config
from pathlib import Path
import typer
from json import load
from typing_extensions import Annotated

from models import CommandListing
from store import CommandStore

logger = logging.getLogger(__name__)
app = typer.Typer()

def config_logging() -> logging.Logger:
    cur_dir = Path(__file__).parent.resolve()
    logs_dir = f"{cur_dir}/logs"
    if not Path(logs_dir).exists():
        Path(logs_dir).mkdir()
    config_file = f"{cur_dir}/configs/logging_config.json"

    with open(config_file) as filein:
        config_settings = load(filein)
    logging.config.dictConfig(config_settings)

    return logging.getLogger(__file__)


@app.command(name='add')
def add(
    filename: Annotated[str, typer.Option(prompt=True)],
    command: Annotated[str, typer.Option(prompt=True)],
    description: Annotated[str, typer.Option(prompt=True)],
    tags: Annotated[str, typer.Option(prompt=True)]
):
    tags_form = tags.split(" ")
    listing = CommandListing(command=command, description=description, tags=tags_form)
    store = CommandStore(filename)
    store.add_listing(listing)
    logger.info(store.get_all_listings())

@app.command(name='list')
def list_all():
    logger.info("'list' command was triggered, test successful")


def main() -> None:
    
    app()



if __name__ == "__main__":
    _ = config_logging()
    main()
