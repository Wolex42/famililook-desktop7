"""Tests for comparison.py — Compatibility scoring engine."""

import pytest
import math
from app.comparison import (
    cosine_similarity,
    feature_similarity,
    get_chemistry_label,
    compute_compatibility,
    compute_group_matrix,
    COMPARE_FEATURES,
    EMBEDDING_WEIGHT,
    FEATURE_WEIGHT,
)
from app.protocol import FeatureComparison
from tests.conftest import MOCK_ATTRS_A, MOCK_ATTRS_B, MOCK_EMBEDDING_A, MOCK_EMBEDDING_B


class TestCosineSimilarity:
    def test_identical_vectors(self):
        v = [1.0, 0.0, 0.0]
        assert cosine_similarity(v, v) == pytest.approx(1.0)

    def test_opposite_vectors(self):
        a = [1.0, 0.0]
        b = [-1.0, 0.0]
        assert cosine_similarity(a, b) == pytest.approx(0.0)

    def test_orthogonal_vectors(self):
        a = [1.0, 0.0]
        b = [0.0, 1.0]
        # Cosine = 0, normalized to 0.5
        assert cosine_similarity(a, b) == pytest.approx(0.5)

    def test_empty_vectors(self):
        assert cosine_similarity([], []) == 0.0

    def test_mismatched_lengths(self):
        assert cosine_similarity([1.0], [1.0, 2.0]) == 0.0

    def test_zero_vector(self):
        assert cosine_similarity([0.0, 0.0], [1.0, 0.0]) == 0.0

    def test_similar_512d_vectors(self):
        """Embedding-like vectors should give reasonable similarity."""
        sim = cosine_similarity(MOCK_EMBEDDING_A, MOCK_EMBEDDING_B)
        assert 0.0 < sim < 1.0

    def test_result_in_0_1_range(self):
        """Result is always normalized to [0, 1]."""
        a = [1.0, 2.0, 3.0]
        b = [-1.0, -2.0, -3.0]
        sim = cosine_similarity(a, b)
        assert 0.0 <= sim <= 1.0


class TestFeatureSimilarity:
    def test_all_matching(self):
        attrs = {
            "parts": {f: {"label": "Same"} for f in COMPARE_FEATURES}
        }
        score, comps = feature_similarity(attrs, attrs)
        assert score == pytest.approx(1.0)
        assert all(c.match for c in comps)
        assert len(comps) == 8

    def test_none_matching(self):
        attrs_a = {"parts": {f: {"label": f"A-{f}"} for f in COMPARE_FEATURES}}
        attrs_b = {"parts": {f: {"label": f"B-{f}"} for f in COMPARE_FEATURES}}
        score, comps = feature_similarity(attrs_a, attrs_b)
        assert score == pytest.approx(0.0)
        assert not any(c.match for c in comps)

    def test_partial_matching(self):
        """Mock attrs A and B share 4 of 8 features."""
        score, comps = feature_similarity(MOCK_ATTRS_A, MOCK_ATTRS_B)
        assert score == pytest.approx(0.5)  # 4/8
        matching = [c for c in comps if c.match]
        assert len(matching) == 4

    def test_empty_attrs(self):
        score, comps = feature_similarity({}, {})
        assert score == pytest.approx(0.0)
        assert len(comps) == 8
        assert all(not c.match for c in comps)

    def test_case_insensitive_matching(self):
        attrs_a = {"parts": {"eyes": {"label": "Almond"}}}
        attrs_b = {"parts": {"eyes": {"label": "almond"}}}
        _, comps = feature_similarity(attrs_a, attrs_b)
        eyes_comp = next(c for c in comps if c.feature == "eyes")
        assert eyes_comp.match is True

    def test_returns_feature_labels(self):
        _, comps = feature_similarity(MOCK_ATTRS_A, MOCK_ATTRS_B)
        eyes = next(c for c in comps if c.feature == "eyes")
        assert eyes.label_a == "Almond"
        assert eyes.label_b == "Almond"

    def test_missing_feature_shows_unknown(self):
        attrs_a = {"parts": {"eyes": {"label": "Almond"}}}
        attrs_b = {"parts": {}}
        _, comps = feature_similarity(attrs_a, attrs_b)
        eyes = next(c for c in comps if c.feature == "eyes")
        assert eyes.label_b == "Unknown"


class TestChemistryLabels:
    def test_feature_twins(self):
        label, color = get_chemistry_label(85)
        assert label == "Feature Twins"
        assert color == "#FFD700"

    def test_feature_twins_max(self):
        label, _ = get_chemistry_label(100)
        assert label == "Feature Twins"

    def test_magnetic_match(self):
        label, color = get_chemistry_label(70)
        assert label == "Magnetic Match"

    def test_magnetic_match_upper(self):
        label, _ = get_chemistry_label(84)
        assert label == "Magnetic Match"

    def test_complementary_pair(self):
        label, color = get_chemistry_label(55)
        assert label == "Complementary Pair"

    def test_interesting_contrast(self):
        label, color = get_chemistry_label(40)
        assert label == "Interesting Contrast"

    def test_opposites_attract(self):
        label, color = get_chemistry_label(39)
        assert label == "Opposites Attract"

    def test_opposites_attract_zero(self):
        label, color = get_chemistry_label(0)
        assert label == "Opposites Attract"
        assert color == "#F97316"

    def test_boundary_85(self):
        """85 is Feature Twins, 84 is Magnetic Match."""
        label_85, _ = get_chemistry_label(85)
        label_84, _ = get_chemistry_label(84)
        assert label_85 == "Feature Twins"
        assert label_84 == "Magnetic Match"

    def test_boundary_70(self):
        label_70, _ = get_chemistry_label(70)
        label_69, _ = get_chemistry_label(69)
        assert label_70 == "Magnetic Match"
        assert label_69 == "Complementary Pair"


class TestComputeCompatibility:
    def test_formula_weights(self):
        """Verify formula: 0.6 * emb_sim + 0.4 * feat_sim."""
        assert EMBEDDING_WEIGHT == pytest.approx(0.6)
        assert FEATURE_WEIGHT == pytest.approx(0.4)
        assert EMBEDDING_WEIGHT + FEATURE_WEIGHT == pytest.approx(1.0)

    def test_identical_faces(self):
        """Same embeddings + same features = high score."""
        emb = [1.0] + [0.0] * 511
        attrs = {"parts": {f: {"label": "Same"} for f in COMPARE_FEATURES}}
        result = compute_compatibility(emb, emb, attrs, attrs)
        assert result.percentage >= 80
        assert result.embedding_similarity == pytest.approx(1.0)
        assert result.feature_similarity == pytest.approx(1.0)

    def test_different_faces(self):
        """Different embeddings + different features = lower score."""
        result = compute_compatibility(
            MOCK_EMBEDDING_A,
            MOCK_EMBEDDING_B,
            MOCK_ATTRS_A,
            MOCK_ATTRS_B,
        )
        assert 0 < result.percentage < 100
        assert result.feature_similarity == pytest.approx(0.5)
        assert len(result.feature_comparisons) == 8
        assert len(result.shared_features) == 4

    def test_returns_chemistry_label(self):
        result = compute_compatibility(
            MOCK_EMBEDDING_A,
            MOCK_EMBEDDING_B,
            MOCK_ATTRS_A,
            MOCK_ATTRS_B,
        )
        assert result.chemistry_label in [
            "Feature Twins", "Magnetic Match", "Complementary Pair",
            "Interesting Contrast", "Opposites Attract",
        ]
        assert result.chemistry_color.startswith("#")

    def test_score_clamped_to_0_1(self):
        result = compute_compatibility(
            MOCK_EMBEDDING_A, MOCK_EMBEDDING_B,
            MOCK_ATTRS_A, MOCK_ATTRS_B,
        )
        assert 0.0 <= result.score <= 1.0
        assert 0 <= result.percentage <= 100

    def test_fusion_image_optional(self):
        result = compute_compatibility(
            MOCK_EMBEDDING_A, MOCK_EMBEDDING_B,
            MOCK_ATTRS_A, MOCK_ATTRS_B,
        )
        assert result.fusion_image is None

        result_with = compute_compatibility(
            MOCK_EMBEDDING_A, MOCK_EMBEDDING_B,
            MOCK_ATTRS_A, MOCK_ATTRS_B,
            fusion_image="data:image/jpeg;base64,abc123",
        )
        assert result_with.fusion_image == "data:image/jpeg;base64,abc123"


class TestComputeGroupMatrix:
    def test_duo_produces_1_pair(self):
        players = [
            {"id": "p1", "name": "Alice", "embedding": MOCK_EMBEDDING_A, "attributes": MOCK_ATTRS_A},
            {"id": "p2", "name": "Bob", "embedding": MOCK_EMBEDDING_B, "attributes": MOCK_ATTRS_B},
        ]
        result = compute_group_matrix(players)
        assert result["total_comparisons"] == 1
        assert len(result["pairs"]) == 1
        assert result["winner_pair"] is not None

    def test_trio_produces_3_pairs(self):
        emb_c = [0.5, 0.5, 0.5] + [0.0] * 509
        attrs_c = {"parts": {f: {"label": f"C-{f}"} for f in COMPARE_FEATURES}}
        players = [
            {"id": "p1", "name": "Alice", "embedding": MOCK_EMBEDDING_A, "attributes": MOCK_ATTRS_A},
            {"id": "p2", "name": "Bob", "embedding": MOCK_EMBEDDING_B, "attributes": MOCK_ATTRS_B},
            {"id": "p3", "name": "Carol", "embedding": emb_c, "attributes": attrs_c},
        ]
        result = compute_group_matrix(players)
        assert result["total_comparisons"] == 3  # C(3,2) = 3

    def test_group_of_4_produces_6_pairs(self):
        players = []
        for i in range(4):
            emb = [0.0] * 512
            emb[i] = 1.0
            players.append({
                "id": f"p{i}",
                "name": f"Player{i}",
                "embedding": emb,
                "attributes": {"parts": {f: {"label": f"P{i}-{f}"} for f in COMPARE_FEATURES}},
            })
        result = compute_group_matrix(players)
        assert result["total_comparisons"] == 6  # C(4,2) = 6

    def test_winner_pair_has_highest_score(self):
        # Make p1 and p2 identical (highest score)
        emb = [1.0] + [0.0] * 511
        attrs = {"parts": {f: {"label": "Same"} for f in COMPARE_FEATURES}}
        players = [
            {"id": "p1", "name": "Alice", "embedding": emb, "attributes": attrs},
            {"id": "p2", "name": "Bob", "embedding": emb, "attributes": attrs},
            {"id": "p3", "name": "Carol", "embedding": MOCK_EMBEDDING_B, "attributes": MOCK_ATTRS_B},
        ]
        result = compute_group_matrix(players)
        assert result["winner_pair"]["a"] == "Alice"
        assert result["winner_pair"]["b"] == "Bob"
        assert result["winner_score"] >= 80

    def test_pairs_contain_names_and_result(self):
        players = [
            {"id": "p1", "name": "Alice", "embedding": MOCK_EMBEDDING_A, "attributes": MOCK_ATTRS_A},
            {"id": "p2", "name": "Bob", "embedding": MOCK_EMBEDDING_B, "attributes": MOCK_ATTRS_B},
        ]
        result = compute_group_matrix(players)
        pair = result["pairs"][0]
        assert pair["a_name"] == "Alice"
        assert pair["b_name"] == "Bob"
        assert "result" in pair
        assert "percentage" in pair["result"]
