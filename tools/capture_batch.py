#!/usr/bin/env python3
"""
Batch capture helper for trackrecord.info.

Reads a CSV (or JSONL) of candidate predictions and appends them
to data/capture_log.jsonl as status=new (or the status you specify).

Never touches predictions_v2.jsonl or scores.
Human review (status → queued) remains mandatory.

Usage:
  python3 tools/capture_batch.py candidates.csv
  python3 tools/capture_batch.py candidates.jsonl --format jsonl
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import uuid
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CAPTURE_LOG = ROOT / "data" / "capture_log.jsonl"
PREDICTIONS = ROOT / "predictions_v2.jsonl"
if not PREDICTIONS.exists():
    PREDICTIONS = ROOT / "data" / "predictions_v2.jsonl"

REQUIRED = ("source_url", "forecaster", "raw_quote")
OPTIONAL = ("rough_claim", "stated_probability", "resolution_criteria", "status")


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


def load_predictions() -> list[dict]:
    if not PREDICTIONS.exists():
        return []
    rows = []
    with PREDICTIONS.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return rows


def is_duplicate_in_log(existing: list[dict], source_url: str, raw_quote: str) -> str | None:
    for row in existing:
        if row.get("source_url") == source_url and row.get("raw_quote") == raw_quote:
            return row.get("capture_id")
    return None


def is_duplicate_in_predictions(preds: list[dict], source_url: str, rough_claim: str, raw_quote: str) -> str | None:
    """Return statement_id if this claim already exists in the live dataset."""
    claim = (rough_claim or raw_quote or "").strip().lower()
    for p in preds:
        if p.get("statement_original_url") == source_url:
            existing_claim = (p.get("original_statement") or "").lower()
            # Simple but effective: same URL + substantial overlap in claim text
            if claim and (claim in existing_claim or existing_claim in claim or
                          claim[:60] == existing_claim[:60]):
                return p.get("statement_id")
        # Also catch same rough claim even on a different URL
        existing_claim = (p.get("original_statement") or "").lower()
        if claim and len(claim) > 20 and claim in existing_claim:
            return p.get("statement_id")
    return None

def append_row(row: dict) -> None:
    CAPTURE_LOG.parent.mkdir(parents=True, exist_ok=True)
    with CAPTURE_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def process_row(raw: dict, existing: list[dict], preds: list[dict], dry_run: bool) -> tuple[str, str]:
    """Returns (status, message)."""
    source_url = (raw.get("source_url") or "").strip()
    forecaster = (raw.get("forecaster") or "").strip()
    raw_quote = (raw.get("raw_quote") or "").strip()
    rough_claim = (raw.get("rough_claim") or "").strip() or raw_quote
    resolution_criteria = (raw.get("resolution_criteria") or "").strip()
    status = (raw.get("status") or "new").strip() or "new"

    if status not in ("new", "queued", "promoted", "skipped"):
        return "error", f"invalid status={status!r}"

    if not source_url or not forecaster or not raw_quote:
        return "error", "missing required field (source_url / forecaster / raw_quote)"

    stated_p = raw.get("stated_probability")
    if stated_p is not None and stated_p != "":
        try:
            stated_p = float(stated_p)
            if not (0.0 <= stated_p <= 1.0):
                return "error", f"stated_probability out of range: {stated_p}"
        except (TypeError, ValueError):
            return "error", f"invalid stated_probability: {stated_p!r}"
    else:
        stated_p = None

    # Check against capture log
    dup_id = is_duplicate_in_log(existing, source_url, raw_quote)
    if dup_id:
        return "skip", f"exact duplicate in capture_log of {dup_id}"

    # Check against already-promoted predictions
    dup_stmt = is_duplicate_in_predictions(preds, source_url, rough_claim, raw_quote)
    if dup_stmt:
        return "skip", f"already exists in predictions_v2.jsonl as {dup_stmt}"

    capture_id = f"cap-{uuid.uuid4().hex[:12]}"
    captured_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    row = {
        "capture_id": capture_id,
        "captured_at": captured_at,
        "source_url": source_url,
        "forecaster": forecaster,
        "raw_quote": raw_quote,
        "rough_claim": rough_claim,
        "stated_probability": stated_p,
        "status": status,
    }
    if resolution_criteria:
        row["resolution_criteria"] = resolution_criteria

    if not dry_run:
        append_row(row)
        existing.append(row)  # so later rows in the same batch see it

    return "ok", f"{capture_id}  {forecaster}  p={stated_p}"


def read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


def read_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Batch append captures to capture_log.jsonl")
    parser.add_argument("file", help="CSV or JSONL file of candidates")
    parser.add_argument("--format", choices=["csv", "jsonl"], default=None,
                        help="Force format (default: guess from extension)")
    parser.add_argument("--dry-run", action="store_true", help="Validate only, do not write")
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 1

    fmt = args.format
    if fmt is None:
        fmt = "jsonl" if path.suffix.lower() in (".jsonl", ".json") else "csv"

    try:
        rows = read_jsonl(path) if fmt == "jsonl" else read_csv(path)
    except Exception as e:
        print(f"ERROR: failed to read {path}: {e}", file=sys.stderr)
        return 1

    if not rows:
        print("No rows found.")
        return 0

    existing = load_existing()
    preds = load_predictions()
    print(f"Loaded {len(rows)} candidate(s). Mode: {'DRY-RUN' if args.dry_run else 'WRITE'}")
    print(f"Existing captures: {len(existing)}  |  Live predictions: {len(preds)}")
    print("-" * 60)

    counts = {"ok": 0, "skip": 0, "error": 0}
    for i, raw in enumerate(rows, 1):
        status, msg = process_row(raw, existing, preds, dry_run=args.dry_run)

    counts = {"ok": 0, "skip": 0, "error": 0}
    for i, raw in enumerate(rows, 1):
        status, msg = process_row(raw, existing, preds, dry_run=args.dry_run)
        counts[status] = counts.get(status, 0) + 1
        symbol = {"ok": "✓", "skip": "–", "error": "✗"}[status]
        print(f"{symbol} [{i:03d}] {status.upper():5}  {msg}")

    print("-" * 60)
    print(f"Done. ok={counts['ok']}  skipped={counts['skip']}  errors={counts['error']}")
    if args.dry_run:
        print("DRY-RUN — nothing written. Re-run without --dry-run to append.")
    else:
        print(f"Log: {CAPTURE_LOG.relative_to(ROOT)}")

    # Auto-open the capture log so the human can immediately review
    if not args.dry_run and counts.get("ok", 0) > 0:
        log_path = str(CAPTURE_LOG)
        editor = os.environ.get("EDITOR") or os.environ.get("VISUAL") or "nano"
        print(f"\nOpening {CAPTURE_LOG.relative_to(ROOT)} in {editor} for review...")
        try:
            # +999999 jumps near the end of the file in most editors
            if editor in ("nano", "vim", "vi", "nvim"):
                subprocess.call([editor, f"+999999", log_path])
            else:
                subprocess.call([editor, log_path])
        except FileNotFoundError:
            print(f"(Could not launch editor '{editor}'. Open the file manually.)")
            
    return 0 if counts["error"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
