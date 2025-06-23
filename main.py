#!/home/bin/env python
import logging, logging.config
from pathlib import Path
import typer
from json import load

from models import CommandListing
from store import CommandStore

logger = logging.getLogger(__name__)
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



def main() -> None:
    store = CommandStore("test_listing_file.json")
    logger.info(store._data)
    all_listings = store.get_all_listings()
    logger.info(f"number of listings is {len(all_listings)}")
    for listing in all_listings:
        logger.info(f"\n{listing.model_dump_json(indent=4, exclude={'hash_id'})}")


if __name__ == "__main__":
    _ = config_logging()
    main()
