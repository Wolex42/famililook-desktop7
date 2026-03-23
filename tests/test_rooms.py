"""Tests for rooms.py — Match room management and isolation."""

import pytest
from unittest.mock import AsyncMock
from app.rooms import MatchRoom, RoomManager, Player, MAX_PLAYERS_BY_TYPE
from app.protocol import RoomType
from tests.conftest import make_player, TEST_PHOTO_BYTES


class TestMatchRoom:
    def test_create_duo_room(self):
        room = MatchRoom("ABC123", host_id="p1", room_type=RoomType.DUO)
        assert room.code == "ABC123"
        assert room.host_id == "p1"
        assert room.room_type == RoomType.DUO
        assert room.max_players == 2
        assert room.player_count == 0

    def test_create_group_room(self):
        room = MatchRoom("XYZ789", host_id="p1", room_type=RoomType.GROUP)
        assert room.max_players == 6

    def test_add_player(self):
        room = MatchRoom("ABC123", host_id="p1", room_type=RoomType.DUO)
        room.add_player(make_player("p1", "Alice"))
        assert room.player_count == 1

    def test_add_player_full(self):
        room = MatchRoom("ABC123", host_id="p1", room_type=RoomType.DUO)
        room.add_player(make_player("p1", "Alice"))
        room.add_player(make_player("p2", "Bob"))
        with pytest.raises(ValueError, match="Room is full"):
            room.add_player(make_player("p3", "Charlie"))

    def test_add_duplicate_player(self):
        room = MatchRoom("ABC123", host_id="p1", room_type=RoomType.DUO)
        room.add_player(make_player("p1", "Alice"))
        with pytest.raises(ValueError, match="Already in room"):
            room.add_player(make_player("p1", "Alice Again"))

    def test_remove_player(self):
        room = MatchRoom("ABC123", host_id="p1", room_type=RoomType.DUO)
        room.add_player(make_player("p1", "Alice"))
        room.add_player(make_player("p2", "Bob"))
        is_empty = room.remove_player("p1")
        assert not is_empty
        assert room.player_count == 1

    def test_remove_last_player_returns_empty(self):
        room = MatchRoom("ABC123", host_id="p1", room_type=RoomType.DUO)
        room.add_player(make_player("p1", "Alice"))
        is_empty = room.remove_player("p1")
        assert is_empty

    def test_remove_cleans_up_player_data(self):
        room = MatchRoom("ABC123", host_id="p1", room_type=RoomType.DUO)
        room.add_player(make_player("p1", "Alice"))
        room.record_consent("p1")
        room.add_photo("p1", TEST_PHOTO_BYTES)
        room.mark_ready("p1")
        room.remove_player("p1")
        assert "p1" not in room.consents
        assert "p1" not in room.photos
        assert "p1" not in room.ready_players

    def test_player_names(self):
        room = MatchRoom("ABC123", host_id="p1", room_type=RoomType.DUO)
        room.add_player(make_player("p1", "Alice"))
        room.add_player(make_player("p2", "Bob"))
        names = room.player_names
        assert len(names) == 2
        assert {"id": "p1", "name": "Alice"} in names


class TestConsent:
    def test_initial_no_consent(self):
        room = MatchRoom("ABC123", host_id="p1", room_type=RoomType.DUO)
        room.add_player(make_player("p1", "Alice"))
        assert not room.all_consented

    def test_record_consent(self):
        room = MatchRoom("ABC123", host_id="p1", room_type=RoomType.DUO)
        room.add_player(make_player("p1", "Alice"))
        room.record_consent("p1")
        assert room.consents["p1"] is True

    def test_all_consented(self):
        room = MatchRoom("ABC123", host_id="p1", room_type=RoomType.DUO)
        room.add_player(make_player("p1", "Alice"))
        room.add_player(make_player("p2", "Bob"))
        room.record_consent("p1")
        assert not room.all_consented
        room.record_consent("p2")
        assert room.all_consented


class TestPhotos:
    def test_add_photo(self):
        room = MatchRoom("ABC123", host_id="p1", room_type=RoomType.DUO)
        room.add_player(make_player("p1", "Alice"))
        room.add_photo("p1", TEST_PHOTO_BYTES)
        assert "p1" in room.photos
        assert room.photos["p1"] == TEST_PHOTO_BYTES

    def test_all_photos_in_false(self):
        room = MatchRoom("ABC123", host_id="p1", room_type=RoomType.DUO)
        room.add_player(make_player("p1", "Alice"))
        room.add_player(make_player("p2", "Bob"))
        room.add_photo("p1", TEST_PHOTO_BYTES)
        assert not room.all_photos_in

    def test_all_photos_in_true(self):
        room = MatchRoom("ABC123", host_id="p1", room_type=RoomType.DUO)
        room.add_player(make_player("p1", "Alice"))
        room.add_player(make_player("p2", "Bob"))
        room.add_photo("p1", TEST_PHOTO_BYTES)
        room.add_photo("p2", TEST_PHOTO_BYTES)
        assert room.all_photos_in

    def test_photos_never_on_disk(self):
        """Photos are stored as bytes in memory, not file paths."""
        room = MatchRoom("ABC123", host_id="p1", room_type=RoomType.DUO)
        room.add_photo("p1", TEST_PHOTO_BYTES)
        assert isinstance(room.photos["p1"], bytes)


class TestReady:
    def test_mark_ready(self):
        room = MatchRoom("ABC123", host_id="p1", room_type=RoomType.DUO)
        room.add_player(make_player("p1", "Alice"))
        room.add_player(make_player("p2", "Bob"))
        room.mark_ready("p1")
        assert not room.all_ready
        room.mark_ready("p2")
        assert room.all_ready


class TestClearData:
    def test_clear_data_removes_photos(self):
        room = MatchRoom("ABC123", host_id="p1", room_type=RoomType.DUO)
        room.add_photo("p1", TEST_PHOTO_BYTES)
        room.add_photo("p2", TEST_PHOTO_BYTES)
        room.results = {"some": "data"}
        room.record_consent("p1")
        room.mark_ready("p1")
        room.clear_data()
        assert len(room.photos) == 0
        assert room.results is None
        assert len(room.ready_players) == 0
        assert len(room.consents) == 0


class TestBroadcast:
    @pytest.mark.asyncio
    async def test_broadcast_sends_to_all(self):
        room = MatchRoom("ABC123", host_id="p1", room_type=RoomType.DUO)
        p1 = make_player("p1", "Alice")
        p2 = make_player("p2", "Bob")
        room.add_player(p1)
        room.add_player(p2)
        await room.broadcast({"type": "test"})
        p1.ws.send_json.assert_called_once()
        p2.ws.send_json.assert_called_once()

    @pytest.mark.asyncio
    async def test_broadcast_excludes_player(self):
        room = MatchRoom("ABC123", host_id="p1", room_type=RoomType.DUO)
        p1 = make_player("p1", "Alice")
        p2 = make_player("p2", "Bob")
        room.add_player(p1)
        room.add_player(p2)
        await room.broadcast({"type": "test"}, exclude="p1")
        p1.ws.send_json.assert_not_called()
        p2.ws.send_json.assert_called_once()

    @pytest.mark.asyncio
    async def test_send_to_specific_player(self):
        room = MatchRoom("ABC123", host_id="p1", room_type=RoomType.DUO)
        p1 = make_player("p1", "Alice")
        p2 = make_player("p2", "Bob")
        room.add_player(p1)
        room.add_player(p2)
        await room.send_to("p2", {"type": "private"})
        p1.ws.send_json.assert_not_called()
        p2.ws.send_json.assert_called_once()


class TestRoomManager:
    def test_create_room(self):
        mgr = RoomManager(max_rooms=100)
        host = make_player("host1", "Alice")
        room = mgr.create_room("duo", host)
        assert room is not None
        assert len(room.code) == 6
        assert room.room_type == RoomType.DUO
        assert mgr.active_room_count == 1
        # Host is automatically added
        assert room.player_count == 1
        assert "host1" in room.players

    def test_create_room_at_capacity(self):
        mgr = RoomManager(max_rooms=1)
        mgr.create_room("duo", make_player("host1", "Alice"))
        with pytest.raises(ValueError, match="capacity"):
            mgr.create_room("duo", make_player("host2", "Bob"))

    def test_get_room(self):
        mgr = RoomManager()
        room = mgr.create_room("duo", make_player("host1", "Alice"))
        found = mgr.get_room(room.code)
        assert found is room

    def test_get_room_not_found(self):
        mgr = RoomManager()
        assert mgr.get_room("ZZZZZZ") is None

    def test_remove_room_clears_data(self):
        mgr = RoomManager()
        room = mgr.create_room("duo", make_player("host1", "Alice"))
        room.add_photo("p1", TEST_PHOTO_BYTES)
        code = room.code
        mgr.remove_room(code)
        assert mgr.active_room_count == 0
        assert len(room.photos) == 0

    def test_room_codes_are_unique(self):
        mgr = RoomManager(max_rooms=100)
        codes = set()
        for i in range(50):
            room = mgr.create_room("duo", make_player(f"host_{i}", f"Host{i}"))
            assert room.code not in codes
            assert len(room.code) == 6
            codes.add(room.code)

    def test_room_code_is_alphanumeric(self):
        """Room codes must be 6-char uppercase alphanumeric."""
        import re
        mgr = RoomManager(max_rooms=100)
        for i in range(20):
            room = mgr.create_room("duo", make_player(f"host_{i}", f"Host{i}"))
            assert re.fullmatch(r"[A-Z0-9]{6}", room.code), f"Bad code: {room.code}"

    def test_active_player_count(self):
        mgr = RoomManager()
        # create_room auto-adds host, then add one more
        room = mgr.create_room("duo", make_player("p1", "Alice"))
        room.add_player(make_player("p2", "Bob"))
        assert mgr.active_player_count == 2

    def test_rooms_are_isolated(self):
        mgr = RoomManager()
        room1 = mgr.create_room("duo", make_player("p1", "Alice"))
        room2 = mgr.create_room("group", make_player("p2", "Bob"))
        assert "p2" not in room1.players
        assert "p1" not in room2.players
        assert room1.code != room2.code

    def test_group_room_allows_6_players(self):
        mgr = RoomManager()
        # create_room auto-adds host (1 player)
        room = mgr.create_room("group", make_player("p0", "Player0"))
        for i in range(1, 6):
            room.add_player(make_player(f"p{i}", f"Player{i}"))
        assert room.player_count == 6
        with pytest.raises(ValueError, match="Room is full"):
            room.add_player(make_player("p6", "Player6"))
