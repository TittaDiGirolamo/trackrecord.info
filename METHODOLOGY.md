# Trackrecord.info — Methodology (v0.6)
**Document Version**: 1.0
**Effective Date**: 2026-06-01
**Scope**: This document defines the precise rules, scoring system, and resolution procedures used by Trackrecord.info. All claims of accuracy are derived exclusively from these rules.

## 1. Core Principles
Trackrecord.info operates under the following non-negotiable principles:
- **Verifiability**: Every prediction, resolution, and score must be traceable to a public source and a deterministic outcome.
- **Independence**: Scoring is performed without regard to the identity, reputation, or prior performance of the forecaster.
- **Granularity**: Predictions are evaluated at the finest level of specificity provided by the forecaster.
- **Transparency**: The full resolution rationale for every prediction is recorded and published.
- **No Retroactive Adjustment**: Once a prediction is logged and resolved, its outcome and score are immutable except for correction of factual errors in the original source material.

## 2. Prediction Logging Rules
A prediction is eligible for tracking only when it meets all of the following criteria:
1. The statement is **publicly verifiable** (tweet, article, podcast transcript, or official forecast with timestamp).
2. The prediction contains a **clear, falsifiable claim** about a future event or measurable outcome.
3. The prediction includes an **implicit or explicit time horizon** (e.g., “by end of 2025”, “in the 2025 NBA Draft”).
4. The forecaster is explicitly named and the source is archived.

**Exclusions**:
- Vague or hedged statements (“I think it’s possible…”)
- Predictions without a defined resolution date or event
- Post-hoc reinterpretations of earlier statements

## 3. The 0–100 Accuracy Score
### 3.1 Normalization Formula
All predictions are scored on a continuous 0–100 scale using the following base formula:
Score = 100 × (1 − |Predicted_Value − Actual_Value| / Range)
textWhere:
- `Predicted_Value` = the numeric or categorical value asserted by the forecaster
- `Actual_Value` = the verified real-world outcome
- `Range` = the maximum possible deviation for that prediction type (defined per category below)

### 3.2 Category-Specific Scoring Rules
#### A. Binary / Yes-No Predictions
- Correct resolution → **100**
- Incorrect resolution → **0**
- Partial credit may be awarded only when the original statement explicitly allows for degrees of correctness (rare).

#### B. Ranked or Ordered Predictions (e.g., Draft Order, Top-10 Lists)
- Score is calculated as the average of per-position accuracy:
Position_Score = 100 × (1 − |Predicted_Rank − Actual_Rank| / Max_Rank)
text- Overall score = arithmetic mean of all position scores.

#### C. Probabilistic or Percentage Predictions
- Brier Score transformation is applied and then linearly mapped to the 0–100 scale:
Brier = (Forecast_Probability − Outcome)^2
Score = 100 × (1 − Brier)
text#### D. Range or Interval Predictions
- Full credit (100) if actual outcome falls inside the stated interval.
- Linear decay outside the interval up to a defined outer bound.

### 3.3 Minimum Sample Requirement
Individual forecaster scores are published only when **at least one resolved prediction** exists. Aggregate scores across all forecasters require a minimum of three resolved predictions.

## 4. Resolution Engine v0.6
### 4.1 Resolution Sources (in priority order)
1. Official final statistics (e.g., NBA.com, NCAA, government election results)
2. Authoritative secondary sources (ESPN, The Athletic, Reuters)
3. Direct confirmation from the forecaster (screenshot or public statement)

### 4.2 Resolution Process
1. Prediction is marked “Pending Resolution” with expected resolution date.
2. On or after the resolution date, the system queries the primary source.
3. A human reviewer (or automated script in v0.7+) confirms the outcome.
4. The resolution record is appended to `predictions.jsonl` with:
 - Original prediction text + source URL + timestamp
 - Actual outcome + source URL + timestamp
 - Resolution rationale (1–3 sentences)
 - Final score
5. All metrics are recalculated and the public report is regenerated.

### 4.3 Edge Cases Handled in v0.6
- **Prediction never resolved**: Remains “Unresolved” indefinitely; does not affect scores.
- **Ambiguous outcome**: Resolution is deferred until authoritative clarification is published.
- **Forecaster correction**: If the forecaster publicly corrects their own prediction before resolution, the corrected version is used (original is preserved for audit).

## 5. Data Storage Format
All predictions are stored in `predictions.jsonl` (newline-delimited JSON). Each record contains the following mandatory fields:
```json
{
"id": "string (UUID)",
"forecaster": "string",
"prediction_text": "string",
"source_url": "string",
"source_timestamp": "ISO-8601",
"topic_tags": ["string"],
"predicted_value": "number | string | object",
"resolution_date": "ISO-8601 | null",
"actual_value": "number | string | object | null",
"resolution_source": "string | null",
"resolution_rationale": "string | null",
"score": "number (0-100) | null",
"status": "logged | resolved | unresolved"
}
6. Audit and Reproducibility
Any third party can reproduce all scores by:

Cloning the repository
Executing the open-source resolution script (to be released in v0.7)
Comparing output against the published resolution_report_v0.6.md

Discrepancies are logged as GitHub issues and resolved according to the correction protocol above.
7. Limitations (Explicitly Acknowledged)

Current sample size is small (3 resolved predictions). Scores are therefore sensitive to individual outcomes.
Topic coverage is currently narrow (primarily sports and elections). Expansion is planned.
No inter-rater reliability study has yet been performed on resolution decisions.

These limitations are disclosed in every public report.

Document Control
Author: Trackrecord.info Maintainer
Review Cycle: Every major version release
Next Review: v0.7 release
This methodology is subject to revision only through documented, versioned updates.
