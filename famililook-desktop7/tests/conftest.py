"""Shared test fixtures for the match server."""

import pytest
from unittest.mock import AsyncMock
from app.rooms import Player


@pytest.fixture
def mock_ws():
    """Create a mock WebSocket."""
    ws = AsyncMock()
    return ws


def make_player(player_id="p1", name="Test", ws=None):
    """Create a player with a mocked WebSocket."""
    if ws is None:
        ws = AsyncMock()
    return Player(player_id, name, ws)


# A small test JPEG (1x1 white pixel)
TEST_PHOTO_BYTES = (
    b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00'
    b'\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t'
    b'\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a'
    b'\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342'
    b'\xff\xc0\x00\x0b\x08\x00\x01\x00\x01\x01\x01\x11\x00'
    b'\xff\xc4\x00\x1f\x00\x00\x01\x05\x01\x01\x01\x01\x01\x01\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b'
    b'\xff\xda\x00\x08\x01\x01\x00\x00?\x00T\xdb\x9e\xa7\x13\xa2\x8a('
    b'\x00\xa2\x8a(\x00\xff\xd9'
)

# Mock 512-dim embedding (all zeros except first element)
MOCK_EMBEDDING_A = [1.0] + [0.0] * 511
MOCK_EMBEDDING_B = [0.7, 0.7] + [0.0] * 510

# Mock attributes response from desktop3
MOCK_ATTRS_A = {
    "parts": {
        "eyes": {"label": "Almond"},
        "eyebrows": {"label": "Arched"},
        "smile": {"label": "Wide"},
        "nose": {"label": "Button"},
        "face_shape": {"label": "Oval"},
        "skin": {"label": "Fair"},
        "hair": {"label": "Curly"},
        "ears": {"label": "Detached"},
    }
}

MOCK_ATTRS_B = {
    "parts": {
        "eyes": {"label": "Almond"},  # same
        "eyebrows": {"label": "Straight"},  # different
        "smile": {"label": "Wide"},  # same
        "nose": {"label": "Straight"},  # different
        "face_shape": {"label": "Oval"},  # same
        "skin": {"label": "Medium"},  # different
        "hair": {"label": "Curly"},  # same
        "ears": {"label": "Attached"},  # different
    }
}
