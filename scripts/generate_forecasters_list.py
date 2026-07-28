#!/usr/bin/env python3
"""
generate_forecasters_list.py
Rebuilds forecasters.html from predictions_v2.jsonl using the
single canonical pure-Brier function. Primary number = Brier Index.
"""

from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import json
from collections import defaultdict
from datetime import date
from typing import Any, Dict

from scoring import score_forecaster, format_index


def load_and_score(jsonl_path: Path = Path("predictions_v2.jsonl")) -> Dict[str, Any]:
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
                name = f"{author.get('firstname', '')} {author.get('lastname', '')}".strip()
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
        # First-Last slug
        parts = [p for p in name.replace(",", " ").split() if p]
        if len(parts) >= 2:
            slug = f"{parts[-1].lower()}-{parts[0].lower()}"
            initials = (parts[-1][0] + parts[0][0]).upper()
        else:
            slug = name.lower().replace(" ", "-")
            initials = (parts[0][:2] if parts else "??").upper()

        result[name] = {
            "slug": slug,
            "initials": initials,
            "overall": scored["overall"],
            "overall_index": scored.get("overall_index"),
            "resolved_count": scored["resolved_count"],
            "pending_count": scored["pending_count"],
        }
    return result


def render_page(scores: Dict[str, Any], build_date: str) -> str:
    # Sort by Index descending (higher is better)
    ordered = sorted(
        scores.items(),
        key=lambda x: (-(x[1].get("overall_index") or 0), -x[1]["resolved_count"]),
    )

    cards = []
    colors = ["emerald", "blue", "violet", "rose", "amber", "indigo", "cyan", "fuchsia", "orange", "sky"]
    for idx, (name, data) in enumerate(ordered):
        color = colors[idx % len(colors)]
        index_str = format_index(data.get("overall_index"))
        n = data["resolved_count"]
        if data.get("overall_index") is None or n == 0:
            score_block = f'''
            <div class="mb-1"><span class="text-base font-medium text-slate-600">No resolved predictions</span></div>
            <div class="text-sm text-slate-500">0 resolved</div>'''
        else:
            score_block = f'''
            <div class="mb-1"><span class="text-3xl font-medium text-slate-900 tabular-nums">{index_str}</span></div>
            <div class="text-sm text-emerald-600">Brier Index · higher is better</div>
            <div class="text-sm text-slate-500">n = {n}</div>'''

        cards.append(f'''
        <a href="forecasters/{data["slug"]}.html" class="block bg-slate-100 rounded-2xl p-5 hover:bg-slate-50 transition-colors">
          <div class="flex items-center gap-x-3 mb-3">
            <div class="w-10 h-10 bg-{color}-600 rounded-xl flex items-center justify-center text-white font-normal text-sm">{data["initials"]}</div>
            <div>
              <div class="font-medium text-slate-900">{name}</div>
              <div class="text-sm text-slate-500">Public forecaster</div>
            </div>
          </div>
          {score_block}
        </a>''')

    cards_html = "\n".join(cards)

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Forecasters | trackrecord.info</title>
  <meta name="description" content="Track record of public forecasters. Scores are Brier Index (higher is better)." />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&display=swap" rel="stylesheet" />
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" />
  <style>body {{ font-family: 'Inter', system-ui, sans-serif; }}</style>
</head>
<body class="bg-white text-slate-900 antialiased">
  <nav id="main-nav" class="bg-white sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-6">
      <div class="flex items-center justify-between h-16 md:h-20">
        <div class="flex items-center gap-x-2.5">
          <div class="w-7 h-7 bg-slate-900 rounded-lg flex items-center justify-center flex-shrink-0">
            <span class="text-white text-sm font-normal tracking-tight">T</span>
          </div>
          <a href="index.html" class="text-lg font-normal tracking-tight text-slate-900">Trackrecord.info</a>
        </div>
        <div class="hidden md:flex items-center gap-x-8 text-sm">
          <a href="predictions.html" class="font-normal text-slate-600 hover:text-slate-900 transition-colors">Predictions</a>
          <a href="forecasters.html" class="font-normal text-slate-900">Forecasters</a>
          <a href="https://github.com/TittaDiGirolamo/trackrecord.info/blob/main/METHODOLOGY.md" class="font-normal text-slate-600 hover:text-slate-900 transition-colors">Methodology</a>
        </div>
        <div class="flex items-center gap-x-3">
          <a href="https://x.com/titta_girolamo" class="hidden sm:flex items-center gap-x-2 px-4 py-2 text-sm font-normal text-slate-700 hover:text-slate-900 transition-colors">
            <i class="fa-brands fa-x-twitter"></i><span>Follow</span>
          </a>
          <button id="mobile-menu-btn" class="md:hidden p-2 text-slate-700" aria-label="Toggle menu">
            <i class="fa-solid fa-bars text-2xl"></i>
          </button>
        </div>
      </div>
      <div id="mobile-menu" class="hidden md:hidden py-4">
        <div class="flex flex-col gap-y-4 text-sm">
          <a href="predictions.html" class="font-normal text-slate-600 px-2 py-1">Predictions</a>
          <a href="forecasters.html" class="font-normal text-slate-900 px-2 py-1">Forecasters</a>
          <a href="https://github.com/TittaDiGirolamo/trackrecord.info/blob/main/METHODOLOGY.md" class="font-normal text-slate-600 px-2 py-1">Methodology</a>
        </div>
      </div>
    </div>
  </nav>

  <main class="max-w-3xl mx-auto px-4 sm:px-6 py-10 md:py-14">
    <p class="text-sm font-normal text-emerald-600 mb-2">All tracked forecasters</p>
    <h1 class="text-3xl md:text-4xl font-medium tracking-tight text-slate-900 mb-2">Forecasters</h1>
    <p class="text-slate-600 mb-8">Primary score is the Brier Index (0–100, higher is better). Pure mean Brier remains the source of truth.</p>

    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
      {cards_html}
    </div>

    <p class="text-xs text-slate-400 mt-10">Generated {build_date}. Scores from the canonical pure-Brier function.</p>
  </main>

  <script>
    document.getElementById('mobile-menu-btn')?.addEventListener('click', function () {{
      const m = document.getElementById('mobile-menu');
      m.classList.toggle('hidden');
    }});
  </script>
</body>
</html>
'''


def main() -> None:
    scores = load_and_score()
    html = render_page(scores, date.today().isoformat())
    Path("forecasters.html").write_text(html, encoding="utf-8")
    print(f"Wrote forecasters.html with {len(scores)} forecasters")


if __name__ == "__main__":
    main()
