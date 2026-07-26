#!/usr/bin/env python3
"""
Rule-based probability extractor (primary method for Phase 1).

Fully deterministic. No models, no network, no randomness.
Anyone with this file can reproduce the exact same probability
from the same source text.

Method ID: rule-extract-keyword-v2
"""

from __future__ import annotations

import json
import re
import datetime
from typing import Optional

METHOD_ID = "rule-extract-keyword-v2"

# Published mapping table. Change this → bump METHOD_ID.
# Order matters: first match wins. More specific phrases first.
RULES = [
    # high confidence positive
    (r"\b(almost\s+certain|virtually\s+certain|extremely\s+likely)\b", 0.95),
    (r"\b(highly\s+probable|highly\s+likely|very\s+likely)\b", 0.85),
    (r"\b(probable|likely|expected|more\s+likely\s+than\s+not)\b", 0.70),
    (r"\b(somewhat\s+likely|rather\s+likely)\b", 0.60),

    # medium / neutral
    (r"\b(about\s+even|roughly\s+even|toss[- ]?up|50[- ]?50)\b", 0.50),
    (r"\b(possible|could\s+happen|might)\b", 0.40),

    # high confidence negative (specific before general)
    (r"\b(almost\s+impossible|extremely\s+unlikely|virtually\s+impossible)\b", 0.05),
    (r"\b(highly\s+unlikely|very\s+unlikely)\b", 0.15),
    (r"\b(somewhat\s+unlikely|rather\s+unlikely)\b", 0.35),
    (r"\b(unlikely|improbable|doubtful)\b", 0.25),
]


def extract_probability(text: str) -> Optional[float]:
    """Return a probability in [0, 1] or None if no rule matches."""
    lowered = text.lower()
    for pattern, prob in RULES:
        if re.search(pattern, lowered):
            return prob
    return None


def make_record(
    *,
    prediction_id: str,
    forecaster_id: str,
    topic: str,
    source_text: str,
    outcome: Optional[float] = None,
    resolved_at: Optional[str] = None,
) -> dict:
    """Build a complete prediction record with provenance."""
    p = extract_probability(source_text)
    if p is None:
        raise ValueError(f"No rule matched for text: {source_text!r}")

    record = {
        "id": prediction_id,
        "forecaster_id": forecaster_id,
        "topic": topic,
        "probability": p,
        "outcome": outcome,
        "probability_method_id": METHOD_ID,
        "probability_source": source_text,
        "probability_generated_at": datetime.datetime.now(datetime.UTC)
        .strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    if resolved_at is not None:
        record["resolved_at"] = resolved_at
    return record


if __name__ == "__main__":
    examples = [
        {
            "prediction_id": "ex-rule-001",
            "forecaster_id": "bob",
            "topic": "geopolitics",
            "source_text": "I think it is more likely than not that the ceasefire holds",
        },
        {
            "prediction_id": "ex-rule-002",
            "forecaster_id": "bob",
            "topic": "geopolitics",
            "source_text": "It is highly probable that sanctions will be lifted",
        },
        {
            "prediction_id": "ex-rule-003",
            "forecaster_id": "carol",
            "topic": "tech",
            "source_text": "AGI this decade is highly unlikely",
        },
    ]

    for ex in examples:
        rec = make_record(**ex)
        print(json.dumps(rec, ensure_ascii=False))
