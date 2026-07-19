# Resolution Workflow — Quick Reference
Date: 2026-07-19
Version: 1.0

Single source of truth: predictions_v2.jsonl
Session logs: resolution_sessions/

## For every new batch

### 1. Prepare updates file
nano batch_updates.json
# Paste the JSON with the records you want to resolve

### 2. Run the update script
python3 update_predictions.py --updates batch_updates.json

### 3. Regenerate public tables
python3 scripts/generate_prediction_tables.py

### 4. Commit
git add predictions_v2.jsonl *.html
git commit -m "feat(resolution): resolve [batch name] (N records)"
git push origin main

### 5. Create/Update session log
# Copy previous batch as template
cp resolution_sessions/2026-07-17_batch01.md resolution_sessions/YYYY-MM-DD_batchXX.md
nano resolution_sessions/YYYY-MM-DD_batchXX.md
# Fill in the per-record blocks, Section 3.5, 4, and sign-off

## Reusable files
- update_predictions.py          → automation script
- batch_updates.json             → per-batch data (create new one each time)
- resolution_sessions/           → full audit trail
- RESOLUTION_WORKFLOW.txt        → this file

## Important rules
- Only update outcome, outcome_proof, outcome_verification_url in predictions_v2.jsonl
- Always make a backup before updating
- Full disclosure in session log (including LLM use)
- Human primary-source verification is mandatory

