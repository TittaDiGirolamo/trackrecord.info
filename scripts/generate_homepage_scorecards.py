#!/usr/bin/env python3
"""
generate_homepage_scorecards.py
Part of Trackrecord.info automation.

Generates dynamic Top-N homepage forecaster scorecards partial (homepage_scorecards.html)
and optionally injects into index.html via placeholder markers.

Reuses/extends the forecaster scoring logic from generate_prediction_tables.py
for consistency with tiered partial-accuracy data in predictions_v2.jsonl.

This enables fully automatic updates via the existing GitHub Action on predictions.jsonl changes.

Methodological Notes (Zero-Assumption Validation):
- Forecaster identity: "{firstname} {lastname}" from "author" dict. Validated against samples and existing script.
- resolved_count: Number of predictions with 'outcome' is not None AND 'partial_accuracy.weighted_score' present.
- overall_score: round( mean(weighted_score * 100 for resolved), 1 )
- Filter: resolved_count >= MIN_RESOLVED (default 15)
- Sort: by overall_score DESC, then resolved_count DESC (tie-break)
- Only tiered match predictions contribute (other resolution types like binary winner use separate scoring per METHODOLOGY.md)
- If 0 qualify: honest empty state with explanation (no fabricated data)
- All reasoning, selection rule, and data source stated transparently in generated HTML (static text ok per req)
- No assumptions on future data volume; code handles gracefully as WC2026 resolutions progress.
- Configurable via CLI for N and MIN_RESOLVED to support experimentation without code changes.
"""

import json
import argparse
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Dict, List, Tuple, Any

# --- Core Scoring Logic (adapted from generate_prediction_tables.py:calculate_forecaster_scores for independence & auditability) ---
def calculate_forecaster_scores(jsonl_path: Path = Path("predictions_v2.jsonl")) -> Dict[str, Dict[str, Any]]:
    """
    Groups resolved predictions by forecaster and computes tiered overall_score + resolved_count.
    Only includes predictions that have partial_accuracy.weighted_score (i.e. tiered-scored match predictions).
    Returns: { "Forecaster Name": {"overall": float|0, "resolved_count": int, "raw_scores": list} , ... }
    """
    if not jsonl_path.exists():
        print(f"Warning: {jsonl_path} not found. Returning empty scores.")
        return {}

    forecasters: Dict[str, Dict[str, Any]] = defaultdict(lambda: {"overall_scores": [], "resolved_count": 0})

    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                print(f"Warning: Skipping invalid JSON at line {line_num}")
                continue

            author = record.get("author", {})
            firstname = author.get("firstname", "").strip()
            lastname = author.get("lastname", "").strip()
            if not firstname and not lastname:
                name = "Unknown Forecaster"
            else:
                name = f"{firstname} {lastname}".strip()

            outcome = record.get("outcome")
            partial = record.get("partial_accuracy", {})
            weighted_score = partial.get("weighted_score")

            if outcome is not None and weighted_score is not None:
                # Valid tiered resolved prediction
                forecasters[name]["overall_scores"].append(weighted_score * 100)
                forecasters[name]["resolved_count"] += 1  # or len(overall_scores) later

    # Compute aggregates
    result = {}
    for name, data in forecasters.items():
        scores = data["overall_scores"]
        if scores:
            avg = sum(scores) / len(scores)
            result[name] = {
                "overall": round(avg, 1),
                "resolved_count": len(scores),
                "raw_scores": scores  # for audit/debug if needed
            }
    return result


def get_top_forecasters(
    forecaster_scores: Dict[str, Dict[str, Any]],
    n: int = 3,
    min_resolved: int = 15
) -> List[Tuple[str, Dict[str, Any]]]:
    """
    Filter to those with resolved_count >= min_resolved, sort by overall DESC then resolved_count DESC, take top n.
    Returns list of (name, data_dict) tuples. Empty list if none qualify (honest handling).
    """
    qualified = [
        (name, data)
        for name, data in forecaster_scores.items()
        if data.get("resolved_count", 0) >= min_resolved
    ]
    if not qualified:
        return []
    qualified.sort(key=lambda item: (-item[1].get("overall", 0.0), -item[1].get("resolved_count", 0)))
    return qualified[:n]


def render_scorecard(name: str, data: Dict[str, Any], color: str, initials: str) -> str:
    """Render a single compact scorecard matching homepage visual language (Tailwind + rounded-3xl)."""
    score = data.get("overall", 0.0)
    n = data.get("resolved_count", 0)
    return f'''<div class="bg-white rounded-3xl p-8 flex flex-col border border-slate-100 hover:border-emerald-100 transition-colors">
    <div class="flex items-center gap-x-4 mb-6">
        <div class="w-12 h-12 bg-{color}-600 rounded-2xl flex-shrink-0 flex items-center justify-center text-white font-semibold text-xl tracking-tighter">{initials}</div>
        <div class="min-w-0">
            <div class="font-semibold text-xl tracking-tight">{name}</div>
            <div class="text-sm text-slate-500">Public Forecaster</div>
        </div>
    </div>

    <div class="mb-6">
        <div class="text-sm font-medium text-slate-500 mb-1">Score</div>
        <div class="flex items-baseline gap-x-2">
            <span class="text-6xl font-semibold tabular-nums tracking-tighter text-emerald-700">{score}</span>
            <span class="text-3xl text-emerald-600 font-medium">/100</span>
        </div>
        <div class="mt-1 text-sm text-slate-500">(n={n}) <span class="font-normal text-emerald-600">(tiered scoring)</span></div>
    </div>

    <div class="flex-1 text-xs text-slate-400 mb-6">
        Average of weighted tiered scores from resolved match predictions.<br>
        Exact = 100 • Winner + GD = 40 • Winner only = 20 (per scoring_rules.md v2.0)
    </div>

    <a href="forecasters.html"
       class="mt-auto inline-flex w-full items-center justify-center gap-x-2 rounded-2xl border border-emerald-200 px-5 py-3 text-sm font-medium text-emerald-700 transition-all hover:border-emerald-300 hover:text-emerald-800 active:scale-[0.985]">
        View full track record <i class="fa-solid fa-arrow-right text-xs"></i>
    </a>
</div>'''


def render_homepage_scorecards(
    top_forecasters: List[Tuple[str, Dict[str, Any]]],
    build_date: str,
    n: int,
    min_resolved: int
) -> str:
    """
    Returns clean, self-contained HTML partial for inclusion.
    Includes transparent selection rule, data source, and "See all" link.
    If no qualified forecasters: shows honest informational card (no data fabrication).
    """
    colors = ["emerald", "blue", "teal", "indigo", "amber"]

    if not top_forecasters:
        cards_html = f'''<div class="col-span-1 md:col-span-3 bg-white rounded-3xl p-10 text-center border border-slate-100">
    <div class="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-2xl bg-slate-100 text-slate-400">
        <i class="fa-solid fa-chart-line text-xl"></i>
    </div>
    <h4 class="text-lg font-semibold tracking-tight text-slate-700">No forecasters qualify yet</h4>
    <p class="mt-2 max-w-md mx-auto text-sm text-slate-500">
        Currently no forecasters have ≥{min_resolved} resolved match predictions with tiered partial-accuracy data in predictions_v2.jsonl.
        As more WC2026 group-stage and knockout matches resolve, this section will automatically populate with the highest-accuracy forecasters.
    </p>
    <p class="mt-4 text-xs text-slate-400">Selection rule is strict and transparent. Check back after resolutions (see resolution dates in predictions_v2.jsonl).</p>
</div>'''
    else:
        cards_list = []
        for idx, (name, data) in enumerate(top_forecasters):
            initials = "".join(word[0].upper() for word in name.split()[:2] if word)
            if not initials:
                initials = "??"
            color = colors[idx % len(colors)]
            cards_list.append(render_scorecard(name, data, color, initials))
        cards_html = "\n".join(cards_list)

    section = f'''<!-- Dynamic Top-N Homepage Forecaster Scorecards
     Generated: {build_date} | N={n} | MIN_RESOLVED={min_resolved}
     Source: predictions_v2.jsonl (tiered partial_accuracy.weighted_score)
     DO NOT EDIT MANUALLY — regenerated automatically by generate_homepage_scorecards.py / GitHub Action
-->
<div class="max-w-7xl mx-auto px-6 py-12">
    <div class="mb-8 flex flex-col md:flex-row md:items-end md:justify-between gap-y-4">
        <div>
            <div class="inline-flex items-center gap-x-2 rounded-full bg-emerald-50 px-3 py-1 text-xs font-medium text-emerald-700 mb-3">
                <i class="fa-solid fa-sync fa-fw"></i>
                LIVE • TIERED SCORING
            </div>
            <h3 class="text-3xl font-semibold tracking-tighter text-slate-900">Top {n} Forecasters by Accuracy</h3>
            <p class="mt-2 max-w-2xl text-slate-600">
                Highest tiered accuracy forecasters with at least {min_resolved} resolved predictions.
                Scores are the average of (weighted_score × 100) rounded to 1 decimal place.
            </p>
        </div>
        <a href="forecasters.html"
           class="inline-flex items-center gap-x-2 self-start rounded-2xl border border-emerald-200 px-4 py-2 text-sm font-medium text-emerald-700 transition hover:bg-emerald-50">
            See all forecasters <i class="fa-solid fa-arrow-right-long"></i>
        </a>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        {cards_html}
    </div>

    <div class="mt-8 text-center">
        <p class="text-xs text-slate-400 max-w-3xl mx-auto">
            <strong>Transparent selection rule:</strong> Top {n} by overall tiered score (descending), tie-broken by resolved_count (descending).
            Only predictions processed with scoring_version 2.0 partial_accuracy (match results: exact/winner+GD/winner-only tiers) contribute.
            Full methodology and all forecasters available on the <a href="forecasters.html" class="underline">forecasters page</a>.
            Auto-regenerated on every predictions.jsonl update via GitHub Actions. No manual curation.
        </p>
    </div>
</div>'''
    return section


def inject_into_index(index_path: Path, scorecards_html: str, marker_start: str = "<!-- HOMEPAGE_SCORECARDS_START -->", marker_end: str = "<!-- HOMEPAGE_SCORECARDS_END -->") -> bool:
    """
    Replaces content between markers in index.html with fresh scorecards_html.
    Returns True if successful. This enables zero future manual edits to index.html after initial placeholder insertion.
    """
    if not index_path.exists():
        print(f"Error: {index_path} does not exist.")
        return False

    content = index_path.read_text(encoding="utf-8")

    if marker_start not in content or marker_end not in content:
        print(f"Warning: Markers not found in {index_path}. Please insert the following once (one-time setup):\n"
              f"{marker_start}\n[old section content can go here or be removed]\n{marker_end}")
        return False

    before, _ = content.split(marker_start, 1)
    _, after = content.split(marker_end, 1)

    new_content = f"{before}{marker_start}\n{scorecards_html}\n{marker_end}{after}"

    index_path.write_text(new_content, encoding="utf-8")
    print(f"Action: Injected dynamic scorecards into {index_path}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Generate dynamic Top-N forecaster scorecards partial for trackrecord.info homepage from predictions_v2.jsonl tiered data."
    )
    parser.add_argument("--predictions-v2", type=Path, default=Path("predictions_v2.jsonl"),
                        help="Path to the scored predictions JSONL (default: predictions_v2.jsonl)")
    parser.add_argument("--n", "--top-n", type=int, default=3, dest="top_n",
                        help="Number of top forecasters to show (default: 3)")
    parser.add_argument("--min-resolved", type=int, default=15, dest="min_resolved",
                        help="Minimum resolved tiered predictions required to appear (default: 15)")
    parser.add_argument("--output", type=Path, default=Path("homepage_scorecards.html"),
                        help="Output file for the HTML partial (default: homepage_scorecards.html)")
    parser.add_argument("--index-html", type=Path, default=Path("index.html"),
                        help="Optional: index.html to inject into (requires markers)")
    parser.add_argument("--build-date", type=str, default=None,
                        help="Build date string (YYYY-MM-DD). Defaults to today.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Compute and print but do not write files (for validation)")

    args = parser.parse_args()

    build_date = args.build_date or date.today().isoformat()

    print(f"=== generate_homepage_scorecards.py | {build_date} ===")
    print(f"Config: N={args.top_n}, MIN_RESOLVED={args.min_resolved}, source={args.predictions_v2}")

    # 1. Calculate scores (reuses/extends existing logic for consistency)
    forecaster_scores = calculate_forecaster_scores(args.predictions_v2)

    # 2. Select top N qualified
    top_forecasters = get_top_forecasters(forecaster_scores, args.top_n, args.min_resolved)
    print(f"Qualified forecasters (>= {args.min_resolved} resolved): {len([k for k,v in forecaster_scores.items() if v['resolved_count'] >= args.min_resolved])}")
    print(f"Top {args.top_n} selected: {[name for name, _ in top_forecasters]}")

    # 3. Render partial
    scorecards_html = render_homepage_scorecards(top_forecasters, build_date, args.top_n, args.min_resolved)

    if args.dry_run:
        print("\n--- DRY RUN: Would write the following partial ---\n")
        print(scorecards_html[:2000] + "..." if len(scorecards_html) > 2000 else scorecards_html)
        print("\n--- End dry run ---")
        return

    # 4. Write the clean partial (include-able anywhere)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(scorecards_html, encoding="utf-8")
    print(f"Action: updated {args.output}")

    # 5. Optional: inject into index.html for full automation (zero future manual changes)
    if args.index_html != Path("index.html") or args.index_html.exists():  # always try if exists
        inject_into_index(args.index_html, scorecards_html)

    print("Done. Feature is now live on next GitHub Action run or manual execution.")


if __name__ == "__main__":
    main()
