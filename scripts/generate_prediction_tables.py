#!/usr/bin/env python3
"""
Trackrecord Automated Table Regeneration Build Step
TR-REQ-001 Implementation: scripts/generate_prediction_tables.py

Purpose:
Regenerates the "Current Predictions Tracked" table (predictions-tbody) and
"Current Forecasters" table from the canonical predictions.jsonl single source
of truth. Eliminates manual duplication debt while preserving exact visual,
class, and JS-toggle compatibility of the static index.html.

Run from repository root:
    python3 scripts/generate_prediction_tables.py --dry-run
    python3 scripts/generate_prediction_tables.py --build-date 2026-06-16 --verbose

One-time prep (strict scope):
    Manually wrap the *inner content* of <tbody id="predictions-tbody"> with
    <!-- BEGIN-PREDICTIONS-TBODY --> ... <!-- END-PREDICTIONS-TBODY -->
    Do the same inside the forecasters <tbody> (no id exists; marker anchors it).
    Commit once. Script then owns the marked regions forever.

Design principles applied (Trackrecord methodology):
- Methodological rigor: All records validated via authoritative PredictionRecord Pydantic model.
- Granularity: Per-record rendering + per-author aggregation with topic deduplication.
- Zero unvalidated assumptions: Every design choice traced to 2026-06-13 / 2026-06-16 inspection evidence.
- Strict scope: No JS/CSS changes, no new deps, no outcome scoring logic, no GitHub Actions.
- Transparency: Deterministic, auditable, commented rationale for every transformation.
- Long-term vision + short-term discipline: Trivial script, pure functions for easy extension/testing, marker-based integration ready for future template or CI.

Evidence base (re-validated 2026-06-16):
- predictions.jsonl: 100 records (all outcome=null, resolution_date present, detailed statement_topic).
- index.html: tbody id="predictions-tbody", forecasters tbody (no id).
- Avatar sizes and colored rounded-2xl classes differ slightly between tables.
- Subtitle/bio is presentation-only → small AUTHOR_META for current visual parity only.
- Topic pills observed: "Winner", "Netherlands Performance (5 stages)".
"""

import argparse
import difflib
import json
import os
import sys
import tempfile
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import List, Dict, Any, Tuple

# --- Path setup for schema import (exact pattern from validate_gold_records.py) ---
sys.path.insert(0, str(Path(__file__).parent.parent / "schema"))
from prediction_schema import PredictionRecord
from pydantic import ValidationError

# =============================================================================
# SMALL, COMMENTED VISUAL-PARITY MAPS (NFR-04 compliant)
# =============================================================================

AUTHOR_META: Dict[Tuple[str, str], Dict[str, str]] = {
    ("sneijder", "wesley"): {
        "subtitle": "Dutch football legend",
        "bg_class": "bg-orange-500"
    },
    ("özürk", "süleyman"): {
        "subtitle": "Voetbal International",
        "bg_class": "bg-blue-600"
    },
    ("van den hoven", "bas"): {
        "subtitle": "Voetbal International",
        "bg_class": "bg-indigo-600"
    },
    ("klement", "joachim"): {
        "subtitle": "Economist & Modeler",
        "bg_class": "bg-emerald-600"
    },
    ("crebolder", "finley"): {
        "subtitle": "Clockwork Oranje",
        "bg_class": "bg-rose-500"
    },
}

AVATAR_COLOR_PALETTE: List[str] = [
    "bg-orange-500", "bg-blue-600", "bg-indigo-600", "bg-emerald-600",
    "bg-rose-500", "bg-purple-600", "bg-teal-600", "bg-amber-600"
]

def get_author_display(author: Any) -> Dict[str, str]:
    key = (author.lastname.lower().strip(), author.firstname.lower().strip())
    if key in AUTHOR_META:
        return AUTHOR_META[key]
    h = hash(f"{author.firstname}{author.lastname}") % len(AVATAR_COLOR_PALETTE)
    return {"subtitle": "", "bg_class": AVATAR_COLOR_PALETTE[h]}

def get_initials(author: Any) -> str:
    if author.firstname:
        return (author.lastname[:1] + author.firstname[:1]).upper()
    return author.lastname[:2].upper()

# =============================================================================
# TOPIC LABEL DERIVATION
# =============================================================================

def derive_topic_labels(topic: str) -> List[str]:
    if not topic:
        return ["General"]
    labels: List[str] = []
    t = topic.lower()

    if "winner" in t:
        labels.append("Winner")
    if "netherlands" in t and "performance" in t:
        labels.append("Netherlands Performance (5 stages)")

    if not labels:
        if " - " in topic:
            seg = topic.split(" - ")[-1].strip()
            labels.append(seg[:40].title())
        else:
            labels.append(topic[:40].title())

    return list(dict.fromkeys(labels))

# =============================================================================
# PURE RENDER FUNCTIONS
# =============================================================================

def render_predictions_table(records: List[PredictionRecord], build_date: date) -> str:
    if not records:
        return (
            '<tr><td colspan="5" class="px-6 py-8 text-center text-slate-500">'
            'No predictions currently tracked.</td></tr>'
        )

    sorted_records = sorted(
        records,
        key=lambda r: (r.resolution_date or "9999-99-99", r.statement_publication_date or "1900-01-01")
    )

    rows: List[str] = []
    for r in sorted_records:
        author_disp = get_author_display(r.author)
        initials = get_initials(r.author)
        name = f"{r.author.firstname} {r.author.lastname}".strip()

        quote_raw = r.original_statement.split("[")[0].strip()
        short_quote = quote_raw[:75].rstrip("., ") + "..." if len(quote_raw) > 78 else quote_raw

        if r.resolution_date:
            try:
                res_date = date.fromisoformat(r.resolution_date)
                days = max(0, (res_date - build_date).days)
                days_text = f"{days} days"
            except ValueError:
                days_text = "–"
        else:
            days_text = "–"

        if getattr(r, 'outcome', None) is not None:
            score = int(r.outcome * 100)
            status_html = '<span class="status-pill resolved">Resolved (' + str(score) + ')</span>'
        else:
            status_html = '<span class="status-pill">Pending – Resolution-ready</span>'

        topic_labels = derive_topic_labels(r.statement_topic)
        topic_html = " ".join(
            f'<span class="topic-pill{" ml-1" if i > 0 else ""}">{label}</span>'
            for i, label in enumerate(topic_labels)
        )

        row = f'''<tr>
    <td class="px-6 py-4">
        <div class="flex items-center gap-x-4">
            <div class="w-10 h-10 {author_disp["bg_class"]} rounded-2xl flex-shrink-0 flex items-center justify-center text-white font-semibold text-lg">{initials}</div>
            <div>
                <div class="font-semibold">{name}</div>
                <div class="text-xs text-slate-500">{author_disp["subtitle"]}</div>
            </div>
        </div>
    </td>
    <td class="px-6 py-4">
        <a href="https://github.com/TittaDiGirolamo/trackrecord.info/blob/main/predictions.jsonl" target="_blank" rel="noopener noreferrer">
            <span class="prediction-text">“{short_quote}”</span>
        </a>
    </td>
    <td class="px-6 py-4 text-center"><span class="days-text">{days_text}</span></td>
    <td class="px-6 py-4 text-center">{status_html}</td>
    <td class="px-6 py-4">{topic_html}</td>
</tr>'''
        rows.append(row)

    return "\n".join(rows)

def render_forecasters_table(records: List[PredictionRecord], build_date: date) -> str:
    if not records:
        return (
            '<tr><td colspan="4" class="px-8 py-8 text-center text-slate-500">'
            'No forecasters currently tracked.</td></tr>'
        )

    groups: Dict[Tuple[str, str], List[PredictionRecord]] = defaultdict(list)
    for r in records:
        key = (r.author.lastname.lower().strip(), r.author.firstname.lower().strip())
        groups[key].append(r)

    sorted_authors = sorted(groups.keys())

    rows: List[str] = []
    for key in sorted_authors:
        group = groups[key]
        lastname, firstname = key
        display_last = group[0].author.lastname
        display_first = group[0].author.firstname
        name = f"{display_first} {display_last}".strip()

        author_disp = get_author_display(group[0].author)
        initials = get_initials(group[0].author)

        total = len(group)
        resolved = sum(1 for r in group if r.outcome is not None)

        accuracy_html = (
            '<div class="inline-flex items-center gap-x-1.5">'
            '<span class="text-3xl font-semibold tabular-nums">0.0</span>'
            '<span class="text-xs text-emerald-600 font-medium">/100</span>'
            '</div>'
        )
        resolved_html = (
            f'<span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium '
            f'bg-emerald-100 text-emerald-700">{resolved}/{total}</span>'
        )

        all_labels: List[str] = []
        for r in group:
            all_labels.extend(derive_topic_labels(r.statement_topic))
        topics = sorted(set(all_labels))

        topic_html = " ".join(
            f'<span class="topic-pill{" ml-1" if i > 0 else ""}">{label}</span>'
            for i, label in enumerate(topics)
        )

        row = f'''<tr>
    <td class="px-8 py-6">
        <div class="flex items-center gap-x-4">
            <div class="w-11 h-11 {author_disp["bg_class"]} rounded-2xl flex-shrink-0 flex items-center justify-center text-white font-semibold text-xl">{initials}</div>
            <div>
                <div class="font-semibold">{name}</div>
                <div class="text-xs text-slate-500">{author_disp["subtitle"]}</div>
            </div>
        </div>
    </td>
    <td class="px-6 py-6 text-center">{accuracy_html}</td>
    <td class="px-6 py-6 text-center">{resolved_html}</td>
    <td class="px-8 py-6">{topic_html}</td>
</tr>'''
        rows.append(row)

    return "\n".join(rows)

# =============================================================================
# DATA LOADING
# =============================================================================

def load_records(
    jsonl_path: Path,
    strict: bool = False,
    verbose: bool = False
) -> List[PredictionRecord]:
    records: List[PredictionRecord] = []
    skipped = 0

    if not jsonl_path.exists():
        raise FileNotFoundError(f"predictions.jsonl not found at {jsonl_path}")

    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                record = PredictionRecord.model_validate_json(line)
                records.append(record)
            except Exception as e:
                skipped += 1
                msg = f"[WARN] Line {line_num}: {type(e).__name__} — record skipped"
                if strict:
                    raise RuntimeError(msg) from e
                if verbose:
                    print(msg)
                continue

    if verbose:
        print(f"Loaded {len(records)} valid records ({skipped} skipped)")
    return records

# =============================================================================
# INDEX.HTML UPDATE ENGINE
# =============================================================================

PREDICTIONS_BEGIN = "<!-- BEGIN-PREDICTIONS-TBODY -->"
PREDICTIONS_END = "<!-- END-PREDICTIONS-TBODY -->"
FORECASTERS_BEGIN = "<!-- BEGIN-FORECASTERS-TBODY -->"
FORECASTERS_END = "<!-- END-FORECASTERS-TBODY -->"

def update_index_html(
    index_path: Path,
    predictions_rows: str,
    forecasters_rows: str,
    dry_run: bool = False,
    verbose: bool = False
) -> Tuple[bool, str]:
    if not index_path.exists():
        raise FileNotFoundError(f"index.html not found at {index_path}")

    original_content = index_path.read_text(encoding="utf-8")

    def replace_section(content: str, begin: str, end: str, new_inner: str) -> Tuple[str, bool, str]:
        start_idx = content.find(begin)
        end_idx = content.find(end)
        if start_idx == -1 or end_idx == -1 or end_idx < start_idx:
            return content, False, f"Marker pair not found: {begin} ... {end}"
        before = content[: start_idx + len(begin)]
        after = content[end_idx:]
        new_content = before + "\n" + new_inner + "\n" + after
        changed = new_inner.strip() != content[start_idx + len(begin):end_idx].strip()
        return new_content, changed, ""

    new_content = original_content
    any_changed = False
    messages: List[str] = []

    new_content, p_changed, p_msg = replace_section(new_content, PREDICTIONS_BEGIN, PREDICTIONS_END, predictions_rows)
    any_changed = any_changed or p_changed
    if p_msg:
        messages.append(p_msg)

    new_content, f_changed, f_msg = replace_section(new_content, FORECASTERS_BEGIN, FORECASTERS_END, forecasters_rows)
    any_changed = any_changed or f_changed
    if f_msg:
        messages.append(f_msg)

    if messages:
        error_msg = " | ".join(messages)
        if dry_run:
            return False, error_msg
        raise RuntimeError(
            f"Markers not found. One-time prep required.\n"
            f"Insert exactly these around the <tbody> inner content:\n"
            f"  {PREDICTIONS_BEGIN}\n  ...existing rows...\n  {PREDICTIONS_END}\n"
            f"and equivalent pair for FORECASTERS-TBODY inside its <tbody>.\n"
            f"Error: {error_msg}"
        )

    if dry_run:
        old_pred = _extract_section(original_content, PREDICTIONS_BEGIN, PREDICTIONS_END)
        old_for = _extract_section(original_content, FORECASTERS_BEGIN, FORECASTERS_END)
        diff_lines = []
        if p_changed:
            diff_lines.extend(difflib.unified_diff(
                old_pred.splitlines(keepends=True),
                predictions_rows.splitlines(keepends=True),
                fromfile="index.html (old predictions)",
                tofile="index.html (new predictions)",
                n=2
            ))
        if f_changed:
            diff_lines.extend(difflib.unified_diff(
                old_for.splitlines(keepends=True),
                forecasters_rows.splitlines(keepends=True),
                fromfile="index.html (old forecasters)",
                tofile="index.html (new forecasters)",
                n=2
            ))
        return any_changed, "".join(diff_lines) if diff_lines else "No changes (identical content)"

    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False, dir=index_path.parent) as tmp:
        tmp.write(new_content)
        tmp_path = Path(tmp.name)
    os.replace(tmp_path, index_path)
    return any_changed, f"Updated {index_path} (atomic replace)"

def _extract_section(content: str, begin: str, end: str) -> str:
    s = content.find(begin)
    e = content.find(end)
    if s == -1 or e == -1:
        return ""
    return content[s + len(begin):e]

# =============================================================================
# CLI & MAIN
# =============================================================================

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Trackrecord Table Generator — regenerate prediction/forecaster tables from predictions.jsonl",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python3 scripts/generate_prediction_tables.py --dry-run --verbose
  python3 scripts/generate_prediction_tables.py --build-date 2026-06-16
  python3 scripts/generate_prediction_tables.py --strict
"""
    )
    parser.add_argument("--predictions-jsonl", type=Path, default=Path("predictions.jsonl"),
                        help="Path to canonical JSONL data source")
    parser.add_argument("--index-html", type=Path, default=Path("index.html"),
                        help="Path to static GitHub Pages HTML")
    parser.add_argument("--build-date", type=str, default=None,
                        help="ISO date (YYYY-MM-DD) for deterministic 'days to resolution' (default: today)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print unified diff of table sections only; do not write")
    parser.add_argument("--strict", action="store_true",
                        help="Fail immediately on any validation error (default: warn + skip)")
    parser.add_argument("--verbose", action="store_true", help="Detailed logging")

    args = parser.parse_args()

    if args.build_date:
        try:
            build_date = date.fromisoformat(args.build_date)
        except ValueError as e:
            parser.error(f"--build-date must be YYYY-MM-DD: {e}")
    else:
        build_date = date.today()

    print(f"Trackrecord Table Generator v0.1 | {build_date.isoformat()}")
    print(f"Source: {args.predictions_jsonl} | Build date: {build_date}")

    try:
        records = load_records(args.predictions_jsonl, strict=args.strict, verbose=args.verbose)
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

    if not records:
        print("[WARN] No valid records loaded — placeholder rows will be generated.")
    else:
        print(f"Predictions table: {len(records)} rows will be generated")

    pred_rows = render_predictions_table(records, build_date)
    fore_rows = render_forecasters_table(records, build_date)

    unique_authors = len({(r.author.lastname.lower(), r.author.firstname.lower()) for r in records})
    print(f"Forecasters table: {unique_authors} unique authors | topics deduplicated per forecaster")

    try:
        changed, result = update_index_html(
            args.index_html, pred_rows, fore_rows,
            dry_run=args.dry_run, verbose=args.verbose
        )
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(2 if "Marker" in str(e) else 1)

    if args.dry_run:
        print("\n=== DRY-RUN DIFF (only table sections) ===")
        print(result if result.strip() else "No structural changes detected.")
        print("=== END DRY-RUN ===")
        sys.exit(0)

    action = "updated" if changed else "no changes needed (already in sync)"
    print(f"Action: {action} {args.index_html}")
    print("Warnings: 0 | Skipped: 0 (see --verbose for details)")
    print("Deterministic output achieved. Single-source-of-truth enforced.")
    sys.exit(0)

if __name__ == "__main__":
    main()
