#!/usr/bin/env python3
"""
Reusable script to update predictions_v2.jsonl with resolution data.
Usage: python3 update_predictions.py --updates batch_updates.json
"""

import json
import argparse
from pathlib import Path
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description="Update predictions_v2.jsonl")
    parser.add_argument("--updates", required=True, help="Path to JSON file with updates")
    parser.add_argument("--input", default="predictions_v2.jsonl", help="Input JSONL file")
    args = parser.parse_args()

    input_file = Path(args.input)
    updates_file = Path(args.updates)

    if not input_file.exists():
        print(f"ERROR: {input_file} not found")
        return
    if not updates_file.exists():
        print(f"ERROR: {updates_file} not found")
        return

    # Load updates
    with updates_file.open(encoding="utf-8") as f:
        updates = json.load(f)

    # Backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = input_file.with_suffix(f".backup_{timestamp}.jsonl")
    input_file.rename(backup_file)
    print(f"Backup created: {backup_file}")

    updated_count = 0

    with backup_file.open(encoding="utf-8") as infile, \
         input_file.open("w", encoding="utf-8") as outfile:

        for line in infile:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                outfile.write(line + "\n")
                continue

            sid = record.get("statement_id")
            if sid in updates:
                record.update(updates[sid])
                updated_count += 1
                print(f"Updated: {sid}")

            outfile.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"\nDone. Updated {updated_count} records in {input_file}")

if __name__ == "__main__":
    main()
