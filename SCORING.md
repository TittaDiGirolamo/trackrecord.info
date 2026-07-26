# Scoring Rules (Phase 1)

**Version:** `brier-1.0.0`  
**Last updated:** 2026-07-26

## What is calculated

Every published score is a **mean Brier score**.

For a single resolved prediction with forecasted probability \( p \) and binary outcome \( o \in \{0,1\} \):

\[
\text{Brier} = (p - o)^2
\]

The overall score for a forecaster (or a topic) is the arithmetic mean of the individual Brier scores of all resolved predictions that belong to that forecaster (or topic).

- Lower is better.
- Only resolved predictions contribute.
- Pending predictions are counted but do not affect the score.

## What is *not* calculated in the backend

Any “accuracy”, “skill”, percentage, or higher-is-better number you see on the site is a **frontend-only presentation**.  
It is derived from the Brier values after the pages are generated and is never stored, never recomputed by the scoring pipeline, and never used for ranking or consistency checks.

## Probability provenance

The scoring function treats the `probability` field as given.  
How that number was obtained is recorded in optional provenance fields.  
See `PROVENANCE.md`.

## Limitations note (shown on every score)

> Scores are mean Brier scores (lower is better). Only resolved predictions are included. Sample sizes remain modest for many topics; treat rankings as provisional.

## Regeneration & audit

The full site is regenerated atomically from `data/predictions_v2.jsonl` by a single process.  
The generation manifest records the git commit that contained these rules and the exact timestamp.
