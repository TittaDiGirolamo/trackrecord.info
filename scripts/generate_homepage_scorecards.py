#!/usr/bin/env python3
"""
generate_homepage_scorecards.py - Hybrid version
Uses ALL resolved predictions (tiered when available + binary fallback)
"""

import json
import argparse
from collections import defaultdict
from datetime import date
from pathlib import Path

def calculate_forecaster_scores(jsonl_path=Path("predictions_v2.jsonl")):
    if not jsonl_path.exists():
        return {}

    forecasters = defaultdict(lambda: {"overall_scores": [], "resolved_count": 0})

    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except:
                continue

            author = record.get("author", {})
            name = f"{author.get('firstname', '')} {author.get('lastname', '')}".strip() or "Unknown"

            outcome = record.get("outcome")
            weighted = record.get("partial_accuracy", {}).get("weighted_score")

            if outcome is not None:
                if weighted is not None:
                    score = weighted * 100
                else:
                    score = 100.0 if bool(outcome) else 0.0

                forecasters[name]["overall_scores"].append(score)
                forecasters[name]["resolved_count"] += 1

    result = {}
    for name, data in forecasters.items():
        if data["overall_scores"]:
            avg = sum(data["overall_scores"]) / len(data["overall_scores"])
            result[name] = {
                "overall": round(avg, 1),
                "resolved_count": len(data["overall_scores"])
            }
    return result


def get_top_forecasters(scores, n=3, min_resolved=10):
    qualified = [(name, data) for name, data in scores.items() if data["resolved_count"] >= min_resolved]
    if not qualified:
        return []
    qualified.sort(key=lambda x: (-x[1]["overall"], -x[1]["resolved_count"]))
    return qualified[:n]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-resolved", type=int, default=10)
    parser.add_argument("--n", type=int, default=3)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    scores = calculate_forecaster_scores()
    top = get_top_forecasters(scores, args.n, args.min_resolved)

    print(f"Qualified forecasters (>= {args.min_resolved} resolved): {len([k for k,v in scores.items() if v['resolved_count'] >= args.min_resolved])}")
    print(f"Top {args.n} selected: {[name for name, _ in top]}")

    if args.dry_run:
        print("DRY RUN - Not writing file")
    else:
        # Simple HTML output (you can improve styling later)
        html = f"<h2>Top Forecasters</h2><ul>"
        for name, data in top:
            html += f"<li>{name}: {data['overall']} (n={data['resolved_count']})</li>"
        html += "</ul>"

        Path("homepage_scorecards.html").write_text(html)
        print("✅ homepage_scorecards.html updated!")


if __name__ == "__main__":
    main()
