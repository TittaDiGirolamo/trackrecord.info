#!/usr/bin/env python3
"""
generate_prediction_tables.py
Rebuilds predictions.html — predictions only, visual system compliant.
No forecaster score cards. Shared nav. Status-tinted cards.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import argparse
import json
from datetime import date
from typing import Any, Dict, List, Optional

from scoring import display_name
from templates.nav import render_nav, nav_script


def load_records(path: Path) -> List[Dict[str, Any]]:
    records = []
    if not path.exists():
        print(f"[ERROR] {path} not found")
        return records
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return records


def format_date(iso: Optional[str]) -> str:
    if not iso:
        return "—"
    try:
        d = date.fromisoformat(iso[:10])
        return d.strftime("%-d %B %Y")
    except Exception:
        return iso


def status_for(outcome) -> tuple[str, str, str]:
    """Returns (label, pill_classes, card_bg)."""
    base = "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-normal"
    if outcome is None:
        return "Pending", f"{base} bg-amber-500 text-white", "bg-amber-50"
    if float(outcome) >= 0.5:
        return "True", f"{base} bg-emerald-600 text-white", "bg-emerald-50"
    return "False", f"{base} bg-rose-600 text-white", "bg-rose-50"


def short_claim(text: str, limit: int = 120) -> str:
    text = (text or "").split("[")[0].strip()
    if len(text) > limit:
        return text[: limit - 1] + "…"
    return text


def render_cards(records: List[Dict[str, Any]]) -> str:
    # Newest resolution first, then newest publication
    def sort_key(r):
        return (
            r.get("resolution_date") or "9999-99-99",
            r.get("statement_publication_date") or "1900-01-01",
        )

    ordered = sorted(records, key=sort_key, reverse=True)
    cards = []
    for r in ordered:
        name = display_name(r.get("forecaster") or "")
        if not name or name == "Unknown":
            author = r.get("author") or {}
            name = display_name(
                f"{author.get('lastname', '')}, {author.get('firstname', '')}".strip(", ")
            )
        claim = short_claim(r.get("original_statement", ""))
        sid = r.get("statement_id") or ""
        href = f"predictions/{sid}.html" if sid else "#"
        pub = format_date(r.get("statement_publication_date"))
        label, pill, card_bg = status_for(r.get("outcome"))
        topic = (r.get("statement_topic") or "").split(" - ")[-1][:40]
        topic_html = ""
        if topic:
            topic_html = f'<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-normal bg-emerald-50 text-emerald-700">{topic}</span>'

        cards.append(
            f"""
        <a href="{href}" class="block {card_bg} rounded-2xl p-5 hover:opacity-90 transition-opacity">
          <div class="flex items-start justify-between gap-x-3 mb-2">
            <p class="font-normal text-slate-900 leading-relaxed flex-1">“{claim}”</p>
            <span class="{pill} shrink-0">{label}</span>
          </div>
          <div class="flex flex-wrap items-center gap-x-3 gap-y-1 text-sm text-slate-500">
            <span class="font-normal text-slate-600">{name}</span>
            <span class="font-mono">{pub}</span>
            {topic_html}
          </div>
        </a>"""
        )
    return "\n".join(cards) if cards else '<p class="text-slate-500">No predictions tracked yet.</p>'


def render_page(records: List[Dict[str, Any]], build_date: str) -> str:
    cards_html = render_cards(records)
    n = len(records)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Predictions | trackrecord.info</title>
  <meta name="description" content="Concrete tracked predictions drawn from the public record. Status is determined solely by primary evidence against pre-defined resolution criteria." />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&display=swap" rel="stylesheet" />
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" />
  <style>body {{ font-family: 'Inter', system-ui, sans-serif; }}</style>
</head>
<body class="bg-white text-slate-900 antialiased">
  {render_nav(active="predictions")}

  <main class="max-w-3xl mx-auto px-4 sm:px-6 py-10 md:py-14">
    <p class="text-sm font-normal text-emerald-600 mb-2">All tracked predictions</p>
    <h1 class="text-3xl md:text-4xl font-medium tracking-tight text-slate-900 mb-2">Predictions</h1>
    <p class="mt-2 text-slate-600 max-w-2xl mb-8">
      Concrete tracked predictions drawn from the public record. Status is determined solely by primary evidence against pre-defined resolution criteria.
    </p>
    <p class="text-sm text-slate-500 mb-6">{n} predictions</p>

    <div class="space-y-3">
      {cards_html}
    </div>

    <p class="text-xs text-slate-400 mt-10">Generated {build_date}.</p>
  </main>

  {nav_script()}
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--predictions-jsonl", type=Path, default=Path("predictions_v2.jsonl"))
    parser.add_argument("--output", type=Path, default=Path("predictions.html"))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    records = load_records(args.predictions_jsonl)
    print(f"Loaded {len(records)} records from {args.predictions_jsonl}")
    html = render_page(records, date.today().isoformat())

    if args.dry_run:
        print(html[:500])
    else:
        args.output.write_text(html, encoding="utf-8")
        print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
