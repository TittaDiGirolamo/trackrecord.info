#!/usr/bin/env python3
"""
Atomic full regeneration (REQ-2.1 – 2.3).

Single entry point. Reads only data/predictions_v2.jsonl.
Calls the canonical scoring function for every forecaster.
Writes every public page + audit artefacts in one run.
"""

from __future__ import annotations

import json
import subprocess
import datetime
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Any

from scoring import score_forecaster, RULES_VERSION, LIMITATIONS_NOTE, format_brier

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "predictions_v2.jsonl"
PUBLIC = ROOT
PUBLIC.mkdir(exist_ok=True)


def load_predictions() -> List[Dict[str, Any]]:
    """
    Load the sole data source and normalize to the shape expected by
    the canonical scoring function, while preserving all original fields.
    """
    preds = []
    with DATA.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            raw = json.loads(line)

            # Normalize real schema → internal shape
            normalized = {
                # Required by scorer
                "id": raw.get("statement_id") or raw.get("id"),
                "forecaster_id": raw.get("forecaster") or raw.get("forecaster_id"),
                "topic": raw.get("statement_topic") or raw.get("topic") or "untagged",
                "probability": raw.get("statement_probability") if "statement_probability" in raw else raw.get("probability"),
                "outcome": raw.get("outcome"),

                # Provenance (default for existing curated data)
                "probability_method_id": raw.get("probability_method_id") or "manual-curation-v1",
                "probability_source": raw.get("original_statement") or raw.get("probability_source"),
                "probability_generated_at": raw.get("statement_publication_date") or raw.get("probability_generated_at"),

                # Keep everything original for rich detail pages
                "original": raw,
            }
            preds.append(normalized)
    return preds


def group_by_forecaster(preds: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    groups: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for p in preds:
        groups[p["forecaster_id"]].append(p)
    return dict(groups)


def get_git_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        return "unknown"


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        json.dump(obj, f, indent=2, sort_keys=True)
        f.write("\n")


def render_score_badge(score: float | None, n: int, generation_id: str, commit: str) -> str:
    brier_str = format_brier(score)
    return (
        f'<div class="score-badge">'
        f'<span class="brier">{brier_str}</span> '
        f'<span class="meta">as of {generation_id} (commit {commit[:7]}) · n = {n} resolved</span> '
        f'<span class="limitations">{LIMITATIONS_NOTE}</span>'
        f'</div>'
    )


def generate_homepage(scores: Dict[str, Any], generation_id: str, commit: str) -> None:
    rows = []
    for fid, s in sorted(scores.items(), key=lambda x: (x[1]["overall"] is None, x[1]["overall"] or 99)):
        badge = render_score_badge(s["overall"], s["resolved_count"], generation_id, commit)
        rows.append(f'<tr><td><a href="profiles/{fid}.html">{fid}</a></td><td>{badge}</td></tr>')

    html = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><title>Forecaster Scores</title></head>
<body>
<h1>Forecaster Scores (Brier)</h1>
<p>Generation: {generation_id} · Rules: {RULES_VERSION} · Commit: {commit}</p>
<table border="1" cellpadding="6">
<thead><tr><th>Forecaster</th><th>Score</th></tr></thead>
<tbody>
{''.join(rows)}
</tbody>
</table>
<p><a href="predictions.html">All predictions</a> · <a href="score_composition.json">Score composition (IDs)</a></p>
</body>
</html>
"""
    (PUBLIC / "index.html").write_text(html)


def generate_profiles(scores: Dict[str, Any], by_forecaster: Dict[str, List], generation_id: str, commit: str) -> None:
    out = PUBLIC / "profiles"
    out.mkdir(exist_ok=True)
    for fid, s in scores.items():
        badge = render_score_badge(s["overall"], s["resolved_count"], generation_id, commit)
        topic_rows = []
        for topic, t in sorted(s["topics"].items()):
            tbadge = render_score_badge(t["score"], t["resolved_count"], generation_id, commit)
            topic_rows.append(f"<tr><td>{topic}</td><td>{tbadge}</td></tr>")

        id_list = ", ".join(s["prediction_ids"]) or "—"

        html = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><title>{fid} – Scores</title></head>
<body>
<h1>{fid}</h1>
{badge}
<h2>Topic scores</h2>
<table border="1" cellpadding="6">
<thead><tr><th>Topic</th><th>Score</th></tr></thead>
<tbody>
{''.join(topic_rows) if topic_rows else '<tr><td colspan="2">No resolved predictions</td></tr>'}
</tbody>
</table>
<h2>Predictions that produced the overall score</h2>
<p>Exact IDs: {id_list}</p>
<p><a href="../index.html">← Home</a></p>
</body>
</html>
"""
        (out / f"{fid}.html").write_text(html)


def generate_predictions_table(preds: List[Dict], scores: Dict[str, Any], generation_id: str, commit: str) -> None:
    summary_rows = []
    for fid, s in sorted(scores.items()):
        badge = render_score_badge(s["overall"], s["resolved_count"], generation_id, commit)
        summary_rows.append(f"<tr><td>{fid}</td><td>{badge}</td></tr>")

    pred_rows = []
    for p in preds:
        outcome = p.get("outcome")
        outcome_str = "—" if outcome is None else str(outcome)
        pred_rows.append(
            f'<tr><td><a href="predictions/{p["id"]}.html">{p["id"]}</a></td>'
            f'<td>{p["forecaster_id"]}</td><td>{p.get("topic","")}</td>'
            f'<td>{p["probability"]}</td><td>{outcome_str}</td></tr>'
        )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><title>Predictions</title></head>
<body>
<h1>Predictions</h1>
<p>Generation: {generation_id}</p>
<h2>Score summary (must be identical to homepage & profiles)</h2>
<table border="1" cellpadding="6">
<thead><tr><th>Forecaster</th><th>Score</th></tr></thead>
<tbody>
{''.join(summary_rows)}
</tbody>
</table>
<h2>All predictions</h2>
<table border="1" cellpadding="6">
<thead><tr><th>ID</th><th>Forecaster</th><th>Topic</th><th>Probability</th><th>Outcome</th></tr></thead>
<tbody>
{''.join(pred_rows)}
</tbody>
</table>
<p><a href="index.html">← Home</a></p>
</body>
</html>
"""
    (PUBLIC / "predictions.html").write_text(html)


def generate_detail_pages(preds: List[Dict], scores: Dict[str, Any], generation_id: str, commit: str) -> None:
    out = PUBLIC / "predictions"
    out.mkdir(exist_ok=True)
    by_id = {str(p["id"]): p for p in preds}

    for pid, p in by_id.items():
        fid = p["forecaster_id"]
        s = scores[fid]
        contrib = s["contributions"].get(pid)
        original = p.get("original") or {}

        if contrib is not None:
            contrib_str = format_brier(contrib)
            contrib_note = f"This prediction contributed <strong>{contrib_str}</strong> to the mean Brier score."
        else:
            contrib_str = "—"
            contrib_note = "This prediction is still pending and does not contribute to any score."

        badge = render_score_badge(s["overall"], s["resolved_count"], generation_id, commit)

        # Provenance
        method = p.get("probability_method_id") or "—"
        source = p.get("probability_source") or "—"
        generated_at = p.get("probability_generated_at") or "—"

        # Rich original fields
        original_statement = original.get("original_statement") or "—"
        context = original.get("statement_context") or "—"
        resolution_criteria = original.get("resolution_criteria") or "—"
        outcome_proof = original.get("outcome_proof") or "—"
        verification_url = original.get("outcome_verification_url") or ""
        original_url = original.get("statement_original_url") or ""
        pub_date = original.get("statement_publication_date") or "—"
        resolution_date = original.get("resolution_date") or "—"

        verification_link = f'<a href="{verification_url}" target="_blank" rel="noopener">{verification_url}</a>' if verification_url else "—"
        original_link = f'<a href="{original_url}" target="_blank" rel="noopener">{original_url}</a>' if original_url else "—"

        html = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><title>Prediction {pid}</title></head>
<body>
<h1>Prediction {pid}</h1>

<p><strong>Forecaster:</strong> <a href="../profiles/{fid}.html">{fid}</a></p>
<p><strong>Topic:</strong> {p.get("topic", "—")}</p>
<p><strong>Probability:</strong> {p["probability"]}</p>
<p><strong>Outcome:</strong> {p.get("outcome") if p.get("outcome") is not None else "pending"}</p>
<p><strong>Publication date:</strong> {pub_date}</p>
<p><strong>Resolution date:</strong> {resolution_date}</p>

<hr>
<h2>Original statement</h2>
<blockquote>{original_statement}</blockquote>

<h2>Context</h2>
<p>{context}</p>

<h2>Resolution criteria</h2>
<p>{resolution_criteria}</p>

<h2>Outcome proof</h2>
<p>{outcome_proof}</p>
<p><strong>Verification:</strong> {verification_link}</p>
<p><strong>Original source:</strong> {original_link}</p>

<hr>
<h2>How this probability was obtained</h2>
<table border="1" cellpadding="6">
<tr><td>Method ID</td><td><code>{method}</code></td></tr>
<tr><td>Source</td><td>{source}</td></tr>
<tr><td>Generated / published at</td><td>{generated_at}</td></tr>
</table>

<hr>
<h2>Contribution to score (REQ-4.1)</h2>
<p>{contrib_note}</p>
<p>Individual Brier: {contrib_str}</p>

<hr>
<h2>Forecaster’s current overall score</h2>
{badge}

<p><a href="../predictions.html">← All predictions</a></p>
</body>
</html>
"""
        (out / f"{pid}.html").write_text(html)

def write_audit(scores: Dict[str, Any], preds: List[Dict[str, Any]], generation_id: str, commit: str) -> None:
    method_counts: Dict[str, int] = {}
    for p in preds:
        mid = p.get("probability_method_id") or "unspecified"
        method_counts[mid] = method_counts.get(mid, 0) + 1

    composition = {
        "generation_id": generation_id,
        "commit": commit,
        "rules_version": RULES_VERSION,
        "probability_methods_used": method_counts,
        "forecasters": {},
    }
    for fid, s in scores.items():
        composition["forecasters"][fid] = {
            "overall_score": s["overall"],
            "resolved_count": s["resolved_count"],
            "pending_count": s["pending_count"],
            "prediction_ids": s["prediction_ids"],
            "topics": {
                topic: {
                    "score": t["score"],
                    "resolved_count": t["resolved_count"],
                    "prediction_ids": t["prediction_ids"],
                }
                for topic, t in s["topics"].items()
            },
        }

    write_json(PUBLIC / "score_composition.json", composition)

    manifest = {
        "generation_id": generation_id,
        "commit": commit,
        "rules_version": RULES_VERSION,
        "limitations_note": LIMITATIONS_NOTE,
        "source": "data/predictions_v2.jsonl",
        "timestamp_utc": generation_id,
        "probability_methods_used": method_counts,
    }
    write_json(PUBLIC / "generation_manifest.json", manifest)


def main() -> None:
    preds = load_predictions()
    by_forecaster = group_by_forecaster(preds)

    scores = {fid: score_forecaster(ps) for fid, ps in by_forecaster.items()}

    generation_id = datetime.datetime.now(datetime.UTC).strftime("%Y%m%dT%H%M%SZ")
    commit = get_git_commit()

    generate_homepage(scores, generation_id, commit)
    generate_profiles(scores, by_forecaster, generation_id, commit)
    generate_predictions_table(preds, scores, generation_id, commit)
    generate_detail_pages(preds, scores, generation_id, commit)
    write_audit(scores, preds, generation_id, commit)

    print(f"Atomic regeneration complete")
    print(f"  generation_id : {generation_id}")
    print(f"  commit        : {commit}")
    print(f"  rules_version : {RULES_VERSION}")
    print(f"  forecasters   : {len(scores)}")
    for fid, s in sorted(scores.items()):
        print(f"    {fid:10s}  Brier={format_brier(s['overall']):6s}  n={s['resolved_count']}")


if __name__ == "__main__":
    main()
