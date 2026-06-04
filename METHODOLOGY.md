# Trackrecord.info — Methodology (v0.7)

**Document Version**: 0.7  
**Effective Date**: 2026-06-04  
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

```
Score = 100 × (1 − |Predicted_Value − Actual_Value| / Range)
```

Where:
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
  ```
  Position_Score = 100 × (1 − |Predicted_Rank − Actual_Rank| / Max_Rank)
  ```
- Overall score = arithmetic mean of all position scores.

#### C. Probabilistic or Percentage Predictions
- Brier Score transformation is applied and then linearly mapped to the 0–100 scale:
  ```
  Brier = (Forecast_Probability − Outcome)^2
  Score = 100 × (1 − Brier)
  ```

#### D. Range or Interval Predictions
- Full credit (100) if actual outcome falls inside the stated interval.
- Linear decay outside the interval up to a defined outer bound.

### 3.3 Minimum Sample Requirement
Individual forecaster scores are published only when **at least one resolved prediction** exists. Aggregate scores across all forecasters require a minimum of three resolved predictions.

## 4. Resolution Engine v0.7
### 4.1 Resolution Sources (in priority order)
1. Official final statistics (e.g., FIFA, KNVB, official match reports)
2. Authoritative secondary sources (Voetbal International, NOS, Reuters, The Athletic)
3. Direct confirmation from the forecaster (screenshot or public statement)

### 4.2 Resolution Process
1. Prediction is marked “Pending Resolution” with expected resolution date.
2. On or after the resolution date, the system queries the primary source.
3. A human reviewer confirms the outcome.
4. The resolution record is appended to `predictions.jsonl` with:
   - Original prediction text + source URL + timestamp
   - Actual outcome + source URL + timestamp
   - Resolution rationale (1–3 sentences)
   - Final score
5. All metrics are recalculated and the public report is regenerated.

### 4.3 Edge Cases Handled in v0.7
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
```

## 6. Audit and Reproducibility
Any third party can reproduce all scores by:

1. Cloning the repository
2. Reviewing the public `predictions.jsonl` and resolution records
3. Comparing output against the published resolution reports

Discrepancies are logged as GitHub issues and resolved according to the correction protocol above.

## 7. Limitations (Explicitly Acknowledged)
- Current sample size is small. Scores are therefore sensitive to individual outcomes.
- Topic coverage is currently focused on football (primarily Dutch national team and Eredivisie-related predictions during the temporary sprint).
- No inter-rater reliability study has yet been performed on resolution decisions.

These limitations are disclosed in every public report.

## 8. Temporary Scope – FIFA World Cup 2026 Oranje Focus (v0.9 Sprint)
**Effective**: 2026-06-04 until re-evaluation on **2026-08-01**

For the duration of this sprint, Trackrecord.info is temporarily narrowing its active tracking to prominent **Dutch voices and experts** making public predictions about:
- The Netherlands national team (Oranje) performance and outcomes during the FIFA World Cup 2026.
- Related Dutch football topics where relevant.

**Rationale**:
- Leverages high current interest in Dutch football ahead of and during the World Cup.
- Increases relevance and potential sign-up conversion from the founder’s local Dutch network (Amersfoort / Netherlands).
- Maintains full methodological transparency while testing event-driven scope narrowing.

**Current Forecasters Being Tracked (v0.9)**:
1. **Wesley Sneijder** – Dutch football legend and former Netherlands international. High public profile and frequent media commentary on Oranje.
2. **Süleyman Öztürk** (Voetbal International) – Experienced football journalist and columnist with deep knowledge of Dutch and international football.
3. **Bas van den Hoven** (Voetbal International) – Journalist focused on English and Spanish football with regular Oranje coverage.
4. **Joachim Klement** – Economist and quantitative modeler known for long-running World Cup prediction models.
5. **Finley Crebolder** (Clockwork Oranje) – Specialist Dutch national team analyst and podcaster.
6. **Michael Statham** (@EredivisieMike) – Dutch football expert and commentator with strong Eredivisie and Oranje coverage.

**Predictor Selection Criteria** (applied for this sprint):
- Public visibility and credibility within Dutch football discourse.
- Regular production of verifiable, falsifiable predictions about Oranje or World Cup outcomes.
- Accessibility of source material (X/Twitter, Voetbal International, podcasts, interviews).
- Diversity of perspectives (former player, journalists, quantitative modeler, specialist analysts).

**Reversion Plan**:
- On or before **2026-08-01**, the scope will be formally re-evaluated.
- Options include: full reversion to broader international forecasters, continuation of Dutch focus, or hybrid model.
- Any permanent change will be documented in a new methodology version with full rationale.

This temporary scope does **not** alter the core scoring rules or principles defined in sections 1–7. It only changes which forecasters and predictions are actively monitored and displayed on the landing page during the sprint period.

## Document Control
**Author**: Trackrecord.info Maintainer  
**Review Cycle**: Every major version release  
**Next Review**: Post World Cup 2026 re-evaluation (2026-08-01 or earlier)  

This methodology is subject to revision only through documented, versioned updates published in this repository.

---

**Changelog v0.7 (2026-06-04)**  
- Added Section 8: Temporary Scope – FIFA World Cup 2026 Oranje Focus  
- Listed current 6 forecasters with selection rationale  
- Updated Effective Date and version  
- Minor clarifications to Resolution Sources for football context  
- Preserved all original principles and rules from v0.6
