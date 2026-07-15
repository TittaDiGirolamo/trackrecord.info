#!/usr/bin/env python3
"""
generate_homepage_scorecards.py - Hybrid version with injection
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
    qualified = [(name, data) for name, data in scores.items() 
                 if data["resolved_count"] >= min_resolved]
    if not qualified:
        return []
    qualified.sort(key=lambda x: (-x[1]["overall"], -x[1]["resolved_count"]))
    return qualified[:n]


def render_homepage_scorecards(top_forecasters, build_date, n, min_resolved):
    if not top_forecasters:
        return f'''<div class="col-span-3 bg-white rounded-3xl p-10 text-center border border-slate-100">
    <h4 class="text-lg font-semibold">No forecasters qualify yet</h4>
    <p class="mt-2 text-sm text-slate-500">No forecasters with ≥{min_resolved} resolved predictions yet.</p>
</div>'''

    cards_html = ""
    colors = ["emerald", "blue", "teal"]
    for idx, (name, data) in enumerate(top_forecasters):
        initials = "".join([w[0].upper() for w in name.split()[:2]]) or "??"
        color = colors[idx % len(colors)]
        cards_html += f'''
        <div class="bg-white rounded-3xl p-8 border border-slate-100">
            <div class="flex items-center gap-x-4 mb-6">
                <div class="w-12 h-12 bg-{color}-600 rounded-2xl flex items-center justify-center text-white font-semibold text-xl">{initials}</div>
                <div>
                    <div class="font-semibold text-xl">{name}</div>
                    <div class="text-sm text-slate-500">Public Forecaster</div>
                </div>
            </div>
            <div>
                <div class="text-sm text-slate-500">Score</div>
                <div class="flex items-baseline gap-x-2">
                    <span class="text-6xl font-semibold text-emerald-700">{data["overall"]}</span>
                    <span class="text-3xl text-emerald-600">/100</span>
                </div>
                <div class="text-sm text-slate-500 mt-1">(n={data["resolved_count"]})</div>
            </div>
        </div>'''

    return f'''<div class="max-w-7xl mx-auto px-6 py-12">
    <div class="mb-8">
        <div class="inline-flex items-center gap-x-2 rounded-full bg-emerald-50 px-3 py-1 text-xs font-medium text-emerald-700 mb-3">
            LIVE
        </div>
        <h3 class="text-3xl font-semibold tracking-tighter">Top {n} Forecasters by Accuracy</h3>
        <p class="mt-2 text-slate-600">Based on all resolved predictions (minimum {min_resolved}).</p>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        {cards_html}
    </div>
</div>'''


def inject_into_index(index_path, scorecards_html):
    if not index_path.exists():
        return False
    content = index_path.read_text(encoding="utf-8")
    if "<!-- HOMEPAGE_SCORECARDS_START -->" not in content:
        return False

    before, rest = content.split("<!-- HOMEPAGE_SCORECARDS_START -->", 1)
    if "<!-- HOMEPAGE_SCORECARDS_END -->" not in rest:
        return False
    _, after = rest.split("<!-- HOMEPAGE_SCORECARDS_END -->", 1)

    new_content = before + "<!-- HOMEPAGE_SCORECARDS_START -->\n" + scorecards_html + "\n<!-- HOMEPAGE_SCORECARDS_END -->" + after
    index_path.write_text(new_content, encoding="utf-8")
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-resolved", type=int, default=10)
    parser.add_argument("--n", type=int, default=3)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    scores = calculate_forecaster_scores()
    top = get_top_forecasters(scores, args.n, args.min_resolved)

    html = render_homepage_scorecards(top, date.today().isoformat(), args.n, args.min_resolved)

    if args.dry_run:
        print(html)
    else:
        Path("homepage_scorecards.html").write_text(html, encoding="utf-8")
        success = inject_into_index(Path("index.html"), html)
        if success:
            print("✅ homepage_scorecards.html updated and injected into index.html!")
        else:
            print("✅ homepage_scorecards.html updated (injection failed)")


if __name__ == "__main__":
    main()
