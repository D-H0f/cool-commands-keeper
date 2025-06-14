#!/usr/local/bin/python3.13
import logging, logging.config
from os.path import exists
from pathlib import Path
import json
import hashlib
import argparse

# A class to represent the structure of a single command and its metadata
"""
object structure:
<hashvalue identifier dict key>:
<value of type dict ->
    "command": "command str value",
    "description": "description str value",
    "tags": <list of str object>
>
"""
class CommandListing:
    def __init__(self,
                 command: str,
                 description: str,
                 tags: list) -> None:

        if not isinstance(command, str) or not command.strip():
            raise ValueError("Command must be non-empty string")
        if not isinstance(description, str) or not description.strip():
            raise ValueError("Description must be non-empty string")
        if not isinstance(tags, list) or any(not isinstance(v, str) for v in tags):
            raise ValueError("tags must be a list containing only str values")
        self.command = command
        self._command_str = command.strip()
        self.description = description
        self.tags = tags
        self.hash_id = self._generate_hash(self._command_str)

    def _generate_hash(self, text: str) -> str:
        """
        Generates a SHA256 hash from the command string with whitespace removed.
        returned as a hexadecimal string.
        """
        return hashlib.sha256(text.encode('utf-8')).hexdigest()

    def to_dict(self):
        return {
            self.hash_id: {
                "command": self.command,
                "description": self.description,
                "tags": self.tags
            }
        }
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, CommandListing): return NotImplemented
        return self.hash_id == other.hash_id

    def __hash__(self):
        return hash(self._command_str)

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


# CRUD operations
def create_json_file(filename: str, listing: CommandListing) -> None:
    if Path(f"{Path(__file__).parent.resolve()}/{filename}.json").exists():
        logger.exception(f"file {filename}.json' already exists")
        raise Exception("this file already exists")
    with open(f"{filename}.json", "w") as f:
        json.dump(listing.to_dict(), f, indent=4)

    logger.info(f"created new file '{filename}.json")
    with open(f"{filename}.json") as f:
        logger.info(f.read())


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
    logger = config_logging()
    main()
