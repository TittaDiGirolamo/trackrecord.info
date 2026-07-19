# Trackrecord.info — Changelog
All notable changes to Trackrecord.info are documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and adheres to [Semantic Versioning](https://semver.org/).
---

## [Unreleased]

### Added
- First pilot resolution batch (2026-07-17_batch01): 5 records resolved using Grok 4 LLM draft assistance with full human primary-source verification.
- Reusable automation script: `update_predictions.py` + batch_updates.json workflow.
- Session log: `resolution_sessions/2026-07-17_batch01.md`

### Changed
- Updated `predictions_v2.jsonl` with 5 resolved records from the FR-01 overdue set (44 total).

## [Unreleased]

### Added
- First pilot resolution batch (2026-07-17_batch01): 5 records resolved using Grok 4 LLM draft assistance with full human verification.
- Session log: `resolution_sessions/2026-07-17_batch01.md`
- Methodology version: [exact string]
- Scoring-rules version: [exact string]

### Changed
- Updated `predictions_v2.jsonl` with 5 resolved records from the FR-01 overdue set.

...

## [Unreleased] — 2026-07-10

## [2026-07-16] — Hybrid LLM-Assisted Resolution Documentation

### Added
- New `resolution_requirements_overdue_2026-07-16.md` defining requirements for human-reviewed resolution with optional LLM assistance.
- New `prompts/resolution_draft_v1.0.md` — controlled prompt for generating resolution drafts.
- Added Section 5.1 **LLM-Assisted Resolution with Human-in-the-Loop** to `METHODOLOGY.md`.
- Full hybrid workflow now documented: LLM for drafting + mandatory human verification, source checking, and approval.

### Changed
- Updated `METHODOLOGY.md` to version 0.9.
- Strengthened documentation and accountability requirements for any use of LLM assistance in resolution.
- Added explicit rules that LLM output is always treated as draft only.- Added explicit rules that LLM output is always treated as draft only.

### Changed
- Refined hero section spacing (tighter margin after introductory paragraph) and removed specified gray borders/lines across pill, search bar, Suggest section, and How it works steps for cleaner, calmer UI.
- Consistent visual treatment for form inputs in Stay Updated section.
- Search icon vertically centered.
- Follows trackrecord-design-principles (clarity, simplicity, mobile-first). No functional or content changes.

## [2026-06-11] — Action 2 Follow-up
### Changed
- Also applied consistent topic labeling (`Winner` + `Netherlands Performance (5 stages)`) to the Current Predictions Tracked table for visual coherence (outside original Action 2 scope).

---

## [0.6.0] — 2026-06-01
### Added
- Professional public launch page (`index.html`) with live accuracy metrics
- Core prediction logging system supporting 13 predictions
- Resolution engine v0.6 with deterministic scoring for binary, ranked, and probabilistic predictions
- Topic tagging and cross-forecaster comparison functionality
- Initial tracking of three forecasters:
  - Nate Silver (@NateSilver538)
  - Ken Pomeroy (@kenpomeroy)
  - Sam Vecenie (@Sam_Vecenie)
- Public display of 3 resolved predictions and overall accuracy score (93.8/100)
- GitHub Pages deployment at `https://TittaDiGirolamo.github.io/trackrecord.info`
- Custom domain `trackrecord.info` configured and submitted for verification
### Changed
- None (initial public release)
### Fixed
- None (initial public release)
### Known Issues
- Custom domain verification pending GitHub support ticket resolution
- `predictions.jsonl` and full resolution reports not yet committed to public repository
- Documentation (README, METHODOLOGY, CHANGELOG) added in this release
---
## [0.5.0] — 2026-05-15 (Internal)
### Added
- Initial data model and JSONL storage format
- Prototype resolution engine (non-public)
- Manual logging of first 13 predictions
- Basic accuracy calculation scripts
### Changed
- Shifted from spreadsheet-based tracking to structured data pipeline

---
## [0.1.0] — 2026-04-20 (Prototype)
### Added
- Concept validation and initial forecaster shortlist
- Manual tracking of early predictions for feasibility testing
---
## Unreleased / Planned
### v0.7 (Target: 2026-06-15)
- Automated daily resolution pipeline (basic)
- Addition of 1–2 new forecasters (e.g., FiveThirtyEight or equivalent)
- Public `predictions.jsonl` and `resolution_report_v0.6.md` committed to repository
- Expanded methodology documentation for probabilistic scoring edge cases
### v0.8 (Target: 2026-07)
- Circle of Competence per-forecaster heatmaps
- Historical trend visualization components
- Public read-only API endpoint (read-only)
### v1.0 (Target: 2026-Q3)
- Optional user accounts and personal forecast tracking
- Community leaderboards
- Full mobile-responsive redesign
- Open-source release of resolution engine under defined license

---
**Legend**
`[MAJOR.MINOR.PATCH]` — Semantic versioning applied from v0.6 onward.
Prior versions used internal milestone numbering.
*This changelog is the authoritative record of all public changes.*

## [2026-06-11] — Action 1 Polish
### Changed
- Refined `statement_topic` field in all 10 `predictions.jsonl` records to distinguish Winner predictions from Netherlands Performance stages using consistent hierarchical vocabulary. Full mapping, rationale, and updated JSONL lines documented in Action 1 revised deliverable. Improves long-term auditability and forecaster scoring granularity within WC2026 English focus only.

## 2026-06-30 - Added 15 resolved WC2026 match predictions (Chris Sutton - BBC)

- Added and resolved 15 specific match score predictions from Chris Sutton (BBC Sport, published 10 June 2026).
- All records now include resolution_date, outcome, and derived accuracy.
- Source: TRACK-SPRINT-REQ-2026-06-P1W3-001

