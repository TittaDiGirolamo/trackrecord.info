#!/usr/bin/env python3
"""
generate_homepage_scorecards.py
Uses the single canonical pure-Brier function.
Primary display number = Brier Index (Higher is better).
"""

from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import argparse
import json
from collections import defaultdict
from datetime import date
from typing import Any, Dict, List, Tuple

from scoring import score_forecaster, format_index, LIMITATIONS_NOTE, display_name, slugify_name, initials_from_name


def calculate_forecaster_scores(jsonl_path: Path = Path("predictions_v2.jsonl")) -> Dict[str, Any]:
    buckets: Dict[str, list] = defaultdict(list)
    with open(jsonl_path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            name = (rec.get("forecaster") or "").strip()
            if not name:
                author = rec.get("author") or {}
                name = f"{author.get("firstname", "")} {author.get("lastname", "")}".strip()
            if not name:
                continue
            buckets[name].append(rec)

    result = {}
    for name, raw_preds in buckets.items():
        normalized = []
        for raw in raw_preds:
            normalized.append({
                "id": raw.get("statement_id") or raw.get("id"),
                "forecaster_id": name,
                "topic": raw.get("statement_topic") or "untagged",
                "probability": raw.get("statement_probability") if "statement_probability" in raw else raw.get("probability"),
                "outcome": raw.get("outcome"),
            })
        scored = score_forecaster(normalized)
        result[name] = {
            "overall": scored["overall"],
            "overall_index": scored.get("overall_index"),
            "resolved_count": scored["resolved_count"],
            "pending_count": scored["pending_count"],
            "prediction_ids": scored["prediction_ids"],
        }
    return result


def get_top_forecasters(scores: Dict[str, Any], n: int = 3, min_resolved: int = 2) -> List[Tuple[str, dict]]:
    qualified = [
        (name, data) for name, data in scores.items()
        if data["resolved_count"] >= min_resolved and data.get("overall_index") is not None
    ]
    qualified.sort(key=lambda x: (-(x[1]["overall_index"] or 0), -x[1]["resolved_count"]))
    return qualified[:n]


def render_homepage_scorecards(top_forecasters, build_date, n, min_resolved):
    if not top_forecasters:
        return f"""<div class="col-span-3 bg-white rounded-3xl p-10 text-center border border-slate-100">
    <h4 class="text-lg font-semibold">No forecasters qualify yet</h4>
    <p class="mt-2 text-sm text-slate-500">No forecasters with ≥{min_resolved} resolved predictions yet.</p>
</div>"""

    cards_html = ""
    # Palette matches profile pages (excludes site primary emerald)
    palette = ["blue", "violet", "rose", "amber", "indigo", "cyan", "fuchsia", "orange", "sky", "pink", "teal", "slate"]
    import hashlib
    for idx, (name, data) in enumerate(top_forecasters):
        shown_name = display_name(name)
        slug = slugify_name(name)
        initials = initials_from_name(name)
        h = hashlib.md5(name.encode("utf-8")).hexdigest()
        color = palette[int(h[:8], 16) % len(palette)]
        index_str = format_index(data.get("overall_index"))
        profile_url = f"forecasters/{slug}.html"

        cards_html += f"""
        <a href="{profile_url}" class="block bg-slate-100 rounded-3xl p-8 min-w-[280px] snap-center flex-shrink-0 md:min-w-0 hover:bg-slate-50 transition-colors" onclick="if(window.plausible){{plausible('figure_selected',{{props:{{figure:'{slug}'}}}})}}">
            <div class="flex items-center gap-x-4 mb-6">
                <div class="w-12 h-12 bg-{color}-600 rounded-2xl flex items-center justify-center text-white font-normal text-xl">{initials}</div>
                <div>
                    <div class="font-medium text-xl text-slate-900">{shown_name}</div>
                    <div class="text-sm text-slate-500">Public Forecaster</div>
                </div>
            </div>
            <div>
                <div class="text-sm text-slate-500">Brier Index</div>
                <div class="flex items-baseline gap-x-1">
                    <span class="text-6xl font-medium text-slate-900">{index_str}</span>
                    <span class="text-xl font-normal text-slate-900">/100</span>
                </div>
                <div class="text-sm text-emerald-600 mt-1">As of {build_date} · n = {data["resolved_count"]}</div>
            </div>
        </a>"""

    return f"""<div class="max-w-7xl mx-auto px-6 py-12 overflow-x-hidden">
    <div class="mb-8">
        <div class="text-sm font-normal text-emerald-600 mb-2">Live rankings</div>
        <h2 class="text-2xl md:text-3xl font-medium tracking-tight mb-6 text-slate-900">Top {n} Forecasters</h2>
        <p class="mt-2 text-slate-600">Based on all resolved predictions (minimum {min_resolved}). Higher Brier Index is better.</p>
        <p class="mt-1 text-xs text-slate-400">As of {build_date} · Pure mean Brier backend</p>
    </div>
    <div class="w-full max-w-full overflow-x-auto overscroll-x-contain pb-4 snap-x snap-mandatory md:overflow-visible md:pb-0">
      <div class="flex gap-6 md:grid md:grid-cols-3">
        {cards_html}
      </div>
    </div>
</div>"""


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
    parser.add_argument("--min-resolved", type=int, default=2)
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
