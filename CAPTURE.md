# Capture + Promote Workflow

Safe, accountable way to add new pending predictions.
Human review remains mandatory. Nothing reaches the live dataset without explicit approval.

## Daily workflow (single path)

```bash
# 1. Ingest candidates (CSV or JSONL)
python3 tools/capture_batch.py candidates.csv

# 2. Review + promote (one interactive command)
python3 tools/review_and_promote.py          # dry-run first
python3 tools/review_and_promote.py --apply  # when happy

# 3. Rebuild site + run checks
python3 regenerate_all.py
python3 ci/check_score_consistency.py
python3 ci/check_pending_accountability.py

## Optional helpers

Create a draft row from a URL:
---
python3 tools/fetch_candidate.py "URL" --forecaster "Lastname, Firstname" --append candidates.csv
---

The review tool automatically suggests:
- probability
- rationale templates (or optional LLM draft)
- topic
- resolution criteria

You still confirm or edit every value.

## Rules

Scratch log (data/capture_log.jsonl) never affects scores
Only rows with status=queued can be promoted
Promoted rows always get outcome: null (pending)
Never skip the dry-run
Only predictions from the existing set of forecasters are allowed
Every new record must contain:
- probability_method_id
- probability_rationale (short human-confirmed paragraph)
- statement_original_url_archive (created automatically by tools/archive_url.py)


## Accountability (since 2026-08)

probability_rationale is mandatory for all new records
The promote tooling creates statement_original_url_archive via Wayback Machine
Manual pasting of archive links is not allowed
CI gate (ci/check_pending_accountability.py) enforces the above for records from 2026-08-03 onward

## Topic system
Topic logic is pluggable (tools/topics/).
Current modules:
- world_cup_2026 (default for FIFA World Cup claims)
- generic (fallback)

New domains can be added without changing the core promote logic.
