# Trackrecord.info Methodology

**Version:** 0.8  
**Effective Date:** 2026-06-09  
**Status:** Active (aligned with Vision Document v1.5 and 90-Day Action Plan v1.0)

## 1. Core Principles

Trackrecord.info is governed by five non-negotiable principles:

- **Verifiability** — Every prediction, resolution, and score must be traceable to a public source and a deterministic outcome.
- **Independence** — Scoring ignores the forecaster’s identity, reputation, or past performance.
- **Granularity** — Predictions are evaluated at the finest level of specificity provided.
- **Transparency** — The full resolution rationale for each prediction is recorded and published.
- **No Retroactive Adjustment** — Once logged and resolved, a prediction’s outcome and score are immutable except for factual corrections to the original source.

## 2. Prediction Logging Rules

A prediction is eligible for tracking only if it satisfies all of the following:

1. Publicly verifiable (tweet, article, podcast transcript, or official forecast with timestamp).
2. Clear, falsifiable claim about a future event or measurable outcome.
3. Explicit or implicit time horizon.
4. Forecaster explicitly named and source archived.

**Exclusions**: Vague/hedged statements, predictions without a defined resolution date or event, and post-hoc reinterpretations.

## 3. The 0–100 Accuracy Score

### 3.1 Normalization Formula
Score = 100 × (1 − |Predicted_Value − Actual_Value| / Range)
text### 3.2 Category-Specific Scoring Rules

| Category              | Rule |
|-----------------------|------|
| **Binary / Yes-No**   | Correct → 100; Incorrect → 0 |
| **Ranked / Ordered**  | Position score = 100 × (1 − \|Predicted_Rank − Actual_Rank\| / Max_Rank) |
| **Probabilistic**     | Brier Score mapped to 0–100 |
| **Range / Interval**  | 100 if outcome inside interval; linear decay outside |

## 4. Human-Reviewed Resolution Process

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

## 5. Data Storage Format (`predictions.jsonl`)

Each record contains the fields defined in `schema/prediction_schema.py`, including (but not limited to):
- `id`, `forecaster`, `prediction_text`, `source_url`, `source_timestamp`
- `predicted_value`, `resolution_date`, `actual_value`, `resolution_source`
- `resolution_rationale`, `score`, `status`

## 6. Gold Standard Reference Dataset

The gold standard dataset (`gold_standard/wc2026/`) serves as:
- Verified reference set for automated extraction pipelines
- Objective evaluation of LLM prompts
- Transparent foundation for calibration

All gold standard records follow the `Gold_Record_Creation_Checklist.md` and are validated against `prediction_schema.py`.

## 7. Scope (Aligned with Vision Document v1.5)

**Current Focus (Phase 1)**: FIFA World Cup 2026 predictions from **English-language sources** only (major outlets, analysts, and quantitative models).

The previous temporary Oranje/Dutch focus (v0.7) is superseded by the broader English-language scope defined in Vision Document v1.5.

## 8. Version History

- v0.7 (2026-06-04): Temporary Oranje focus
- **v0.8 (2026-06-09)**: Aligned with Vision Document v1.5 (English WC2026 focus). Clarified gold standard vs public prediction workflows. Updated scope and references.

## 9. Governance

All changes to this methodology must be version-controlled, include a clear delta, and be validated against the Problem & Vision Document v1.5.

---

**Trackrecord.info — Building transparent accountability for public predictions from a clean, integrity-first foundation.**
