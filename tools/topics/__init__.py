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


GENERIC = GenericTopic()


def get_topic_module(claim: str) -> TopicModule:
    """Return the first matching topic module, or the generic fallback."""
    for mod in MODULES:
        if mod.matches(claim):
            return mod
    return GENERIC
