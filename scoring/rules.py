"""
Published scoring rules — single source of truth for the mathematics.

All backend calculations use Brier score exclusively.
Any "accuracy" number shown on the site is a pure frontend transformation
of these Brier values and is never computed or stored here.
"""

from typing import List, Dict, Any

RULES_VERSION = "brier-1.0.0"

LIMITATIONS_NOTE = (
    "Scores are mean Brier scores (lower is better). "
    "Only resolved predictions are included. "
    "Sample sizes remain modest for many topics; treat rankings as provisional."
)


def score_one(prediction: Dict[str, Any]) -> float:
    """Individual Brier score for one resolved prediction."""
    p = float(prediction["probability"])
    o = float(prediction["outcome"])
    p = max(0.0, min(1.0, p))
    return (p - o) ** 2


def aggregate(contributions: List[float]) -> float | None:
    """Mean Brier score. Returns None if no contributions."""
    if not contributions:
        return None
    return sum(contributions) / len(contributions)


def format_brier(brier: float | None, decimals: int = 3) -> str:
    """Canonical string representation used everywhere in generated pages."""
    if brier is None:
        return "—"
    return f"{brier:.{decimals}f}"


def brier_to_index(brier: float | None) -> float | None:
    """
    Brier Index = (1 - sqrt(Brier)) * 100
    Higher is better, scale 0–100.
    Applied only after the mean Brier is calculated (preserves rankings).
    """
    if brier is None:
        return None
    return (1.0 - (brier ** 0.5)) * 100.0


def format_index(index: float | None, decimals: int = 1) -> str:
    """String representation of the Brier Index for display."""
    if index is None:
        return "—"
    return f"{index:.{decimals}f}"
