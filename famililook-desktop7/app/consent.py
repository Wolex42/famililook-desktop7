"""
BIPA consent tracking for match rooms.
All consent data is in-memory only — never persisted.
"""

from typing import List
from .rooms import MatchRoom


CONSENT_TEXT = (
    "I consent to my photo being processed in memory for facial comparison. "
    "Photos are never saved to disk and are deleted when this session ends."
)


def get_pending_consents(room: MatchRoom) -> List[str]:
    """Return list of player IDs who haven't consented yet."""
    return [
        pid for pid in room.players
        if not room.consents.get(pid, False)
    ]


def all_consented(room: MatchRoom) -> bool:
    """Check if all players in the room have consented."""
    return room.all_consented
