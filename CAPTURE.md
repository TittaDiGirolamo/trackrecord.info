# Capture + Promote Workflow

Safe way to add new predictions without touching scores until human review.

## Daily steps

```bash
# 1. Capture a new claim (goes only into the scratch log)
python3 tools/capture_append.py \
  --source-url "https://..." \
  --forecaster "Lastname, Firstname" \
  --raw-quote "Exact words from the source" \
  --rough-claim "Normalized claim" \
  --stated-probability 0.42

# 2. Human review
nano data/capture_log.jsonl
# Change "status": "new" → "status": "queued"
# Make sure resolution_criteria is filled

# 3. Dry-run first (safe)
python3 tools/promote_captures.py

# 4. If it looks good, apply
python3 tools/promote_captures.py --apply

# 5. Rebuild site + check consistency
python3 regenerate_all.py
python3 ci/check_score_consistency.py

## Rules

Scratch log (data/capture_log.jsonl) never affects scores
Only rows with status=queued can be promoted
Promoted rows always get outcome: null (pending)
Never skip the dry-run
