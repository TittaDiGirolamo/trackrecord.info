#!/usr/bin/env python3
"""
Trackrecord Table Generator - Updated to generate predictions.html
"""

import argparse
from datetime import date
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "schema"))
from prediction_schema import PredictionRecord

def load_records(path: Path):
    records = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    records.append(PredictionRecord.model_validate_json(line))
                except:
                    pass
    return records

def render_predictions_table(records, build_date):
    if not records:
        return '<tr><td colspan="5" class="px-6 py-8 text-center text-slate-500">No predictions currently tracked.</td></tr>'

    sorted_records = sorted(records, key=lambda r: (r.resolution_date or "9999-99-99", r.statement_publication_date or "1900-01-01"))
    rows = []

    for r in sorted_records:
        name = f"{r.author.firstname} {r.author.lastname}".strip()
        quote = r.original_statement.split("[")[0].strip()[:80]
        if len(quote) > 75:
            quote = quote[:75] + "..."

        days_text = "–"
        if r.resolution_date:
            try:
                days = max(0, (date.fromisoformat(r.resolution_date) - build_date).days)
                days_text = f"{days} days"
            except:
                pass

        if getattr(r, 'outcome', None) is not None:
            status = f'<span class="status-pill resolved">Resolved ({int(r.outcome*100)})</span>'
        else:
            status = '<span class="status-pill">Pending – Resolution-ready</span>'

        topics = " ".join([f'<span class="topic-pill">{t}</span>' for t in [r.statement_topic[:30]]])

        row = f'''<tr>
    <td class="px-6 py-4 font-medium" data-label="Forecaster">{name}</td>
    <td class="px-6 py-4 prediction-text" data-label="Prediction">“{quote}”</td>
    <td class="px-6 py-4 lg:text-center text-emerald-700 font-medium" data-label="Days">{days_text}</td>
    <td class="px-6 py-4 lg:text-center" data-label="Status">{status}</td>
    <td class="px-6 py-4" data-label="Topic">{topics}</td>
</tr>'''
        rows.append(row)
    return "\n".join(rows)

def write_predictions_html(path: Path, rows: str, build_date: date):
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Predictions • Trackrecord.info</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50 text-slate-900">
    <nav class="border-b border-slate-200 bg-white">
        <div class="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
            <div class="flex items-center gap-x-2">
                <div class="w-7 h-7 bg-slate-900 rounded-lg flex items-center justify-center"><span class="text-white font-bold">T</span></div>
                <a href="index.html" class="font-semibold">Trackrecord.info</a>
            </div>
            <a href="predictions.html" class="text-emerald-600 font-medium">Predictions</a>
        </div>
    </nav>
    <main class="max-w-7xl mx-auto px-6 py-10">
        <h1 class="text-3xl font-semibold mb-6">All Predictions Tracked</h1>
        <div class="bg-white border border-slate-200 rounded-3xl overflow-x-auto">
            <table class="w-full min-w-[1100px]">
                <thead class="hidden lg:table-header-group bg-slate-50">
                    <tr>
                        <th class="text-left px-6 py-4">Forecaster</th>
                        <th class="text-left px-6 py-4">Prediction</th>
                        <th class="text-center px-6 py-4">Days</th>
                        <th class="text-center px-6 py-4">Status</th>
                        <th class="text-left px-6 py-4">Topic</th>
                    </tr>
                </thead>
                <tbody>{rows}</tbody>
            </table>
        </div>
    </main>
</body>
</html>"""
    path.write_text(html, encoding="utf-8")
    print(f"Action: updated {path}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--predictions-jsonl", type=Path, default=Path("predictions.jsonl"))
    parser.add_argument("--predictions-html", type=Path, default=Path("predictions.html"))
    parser.add_argument("--build-date", type=str, default=None)
    args = parser.parse_args()

    build_date = date.fromisoformat(args.build_date) if args.build_date else date.today()
    print(f"Trackrecord Table Generator | {build_date}")

    records = load_records(args.predictions_jsonl)
    print(f"Predictions table: {len(records)} rows will be generated")

    pred_rows = render_predictions_table(records, build_date)
    write_predictions_html(args.predictions_html, pred_rows, build_date)

    print("Done.")

if __name__ == "__main__":
    main()