# Trackrecord.info Methodology

**Version:** 0.9  
**Effective Date:** 2026-07-16  
**Status:** Active (aligned with Vision Document v1.5 and 90-Day Action Plan v1.0)

## 1. Core Principles

Trackrecord.info is governed by five non-negotiable principles:

- **Verifiability** — Every prediction, resolution, and score must be traceable to a public source and a deterministic outcome.
- **Independence** — Scoring ignores the forecaster’s identity, reputation, or past performance.
- **Granularity** — Predictions are evaluated at the finest level of specificity provided.
- **Transparency** — The full resolution rationale for each prediction is recorded and published.
- **No Retroactive Adjustment** — Once logged and resolved, a prediction’s outcome and score are immutable except for factual corrections to the original source.

## 2. Handling of Compound and Conjunctive Predictions

Some predictions combine multiple claims using “and”, “or”, or similar logical connectors (e.g., “Netherlands tops Group F **and** reaches at least the quarterfinals”).

**Policy:**
- Conjunctive claims (“A **and** B”) are evaluated as a single statement. The prediction is considered correct only if **all** sub-claims are true.
- If any sub-claim is false, the overall prediction is scored as incorrect (0).
- Disjunctive claims (“A **or** B”) are generally avoided. When they appear, they are scored as correct if at least one sub-claim holds, unless the original statement clearly intends a different interpretation.
- Forecasters and extractors are encouraged to decompose compound predictions into separate atomic predictions when the source material allows it. This improves analytical value and reduces ambiguity.

**Rationale transparency:**  
When resolving a compound prediction, the `resolution_rationale` must explicitly state the status of each major sub-claim, even though only one overall score is recorded for the prediction.

This policy prioritizes fidelity to the original statement while maximizing learning from errors.

## 3. Prediction Logging Rules

A prediction is eligible for tracking only if it satisfies all of the following:

1. Publicly verifiable (tweet, article, podcast transcript, or official forecast with timestamp).
2. Clear, falsifiable claim about a future event or measurable outcome.
3. Explicit or implicit time horizon.
4. Forecaster explicitly named and source archived.

**Exclusions**: Vague/hedged statements, predictions without a defined resolution date or event, and post-hoc reinterpretations.

## 4. The 0–100 Accuracy Score

### 4.1 Normalization Formula
Score = 100 × (1 − |Predicted_Value − Actual_Value| / Range)

### 4.2 Category-Specific Scoring Rules

| Category              | Rule |
|-----------------------|------|
| **Binary / Yes-No**   | Correct → 100; Incorrect → 0 |
| **Ranked / Ordered**  | Position score = 100 × (1 − \|Predicted_Rank − Actual_Rank\| / Max_Rank) |
| **Probabilistic**     | Brier Score mapped to 0–100 |
| **Range / Interval**  | 100 if outcome inside interval; linear decay outside |

### 4.3 Topic / Circle-of-Competence Scoring

In addition to overall accuracy, we calculate **subject-specific (topic) accuracy** where sufficient data exists (minimum 5 resolved predictions in a topic for meaningful display).

- Topics are defined hierarchically in the `statement_topic` field (e.g., “FIFA World Cup 2026 - England Performance - Group Stage”).
- Overall score remains the primary metric.
- Per-topic scores are displayed on forecaster cards, filtered views, and full track records when data volume justifies it.
- Interpretation: High performance in one domain does not imply skill in others. This reveals true expertise boundaries (circles of competence).

We only display per-topic scores publicly when statistically meaningful. Otherwise: “Insufficient data for topic breakdown.”

## 5. Human-Reviewed Resolution Process

All resolutions follow this process:

1. Mark prediction as “Pending Resolution” with expected resolution date.
2. On/after the resolution date, query primary source(s).
3. Human reviewer confirms outcome using official sources.
4. Append resolution record to `predictions.jsonl` with:
   - Original prediction + source + timestamp
   - Actual outcome + source + timestamp
   - Resolution rationale (1–3 sentences)
   - Final score
5. Regenerate public reports.

**Gold Standard vs Public Predictions**:
- **Gold Standard** records (`gold_standard/wc2026/`) are manually created high-fidelity examples used for prompt development and calibration.
- **Public predictions** (`predictions.jsonl`) are real-world forecasts made by identifiable individuals that are resolved through the human-reviewed process above.

### 5.1 LLM-Assisted Resolution with Human-in-the-Loop

To efficiently resolve large volumes of overdue predictions while maintaining the project’s strict standards of accuracy, verifiability, and accountability, a hybrid workflow is supported.

**LLM Draft Phase (optional)**  
An LLM, guided by a controlled and versioned prompt from `prompts/resolution_draft_v*.md`, may generate draft proposals for `outcome`, `outcome_proof`, `outcome_verification_url`, and `rationale`. Drafts must be based strictly on the provided `resolution_criteria` and available source materials.

**Human Verification & Approval Phase (mandatory)**  
The human resolver must:
- Access primary/official sources directly (FIFA, official match reports, etc.).
- Validate or correct the LLM’s interpretation of the `resolution_criteria`.
- Confirm or revise the proposed `outcome` (including any application of `scoring_rules.md` or `apply_partial_scoring.py`).
- Ensure `outcome_proof` and `outcome_verification_url` are accurate and point to authoritative sources.
- Approve or rewrite the final 1–3 sentence rationale.

**Documentation**  
Every resolution session Markdown file must explicitly record:
- Whether LLM assistance was used for that record.
- The model and prompt version used.
- Any material differences between the LLM draft and the final human-approved values.
- Confirmation that the human resolver personally verified the primary sources.

This hybrid approach does **not** change any core principles of the project. The LLM functions only as a productivity tool for drafting and research acceleration. The named human resolver remains fully accountable for every resolved record.

## 6. Data Storage Format (`predictions.jsonl`)

Each record contains the fields defined in `schema/prediction_schema.py`, including (but not limited to):
- `id`, `forecaster`, `prediction_text`, `source_url`, `source_timestamp`
- `predicted_value`, `resolution_date`, `actual_value`, `resolution_source`
- `resolution_rationale`, `score`, `status`

## 7. Gold Standard Reference Dataset

The gold standard dataset (`gold_standard/wc2026/`) serves as:
- Verified reference set for automated extraction pipelines
- Objective evaluation of LLM prompts
- Transparent foundation for calibration

All gold standard records follow the `Gold_Record_Creation_Checklist.md` and are validated against `prediction_schema.py`.

## 8. Scope (Aligned with Vision Document v1.5)

**Current Focus (Phase 1)**: FIFA World Cup 2026 predictions from **English-language sources** only (major outlets, analysts, and quantitative models).

The previous temporary Oranje/Dutch focus (v0.7) is superseded by the broader English-language scope defined in Vision Document v1.5.

## 9. Version History

- **v0.7 (2026-06-04)**: Temporary Oranje focus
- **v0.8 (2026-06-09)**: Aligned with Vision Document v1.5 (English WC2026 focus). Clarified gold standard vs public prediction workflows. Updated scope and references.
- **v0.9 (2026-07-16)**: Added hybrid LLM-assisted resolution with mandatory human oversight (Section 5.1). Introduced `prompts/resolution_draft_v*.md` and updated documentation requirements for LLM usage.

## 10. Governance

All changes to this methodology must be version-controlled, include a clear delta, and be validated against the Problem & Vision Document v1.5.

## 11. Statistical Foundations and Guardrails

To support credible long-term use, the following statistical principles guide how scores are calculated, displayed, and interpreted:

- **Sample size requirements**: Overall forecaster scores are only shown when a minimum number of resolved predictions exists (currently under review; topic-level scores require at least 5 resolved predictions).
- **Uncertainty and small samples**: Scores based on small numbers of predictions are inherently uncertain. Future versions will display confidence intervals or use shrinkage methods for low-volume forecasters.
- **Topic-specific scoring**: Performance is broken down by topic (“circle of competence”) only when sufficient data exists. Topics with very few resolutions are not displayed to avoid misleading conclusions.
- **Calibration analysis**: The system will increasingly support calibration diagnostics (how well predicted probabilities match observed frequencies). These will be published alongside accuracy metrics.
- **Avoidance of gaming**: Scoring rules are designed to penalize overconfidence and vague or compound claims. Predictions are evaluated strictly according to their stated resolution criteria.
- **No retroactive adjustment**: Once a prediction is resolved and scored, the outcome and score are considered final except in cases of clear factual error in the original source or resolution.

These guardrails exist to prevent over-interpretation of limited data and to maintain the integrity of comparisons across forecasters.

## 12. Interpretation of Scores and Known Limitations

Scores on Trackrecord.info should be interpreted with the following considerations:

**What scores represent:**
- A measure of accuracy on the specific set of publicly made predictions that have been logged and resolved.
- Topic-specific insight into areas where a forecaster has demonstrated relative strength or weakness.

**What scores do not represent:**
- A complete or definitive measure of a person’s forecasting ability.
- A guarantee of future performance.
- A judgment on the forecaster’s character, expertise, or overall credibility.
- A statistically robust ranking when sample sizes are small.

**Known limitations:**
- Many predictions currently tracked are binary or low-granularity. Probabilistic predictions (with explicit probabilities) allow for more powerful evaluation using proper scoring rules.
- Small sample sizes limit statistical confidence. Interpretations should remain cautious until larger datasets are available.
- The system currently focuses on English-language sources for WC2026. Broader language and topic coverage is planned for future phases.

---

*This document is version-controlled. All changes must be proposed via pull request with clear justification.*
