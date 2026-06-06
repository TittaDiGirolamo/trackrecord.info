# Trackrecord.info

**Track public predictions. Measure accuracy. Build accountability.**

Trackrecord.info systematically compares public predictions from experts and forecasters against real-world outcomes and publishes transparent, auditable accuracy metrics.

---

## Current Status (June 2026)

- **13 high-quality gold standard records** created for FIFA World Cup 2026
- Structured `PredictionRecord` schema with strict validation
- Automated validation pipeline in place
- Focus: Transparent forecasting accountability

---

## Gold Standard Dataset

We maintain a high-fidelity gold standard dataset to support the development of automated prediction extraction systems.

**Location**: [`gold_standard/wc2026/`](./gold_standard/wc2026/)

This dataset includes:
- 13 manually validated prediction records
- Clear `resolution_criteria` for every claim
- Independent probability calibration
- Full audit trail and documentation

The gold standard is used to:
- Develop and test automated extraction pipelines
- Evaluate LLM prompt quality
- Establish baselines for future automation

---

## Repository Structure

trackrecord.info/
├── gold_standard/wc2026/     # High-fidelity gold standard records
├── schema/                   # Canonical Pydantic data model
├── scripts/                  # Validation and utility scripts
├── predictions.jsonl         # Main public prediction database
├── METHODOLOGY.md            # Full scoring and resolution rules
└── index.html                # Public website (GitHub Pages)

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

This focused sprint allows us to test our systems with high-interest content while maintaining full methodological rigor.

---

## Contributing

We welcome contributions in several forms:

- **Gold Standard Records** — Help expand the validated reference dataset (see [Gold_Record_Creation_Checklist.md](./gold_standard/wc2026/Gold_Record_Creation_Checklist.md))
- **Bug Reports** — Report issues with scoring, data, or methodology
- **Methodology Improvements** — Suggest refinements to scoring rules

Please open an issue or pull request to discuss contributions.

---

## License

This project is currently unlicensed. Licensing terms will be defined in a future release.

---

## Contact & Links

- **Website**: [trackrecord.info](https://trackrecord.info)
- **Repository**: [github.com/TittaDiGirolamo/trackrecord.info](https://github.com/TittaDiGirolamo/trackrecord.info)
- **Issues**: [GitHub Issues](https://github.com/TittaDiGirolamo/trackrecord.info/issues)

---

**Want to explore or contribute?**  
Check out the [Gold Standard Dataset](./gold_standard/wc2026/) or read the full [Methodology](./METHODOLOGY.md).

*Building transparent accountability for public predictions.*
