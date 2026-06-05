# Gold Record Creation Checklist

**Project**: Trackrecord.info - FIFA World Cup 2026 Gold Standard Dataset  
**Version**: 1.0 (as of 2026-06-04)  
**Purpose**: Ensure every manual gold-standard `PredictionRecord` meets the exact format requirements with methodological rigor, nuance preservation, and zero implicit assumptions.

Use this checklist for **every** record created. Mark each item as ✓ (complete) or note exceptions with reasoning.

---

## 1. Preparation (Before Extraction)
- [ ] Select one distinct future-oriented prediction from an **approved whitelist source** only (The Analyst, Nate Silver’s Silver Bulletin, The Guardian, The Athletic, etc.).
- [ ] Confirm the source is English-language written text with clear byline.
- [ ] Read the full article/context to understand nuance.
- [ ] Copy the relevant paragraph(s) as `source_text_snippet`.

**Zero-Assumption Validation**: Explicitly note any temporal references, pronouns, or incomplete names that require [clarifications].

---

## 2. original_statement
- [ ] Use **exact verbatim** wording where possible.
- [ ] Make the statement **long enough and self-contained** so a reader understands it without the full article.
- [ ] Enclose the entire value in double quotes.
- [ ] Append [clarifications] immediately for:
  - Ambiguous pronouns ("he", "they", "it", etc.) → explicit interpretation.
  - Incomplete names → full reference.
  - Temporal references ("this summer", "by the end of group stage") → explicit [2026-06-XX] or range.
- [ ] Do **not** merge, split, or omit any distinct claim.

---

## 3. Author Identification
- [ ] Use byline from the text if present → "Lastname","Firstname" format.
- [ ] If no clear author in text, use permitted external lookup on title/URL only.
- [ ] If no credible author found → lastname: "[anonymous]", firstname: "".
- [ ] Document source of lookup (if any) in `statement_context`.

---

## 4. Metadata Fields
- [ ] `statement_id`: Unique (e.g., `gold_XXX` for manual phase; later use deterministic hash + run_id).
- [ ] `statement_topic`: Specific and scoped (e.g., "FIFA World Cup 2026 - Group stage qualification", "FIFA World Cup 2026 - Tournament winner").
- [ ] `statement_publication_date`: Exact YYYY-MM-DD from article/metadata. Use today's date (2026-06-04) only if none present.
- [ ] `statement_original_url`: Full URL from source. Use "Not provided" only if truly absent.
- [ ] `extraction_timestamp`: Current date (YYYY-MM-DD).

---

## 5. statement_probability (0.00–1.00)
- [ ] Provide your **independent calibrated probability** that the claim resolves true.
- [ ] Base **only** on information in the text + general knowledge as of extraction date.
- [ ] Do **not** use external real-time data, betting odds, or new searches.
- [ ] Document brief reasoning if deviating significantly from source probability.

---

## 6. statement_context
- [ ] Describe **only** situational attributes: delivery format, seriousness, speaker authority, editing level, methodology signals.
- [ ] Example: "Excerpt from data-driven group stage preview published by The Analyst on 2026-06-03. Author Dan Edwards using Opta supercomputer methodology."
- [ ] **Never** restate or summarize the substantive prediction content.

---

## 7. resolution_date
- [ ] Derive from statement or explicit timing in the claim.
- [ ] Use YYYY-MM-DD format.
- [ ] Leave empty only if truly undeterminable (rare).

---

## 8. resolution_criteria (Critical Field)
- [ ] Write **one single falsifiable sentence**.
- [ ] Must satisfy **all four** requirements:
  - Specific and Unambiguous (Falsifiable)
  - Time-Bound (clear end date/period)
  - Probabilistic where appropriate (preserve hedges)
  - Specifies exact observable data source/outcome (e.g., "official FIFA final standings", "lifting the official trophy")
- [ ] If any requirement cannot be met without distorting original meaning:
  - Use exact phrase: "Cannot formulate sufficient resolution_criteria: missing [list of missing elements]"
  - Set `statement_probability` to 0.00 if appropriate.

**Rule**: Preserve full nuance. Better to use failure phrase than force a distorted criteria.

---

## 9. Outcome Fields (for pending records)
- [ ] `outcome`: `null`
- [ ] `outcome_proof`: `null`
- [ ] `outcome_verification_url`: `null`

---

## 10. Final Validation & Saving
- [ ] Paste record into `prediction_schema.py` Pydantic model and confirm it validates cleanly.
- [ ] File name format: `gold_XXX.json` (sequential numbering).
- [ ] Store in `/home/workdir/artifacts/gold_standard/wc2026/`
- [ ] Add/update `README.md` in the folder with selection criteria and any format decisions.

---

## Common Pitfalls to Avoid
- Over-interpreting vague claims into specific criteria.
- Mixing model forecasts with referenced prediction markets.
- Making `statement_context` describe *what* the prediction says.
- Using external searches except for permitted author lookup.
- Creating non-self-contained `original_statement`.

---

**Approval Gate**: After completing 5+ records, review the full batch for consistency before proceeding to automation prompt development.

**Long-term vision**: This checklist ensures the gold set is auditable, repeatable, and high-fidelity, forming the foundation for scalable automated extraction while maintaining short-term discipline.

---
*Last updated: 2026-06-04*  
*Maintainer: Trackrecord.info Project*