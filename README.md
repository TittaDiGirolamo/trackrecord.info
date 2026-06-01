### 1. README.md
Markdown# Trackrecord.info
**Verify public predictions against real-world outcomes.**
**Current Version**: v0.6
**Status (2026-06-01)**: 3 forecasters tracked • 13 predictions logged • 3 resolved • Overall accuracy **93.8 / 100**
Trackrecord.info systematically compares public predictions from experts and forecasters against actual outcomes and publishes transparent, auditable accuracy metrics.
## Mission
Most public predictions disappear without accountability. Trackrecord.info creates a permanent, transparent record so that anyone can evaluate who gets it right over time.
## Current Forecasters
| Forecaster | Handle | Accuracy Score | Resolved | Notes |
|-------------------------|-------------------|----------------|----------|------------------------|
| Nate Silver | @NateSilver538 | 93.8 / 100 | 1 / 1 | Leads on current sample|
| Ken Pomeroy | @kenpomeroy | 6.2 / 100 | 0 / 1 | Small sample size |
| Sam Vecenie | @Sam_Vecenie | 6.2 / 100 | 0 / 1 | Small sample size |
*Scores calculated exclusively from resolved predictions. More data will be added as resolutions occur.*
## v0.6 Features
- **0–100 Accuracy Score**: An intuitive, normalized metric that enables direct comparison across forecasters and topics.
- **Topic Tagging**: Every prediction is categorized (e.g., NBA Draft, College Basketball, Elections) for filtering and cross-forecaster analysis.
- **Cross-Target Comparison**: Direct side-by-side evaluation of multiple forecasters on identical or related predictions.
- **Resolution Engine v0.6**: Systematic, rule-based determination of prediction outcomes with full audit trail.
- **Daily Automated Updates**: The system processes new resolutions and recalculates metrics on a recurring schedule.
## Repository Structure
trackrecord.info/
├── index.html # Live public interface (GitHub Pages)
├── CNAME # Custom domain configuration
├── README.md # This file
├── METHODOLOGY.md # Scoring rules and resolution process
├── CHANGELOG.md # Version history
├── predictions.jsonl # Primary data store (to be added)
├── resolution_report_v0.6.md # Latest accuracy report (to be added)
└── docs/
    └── data-schema.md # Technical specification (planned)
text## Access
- **Live Site** (GitHub Pages): https://TittaDiGirolamo.github.io/trackrecord.info
- **Custom Domain** (pending verification): https://trackrecord.info
- **Source Repository**: https://github.com/TittaDiGirolamo/trackrecord.info
## Roadmap (High-Level)
**Sprint 1 (Immediate)**
- Complete public documentation (this release)
- Add 1–2 additional high-signal forecasters
- Release resolution engine v0.7 (basic automation)
**Sprint 2 (2–4 weeks)**
- Circle of Competence tracking per forecaster
- Historical trend graphs
- Public read-only API
**Sprint 3 (1–2 months)**
- Optional user accounts and personal dashboards
- Leaderboards
- Mobile-responsive refinements
## Contributing & Transparency
All data, scoring logic, and resolutions are designed to be fully auditable. Suggestions, corrections, and additional forecaster proposals are welcome via GitHub issues or direct contact.
**License**: To be defined in v0.7 (currently all rights reserved by the project maintainer).
---
*Last updated: 2026-06-01*
*Trackrecord.info — Building verifiable forecasting accountability.*
