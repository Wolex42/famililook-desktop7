"""
Room management for the match server.
Handles room creation, joining, photo storage, and lifecycle.
All data is in-memory only. Photos are never written to disk.
"""

import asyncio
import gc
import secrets
import string
import time
from typing import Dict, List, Optional
from fastapi import WebSocket

from .protocol import RoomType


# Max players per room type
MAX_PLAYERS_BY_TYPE = {
    RoomType.DUO: 2,
    RoomType.GROUP: 6,
}


class Player:
    """A connected player in a match room."""
    __slots__ = ("id", "name", "ws", "connection_id", "connected_at", "disconnected_at")

    def __init__(self, id: str, name: str, ws: WebSocket, connection_id: str = ""):
        self.id = id
        self.name = name
        self.ws = ws
        self.connection_id = connection_id or f"conn_{secrets.token_hex(4)}"
        self.connected_at = time.time()
        self.disconnected_at: float | None = None


class MatchRoom:
    """
    A single match room. Holds players, photos, and consent state in memory.
    Photos are stored as raw bytes — never written to disk.
    """

    DISCONNECT_TIMEOUT = 300  # 5 minutes — grace period for reconnection

    def __init__(self, code: str, host_id: str, room_type: RoomType):
        self.code = code
        self.host_id = host_id
        self.room_type = room_type
        self.max_players = MAX_PLAYERS_BY_TYPE.get(room_type, 2)
        self.players: Dict[str, Player] = {}
        self._disconnected: Dict[str, Player] = {}  # player_id -> Player (grace period)
        self.consents: Dict[str, bool] = {}
        self.photos: Dict[str, bytes] = {}  # player_id -> raw photo bytes (RAM only)
        self.ready_players: set = set()
        self.results: Optional[dict] = None
        self.created_at = time.time()
        self.last_activity = time.time()

    @property
    def player_count(self) -> int:
        return len(self.players)

    @property
    def is_full(self) -> bool:
        return (self.player_count + len(self._disconnected)) >= self.max_players

    @property
    def all_consented(self) -> bool:
        return len(self.consents) >= self.player_count and all(self.consents.values())

    @property
    def all_photos_in(self) -> bool:
        return len(self.photos) >= self.player_count and self.player_count > 0

    @property
    def all_ready(self) -> bool:
        return len(self.ready_players) >= self.player_count and self.player_count > 0

    @property
    def player_names(self) -> List[dict]:
        return [{"id": p.id, "name": p.name} for p in self.players.values()]

    def add_player(self, player: Player):
        """Add a player. Raises ValueError if room is full or player already in."""
        # Allow reconnecting players (they are in _disconnected, not players)
        if player.id not in self._disconnected and self.is_full:
            raise ValueError("Room is full")
        if player.id in self.players:
            raise ValueError("Already in room")
        self.players[player.id] = player
        self.last_activity = time.time()

    def disconnect_player(self, player_id: str):
        """Mark a player as disconnected but keep their data (photos, consent) intact.

        The player is moved from active players to the _disconnected dict.
        After DISCONNECT_TIMEOUT (5 min), _cleanup_disconnected removes them fully.
        """
        player = self.players.pop(player_id, None)
        if player:
            player.disconnected_at = time.time()
            self._disconnected[player_id] = player
        self.last_activity = time.time()

    def rejoin_player(self, player_id: str, new_ws: 'WebSocket', new_connection_id: str) -> Optional[Player]:
        """Rejoin a disconnected player with a new WebSocket connection.

        Returns the restored Player on success, None if the player is not
        in the disconnected set.
        """
        player = self._disconnected.pop(player_id, None)
        if not player:
            return None
        player.ws = new_ws
        player.connection_id = new_connection_id
        player.disconnected_at = None
        self.players[player_id] = player
        self.last_activity = time.time()
        return player

    def cleanup_disconnected(self):
        """Remove players who have been disconnected longer than DISCONNECT_TIMEOUT.

        Also removes their photos, consent, and ready state.
        """
        now = time.time()
        expired = [
            pid for pid, p in self._disconnected.items()
            if p.disconnected_at and (now - p.disconnected_at) > self.DISCONNECT_TIMEOUT
        ]
        for pid in expired:
            self._disconnected.pop(pid, None)
            self.consents.pop(pid, None)
            self.photos.pop(pid, None)
            self.ready_players.discard(pid)

    def remove_player(self, player_id: str) -> bool:
        """Remove a player and their data completely (explicit leave). Returns True if room is now empty."""
        self.players.pop(player_id, None)
        self._disconnected.pop(player_id, None)
        self.consents.pop(player_id, None)
        self.photos.pop(player_id, None)
        self.ready_players.discard(player_id)
        self.last_activity = time.time()
        return len(self.players) == 0 and len(self._disconnected) == 0

    def record_consent(self, player_id: str):
        """Record that a player has consented to photo processing."""
        self.consents[player_id] = True
        self.last_activity = time.time()

    def add_photo(self, player_id: str, photo_bytes: bytes):
        """Store a player's photo in RAM."""
        self.photos[player_id] = photo_bytes
        self.last_activity = time.time()

    def mark_ready(self, player_id: str):
        """Mark a player as ready for analysis."""
        self.ready_players.add(player_id)
        self.last_activity = time.time()

    def clear_data(self):
        """Explicitly clear all photo data and results from memory.

        Overwrites photo bytes with zeros before deleting references,
        then forces garbage collection to reclaim memory promptly.
        """
        for pid in list(self.photos.keys()):
            photo = self.photos[pid]
            if isinstance(photo, (bytes, bytearray)):
                # Overwrite mutable copy with zeros to reduce residual data window
                try:
                    zeroed = bytearray(len(photo))
                    self.photos[pid] = zeroed
                except Exception:
                    pass
            del self.photos[pid]
        self.photos.clear()
        self.results = None
        self.ready_players.clear()
        self.consents.clear()
        self._disconnected.clear()
        gc.collect()

    async def broadcast(self, message: dict, exclude: Optional[str] = None):
        """Send a message to all players in this room (except excluded)."""
        disconnected = []
        for pid, player in self.players.items():
            if pid == exclude:
                continue
            try:
                await player.ws.send_json(message)
            except Exception:
                disconnected.append(pid)
        for pid in disconnected:
            self.players.pop(pid, None)

    async def send_to(self, player_id: str, message: dict):
        """Send a message to a specific player."""
        player = self.players.get(player_id)
        if player:
            try:
                await player.ws.send_json(message)
            except Exception:
                self.players.pop(player_id, None)


class RoomManager:
    """
    Manages all active match rooms. In-memory only.
    """

    def __init__(self, max_rooms: int = 5000, idle_timeout: int = 1800):
        self._rooms: Dict[str, MatchRoom] = {}
        self.max_rooms = max_rooms
        self.idle_timeout = idle_timeout
        self._cleanup_task: Optional[asyncio.Task] = None

    def start_cleanup_loop(self):
        """Start the background cleanup task for idle rooms."""
        if self._cleanup_task is None:
            self._cleanup_task = asyncio.create_task(self._cleanup_loop())

    async def _cleanup_loop(self):
        """Periodically remove idle rooms and expired disconnected players."""
        while True:
            await asyncio.sleep(60)
            now = time.time()
            # Clean up disconnected players whose grace period has expired
            for room in self._rooms.values():
                room.cleanup_disconnected()
            # Remove idle rooms
            expired = [
                code for code, room in self._rooms.items()
                if now - room.last_activity > self.idle_timeout
            ]
            for code in expired:
                room = self._rooms.pop(code, None)
                if room:
                    room.clear_data()
                    await room.broadcast({"type": "error", "data": {"message": "Room closed due to inactivity"}})

    _CODE_ALPHABET = string.ascii_uppercase + string.digits  # 36 chars
    _CODE_LENGTH = 6  # 36^6 ≈ 2.18 billion possible codes

    def _generate_code(self) -> str:
        """Generate a unique 6-character alphanumeric room code (cryptographic RNG)."""
        for _ in range(100):
            code = ''.join(secrets.choice(self._CODE_ALPHABET) for _ in range(self._CODE_LENGTH))
            if code not in self._rooms:
                return code
        raise RuntimeError("Could not generate unique room code")

    def create_room(self, room_type: str, host_player: Player) -> MatchRoom:
        """Create a new match room with the host player already added.

        Args:
            room_type: "duo" or "group" string (converted to RoomType enum).
            host_player: The Player who is creating/hosting the room.

        Raises ValueError if at capacity.
        """
        if len(self._rooms) >= self.max_rooms:
            raise ValueError("Server at room capacity")
        rt = RoomType(room_type)
        code = self._generate_code()
        room = MatchRoom(code=code, host_id=host_player.id, room_type=rt)
        room.add_player(host_player)
        self._rooms[code] = room
        return room

    def get_room(self, code: str) -> Optional[MatchRoom]:
        """Look up a room by code."""
        return self._rooms.get(code)

    def rejoin_player(self, room_code: str, player_id: str, new_ws: 'WebSocket', new_connection_id: str) -> Optional[Player]:
        """Rejoin a disconnected player to their room.

        Returns the restored Player on success, None if room or player not found.
        """
        room = self.get_room(room_code)
        if not room:
            return None
        return room.rejoin_player(player_id, new_ws, new_connection_id)

    def remove_room(self, code: str):
        """Remove a room, clearing all its data first."""
        room = self._rooms.pop(code, None)
        if room:
            room.clear_data()

    @property
    def active_room_count(self) -> int:
        return len(self._rooms)

    @property
    def active_player_count(self) -> int:
        return sum(room.player_count for room in self._rooms.values())
