# Probability Provenance (Phase 1)

Every probability that enters `predictions_v2.jsonl` must be reproducible.
The scoring pipeline itself never recalculates a probability; it only reads the
number that is already present. Provenance fields make the origin of that
number inspectable and auditable.

## Required practice

When a probability is written into the jsonl, the writer **must** also write a
`probability_method_id`. This ID is a stable, published identifier of the exact
method and version used.

Examples of good method IDs:

- `human-elicited-v1`
- `rule-extract-keyword-v2`
- `llm-extract-claude-3.5-prompt-v4`
- `manual-curation-2026-03`

If two people (or two runs) can produce different numbers from the same source
text, the method is not yet deterministic enough.

## Schema fields

| Field                       | Type     | Purpose |
|-----------------------------|----------|---------|
| `probability_method_id`     | string   | Stable ID of the exact method/version |
| `probability_source`        | string   | Original text snippet or reference |
| `probability_generated_at`  | string   | ISO-8601 timestamp |
| `probability_model`         | string   | Model name/version (LLM methods) |
| `probability_prompt_hash`   | string   | Content hash of the prompt template |
| `probability_seed`          | integer  | RNG seed if stochastic |

The scoring function ignores all of these fields.  
Detail pages and `score_composition.json` surface them for transparency.
