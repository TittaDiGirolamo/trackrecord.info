#!/usr/bin/env python3
"""
Trackrecord Table Generator
Final clean version - Generates both index.html and predictions.html
"""

import argparse
from datetime import date
from pathlib import Path
import sys
from collections import defaultdict

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

    # Sort by resolution date
    sorted_records = sorted(records, key=lambda r: (r.resolution_date or "9999-99-99", r.statement_publication_date or "1900-01-01"))
    rows = []

    for r in sorted_records:
        name = f"{r.author.firstname} {r.author.lastname}".strip()
        quote = r.original_statement.split("[")[0].strip()[:85]
        if len(quote) > 80:
            quote = quote[:80] + "..."

        # Calculate days remaining
        days_text = "–"
        if r.resolution_date:
            try:
                days = max(0, (date.fromisoformat(r.resolution_date) - build_date).days)
                days_text = f"{days} days"
            except:
                pass

        # Status
        if getattr(r, 'outcome', None) is not None:
            score = int(r.outcome * 100)
            status = f'<span class="status-pill resolved">Resolved ({score})</span>'
        else:
            status = '<span class="status-pill">Pending – Resolution-ready</span>'

        # Topic
        topic = r.statement_topic[:35] if r.statement_topic else "General"
        topic_html = f'<span class="topic-pill">{topic}</span>'

        row = f'''<tr class="prediction-row mobile-table-row">
    <td class="px-6 py-4 font-medium text-slate-900 order-2 lg:order-1" data-label="Forecaster">{name}</td>
    <td class="px-6 py-4 prediction-text order-1 lg:order-2" data-label="Prediction">“{quote}”</td>
    <td class="px-6 py-4 lg:text-center text-emerald-700 font-medium order-3 lg:order-3" data-label="Days to Resolution">{days_text}</td>
    <td class="px-6 py-4 lg:text-center order-4 lg:order-4" data-label="Status">{status}</td>
    <td class="px-6 py-4 order-5 lg:order-5" data-label="Topic">{topic_html}</td>
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
    <style>
        body {{ font-family: 'Inter', system-ui, sans-serif; }}
        .prediction-text {{ font-size: 1.02rem; line-height: 1.4; }}
        .status-pill {{ display: inline-flex; align-items: center; padding: 2px 10px; background-color: #fef3c7; color: #92400e; font-size: 0.75rem; font-weight: 600; border-radius: 9999px; }}
        .status-pill.resolved {{ background-color: #d1fae5; color: #065f46; }}
        .topic-pill {{ display: inline-flex; align-items: center; padding: 2px 10px; background-color: #10b981; color: white; font-size: 0.75rem; font-weight: 600; border-radius: 9999px; }}
        
        @media (max-width: 1023px) {
            .mobile-table-row {{ display: flex; flex-direction: column; }}
            .mobile-table-row td {{ display: block; padding-top: 0.5rem; padding-bottom: 0.5rem; }}
        }
    </style>
</head>
<body class="bg-slate-50 text-slate-900">
    <nav class="border-b border-slate-200 bg-white">
        <div class="max-w-7xl mx-auto px-6">
            <div class="flex items-center justify-between h-16">
                <div class="flex items-center gap-x-2.5">
                    <div class="w-7 h-7 bg-slate-900 rounded-lg flex items-center justify-center">
                        <span class="text-white text-xl font-bold tracking-tighter">T</span>
                    </div>
                    <a href="index.html" class="font-semibold tracking-tight">Trackrecord.info</a>
                </div>
                <div class="flex items-center gap-x-6 text-sm">
                    <a href="index.html" class="text-slate-600 hover:text-slate-900">Home</a>
                    <a href="predictions.html" class="text-emerald-600 font-medium">Predictions</a>
                    <a href="forecasters.html" class="text-slate-600 hover:text-slate-900">Forecasters</a>
                </div>
            </div>
        </div>
    </nav>

    <main class="max-w-7xl mx-auto px-6 py-10">
        <h1 class="text-3xl font-semibold tracking-tight mb-2">All Predictions Tracked</h1>
        <p class="text-slate-600 mb-6">Unfiltered view • Data from predictions.jsonl • Generated on {build_date}</p>

        <div class="bg-white border border-slate-200 rounded-3xl overflow-x-auto shadow-sm">
            <table class="w-full min-w-[1100px] lg:min-w-0">
                <thead class="hidden lg:table-header-group">
                    <tr class="border-b border-slate-100 bg-slate-50/50">
                        <th class="text-left py-4 px-6 text-sm font-semibold text-slate-600">Forecaster</th>
                        <th class="text-left py-4 px-6 text-sm font-semibold text-slate-600">Prediction</th>
                        <th class="text-center py-4 px-6 text-sm font-semibold text-slate-600">Days to Resolution</th>
                        <th class="text-center py-4 px-6 text-sm font-semibold text-slate-600">Status</th>
                        <th class="text-left py-4 px-6 text-sm font-semibold text-slate-600">Topic</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-slate-100 text-sm">
                    {rows}
                </tbody>
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