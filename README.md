# Phase 1 – Canonical Brier Scoring Foundation

Single source of truth + pure Brier scores + atomic regeneration + CI consistency gate + probability provenance.

## Quick start

```bash
# 1. Put your predictions in data/predictions_v2.jsonl
# 2. Regenerate everything
python3 regenerate.py

# 3. Verify consistency (must pass before any deploy)
python3 ci/check_score_consistency.py
Core guarantees

Single source of truth: only data/predictions_v2.jsonl is read.
One canonical scoring function: pure mean Brier (scoring/score.py).
Atomic regeneration: one command rebuilds every public page.
CI gate: recomputes every score and fails the build on any mismatch.
Inspectable: every score shows “as of”, sample size, limitations note, and the exact prediction IDs that produced it.
Provenance: every probability carries a probability_method_id so extraction is reproducible.

## Key files

| File / directory                  | Purpose                                      |
|-----------------------------------|----------------------------------------------|
| SCORING.md                        | Human-readable scoring rules                 |
| PROVENANCE.md                     | How probabilities may enter the dataset      |
| CAPTURE.md                        | Capture + promote workflow                   |
| scoring/                          | Canonical Brier implementation               |
| regenerate_all.py                 | Atomic full-site rebuild                     |
| ci/check_score_consistency.py     | Consistency gate                             |
| extractors/                       | Upstream probability extractors              |
| tools/archive_url.py              | Wayback Machine helper – creates `statement_original_url_archive` |
| data/predictions_v2.jsonl         | Sole authoritative data                      |

## Product Metrics

**North Star:** Weekly completed accountability lookups

A completed lookup is a session in which a user selects a public figure, views their accuracy profile, and opens at least one resolved prediction detail page that shows the full evidence trail.

We optimize for **sustained** growth of this metric over the long run. Every significant initiative must document its expected impact on the North Star *before* work begins. The required depth of the hypothesis scales with the size of the initiative.

Full definition, measurement method, size-based requirements, and initiative tracking:  
→ [NORTH_STAR.md](NORTH_STAR.md)

## Regenerate the public site (Phase 1)

```bash
python3 regenerate_all.py
python3 ci/check_score_consistency.py   # must pass before deploy
```

- Sole data source: `predictions_v2.jsonl`
- Canonical math: `scoring/` + `SCORING.md` (pure mean Brier; Brier Index is display-only)
- Do **not** use legacy `regenerate.py` for the live `forecasters/` tree

