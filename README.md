# Trackrecord.info

**Track public predictions. Measure accuracy. Build accountability.**

Trackrecord.info systematically compares public predictions from experts and forecasters against real-world outcomes and publishes transparent, auditable accuracy metrics.

---

## Current Status (June 2026)

- **25 validated gold standard records** (gold_001–gold_025.json) for FIFA World Cup 2026
- Structured `PredictionRecord` schema with automated validation
- Clean repository structure with schema and tooling in place
- Automated table generation from `predictions.jsonl`
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

---

## Design Principles

The design of Trackrecord.info follows a clear set of principles focused on clarity, transparency, and respect for the user.

- [Design Principles](./trackrecord-design-principles/README.md) — Official design principles (v1.1), including typography decisions and contribution process.

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

- trackrecord.info/
- ├── gold_standard/
- │   └── wc2026/                  # High-fidelity gold standard records
- ├── schema/
- │   └── prediction_schema.py     # Canonical Pydantic data model
- ├── scripts/
- │   ├── validate_gold_records.py
- │   └── generate_prediction_tables.py
- ├── predictions.jsonl            # Main public prediction database
- ├── METHODOLOGY.md               # Full scoring and resolution rules
- ├── index.html                   # Public website (GitHub Pages)
- └── README.md

---

## How It Works

1. **Prediction Logging** — Public predictions are logged with source and timestamp
2. **Resolution** — Outcomes are determined using official sources
3. **Scoring** — Predictions are scored on a 0–100 scale using transparent rules
4. **Publication** — Scores and rationale are published publicly

Full methodology: [METHODOLOGY.md](./METHODOLOGY.md)

---

## Why This Matters

- Creates **accountability** for public forecasters
- Enables **objective comparison** across different experts
- Builds **infrastructure** for automated prediction tracking
- Contributes to better **forecasting practices** over time

---

## Current Focus

During the 2026 FIFA World Cup period, we are temporarily focusing on high-visibility forecasters and experts making predictions about the 2026 FIFA World Cup.

---

## Automated Table Regeneration

The prediction and forecaster tables on the website are **automatically generated** from `predictions.jsonl`.

### Manual Regeneration

```bash

# Preview what would change (safe)
python3 scripts/generate_prediction_tables.py --dry-run --verbose

# Update index.html
python3 scripts/generate_prediction_tables.py

```

### Automatic Updates via GitHub Actions
A GitHub Action automatically regenerates the tables whenever `predictions.jsonl` is updated and pushed to `main`.

---

## Contributing
We welcome contributions, especially:
- Expanding the Gold Standard dataset
- Improving documentation and methodology
- Reporting bugs or suggesting improvements
- Please open an issue or pull request to discuss.

## License
This project is currently unlicensed. Licensing terms will be defined in a future release.

## Links
Website: trackrecord.info
Repository: github.com/TittaDiGirolamo/trackrecord.info
Issues: GitHub Issues

Building transparent accountability for public predictions.