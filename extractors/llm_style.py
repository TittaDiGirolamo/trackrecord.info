#!/usr/bin/env python3
"""
LLM-style probability extractor (optional secondary method).

This is a template. It shows the exact provenance fields that must be
written so the extraction remains reproducible.

In production:
  1. Pin a specific model snapshot.
  2. Freeze the prompt template and record its content hash.
  3. Use temperature = 0 (or a fixed seed).
  4. Bump METHOD_ID whenever the prompt or model changes.

Method ID example: llm-extract-claude-3.5-prompt-v4
"""

from __future__ import annotations

import json
import hashlib
import datetime
from typing import Optional

METHOD_ID = "llm-extract-claude-3.5-prompt-v4"
MODEL = "claude-3.5-sonnet-20241022"
TEMPERATURE = 0.0
SEED = 42

PROMPT_TEMPLATE = """\
You are a careful probability extractor.
Read the text below and reply with ONLY a single number between 0 and 1
that best represents the author's implied probability for the event.
Do not explain. Do not add any other text.

Text:
\"\"\"{source_text}\"\"\"
"""


def prompt_hash(template: str = PROMPT_TEMPLATE) -> str:
    return hashlib.sha256(template.encode("utf-8")).hexdigest()[:16]


def build_prompt(source_text: str) -> str:
    return PROMPT_TEMPLATE.format(source_text=source_text)


def call_llm(prompt: str) -> float:
    """
    Placeholder for the real model call.
    Replace with a real client that uses the pinned MODEL, TEMPERATURE and SEED.
    This mock is deterministic and offline-safe.
    """
    h = int(hashlib.sha256(prompt.encode()).hexdigest()[:8], 16)
    return round((h % 1000) / 1000.0, 2)


def make_record(
    *,
    prediction_id: str,
    forecaster_id: str,
    topic: str,
    source_text: str,
    outcome: Optional[float] = None,
    resolved_at: Optional[str] = None,
) -> dict:
    prompt = build_prompt(source_text)
    p = call_llm(prompt)

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
        "probability_model": MODEL,
        "probability_prompt_hash": prompt_hash(),
        "probability_seed": SEED,
    }
    if resolved_at is not None:
        record["resolved_at"] = resolved_at
    return record


if __name__ == "__main__":
    examples = [
        {
            "prediction_id": "ex-llm-001",
            "forecaster_id": "bob",
            "topic": "economy",
            "source_text": "The report discusses mild recession odds in the coming year.",
        },
        {
            "prediction_id": "ex-llm-002",
            "forecaster_id": "carol",
            "topic": "tech",
            "source_text": "I expect the model release before summer.",
        },
    ]

    print(f"# METHOD_ID   = {METHOD_ID}")
    print(f"# MODEL       = {MODEL}")
    print(f"# PROMPT_HASH = {prompt_hash()}")
    print(f"# SEED        = {SEED}")
    print()

    for ex in examples:
        rec = make_record(**ex)
        print(json.dumps(rec, ensure_ascii=False))
