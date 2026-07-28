"""Shared display-name and slug helpers — single source of truth for naming."""

import re
import unicodedata
from typing import Tuple


def parse_name(raw: str) -> Tuple[str, str]:
    """Accepts "Last, First" or "First Last". Returns (first, last)."""
    raw = (raw or "").strip()
    if "," in raw:
        last, first = [p.strip() for p in raw.split(",", 1)]
        return first, last
    parts = raw.split()
    if len(parts) >= 2:
        return parts[0], parts[-1]
    return raw, ""


def display_name(raw: str) -> str:
    """Canonical display form: First Last."""
    first, last = parse_name(raw)
    return f"{first} {last}".strip() or raw


def slugify_name(raw: str) -> str:
    """Canonical slug: firstname-lastname, ASCII, lowercase."""
    first, last = parse_name(raw)
    text = f"{first}-{last}".strip("-")
    nfkd = unicodedata.normalize("NFKD", text)
    ascii_text = "".join(c for c in nfkd if not unicodedata.combining(c))
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_text.lower()).strip("-")
    return slug or "unknown"


def initials_from_name(raw: str) -> str:
    first, last = parse_name(raw)
    if first and last:
        return (first[0] + last[0]).upper()
    return (raw[:2] if raw else "??").upper()
