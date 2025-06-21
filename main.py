#!/home/bin/env python
import logging, logging.config
from pathlib import Path
from json import dump, load
import typer

from models import CommandListing

logger = logging.getLogger(__name__)
"""
object structure:
{ <hash_id str> : {
    "command": <command str>,
    "description": <description str>,
    "tags": [<tag str>, <tag str>],
    "creation_date": <timestamp>,
    "last_updated": <timestamp
}}
"""
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


def validate_file_structure(data: dict):
    for v in iter(data.values()):
        if not isinstance(v, dict):
            logger.exception("invalid data schema in file")
            raise Exception("invalid data schema in file")


def file_exists(filename: str) -> bool:
    if Path(f"{Path(__file__).parent.resolve()}/{filename}").exists():
        return True
    else: return False

# CRUD operations
# CREATE
def create_json_file(filename: str, listing: CommandListing) -> None:
    with open(f"{filename}", "w") as f:
        dump(listing.to_dict(), f, indent=4)

def add_obj_to_file(filename: str, listing: CommandListing) -> None:
    with open(f"{filename}", "r") as f:
        data: dict = load(f)

    validate_file_structure(data)

    data.update(listing.to_dict())
    with open(f"{filename}", "w") as f:
        dump(data, f, indent=4)
    

# READ
def read_file(filename: str) -> dict:
    with open(f"{filename}", "r") as f:
        data: dict = load(f)
    return data
    
def get_listing_by_hash(data: dict, hash_id: str) -> CommandListing:
    if not hash_id in data.keys():
        raise KeyError("key not found")
    
    listing_data: dict = data[hash_id]
    listing = CommandListing.from_dict(listing_data)
    return listing


# UPDATE
"""
cannot update the command of a listing as the id of a listing is tied to the command.
altering the command string would just create a new listing.
"""
def update_listing_description(filename: str, id: str, new_description: str) -> None:
    data: dict = read_file(filename)
    listing = get_listing_by_hash(data, id)

    listing.description = new_description
    listing.new_last_updated()

    data[id] = listing.to_dict()
    with open(filename, 'w') as f:
        dump(data, f, indent=4)


def add_tag(filename: str, id: str, tag: str) -> None:
    pass

def remove_tag(filename: str, id: str, tag: str) -> None:
    pass

# DELETE
def delete_listing(filename: str, id: str) -> None:
    pass


def main() -> None:
    test_command = CommandListing(
        "ls -la",
        "lists all files and directories in the currentdirectory, in long format, including hidden",
        ["directory", "list", "bash"]
    )

    new_desc = '''\
    new description to test crud functions\
    '''
    update_listing_description("test_listing_file.json", test_command.hash_id, new_desc)


if __name__ == "__main__":
    _ = config_logging()
    main()
