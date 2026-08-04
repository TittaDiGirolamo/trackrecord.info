#!/usr/bin/env python3
"""
Optional frozen-LLM draft for probability rationales.

This is a template. In production:
  1. Pin a specific model snapshot.
  2. Freeze the prompt and record its content hash.
  3. Use temperature = 0.
  4. Bump METHOD_ID whenever the prompt or model changes.

The draft is NEVER written automatically into the live dataset.
A human must still accept or edit it.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Optional

METHOD_ID = "llm-rationale-draft-v1"
MODEL = "grok-4.5-2026"
TEMPERATURE = 0.0

PROMPT_TEMPLATE = """\
You are helping document a forecasting track record.

Given the following public prediction claim and the probability that a human reviewer has chosen,
write a short (2–4 sentence) plain-English rationale that explains why that probability is reasonable.

Rules:
- Be neutral and factual.
- Mention that no numerical probability was stated by the original speaker (if true).
- Do not invent market odds or external data that are not provided.
- Do not use first-person.

Claim: {claim}
Chosen probability: {probability}

Rationale:"""


def prompt_hash() -> str:
    return hashlib.sha256(PROMPT_TEMPLATE.encode("utf-8")).hexdigest()[:16]


def build_prompt(claim: str, probability: float) -> str:
    return PROMPT_TEMPLATE.format(claim=claim.strip(), probability=f"{probability:.2f}")


def make_provenance(claim: str, probability: float, draft: str) -> dict:
    """Return the provenance fields that should be stored alongside the rationale."""
    return {
        "probability_method_id": METHOD_ID,
        "probability_model": MODEL,
        "probability_prompt_hash": prompt_hash(),
        "probability_generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "probability_source": claim[:300],
        "llm_draft_rationale": draft,          # keep the raw draft for audit
    }


# ---------------------------------------------------------------------------
# Placeholder for the actual LLM call.
# Replace the body of this function with your real client (Anthropic, OpenAI, etc.)
# ---------------------------------------------------------------------------
def call_llm(prompt: str) -> str:
    """
    Return a draft rationale.
    For now this is a deterministic stub so the rest of the pipeline can be tested
    without network or API keys. Replace with a real call when ready.
    """
    # --- real implementation would look like: ---
    # client = anthropic.Anthropic()
    # resp = client.messages.create(model=MODEL, max_tokens=300, temperature=TEMPERATURE,
    #                               messages=[{"role": "user", "content": prompt}])
    # return resp.content[0].text.strip()
    # --------------------------------------------

    return (
        "The claim is a clear directional statement. No numerical probability was provided "
        "by the original speaker. The chosen value reflects moderate confidence consistent "
        "with similar qualitative predictions while remaining conservative."
    )


def draft_rationale(claim: str, probability: float) -> tuple[str, dict]:
    """
    Returns (draft_text, provenance_dict).
    The caller must still present the draft to a human for acceptance/editing.
    """
    prompt = build_prompt(claim, probability)
    draft = call_llm(prompt)
    provenance = make_provenance(claim, probability, draft)
    return draft, provenance
