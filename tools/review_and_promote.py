#!/usr/bin/env python3
"""
One-shot review + promote for trackrecord.info

Shows a compact table of all status=queued captures,
lets you approve / skip / set probability & rationale,
then runs the normal promote path (dry-run first).

Usage:
  python3 tools/review_and_promote.py
  python3 tools/review_and_promote.py --apply
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CAPTURE_LOG = ROOT / "data" / "capture_log.jsonl"
sys.path.insert(0, str(ROOT / "tools"))

from tools.topics import get_topic_module

def load_captures() -> list[dict]:
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


def save_captures(rows: list[dict]) -> None:
    with CAPTURE_LOG.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def print_table(queued: list[dict]) -> None:
    print("\nQueued captures")
    print("-" * 100)
    print(f"{'#':>3}  {'ID':<18}  {'Forecaster':<22}  {'Claim':<40}  {'p':>5}")
    print("-" * 100)
    for i, c in enumerate(queued, 1):
        claim = (c.get("rough_claim") or c.get("raw_quote") or "")[:38]
        p = c.get("stated_probability")
        p_str = f"{p:.2f}" if p is not None else " — "
        print(f"{i:>3}  {c.get('capture_id','?'):<18}  {c.get('forecaster','?'):<22}  {claim:<40}  {p_str:>5}")
    print("-" * 100)


def review_one(cap: dict) -> dict | None:
    claim = cap.get("rough_claim") or cap.get("raw_quote") or ""
    mod = get_topic_module(cap.get("rough_claim") or cap.get("raw_quote") or "")
    suggested = mod.suggest_probability(cap.get("rough_claim") or cap.get("raw_quote") or "")
    ...
    templates = mod.rationale_templates(cap.get("rough_claim") or "", p)
    ...
    topic = mod.normalize_topic(cap.get("rough_claim") or "")

    action = input("Action: [a]pprove  [s]kip  [e]dit probability/rationale  [q]uit  [a]: ").strip().lower() or "a"
    if action == "q":
        return "QUIT"
    if action == "s":
        cap["status"] = "skipped"
        print("  → skipped")
        return cap

    # Probability
    current = cap.get("stated_probability")
    default = current if current is not None else suggested
    ans = input(f"  Probability 0-1 [{default:.2f}]: ").strip()
    if ans:
        try:
            p = float(ans)
            if not (0.0 <= p <= 1.0):
                print("  Invalid probability – keeping previous")
                p = default
        except ValueError:
            print("  Invalid number – keeping previous")
            p = default
    else:
        p = default
    cap["stated_probability"] = p

    # Rationale
    templates = rationale_templates(cap.get("rough_claim") or "", p)
    print("\n  Rationale templates:")
    for i, t in enumerate(templates, 1):
        print(f"    [{i}] {t[:90]}...")
    print("    [4] Write my own")
    choice = input("  Choose 1-4 [1]: ").strip() or "1"
    if choice in ("1", "2", "3"):
        cap["probability_rationale"] = templates[int(choice) - 1]
    else:
        from promote_captures import prompt_nonempty
        cap["probability_rationale"] = prompt_nonempty("  Enter rationale: ")

    # Topic suggestion (stored for later)
    topic = normalize_topic(cap.get("rough_claim") or "")
    t = input(f"  Topic [{topic}]: ").strip()
    if t:
        topic = t
    cap["statement_topic"] = topic

    # Resolution criteria (suggested, human confirms)
    current_criteria = (cap.get("resolution_criteria") or "").strip()
    suggested_criteria = mod.suggest_resolution_criteria(claim)
    if current_criteria:
        print(f"\n  Current resolution_criteria:\n    {current_criteria}")
    print(f"\n  Suggested resolution_criteria:\n    {suggested_criteria}")
    ans = input("  Accept suggestion / edit / keep current? [a]ccept  [e]dit  [k]eep  [a]: ").strip().lower() or "a"
    if ans == "a":
        cap["resolution_criteria"] = suggested_criteria
    elif ans == "e":
        from promote_captures import prompt_nonempty
        cap["resolution_criteria"] = prompt_nonempty("  Enter resolution_criteria: ")
    # else keep whatever is already there

    cap["status"] = "queued"  # ensure it stays queued for promote
    print("  → approved for promote")
    return cap


def main() -> int:
    parser = argparse.ArgumentParser(description="Review queued captures then promote")
    parser.add_argument("--apply", action="store_true", help="Actually promote after review")
    args = parser.parse_args()

    captures = load_captures()
    queued = [c for c in captures if c.get("status") == "queued"]

    if not queued:
        print("No captures with status=queued.")
        return 0

    print_table(queued)

    print("\nReview each capture (or press Enter to approve with suggestions)")
    updated = []
    for cap in queued:
        result = review_one(cap)
        if result == "QUIT":
            print("Stopped by user.")
            break
        if result is not None:
            # replace in the full list
            for i, c in enumerate(captures):
                if c.get("capture_id") == result.get("capture_id"):
                    captures[i] = result
                    break
            updated.append(result)

    save_captures(captures)
    print(f"\nSaved {len(updated)} reviewed capture(s).")

    if not updated:
        print("Nothing left to promote.")
        return 0

    # Run the normal promote path
    cmd = [sys.executable, str(ROOT / "tools" / "promote_captures.py")]
    if args.apply:
        cmd.append("--apply")
        print("\nRunning promote with --apply ...")
    else:
        print("\nRunning promote dry-run ...")

    return subprocess.call(cmd)


if __name__ == "__main__":
    sys.exit(main())
