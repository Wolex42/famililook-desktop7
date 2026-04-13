"""
Compatibility scoring engine.
Computes face similarity from embeddings + feature attributes.
Formula: 0.6 * embedding_similarity + 0.4 * feature_similarity

All scoring logic lives here because desktop3 is frozen.
Desktop3 provides raw ML outputs; this module interprets them.
"""

import math
from typing import Dict, List, Optional, Tuple
from .protocol import CompatibilityResult, FeatureComparison


# 8 facial features for comparison
COMPARE_FEATURES = ["eyes", "eyebrows", "smile", "nose", "face_shape", "skin", "hair", "ears"]

# Chemistry label thresholds (percentage -> label + color)
CHEMISTRY_LABELS = [
    (85, "Feature Twins", "#FFD700"),      # Gold
    (70, "Magnetic Match", "#8B5CF6"),      # Purple
    (55, "Complementary Pair", "#3B82F6"),  # Blue
    (40, "Interesting Contrast", "#14B8A6"),  # Teal
    (0, "Opposites Attract", "#F97316"),    # Orange
]

# Weights for the compatibility formula
EMBEDDING_WEIGHT = 0.6
FEATURE_WEIGHT = 0.4


def cosine_similarity(emb_a: List[float], emb_b: List[float]) -> float:
    """
    Compute cosine similarity between two embedding vectors.
    Returns value in [0, 1] range (0 = opposite, 1 = identical).
    """
    if not emb_a or not emb_b or len(emb_a) != len(emb_b):
        return 0.0

    dot = sum(a * b for a, b in zip(emb_a, emb_b))
    norm_a = math.sqrt(sum(a * a for a in emb_a))
    norm_b = math.sqrt(sum(b * b for b in emb_b))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    # Cosine similarity is [-1, 1]; normalize to [0, 1]
    raw = dot / (norm_a * norm_b)
    return max(0.0, min(1.0, (raw + 1.0) / 2.0))


def _extract_feature_label(attrs: dict, feature_key: str) -> str:
    """Extract a feature label from desktop3 attributes response."""
    if not attrs or not isinstance(attrs, dict):
        return ""

    # Try parts -> feature -> label path
    parts = attrs.get("parts", {})
    if isinstance(parts, dict):
        part = parts.get(feature_key, {})
        if isinstance(part, dict):
            label = part.get("label", "")
            if label:
                return str(label)

    # Try direct feature path
    features = attrs.get("features", {})
    if isinstance(features, dict):
        label = features.get(feature_key, "")
        if label:
            return str(label)

    return ""


def feature_similarity(attrs_a: dict, attrs_b: dict) -> Tuple[float, List[FeatureComparison]]:
    """
    Compare 8 facial features between two faces.
    Returns (similarity_score, list of feature comparisons).
    Score is fraction of matching features (0.0 to 1.0).
    """
    comparisons = []
    matches = 0

    for feature in COMPARE_FEATURES:
        label_a = _extract_feature_label(attrs_a, feature)
        label_b = _extract_feature_label(attrs_b, feature)

        # Match if both labels exist and are equal (case-insensitive)
        is_match = bool(label_a and label_b and label_a.lower() == label_b.lower())
        if is_match:
            matches += 1

        comparisons.append(FeatureComparison(
            feature=feature,
            label_a=label_a or "Unknown",
            label_b=label_b or "Unknown",
            match=is_match,
        ))

    score = matches / len(COMPARE_FEATURES) if COMPARE_FEATURES else 0.0
    return score, comparisons


def get_chemistry_label(percentage: int) -> Tuple[str, str]:
    """
    Map a compatibility percentage to a chemistry label and color.
    Returns (label, color_hex).
    """
    for threshold, label, color in CHEMISTRY_LABELS:
        if percentage >= threshold:
            return label, color
    return CHEMISTRY_LABELS[-1][1], CHEMISTRY_LABELS[-1][2]


def compute_compatibility(
    emb_a: List[float],
    emb_b: List[float],
    attrs_a: dict,
    attrs_b: dict,
    fusion_image: Optional[str] = None,
) -> CompatibilityResult:
    """
    Compute full compatibility between two faces.
    Formula: 0.6 * embedding_similarity + 0.4 * feature_similarity
    """
    emb_sim = cosine_similarity(emb_a, emb_b)
    feat_sim, comparisons = feature_similarity(attrs_a, attrs_b)

    score = (EMBEDDING_WEIGHT * emb_sim) + (FEATURE_WEIGHT * feat_sim)
    score = max(0.0, min(1.0, score))
    percentage = round(score * 100)

    label, color = get_chemistry_label(percentage)
    shared = [c.feature for c in comparisons if c.match]

    return CompatibilityResult(
        score=score,
        percentage=percentage,
        chemistry_label=label,
        chemistry_color=color,
        embedding_similarity=round(emb_sim, 4),
        feature_similarity=round(feat_sim, 4),
        feature_comparisons=comparisons,
        shared_features=shared,
        fusion_image=fusion_image,
    )


def compute_group_matrix(
    player_data: List[dict],
) -> dict:
    """
    Compute NxN pairwise compatibility for a group.

    player_data: list of {"id": str, "name": str, "embedding": list, "attributes": dict}

    Returns {
        "matrix": [ [CompatibilityResult for each pair] ],
        "winner_pair": {"a": name, "b": name},
        "winner_score": int,
        "pairs": [ {"a": name, "b": name, "result": CompatibilityResult} ]
    }
    """
    n = len(player_data)
    pairs = []
    best_score = -1
    best_pair = None

    for i in range(n):
        for j in range(i + 1, n):
            a = player_data[i]
            b = player_data[j]
            result = compute_compatibility(
                a.get("embedding", []),
                b.get("embedding", []),
                a.get("attributes", {}),
                b.get("attributes", {}),
            )
            pair_info = {
                "a_id": a["id"],
                "a_name": a["name"],
                "b_id": b["id"],
                "b_name": b["name"],
                "result": result.model_dump(),
            }
            pairs.append(pair_info)

            if result.percentage > best_score:
                best_score = result.percentage
                best_pair = {"a": a["name"], "b": b["name"]}

    return {
        "pairs": pairs,
        "winner_pair": best_pair,
        "winner_score": best_score,
        "total_comparisons": len(pairs),
    }
