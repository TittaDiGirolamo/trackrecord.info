#!/usr/bin/env python3
"""Base interface for topic modules."""

from __future__ import annotations
from typing import Protocol, runtime_checkable


@runtime_checkable
class TopicModule(Protocol):
    """Every topic module must implement these methods."""

    name: str
    """Short identifier, e.g. 'world_cup_2026'"""

    def matches(self, claim: str) -> bool:
        """Return True if this module should handle the claim."""
        ...

    def normalize_topic(self, claim: str) -> str:
        ...

    def suggest_probability(self, claim: str) -> float:
        ...

    def suggest_resolution_criteria(self, claim: str) -> str:
        ...

    def rationale_templates(self, claim: str, probability: float) -> list[str]:
        ...
