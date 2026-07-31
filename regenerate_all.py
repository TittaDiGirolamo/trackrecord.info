#!/usr/bin/env python3
"""
Phase 1 close — single entrypoint for the LIVE site pipeline.

Reads only predictions_v2.jsonl (repo root).
Runs every public generator in a fixed order.
Writes generation_manifest.json with commit + rules version.

Does NOT use the legacy dual-path regenerate.py → profiles/ tree.
"""
from __future__ import annotations

import json
import subprocess
import sys
import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
JSONL = ROOT / "predictions_v2.jsonl"

# Live generators in dependency order
GENERATORS = [
    "scripts/generate_homepage_scorecards.py",
    "scripts/generate_forecaster_profiles.py",
    "scripts/generate_forecasters_list.py",
    "scripts/generate_prediction_tables.py",
    "scripts/generate_prediction_details.py",
]


def git_commit() -> str:
    try:
        return (
            subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=ROOT, stderr=subprocess.DEVNULL
            )
            .decode()
            .strip()
        )
    except Exception:
        return "unknown"


def count_jsonl(path: Path) -> int:
    if not path.exists():
        return 0
    n = 0
    with path.open() as f:
        for line in f:
            if line.strip():
                n += 1
    return n


def run(script: str) -> None:
    print(f"\n>>> {script}")
    r = subprocess.run([sys.executable, script], cwd=ROOT)
    if r.returncode != 0:
        raise SystemExit(f"FAILED: {script} (exit {r.returncode})")


def main() -> None:
    if not JSONL.exists():
        raise SystemExit(f"Missing sole data source: {JSONL}")

    generation_id = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    commit = git_commit()

    try:
        sys.path.insert(0, str(ROOT))
        from scoring import RULES_VERSION
    except Exception:
        RULES_VERSION = "unknown"

    n_records = count_jsonl(JSONL)
    print("Atomic live regeneration")
    print(f"  generation_id : {generation_id}")
    print(f"  commit        : {commit}")
    print(f"  rules_version : {RULES_VERSION}")
    print(f"  records       : {n_records}")
    print(f"  source        : {JSONL.name}")

    for g in GENERATORS:
        run(g)

    # Canonical composition for CI (same math as scoring package)
    from collections import defaultdict
    from scoring import score_forecaster

    preds = []
    with JSONL.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            raw = json.loads(line)
            preds.append({
                "id": raw.get("statement_id") or raw.get("id"),
                "forecaster_id": raw.get("forecaster") or raw.get("forecaster_id"),
                "topic": raw.get("statement_topic") or raw.get("topic") or "untagged",
                "probability": raw.get("statement_probability") if "statement_probability" in raw else raw.get("probability"),
                "outcome": raw.get("outcome"),
            })
    by_f = defaultdict(list)
    for pr in preds:
        by_f[pr["forecaster_id"]].append(pr)
    composition = {
        "generation_id": generation_id,
        "commit": commit,
        "rules_version": RULES_VERSION,
        "source": "predictions_v2.jsonl",
        "forecasters": {},
    }
    for fid, ps in sorted(by_f.items()):
        s = score_forecaster(ps)
        composition["forecasters"][fid] = {
            "overall_score": s.get("overall"),
            "resolved_count": s.get("resolved_count"),
            "pending_count": s.get("pending_count"),
            "prediction_ids": s.get("prediction_ids", []),
            "topics": {
                t: {"score": td.get("score"), "n": td.get("n") or td.get("resolved_count")}
                for t, td in (s.get("topics") or {}).items()
            },
        }
    comp_path = ROOT / "score_composition.json"
    comp_path.write_text(json.dumps(composition, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote {comp_path.name} ({len(composition['forecasters'])} forecasters)")

    manifest = {
        "generation_id": generation_id,
        "commit": commit,
        "rules_version": RULES_VERSION,
        "source": "predictions_v2.jsonl",
        "record_count": n_records,
        "generators": GENERATORS,
        "note": "Live pipeline only (forecasters/, index.html, predictions/). Legacy regenerate.py → profiles/ is not used.",
    }
    out = ROOT / "generation_manifest.json"
    out.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out.name}")
    print("Atomic live regeneration complete")


if __name__ == "__main__":
    main()
