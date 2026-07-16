# Requirements Specification: Resolution of Predictions with `resolution_date` ≤ 2026-07-16 (Overdue / Due Today)

**Version:** 1.1 (Hybrid LLM-assisted with Human-in-the-Loop)  
**Date:** 2026-07-16  
**Applies to:** All `PredictionRecord` entries in `predictions_v2.jsonl` (and analogously gold-standard records) where `resolution_date` ≤ 2026-07-16 and `outcome` is null/unresolved.  
**References:** `METHODOLOGY.md`, `prediction_schema.py`, `scoring_rules.md`, `apply_partial_scoring.py`, existing `resolution_sessions/*.md`

### 1. Purpose
Define the mandatory requirements for **human-reviewed resolution** of overdue or due-today predictions, with optional LLM assistance for drafting. This ensures every prediction is evaluated against real-world outcomes using verifiable primary sources, maintains full transparency and auditability, applies consistent scoring, and updates all public artifacts without retroactive changes.

### 2. Scope
Same as original (predictions in `predictions_v2.jsonl` with `resolution_date` ≤ 2026-07-16 and unresolved).

### 3. Definitions
- **resolution_date**: The date by which the underlying event is expected to be resolvable.
- **Resolved**: A record has a non-null `outcome` (float 0.0–1.0), supporting evidence fields populated, and has been through the human-reviewed process.
- **Primary sources**: Official FIFA results, brackets, match reports, and FIFA-sourced tables (preferred).
- **Outcome value**: 1.0 = event occurred / prediction correct; 0.0 = event did not occur / incorrect. Fractional values permitted only when tiered partial scoring is explicitly applied.
- **Rationale**: 1–3 sentence human explanation of how the `resolution_criteria` evaluated against the actual outcome.
- **Human-reviewed only**: No fully automated resolution. Every outcome requires human confirmation and approval.
- **LLM-assisted resolution**: A hybrid process in which a large language model generates *draft* proposals for `outcome`, `outcome_proof`, `outcome_verification_url`, and `rationale`. These drafts are always treated as untrusted suggestions. A human resolver must independently verify primary sources, review/edit the drafts, and explicitly approve the final values before any record is updated in `predictions_v2.jsonl`. The human resolver remains fully accountable.

### 4. Functional Requirements (FR)

**FR-01 – Identification**  
All qualifying records must be identified by filtering `predictions_v2.jsonl` for `resolution_date` ≤ '2026-07-16' **AND** `outcome` is null.

**FR-02 – Source Verification**  
For every prediction, the **human resolver** (optionally assisted by LLM for initial source identification and draft generation) must query **and personally verify** primary/official sources on or after the `resolution_date` and confirm whether the event described in `resolution_criteria` occurred.

**FR-03 – Outcome Assignment**  
Assign a numeric `outcome` (0.0–1.0) that reflects whether the prediction’s event materialized according to the stated `resolution_criteria`.

**FR-04 – Evidence Population**  
Populate `outcome_proof` and `outcome_verification_url` for every resolved record.

**FR-05 – No Retroactive Adjustment**  
Once a record is resolved and committed, its `outcome`, `outcome_proof`, and `outcome_verification_url` are immutable except for purely factual corrections.

**FR-06 – Batch Processing**  
Resolutions must be performed and documented in coherent batches.

**FR-07 – Artifact Regeneration**  
After updating `predictions_v2.jsonl`, the public tables must be regenerated using `scripts/generate_prediction_tables.py`.

**FR-08 – LLM Assistance with Mandatory Human Oversight (Optional)**  
LLM tools may be used to accelerate resolution by generating draft proposals.  
**Mandatory safeguards**:
- All LLM output is treated as a draft only.
- The human resolver must independently access and personally verify primary sources.
- The human resolver must review, edit if necessary, and **explicitly approve** every field.
- Use of LLM assistance (model + prompt version) **must** be disclosed in the batch documentation.
- No record may be committed based solely on LLM output without documented human review and approval.

### 5. Data / Field Requirements
Same as original.

### 6. Process / Workflow Requirements

1. **Preparation** — Review `METHODOLOGY.md`, `scoring_rules.md`, and prior resolution session files.
2. **Batch Documentation** — Create `resolution_sessions/2026-07-16_batchXX.md`.
3. **Optional LLM Draft Generation** — When using LLM assistance: Use a controlled prompt from `prompts/resolution_draft_vX.md`. Review LLM output for hallucinations before human verification.
4. **Resolution Execution** — For each record: **Human reviews any LLM-proposed draft** → personally verifies the outcome against `resolution_criteria` using primary sources → edits/corrects the draft as needed → assigns final `outcome` → writes/approves `outcome_proof` + `outcome_verification_url` → records the final rationale (noting LLM assistance if used).
5. **Data Update** — Update the corresponding records in `predictions_v2.jsonl`.
6. **Scoring** — Apply scoring rules.
7. **Regeneration** — Run the table generation script.
8. **Commit & Publish** — Commit with clear message.
9. **Verification** — Confirm updated tables on the live site.

### 7. Documentation & Artifact Requirements
Same as original + new files created in this process.

### 8. Scoring Requirements
Same as original.

### 9. Quality Assurance & Audit Requirements
Every batch **must** complete the self-audit checklist.  
**Additional checklist items when LLM assistance is used**:
- [ ] If LLM assistance was used: the human resolver independently verified primary sources and explicitly approved the final values. LLM usage is fully disclosed.
- [ ] No record was committed based solely on LLM output without human review and approval.

### 10. Constraints & Non-Functional Requirements
**Hybrid human-in-the-loop resolution** — Fully automated resolution and LLM-only resolution (without mandatory human review, primary source verification by the human, and explicit approval) are **not permitted**. LLM assistance is explicitly allowed for drafting, **provided that** a qualified human resolver always personally verifies primary sources, reviews/corrects drafts, explicitly approves every record, and documents LLM usage transparently.

The human resolver retains full accountability at all times.
