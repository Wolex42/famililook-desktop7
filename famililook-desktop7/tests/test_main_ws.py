"""Integration tests for the WebSocket endpoint."""

import json
import base64
import pytest
from unittest.mock import patch, AsyncMock, MagicMock

from fastapi.testclient import TestClient
from app.main import app
from app.rooms import RoomManager
from app.protocol import ClientMessageType, ServerMessageType


@pytest.fixture(autouse=True)
def fresh_room_manager():
    """Reset the room manager before each test to prevent state leaks."""
    app.state.room_manager = RoomManager()
    yield


@pytest.fixture()
def client():
    """Create a TestClient per test to avoid lifespan issues."""
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c


class TestHealthEndpoint:
    def test_health(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert "rooms" in data


class TestWebSocketCreateRoom:
    def test_create_room(self, client):
        with client.websocket_connect("/ws/match") as ws:
            ws.send_text(json.dumps({
                "type": ClientMessageType.CREATE_ROOM.value,
                "data": {"name": "Alice", "room_type": "duo"},
            }))
            resp = json.loads(ws.receive_text())
            assert resp["type"] == ServerMessageType.ROOM_CREATED.value
            assert "room_code" in resp["data"]
            assert resp["data"]["player_id"].startswith("p_")
            assert resp["data"]["room_type"] == "duo"

    def test_create_group_room(self, client):
        with client.websocket_connect("/ws/match") as ws:
            ws.send_text(json.dumps({
                "type": ClientMessageType.CREATE_ROOM.value,
                "data": {"name": "Alice", "room_type": "group"},
            }))
            resp = json.loads(ws.receive_text())
            assert resp["type"] == ServerMessageType.ROOM_CREATED.value
            assert resp["data"]["room_type"] == "group"


class TestWebSocketJoinRoom:
    def test_join_existing_room(self, client):
        with client.websocket_connect("/ws/match") as ws1:
            # Create room
            ws1.send_text(json.dumps({
                "type": ClientMessageType.CREATE_ROOM.value,
                "data": {"name": "Alice", "room_type": "duo"},
            }))
            create_resp = json.loads(ws1.receive_text())
            code = create_resp["data"]["room_code"]

            with client.websocket_connect("/ws/match") as ws2:
                # Join room
                ws2.send_text(json.dumps({
                    "type": ClientMessageType.JOIN_ROOM.value,
                    "data": {"room_code": code, "name": "Bob"},
                }))

                # ws1 gets player_joined
                join_msg1 = json.loads(ws1.receive_text())
                assert join_msg1["type"] == ServerMessageType.PLAYER_JOINED.value
                assert len(join_msg1["data"]["players"]) == 2

                # ws2 gets player_joined + consent_required
                join_msg2 = json.loads(ws2.receive_text())
                assert join_msg2["type"] == ServerMessageType.PLAYER_JOINED.value

    def test_join_nonexistent_room(self, client):
        with client.websocket_connect("/ws/match") as ws:
            ws.send_text(json.dumps({
                "type": ClientMessageType.JOIN_ROOM.value,
                "data": {"room_code": "ZZZZ", "name": "Bob"},
            }))
            resp = json.loads(ws.receive_text())
            assert resp["type"] == ServerMessageType.ERROR.value
            assert "not found" in resp["data"]["message"].lower()


class TestWebSocketConsent:
    def test_grant_consent(self, client):
        with client.websocket_connect("/ws/match") as ws1:
            # Create
            ws1.send_text(json.dumps({
                "type": ClientMessageType.CREATE_ROOM.value,
                "data": {"name": "Alice", "room_type": "duo"},
            }))
            create_resp = json.loads(ws1.receive_text())
            code = create_resp["data"]["room_code"]
            pid = create_resp["data"]["player_id"]

            # Grant consent
            ws1.send_text(json.dumps({
                "type": ClientMessageType.GRANT_CONSENT.value,
                "data": {},
            }))
            consent_resp = json.loads(ws1.receive_text())
            assert consent_resp["type"] == ServerMessageType.CONSENT_GRANTED.value
            assert consent_resp["data"]["player_id"] == pid


class TestWebSocketPhoto:
    def test_upload_photo_without_consent(self, client):
        with client.websocket_connect("/ws/match") as ws:
            # Create room
            ws.send_text(json.dumps({
                "type": ClientMessageType.CREATE_ROOM.value,
                "data": {"name": "Alice", "room_type": "duo"},
            }))
            json.loads(ws.receive_text())  # room_created

            # Upload without consent
            photo_b64 = base64.b64encode(b"fake_photo").decode()
            ws.send_text(json.dumps({
                "type": ClientMessageType.UPLOAD_PHOTO.value,
                "data": {"photo": photo_b64},
            }))
            resp = json.loads(ws.receive_text())
            assert resp["type"] == ServerMessageType.ERROR.value
            assert "consent" in resp["data"]["message"].lower()

    def test_upload_photo_with_consent(self, client):
        with client.websocket_connect("/ws/match") as ws:
            # Create room
            ws.send_text(json.dumps({
                "type": ClientMessageType.CREATE_ROOM.value,
                "data": {"name": "Alice", "room_type": "duo"},
            }))
            json.loads(ws.receive_text())  # room_created

            # Grant consent
            ws.send_text(json.dumps({
                "type": ClientMessageType.GRANT_CONSENT.value,
                "data": {},
            }))
            json.loads(ws.receive_text())  # consent_granted

            # Upload photo
            photo_b64 = base64.b64encode(b"fake_photo").decode()
            ws.send_text(json.dumps({
                "type": ClientMessageType.UPLOAD_PHOTO.value,
                "data": {"photo": photo_b64},
            }))
            resp = json.loads(ws.receive_text())
            assert resp["type"] == ServerMessageType.PHOTO_RECEIVED.value


class TestWebSocketLeave:
    def test_leave_room(self, client):
        with client.websocket_connect("/ws/match") as ws1:
            # Create
            ws1.send_text(json.dumps({
                "type": ClientMessageType.CREATE_ROOM.value,
                "data": {"name": "Alice", "room_type": "duo"},
            }))
            create_resp = json.loads(ws1.receive_text())
            code = create_resp["data"]["room_code"]

            with client.websocket_connect("/ws/match") as ws2:
                # Join
                ws2.send_text(json.dumps({
                    "type": ClientMessageType.JOIN_ROOM.value,
                    "data": {"room_code": code, "name": "Bob"},
                }))
                # Consume join messages
                json.loads(ws1.receive_text())  # player_joined on ws1
                json.loads(ws2.receive_text())  # player_joined on ws2

                # Bob leaves
                ws2.send_text(json.dumps({
                    "type": ClientMessageType.LEAVE.value,
                    "data": {},
                }))

                # Alice gets player_left
                left_msg = json.loads(ws1.receive_text())
                assert left_msg["type"] == ServerMessageType.PLAYER_LEFT.value
                assert left_msg["data"]["name"] == "Bob"


class TestWebSocketErrors:
    def test_invalid_json(self, client):
        with client.websocket_connect("/ws/match") as ws:
            ws.send_text("not json!")
            resp = json.loads(ws.receive_text())
            assert resp["type"] == ServerMessageType.ERROR.value

    def test_unknown_message_type(self, client):
        with client.websocket_connect("/ws/match") as ws:
            ws.send_text(json.dumps({"type": "unknown_type", "data": {}}))
            resp = json.loads(ws.receive_text())
            assert resp["type"] == ServerMessageType.ERROR.value

    def test_ready_without_room(self, client):
        with client.websocket_connect("/ws/match") as ws:
            ws.send_text(json.dumps({
                "type": ClientMessageType.READY.value,
                "data": {},
            }))
            resp = json.loads(ws.receive_text())
            assert resp["type"] == ServerMessageType.ERROR.value
