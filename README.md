# Trackrecord.info

**Track public predictions. Measure accuracy. Build accountability.**

Trackrecord.info systematically compares public predictions from experts and forecasters against real-world outcomes and publishes transparent, auditable accuracy metrics.

---

## Current Status (June 2026)

- **25 validated gold standard records** (gold_001–gold_025.json) for FIFA World Cup 2026
- 10 WC2026 predictions tracked in `predictions.jsonl` (all in pending resolution-ready preparation state as of 2026-06-10 per Sprint Resolution Requirements Specification TRACK-SPRINT-REQ-2026-06-P1W1-001; all expected_resolution_dates future, earliest 2026-06-27; no outcomes assigned yet. Preparatory human review and schema validation in progress.)
- Structured `PredictionRecord` schema with automated validation
- Clean repository structure with schema and tooling in place
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

## Gold Standard Dataset

We maintain a high-fidelity **gold standard dataset** to support the development of automated prediction extraction.

**Location:** [`gold_standard/wc2026/`](./gold_standard/wc2026/)

This dataset includes:
- 13 manually created and validated prediction records
- Clear, falsifiable `resolution_criteria` for every claim
- Independent probability calibration
- Full documentation and validation tooling

The gold standard is used to develop and test automated extraction systems.

---

## Repository Structure

trackrecord.info/
├── gold_standard/
│   └── wc2026/                    # High-fidelity gold standard records
├── schema/
│   └── prediction_schema.py       # Canonical Pydantic data model
├── scripts/
│   └── validate_gold_records.py   # Validation script
├── predictions.jsonl              # Main public prediction database
├── METHODOLOGY.md                 # Full scoring and resolution rules
├── index.html                     # Public website (GitHub Pages)
└── README.md
text---

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

During the 2026 FIFA World Cup period, we are temporarily focusing on high-visibility Dutch forecasters and experts making predictions about the Netherlands national team (Oranje).

---

## Contributing

We welcome contributions, especially:

- Expanding the Gold Standard dataset
- Improving documentation and methodology
- Reporting bugs or suggesting improvements

Please open an issue or pull request to discuss.

---

## License

This project is currently unlicensed. Licensing terms will be defined in a future release.

---

## Links

- **Website**: [trackrecord.info](https://trackrecord.info)
- **Repository**: [github.com/TittaDiGirolamo/trackrecord.info](https://github.com/TittaDiGirolamo/trackrecord.info)
- **Issues**: [GitHub Issues](https://github.com/TittaDiGirolamo/trackrecord.info/issues)

---

*Building transparent accountability for public predictions.* 
