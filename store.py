from json import dump, load, JSONDecodeError
from pathlib import Path
import logging
from pydantic import ValidationError

from models import CommandListing

logger = logging.getLogger(__name__)

class CommandStore:
    """
    Manages all CRUD operations for CommandListings.
    """
    def __init__(self, filepath: str | Path):
        self.filepath = Path(filepath)
        self._data: dict[str, CommandListing] = self._load()

    def _load(self) -> dict[str, CommandListing]:
        """
        Loads listings from a JSON file into memory.
        """
        if not self.filepath.exists():
            return {}
        
        try:
            with self.filepath.open('r') as f:
                raw_data: dict = load(f)
        except JSONDecodeError as e:
            raise Exception(f"could not decode JSON data from {self.filepath}") from e

        listings = {}
        for hash_id, listing_data in raw_data.items():
            try:
                #TODO add more robust validation
                listing_obj = CommandListing.model_validate(listing_data)
                listings[hash_id] = listing_obj
            except ValidationError as e:
                logger.warning(f"Skipping invalid record with id '{hash_id}': {e}")
                continue
        return listings
    
    def _save(self) -> None:
        """
        Saves the current in-memory data back to the JSON file.
        """
        raw_data = {listing.hash_id: listing.model_dump(mode='json', exclude={'hash_id'})
            for listing in self._data.values()
        }
        logger.info(raw_data)
        
        with self.filepath.open('w') as f:
            dump(raw_data, f, indent=4)

    # Public CRUD methods
    # CREATE
    def add_listing(self, listing: CommandListing):
        """
        adds a new CommandListing to the store and saves it to the file.
        """
        if listing.hash_id in self._data:
            raise ValueError(f"A listing with the command {listing.command} already exists")

        self._data[listing.hash_id] = listing
        self._save()

    # READ
    def get_listing(self, hash_id: str) -> CommandListing:
        """
        Retrieves a single listing by its hash id.
        """
        if hash_id not in self._data.keys():
            raise Exception(f"No listing found with ID: {hash_id}")

        return self._data[hash_id]
    
    def get_all_listings(self) -> list[CommandListing]:
        """
        Returns a list of all listing objects.
        """
        return list(self._data.values())

    # UPDATE
    def update_listing(self, listing: CommandListing) -> None:
        """
        Updates an existing command listing.
        """
        if listing.hash_id not in self._data:
            raise Exception(f"listing '{listing.hash_id}' cannot be updated, does not exist.")
        listing.new_last_updated()
        self._data[listing.hash_id] = listing
        self._save()

    # DELETE
    def delete_listing(self, hash_id: str):
        """
        Deletes a listing.
        """
        if hash_id not in self._data.keys():
            raise Exception(f"listing '{hash_id}' does not exist")
        del self._data[hash_id]
        self._save()
