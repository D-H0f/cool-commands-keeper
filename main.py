#!/home/bin/env python
import logging, logging.config
from pathlib import Path
import json
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
        config_settings = json.load(filein)
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
        json.dump(listing.to_dict(), f, indent=4)

    logger.info(f"created new file '{filename}.json")
    with open(f"{filename}", "r") as f:
        logger.info(f.read())

def add_obj_to_file(filename: str, listing: CommandListing) -> None:
    with open(f"{filename}", "r") as f:
        data: dict = json.load(f)

    validate_file_structure(data)

    data.update(listing.to_dict())
    with open(f"{filename}", "w") as f:
        json.dump(data, f, indent=4)
    

# READ
def read_file(filename: str) -> dict:
    with open(f"{filename}", "r") as f:
        data: dict = json.load(f)
    return data
    
def get_listing(filename: str, hash_id: str) -> CommandListing:
    with open(filename, 'r') as f:
        data: dict = json.load(f)

    if not hash_id in data.keys():
        raise KeyError("key not found")
    
    listing_data: dict = data[hash_id]
    listing = CommandListing(
        listing_data["command"],
        listing_data["description"],
        listing_data["tags"],
        listing_data["creation_date"],
        listing_data["last_updated"]
    )
    return listing


# UPDATE
"""
cannot update the command of a listing as the id of a listing is tied to the command.
altering the command string would just create a new listing.
"""
def update_listing_description(filename: str, id: str, new_description: str) -> None:
    pass

def add_tag(filename: str, id: str, tag: str) -> None:
    pass

def remove_tag(filename: str, id: str, tag: str) -> None:
    pass

# DELETE
def delete_listing(filename: str, id: str) -> None:
    pass


def main() -> None:
    # logger.info("testing info message")
    # logger.debug("testing debug message")
    # logger.warning("testing warn message")
    # logger.error("testing error message")
    # logger.exception("testing exception message")
    # logger.critical("testing critical message")
    test_command = CommandListing(
        "ls -la",
        "lists all files and directories in the currentdirectory, in long format, including hidden",
        ["directory", "list", "bash"]
    )

    logger.info(test_command)
    logger.info(test_command.hash_id)
    logger.info(test_command.to_dict)
    create_json_file("test_file", test_command)


if __name__ == "__main__":
    _ = config_logging()
    main()
