"""Challenge-a-friend endpoints for FamiliMatch.

POST /challenge/create — store face photo + metadata, return challenge ID
GET  /challenge/{id}   — return challenge metadata (name, score, NOT photo)
POST /challenge/{id}/accept — compare uploaded face against stored challenger

Privacy: Photos stored in-memory only, purged on expiry (7 days).
Challenges expire after 7 days. Max 10 active per IP.
"""

import time
import uuid
import logging
from typing import Optional

from fastapi import APIRouter, Request, UploadFile, File, Form, HTTPException
from pydantic import BaseModel

from .desktop3_client import compare_faces, compute_embedding, detect_face

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/challenge", tags=["challenge"])

# In-memory challenge store (production would use Redis/DB)
_challenges: dict[str, dict] = {}
_challenges_per_ip: dict[str, list[str]] = {}

MAX_CHALLENGES_PER_IP = 10
CHALLENGE_TTL_SECONDS = 7 * 24 * 3600  # 7 days


def _prune_expired():
    """Remove expired challenges."""
    now = time.time()
    expired = [cid for cid, c in _challenges.items() if now - c["created_at"] > CHALLENGE_TTL_SECONDS]
    for cid in expired:
        ip = _challenges[cid].get("ip", "")
        if ip in _challenges_per_ip:
            _challenges_per_ip[ip] = [x for x in _challenges_per_ip[ip] if x != cid]
        del _challenges[cid]


class ChallengeResponse(BaseModel):
    id: str
    name: str
    percentage: int
    chemistry_label: str
    chemistry_color: str
    created_at: float


class ChallengeCreateResponse(BaseModel):
    ok: bool
    challenge_id: str


@router.post("/create", response_model=ChallengeCreateResponse)
async def create_challenge(
    request: Request,
    photo: UploadFile = File(...),
    name: str = Form(...),
    percentage: int = Form(...),
    chemistry_label: str = Form(...),
    chemistry_color: str = Form(...),
):
    """Create a challenge from a Solo result.

    Stores the face photo (in-memory only) so a friend can
    compare against it later. Purged on expiry.
    """
    _prune_expired()

    client_ip = request.headers.get("X-Forwarded-For", "").split(",")[0].strip() or (
        request.client.host if request.client else "unknown"
    )

    # Rate limit: max 10 active challenges per IP
    active = _challenges_per_ip.get(client_ip, [])
    active = [cid for cid in active if cid in _challenges]
    if len(active) >= MAX_CHALLENGES_PER_IP:
        raise HTTPException(status_code=429, detail="Challenge limit reached (max 10 active)")

    # Read photo and validate face via desktop3
    photo_bytes = await photo.read()
    if len(photo_bytes) > 10 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Photo too large (max 10MB)")

    try:
        detect_result = await detect_face(photo_bytes)
        if not detect_result.get("faces"):
            raise HTTPException(status_code=422, detail="No face detected in photo")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[challenge/create] Face detection failed: {e}")
        raise HTTPException(status_code=500, detail="Face analysis failed")

    challenge_id = uuid.uuid4().hex[:8]
    _challenges[challenge_id] = {
        "id": challenge_id,
        "name": name[:30],
        "percentage": max(0, min(100, percentage)),
        "chemistry_label": chemistry_label[:30],
        "chemistry_color": chemistry_color[:10],
        "photo_bytes": photo_bytes,
        "ip": client_ip,
        "created_at": time.time(),
    }
    _challenges_per_ip.setdefault(client_ip, []).append(challenge_id)

    logger.info(f"[challenge/create] id={challenge_id} name={name[:30]} ip={client_ip}")
    return ChallengeCreateResponse(ok=True, challenge_id=challenge_id)


@router.get("/{challenge_id}", response_model=ChallengeResponse)
async def get_challenge(challenge_id: str):
    """Get challenge metadata. Does NOT return photo or embedding."""
    _prune_expired()

    challenge = _challenges.get(challenge_id)
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found or expired")

    return ChallengeResponse(
        id=challenge["id"],
        name=challenge["name"],
        percentage=challenge["percentage"],
        chemistry_label=challenge["chemistry_label"],
        chemistry_color=challenge["chemistry_color"],
        created_at=challenge["created_at"],
    )


@router.post("/{challenge_id}/accept")
async def accept_challenge(
    challenge_id: str,
    photo: UploadFile = File(...),
    name: str = Form(default="Challenger"),
):
    """Accept a challenge — compare the uploaded face against the stored one.

    Uses desktop3 /compare/faces with the stored photo and the new upload.
    Returns the full compare_faces.v1 response plus the original challenge score.
    """
    _prune_expired()

    challenge = _challenges.get(challenge_id)
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found or expired")

    challenger_photo = await photo.read()
    if len(challenger_photo) > 10 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Photo too large (max 10MB)")

    try:
        result = await compare_faces(
            photo_a=challenge["photo_bytes"],
            photo_b=challenger_photo,
            name_a=challenge["name"],
            name_b=name[:30],
        )
    except Exception as e:
        logger.error(f"[challenge/{challenge_id}/accept] Comparison failed: {e}")
        raise HTTPException(status_code=500, detail="Comparison failed")

    return {
        "ok": True,
        "challenge_name": challenge["name"],
        "challenge_percentage": challenge["percentage"],
        **result,
    }
