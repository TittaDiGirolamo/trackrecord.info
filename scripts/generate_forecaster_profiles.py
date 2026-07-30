#!/usr/bin/env python3
"""
generate_forecaster_profiles.py
===============================
Generates permanent static Forecaster Profile pages for trackrecord.info.

Implements REQUIREMENTS_Forecaster_Profile_Surface.md (v1.0.0, 2026-07-24)

Usage (from repo root):
  python3 scripts/generate_forecaster_profiles.py
  python3 scripts/generate_forecaster_profiles.py --dry-run --verbose
"""

from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import argparse
import hashlib
import json
import re
import unicodedata
from scoring import score_forecaster, format_brier, format_index, LIMITATIONS_NOTE, RULES_VERSION
from templates.nav import render_nav, nav_script
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
MIN_RESOLVED_FOR_OVERALL = 1
MIN_RESOLVED_FOR_TOPIC = 1
MAX_TOPICS_SHOWN = 7
MAX_PREDICTIONS_LIST = 10_000  # show all on profile
OUTPUT_DIR = Path("forecasters")
SEARCH_INDEX_PATH = Path("forecasters_index.json")
PREDICTIONS_JSONL = Path("predictions_v2.jsonl")
METHODOLOGY_REF = "SCORING.md (pure mean Brier is the source of truth; Brier Index is shown as the primary display number)"


# ---------------------------------------------------------------------------
# Name / slug helpers
# ---------------------------------------------------------------------------
def display_name_from_record(record: dict) -> str:
    author = record.get("author") or {}
    first = (author.get("firstname") or "").strip()
    last = (author.get("lastname") or "").strip()
    name = f"{first} {last}".strip()
    if not name:
        name = (record.get("forecaster") or "Unknown").strip()
    return name


def slugify(name: str) -> str:
    nfkd = unicodedata.normalize("NFKD", name)
    ascii_name = "".join(c for c in nfkd if not unicodedata.combining(c))
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_name.lower()).strip("-")
    return slug or "unknown"


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def status_label(record: dict) -> Tuple[str, str, str]:
    outcome = record.get("outcome")
    if outcome is None:
        return "Pending", "bg-amber-500 text-white", "bg-amber-50"
    if float(outcome) >= 0.5:
        return "True", "bg-emerald-600 text-white", "bg-emerald-50"
    return "False", "bg-rose-600 text-white", "bg-rose-50"


def short_topic_label(topic: str) -> str:
    if not topic:
        return "General"
    parts = [p.strip() for p in topic.split(" - ") if p.strip()]
    if not parts:
        return "General"
    last = parts[-1]
    mapping = {
        "Group Stage": "Group",
        "Knockout Stages": "Knockout",
        "Last 16": "R16",
        "Round of 16": "R16",
        "Quarterfinals": "Quarters",
        "Semifinals": "Semis",
        "Final": "Final",
        "Winner": "Winner",
    }
    return mapping.get(last, last.split()[0] if " " in last and len(last) > 14 else last)


_AVATAR_PALETTE = [
    "bg-blue-600",
    "bg-violet-600",
    "bg-rose-600",
    "bg-amber-600",
    "bg-indigo-600",
    "bg-cyan-600",
    "bg-fuchsia-600",
    "bg-orange-600",
    "bg-sky-600",
    "bg-pink-600",
    "bg-teal-700",
    "bg-slate-600",
]


def initials_and_color(name: str) -> Tuple[str, str]:
    parts = [p for p in name.replace(",", " ").split() if p]
    if len(parts) >= 2:
        initials = (parts[0][0] + parts[-1][0]).upper()
    elif parts:
        initials = parts[0][:2].upper()
    else:
        initials = "?"
    h = hashlib.md5(name.encode("utf-8")).hexdigest()
    idx = int(h[:8], 16) % len(_AVATAR_PALETTE)
    return initials, _AVATAR_PALETTE[idx]


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------
def load_and_aggregate(jsonl_path: Path) -> Dict[str, Any]:
    """
    Load predictions_v2.jsonl and score every forecaster with the
    single canonical pure-Brier function. No divergent logic allowed.
    """
    from collections import defaultdict

    # Group raw records by display name
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
            name = display_name_from_record(rec)
            if not name or name == "Unknown":
                continue
            buckets[name].append(rec)

    result = {}
    for name, raw_preds in buckets.items():
        # Normalize to the shape expected by the canonical scorer
        normalized = []
        for raw in raw_preds:
            normalized.append({
                "id": raw.get("statement_id") or raw.get("id"),
                "forecaster_id": name,
                "topic": raw.get("statement_topic") or "untagged",
                "probability": raw.get("statement_probability") if "statement_probability" in raw else raw.get("probability"),
                "outcome": raw.get("outcome"),
            })

        # THE only place scores are calculated
        scored = score_forecaster(normalized)

        # Keep a short list of recent predictions for the profile page
        resolved_preds = [r for r in raw_preds if r.get("outcome") is not None]
        pending_preds = [r for r in raw_preds if r.get("outcome") is None]
        resolved_preds.sort(key=lambda r: r.get("resolution_date") or "", reverse=True)
        pending_preds.sort(key=lambda r: r.get("statement_publication_date") or "", reverse=True)
        preds_sorted = resolved_preds + pending_preds

        # Topic stats in the shape the HTML expects
        topic_stats = {}
        for t, tdata in scored["topics"].items():
            topic_stats[t] = {
            "count": tdata["resolved_count"],
            "avg": tdata["score"],
            "index": tdata.get("index"),
        }

        result[name] = {
            "slug": slugify(name),
            "total": scored["resolved_count"] + scored["pending_count"],
            "resolved_count": scored["resolved_count"],
            "pending_count": scored["pending_count"],
            "overall": scored["overall"],
            "overall_index": scored.get("overall_index"),
            "prediction_ids": scored["prediction_ids"],
            "topics": topic_stats,
            "predictions": preds_sorted[:MAX_PREDICTIONS_LIST],
            "statement_ids": sorted(
                [str(p.get("statement_id") or p.get("id") or "") for p in raw_preds if p.get("statement_id") or p.get("id")]
            ),
            "limitations_note": LIMITATIONS_NOTE,
            "rules_version": RULES_VERSION,
        }
    return result

# ---------------------------------------------------------------------------
# HTML
# ---------------------------------------------------------------------------

def render_profile_page(
    name: str,
    data: dict,
    build_date: str,
    data_hash: str,
) -> str:
    slug = data["slug"]
    resolved = data["resolved_count"]
    total = data["total"]
    pending = data["pending_count"]
    overall = data["overall"]
    overall_index = data.get("overall_index")

    if overall is None or resolved == 0:
        score_html = f"""
        <div class="mt-4">
          <p class="text-2xl md:text-3xl font-medium text-slate-700 leading-snug">
            No resolved predictions yet
          </p>
          <p class="text-sm text-slate-500 mt-2">
            Scores appear once at least one prediction has been resolved.
          </p>
        </div>"""
        og_score = f"No resolved data (n={resolved})"
    else:
        index_str = format_index(overall_index)
        brier_str = format_brier(overall)
        score_html = f"""
        <div class="mt-4">
          <div class="flex items-baseline gap-x-2">
            <span class="text-5xl md:text-6xl font-medium text-slate-900 tabular-nums tracking-tight">{index_str}</span>
          </div>
          <p class="text-sm text-slate-500 mt-1">
            Brier Index · 0–100 · higher is better · n = {resolved}
          </p>
          <p class="text-xs text-slate-400 mt-1">
            Raw Brier: {brier_str} (lower is better)
          </p>
          <p class="text-xs text-slate-400 mt-2 max-w-md">
            {LIMITATIONS_NOTE}
          </p>
        </div>"""
        og_score = f"{index_str} (n={resolved})"
    
    initials, avatar_bg = initials_and_color(name)
    bio = "Public forecaster"

    topics_sorted = sorted(
        data["topics"].items(),
        key=lambda kv: (-kv[1]["count"], kv[0]),
    )[:MAX_TOPICS_SHOWN]

    if topics_sorted:
        topic_pills = []
        for t, stats in topics_sorted:
            short = short_topic_label(t)
            if stats["avg"] is not None:
                pill = f"""
                <div class="inline-flex items-center gap-x-2 px-3 py-1.5 rounded-full bg-emerald-50 text-emerald-800 text-sm">
                  <span class="font-medium">{short}</span>
                  <span class="tabular-nums text-emerald-700">{format_index(stats.get("index"))}</span>
                  <span class="text-emerald-500 text-xs">({stats["count"]})</span>
                </div>"""
            else:
                pill = f"""
                <div class="inline-flex items-center gap-x-2 px-3 py-1.5 rounded-full bg-slate-100 text-slate-600 text-sm">
                  <span class="font-medium">{short}</span>
                  <span class="text-slate-400 text-xs">{stats["count"]}</span>
                </div>"""
            topic_pills.append(pill)
        topics_html = f"""
        <section class="mt-10">
          <h2 class="text-sm font-normal text-emerald-600 mb-3">Topic breakdown</h2>
          <div class="flex flex-wrap gap-2">
            {''.join(topic_pills)}
          </div>
	    <p class="text-xs text-slate-400 mt-3">Topics ordered by resolved count. Numbers are Brier Index (0–100, higher is better), same scale as the main score.</p>
        </section>"""
    else:
        topics_html = ""

    pred_items = []
    for rec in data["predictions"]:
        label, badge_cls, card_bg = status_label(rec)
        stmt = rec.get("original_statement") or ""
        if len(stmt) > 140:
            stmt = stmt[:137] + "…"
        quoted = f"“{stmt}”"
        pub = rec.get("statement_publication_date") or "—"
        sid = rec.get("statement_id") or ""
        link = f"../predictions/{sid}.html" if sid else "#"
        pred_items.append(f"""
        <a href="{link}" class="block p-4 rounded-xl {card_bg} hover:opacity-90 transition-opacity">
          <div class="flex items-start justify-between gap-x-3">
            <p class="text-sm font-normal text-slate-800 leading-relaxed flex-1">{quoted}</p>
            <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-normal shrink-0 {badge_cls}">{label}</span>
          </div>
          <div class="mt-1.5 text-xs text-slate-500">
            <span>{pub}</span>
          </div>
        </a>""")

    selection_note = (
        "Ordered by resolution date (most recent first), then publication date. "
        "Limit 8. No editorial ranking applied."
    )

    predictions_html = f"""
    <section class="mt-10">
      <h2 class="text-sm font-normal text-emerald-600 mb-3">Recent predictions</h2>
      <div class="space-y-3">
        {''.join(pred_items) if pred_items else '<p class="py-6 text-sm text-slate-500">No predictions recorded.</p>'}
      </div>
      <p class="text-xs text-slate-400 mt-3">{selection_note}</p>
      <p class="mt-4">

      </p>
    </section>"""

    og_title = f"{name} — Forecaster Profile | trackrecord.info"
    og_desc = f"Accuracy {og_score}. {resolved} resolved of {total} tracked predictions."
    permanent_url = f"https://trackrecord.info/forecasters/{slug}.html"

    audit_comment = (
        f"<!-- PROFILE_AUDIT "
        f"generated={build_date} "
        f"data_hash={data_hash} "
        f"statement_ids={','.join(data['statement_ids'][:20])}{'...' if len(data['statement_ids'])>20 else ''} "
        f"threshold_overall={MIN_RESOLVED_FOR_OVERALL} "
        f"threshold_topic={MIN_RESOLVED_FOR_TOPIC} "
        f"scoring={METHODOLOGY_REF} "
        f"-->"
    )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{name} — Forecaster Profile | trackrecord.info</title>
  <meta name="description" content="{og_desc}" />
  <link rel="canonical" href="{permanent_url}" />

  <meta property="og:type" content="profile" />
  <meta property="og:url" content="{permanent_url}" />
  <meta property="og:title" content="{og_title}" />
  <meta property="og:description" content="{og_desc}" />
  <meta property="og:site_name" content="trackrecord.info" />

  <meta name="twitter:card" content="summary" />
  <meta name="twitter:title" content="{og_title}" />
  <meta name="twitter:description" content="{og_desc}" />

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&display=swap" rel="stylesheet" />
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" />
  <style>
    body {{ font-family: 'Inter', system-ui, sans-serif; }}
  </style>
  {audit_comment}
  <!-- Privacy-friendly analytics by Plausible -->
  <script async src="https://plausible.io/js/pa-MQu87Y2WzO-sB_YzB2L-N.js"></script>
  <script>
    window.plausible=window.plausible||function(){(plausible.q=plausible.q||[]).push(arguments)},plausible.init=plausible.init||function(i){plausible.o=i||{}};
    plausible.init()
  </script>
</head>
<body class="bg-white text-slate-900 antialiased">
  {render_nav(active="", relative_prefix="../")}

  <main class="max-w-3xl mx-auto px-4 sm:px-6 py-10 md:py-14">

    <p class="text-sm font-normal text-emerald-600 mb-3">Forecaster profile</p>

    <header class="bg-slate-100 rounded-2xl p-6 md:p-8">
      <div class="flex items-center gap-x-4">
        <div class="w-12 h-12 {avatar_bg} rounded-2xl flex items-center justify-center text-white font-medium text-lg shrink-0">{initials}</div>
        <div>
          <h1 class="text-2xl md:text-3xl font-medium tracking-tight text-slate-900">{name}</h1>
          <p class="text-sm text-slate-500 mt-0.5">{bio}</p>
        </div>
      </div>
      {score_html}

      <div class="mt-6 flex flex-wrap gap-x-6 gap-y-2 text-sm text-slate-600">
        <div><span class="text-slate-400">Tracked</span> <span class="tabular-nums font-medium text-slate-800">{total}</span></div>
        <div><span class="text-slate-400">Resolved</span> <span class="tabular-nums font-medium text-slate-800">{resolved}</span></div>
        <div><span class="text-slate-400">Pending</span> <span class="tabular-nums font-medium text-slate-800">{pending}</span></div>
      </div>
    </header>

    {topics_html}
    {predictions_html}

    <footer class="mt-16 pt-8 border-t border-slate-200">
      <p class="text-xs text-slate-400 leading-relaxed">
        Score calculated per {METHODOLOGY_REF}. Pending predictions are excluded from accuracy.
        No relative ranking, percentile, or editorial framing is applied.
        Generated {build_date}. Data hash: <code class="font-mono">{data_hash[:12]}…</code>.
        Permanent URL: <a href="{permanent_url}" class="text-emerald-700 hover:underline">{permanent_url}</a>
      </p>
      <p class="text-xs text-slate-400 mt-3">
        <button onclick="navigator.clipboard.writeText('{permanent_url}'); this.textContent='Copied';"
                class="text-emerald-700 hover:text-emerald-800 underline-offset-2 hover:underline">
          Copy permanent link
        </button>
      </p>
    </footer>
  </main>

  {nav_script()}
</body>
</html>
"""
    return html


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description="Generate static Forecaster Profile pages")
    parser.add_argument("--predictions-jsonl", type=Path, default=PREDICTIONS_JSONL)
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    parser.add_argument("--index-path", type=Path, default=SEARCH_INDEX_PATH)
    parser.add_argument("--build-date", type=str, default=date.today().isoformat())
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    if not args.predictions_jsonl.exists():
        raise SystemExit(f"Input not found: {args.predictions_jsonl}")

    print(f"Loading {args.predictions_jsonl} …")
    aggregates = load_and_aggregate(args.predictions_jsonl)
    print(f"  Found {len(aggregates)} distinct forecasters")

    all_ids = sorted(sid for d in aggregates.values() for sid in d["statement_ids"])
    data_hash = hashlib.sha256("|".join(all_ids).encode()).hexdigest()

    args.output_dir.mkdir(parents=True, exist_ok=True)

    index: Dict[str, str] = {}
    written = 0

    for name in sorted(aggregates.keys()):
        data = aggregates[name]
        slug = data["slug"]
        index[name] = slug

        html = render_profile_page(name, data, args.build_date, data_hash)
        out_path = args.output_dir / f"{slug}.html"

        if args.verbose or args.dry_run:
            score_disp = (
                data["overall"]
                if data["resolved_count"] >= MIN_RESOLVED_FOR_OVERALL
                else f"insuff (n={data['resolved_count']})"
            )
            print(f"  {name:30s}  slug={slug:25s}  score={score_disp}  resolved={data['resolved_count']}")

        if not args.dry_run:
            out_path.write_text(html, encoding="utf-8")
            written += 1

    index_payload = {
        "generated": args.build_date,
        "data_hash": data_hash,
        "forecasters": [
            {"name": n, "slug": s, "url": f"/forecasters/{s}.html"}
            for n, s in sorted(index.items())
        ],
    }
    if not args.dry_run:
        args.index_path.write_text(
            json.dumps(index_payload, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        print(f"Wrote search index → {args.index_path}")

    print(f"{'Would write' if args.dry_run else 'Wrote'} {written} profile pages under {args.output_dir}/")
    print("Done.")


if __name__ == "__main__":
    main()
