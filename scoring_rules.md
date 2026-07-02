# Trackrecord Scoring Rules v2.0
**Date**: 2026-07-02
**Status**: Implemented (Long-term recommendation)
**Version**: 2.0 (supersedes any prior binary-only system)

## 1. Purpose and Principles
- Provide granular, auditable scoring for match predictions while preserving the primary binary `outcome` field.
- Reward different levels of accuracy: exact score > winner + GD > winner only.
- Support long-term calibration as more data becomes available.
- Maintain strict falsifiability, transparency, and independence from external influence.
- All rules are explicit, versioned, and applied consistently.

## 2. Scope
- Applies primarily to **match result predictions** (exact score forecasts).
- Non-match statements (e.g., "reaches quarter-finals", "wins tournament") remain binary (1.0/0.0) unless a clear decomposition is defined in future versions.
- Only applied to resolved predictions (non-null `outcome`).

## 3. Tiered Scoring System (Core Rules)
For resolved match predictions, the following tiers are used:

| Tier | Condition | Weighted Score | Notes |
|------|-----------|----------------|-------|
| Exact Score | Predicted score == Actual score | 1.0 | Highest reward; implies correct winner + GD |
| Winner + GD | Correct winner **and** correct goal difference (including 0-0) | 0.4 | Intermediate; recognizes directional + margin accuracy |
| Winner Only | Correct winner but incorrect GD | 0.2 | Base directional credit |
| GD Only (optional) | Incorrect winner but correct GD | 0.1 | Rare; low weight to discourage |
| None | Incorrect winner | 0.0 | No credit |

**Derivation of Weights**:
- Exact = 1.0 (full credit, benchmark)
- Winner + GD = 0.4 (40% of full; meaningful but not dominant)
- Winner Only = 0.2 (20% of full; conservative directional recognition)
- Calibrated proportionally; adjustable in future versions based on empirical performance (e.g., correlation with long-term accuracy).

**Edge Cases**:
- Draws (0-0, 1-1, etc.): GD = 0 is correctly handled.
- High-scoring matches: No special adjustment; GD is absolute difference.
- Forfeits or abandoned matches: Use official FIFA/competition ruling.

## 4. JSON Schema Extension
Add to each resolved prediction object:

```json
"scoring_version": "2.0",
"partial_accuracy": {
  "winner_correct": boolean,
  "goal_difference_correct": boolean,
  "exact_score_correct": boolean,
  "weighted_score": number (0.0 to 1.0),
  "tier": "exact" | "winner_gd" | "winner_only" | "none",
  "notes": "string (optional, e.g. 'GD off by 1 goal')"
}
```

The primary `outcome` field (1.0/0.0) remains unchanged for backward compatibility and binary aggregation.

## 5. Implementation Process
1. Backup current `predictions.jsonl`.
2. For each resolved match prediction:
   - Determine actual result from `outcome_proof` or verification URL.
   - Apply tier rules above.
   - Populate `partial_accuracy` object.
3. Add top-level `"scoring_version": "2.0"` to the file or per-object.
4. Validate JSON.
5. Commit with message referencing this rules document.

## 6. Calibration and Future-Proofing (Long-Term Vision)
- **Initial Weights**: As defined above (data-driven starting point).
- **Calibration Method**: After every 50+ new resolved predictions, re-evaluate weights using:
  - Correlation of partial scores with overall forecasting skill (e.g., Brier score on probabilistic statements).
  - Frequency distribution of tiers achieved.
  - Update to v2.1+ with changelog.
- **Versioning**: Always increment on material changes. Old versions remain in git history.
- **Extension Path**: Add support for multi-goal closeness bonuses or probabilistic weighting in future versions.

## 7. Auditability and Independence
- All determinations reference official sources only (FIFA, competition results).
- No subjective judgment; rules are deterministic.
- Full history preserved in repository.

This document constitutes the explicit, auditable foundation for the tiered scoring system. Apply prospectively to new resolutions and retroactively to existing resolved entries for consistency.