import hashlib
import datetime
import logging
from pydantic import BaseModel, Field, computed_field

logger = logging.getLogger(__name__)
class CommandListing(BaseModel):
    command: str = Field(min_length=1)
    description: str = Field(min_length=1)
    tags: list[str] = Field(default_factory=list)
    creation_date: datetime.datetime = Field(default_factory=datetime.datetime.now)
    last_updated: datetime.datetime = Field(default_factory=datetime.datetime.now)



    @computed_field
    @property
    def hash_id(self) -> str:
        """
        Generates a SHA256 hash from the command string with whitespace removed.
        returned as a hexadecimal string.
        """
        cleaned_command = self.command.strip()
        return hashlib.sha256(cleaned_command.encode('utf-8')).hexdigest()

    def new_last_updated(self) -> None:
        self.last_updated: datetime.datetime = datetime.datetime.now()
