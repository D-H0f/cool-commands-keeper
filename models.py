import hashlib
import datetime


class CommandListing:
    def __init__(self,
                 command: str,
                 description: str,
                 tags: list,
                 creation_date: str|None = None,
                 last_updated: str|None = None
                 ) -> None:

        if not isinstance(command, str) or not command.strip():
            raise ValueError("Command must be non-empty string")
        if not isinstance(description, str) or not description.strip():
            raise ValueError("Description must be non-empty string")
        if not isinstance(tags, list) or any(not isinstance(v, str) for v in tags):
            raise ValueError("tags must be a list containing only str values")

        self.command: str = command
        self._command_str: str = command.strip()
        self.description: str = description
        self.tags: list[str] = tags
        self.hash_id: str = self._generate_hash(self._command_str)

        if creation_date is None:
            self.creation_date = datetime.datetime.now().isoformat()
        else:
            self.creation_date = creation_date

        if last_updated is None:
            self.last_updated: str = self.creation_date
        else:
            self.last_updated: str = last_updated
    def _generate_hash(self, text: str) -> str:
        """
        Generates a SHA256 hash from the command string with whitespace removed.
        returned as a hexadecimal string.
        """
        return hashlib.sha256(text.encode('utf-8')).hexdigest()

    def new_last_updated(self) -> None:
        self.last_updated: str = datetime.datetime.now().isoformat()

    def to_dict(self) -> dict:
        return {
            self.hash_id: {
                "command": self.command,
                "description": self.description,
                "tags": self.tags,
                "created": self.creation_date,
                "last_updated": self.last_updated
            }
        }
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, CommandListing): return NotImplemented
        return self.hash_id == other.hash_id

    def __hash__(self):
        return hash(self._command_str)

    @classmethod
    def from_dict(cls, data: dict) -> 'CommandListing':
        if not all([
            "command" in data.keys(),
            "description" in data.keys(),
            "tags" in data.keys(),
            "creation_date" in data.keys(),
            "last_updated" in data.keys()
        ]):
            raise ValueError("dict does not match data schema")

        return cls(
            data["command"],
            data["description"],
            data["tags"],
            data["creation_date"],
            data["last_updated"]
        )
