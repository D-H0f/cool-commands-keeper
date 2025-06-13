#!/usr/local/bin/python3.13
import logging, logging.config
from pathlib import Path
import json

# A class to represent the structure of a single command and its metadata
class CommandListing:
    def __init__(self,
                 command: str,
                 description: str,
                 tags: list) -> None:
        self.command = command
        self.description = description
        self.tags = tags


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


def main() -> None:
    """
    logger.info("testing info message")
    logger.debug("testing debug message")
    logger.warning("testing warn message")
    logger.error("testing error message")
    logger.exception("testing exception message")
    logger.critical("testing critical message")
    """


if __name__ == "__main__":
    logger = config_logging()
    main()
