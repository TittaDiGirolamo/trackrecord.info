#!/usr/bin/env python3
"""Rule-based probability extractor – primary method (rule-extract-keyword-v2)."""

import json
import re
import datetime
from typing import Optional

METHOD_ID = "rule-extract-keyword-v2"

RULES = [
    (r"\b(almost\s+certain|virtually\s+certain|extremely\s+likely)\b", 0.95),
    (r"\b(highly\s+probable|highly\s+likely|very\s+likely)\b", 0.85),
    (r"\b(probable|likely|expected|more\s+likely\s+than\s+not)\b", 0.70),
    (r"\b(somewhat\s+likely|rather\s+likely)\b", 0.60),
    (r"\b(about\s+even|roughly\s+even|toss[- ]?up|50[- ]?50)\b", 0.50),
    (r"\b(possible|could\s+happen|might)\b", 0.40),
    (r"\b(somewhat\s+unlikely|rather\s+unlikely)\b", 0.35),
    (r"\b(unlikely|improbable|doubtful)\b", 0.25),
    (r"\b(highly\s+unlikely|very\s+unlikely)\b", 0.15),
    (r"\b(almost\s+impossible|extremely\s+unlikely|virtually\s+impossible)\b", 0.05),
]

def extract_probability(text: str) -> Optional[float]:
    lowered = text.lower()
    for pattern, prob in RULES:
        if re.search(pattern, lowered):
            return prob
    return None

if __name__ == "__main__":
    examples = [
        "I think it is more likely than not that the ceasefire holds",
        "It is highly probable that sanctions will be lifted",
        "AGI this decade is highly unlikely",
    ]
    for text in examples:
        p = extract_probability(text)
        print(f"{p:.2f}  ←  {text}")
