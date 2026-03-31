"""Tests for protocol.py — Message types and schemas."""

import pytest
from app.protocol import (
    ClientMessageType,
    ServerMessageType,
    RoomType,
    CompatibilityResult,
    FeatureComparison,
    server_msg,
    error_msg,
)


class TestClientMessageTypes:
    def test_all_types_are_strings(self):
        assert ClientMessageType.CREATE_ROOM == "create_room"
        assert ClientMessageType.JOIN_ROOM == "join_room"
        assert ClientMessageType.GRANT_CONSENT == "grant_consent"
        assert ClientMessageType.UPLOAD_PHOTO == "upload_photo"
        assert ClientMessageType.READY == "ready"
        assert ClientMessageType.LEAVE == "leave"

    def test_has_6_types(self):
        assert len(ClientMessageType) == 6


class TestServerMessageTypes:
    def test_all_types_are_strings(self):
        assert ServerMessageType.ROOM_CREATED == "room_created"
        assert ServerMessageType.PLAYER_JOINED == "player_joined"
        assert ServerMessageType.PLAYER_LEFT == "player_left"
        assert ServerMessageType.CONSENT_REQUIRED == "consent_required"
        assert ServerMessageType.PHOTO_RECEIVED == "photo_received"
        assert ServerMessageType.ALL_PHOTOS_IN == "all_photos_in"
        assert ServerMessageType.ANALYZING == "analyzing"
        assert ServerMessageType.COUNTDOWN == "countdown"
        assert ServerMessageType.REVEAL == "reveal"
        assert ServerMessageType.GROUP_REVEAL == "group_reveal"
        assert ServerMessageType.ERROR == "error"

    def test_has_12_types(self):
        assert len(ServerMessageType) == 12


class TestRoomType:
    def test_duo(self):
        assert RoomType.DUO == "duo"

    def test_group(self):
        assert RoomType.GROUP == "group"


class TestFeatureComparison:
    def test_matching_feature(self):
        fc = FeatureComparison(feature="eyes", label_a="Almond", label_b="Almond", match=True)
        assert fc.match is True
        assert fc.feature == "eyes"

    def test_non_matching_feature(self):
        fc = FeatureComparison(feature="nose", label_a="Button", label_b="Straight", match=False)
        assert fc.match is False


class TestCompatibilityResult:
    def test_minimal(self):
        result = CompatibilityResult(
            score=0.78,
            percentage=78,
            chemistry_label="Magnetic Match",
            chemistry_color="#8B5CF6",
            embedding_similarity=0.82,
            feature_similarity=0.5,
        )
        assert result.percentage == 78
        assert result.fusion_image is None
        assert result.feature_comparisons == []

    def test_with_features(self):
        result = CompatibilityResult(
            score=0.85,
            percentage=85,
            chemistry_label="Feature Twins",
            chemistry_color="#FFD700",
            embedding_similarity=0.9,
            feature_similarity=0.75,
            feature_comparisons=[
                FeatureComparison(feature="eyes", label_a="Almond", label_b="Almond", match=True),
            ],
            shared_features=["eyes"],
        )
        assert len(result.feature_comparisons) == 1
        assert result.shared_features == ["eyes"]

    def test_serialization(self):
        result = CompatibilityResult(
            score=0.5,
            percentage=50,
            chemistry_label="Interesting Contrast",
            chemistry_color="#14B8A6",
            embedding_similarity=0.6,
            feature_similarity=0.3,
        )
        data = result.model_dump()
        assert isinstance(data, dict)
        assert data["percentage"] == 50


class TestServerMsg:
    def test_includes_type_and_data(self):
        msg = server_msg(ServerMessageType.ROOM_CREATED, {"room_code": "1234"})
        assert msg["type"] == "room_created"
        assert msg["data"]["room_code"] == "1234"

    def test_empty_data(self):
        msg = server_msg(ServerMessageType.ALL_PHOTOS_IN)
        assert msg["type"] == "all_photos_in"
        assert msg["data"] == {}

    def test_error_msg(self):
        msg = error_msg("Something went wrong")
        assert msg["type"] == "error"
        assert msg["data"]["message"] == "Something went wrong"

    def test_multiple_fields(self):
        msg = server_msg(
            ServerMessageType.ANALYZING,
            {"step": 2, "total_steps": 4, "description": "Computing embeddings..."},
        )
        assert msg["data"]["step"] == 2
        assert msg["data"]["total_steps"] == 4
