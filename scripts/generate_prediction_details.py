#!/usr/bin/env python3
"""
Trackrecord Prediction Detail Page Generator

Generates permanent static detail pages for each resolved prediction:
  predictions/{statement_id}.html

Visual language locked to the current homepage (index.html).
Claim is the central element; section headings match the
"High-visibility predictions" eyebrow style.

Satisfies REQ-PD-001 … REQ-PD-008.

Usage:
  python3 scripts/generate_prediction_details.py
  python3 scripts/generate_prediction_details.py --dry-run --verbose
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path as _Path
sys.path.insert(0, str(_Path(__file__).resolve().parent.parent))
from scoring import brier_to_index, format_brier, format_index
from scoring.rules import score_one
from templates.nav import render_nav, nav_script
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

DEFAULT_JSONL = Path("predictions_v2.jsonl")
DEFAULT_OUT_DIR = Path("predictions")
DEFAULT_RESOLVED_DETAILS = Path("resolved_details.jsonl")


def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    records = []
    if not path.exists():
        print(f"[ERROR] {path} not found")
        return records
    with path.open(encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"[WARNING] Line {i}: invalid JSON – {e}")
    return records


def load_resolved_details(path: Path) -> Dict[str, Dict[str, Any]]:
    details: Dict[str, Dict[str, Any]] = {}
    if not path.exists():
        return details
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
                sid = rec.get("statement_id")
                if sid:
                    details[sid] = rec
            except json.JSONDecodeError:
                continue
    return details


def get_predictor_display_name(rec: Dict[str, Any]) -> str:
    """Firstname Lastname for the title form."""
    author = rec.get("author") or {}
    first = (author.get("firstname") or "").strip()
    last = (author.get("lastname") or "").strip()
    if first or last:
        return f"{first} {last}".strip()

    forecaster = (rec.get("forecaster") or "").strip()
    if "," in forecaster:
        parts = [p.strip() for p in forecaster.split(",", 1)]
        if len(parts) == 2:
            return f"{parts[1]} {parts[0]}".strip()
    return forecaster or "Unknown"


def format_date(iso: Optional[str]) -> str:
    """Day Month Year, e.g. '6 December 2025'."""
    if not iso:
        return "—"
    try:
        d = datetime.strptime(iso[:10], "%Y-%m-%d")
        return d.strftime("%-d %B %Y")
    except Exception:
        return iso


def outcome_pill(outcome: Optional[float]) -> Tuple[str, str, str]:
    """Clear solid status pills + matching light card background.
    Returns (label, pill_classes, card_bg_classes).
    """
    base = "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-normal"
    if outcome is None:
        return ("Pending", f"{base} bg-amber-500 text-white", "bg-amber-50")
    if outcome >= 0.999:
        return ("True", f"{base} bg-emerald-600 text-white", "bg-emerald-50")
    if outcome <= 0.001:
        return ("False", f"{base} bg-rose-600 text-white", "bg-rose-50")
    pct = int(round(outcome * 100))
    return (f"Partial ({pct})", f"{base} bg-amber-500 text-white", "bg-amber-50")


def clean_topic(topic: str) -> str:
    """Strip the shared FIFA World Cup 2026 prefix — all predictions are WC 2026."""
    if not topic:
        return ""
    for prefix in ("FIFA World Cup 2026 - ", "FIFA World Cup 2026"):
        if topic.startswith(prefix):
            topic = topic[len(prefix):].strip()
            break
    return topic


def clean_claim(claim: str) -> str:
    """Remove trailing [Name, date] attribution embedded in original_statement."""
    if not claim:
        return ""
    # Strip trailing bracketed attribution, e.g. " … [Wesley Sneijder, December 2025]"
    import re
    claim = re.sub(r"\s*\[[^\]]*\]\s*$", "", claim).strip()
    return claim


def topic_pills(topic: str) -> str:
    """Split cleaned topic on ' - ' into individual soft pills (frontend-only)."""
    topic = clean_topic(topic)
    if not topic:
        return ""
    # e.g. "Netherlands Performance - Quarterfinals" → ["Netherlands Performance", "Quarterfinals"]
    parts = [part.strip() for part in topic.split(" - ") if part.strip()]
    if not parts:
        return ""
    pills = []
    for part in parts:
        pills.append(
            f'<span class="inline-flex items-center px-2.5 py-0.5 rounded-full '
            f'text-xs font-normal bg-emerald-50 text-emerald-700">{part}</span>'
        )
    return " ".join(pills)


def render_detail_page(
    rec: Dict[str, Any],
    enrichment: Optional[Dict[str, Any]] = None,
    build_date: Optional[date] = None,
) -> str:

    sid = rec["statement_id"]
    predictor = get_predictor_display_name(rec)
    slug = "-".join(predictor.lower().replace(",", "").split())
    claim = clean_claim(rec.get("original_statement", "").strip())
    source_url = rec.get("statement_original_url", "#")
    archive_url = (rec.get("statement_original_url_archive") or "").strip()
    pub_date = format_date(rec.get("statement_publication_date"))
    res_date = format_date(rec.get("resolution_date"))
    criteria = rec.get("resolution_criteria", "").strip()
    context = (rec.get("statement_context") or "").strip()
    probability_rationale = (rec.get("probability_rationale") or "").strip()
    proof = rec.get("outcome_proof", "").strip() or "—"
    verify_url = rec.get("outcome_verification_url") or ""
    topic = rec.get("statement_topic", "")
    probability = rec.get("statement_probability")
    outcome = rec.get("outcome")

    if probability is not None and outcome is not None:
        brier = score_one({"probability": probability, "outcome": outcome})
        index = brier_to_index(brier)
        brier_html = f"""
            <p class="text-sm font-mono text-slate-500 mt-1">
                Brier contribution: {format_brier(brier)} · Brier Index: {format_index(index)}
            </p>"""

    label, pill_classes, card_bg = outcome_pill(outcome)
    topic_html = topic_pills(topic)

    resolver = "Tonnis Sebo Anko Douma"
    if enrichment:
        resolver = enrichment.get("resolver") or resolver

    # Shared link style — identical height, weight and colour for both source links
    link_cls = "text-sm font-normal text-emerald-700 hover:text-emerald-800 transition-colors underline underline-offset-2"

    prob_html = ""
    if probability is not None:
        prob_html = f"""
            <p class="text-sm font-mono text-slate-500 mt-3">
                Stated probability: {probability:.0%}
            </p>"""

    verify_block = ""
    if verify_url:
        verify_block = f"""
                <p class="mt-3">
                    <a href="{verify_url}" target="_blank" rel="noopener noreferrer" class="{link_cls} inline-flex items-center">
                        Primary evidence source
                        <svg class="w-3.5 h-3.5 inline-block ml-1 -mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>
                    </a>
                </p>"""

    gen_date = (build_date or date.today()).isoformat()

    # Section heading style = homepage "High-visibility predictions" eyebrow
    section_h = "text-sm font-normal text-emerald-600 mb-2"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prediction by {predictor} • Trackrecord.info</title>
    <meta name="description" content="Permanent public record of the prediction: {claim[:120]}">
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500&display=swap');
        body, h1, h2, h3, h4, h5, h6, a, button, input, p, span, div {{
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
        }}
    </style>
    <!-- Privacy-friendly analytics by Plausible -->
    <script async src="https://plausible.io/js/pa-MQu87Y2WzO-sB_YzB2L-N.js"></script>
    <script>
      window.plausible=window.plausible||function(){{(plausible.q=plausible.q||[]).push(arguments)}},plausible.init=plausible.init||function(i){{plausible.o=i||{{}}}};
      plausible.init()
    </script>
    <script>
      document.addEventListener('DOMContentLoaded', function() {{
        if (window.plausible) {{
          plausible('prediction_detail_viewed', {{
            props: {{
              prediction_id: '{sid}',
              status: '{("resolved" if outcome is not None else "pending")}'
            }}
          }});
        }}
      }});
    </script>
</head>
<body class="bg-white text-slate-900">

    {render_nav(active="predictions", relative_prefix="../")}

    <main class="max-w-3xl mx-auto px-6 py-10">

        <!-- ========== SCORECARD ========== -->
        <section class="mb-10">
            <div class="{card_bg} rounded-3xl p-6 sm:p-8 shadow-sm">
                <div class="flex items-start justify-between gap-4 mb-4">
                    <div class="text-sm font-normal text-slate-500">
                        <a href="../forecasters/{slug}.html" class="hover:text-slate-900 transition-colors">{predictor}</a>
                    </div>
                    <span class="{pill_classes}">{label}</span>
                </div>
                <p class="text-slate-900 font-normal text-xl sm:text-2xl leading-snug">
                    “{claim}”
                </p>
                <p class="mt-3">
                    <a href="{source_url}" target="_blank" rel="noopener noreferrer" class="{link_cls} inline-flex items-center">
                        Original source
                        <svg class="w-3.5 h-3.5 inline-block ml-1 -mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>
                    </a>
                </p>
                {f"""
                <p class="mt-2">
                    <a href="{archive_url}" target="_blank" rel="noopener noreferrer" class="{link_cls} inline-flex items-center">
                        Archived copy
                        <svg class="w-3.5 h-3.5 inline-block ml-1 -mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>
                    </a>
                </p>
                """ if archive_url else ""}
                {f"""
                <p class="mt-5 font-normal text-slate-800 leading-relaxed">
                    {proof}
                </p>
                <p class="mt-3">
                    <a href="{verify_url}" target="_blank" rel="noopener noreferrer" class="{link_cls} inline-flex items-center">
                        Primary evidence source
                        <svg class="w-3.5 h-3.5 inline-block ml-1 -mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>
                    </a>
                </p>
                """ if outcome is not None and verify_url else (f"""
                <p class="mt-5 font-normal text-slate-800 leading-relaxed">
                    {proof}
                </p>
                """ if outcome is not None else "")}
            </div>
        </section>

        <!-- ========== DETAILS (claim details + outcome status, no doublings) ========== -->
        <section class="mb-10">
            <div class="{section_h}">Claim details</div>
            <table class="w-full text-left border-collapse mb-5">
                <tbody class="font-normal text-slate-800">
                    <tr>
                        <td class="py-1.5 pr-4 align-top whitespace-nowrap">Published</td>
                        <td class="py-1.5 align-top">{pub_date}</td>
                    </tr>
                    {f"""<tr>
                        <td class="py-1.5 pr-4 align-top whitespace-nowrap">Resolved</td>
                        <td class="py-1.5 align-top">{res_date}</td>
                    </tr>""" if outcome is not None else ""}
                    {f"""<tr>
                        <td class="py-1.5 pr-4 align-top whitespace-nowrap">Stated probability</td>
                        <td class="py-1.5 align-top">{probability:.0%}</td>
                    </tr>""" if probability is not None else ""}
                    {f"""<tr>
                        <td class="py-1.5 pr-4 align-top whitespace-nowrap">Brier contribution</td>
                        <td class="py-1.5 align-top">{format_brier(score_one({"probability": probability, "outcome": outcome}))}</td>
                    </tr>""" if probability is not None and outcome is not None else ""}
                    {f"""<tr>
                        <td class="py-1.5 pr-4 align-top whitespace-nowrap">Brier Index</td>
                        <td class="py-1.5 align-top">{format_index(brier_to_index(score_one({"probability": probability, "outcome": outcome})))}</td>
                    </tr>""" if probability is not None and outcome is not None else ""}
                    <tr>
                        <td class="py-1.5 pr-4 align-top whitespace-nowrap">Prediction id</td>
                        <td class="py-1.5 align-top">{sid}</td>
                    </tr>
                    {f"""<tr>
                        <td class="py-1.5 pr-4 align-top whitespace-nowrap">Topic</td>
                        <td class="py-1.5 align-top">
                            <div class="flex flex-wrap items-center gap-x-2 gap-y-2">
                                {topic_html}
                            </div>
                        </td>
                    </tr>""" if topic_html else ""}
                </tbody>
            </table>
            {f'''
                <div class="{section_h}">Statement context</div>
                <p class="font-normal text-slate-800 leading-relaxed mb-6">{context}</p>
                ''' if context else ""}
            {f'''
                <div class="{section_h}">Probability accountability</div>
                <p class="font-normal text-slate-800 leading-relaxed mb-6">{probability_rationale}</p>
                ''' if probability_rationale else ""}
            <div class="{section_h}">Resolution criteria</div>
                <p class="font-normal text-slate-800 leading-relaxed whitespace-pre-line mb-6">{criteria}</p>
        </section>

                {f'''
        <!-- Verification (resolved only) -->
        <section class="mb-12">
            <div class="{section_h}">Verification</div>
            <p class="font-normal text-slate-800 leading-relaxed">
                This resolution was performed by human examination of primary sources against the exact wording of the resolution criteria.
                The resolver ({resolver}) takes personal responsibility for the recorded outcome.
                Full methodological rules are published in the project’s
                <a href="https://github.com/TittaDiGirolamo/trackrecord.info/blob/main/METHODOLOGY.md" class="{link_cls}">METHODOLOGY.md</a>.
            </p>
        </section>
                ''' if outcome is not None else ""}

        <!-- Footer meta -->
        <footer class="pt-8 text-xs text-slate-400">
            <p>Permanent url: /predictions/{sid}.html</p>
            <p class="mt-1">Generated {gen_date} · Trackrecord.info</p>
        </footer>
    </main>

    {nav_script()}
</body>
</html>
"""
    return html


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate permanent prediction detail pages")
    parser.add_argument("--jsonl", type=Path, default=DEFAULT_JSONL)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--resolved-details", type=Path, default=DEFAULT_RESOLVED_DETAILS)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    build_date = date.today()
    print(f"Prediction detail generator | {build_date}")

    records = load_jsonl(args.jsonl)
    print(f"Loaded {len(records)} records from {args.jsonl}")

    enrichment = load_resolved_details(args.resolved_details)
    print(f"Loaded {len(enrichment)} enrichment records from {args.resolved_details}")

    # Generate detail pages for both resolved and pending predictions
    all_predictions = [r for r in records if r.get("statement_id")]
    print(f"Predictions eligible for detail pages (resolved + pending): {len(all_predictions)}")

    if args.limit > 0:
        resolved = resolved[: args.limit]
        print(f"Limited to first {args.limit}")

    if not args.dry_run:
        args.out_dir.mkdir(parents=True, exist_ok=True)

    generated = 0
    for rec in all_predictions:
        sid = rec.get("statement_id")
        if not sid:
            print("[WARNING] Skipping record without statement_id")
            continue

        enr = enrichment.get(sid)
        html = render_detail_page(rec, enr, build_date)
        out_path = args.out_dir / f"{sid}.html"

        if args.dry_run:
            if args.verbose:
                print(f"[DRY-RUN] Would write {out_path} ({len(html)} bytes)")
            generated += 1
            continue

        out_path.write_text(html, encoding="utf-8")
        generated += 1
        if args.verbose:
            print(f"  Wrote {out_path}")

    print(f"{'Would have written' if args.dry_run else 'Wrote'} {generated} detail pages to {args.out_dir}/")
    if not args.dry_run:
        print("Done.")


if __name__ == "__main__":
    main()
