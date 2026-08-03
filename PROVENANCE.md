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

## Probability rationale (required since 2026-08)

Every newly promoted prediction **must** contain a short plain-English paragraph that explains *why* the chosen probability was assigned.

Field name: `probability_rationale`

Requirements:
- 2–4 sentences
- Reference the original wording / strength of language
- Mention any external context used (e.g. market odds) if relevant
- Note any caveats
- Must be written by a human reviewer (never auto-generated without review)

Example:
“Sutton makes a clear, repeated directional claim (‘I’ve gone for France… I am not going to change my mind now’). No numerical odds are given. Pre-tournament market implied probability for France was ~15–18 %. 0.22 sits slightly above the market while remaining conservative for a qualitative pick.”

This field is surfaced on detail pages and in `score_composition.json` for full inspectability.

## Schema fields

| Field                       | Type     | Purpose |
|-----------------------------|----------|---------|
| `probability_method_id`     | string   | Stable ID of the exact method/version |
| `probability_source`        | string   | Original text snippet or reference |
| `probability_generated_at`  | string   | ISO-8601 timestamp |
| `probability_model`         | string   | Model name/version (LLM methods) |
| `probability_prompt_hash`   | string   | Content hash of the prompt template |
| `probability_seed`          | integer  | RNG seed if stochastic |
| `probability_rationale`     | string   | Short human-written justification of the chosen probability |

The scoring function ignores all of these fields.  
Detail pages and `score_composition.json` surface them for transparency.
