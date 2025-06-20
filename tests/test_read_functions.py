import pytest
import logging
import main
import io
import json
import tempfile
import pathlib
import logging


def test_read_file(caplog):
    dummy_data = main.CommandListing(
        "ls -la",
        "you know what this does",
        ["bash", "directory", "navigation"]
    )
    caplog.set_level(logging.INFO)
    with tempfile.NamedTemporaryFile(mode='w+', delete=True, encoding='utf-8') as temp_f:
        json.dump(dummy_data.to_dict(), temp_f)
        temp_f.flush()
        filename = temp_f.name
        main.logger.info(filename)
        temp_f.close()

        assert main.file_exists(filename)

        data = main.read_file(filename)
        assert isinstance(data, dict)
        main.validate_file_structure(data)
        
        data = main.read_listing_from_hash(filename, dummy_data.hash_id)
        assert isinstance(data, dict)
