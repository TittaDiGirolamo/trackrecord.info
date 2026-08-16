# Logging Checklist
**Version:** 1.2  
**Date:** 2026-08-15  
**Status:** Active  
**Aligned with:** METHODOLOGY.md v0.9 (exact section references required in notes), CAPTURE.md, PROVENANCE.md, Problem & Vision Document v1.5

This checklist is the quality gate **before** a prediction is promoted into `predictions_v2.jsonl` as a pending record.  
It is topic-agnostic and intended to scale to any domain while preserving high verification standards.  
Nothing reaches the live dataset without an Overall **Pass**. Human review remains mandatory.  
All judgments must be recorded with explicit evidence; undefined or subjective terms are disallowed.

---

## Scoring Rules

| Score   | Meaning |
|---------|---------|
| **Pass**   | Fully meets the standard with no residual ambiguity on the dimension. |
| **Minor**  | Small, fully documented issue that does **not** affect verifiability, uniqueness, temporal integrity, source fidelity, or future resolvability. Maximum of **one** Minor allowed across the entire checklist for an Overall Pass. |
| **Fail**   | Material problem with identity, source fidelity, claim quality/resolvability, uniqueness, temporal integrity, or required provenance. |

**Overall judgment rules (strict):**
- Any **Fail** on dimensions 1, 2, 3, or 4 → Overall **Fail**
- Two or more **Minor** scores anywhere → Overall **Fail** (or “Request changes”)
- Only zero or one **Minor**, and no Fails on 1–4 → Overall may be **Pass**
- Probability Provenance (5) and Topic & Context (6) cannot alone produce an Overall Fail, but a Fail on either still requires notes and may block promotion if it affects resolvability.

**Mandatory recording:** Every score must be accompanied by concrete evidence or a quoted excerpt. “Appears adequate” or equivalent language is prohibited.

---

## Checklist (apply in this order)

### 1. Identity & Required Fields
- [ ] `statement_id` is present, follows the current ID scheme, and is unique within the dataset
- [ ] `original_statement` is present, clear, and contains sufficient detail to stand alone
- [ ] `forecaster` (or structured `author`) is correctly identified and disambiguated
- [ ] `statement_publication_date` is present, accurate (YYYY-MM-DD), and **precedes** any known or expected resolution event
- [ ] `statement_original_url` is present and resolves to the source
- [ ] `statement_topic` is assigned according to the current topic system; the topic-system version or definition used is recorded in notes
- [ ] `resolution_criteria` is present and written as an explicit, testable condition
- [ ] `statement_probability` is present and within 0.0–1.0
- [ ] `probability_method_id` is present and matches a defined method
- [ ] `probability_rationale` is present and has been **human-reviewed and accepted**
- [ ] `statement_original_url_archive` is present; the archive timestamp is after the publication date and the archived text matches the logged `original_statement`

**Score:** Pass / Minor / Fail  
**Notes:** (must quote any missing or discrepant field)

### 2. Source Fidelity
- [ ] Logged `original_statement` is a faithful representation of the source (no material distortion, selective omission that changes meaning, or added interpretation)
- [ ] Exact source span or verbatim quote of the claim is recorded in notes or in the record
- [ ] Any supporting context or snippet is faithful to the original
- [ ] Publication context (medium, audience, surrounding text if material) is correctly captured
- [ ] Archive link content matches the logged statement at the time of capture

**Score:** Pass / Minor / Fail  
**Notes:** (must include the exact quoted span used)

### 3. Claim Quality & Resolvability
- [ ] The claim is clear, specific, and falsifiable by publicly observable evidence
- [ ] An **explicit** time horizon or resolution event is stated in the claim or fully surfaced in `resolution_criteria` (purely “clearly implicit” is insufficient unless the implicit horizon is made explicit in the criteria and documented)
- [ ] `resolution_criteria` are objective, unambiguous, match the meaning of the original claim, and do not introduce new conditions
- [ ] The claim is a genuine prediction about a future state (not a value judgment, description of a current event, or non-falsifiable hedge)
- [ ] Temporal integrity holds: `statement_publication_date` precedes the resolution event defined by the criteria

**Score:** Pass / Minor / Fail  
**Notes:** (must state the explicit resolution condition used)

### 4. Uniqueness
- [ ] A search for existing records with the same or substantially overlapping claim by the same or closely related forecaster has been performed and the result recorded
- [ ] No existing record contains substantially the same claim by the same (or very similar) forecaster under comparable time context
- [ ] If a near-duplicate exists, a clear, documented justification is present that cites material difference in wording, date, probability, or context; the justification must be specific and auditable
- [ ] `statement_id` is unique **and** the combination of (forecaster + substantive content + time context) is unique

**Operational note:** “Substantially the same” is judged by whether a reasonable third party would consider the two claims interchangeable for scoring purposes. The reviewer must state the search scope used.

**Score:** Pass / Minor / Fail  
**Notes:** (must describe the search performed and any near-duplicates considered)

### 5. Probability Provenance & Consistency
- [ ] `probability_method_id` correctly identifies the method and version used
- [ ] `probability_rationale` has been human-reviewed and accepted (LLM draft origin is permitted only if final human approval is recorded)
- [ ] The assigned probability is consistent with the linguistic force and any numerical language in the original statement
- [ ] The reviewer has listed the specific linguistic markers, confidence language, or external anchors (if any) used to judge consistency

**How consistency is judged (required procedure):**
1. Extract and list the key force-carrying words or phrases (“will”, “almost certain”, “I expect”, “possible”, “unlikely”, “could”, numerical odds, ranges, etc.).
2. Note any explicit numerical confidence or market reference present in the original statement.
3. State whether the assigned probability is higher, lower, or aligned with that force, and why the chosen value is reasonable given the wording.
4. The test is transparency of reasoning and absence of clear contradiction with the text; perfect calibration is not required.

**Score:** Pass / Minor / Fail  
**Notes:** (must list the linguistic markers used)

### 6. Topic & Context
- [ ] `statement_topic` follows the current topic system (version recorded)
- [ ] `statement_context` provides the necessary background for later independent resolution and explains why the prediction was logged
- [ ] No material background required for understanding the claim is omitted

**Score:** Pass / Minor / Fail  
**Notes:**

### 7. Independence & Process Integrity (new mandatory gate)
- [ ] Reviewer has no material conflict of interest with the forecaster or the subject matter that would reasonably affect judgment
- [ ] Any LLM assistance used in drafting fields has been human-reviewed; the fact of assistance is noted if material
- [ ] The methodology version applied (METHODOLOGY.md v0.9 or later) is explicitly recorded

**Score:** Pass / Minor / Fail  
**Notes:**

---

## Overall Judgment

| Dimension                            | Score |
|--------------------------------------|-------|
| 1. Identity & Required Fields        |       |
| 2. Source Fidelity                   |       |
| 3. Claim Quality & Resolvability     |       |
| 4. Uniqueness                        |       |
| 5. Probability Provenance & Consistency |   |
| 6. Topic & Context                   |       |
| 7. Independence & Process Integrity  |       |
| **Overall**                          | **Pass / Fail** |

**One-line summary:**  
**Action:** Promote / Reject / Request changes  
**Methodology version applied:**  

---

## Recording Template

```markdown
### Candidate / statement_id
- Forecaster: 
- Claim (short): 
- Publication date: 
- Methodology version applied: 

| Dimension                            | Score | Notes (required evidence / quotes) |
|--------------------------------------|-------|------------------------------------|
| 1. Identity & Required Fields        |       |                                    |
| 2. Source Fidelity                   |       | Exact source span:                 |
| 3. Claim Quality & Resolvability     |       | Explicit resolution condition:     |
| 4. Uniqueness                        |       | Search performed:                  |
| 5. Probability Provenance & Consistency |   | Linguistic markers used:           |
| 6. Topic & Context                   |       |                                    |
| 7. Independence & Process Integrity  |       | Conflict declared: None / ...      |
| **Overall**                          |       |                                    |

Decision: Promote / Reject / Changes needed
```