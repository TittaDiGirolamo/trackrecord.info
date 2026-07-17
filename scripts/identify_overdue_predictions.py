#!/usr/bin/env python3
"""
FR-01: Overdue Candidate Identification (Hard Gate)
Trackrecord.info — Overdue Predictions Resolution Requirements v1.1

Produces the exact, reproducible list of records where:
  resolution_date ≤ 2026-07-16
  AND outcome is null / missing

Outputs:
  - Machine-readable:  overdue_candidates_2026-07-16.jsonl
  - Human-readable:    overdue_candidates_2026-07-16.md

Usage:
  python3 scripts/identify_overdue_predictions.py
  python3 scripts/identify_overdue_predictions.py --cutoff 2026-07-16
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
DEFAULT_CUTOFF = "2026-07-16"
PREDICTIONS_FILE = Path("predictions_v2.jsonl")
OUTPUT_JSONL = Path("overdue_candidates_2026-07-16.jsonl")
OUTPUT_MD = Path("overdue_candidates_2026-07-16.md")


def parse_date(value: Any) -> date | None:
    """Parse ISO date string or return None."""
    if value is None:
        return None
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(str(value)[:10])
    except (ValueError, TypeError):
        return None


def is_unresolved(record: dict) -> bool:
    """A record is unresolved if and only if the outcome field is missing or null."""
    return record.get("outcome") is None


def load_records(path: Path) -> list[dict]:
    records = []
    with path.open(encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"WARNING: skipping malformed line {lineno}: {e}", file=sys.stderr)
    return records


def identify_overdue(records: list[dict], cutoff: date) -> list[dict]:
    overdue = []
    for rec in records:
        res_date = parse_date(rec.get("resolution_date"))
        if res_date is None:
            continue
        if res_date <= cutoff and is_unresolved(rec):
            overdue.append(rec)
    # Primary sort: resolution_date ascending
    # Secondary: author lastname, then original_statement
    overdue.sort(
        key=lambda r: (
            parse_date(r.get("resolution_date")) or date.min,
            (r.get("author") or {}).get("lastname", "").lower(),
            (r.get("original_statement") or "")[:80],
        )
    )
    return overdue


def write_jsonl(records: list[dict], path: Path) -> None:
    with path.open("w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def write_markdown(records: list[dict], path: Path, cutoff: date) -> None:
    lines = [
        "# Overdue Candidates — FR-01 Identification Output",
        "",
        f"**Generated:** {date.today().isoformat()}",
        f"**Cutoff:** resolution_date ≤ {cutoff.isoformat()}",
        f"**Source:** predictions_v2.jsonl",
        f"**Count:** {len(records)}",
        "",
        "This list is the authoritative FR-01 output required by",
        "`resolution_requirements_overdue_2026-07-17.md` (v1.1).",
        "No resolution work may begin until this list is embedded or linked.",
        "",
        "| # | statement_id / key | resolution_date | author | original_statement (truncated) |",
        "|---|--------------------|-----------------|--------|-------------------------------|",
    ]

    for i, rec in enumerate(records, 1):
        sid = (
            rec.get("statement_id")
            or rec.get("id")
            or rec.get("record_id")
            or f"line-{i}"
        )
        res_date = rec.get("resolution_date", "")
        author = rec.get("author") or {}
        author_str = f"{author.get('firstname', '')} {author.get('lastname', '')}".strip() or "[anonymous]"
        stmt = (rec.get("original_statement") or "")[:90].replace("\n", " ")
        if len(rec.get("original_statement") or "") > 90:
            stmt += "…"
        lines.append(f"| {i} | `{sid}` | {res_date} | {author_str} | {stmt} |")

    lines.append("")
    lines.append("---")
    lines.append(f"**Total overdue records:** {len(records)}")
    lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="FR-01 Overdue Candidate Identification")
    parser.add_argument(
        "--cutoff",
        default=DEFAULT_CUTOFF,
        help=f"ISO date cutoff (default: {DEFAULT_CUTOFF})",
    )
    parser.add_argument(
        "--predictions",
        type=Path,
        default=PREDICTIONS_FILE,
        help="Path to predictions_v2.jsonl",
    )
    args = parser.parse_args()

    try:
        cutoff = date.fromisoformat(args.cutoff)
    except ValueError:
        print(f"ERROR: invalid cutoff date '{args.cutoff}'", file=sys.stderr)
        return 1

    if not args.predictions.exists():
        print(f"ERROR: {args.predictions} not found", file=sys.stderr)
        return 1

    records = load_records(args.predictions)
    overdue = identify_overdue(records, cutoff)

    write_jsonl(overdue, OUTPUT_JSONL)
    write_markdown(overdue, OUTPUT_MD, cutoff)

    print(f"FR-01 complete.")
    print(f"  Total records scanned : {len(records)}")
    print(f"  Overdue (cutoff ≤ {cutoff}) : {len(overdue)}")
    print(f"  Machine-readable      : {OUTPUT_JSONL}")
    print(f"  Human-readable        : {OUTPUT_MD}")
    print()
    print("Next required step (Phase 0):")
    print("  Embed or permanently link the contents of the Markdown file")
    print("  into resolution_requirements_overdue_2026-07-17.md")
    print("  or the first resolution_sessions/YYYY-MM-DD_batchXX.md file.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
