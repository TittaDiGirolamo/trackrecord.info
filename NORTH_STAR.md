# Trackrecord.info — North Star Metric

**Version:** 1.0  
**Date:** 2026-07-29  
**Status:** Active  
**Aligned with:** Problem & Vision Document v1.5 and 90-Day Action Plan v1.0

---

## 1. Purpose

This document defines the single primary metric that measures whether Trackrecord.info is delivering its core value, and the process for tracking initiatives that are expected to improve it.

The goal is clarity and focus: one outcome metric that reflects real user value, plus a lightweight system for linking product work to that outcome.

---

## 2. North Star Metric

**Weekly completed accountability lookups**

### Definition

A **completed accountability lookup** is a single browser session in which a user:

1. Selects or searches for a public figure (forecaster)
2. Views that figure’s accuracy profile page
3. Opens **at least one resolved prediction** detail page that displays the full evidence trail (original statement + source, resolution criteria, primary evidence, and final status)

Only sessions that complete this full sequence count.

The North Star is the **number of unique sessions** that complete this sequence in a given calendar week.

### Why this metric

This is the closest measurable proxy for the core user outcome described in the product vision:

> A user arrives with the question “Has this person been right before?”, leaves with a concrete, citable, evidence-backed answer, and experiences the interaction as fast, neutral, and trustworthy.

It directly maps to the MVP happy path:

Search / select figure → Profile → Resolved prediction with evidence trail → Clarity

Secondary metrics (page views, time on site, shares, etc.) are useful diagnostics but are not the North Star.

---

## 3. How the metric is measured

### Analytics events (required)

The following client-side events must be instrumented:

| Event                        | Trigger                                      | Required properties                          |
|-----------------------------|----------------------------------------------|----------------------------------------------|
| `figure_selected`           | User searches or clicks a figure             | `figure_id` (or slug)                        |
| `profile_viewed`            | Accuracy profile page loads                  | `figure_id`                                  |
| `prediction_detail_viewed`  | Prediction detail page loads                 | `prediction_id`, `figure_id`, `status`       |

Only events where `status = "resolved"` count toward the North Star.

### Counting rules

- Count **unique sessions** that fire the sequence above within the same session.
- A session may view multiple resolved predictions; it still counts as one completed lookup.
- Direct landings on a resolved prediction page (e.g. via share link) do **not** count unless the user also views the corresponding profile in the same session.
- Pending predictions never count.

### Tooling

Current implementation uses **Plausible Analytics**.

The weekly number is the primary score reviewed by the project.

---

## 4. Tracking initiatives that move the North Star

Every product or content initiative that aims to improve the user experience must state an explicit hypothesis about how it will increase completed accountability lookups.

### Initiative tracking table

The table below is the single source of truth for active and recently completed initiatives. Update it in place.

| Initiative | Hypothesis | Target funnel step | Expected impact | Ship date | Result (1–2 weeks later) | Status |
|------------|------------|--------------------|-----------------|-----------|---------------------------|--------|
|            |            |                    |                 |           |                           |        |
|            |            |                    |                 |           |                           |        |
|            |            |                    |                 |           |                           |        |

**Status values:** `Planned` · `In progress` · `Shipped` · `Moved the needle` · `No clear impact` · `Negative` · `Abandoned`

### Rules

- An initiative without a clear hypothesis linking it to completed lookups should not be started.
- After shipping, measure the North Star (and the relevant funnel step) for 1–2 weeks.
- Record the observed result in the table. Archive completed rows after review (keep the learning visible in git history).

### Supporting funnel metrics

These secondary metrics help diagnose *where* an initiative had (or failed to have) impact:

- Conversion: `figure_selected` → `profile_viewed`
- Conversion: `profile_viewed` → `prediction_detail_viewed` (resolved only)
- Overall completed lookup rate

---

## 5. Review cadence

- **Weekly:** Review the North Star number first. Then update the initiative table for any recently shipped work.
- Keep the active list short (ideally ≤ 4 initiatives at a time).
- The North Star number is the first item in any product or prioritization discussion.

---

## 6. Relationship to other documents

- **Problem & Vision Document v1.5** — defines the user outcome this metric measures.
- **90-Day Action Plan v1.0** — early targets and scope constraints.
- **METHODOLOGY.md / SCORING.md / PROVENANCE.md** — govern data quality and resolution integrity (necessary conditions for the metric to be meaningful).

This document is the operational layer that connects product work to measurable user value.

---

*End of document*
