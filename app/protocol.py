"""
Message protocol for the match/comparison server.
All client<->server messages are JSON with a mandatory "type" field.
"""

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class ClientMessageType(str, Enum):
    CREATE_ROOM = "create_room"
    JOIN_ROOM = "join_room"
    REJOIN_ROOM = "rejoin_room"
    GRANT_CONSENT = "grant_consent"
    UPLOAD_PHOTO = "upload_photo"
    READY = "ready"
    LEAVE = "leave"
    SEND_CHAT = "send_chat"


class ServerMessageType(str, Enum):
    ROOM_CREATED = "room_created"
    PLAYER_JOINED = "player_joined"
    PLAYER_LEFT = "player_left"
    PLAYER_RECONNECTED = "player_reconnected"
    REJOIN_SUCCESS = "rejoin_success"
    CONSENT_REQUIRED = "consent_required"
    CONSENT_GRANTED = "consent_granted"
    PHOTO_RECEIVED = "photo_received"
    ALL_PHOTOS_IN = "all_photos_in"
    ANALYZING = "analyzing"
    COUNTDOWN = "countdown"
    REVEAL = "reveal"
    GROUP_REVEAL = "group_reveal"
    CHAT_MESSAGE = "chat_message"
    ERROR = "error"


class RoomType(str, Enum):
    DUO = "duo"
    GROUP = "group"


class FeatureComparison(BaseModel):
    """Single feature comparison between two faces."""
    feature: str
    label_a: str
    label_b: str
    match: bool


class CompatibilityResult(BaseModel):
    """Full compatibility result between two faces."""
    score: float  # 0.0-1.0
    percentage: int  # 0-100
    chemistry_label: str
    chemistry_color: str
    embedding_similarity: float
    feature_similarity: float
    feature_comparisons: List[FeatureComparison] = []
    shared_features: List[str] = []
    fusion_image: Optional[str] = None  # base64 data URL


def server_msg(msg_type: ServerMessageType, data: dict = None) -> dict:
    """Build a server->client message with a 'data' envelope."""
    msg = {"type": msg_type.value, "data": data or {}}
    return msg


def error_msg(message: str) -> dict:
    """Build an error message."""
    return {"type": ServerMessageType.ERROR.value, "data": {"message": message}}
