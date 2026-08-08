#!/usr/bin/env python3
"""Topic module registry."""

from __future__ import annotations
from .world_cup_2026 import WorldCup2026
from .base import TopicModule

# Ordered list – first match wins
MODULES: list[TopicModule] = [
    WorldCup2026(),
]


class GenericTopic:
    """Fallback when no specific module matches."""
    name = "generic"

    def matches(self, claim: str) -> bool:
        return True

    def normalize_topic(self, claim: str) -> str:
        return "General"

    def suggest_probability(self, claim: str) -> float:
        return 0.30

    def suggest_resolution_criteria(self, claim: str) -> str:
        return (
            "The claim is verified against primary, authoritative sources "
            "relevant to the subject matter."
        )

    def rationale_templates(self, claim: str, probability: float) -> list[str]:
        return [
            (
                f"The claim is a directional statement without an explicit numerical probability. "
                f"{probability:.2f} is a conservative human-elicited value."
            ),
            (
                f"No numerical odds were provided by the forecaster. "
                f"A probability of {probability:.2f} reflects moderate confidence."
            ),
            (
                f"Language is directional but not emphatic. "
                f"{probability:.2f} avoids over-confidence."
            ),
        ]

    def display_tags(self, claim: str, statement_topic: str = "") -> list[str]:
        topic = (statement_topic or "").strip()
        if not topic or topic.lower() in ("general", "untagged"):
            return []
        parts = [p.strip() for p in topic.split(" - ") if p.strip()]
        umbrellas = ("fifa world cup 2026", "fifa world cup", "world cup 2026", "general")
        if parts and parts[0].lower() in umbrellas:
            parts = parts[1:]
        out = []
        for p in parts:
            if p.lower().endswith(" performance"):
                p = p[: -len(" Performance")]
            out.append(p)
        return out



GENERIC = GenericTopic()


def get_topic_module(claim: str, statement_topic: str = "") -> TopicModule:
    """Return the first matching topic module, or the generic fallback."""
    blob = f"{claim or ''} {statement_topic or ''}".strip()
    for mod in MODULES:
        if mod.matches(blob):
            return mod
    return GENERIC
