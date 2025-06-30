#!./venv/bin/python
import logging, logging.config
from pathlib import Path
import rich
import typer
from json import load, dumps
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
def list_all(
    filename: Annotated[str, typer.Option(prompt=True)]
):
    store = CommandStore(filename)
    listings: list[CommandListing] = store.get_all_listings()
    for listing in listings:
        rich.print(f"Listing ID is {listing.hash_id}")
        rich.print(listing.model_dump_json(indent=4, exclude={'hash_id'}))

@app.command(name='get')
def get_listing(
    filename: Annotated[str, typer.Option(prompt=True)],
    id: Annotated[str, typer.Option(prompt=True)]    
):
    listing = CommandStore(filename).get_listing(id)
    rich.print(dumps(listing.model_dump(mode='json'), indent=4))

@app.command(name='update')    
def update_listing(
    filename: Annotated[str, typer.Option("--filename", "-f", prompt=True)],
    id: Annotated[str, typer.Option("--id", "-i", prompt=True)],
    description: Annotated[str|None, typer.Option("--desc", "-d")] = None,
    tags: Annotated[str|None, typer.Option("--tags", "-t")] = None
):
    if description is None and tags is None:quit()
    store = CommandStore(filename)
    listing = store.get_listing(id)

    if not description is None:
        listing.description = description
    if not tags is None:
        listing.tags = tags.split(" ")
    
    store.update_listing(listing)


def main() -> None:
    
    app()



if __name__ == "__main__":
    _ = config_logging()
    main()
