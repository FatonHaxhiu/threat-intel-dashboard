import pytest
from backend.fetch_feeds import fetch_alienvault

def test_fetch_alienvault_feed_returns_list():
    result = fetch_alienvault()
    assert isinstance(result, list)
    # You can add more checks if you know what the expected output looks like