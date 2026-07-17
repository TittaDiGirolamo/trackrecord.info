**Trackrecord.info — Overdue Predictions Resolution Requirements**
**Version:** 1.1
**Date:** 2026-07-17
**Status:** Ready for review / implementation only after FR-01 identification output is embedded
**Supersedes:** v1.0 (2026-07-16)
**Author of revisions:** Independent critical review against project principles
**Related Documents:**
- `METHODOLOGY.md` (current version governing hybrid resolution; treat as ≥ v0.9 for LLM formalisation)
- `scoring_rules.md`
- `schema/prediction_schema.py`
- `predictions_v2.jsonl` (single source of truth)
- Existing resolution session convention (`resolution_sessions/YYYY-MM-DD_batchXX.md`)
- `CHANGELOG.md`
---
### Changes from v1.0 (Transparency Record)
- Removed all unverified quantitative claims (“100 records”, “~86 overdue”). Exact counts must be produced by the FR-01 identification script and embedded before any resolution work begins.
- Corrected methodology version references and aligned with hybrid process formalisation.
- Enforced existing batch naming convention (`YYYY-MM-DD_batchXX.md`).
- Strengthened granularity language: no rationale templating permitted without explicit per-record justification in the session log.
- Clarified schema field handling: only fields validated by `prediction_schema.py` may be written to `predictions_v2.jsonl`. Detailed rationales that exceed schema fields are stored exclusively in the session log.
- Added mandatory recording of methodology version, scoring_rules version, and source snapshot context.
- Removed promotional / demonstrative language.
- Added pre-commit validation and immutability technical controls.
- Tightened edge-case handling and out-of-scope boundaries.
- Made Phase 0 a hard gate on verified data.
---
## 1. Executive Summary / Purpose
Trackrecord.info systematically logs, resolves, and scores public predictions to create transparent accuracy records.
As of the effective date of this specification, a non-trivial number of records in `predictions_v2.jsonl` have `resolution_date` ≤ 2026-07-16 and lack a populated `outcome`. The exact count and identity of these records are **unknown until the identification script defined in FR-01 is executed**.
This document defines the complete, auditable requirements for resolving every such overdue prediction while remaining in strict compliance with the project’s core principles (Verifiability, Independence, Granularity, Transparency, No Retroactive Adjustment).
**Project Goal**: Resolve 100 % of the overdue set identified by FR-01, populate only the permitted resolution fields, document the process in full, and regenerate public artefacts from the single source of truth.
---
## 2. Objectives & Success Criteria
### Primary Objectives
- Achieve 100 % resolution of every record returned by the FR-01 identification filter.
- Populate only schema-validated resolution fields.
- Produce a complete, versioned audit trail in `resolution_sessions/`.
- Regenerate all public tables exclusively from the updated `predictions_v2.jsonl`.
### Quantitative Success Metrics (to be filled after FR-01)
- Exact number of records resolved (must equal the FR-01 output count).
- 100 % of updated records pass validation against `schema/prediction_schema.py`.
- Every resolved record contains a stable, authoritative `outcome_verification_url`.
- All dependent HTML tables regenerate without error.
### Qualitative Success Metrics
- Full compliance with the hybrid human-reviewed process (LLM draft optional, human verification and approval mandatory).
- Every rationale (whether stored in the record or only in the session log) is written against the specific wording of that record’s `resolution_criteria`.
- Complete disclosure of any LLM use (model, prompt version, material differences).
- No original prediction fields altered.
- Session log records the exact methodology version and scoring_rules version that governed the batch.
---
## 3. Scope
### In Scope
- Identification and resolution of overdue records from `predictions_v2.jsonl` only.
- Binary, probabilistic, ranked, and compound claims according to existing rules.
- Optional LLM drafting using versioned prompts from `prompts/`.
- Mandatory human verification against primary/official sources.
- Application of scoring rules current at the time of resolution.
- Creation of session artefacts following the established naming convention.
- Post-resolution validation, table regeneration, commit, and site update.
- Full audit documentation.
### Out of Scope
- Any record with `resolution_date` > 2026-07-16.
- Creation of new predictions or expansion of the gold-standard set.
- Modification of any original prediction field (`original_statement`, `statement_probability`, `resolution_criteria`, source metadata, etc.).
- Schema changes, scoring-rule changes, or methodology changes (any such change requires a separate, versioned process).
- Website redesign or new features.
- Automated ongoing resolution pipelines.
- Appeals, disputes, or post-resolution corrections (governed by future editorial process).
---
## 4. Current State & Data Context
**Single source of truth**: `predictions_v2.jsonl`.
**Status definition**: A record is unresolved if and only if the `outcome` field is missing or null.
**Exact overdue set**: Must be produced by the FR-01 identification script. No approximate counts are authoritative.
**Schema authority**: Only fields defined and validated by `schema/prediction_schema.py` may be written. If a detailed `resolution_rationale` exceeds the current schema, it is stored exclusively in the corresponding session log file.
**Official sources**: FIFA official results, brackets, and match reports as they stood on the resolution date of each claim.
---
## 5. Functional Requirements
### FR-01: Overdue Candidate Identification (Hard Gate)
- Produce an exact, reproducible list of every record where `resolution_date` ≤ “2026-07-16” and `outcome` is null/missing.
- Output both a machine-readable file (JSON/JSONL) and a human-readable Markdown table.
- Sort primarily by `resolution_date` ascending, secondarily by forecaster / claim type.
- Embed the exact output (or a permanent link to it) into this requirements document or the first session log before any resolution work begins.
- No resolution activity is permitted until this step is complete and recorded.
### FR-02: Per-Prediction Resolution Workflow
Must follow the hybrid process defined in the governing `METHODOLOGY.md`.
For each record:
1. Read the full record, paying particular attention to the exact text of `resolution_criteria`.
2. Gather evidence exclusively from primary/official sources. Record the source and, where the page is dynamic, a stable archive reference or retrieval timestamp.
3. Optional LLM draft phase: use only a versioned prompt from `prompts/`. Log model, prompt version, and timestamp.
4. Human verification and final decision (mandatory):
   - Independently confirm or correct every field.
   - Set `outcome` to the realised value consistent with the criteria and scoring rules (normally 0.0 or 1.0; fractional only when partial scoring is explicitly authorised).
   - Write `outcome_proof` (concise, factual).
   - Write `outcome_verification_url` (stable, authoritative).
   - Any explanatory text that cannot be stored in schema-validated fields is placed in the session log.
5. Never alter any original prediction field.
6. Validate the updated record against `schema/prediction_schema.py` before acceptance.
**Granularity rule**: Every explanatory statement must be written against the specific wording of that record’s `resolution_criteria`. Shared phrasing across records is permitted only when the criteria text is identical and the justification is recorded in the session log.
### FR-03: Batch Management & Session Documentation
- Create one or more files in `resolution_sessions/` using the established convention:
  `YYYY-MM-DD_batchXX.md` (e.g., `2026-07-17_batch01.md`).
- Each session file must contain:
  - Exact list of `statement_id`s resolved.
  - Methodology version and scoring_rules version that governed the batch.
  - Confirmation of personal primary-source verification by the named human resolver.
  - Full LLM disclosure (if any) including material differences from draft to final.
  - Self-audit checklist.
  - Any edge-case interpretations and their justification.
  - Source snapshot / archive notes where relevant.
### FR-04: Post-Resolution Pipeline
1. Full schema validation of the updated `predictions_v2.jsonl`.
2. Execution of `scripts/generate_prediction_tables.py`.
3. Commit with a factual message that states the batch identifier, number of records, and methodology version (no narrative or promotional language).
4. Push and verification that public tables and scores update correctly.
5. Changelog entry.
### FR-05: Edge Cases & Quality Gates
- Ambiguous criteria → adopt the most literal, verifiable interpretation; document the reading in the session log.
- Already partially populated records → complete or confirm; do not overwrite verified data.
- Compound claims → address every sub-claim explicitly.
- Validation failure → do not commit.
- Pre-commit technical control: confirm that the only modified fields in any record are the permitted resolution fields.
---
## 6. Non-Functional Requirements
| ID | Category | Requirement |
|--------|--------------------|-------------|
| NFR-01 | Process Compliance | 100 % of resolutions follow the hybrid process; LLM metadata fully logged. |
| NFR-02 | Source Integrity | Every `outcome_verification_url` points to a stable, authoritative source. Source retrieval context recorded when necessary. |
| NFR-03 | Independence | Outcome determination ignores forecaster identity or reputation. |
| NFR-04 | Auditability | Any third party can re-verify every resolution from the session log + primary sources. |
| NFR-05 | Granularity | Rationales and proofs remain specific to the individual `resolution_criteria`. No unjustified templating. |
| NFR-06 | Immutability | Resolved fields are final. Subsequent changes require a new rationale, changelog entry, and explicit justification. |
| NFR-07 | Data Quality | Updated JSONL must validate cleanly; downstream generation must succeed. |
---
## 7. Deliverables
1. Updated `predictions_v2.jsonl` containing only schema-valid resolution fields for the exact FR-01 set.
2. One or more `resolution_sessions/YYYY-MM-DD_batchXX.md` files forming a complete audit trail.
3. Regenerated public tables.
4. Validation output and short factual summary of counts and LLM usage.
5. Changelog entry.
6. This requirements document (v1.1) committed with the FR-01 identification output attached or linked.
---
## 8. Assumptions, Constraints & Dependencies
**Assumptions** (explicitly stated and requiring validation)
- Official outcomes for the relevant stages exist and are stable.
- The identification script can be executed against the current `predictions_v2.jsonl`.
- Versioned resolution prompts exist or can be created without changing methodology.
**Constraints**
- Human accountability is mandatory.
- No violation of any core principle is permitted.
- Exact FR-01 output is a prerequisite for all subsequent work.
**Dependencies**
- `schema/prediction_schema.py`
- `scripts/generate_prediction_tables.py`
- Current `METHODOLOGY.md` and `scoring_rules.md`
- Official FIFA sources
---
## 9. Risks & Mitigations
| Risk | Mitigation |
|------|------------|
| Unverified starting count | FR-01 is a hard gate; no work begins until exact list is produced and recorded. |
| Misreading of criteria | Literal reading required; interpretation logged; spot-checks mandatory. |
| LLM draft error | Drafts are untrusted; human must re-verify every field and log differences. |
| Schema drift | Only existing validated fields may be written; any extension requires separate process. |
| Loss of granularity | Explicit ban on unjustified rationale templating. |
| Incomplete audit trail | Session files must contain methodology version, scoring version, and full LLM disclosure. |
---
## 10. Implementation Approach
**Phase 0 – Mandatory Setup**
Execute FR-01. Embed or permanently link the exact overdue list. Initialise the first session file. Confirm methodology and scoring versions. No further progress is authorised until this phase is complete.
**Phase 1 – Pilot**
Resolve a small, representative subset. Validate end-to-end pipeline. Refine only logging detail (not process or principles).
**Phase 2 – Full Resolution**
Process remaining records in chronological batches. Maintain session logs in real time. Perform periodic independent spot-checks.
**Phase 3 – Finalisation**
Full validation, table regeneration, commit, live-site verification, changelog entry.
**Phase 4 – Retrospective**
Factual record of lessons learned, confined to process observations that do not alter principles or scope.
---
## 11. Governance
- Any deviation from this specification must be recorded in the relevant session log before the affected records are committed.
- Future revisions of these requirements follow semantic versioning and are recorded in `CHANGELOG.md`.
---
**This v1.1 specification corrects the factual, versioning, granularity, naming, and transparency defects identified in v1.0. It is executable only after the FR-01 identification output has been produced and recorded. All subsequent work must remain inside the boundaries defined above.**

---

## Phase 0 Completion Record (2026-07-17)

FR-01 identification executed successfully.

- Script: `scripts/identify_overdue_predictions.py`
- Machine-readable output: `overdue_candidates_2026-07-16.jsonl`
- Human-readable output: `overdue_candidates_2026-07-16.md`
- Exact overdue count: **44**
- Total records scanned: 73
- Cutoff applied: `resolution_date` ≤ 2026-07-16 **and** `outcome` is null

This list is now the single authoritative set for all subsequent resolution work.
No records outside this set may be resolved under this specification.

