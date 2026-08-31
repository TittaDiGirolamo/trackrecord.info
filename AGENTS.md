# Agent rules for trackrecord.info

This repository publishes a static, high-integrity record of public predictions.

## Non-negotiable

- Single source of truth for scores: `predictions_v2.jsonl` plus `scoring/`.
- Public HTML is produced by `regenerate_all.py` (or the Actions workflow that runs the same generators). Do not hand-edit generated pages as the durable fix.
- Formal score is mean Brier. Display indexes are presentation only.
- Human review remains mandatory for logging and resolution. Do not auto-resolve live records.
