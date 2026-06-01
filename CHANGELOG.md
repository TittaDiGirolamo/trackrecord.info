# Trackrecord.info — Changelog
All notable changes to Trackrecord.info are documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and adheres to [Semantic Versioning](https://semver.org/).

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
