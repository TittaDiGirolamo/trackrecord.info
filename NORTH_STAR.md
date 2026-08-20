# Trackrecord.info — North Star Metric

**Version:** 1.0  
**Date:** 2026-07-29  
**Status:** Active  
**Aligned with:** Problem & Vision Document v1.5 and 90-Day Action Plan v1.0

---

## 1. Purpose

This document defines the single primary metric that measures whether Trackrecord.info is delivering its core value, and the process for tracking initiatives that are expected to improve it.

The goal is clarity and focus: one outcome metric that reflects real user value, plus a lightweight system for linking product work to that outcome.

We optimize for **sustained** weekly completed accountability lookups over the long run. Short-term spikes that come at the expense of long-term credibility, data integrity, or user trust are considered negative.

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

Every product, content, or process initiative must state an explicit hypothesis about how it will affect completed accountability lookups **before work begins**.

We care about sustained impact. The larger and more structural an initiative is, the more carefully its long-term effect on the North Star must be articulated.

### Size-based requirements

| Initiative size | Examples | Required documentation |
|-----------------|----------|------------------------|
| **Tiny / tactical** | Copy tweaks, small UI fixes, single extractor improvement | One-sentence rationale linking it to the North Star (or a funnel step) is enough. |
| **Medium** | New profile features, improved resolution workflow, topic expansion within current scope | Clear hypothesis + expected near-term effect + target funnel step. |
| **Large / structural** | New domains, major methodology changes, automation of core processes, significant UX redesigns | Explicit long-run hypothesis (6–18 months), including second-order effects, risks to data quality or trust, and how the initiative compounds over time. |

### Initiative tracking table

The table below is the single source of truth for active and recently completed initiatives. Update it in place.

| Initiative | Size | Hypothesis (incl. long-run view for Medium+) | Target funnel step | Expected impact | Ship date | Result (1–2 weeks later) | Status |
|------------|------|---------------------------------------------|--------------------|-----------------|-----------|---------------------------|--------|
|Phase 0 — Measurement Validation & Freeze|Medium|Reliable measurement is a necessary condition for any subsequent claim about demand|Full North Star sequence (figure_selected → profile_viewed → prediction_detail_viewed with status=resolved)|Enables trustworthy baseline and all later demand claims|—|—|In progress|
|            |      |                                             |                    |                 |           |                           |        |

**Status values:** `Planned` · `In progress` · `Shipped` · `Moved the needle` · `No clear impact` · `Negative` · `Abandoned`

### Rules

- No initiative may be started without a hypothesis that matches its size (see table above).
- Tiny changes need only a short rationale. Medium and Large initiatives require a written hypothesis *before* work begins.
- Large / structural initiatives must explicitly address long-run effects (6–18 months) and any risks to data quality, resolution integrity, or user trust.
- After shipping, measure the North Star and the relevant funnel step for 1–2 weeks and record the result in the table.
- Completed rows should be archived after review so the learning remains visible in git history.
- When in doubt about size classification, treat the initiative as one level larger.

### Operating rule (current stage)

This project is still small. Formal automated enforcement is deliberately kept light.

The real standard is personal and documentary:

- Before starting any Medium or Large initiative, update the tracking table with a hypothesis appropriate to its size.
- Treat the written hypothesis as a public commitment (even if only to your future self).
- Review progress against the hypothesis during the regular weekly North Star check.

The goal is better decisions and clearer learning, not process theatre.

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
