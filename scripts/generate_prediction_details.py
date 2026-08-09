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
    impact: Optional[Dict[str, Any]] = None,
) -> str:

    sid = rec["statement_id"]
    predictor = get_predictor_display_name(rec)
    slug = "-".join(predictor.lower().replace(",", "").split())
    claim = clean_claim(rec.get("original_statement", "").strip())
    source_url = rec.get("statement_original_url", "#")
    archive_url = (rec.get("statement_original_url_archive") or "").strip()
    pub_date = format_date(rec.get("statement_publication_date"))
    res_date = format_date(rec.get("resolution_date"))
    logged_raw = rec.get("extraction_timestamp") or rec.get("probability_generated_at")
    logged_date = format_date(logged_raw[:10] if logged_raw and len(str(logged_raw)) >= 10 else None)
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

    # Impact on track record block (only for resolved predictions that have impact data)
    impact_html = ""
    if impact and outcome is not None:
        bi = impact.get("before_index")
        ai = impact.get("after_index")
        bb = impact.get("before_brier")
        ab = impact.get("after_brier")
        br = impact.get("before_rank")
        ar = impact.get("after_rank")
        delta = impact.get("delta_index")
        status = impact.get("status", label)
        slug = impact.get("forecaster_slug", slug)
        bi_str = format_index(bi) if bi is not None else "—"
        ai_str = format_index(ai) if ai is not None else "—"
        bb_str = format_brier(bb) if bb is not None else "—"
        ab_str = format_brier(ab) if ab is not None else "—"
        if delta is not None:
            sign = "+" if delta >= 0 else ""
            delta_str = f"{sign}{format_index(delta)}"
        else:
            delta_str = "—"
        br_str = str(br) if br is not None else "—"
        ar_str = str(ar) if ar is not None else "—"
        impact_html = f"""
        <section class="mb-10">
            <div class="{section_h}">Impact on track record</div>
            <div class="rounded-2xl border border-slate-200 p-5 md:p-6">
                <div class="flex items-center gap-x-3 mb-4">
                    <span class="{pill_classes}">{status}</span>
                </div>
                <div class="mb-3">
                    <p class="text-xs text-slate-500 mb-0.5">Brier Index</p>
                    <p class="text-2xl md:text-3xl font-medium text-slate-900 tabular-nums tracking-tight">
                        {bi_str} → {ai_str}
                        <span class="text-base font-normal text-slate-500">({delta_str})</span>
                    </p>
                </div>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm">
                    <div>
                        <p class="text-slate-500 text-xs mb-0.5">Raw Brier</p>
                        <p class="tabular-nums text-slate-800">{bb_str} → {ab_str}</p>
                    </div>
                    <div>
                        <p class="text-slate-500 text-xs mb-0.5">Overall rank</p>
                        <p class="tabular-nums text-slate-800">{br_str} → {ar_str}</p>
                    </div>
                </div>
                <div class="mt-4">
                    <a href="../forecasters/{slug}.html" class="inline-flex items-center text-sm font-medium text-emerald-700 hover:text-emerald-800 transition-colors">
                        View updated profile →
                    </a>
                </div>
            </div>
        </section>
        """
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

        <!-- ========== IMPACT ON TRACK RECORD ========== -->
        {impact_html}

        <!-- ========== DETAILS (claim details + outcome status, no doublings) ========== -->
        <section class="mb-10">
            <div class="{section_h}">Claim details</div>
            <p class="text-xs text-slate-400 mb-3">Published → Logged → Resolved</p>
            <table class="w-full text-left border-collapse mb-5">
                <tbody class="font-normal text-slate-800">
                    <tr>
                        <td class="py-1.5 pr-4 align-top whitespace-nowrap">Published</td>
                        <td class="py-1.5 align-top">{pub_date}</td>
                    </tr>
                    {f"""<tr>
                        <td class="py-1.5 pr-4 align-top whitespace-nowrap">Logged</td>
                        <td class="py-1.5 align-top">{logged_date}</td>
                    </tr>""" if logged_date and logged_date != "—" else ""}
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
                        <td class="py-1.5 pr-4 align-top whitespace-nowrap">Brier Index (this prediction)</td>
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
                    {f"""<tr>
                        <td class="py-1.5 pr-4 align-top whitespace-nowrap">Archived source</td>
                        <td class="py-1.5 align-top"><a href="{archive_url}" target="_blank" rel="noopener noreferrer" class="{link_cls}">View archive</a></td>
                    </tr>""" if archive_url else ""}
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


def compute_impacts(records: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """
    For every resolved prediction, compute the effect on its forecaster's
    overall Brier Index and rank (with vs without that prediction).
    Rank is among forecasters meeting the min resolved threshold, sorted by
    Brier Index descending (higher better).
    """
    from scoring import score_forecaster
    from collections import defaultdict

    buckets: Dict[str, List[Dict]] = defaultdict(list)
    for rec in records:
        name = get_predictor_display_name(rec)
        if name and name != "Unknown":
            buckets[name].append(rec)

    full_scores: Dict[str, Any] = {}
    for name, preds in buckets.items():
        normalized = []
        for raw in preds:
            if raw.get("outcome") is None:
                continue
            normalized.append({
                "id": raw.get("statement_id") or raw.get("id"),
                "forecaster_id": name,
                "topic": raw.get("statement_topic") or "untagged",
                "probability": raw.get("statement_probability") if "statement_probability" in raw else raw.get("probability"),
                "outcome": raw.get("outcome"),
            })
        full_scores[name] = score_forecaster(normalized)

    MIN_R = 1
    eligible = [
        (n, s) for n, s in full_scores.items()
        if s["resolved_count"] >= MIN_R and s.get("overall_index") is not None
    ]
    eligible.sort(key=lambda x: (-x[1]["overall_index"], x[0]))
    current_ranks = {n: i for i, (n, _) in enumerate(eligible, 1)}

    impacts: Dict[str, Dict[str, Any]] = {}
    for name, preds in buckets.items():
        resolved = [r for r in preds if r.get("outcome") is not None]
        if not resolved:
            continue
        after = full_scores[name]
        after_index = after.get("overall_index")
        after_brier = after.get("overall")
        after_rank = current_ranks.get(name)

        for target in resolved:
            tid = target.get("statement_id") or target.get("id")
            if not tid:
                continue
            remaining = []
            for raw in resolved:
                rid = raw.get("statement_id") or raw.get("id")
                if rid == tid:
                    continue
                remaining.append({
                    "id": rid,
                    "forecaster_id": name,
                    "topic": raw.get("statement_topic") or "untagged",
                    "probability": raw.get("statement_probability") if "statement_probability" in raw else raw.get("probability"),
                    "outcome": raw.get("outcome"),
                })
            before = score_forecaster(remaining)
            before_index = before.get("overall_index")
            before_brier = before.get("overall")

            before_rank = None
            if before_index is not None and before["resolved_count"] >= MIN_R:
                temp = []
                for n2, s2 in full_scores.items():
                    if n2 == name:
                        temp.append((n2, before_index))
                    elif s2.get("overall_index") is not None and s2["resolved_count"] >= MIN_R:
                        temp.append((n2, s2["overall_index"]))
                temp.sort(key=lambda x: (-x[1], x[0]))
                for i, (n2, _) in enumerate(temp, 1):
                    if n2 == name:
                        before_rank = i
                        break

            slug = "-".join(name.lower().replace(",", "").split())
            impacts[tid] = {
                "forecaster_name": name,
                "forecaster_slug": slug,
                "status": "TRUE" if float(target.get("outcome", 0)) >= 0.5 else "FALSE",
                "before_index": before_index,
                "after_index": after_index,
                "before_brier": before_brier,
                "after_brier": after_brier,
                "before_rank": before_rank,
                "after_rank": after_rank,
                "delta_index": (after_index - before_index) if (after_index is not None and before_index is not None) else None,
            }
    return impacts


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

    print("Computing impact-on-track-record deltas …")
    impacts = compute_impacts(records)
    print(f"  Computed impacts for {len(impacts)} resolved predictions")

    all_predictions = [r for r in records if r.get("statement_id")]
    print(f"Predictions eligible for detail pages (resolved + pending): {len(all_predictions)}")

    if args.limit > 0:
        all_predictions = all_predictions[: args.limit]
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
        impact = impacts.get(sid)
        html = render_detail_page(rec, enr, build_date, impact=impact)
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
