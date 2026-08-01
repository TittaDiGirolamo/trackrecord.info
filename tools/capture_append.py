#!/usr/bin/env python3
"""
Minimal capture append CLI for trackrecord.info Phase-1 foundation.

Appends one scratch row to data/capture_log.jsonl.
Never touches predictions_v2.jsonl or scores.
"""
from __future__ import annotations

import argparse
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CAPTURE_LOG = ROOT / "data" / "capture_log.jsonl"


def load_existing() -> list[dict]:
    if not CAPTURE_LOG.exists():
        return []
    rows = []
    with CAPTURE_LOG.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Append a scratch capture row (never scored)."
    )
    parser.add_argument("--source-url", required=True, help="Public source URL (required)")
    parser.add_argument("--forecaster", required=True, help="Forecaster name, e.g. 'Lastname, Firstname'")
    parser.add_argument("--raw-quote", required=True, help="Exact quoted text from source")
    parser.add_argument("--rough-claim", default="", help="Normalized claim text (optional)")
    parser.add_argument(
        "--stated-probability",
        type=float,
        default=None,
        help="Stated probability 0-1 or omit for null",
    )
    parser.add_argument(
        "--status",
        choices=["new", "queued", "promoted", "skipped"],
        default="new",
        help="Initial status (default: new)",
    )
    parser.add_argument(
        "--resolution-criteria",
        default="",
        help="Optional resolution criteria (useful when status=queued)",
    )
    args = parser.parse_args()

    source_url = (args.source_url or "").strip()
    forecaster = (args.forecaster or "").strip()
    raw_quote = (args.raw_quote or "").strip()
    rough_claim = (args.rough_claim or "").strip() or raw_quote

    if not source_url:
        print("ERROR: --source-url must be non-empty", file=sys.stderr)
        return 1
    if not forecaster:
        print("ERROR: --forecaster must be non-empty", file=sys.stderr)
        return 1
    if not raw_quote:
        print("ERROR: --raw-quote must be non-empty", file=sys.stderr)
        return 1

    if args.stated_probability is not None:
        if not (0.0 <= args.stated_probability <= 1.0):
            print("ERROR: --stated-probability must be in [0, 1]", file=sys.stderr)
            return 1

    existing = load_existing()
    for row in existing:
        if (
            row.get("source_url") == source_url
            and row.get("raw_quote") == raw_quote
        ):
            print(
                f"WARNING: exact duplicate already exists "
                f"(capture_id={row.get('capture_id')}, status={row.get('status')})",
                file=sys.stderr,
            )

    capture_id = f"cap-{uuid.uuid4().hex[:12]}"
    captured_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    row = {
        "capture_id": capture_id,
        "captured_at": captured_at,
        "source_url": source_url,
        "forecaster": forecaster,
        "raw_quote": raw_quote,
        "rough_claim": rough_claim,
        "stated_probability": args.stated_probability,
        "status": args.status,
    }
    if args.resolution_criteria.strip():
        row["resolution_criteria"] = args.resolution_criteria.strip()

    CAPTURE_LOG.parent.mkdir(parents=True, exist_ok=True)
    with CAPTURE_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"Appended capture_id={capture_id} status={args.status}")
    print(f"  log: {CAPTURE_LOG.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
