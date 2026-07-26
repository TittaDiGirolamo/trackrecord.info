#!/usr/bin/env python3
"""
CI Consistency Gate

Recomputes every forecaster’s scores with the canonical function and
compares them to the values in score_composition.json.
Any mismatch → non-zero exit.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scoring import score_forecaster, format_brier

DATA = ROOT / "data" / "predictions_v2.jsonl"
PUBLIC = ROOT / "public"
COMPOSITION = PUBLIC / "score_composition.json"


def load_predictions() -> List[Dict[str, Any]]:
    preds = []
    with DATA.open() as f:
        for line in f:
            line = line.strip()
            if line:
                preds.append(json.loads(line))
    return preds


def group_by_forecaster(preds: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    groups: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for p in preds:
        groups[p["forecaster_id"]].append(p)
    return dict(groups)


def nearly_equal(a: float | None, b: float | None, tol: float = 1e-9) -> bool:
    if a is None and b is None:
        return True
    if a is None or b is None:
        return False
    return abs(a - b) < tol


def main() -> int:
    if not COMPOSITION.exists():
        print("FAIL: public/score_composition.json does not exist. Run regenerate first.")
        return 1

    with COMPOSITION.open() as f:
        published = json.load(f)

    preds = load_predictions()
    by_forecaster = group_by_forecaster(preds)
    recomputed = {fid: score_forecaster(ps) for fid, ps in by_forecaster.items()}

    errors: List[str] = []

    pub_fids = set(published.get("forecasters", {}).keys())
    rec_fids = set(recomputed.keys())
    if pub_fids != rec_fids:
        missing = rec_fids - pub_fids
        extra = pub_fids - rec_fids
        if missing:
            errors.append(f"Missing from published composition: {sorted(missing)}")
        if extra:
            errors.append(f"Extra in published composition: {sorted(extra)}")

    for fid in sorted(rec_fids & pub_fids):
        rec = recomputed[fid]
        pub = published["forecasters"][fid]

        if not nearly_equal(rec["overall"], pub.get("overall_score")):
            errors.append(
                f"{fid}: overall Brier mismatch – "
                f"canonical={format_brier(rec['overall'])}  "
                f"published={format_brier(pub.get('overall_score'))}"
            )

        if rec["resolved_count"] != pub.get("resolved_count"):
            errors.append(
                f"{fid}: resolved_count mismatch – "
                f"canonical={rec['resolved_count']}  published={pub.get('resolved_count')}"
            )

        if sorted(rec["prediction_ids"]) != sorted(pub.get("prediction_ids", [])):
            errors.append(f"{fid}: prediction_ids differ")

        for topic, t_rec in rec["topics"].items():
            t_pub = pub.get("topics", {}).get(topic)
            if t_pub is None:
                errors.append(f"{fid}/{topic}: topic missing from published composition")
                continue
            if not nearly_equal(t_rec["score"], t_pub.get("score")):
                errors.append(
                    f"{fid}/{topic}: topic Brier mismatch – "
                    f"canonical={format_brier(t_rec['score'])}  "
                    f"published={format_brier(t_pub.get('score'))}"
                )

    if errors:
        print("SCORE CONSISTENCY CHECK FAILED")
        print("=" * 60)
        for e in errors:
            print(f"  • {e}")
        print("=" * 60)
        print(f"{len(errors)} mismatch(es) found. Deployment blocked.")
        return 1

    print("SCORE CONSISTENCY CHECK PASSED")
    print(f"  Checked {len(recomputed)} forecasters against score_composition.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
