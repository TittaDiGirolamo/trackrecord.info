# Trackrecord.info

**Track public predictions. Measure accuracy. Build accountability.**

Trackrecord.info systematically compares public predictions from experts and forecasters against real-world outcomes and publishes transparent, auditable accuracy metrics.

---

## Current Status (July 2026)

- **25 validated gold standard records** (gold_001–gold_025.json) for FIFA World Cup 2026
- Structured `PredictionRecord` schema with automated validation
- **Topic-specific accuracy scoring** (circle of competence) for granular insights by subject
- Clean repository structure with schema and tooling in place
- Automated table and detail-page generation from `predictions_v2.jsonl`
- Permanent prediction detail pages at `/predictions/{statement_id}.html`
- Focus: Transparent forecasting accountability

---

## What We Do

Most public predictions disappear without accountability. Trackrecord.info creates a permanent, transparent record so we can all see who gets it right over time.

**Core Principles:**

- Verifiability
- Independence
- Granularity
- Transparency
- No retroactive adjustment

## Long-term Vision

Trackrecord.info aims to develop rigorous, transparent, and reproducible methods for evaluating public predictions and statements. Over time, we intend to build the technical and methodological infrastructure that could serve as a reference standard for measuring forecasting accuracy and accountability.

Our core technical commitments include:
- Primary use of **proper scoring rules** (especially Brier Score) for probabilistic predictions
- Clear, falsifiable resolution criteria for every claim
- Topic-specific performance analysis while respecting statistical limitations
- Full auditability and reproducibility of resolutions and scores
- Explicit handling of different prediction types (binary, probabilistic, ranked, compound, etc.)
- Statistical guardrails to prevent over-interpretation of limited data

The evaluation methodology is versioned. Significant changes to scoring rules, prediction type handling, or statistical standards will be documented and versioned in `METHODOLOGY.md` to ensure reproducibility and transparency over time.

We prioritize long-term credibility, methodological soundness, and usefulness to serious researchers and decision-makers over short-term metrics or volume of predictions.

## Current Scope and Limitations

The project is currently focused on high-visibility public predictions, with an initial emphasis on the 2026 FIFA World Cup. While we track both probabilistic and binary claims, many early records are binary or compound in nature.

Aggregate scores should be interpreted cautiously, especially with small sample sizes. We are actively developing stronger statistical tooling and clearer evaluation standards. For the most accurate picture, users should review individual resolved predictions and their rationales rather than relying only on overall numbers.

---

## Design Principles

The design of Trackrecord.info follows a clear set of principles focused on clarity, transparency, and respect for the user.

- [Design Principles](./trackrecord-design-principles/README.md) — Official design principles (v1.1), including typography decisions and contribution process.
- [Visual system](./trackrecord-design-principles/VISUAL_SYSTEM.md) — Concrete UI rules for public pages (pills, type weights, scorecards, detail layout).

---

## Gold Standard Dataset

We maintain a high-fidelity **gold standard dataset** to support the development of automated prediction extraction.

**Location:** [`gold_standard/wc2026/`](./gold_standard/wc2026/)

This dataset includes:
- Manually created and validated prediction records
- Clear, falsifiable `resolution_criteria` for every claim
- Independent probability calibration
- Full documentation and validation tooling

The gold standard is used to develop and test automated extraction systems.

---

## Repository Structure

```text
trackrecord.info/
├── gold_standard/wc2026/          # High-fidelity gold standard records
├── schema/
│   └── prediction_schema.py       # Canonical Pydantic data model
├── scripts/
│   ├── validate_gold_records.py
│   ├── generate_prediction_tables.py
│   └── generate_prediction_details.py
├── predictions/                   # Permanent detail pages (static HTML)
├── trackrecord-design-principles/
│   ├── DESIGN-PRINCIPLES.md
│   └── VISUAL_SYSTEM.md
├── predictions_v2.jsonl           # Main predictions database (single source of truth)
├── METHODOLOGY.md                 # Full scoring and resolution rules
├── index.html                     # Public website (GitHub Pages)
├── predictions.html               # Predictions table
└── README.md

How It Works

Prediction Logging — Public predictions are logged with source and timestamp
Resolution — Outcomes are determined using official sources
Scoring — Predictions are scored on a 0–100 scale (overall + by topic where data allows) using transparent rules
Publication — Scores and rationale are published publicly, including a permanent detail page per resolved prediction

Full methodology: METHODOLOGY.md

Why This Matters

Creates accountability for public forecasters
Enables objective comparison across different experts
Builds infrastructure for automated prediction tracking
Contributes to better forecasting practices over time


Current Focus
During the 2026 FIFA World Cup period, we are temporarily focusing on high-visibility forecasters and experts making predictions about the 2026 FIFA World Cup.

Automated Table Regeneration
The prediction table, homepage scorecards, and prediction detail pages are automatically generated from predictions_v2.jsonl.
Manual Regeneration
Bash# Preview table changes (safe)
python3 scripts/generate_prediction_tables.py --dry-run --verbose

# Update the predictions table
python3 scripts/generate_prediction_tables.py

# Generate or refresh all prediction detail pages
python3 scripts/generate_prediction_details.py
Prediction detail pages
Each resolved prediction has a permanent page at:
/predictions/{statement_id}.html
Example: https://trackrecord.info/predictions/pred-2026-04-18-statham-nl-qf.html
The Predictions table links each claim to its detail page.
Automatic updates via GitHub Actions
A GitHub Action regenerates the table, detail pages, and homepage scorecards whenever predictions_v2.jsonl is updated and pushed to main.

Contributing
We welcome contributions, especially:

Expanding the Gold Standard dataset
Improving documentation and methodology
Reporting bugs or suggesting improvements

Please open an issue or pull request to discuss.
License
This project is currently unlicensed. Licensing terms will be defined in a future release.
Links

Website: https://trackrecord.info
Repository: https://github.com/TittaDiGirolamo/trackrecord.info
Issues: https://github.com/TittaDiGirolamo/trackrecord.info/issues

Building transparent accountability for public predictions.