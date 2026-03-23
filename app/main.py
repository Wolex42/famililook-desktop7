"""FastAPI WebSocket server for real-time face comparison rooms."""

import asyncio
import json
import os
import time
import uuid
import logging
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from .protocol import ClientMessageType, ServerMessageType, server_msg, error_msg
from .rooms import RoomManager, Player
from .desktop3_client import compare_faces, create_duo_morph
from .consent import get_pending_consents

logger = logging.getLogger(__name__)

ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS", "http://localhost:5174,http://localhost:5173"
).split(",")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Start room cleanup loop on startup, stop on shutdown."""
    manager = app.state.room_manager
    cleanup_task = asyncio.create_task(manager._cleanup_loop())
    yield
    cleanup_task.cancel()
    try:
        await cleanup_task
    except asyncio.CancelledError:
        pass


app = FastAPI(title="Match Server", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.room_manager = RoomManager()

MAX_CONNECTIONS_PER_IP = int(os.getenv("MAX_CONNECTIONS_PER_IP", "10"))
_connections_per_ip: dict[str, int] = {}


@app.get("/health")
async def health():
    manager = app.state.room_manager
    return {"status": "ok", "rooms": len(manager._rooms)}


@app.websocket("/ws/match")
async def ws_match(websocket: WebSocket):
    # Per-IP connection limit
    client_ip = websocket.client.host if websocket.client else "unknown"
    count = _connections_per_ip.get(client_ip, 0)
    if count >= MAX_CONNECTIONS_PER_IP:
        await websocket.accept()
        await websocket.close(code=1008, reason="Too many connections")
        return
    _connections_per_ip[client_ip] = count + 1

    await websocket.accept()
    manager: RoomManager = app.state.room_manager
    player: Player | None = None
    room_code: str | None = None
    player_id = f"p_{uuid.uuid4().hex[:8]}"
    _join_fail_times: list[float] = []  # rate-limit: timestamps of failed join attempts
    _JOIN_MAX = 5
    _JOIN_WINDOW = 60  # seconds
    _room_create_times: list[float] = []  # rate-limit: timestamps of room creation
    _CREATE_MAX = 3
    _CREATE_WINDOW = 3600  # 1 hour

    try:
        while True:
            raw = await websocket.receive_text()
            try:
                msg = json.loads(raw)
            except json.JSONDecodeError:
                await websocket.send_text(json.dumps(error_msg("Invalid JSON")))
                continue

            msg_type = msg.get("type")
            data = msg.get("data", {})

            # --- CREATE ROOM ---
            if msg_type == ClientMessageType.CREATE_ROOM.value:
                # Rate-limit room creation per connection (3/hour)
                now = time.time()
                _room_create_times = [t for t in _room_create_times if now - t < _CREATE_WINDOW]
                if len(_room_create_times) >= _CREATE_MAX:
                    await websocket.send_text(json.dumps(error_msg("Room creation limit reached. Try again later.")))
                    continue

                name = data.get("name", "Player")[:30]
                room_type = data.get("room_type", "duo")

                player = Player(
                    id=player_id,
                    name=name,
                    ws=websocket,
                )
                room = manager.create_room(room_type, player)
                _room_create_times.append(time.time())
                room_code = room.code

                await websocket.send_text(json.dumps(server_msg(
                    ServerMessageType.ROOM_CREATED,
                    {
                        "room_code": room.code,
                        "player_id": player.id,
                        "room_type": room_type,
                    },
                )))

            # --- JOIN ROOM ---
            elif msg_type == ClientMessageType.JOIN_ROOM.value:
                # Rate-limit failed join attempts per connection
                now = time.time()
                _join_fail_times = [t for t in _join_fail_times if now - t < _JOIN_WINDOW]
                if len(_join_fail_times) >= _JOIN_MAX:
                    await websocket.send_text(json.dumps(error_msg("Too many attempts. Wait and try again.")))
                    continue

                code = data.get("room_code", "").upper()
                name = data.get("name", "Player")[:30]

                room = manager.get_room(code)
                if not room:
                    _join_fail_times.append(now)
                    logger.warning("Failed join attempt: code=%s conn=%s", code, player_id)
                    await websocket.send_text(json.dumps(error_msg("Room not found")))
                    continue

                player = Player(
                    id=player_id,
                    name=name,
                    ws=websocket,
                )

                try:
                    room.add_player(player)
                except ValueError as e:
                    await websocket.send_text(json.dumps(error_msg(str(e))))
                    continue

                room_code = room.code

                # Notify all players
                await room.broadcast(server_msg(
                    ServerMessageType.PLAYER_JOINED,
                    {
                        "player_id": player.id,
                        "name": name,
                        "players": [
                            {"id": p.id, "name": p.name}
                            for p in room.players.values()
                        ],
                    },
                ))

                # Check if consent is needed
                pending = get_pending_consents(room)
                if pending:
                    await websocket.send_text(json.dumps(server_msg(
                        ServerMessageType.CONSENT_REQUIRED,
                        {"pending": pending},
                    )))

            # --- GRANT CONSENT ---
            elif msg_type == ClientMessageType.GRANT_CONSENT.value:
                if not player or not room_code:
                    await websocket.send_text(json.dumps(error_msg("Not in a room")))
                    continue

                room = manager.get_room(room_code)
                if not room:
                    continue

                room.record_consent(player.id)
                await room.broadcast(server_msg(
                    ServerMessageType.CONSENT_GRANTED,
                    {"player_id": player.id},
                ))

            # --- UPLOAD PHOTO ---
            elif msg_type == ClientMessageType.UPLOAD_PHOTO.value:
                if not player or not room_code:
                    await websocket.send_text(json.dumps(error_msg("Not in a room")))
                    continue

                room = manager.get_room(room_code)
                if not room:
                    continue

                # Check consent
                if player.id not in room.consents:
                    await websocket.send_text(json.dumps(error_msg("Consent required")))
                    continue

                # Photo as base64 in data — validate size before decoding
                import base64
                photo_b64 = data.get("photo", "")
                MAX_PHOTO_B64_LEN = 10 * 1024 * 1024 * 4 // 3  # ~10MB decoded
                if len(photo_b64) > MAX_PHOTO_B64_LEN:
                    await websocket.send_text(json.dumps(error_msg("Photo too large (max 10MB)")))
                    continue
                try:
                    photo_bytes = base64.b64decode(photo_b64)
                except Exception:
                    await websocket.send_text(json.dumps(error_msg("Invalid photo data")))
                    continue

                room.add_photo(player.id, photo_bytes)

                await room.broadcast(server_msg(
                    ServerMessageType.PHOTO_RECEIVED,
                    {
                        "player_id": player.id,
                        "players_with_photos": list(room.photos.keys()),
                    },
                ))

                if room.all_photos_in:
                    await room.broadcast(server_msg(
                        ServerMessageType.ALL_PHOTOS_IN, {}
                    ))

            # --- READY ---
            elif msg_type == ClientMessageType.READY.value:
                if not player or not room_code:
                    await websocket.send_text(json.dumps(error_msg("Not in a room")))
                    continue

                room = manager.get_room(room_code)
                if not room:
                    continue

                room.mark_ready(player.id)

                if room.all_ready and room.all_photos_in:
                    # Start analysis pipeline
                    await _run_analysis(room, manager)

            # --- LEAVE ---
            elif msg_type == ClientMessageType.LEAVE.value:
                if room_code and player:
                    room = manager.get_room(room_code)
                    if room:
                        room.remove_player(player.id)
                        await room.broadcast(server_msg(
                            ServerMessageType.PLAYER_LEFT,
                            {"player_id": player.id, "name": player.name},
                        ))
                        if not room.players:
                            room.clear_data()
                            manager.remove_room(room_code)
                room_code = None
                player = None

            else:
                await websocket.send_text(json.dumps(error_msg(f"Unknown message type: {msg_type}")))

    except WebSocketDisconnect:
        if room_code and player:
            room = manager.get_room(room_code)
            if room:
                room.remove_player(player.id)
                await room.broadcast(server_msg(
                    ServerMessageType.PLAYER_LEFT,
                    {"player_id": player.id, "name": player.name},
                ))
                if not room.players:
                    room.clear_data()
                    manager.remove_room(room_code)
    except Exception as e:
        logger.exception(f"WebSocket error: {e}")
        try:
            await websocket.send_text(json.dumps(error_msg("Internal server error")))
        except Exception:
            pass
    finally:
        # Decrement per-IP connection counter
        _connections_per_ip[client_ip] = max(0, _connections_per_ip.get(client_ip, 1) - 1)
        if _connections_per_ip.get(client_ip) == 0:
            _connections_per_ip.pop(client_ip, None)


async def _run_analysis(room, manager: RoomManager):
    """Run the full analysis pipeline for a room.

    Calls desktop3's /compare/faces for each pair of players.
    Desktop3 returns authoritative results — no local scoring.
    """
    try:
        player_ids = list(room.photos.keys())
        player_names = {
            pid: room.players[pid].name if pid in room.players else "Player"
            for pid in player_ids
        }

        await room.broadcast(server_msg(
            ServerMessageType.ANALYZING, {"progress": 0, "step": "Starting analysis..."}
        ))

        # Generate all pairs
        pairs = []
        for i in range(len(player_ids)):
            for j in range(i + 1, len(player_ids)):
                pairs.append((player_ids[i], player_ids[j]))

        total_pairs = len(pairs)

        async with httpx.AsyncClient() as client:
            pair_results = []

            for idx, (pid_a, pid_b) in enumerate(pairs):
                # Progress: 0-70% for comparisons
                progress = int((idx / max(total_pairs, 1)) * 70)
                await room.broadcast(server_msg(
                    ServerMessageType.ANALYZING,
                    {"progress": progress, "step": f"Comparing faces ({idx + 1}/{total_pairs})..."},
                ))

                result = await compare_faces(
                    photo_a=room.photos[pid_a],
                    photo_b=room.photos[pid_b],
                    name_a=player_names[pid_a],
                    name_b=player_names[pid_b],
                    client=client,
                )

                pair_results.append({
                    "a_id": pid_a,
                    "b_id": pid_b,
                    "a_name": player_names[pid_a],
                    "b_name": player_names[pid_b],
                    "result": result,
                })

            # Morph phase: 70-90%
            await room.broadcast(server_msg(
                ServerMessageType.ANALYZING, {"progress": 70, "step": "Creating fusion..."}
            ))

            if len(player_ids) == 2:
                # --- DUO MODE ---
                comparison = pair_results[0]["result"]
                p1, p2 = player_ids

                fusion_image = await create_duo_morph(
                    photo_a=room.photos[p1],
                    photo_b=room.photos[p2],
                    name_a=player_names[p1],
                    name_b=player_names[p2],
                    client=client,
                )

                await room.broadcast(server_msg(
                    ServerMessageType.ANALYZING, {"progress": 90, "step": "Preparing reveal..."}
                ))

                # Countdown: 3 separate messages
                for sec in [3, 2, 1]:
                    await room.broadcast(server_msg(
                        ServerMessageType.COUNTDOWN, {"seconds": sec}
                    ))
                    await asyncio.sleep(1)

                # Build reveal from desktop3's authoritative response
                reveal_data = dict(comparison)
                if fusion_image:
                    reveal_data["fusion_image"] = fusion_image
                reveal_data["players"] = {
                    p1: player_names[p1],
                    p2: player_names[p2],
                }
                room.results = reveal_data

                await room.broadcast(server_msg(
                    ServerMessageType.REVEAL, reveal_data
                ))

            else:
                # --- GROUP MODE ---
                # Find winner pair (highest percentage)
                best_pair = max(pair_results, key=lambda p: p["result"].get("percentage", 0))

                fusion_image = await create_duo_morph(
                    photo_a=room.photos[best_pair["a_id"]],
                    photo_b=room.photos[best_pair["b_id"]],
                    name_a=best_pair["a_name"],
                    name_b=best_pair["b_name"],
                    client=client,
                )

                await room.broadcast(server_msg(
                    ServerMessageType.ANALYZING, {"progress": 90, "step": "Preparing reveal..."}
                ))

                # Countdown: 3 separate messages
                for sec in [3, 2, 1]:
                    await room.broadcast(server_msg(
                        ServerMessageType.COUNTDOWN, {"seconds": sec}
                    ))
                    await asyncio.sleep(1)

                group_data = {
                    "pairs": pair_results,
                    "winner_pair": {
                        "a": best_pair["a_name"],
                        "b": best_pair["b_name"],
                    },
                    "winner_score": best_pair["result"].get("percentage", 0),
                    "winner_fusion": fusion_image,
                    "total_comparisons": len(pair_results),
                }
                room.results = group_data

                await room.broadcast(server_msg(
                    ServerMessageType.GROUP_REVEAL, group_data
                ))

    except Exception as e:
        logger.exception(f"Analysis error: {e}")
        await room.broadcast(error_msg(f"Analysis failed: {str(e)}"))
    finally:
        # Clean up photos from RAM
        room.clear_data()
