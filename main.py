#!/home/bin/env python
import logging, logging.config
from pathlib import Path
from json import dump, load
import typer

from models import CommandListing
from store import CommandStore

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

def main() -> None:
    pass


if __name__ == "__main__":
    _ = config_logging()
    main()
