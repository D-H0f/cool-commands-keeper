import pytest
import main
import logging

def test_command_listing_creation_and_logging(caplog):
    dummy_data = main.CommandListing(
        'ls -la',
        'you know what this does',
        ['bash', 'directory']
    )

    caplog.set_level(logging.INFO)
    main.logger.info(f"dummy data created:")
    main.logger.info(dummy_data.to_dict())

    assert isinstance(dummy_data.hash_id, str)
    assert dummy_data.command == 'ls -la'
    assert dummy_data.description == 'you know what this does'
    assert isinstance(dummy_data.tags, list)

    assert "dummy data created:" in caplog.text
