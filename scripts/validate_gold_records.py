#!/usr/bin/env python3
"""
Batch Validation Script for Trackrecord.info Gold Standard Records

Run from the repository root:
    python3 scripts/validate_gold_records.py
"""

import json
import sys
from pathlib import Path

# Make sure we can import from the schema folder
sys.path.insert(0, str(Path(__file__).parent.parent / "schema"))

from prediction_schema import PredictionRecord


def main():
    repo_root = Path(__file__).parent.parent
    gold_dir = repo_root / "gold_standard" / "wc2026"

    if not gold_dir.exists():
        print(f"❌ Error: Folder not found: {gold_dir}")
        sys.exit(1)

    json_files = sorted(gold_dir.glob("gold_*.json"))

    if not json_files:
        print(f"❌ No gold_*.json files found in {gold_dir}")
        sys.exit(1)

    print(f"🔍 Found {len(json_files)} gold records to validate...\n")

    success = 0
    failed = []

    for file_path in json_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            PredictionRecord.model_validate(data)
            print(f"✅ {file_path.name}")
            success += 1

        except Exception as e:
            print(f"❌ {file_path.name} → {type(e).__name__}: {e}")
            failed.append(file_path.name)

    print("\n" + "=" * 55)
    print(f"Total: {len(json_files)}  |  ✅ Passed: {success}  |  ❌ Failed: {len(failed)}")

    if failed:
        print("\nFailed files:")
        for name in failed:
            print(f"  - {name}")
        sys.exit(1)
    else:
        print("\n🎉 All records are valid!")
        sys.exit(0)


if __name__ == "__main__":
    main()
