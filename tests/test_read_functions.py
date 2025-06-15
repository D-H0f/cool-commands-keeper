import pytest
import logging
import main
import io
import json

dummy_data = main.CommandListing(
    "ls -la",
    "you know what this does",
    ["bash", "directory", "navigation"]
)

def test_read_file():
    json_data = json.dumps(dummy_data.to_dict())
    simulated_file = io.StringIO(json_data)
