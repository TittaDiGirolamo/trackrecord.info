"""
Canonical scoring function.

This is the only place that turns resolved predictions into numbers.
Every generator (homepage, profiles, table, detail pages) must call this.

Pure mean Brier is the source of truth.
Brier Index is a derived display value only.
"""

from typing import List, Dict, Any
from .rules import score_one, aggregate, RULES_VERSION, LIMITATIONS_NOTE, brier_to_index


def score_forecaster(
    predictions: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    THE single canonical scoring function.

    Returns:
      - overall          : mean Brier (lower = better) or None
      - overall_index    : Brier Index (higher = better, 0–100) or None
      - topics           : {topic: {score, index, resolved_count, prediction_ids}}
      - resolved_count
      - pending_count
      - prediction_ids
      - contributions    : {pred_id: individual Brier}
      - rules_version
      - limitations_note
    """
    resolved = [p for p in predictions if p.get("outcome") is not None]
    pending = [p for p in predictions if p.get("outcome") is None]

    if not resolved:
        return {
            "overall": None,
            "overall_index": None,
            "topics": {},
            "resolved_count": 0,
            "pending_count": len(pending),
            "prediction_ids": [],
            "contributions": {},
            "rules_version": RULES_VERSION,
            "limitations_note": LIMITATIONS_NOTE,
        }

    contributions: Dict[str, float] = {}
    for p in resolved:
        contributions[str(p["id"])] = score_one(p)

    overall = aggregate(list(contributions.values()))
    overall_index = brier_to_index(overall)

    topics: Dict[str, Any] = {}
    topic_names = {p.get("topic") or "untagged" for p in resolved}
    for topic in topic_names:
        topic_preds = [p for p in resolved if (p.get("topic") or "untagged") == topic]
        topic_ids = [str(p["id"]) for p in topic_preds]
        topic_contribs = [contributions[i] for i in topic_ids]
        t_score = aggregate(topic_contribs)
        topics[topic] = {
            "score": t_score,
            "index": brier_to_index(t_score),
            "resolved_count": len(topic_preds),
            "prediction_ids": topic_ids,
        }

    return {
        "overall": overall,
        "overall_index": overall_index,
        "topics": topics,
        "resolved_count": len(resolved),
        "pending_count": len(pending),
        "prediction_ids": list(contributions.keys()),
        "contributions": contributions,
        "rules_version": RULES_VERSION,
        "limitations_note": LIMITATIONS_NOTE,
    }
