#!/usr/bin/env python3
"""
Master script to prepare a new resolution batch.
Usage: python3 resolve_batch.py --batch 2026-07-19_batch02 --ids pred-1,pred-2,...
"""

import json
import argparse
from pathlib import Path
from datetime import datetime

RESOLVED_DIR = Path("resolved_predictions")
SESSION_DIR = Path("resolution_sessions")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", required=True, help="Batch name e.g. 2026-07-19_batch02")
    parser.add_argument("--ids", required=True, help="Comma-separated statement_ids")
    parser.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"), help="Verification date")
    args = parser.parse_args()

    statement_ids = [sid.strip() for sid in args.ids.split(",")]

    # Create batch_updates.json template
    updates = {}
    for sid in statement_ids:
        updates[sid] = {
            "outcome": 0.0,  # placeholder
            "outcome_proof": "TODO: Write factual proof after verification",
            "outcome_verification_url": "https://www.fifa.com/..."  # placeholder
        }

    with open(f"{args.batch}_updates.json", "w", encoding="utf-8") as f:
        json.dump(updates, f, indent=2)

    print(f"Created {args.batch}_updates.json with {len(statement_ids)} records")

    # Generate individual files
    RESOLVED_DIR.mkdir(exist_ok=True)
    for sid in statement_ids:
        filepath = RESOLVED_DIR / f"{sid}.md"
        with filepath.open("w", encoding="utf-8") as f:
            f.write(f"# Resolved Prediction\n\n**Statement ID:** `{sid}`\n**Batch:** {args.batch}\n**Resolver:** Tonnis Sebo Anko Douma\n**Date verified:** {args.date}\n\nTODO: Fill full details...\n")
        print(f"Created: {filepath}")

    print("\nBatch preparation complete.")
    print("Next steps:")
    print("1. Edit the *_updates.json file with real outcome/proof/URL")
    print("2. Run: python3 update_predictions.py --updates [file]")
    print("3. Run: python3 generate_resolved_files.py")
    print("4. Fill session log and commit")

if __name__ == "__main__":
    main()
