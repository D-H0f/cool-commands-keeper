import hashlib


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

    def to_dict(self) -> dict:
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
