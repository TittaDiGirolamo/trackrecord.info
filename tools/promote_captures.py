#!/usr/bin/env python3
"""
Promote queued captures into predictions_v2.jsonl as pending rows only.

Default is dry-run. Use --apply to write.
Only status=queued rows are considered.
outcome is always null.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

ROOT = Path(__file__).resolve().parent.parent
CAPTURE_LOG = ROOT / "data" / "capture_log.jsonl"
PREDICTIONS = ROOT / "predictions_v2.jsonl"
if not PREDICTIONS.exists():
    PREDICTIONS = ROOT / "data" / "predictions_v2.jsonl"


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"WARNING: skip malformed line in {path.name}: {e}", file=sys.stderr)
    return rows


def save_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def normalize_for_dupe(s: str) -> str:
    s = (s or "").lower().strip()
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"[^\w\s]", "", s)
    return s


def is_duplicate(existing: list[dict], url: str, statement: str) -> Optional[str]:
    norm_stmt = normalize_for_dupe(statement)
    for row in existing:
        if row.get("statement_original_url") != url:
            continue
        existing_stmt = normalize_for_dupe(row.get("original_statement", ""))
        if norm_stmt == existing_stmt or (
            len(norm_stmt) > 20
            and (norm_stmt in existing_stmt or existing_stmt in norm_stmt)
        ):
            return row.get("statement_id")
    return None


def slugify(text: str, max_len: int = 40) -> str:
    text = (text or "").lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text).strip("-")
    return text[:max_len].rstrip("-") or "claim"


def make_statement_id(forecaster: str, pub_date: str, claim: str, existing_ids: set[str]) -> str:
    last = "unknown"
    if "," in forecaster:
        last = forecaster.split(",")[0].strip().lower()
    else:
        parts = forecaster.strip().split()
        last = parts[-1].lower() if parts else "unknown"
    last = re.sub(r"[^a-z0-9]", "", last) or "unknown"
    slug = slugify(claim, 32)
    base = f"pred-{pub_date}-{last}-{slug}"
    candidate = base
    n = 1
    while candidate in existing_ids:
        n += 1
        candidate = f"{base}-{n}"
    return candidate


def parse_forecaster_to_author(forecaster: str) -> dict:
    if "," in forecaster:
        last, first = [p.strip() for p in forecaster.split(",", 1)]
        return {"lastname": last or "[anonymous]", "firstname": first}
    parts = forecaster.strip().split()
    if len(parts) >= 2:
        return {"lastname": parts[-1], "firstname": " ".join(parts[:-1])}
    return {"lastname": forecaster or "[anonymous]", "firstname": ""}


def prompt_nonempty(prompt: str, default: str = "") -> str:
    while True:
        raw = input(f"{prompt} ").strip()
        if raw:
            return raw
        if default:
            return default
        print("  (required, cannot be empty)")


def build_prediction_row(
    cap: dict,
    existing_preds: list[dict],
    existing_ids: set[str],
    interactive: bool,
) -> tuple[dict, dict]:
    source_url = cap["source_url"]
    rough = cap.get("rough_claim") or cap.get("raw_quote") or ""
    raw_quote = cap.get("raw_quote") or ""
    forecaster = cap["forecaster"]
    stated_p = cap.get("stated_probability")

    dup_id = is_duplicate(existing_preds, source_url, rough)
    if dup_id:
        raise ValueError(
            f"Refusing promote: duplicate of existing statement_id={dup_id} "
            f"(same url + similar statement)"
        )

    captured = cap.get("captured_at") or ""
    pub_date = captured[:10] if len(captured) >= 10 else datetime.now(timezone.utc).strftime("%Y-%m-%d")

    probability_method_id = None
    if stated_p is not None:
        statement_probability = float(stated_p)
        probability_method_id = "human-elicited-v1"
    else:
        if interactive:
            print(f"\n  Capture {cap['capture_id']} has no stated_probability.")
            ans = input("  Enter probability 0-1 (or leave blank to abort this row): ").strip()
            if not ans:
                raise ValueError("Aborted: probability required when not stated")
            statement_probability = float(ans)
            if not (0.0 <= statement_probability <= 1.0):
                raise ValueError("probability must be in [0, 1]")
            probability_method_id = "human-elicited-v1"
        else:
            raise ValueError(
                "stated_probability is null and non-interactive; "
                "cannot promote without a probability"
            )

    criteria = cap.get("resolution_criteria") or ""
    if not criteria.strip():
        if interactive:
            print(f"\n  Capture {cap['capture_id']} missing resolution_criteria.")
            print(f"  Claim: {rough[:120]}...")
            criteria = prompt_nonempty("  Enter resolution_criteria:")
        else:
            raise ValueError("resolution_criteria missing and non-interactive mode")

    topic = cap.get("statement_topic") or "FIFA World Cup 2026"
    if interactive and not cap.get("statement_topic"):
        t = input(f"  statement_topic [{topic}]: ").strip()
        if t:
            topic = t

    context = cap.get("statement_context") or (
        f"Captured from public source. Raw quote: {raw_quote[:200]}"
    )

    statement_id = make_statement_id(forecaster, pub_date, rough, existing_ids)
    existing_ids.add(statement_id)

    author = parse_forecaster_to_author(forecaster)

    orig = rough.strip()
    if len(orig) < 20:
        orig = f"{orig} [{forecaster}, {pub_date}]"
    elif "[" not in orig:
        orig = f"{orig} [{forecaster}, {pub_date}]"

    pred = {
        "original_statement": orig,
        "author": author,
        "statement_id": statement_id,
        "statement_topic": topic,
        "statement_publication_date": pub_date,
        "statement_original_url": source_url,
        "statement_probability": statement_probability,
        "statement_context": context,
        "resolution_criteria": criteria.strip(),
        "forecaster": forecaster,
        "outcome": None,
        "extraction_timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "source_text_snippet": raw_quote[:300] if raw_quote else None,
        "probability_method_id": probability_method_id,
    }

    updated_cap = {
        "status": "promoted",
        "promoted_statement_id": statement_id,
        "promoted_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    return pred, updated_cap


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Promote status=queued captures → pending rows in predictions_v2.jsonl"
    )
    parser.add_argument("--apply", action="store_true", help="Actually write (default is dry-run)")
    parser.add_argument("--non-interactive", action="store_true", help="Fail instead of prompting")
    args = parser.parse_args()
    interactive = not args.non_interactive and sys.stdin.isatty()

    captures = load_jsonl(CAPTURE_LOG)
    queued = [c for c in captures if c.get("status") == "queued"]

    if not queued:
        print("No captures with status=queued. Nothing to promote.")
        print("Tip: set status=queued on desired rows in data/capture_log.jsonl")
        return 0

    preds = load_jsonl(PREDICTIONS)
    existing_ids = {p.get("statement_id") for p in preds if p.get("statement_id")}

    print(f"Found {len(queued)} queued capture(s). Mode: {'APPLY' if args.apply else 'DRY-RUN'}")
    print(f"Authority file: {PREDICTIONS.relative_to(ROOT)}")
    print("-" * 60)

    to_append: list[dict] = []
    capture_updates: dict[str, dict] = {}
    errors = 0

    for cap in queued:
        cid = cap.get("capture_id", "?")
        print(f"\nProcessing {cid} …")
        try:
            pred, upd = build_prediction_row(
                cap, preds + to_append, existing_ids, interactive
            )
            to_append.append(pred)
            capture_updates[cid] = upd
            print(f"  → statement_id = {pred['statement_id']}")
            print(f"  → probability  = {pred['statement_probability']} ({pred.get('probability_method_id')})")
            print(f"  → outcome      = null (pending)")
            print(f"  → criteria     = {pred['resolution_criteria'][:80]}…")
        except ValueError as e:
            print(f"  REFUSED: {e}")
            errors += 1
            continue
        except Exception as e:
            print(f"  ERROR: {e}")
            errors += 1
            continue

    if not to_append:
        print("\nNo rows ready to promote.")
        return 1 if errors else 0

    print("\n" + "=" * 60)
    print(f"Ready to promote {len(to_append)} row(s).")
    if not args.apply:
        print("DRY-RUN — no files written. Re-run with --apply to commit.")
        print("\nLive-shaped rows that would be appended:")
        for p in to_append:
            print(json.dumps(p, ensure_ascii=False, indent=2))
            print("---")
        return 0

    with PREDICTIONS.open("a", encoding="utf-8") as f:
        for p in to_append:
            f.write(json.dumps(p, ensure_ascii=False) + "\n")
    print(f"Appended {len(to_append)} pending row(s) to {PREDICTIONS.relative_to(ROOT)}")

    data_pred = ROOT / "data" / "predictions_v2.jsonl"
    if data_pred.exists() and data_pred.resolve() != PREDICTIONS.resolve():
        with data_pred.open("a", encoding="utf-8") as f:
            for p in to_append:
                f.write(json.dumps(p, ensure_ascii=False) + "\n")
        print(f"Also synced data/predictions_v2.jsonl")

    new_captures = []
    for c in captures:
        cid = c.get("capture_id")
        if cid in capture_updates:
            c = {**c, **capture_updates[cid]}
        new_captures.append(c)
    save_jsonl(CAPTURE_LOG, new_captures)
    print(f"Updated {len(capture_updates)} capture(s) → status=promoted")

    print("\nNext steps (must pass):")
    print("  python3 regenerate_all.py")
    print("  python3 ci/check_score_consistency.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
