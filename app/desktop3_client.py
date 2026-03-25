"""Async HTTP client for desktop3 ML endpoints.

Replicates the desktop2 → desktop3 contract:
- All endpoints use multipart/form-data with 'file' field
- /detect: FormData(file) → {faces: [{box, ...}]}
- /embed: FormData(file, boxes) → {embeddings: [[float...]]}
- /face/morph: FormData(fusion_slots, face_<Name>) → {image: base64}
"""

import asyncio
import json
import os
import base64
import httpx

DESKTOP3_URL = os.getenv("DESKTOP3_URL", "http://localhost:8008")
TIMEOUT = float(os.getenv("DESKTOP3_TIMEOUT", "30"))

COMPARE_FEATURES = ["eyes", "eyebrows", "smile", "nose", "face_shape", "skin", "hair", "ears"]


DESKTOP3_HEADERS = {"X-Biometric-Consent": "granted"}


async def _post_form(
    path: str,
    files: dict,
    data: dict | None = None,
    client: httpx.AsyncClient | None = None,
) -> dict:
    """POST multipart form to desktop3 and return JSON response."""
    url = f"{DESKTOP3_URL}{path}"
    if client:
        resp = await client.post(url, files=files, data=data or {}, headers=DESKTOP3_HEADERS, timeout=TIMEOUT)
    else:
        async with httpx.AsyncClient() as c:
            resp = await c.post(url, files=files, data=data or {}, headers=DESKTOP3_HEADERS, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()


async def detect_face(photo_bytes: bytes, client: httpx.AsyncClient | None = None) -> dict:
    """Detect face in photo via multipart FormData.

    POST /detect  FormData(file=<bytes>)
    Response: { "faces": [{box, ...}] }
    """
    files = {"file": ("photo.jpg", photo_bytes, "image/jpeg")}
    return await _post_form("/detect", files, client=client)


async def compute_embedding(
    photo_bytes: bytes,
    boxes: list | None = None,
    client: httpx.AsyncClient | None = None,
) -> list[float]:
    """Compute face embedding via multipart FormData.

    POST /embed  FormData(file=<bytes>, boxes=JSON)
    Response: { "embeddings": [[float...]] }
    """
    files = {"file": ("photo.jpg", photo_bytes, "image/jpeg")}
    data = {}
    if boxes:
        data["boxes"] = json.dumps(boxes)
    result = await _post_form("/embed", files, data=data, client=client)
    # Handle both response shapes
    embs = result.get("embeddings", [])
    if embs:
        return embs[0]
    return result.get("embedding", [])


async def compare_faces(
    photo_a: bytes,
    photo_b: bytes,
    name_a: str,
    name_b: str,
    client: httpx.AsyncClient | None = None,
) -> dict:
    """Compare two faces via desktop3's /compare/faces endpoint.

    POST /compare/faces  FormData(face_a=<bytes>, face_b=<bytes>, name_a, name_b)
    Returns full compare_faces.v1 response (percentage, chemistry_label, feature_comparisons, etc.)
    """
    files = {
        "face_a": ("face_a.jpg", photo_a, "image/jpeg"),
        "face_b": ("face_b.jpg", photo_b, "image/jpeg"),
    }
    data = {"name_a": name_a, "name_b": name_b}
    return await _post_form("/compare/faces", files, data=data, client=client)


# 50/50 alternating feature split for face morph
FEATURES_A = ["eyes", "smile", "face_shape", "skin"]
FEATURES_B = ["eyebrows", "nose", "hair", "ears"]


async def create_duo_morph(
    photo_a: bytes,
    photo_b: bytes,
    name_a: str,
    name_b: str,
    client: httpx.AsyncClient | None = None,
) -> str | None:
    """Create a balanced 50/50 face morph between two players.

    POST /face/morph  FormData(fusion_slots=JSON, face_<name>=<bytes>)
    Features are alternated: name_a gets eyes/smile/face_shape/skin,
    name_b gets eyebrows/nose/hair/ears.
    Returns base64 image or None on failure.
    """
    try:
        fusion_slots = {}
        for f in FEATURES_A:
            fusion_slots[f] = name_a
        for f in FEATURES_B:
            fusion_slots[f] = name_b

        files = {
            f"face_{name_a}": (f"{name_a}.jpg", photo_a, "image/jpeg"),
            f"face_{name_b}": (f"{name_b}.jpg", photo_b, "image/jpeg"),
        }
        data = {
            "fusion_slots": json.dumps(fusion_slots),
            "output_size": "512",
        }
        result = await _post_form("/face/morph", files, data=data, client=client)
        return result.get("image")
    except (httpx.HTTPError, KeyError, Exception):
        return None


async def create_morph(
    photo_a_b64: str,
    photo_b_b64: str,
    client: httpx.AsyncClient | None = None,
) -> str | None:
    """Legacy morph — kept for backward compatibility with existing tests.

    Accepts base64 strings, assigns all features to PersonA.
    Use create_duo_morph() for production 50/50 morphs.
    """
    try:
        bytes_a = base64.b64decode(photo_a_b64)
        bytes_b = base64.b64decode(photo_b_b64)
        fusion_slots = {f: "PersonA" for f in COMPARE_FEATURES}
        files = {
            "face_PersonA": ("PersonA.jpg", bytes_a, "image/jpeg"),
            "face_PersonB": ("PersonB.jpg", bytes_b, "image/jpeg"),
        }
        data = {
            "fusion_slots": json.dumps(fusion_slots),
            "output_size": "512",
        }
        result = await _post_form("/face/morph", files, data=data, client=client)
        return result.get("image")
    except (httpx.HTTPError, KeyError, Exception):
        return None


async def analyze_player(photo_bytes: bytes, client: httpx.AsyncClient | None = None) -> dict:
    """Full analysis pipeline for one player's photo.

    1. /detect — verify face exists, get bounding boxes
    2. /embed — get embedding vector (pass boxes from detect)

    Returns { "embedding": [...], "attributes": {...}, "photo_b64": str }
    (photo_b64 matches main.py's calling convention for create_morph)
    """
    # Detect first — fail fast if no face
    detect_result = await detect_face(photo_bytes, client)
    if not detect_result.get("faces"):
        raise ValueError("No face detected in photo")

    # Get embedding with bounding boxes from detect
    boxes = [f["box"] for f in detect_result["faces"] if "box" in f]
    embedding = await compute_embedding(photo_bytes, boxes=boxes, client=client)

    # Extract attributes from detect response if present
    attributes = detect_result.get("faces", [{}])[0].get("attributes", {})

    return {
        "embedding": embedding,
        "attributes": attributes,
        "photo_b64": base64.b64encode(photo_bytes).decode("utf-8"),
    }
