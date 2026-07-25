#!/usr/bin/env python3
"""
generate_forecaster_profiles.py
===============================
Generates permanent static Forecaster Profile pages for trackrecord.info.

Implements REQUIREMENTS_Forecaster_Profile_Surface.md (v1.0.0, 2026-07-24)

Key design decisions (Zero-Assumption Validation):
- ASS-PR-001: Uses author.firstname + " " + author.lastname (same as existing
  generate_homepage_scorecards.py / generate_prediction_tables.py) as the
  canonical display name and grouping key. The parallel "forecaster" field
  (Lastname, Firstname) is ignored for consistency with published scores.
  Validation: all current records have consistent author objects; no
  systematic fragmentation observed among the ~25 names.
- ASS-PR-002: Re-uses the exact scoring logic from generate_homepage_scorecards.py
  so NFR-PR-003 (cross-surface consistency) holds by construction.
- ASS-PR-003: statement_topic is present on all records and used as-is.
- ASS-PR-004: Emits pure static HTML under forecasters/{slug}.html + a small
  JSON search index. Compatible with existing GitHub Pages + Actions pattern.
- ASS-PR-005: Overall numeric score shown only when resolved_count >= 10
  (observed live homepage threshold). Topic scores require >= 5 (METHODOLOGY.md).
- ASS-PR-006: Stable permanent URLs /forecasters/{slug}.html required for Share.

Usage (from repo root):
  python3 scripts/generate_forecaster_profiles.py
  python3 scripts/generate_forecaster_profiles.py --dry-run --verbose
  python3 scripts/generate_forecaster_profiles.py --min-resolved 10

The script is intended to be called from the same GitHub Action that already
regenerates tables and detail pages, guaranteeing atomicity.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Constants (validated against live site + METHODOLOGY.md)
# ---------------------------------------------------------------------------
MIN_RESOLVED_FOR_OVERALL = 10          # homepage scorecards threshold
MIN_RESOLVED_FOR_TOPIC = 5             # METHODOLOGY.md
MAX_TOPICS_SHOWN = 7
MAX_PREDICTIONS_LIST = 8
OUTPUT_DIR = Path("forecasters")
SEARCH_INDEX_PATH = Path("forecasters_index.json")
PREDICTIONS_JSONL = Path("predictions_v2.jsonl")
METHODOLOGY_REF = "METHODOLOGY.md §4 (0–100 Accuracy Score) + scoring_rules.md v2.0"


# ---------------------------------------------------------------------------
# Name / slug helpers (pure, deterministic, reversible for audit)
# ---------------------------------------------------------------------------
def display_name_from_record(record: dict) -> str:
    """Canonical display name matching existing generators."""
    author = record.get("author") or {}
    first = (author.get("firstname") or "").strip()
    last = (author.get("lastname") or "").strip()
    name = f"{first} {last}".strip()
    if not name:
        # Fallback to the parallel field if author is missing
        name = (record.get("forecaster") or "Unknown").strip()
    return name


def slugify(name: str) -> str:
    """
    Deterministic URL-safe slug.
    "Chris Sutton" -> "chris-sutton"
    "Süleyman Öztürk" -> "suleyman-ozturk"
    """
    # Normalize unicode (ö -> o, etc.)
    nfkd = unicodedata.normalize("NFKD", name)
    ascii_name = "".join(c for c in nfkd if not unicodedata.combining(c))
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_name.lower()).strip("-")
    return slug or "unknown"


# ---------------------------------------------------------------------------
# Scoring (byte-identical logic to generate_homepage_scorecards.py)
# ---------------------------------------------------------------------------
def score_of_record(record: dict) -> Optional[float]:
    """Return 0–100 score for a resolved record, or None if pending."""
    if record.get("outcome") is None:
        return None
    weighted = (record.get("partial_accuracy") or {}).get("weighted_score")
    if weighted is not None:
        return float(weighted) * 100.0
    # Binary fallback
    return 100.0 if bool(record["outcome"]) else 0.0


def status_label(record: dict) -> Tuple[str, str, str]:
    """
    Return (label, badge_classes, card_bg_classes) for status.
    Vocabulary matches Prediction Detail + Visual System.
    Card backgrounds: green / amber / red for True / Pending / False.
    """
    outcome = record.get("outcome")
    if outcome is None:
        return "Pending", "bg-amber-500 text-white", "bg-amber-50"
    if float(outcome) >= 0.5:
        return "True", "bg-emerald-600 text-white", "bg-emerald-50"
    return "False", "bg-rose-600 text-white", "bg-rose-50"


def short_topic_label(topic: str) -> str:
    """Prefer a single concise word/phrase from the hierarchical topic."""
    if not topic:
        return "General"
    parts = [p.strip() for p in topic.split(" - ") if p.strip()]
    if not parts:
        return "General"
    last = parts[-1]
    # Collapse common multi-word endings to one preferred word where sensible
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


# Deterministic initials badge colour — excludes primary emerald / green
# so the badge never collides with the site accent (matches homepage spirit).
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
    """
    Return (initials, tailwind_bg_class).
    Same name always yields the same colour across the whole site.
    """
    parts = [p for p in name.replace(",", " ").split() if p]
    if len(parts) >= 2:
        initials = (parts[0][0] + parts[-1][0]).upper()
    elif parts:
        initials = parts[0][:2].upper()
    else:
        initials = "?"
    # Stable hash → palette index (avoid emerald/primary green)
    h = hashlib.md5(name.encode("utf-8")).hexdigest()
    idx = int(h[:8], 16) % len(_AVATAR_PALETTE)
    return initials, _AVATAR_PALETTE[idx]


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------
def load_and_aggregate(jsonl_path: Path) -> Dict[str, Any]:
    """
    Returns:
      {
        display_name: {
          "slug": str,
          "total": int,
          "resolved_count": int,
          "pending_count": int,
          "overall": float | None,          # None when below threshold
          "scores": list[float],            # for audit
          "topics": {topic: {"count": int, "avg": float | None}},
          "predictions": list[dict],        # sorted for the short list
          "statement_ids": list[str],
        }
      }
    """
    buckets: Dict[str, dict] = defaultdict(
        lambda: {
            "scores": [],
            "topics": defaultdict(list),
            "predictions": [],
            "statement_ids": [],
        }
    )

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

            sc = score_of_record(rec)
            raw_topic = (rec.get("statement_topic") or "General").strip()
            topic = short_topic_label(raw_topic)  # one-word / short pills
            sid = rec.get("statement_id") or ""

            buckets[name]["predictions"].append(rec)
            if sid:
                buckets[name]["statement_ids"].append(sid)

            if sc is not None:
                buckets[name]["scores"].append(sc)
                buckets[name]["topics"][topic].append(sc)

    result = {}
    for name, data in buckets.items():
        resolved = len(data["scores"])
        total = len(data["predictions"])
        pending = total - resolved

        overall = None
        if resolved >= MIN_RESOLVED_FOR_OVERALL and data["scores"]:
            overall = round(sum(data["scores"]) / len(data["scores"]), 1)
        elif resolved > 0:
            # Still compute for internal use / audit, but UI will hide it
            overall = round(sum(data["scores"]) / len(data["scores"]), 1)

        topic_stats = {}
        for t, scores in data["topics"].items():
            cnt = len(scores)
            avg = round(sum(scores) / cnt, 1) if cnt >= MIN_RESOLVED_FOR_TOPIC else None
            topic_stats[t] = {"count": cnt, "avg": avg}

        # Deterministic ordering of the prediction list (REQ-PR-004)
        # Resolved first (most recent resolution_date desc), then pending
        # (publication_date desc). AC-004: pending appear only after resolved.
        resolved_preds = [r for r in data["predictions"] if r.get("outcome") is not None]
        pending_preds = [r for r in data["predictions"] if r.get("outcome") is None]
        resolved_preds.sort(key=lambda r: r.get("resolution_date") or "", reverse=True)
        pending_preds.sort(key=lambda r: r.get("statement_publication_date") or "", reverse=True)
        preds_sorted = resolved_preds + pending_preds

        result[name] = {
            "slug": slugify(name),
            "total": total,
            "resolved_count": resolved,
            "pending_count": pending,
            "overall": overall,
            "scores": data["scores"],
            "topics": topic_stats,
            "predictions": preds_sorted[:MAX_PREDICTIONS_LIST],
            "statement_ids": sorted(data["statement_ids"]),
        }
    return result


# ---------------------------------------------------------------------------
# HTML rendering (matches Visual System + existing detail/homepage style)
# ---------------------------------------------------------------------------
def render_nav(relative_prefix: str = "../") -> str:
    return f"""
  <nav class="sticky top-0 z-50 bg-white/90 backdrop-blur border-b border-slate-100">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 h-14 flex items-center justify-between">
      <a href="{relative_prefix}index.html" class="flex items-center gap-x-2.5">
        <div class="w-7 h-7 bg-slate-900 rounded-lg"></div>
        <span class="text-lg font-normal tracking-tight text-slate-900">trackrecord.info</span>
      </a>
      <div class="hidden md:flex items-center gap-x-6 text-sm font-normal text-slate-600">
        <a href="{relative_prefix}predictions.html" class="hover:text-slate-900">Predictions</a>
        <a href="{relative_prefix}forecasters.html" class="hover:text-slate-900">Forecasters</a>
        <a href="https://github.com/TittaDiGirolamo/trackrecord.info/blob/main/METHODOLOGY.md" class="hover:text-slate-900" target="_blank" rel="noopener">Methodology</a>
      </div>
      <button id="mobile-menu-btn" class="md:hidden p-2 text-slate-600" aria-label="Open menu" aria-expanded="false">
        <i class="fa-solid fa-bars"></i>
      </button>
    </div>
    <div id="mobile-menu" class="hidden md:hidden border-t border-slate-100 bg-white">
      <div class="px-4 py-3 space-y-2 text-sm">
        <a href="{relative_prefix}predictions.html" class="block py-2 text-slate-700">Predictions</a>
        <a href="{relative_prefix}forecasters.html" class="block py-2 text-slate-700">Forecasters</a>
        <a href="https://github.com/TittaDiGirolamo/trackrecord.info/blob/main/METHODOLOGY.md" class="block py-2 text-slate-700" target="_blank" rel="noopener">Methodology</a>
      </div>
    </div>
  </nav>
"""


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

    # Score block (REQ-PR-002 + REQ-PR-008) — sits inside the light-grey main card
    # Note: resolved count is already shown in the counts row below, so we omit
    # the redundant "n = X resolved" line under the large score (matches homepage).
    if resolved < MIN_RESOLVED_FOR_OVERALL:
        score_html = f"""
        <div class="mt-4">
          <p class="text-2xl md:text-3xl font-medium text-slate-700 leading-snug">
            Insufficient resolved data (n = {resolved})
          </p>
          <p class="text-sm text-slate-500 mt-2">
            A numeric overall score is shown only when at least {MIN_RESOLVED_FOR_OVERALL} resolved predictions exist (same threshold used on the homepage).
          </p>
        </div>"""
        og_score = f"Insufficient data (n={resolved})"
    else:
        score_html = f"""
        <div class="mt-4">
          <p class="text-sm text-slate-500 mb-0.5">Score</p>
          <div class="flex items-baseline gap-x-2">
            <span class="text-5xl md:text-6xl font-medium text-slate-900 tabular-nums tracking-tight">{overall}</span>
            <span class="text-2xl text-slate-500">/100</span>
          </div>
        </div>"""
        og_score = f"{overall}/100 (n={resolved})"

    initials, avatar_bg = initials_and_color(name)
    # Placeholder bio — can later be driven from data if a bio field is added
    bio = "Public forecaster"

    # Topic breakdown (REQ-PR-003) — short one-word (or short-phrase) pills
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
                  <span class="tabular-nums text-emerald-700">{stats["avg"]}</span>
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
          <p class="text-xs text-slate-400 mt-3">Topics ordered by resolved count. Numeric score shown only when ≥{MIN_RESOLVED_FOR_TOPIC} resolved.</p>
        </section>"""
    else:
        topics_html = ""

    # Prediction short list (REQ-PR-004) — status-tinted card backgrounds
    pred_items = []
    for rec in data["predictions"]:
        label, badge_cls, card_bg = status_label(rec)
        stmt = rec.get("original_statement") or ""
        if len(stmt) > 140:
            stmt = stmt[:137] + "…"
        # Present as a quotation; outcome is already conveyed by the True/False/Pending pill
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
        <a href="../predictions.html?search={name.replace(' ', '%20')}" class="text-sm text-emerald-700 hover:text-emerald-800">
          See all predictions by this person →
        </a>
      </p>
    </section>"""

    # Open Graph / Twitter cards (REQ-PR-007)
    og_title = f"{name} — Forecaster Profile | trackrecord.info"
    og_desc = f"Accuracy {og_score}. {resolved} resolved of {total} tracked predictions."
    permanent_url = f"https://trackrecord.info/forecasters/{slug}.html"

    # Audit meta (NFR-PR-005)
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

  <!-- Open Graph -->
  <meta property="og:type" content="profile" />
  <meta property="og:url" content="{permanent_url}" />
  <meta property="og:title" content="{og_title}" />
  <meta property="og:description" content="{og_desc}" />
  <meta property="og:site_name" content="trackrecord.info" />

  <!-- Twitter Card -->
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
</head>
<body class="bg-white text-slate-900 antialiased">
  {render_nav("../")}

  <main class="max-w-3xl mx-auto px-4 sm:px-6 py-10 md:py-14">
    <!-- Back link -->
    <a href="../forecasters.html" class="inline-flex items-center gap-x-1.5 text-sm text-slate-500 hover:text-slate-800 mb-6">
      <i class="fa-solid fa-arrow-left text-xs"></i> All forecasters
    </a>

    <!-- Section title sits outside the card (matches homepage pattern) -->
    <p class="text-sm font-normal text-emerald-600 mb-3">Forecaster profile</p>

    <!-- Primary info in light-grey block (above the fold) -->
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

    <!-- Neutrality + audit footer (REQ-PR-008, NFR-PR-005) -->
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

  <script>
    // Mobile menu (same pattern as other pages)
    document.getElementById('mobile-menu-btn')?.addEventListener('click', function () {{
      const m = document.getElementById('mobile-menu');
      const open = !m.classList.contains('hidden');
      m.classList.toggle('hidden', open);
      this.setAttribute('aria-expanded', String(!open));
      this.querySelector('i').className = open ? 'fa-solid fa-bars' : 'fa-solid fa-xmark';
    }});
  </script>
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

    # Data hash for audit (NFR-PR-005)
    all_ids = sorted(sid for d in aggregates.values() for sid in d["statement_ids"])
    data_hash = hashlib.sha256("|".join(all_ids).encode()).hexdigest()

    args.output_dir.mkdir(parents=True, exist_ok=True)

    index: Dict[str, str] = {}  # display_name -> slug
    written = 0

    for name in sorted(aggregates.keys()):
        data = aggregates[name]
        slug = data["slug"]
        index[name] = slug

        html = render_profile_page(name, data, args.build_date, data_hash)
        out_path = args.output_dir / f"{slug}.html"

        if args.verbose or args.dry_run:
            score_disp = data["overall"] if data["resolved_count"] >= MIN_RESOLVED_FOR_OVERALL else f"insuff (n={data['resolved_count']})"
            print(f"  {name:30s}  slug={slug:25s}  score={score_disp}  resolved={data['resolved_count']}")

        if not args.dry_run:
            out_path.write_text(html, encoding="utf-8")
            written += 1

    # Search index (REQ-PR-005)
    index_payload = {
        "generated": args.build_date,
        "data_hash": data_hash,
        "forecasters": [
            {"name": n, "slug": s, "url": f"/forecasters/{s}.html"}
            for n, s in sorted(index.items())
        ],
    }
    if not args.dry_run:
        args.index_path.write_text(json.dumps(index_payload, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Wrote search index → {args.index_path}")

    print(f"{'Would write' if args.dry_run else 'Wrote'} {written} profile pages under {args.output_dir}/")
    print("Done.")


if __name__ == "__main__":
    main()
