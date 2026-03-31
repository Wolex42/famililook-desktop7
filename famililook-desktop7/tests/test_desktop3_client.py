"""Tests for desktop3_client — all HTTP calls mocked."""

import base64
import json
import pytest
import httpx
from unittest.mock import AsyncMock, patch, MagicMock

from app.desktop3_client import (
    detect_face,
    compute_embedding,
    create_morph,
    create_duo_morph,
    compare_faces,
    analyze_player,
    DESKTOP3_URL,
    FEATURES_A,
    FEATURES_B,
)


# --- Fixtures ---

FAKE_PHOTO = b"fake_photo_bytes"
FAKE_B64 = base64.b64encode(FAKE_PHOTO).decode()

MOCK_DETECT_OK = {"faces": [{"box": [10, 10, 100, 100]}]}
MOCK_DETECT_ATTRS = {"faces": [{"box": [10, 10, 100, 100], "attributes": {"eyes": "Almond", "nose": "Narrow"}}]}
MOCK_DETECT_EMPTY = {"faces": []}
MOCK_EMBEDDING = {"embeddings": [[0.1] * 512]}
MOCK_EMBEDDING_LEGACY = {"embedding": [0.2] * 512}
MOCK_MORPH = {"image": "base64_morphed_data"}
MOCK_COMPARE_FACES = {
    "ok": True,
    "percentage": 72,
    "chemistry_label": "Magnetic Match",
    "chemistry_color": "#8B5CF6",
    "embedding_similarity": 0.78,
    "feature_similarity": 0.625,
    "feature_comparisons": [
        {"feature": "eyes", "label_a": "Round", "label_b": "Round", "match": True},
        {"feature": "eyebrows", "label_a": "Arched", "label_b": "Flat", "match": False},
        {"feature": "smile", "label_a": "Wide", "label_b": "Wide", "match": True},
        {"feature": "nose", "label_a": "Narrow", "label_b": "Wide", "match": False},
        {"feature": "face_shape", "label_a": "Oval", "label_b": "Oval", "match": True},
        {"feature": "skin", "label_a": "Medium", "label_b": "Medium", "match": True},
        {"feature": "hair", "label_a": "Dark", "label_b": "Light", "match": False},
        {"feature": "ears", "label_a": "Average", "label_b": "Average", "match": True},
    ],
    "shared_features": ["eyes", "smile", "face_shape", "skin", "ears"],
    "calibrated_a": {},
    "calibrated_b": {},
    "name_a": "Alice",
    "name_b": "Bob",
}


def make_mock_response(json_data, status=200):
    resp = MagicMock(spec=httpx.Response)
    resp.status_code = status
    resp.json.return_value = json_data
    resp.raise_for_status = MagicMock()
    if status >= 400:
        resp.raise_for_status.side_effect = httpx.HTTPStatusError(
            "error", request=MagicMock(), response=resp
        )
    return resp


# --- detect_face ---

class TestDetectFace:
    @pytest.mark.asyncio
    async def test_detect_ok(self):
        client = AsyncMock(spec=httpx.AsyncClient)
        client.post.return_value = make_mock_response(MOCK_DETECT_OK)

        result = await detect_face(FAKE_PHOTO, client)
        assert len(result["faces"]) == 1
        assert result["faces"][0]["box"] == [10, 10, 100, 100]
        client.post.assert_called_once()

        # Verify multipart files kwarg
        call_kwargs = client.post.call_args[1]
        assert "files" in call_kwargs
        file_tuple = call_kwargs["files"]["file"]
        assert file_tuple[0] == "photo.jpg"  # filename
        assert file_tuple[1] == FAKE_PHOTO   # bytes
        assert file_tuple[2] == "image/jpeg"  # content type

    @pytest.mark.asyncio
    async def test_detect_no_faces(self):
        client = AsyncMock(spec=httpx.AsyncClient)
        client.post.return_value = make_mock_response(MOCK_DETECT_EMPTY)

        result = await detect_face(FAKE_PHOTO, client)
        assert result["faces"] == []

    @pytest.mark.asyncio
    async def test_detect_http_error(self):
        client = AsyncMock(spec=httpx.AsyncClient)
        client.post.return_value = make_mock_response({}, status=500)

        with pytest.raises(httpx.HTTPStatusError):
            await detect_face(FAKE_PHOTO, client)


# --- compute_embedding ---

class TestComputeEmbedding:
    @pytest.mark.asyncio
    async def test_returns_512_dim(self):
        client = AsyncMock(spec=httpx.AsyncClient)
        client.post.return_value = make_mock_response(MOCK_EMBEDDING)

        emb = await compute_embedding(FAKE_PHOTO, client=client)
        assert len(emb) == 512
        assert all(isinstance(v, float) for v in emb)

    @pytest.mark.asyncio
    async def test_legacy_embedding_key(self):
        """Handles desktop3 returning 'embedding' instead of 'embeddings'."""
        client = AsyncMock(spec=httpx.AsyncClient)
        client.post.return_value = make_mock_response(MOCK_EMBEDDING_LEGACY)

        emb = await compute_embedding(FAKE_PHOTO, client=client)
        assert len(emb) == 512
        assert emb[0] == 0.2

    @pytest.mark.asyncio
    async def test_empty_on_missing_key(self):
        client = AsyncMock(spec=httpx.AsyncClient)
        client.post.return_value = make_mock_response({"ok": True})

        emb = await compute_embedding(FAKE_PHOTO, client=client)
        assert emb == []

    @pytest.mark.asyncio
    async def test_passes_boxes(self):
        client = AsyncMock(spec=httpx.AsyncClient)
        client.post.return_value = make_mock_response(MOCK_EMBEDDING)

        boxes = [[10, 10, 100, 100]]
        await compute_embedding(FAKE_PHOTO, boxes=boxes, client=client)

        call_kwargs = client.post.call_args[1]
        assert "data" in call_kwargs
        assert json.loads(call_kwargs["data"]["boxes"]) == boxes

    @pytest.mark.asyncio
    async def test_no_boxes_means_no_data(self):
        client = AsyncMock(spec=httpx.AsyncClient)
        client.post.return_value = make_mock_response(MOCK_EMBEDDING)

        await compute_embedding(FAKE_PHOTO, client=client)

        call_kwargs = client.post.call_args[1]
        # data should be empty dict when no boxes
        assert call_kwargs.get("data", {}) == {}


# --- create_morph ---

class TestCreateMorph:
    @pytest.mark.asyncio
    async def test_returns_base64(self):
        client = AsyncMock(spec=httpx.AsyncClient)
        client.post.return_value = make_mock_response(MOCK_MORPH)

        result = await create_morph(FAKE_B64, FAKE_B64, client=client)
        assert result == "base64_morphed_data"

    @pytest.mark.asyncio
    async def test_returns_none_on_error(self):
        client = AsyncMock(spec=httpx.AsyncClient)
        client.post.return_value = make_mock_response({}, status=500)

        result = await create_morph(FAKE_B64, FAKE_B64, client=client)
        assert result is None

    @pytest.mark.asyncio
    async def test_sends_fusion_slots_and_files(self):
        client = AsyncMock(spec=httpx.AsyncClient)
        client.post.return_value = make_mock_response(MOCK_MORPH)

        await create_morph(FAKE_B64, FAKE_B64, client=client)

        call_kwargs = client.post.call_args[1]
        # Verify fusion_slots in data
        slots = json.loads(call_kwargs["data"]["fusion_slots"])
        assert "eyes" in slots
        assert "ears" in slots
        assert slots["eyes"] == "PersonA"
        # Verify output_size
        assert call_kwargs["data"]["output_size"] == "512"
        # Verify face files
        assert "face_PersonA" in call_kwargs["files"]
        assert "face_PersonB" in call_kwargs["files"]
        # File tuples: (filename, bytes, content_type)
        assert call_kwargs["files"]["face_PersonA"][0] == "PersonA.jpg"
        assert call_kwargs["files"]["face_PersonB"][0] == "PersonB.jpg"

    @pytest.mark.asyncio
    async def test_returns_none_on_missing_image_key(self):
        client = AsyncMock(spec=httpx.AsyncClient)
        client.post.return_value = make_mock_response({"ok": True})

        result = await create_morph(FAKE_B64, FAKE_B64, client=client)
        assert result is None


# --- analyze_player ---

class TestAnalyzePlayer:
    @pytest.mark.asyncio
    async def test_full_pipeline(self):
        client = AsyncMock(spec=httpx.AsyncClient)

        # detect, then embed (2 calls — no separate attributes call)
        client.post.side_effect = [
            make_mock_response(MOCK_DETECT_ATTRS),
            make_mock_response(MOCK_EMBEDDING),
        ]

        result = await analyze_player(FAKE_PHOTO, client)
        assert len(result["embedding"]) == 512
        assert result["attributes"]["eyes"] == "Almond"
        assert result["attributes"]["nose"] == "Narrow"
        assert result["photo_b64"] == FAKE_B64
        assert client.post.call_count == 2

    @pytest.mark.asyncio
    async def test_attributes_from_detect_response(self):
        """Attributes are extracted from detect face data, not a separate endpoint."""
        client = AsyncMock(spec=httpx.AsyncClient)
        detect_with_attrs = {
            "faces": [{"box": [5, 5, 50, 50], "attributes": {"hair": "Curly", "skin": "Fair"}}]
        }
        client.post.side_effect = [
            make_mock_response(detect_with_attrs),
            make_mock_response(MOCK_EMBEDDING),
        ]

        result = await analyze_player(FAKE_PHOTO, client)
        assert result["attributes"]["hair"] == "Curly"
        assert result["attributes"]["skin"] == "Fair"

    @pytest.mark.asyncio
    async def test_empty_attributes_when_not_in_detect(self):
        """When detect doesn't return attributes, result has empty dict."""
        client = AsyncMock(spec=httpx.AsyncClient)
        client.post.side_effect = [
            make_mock_response(MOCK_DETECT_OK),  # no attributes key
            make_mock_response(MOCK_EMBEDDING),
        ]

        result = await analyze_player(FAKE_PHOTO, client)
        assert result["attributes"] == {}

    @pytest.mark.asyncio
    async def test_passes_boxes_from_detect_to_embed(self):
        """Bounding boxes from detect are forwarded to embed call."""
        client = AsyncMock(spec=httpx.AsyncClient)
        client.post.side_effect = [
            make_mock_response(MOCK_DETECT_OK),
            make_mock_response(MOCK_EMBEDDING),
        ]

        await analyze_player(FAKE_PHOTO, client)

        # Second call is embed — should have boxes in data
        embed_call = client.post.call_args_list[1]
        embed_data = embed_call[1].get("data", {})
        assert "boxes" in embed_data
        assert json.loads(embed_data["boxes"]) == [[10, 10, 100, 100]]

    @pytest.mark.asyncio
    async def test_raises_on_no_face(self):
        client = AsyncMock(spec=httpx.AsyncClient)
        client.post.return_value = make_mock_response(MOCK_DETECT_EMPTY)

        with pytest.raises(ValueError, match="No face detected"):
            await analyze_player(FAKE_PHOTO, client)

    @pytest.mark.asyncio
    async def test_raises_on_detect_failure(self):
        client = AsyncMock(spec=httpx.AsyncClient)
        client.post.return_value = make_mock_response({"faces": []})

        with pytest.raises(ValueError, match="No face detected"):
            await analyze_player(FAKE_PHOTO, client)


# --- compare_faces ---

class TestCompareFaces:
    @pytest.mark.asyncio
    async def test_sends_correct_form_data(self):
        client = AsyncMock(spec=httpx.AsyncClient)
        client.post.return_value = make_mock_response(MOCK_COMPARE_FACES)

        await compare_faces(FAKE_PHOTO, FAKE_PHOTO, "Alice", "Bob", client=client)

        call_kwargs = client.post.call_args[1]
        # Verify file fields
        assert "face_a" in call_kwargs["files"]
        assert "face_b" in call_kwargs["files"]
        assert call_kwargs["files"]["face_a"][1] == FAKE_PHOTO
        assert call_kwargs["files"]["face_b"][1] == FAKE_PHOTO
        # Verify name fields
        assert call_kwargs["data"]["name_a"] == "Alice"
        assert call_kwargs["data"]["name_b"] == "Bob"

    @pytest.mark.asyncio
    async def test_returns_full_response(self):
        client = AsyncMock(spec=httpx.AsyncClient)
        client.post.return_value = make_mock_response(MOCK_COMPARE_FACES)

        result = await compare_faces(FAKE_PHOTO, FAKE_PHOTO, "Alice", "Bob", client=client)
        assert result["percentage"] == 72
        assert result["chemistry_label"] == "Magnetic Match"
        assert len(result["feature_comparisons"]) == 8
        assert result["name_a"] == "Alice"
        assert result["name_b"] == "Bob"

    @pytest.mark.asyncio
    async def test_raises_on_http_error(self):
        client = AsyncMock(spec=httpx.AsyncClient)
        client.post.return_value = make_mock_response({}, status=500)

        with pytest.raises(httpx.HTTPStatusError):
            await compare_faces(FAKE_PHOTO, FAKE_PHOTO, "A", "B", client=client)

    @pytest.mark.asyncio
    async def test_calls_compare_faces_endpoint(self):
        client = AsyncMock(spec=httpx.AsyncClient)
        client.post.return_value = make_mock_response(MOCK_COMPARE_FACES)

        await compare_faces(FAKE_PHOTO, FAKE_PHOTO, "A", "B", client=client)

        call_args = client.post.call_args[0]
        assert "/compare/faces" in call_args[0]


# --- create_duo_morph ---

class TestCreateDuoMorph:
    @pytest.mark.asyncio
    async def test_alternating_fusion_slots(self):
        client = AsyncMock(spec=httpx.AsyncClient)
        client.post.return_value = make_mock_response(MOCK_MORPH)

        await create_duo_morph(FAKE_PHOTO, FAKE_PHOTO, "Alice", "Bob", client=client)

        call_kwargs = client.post.call_args[1]
        slots = json.loads(call_kwargs["data"]["fusion_slots"])

        # Alice gets 4 features
        for f in FEATURES_A:
            assert slots[f] == "Alice"
        # Bob gets 4 features
        for f in FEATURES_B:
            assert slots[f] == "Bob"
        # Total 8 features
        assert len(slots) == 8

    @pytest.mark.asyncio
    async def test_uses_real_player_names(self):
        client = AsyncMock(spec=httpx.AsyncClient)
        client.post.return_value = make_mock_response(MOCK_MORPH)

        await create_duo_morph(FAKE_PHOTO, FAKE_PHOTO, "Sarah", "Dan", client=client)

        call_kwargs = client.post.call_args[1]
        slots = json.loads(call_kwargs["data"]["fusion_slots"])
        # Names should be real names, not PersonA/PersonB
        assert "PersonA" not in slots.values()
        assert "PersonB" not in slots.values()
        assert "Sarah" in slots.values()
        assert "Dan" in slots.values()
        # File keys use real names
        assert "face_Sarah" in call_kwargs["files"]
        assert "face_Dan" in call_kwargs["files"]

    @pytest.mark.asyncio
    async def test_returns_base64_image(self):
        client = AsyncMock(spec=httpx.AsyncClient)
        client.post.return_value = make_mock_response(MOCK_MORPH)

        result = await create_duo_morph(FAKE_PHOTO, FAKE_PHOTO, "A", "B", client=client)
        assert result == "base64_morphed_data"

    @pytest.mark.asyncio
    async def test_returns_none_on_error(self):
        client = AsyncMock(spec=httpx.AsyncClient)
        client.post.return_value = make_mock_response({}, status=500)

        result = await create_duo_morph(FAKE_PHOTO, FAKE_PHOTO, "A", "B", client=client)
        assert result is None
