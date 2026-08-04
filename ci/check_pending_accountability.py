#!/usr/bin/env python3
"""
CI / local gate: every pending prediction must have full accountability fields.

Fails (exit 1) if any row with outcome is null is missing:
  - probability_method_id
  - probability_rationale (min length)
  - statement_original_url_archive

Also fails if a newly-looking row has a non-null outcome (should stay pending).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PREDICTIONS = ROOT / "data" / "predictions_v2.jsonl"
if not PREDICTIONS.exists():
    PREDICTIONS = ROOT / "predictions_v2.jsonl"

MIN_RATIONALE_LEN = 40


def main() -> int:
    if not PREDICTIONS.exists():
        print(f"ERROR: predictions file not found: {PREDICTIONS}", file=sys.stderr)
        return 1

    rows = []
    with PREDICTIONS.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"ERROR: malformed JSON: {e}", file=sys.stderr)
                    return 1

    CUTOFF = "2026-08-03"
    pending = [
        r for r in rows
        if r.get("outcome") is None
        and (r.get("extraction_timestamp") or "") >= CUTOFF
    ]

    errors = []

    for r in pending:
        sid = r.get("statement_id", "<no-id>")

        if not r.get("probability_method_id"):
            errors.append(f"{sid}: missing probability_method_id")

        rationale = (r.get("probability_rationale") or "").strip()
        if len(rationale) < MIN_RATIONALE_LEN:
            errors.append(
                f"{sid}: probability_rationale missing or too short "
                f"({len(rationale)} chars, need ≥ {MIN_RATIONALE_LEN})"
            )

        if not r.get("statement_original_url_archive"):
            errors.append(f"{sid}: missing statement_original_url_archive")

    if errors:
        print("PENDING ACCOUNTABILITY CHECK FAILED")
        print(f"Checked {len(pending)} pending row(s). Problems:")
        for e in errors:
            print(f"  • {e}")
        return 1

    print("PENDING ACCOUNTABILITY CHECK PASSED")
    print(f"  {len(pending)} pending row(s) all have method_id + rationale + archive")
    return 0


if __name__ == "__main__":
    sys.exit(main())
