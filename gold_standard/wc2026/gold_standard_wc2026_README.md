# WC2026 Gold Standard Dataset


**Project**: Trackrecord.info  
**Topic**: FIFA World Cup 2026  
**Version**: 1.0  
**Last Updated**: 2026-06-05  
**Total Records**: 13  
**Status**: Validated and ready for use

---

## Purpose

This directory contains the high-fidelity **gold standard** dataset for FIFA World Cup 2026 predictions. These records serve as the authoritative reference for:

- Developing and testing automated prediction extraction pipelines
- Evaluating LLM prompt quality and fidelity
- Establishing baseline calibration for future automated systems
- Ensuring long-term auditability and methodological rigor

Every record has been manually extracted following strict rules for verbatim fidelity, nuance preservation, falsifiable resolution criteria, and independent probability calibration.

---

## Dataset Composition

| Category                        | Count | Examples |
|--------------------------------|-------|----------|
| Group Stage Qualification      | 3     | Switzerland, England, Mexico advancement |
| Tournament Winner Probabilities| 6     | Spain, France, England, Argentina, Brazil |
| Pre-tournament Team Ratings    | 2     | Spain top-rated (PELE & Opta) |
| Tournament Format / Structure  | 1     | 32 teams advancing rule |
| **Total**                      | **13**| — |

**Methodologies Represented**:
- Opta Supercomputer (The Analyst)
- PELE Model 100,000 simulations (Nate Silver’s Silver Bulletin)
- Expert analysis (The Guardian)

---

## File Naming Convention

- `gold_001.json` to `gold_013.json`
- Sequential numbering reflects creation order
- All files follow the canonical `PredictionRecord` schema defined in `schema/prediction_schema.py`

---

## Validation Status

All 13 records have been validated against the Pydantic schema (`prediction_schema.py`).

**Validation Rules Enforced**:
- Correct field types and ranges
- `statement_probability` between 0.00–1.00
- `resolution_criteria` is either a single falsifiable sentence or the exact failure phrase
- `statement_context` contains only situational attributes (no content leakage)
- Proper use of `[clarifications]` in `original_statement`

**Last Validation**: 2026-06-05

---

## How to Use This Dataset

### 1. Local Validation
```bash
python scripts/validate_gold_records.py
```

### 2. Adding New Records
1. Follow the process documented in `Gold_Record_Creation_Checklist.md`
2. Create new file as `gold_XXX.json` (next available number)
3. Run validation script
4. Update this README with new record summary if significant

### 3. Future Automation
This gold set will be used to:
- Iteratively develop and refine LLM extraction prompts
- Measure precision/recall of automated extraction
- Create training/evaluation splits for fine-tuning (if needed)

---

## Record Index

| ID        | Topic                                      | Source                  | Probability | Resolution Date |
|-----------|--------------------------------------------|-------------------------|-------------|-----------------|
| gold_001  | Switzerland Group B advancement            | The Analyst (Opta)      | 0.82        | 2026-06-26      |
| gold_002  | England Group L advancement                | The Analyst (Opta)      | 0.91        | 2026-06-26      |
| gold_003  | Netherlands semi-final ambition (vague)    | The Guardian            | 0.15        | 2026-07-19      |
| gold_004  | Spain top PELE rating                      | Nate Silver (PELE)      | 0.68        | 2026-06-11      |
| gold_005  | Mexico Group A favorite                    | Nate Silver (PELE)      | 0.79        | 2026-06-26      |
| gold_006  | 32 teams advancing format rule             | Nate Silver (PELE)      | 1.00        | 2026-06-26      |
| gold_007  | Spain tournament win probability (Opta)    | The Analyst (Opta)      | 0.18        | 2026-07-19      |
| gold_008  | France ~17% market probability             | Nate Silver (PELE)      | 0.50        | 2026-06-10      |
| gold_009  | Argentina tournament win probability       | The Analyst (Opta)      | 0.12        | 2026-07-19      |
| gold_010  | Spain top PELE rating (refined)            | Nate Silver (PELE)      | 0.67        | 2026-06-11      |
| gold_011  | France tournament win probability (Opta)   | The Analyst (Opta)      | 0.14        | 2026-07-19      |
| gold_012  | England tournament win probability (Opta)  | The Analyst (Opta)      | 0.13        | 2026-07-19      |
| gold_013  | Brazil tournament win probability (Opta)   | The Analyst (Opta)      | 0.08        | 2026-07-19      |

---

## Contributing / Extending

When adding new records:
- Always follow the `Gold_Record_Creation_Checklist.md`
- Prefer high-signal sources from the approved whitelist
- Maintain methodological diversity (different forecasters/models)
- Document any deviations in this README

---

## License & Usage

These gold records are intended for internal development of Trackrecord.info systems. They may be referenced in methodology documentation and future research outputs with appropriate attribution.

---

**Maintainer**: Trackrecord.info Project  
**Contact**: GitHub Issues

*This dataset represents the foundation for transparent, auditable, and methodologically rigorous prediction tracking.*
