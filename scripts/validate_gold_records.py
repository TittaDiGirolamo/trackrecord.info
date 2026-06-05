#!/usr/bin/env python3
"""
Batch Validation Script for Trackrecord.info Gold Standard Records

Usage (from repository root):
    python scripts/validate_gold_records.py

This script validates all gold_*.json files inside gold_standard/wc2026/
against the canonical PredictionRecord schema.

Location: scripts/validate_gold_records.py
"""

import json
import sys
from pathlib import Path
from typing import List, Tuple

# Add schema directory to path so we can import the model
sys.path.append(str(Path(__file__).parent.parent / "schema"))
from prediction_schema import PredictionRecord


def validate_gold_records() -> bool:
    """Validate all gold records in the repository."""
    
    repo_root = Path(__file__).parent.parent
    gold_dir = repo_root / "gold_standard" / "wc2026"
    
    if not gold_dir.exists():
        print(f"❌ Error: Directory not found: {gold_dir}")
        return False
    
    json_files: List[Path] = sorted(gold_dir.glob("gold_*.json"))
    
    if not json_files:
        print(f"❌ Error: No gold_*.json files found in {gold_dir}")
        return False
    
    print(f"🔍 Found {len(json_files)} gold records to validate...\n")
    
    success_count = 0
    failures: List[Tuple[str, str]] = []
    
    for file_path in json_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Validate with Pydantic
            record = PredictionRecord.model_validate(data)
            
            print(f"✅ {file_path.name}")
            success_count += 1
            
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON: {e}"
            print(f"❌ {file_path.name} → {error_msg}")
            failures.append((file_path.name, error_msg))
            
        except Exception as e:
            error_msg = f"{type(e).__name__}: {e}"
            print(f"❌ {file_path.name} → {error_msg}")
            failures.append((file_path.name, error_msg))
    
    # Final report
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    print(f"Total records checked : {len(json_files)}")
    print(f"✅ Successful         : {success_count}")
    print(f"❌ Failed             : {len(failures)}")
    
    if failures:
        print("\nFailed records:")
        for name, error in failures:
            print(f"  • {name}")
            print(f"    {error}\n")
        return False
    else:
        print("\n🎉 All gold records passed validation successfully!")
        return True


if __name__ == "__main__":
    success = validate_gold_records()
    sys.exit(0 if success else 1)
