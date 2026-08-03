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

## New mandatory field (since 2026-08)

Every newly promoted prediction **must** contain the field:

`statement_original_url_archive`

This field is generated **automatically** during the promote step by `tools/archive_url.py` (Wayback Machine).  
It stores a permanent archive link of the original source URL.

- Manual pasting of archive links is not allowed.
- The promote tooling is responsible for creating this field.
- Existing records are not retroactively updated.

## Probability rationale (mandatory for all new records)

When promoting, every record must receive a short `probability_rationale` paragraph that explains why the probability was chosen.  
The promote tool will prompt for it interactively if it is missing.
