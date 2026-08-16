# Resolution Checklist
**Version:** 1.2  
**Date:** 2026-08-15  
**Status:** Active  
**Aligned with:** METHODOLOGY.md v0.9 (exact section references required in notes), RESOLUTION_WORKFLOW.md, Problem & Vision Document v1.5

This checklist is the quality gate **before** an outcome is written and the record is marked resolved.  
It is topic-agnostic and designed to scale to any domain while preserving high verification standards.  
It is also the standard used for sample audits and any future quality reviews.  
All judgments must be recorded with explicit evidence; undefined or subjective terms are disallowed.  
Nothing is marked resolved without an Overall **Pass**.

---

## Scoring Rules

| Score   | Meaning |
|---------|---------|
| **Pass**   | Fully meets the standard with no residual ambiguity on the dimension. |
| **Minor**  | Small, fully documented wording or completeness issue that does **not** affect outcome correctness, evidence quality, or consistency with the original criteria. Maximum of **one** Minor allowed across the entire checklist for an Overall Pass. |
| **Fail**   | Material problem with outcome correctness, evidence quality, identity/completeness of the resolution, or consistency with the original record. |
| **N/A**    | Dimension does not apply (Special Cases only). |

**Overall judgment rules (strict):**
- Any **Fail** on dimensions 1, 2, 3, or 6 → Overall **Fail**
- Two or more **Minor** scores anywhere → Overall **Fail** (or “Correction needed”)
- Only zero or one **Minor**, and no Fails on 1–3 or 6 → Overall may be **Pass**
- Special Cases (5) and Transparency (4) Failures still require explicit notes and may block if they affect correctness or auditability.
- Target for sample audits: ≥ 95 % Overall Pass (sampling frame and method must be documented separately).

**Mandatory recording:** Every score must be accompanied by concrete evidence, exact quotes of criteria applied, and retrieval details. “Appears correct” language is prohibited.

---

## Checklist (apply in this order)

### 1. Identity & Completeness (of the resolution)
- [ ] `resolution_date` is present and accurate (YYYY-MM-DD)
- [ ] `outcome` is recorded (0.0 / 1.0 or valid partial score strictly according to current scoring rules)
- [ ] `outcome_proof` is present
- [ ] `outcome_verification_url` is present
- [ ] All core resolution fields required by the current schema are filled
- [ ] The methodology version applied is explicitly recorded

**Score:** Pass / Minor / Fail  
**Notes:** (list any missing fields)

### 2. Outcome Correctness *(highest bar)*
- [ ] The best available primary official source has been consulted; if none exists, the highest-quality secondary source is used and the reason for absence of a primary source is documented
- [ ] The recorded `outcome` correctly follows from the original `resolution_criteria` + the actual result
- [ ] Any ambiguity has been resolved in favour of the **stricter interpretation**
- [ ] The outcome remains faithful to the meaning of the original claim; no silent broadening or narrowing has occurred
- [ ] Temporal integrity: the original `statement_publication_date` precedes the resolution event

**Definition of “stricter interpretation” (binding):**  
The reading of the claim or criteria that imposes the higher bar for the prediction to be scored as correct (i.e., the interpretation under which it is harder for the forecaster to be judged right). When two readings are equally plausible, the stricter one is selected and the choice is documented.

**Score:** Pass / Minor / Fail  
**Notes:** (must quote the exact resolution criteria text applied and the key evidence)

### 3. Evidence Quality
- [ ] `outcome_proof` clearly states what happened and why the outcome follows from the criteria (no unsupported leaps)
- [ ] `outcome_verification_url` points to a primary/official source whenever one exists; retrieval date/time is recorded
- [ ] A third party with ordinary domain competence can independently verify the outcome from the provided evidence without additional research beyond the cited sources
- [ ] If secondary sources are used, their relationship to the primary facts is explained

**Score:** Pass / Minor / Fail  
**Notes:** (include retrieval timestamps)

### 4. Transparency & Rationale
- [ ] The resolution decision is clearly explained in plain language
- [ ] For compound or multi-part predictions: the status of each major sub-claim is explicitly stated
- [ ] Any LLM assistance used in drafting the resolution text has been human-reviewed; the fact and scope of assistance is disclosed
- [ ] The exact methodology section(s) applied (especially scoring rules) are cited

**Score:** Pass / Minor / Fail  
**Notes:**

### 5. Special Cases
- [ ] Exact or highly specific predictions are scored strictly according to the stated criteria (no charitable reading)
- [ ] Compound / conjunctive / exact-set predictions follow the logical rules defined in the methodology (currently: all-or-nothing per METHODOLOGY.md §2). Use of partial scoring on a compound claim is a **Fail** unless an explicit, documented exception citing the methodology is present
- [ ] Partial scoring (when legitimately applicable under current rules) is applied consistently and the rule version is cited
- [ ] Any other special handling is fully documented

**Score:** Pass / Minor / Fail / N/A  
**Notes:** (must state whether the claim is compound and how scoring was applied)

### 6. Consistency with Original Record
- [ ] The resolution respects the original `resolution_criteria` exactly (no silent reinterpretation or addition of new conditions)
- [ ] No retroactive change has been made to the original statement, criteria, probability, or other logged fields
- [ ] The resolution does not import later statements, retractions, or self-assessments by the forecaster as evidence of the original claim’s meaning

**Score:** Pass / Minor / Fail  
**Notes:** (quote original criteria if material)

### 7. Independence & Process Integrity (new mandatory gate)
- [ ] Reviewer has no material conflict of interest with the forecaster, the subject matter, or the outcome that would reasonably affect judgment
- [ ] Resolution is independent of any post-statement commentary by the original forecaster
- [ ] Methodology version applied is recorded

**Score:** Pass / Minor / Fail  
**Notes:** (Conflict declared: None / description)

---

## Overall Judgment

| Dimension                         | Score |
|-----------------------------------|-------|
| 1. Identity & Completeness        |       |
| 2. Outcome Correctness            |       |
| 3. Evidence Quality               |       |
| 4. Transparency & Rationale       |       |
| 5. Special Cases                  |       |
| 6. Consistency with Original      |       |
| 7. Independence & Process Integrity |     |
| **Overall**                       | **Pass / Fail** |

**One-line summary:**  
**Correction needed (if any):**  
**Methodology version applied:**  

---

## Recording Template

```markdown
### `statement_id`
- Forecaster: 
- Topic: 
- Recorded outcome: 
- Resolution date: 
- Methodology version applied: 

| Dimension                         | Score | Notes (required evidence / quotes / timestamps) |
|-----------------------------------|-------|-------------------------------------------------|
| 1. Identity & Completeness        |       |                                                 |
| 2. Outcome Correctness            |       | Exact criteria applied:                         |
|                                   |       | Key evidence:                                   |
|                                   |       | Stricter interpretation choice (if any):        |
| 3. Evidence Quality               |       | Retrieval date/time of primary source:          |
| 4. Transparency & Rationale       |       | LLM assistance disclosed:                       |
| 5. Special Cases                  |       | Compound? Scoring rule applied:                 |
| 6. Consistency with Original      |       |                                                 |
| 7. Independence & Process Integrity |     | Conflict declared: None / ...                   |
| **Overall**                       |       |                                                 |

Decision: Accept resolution / Correction needed
```