**Trackrecord.info**

**Problem & Vision Document**

**Version**: 1.5

**Date**: 2026-06-08

**Status**: Simplified MVP scope (v1.5) — lean core loop only; WC2026 English focus; user accounts and advanced UI deferred

### 1. Why are we doing this?

We are building Trackrecord.info because public discourse currently lacks any systematic, accessible, and neutral mechanism to hold identifiable individuals accountable for the forward-looking predictions they make in public.

**Evidence base**

This document is derived exclusively from:

- The project’s publicly stated purpose on its homepage (https://trackrecord.info/, accessed 2026-06-08): “Trackrecord.info is building a platform that allows users to verify the factual accuracy of public predictions by individuals and compare them with demonstrable results in the real world.”
- The public GitHub repository (https://github.com/TittaDiGirolamo/trackrecord.info, accessed 2026-06-08), including README.md, METHODOLOGY.md, and supporting files which detail the implementation, gold standard dataset (manually created and validated records), scoring rules, human-reviewed resolution process, and temporary focus on FIFA World Cup 2026 predictions (English-language sources).
- Current operational baseline: 0 unique “Express interest” sign-ups on the landing page as of 2026-06-08.

No internal market research, user interviews, or competitor analyses were used. All reasoning below represents a logical extension of this stated purpose, open-source implementation details, and the explicit zero-subscriber starting point.

**Core rationale**

Predictions influence policy, investment decisions, media narratives, and individual behaviour. When inaccurate predictions by high-visibility figures carry no visible consequences, three systemic problems persist:

- Erosion of epistemic trust in public figures and institutions.
- Repeated societal and economic costs from acting on low-accuracy forecasts.
- Absence of feedback mechanisms that would incentivise higher-quality prediction behaviour over time.

Trackrecord.info exists to close this accountability gap. The long-term vision is a durable public-good infrastructure that makes prediction accuracy a measurable, comparable, and searchable attribute of public figures — analogous to credit scores or academic citation indices. Short-term discipline requires proving technical feasibility, data quality, and early demand signals before expanding scope or pursuing aggressive growth targets.

### 2. What problem are we solving for whom?

**Primary problem statement**

There is no neutral, comprehensive, and easily queryable public record of forward-looking predictions made by identifiable individuals that is systematically linked to their real-world outcomes. Existing fact-checking organisations focus predominantly on contemporaneous claims. Prediction-tracking platforms (e.g. PredictionBook, Metaculus) are designed for voluntary individual forecasters rather than the asymmetric accountability of high-visibility public figures.

**Important distinction: Predictor vs Reporter**

When a journalist or commentator reports on the output of a model or forecasting system (e.g. Opta supercomputer, PELE model), Trackrecord.info distinguishes between:

- The **Predictor** (the model, institution, or individual whose forecast is being reported), and
- The **Reporter/Author** (the journalist or commentator writing about the prediction).

In such cases, the substantive prediction is attributed to the predictor where identifiable, while the reporter is recorded as context. Both are captured to maintain accuracy and auditability.

**Whom we serve**

| Segment | Primary Pain | Expected Value from Trackrecord.info | Validation Status |
| --- | --- | --- | --- |
| General public / voters | Difficulty assessing credibility of experts and public figures | Searchable accuracy profiles of high-visibility figures | Assumed |
| Journalists & researchers | Manual, time-consuming tracking of prediction outcomes | Structured, citable database with verification trail | Assumed |
| Investors & analysts | Lack of track records for influential commentators | Calibrated accuracy data linked to real outcomes | Assumed |
| Public figures & institutions | Reputational risk from untracked predictions | Transparent, auditable personal or institutional track record | Assumed (secondary) |

**Scope assumption**

Trackrecord.info focuses on **predictions** — statements about future states that can be resolved as true/false or probabilistic outcomes within a defined timeframe. It does not address pure opinions, value judgements, or unverifiable claims.

### 3. What does success look like?

**Critical Success Factors (non-negotiable)**

1. **Verification integrity** — Every outcome linkage must be traceable to primary sources with transparent methodology and human review where required.
2. **Coverage of high-impact figures** — Sufficient breadth and depth among influential public figures to create meaningful accountability.
3. **Perceived neutrality** — The platform must remain independent of political, commercial, or ideological capture.
4. **Technical scalability** — Architecture must support growth without proportional increase in manual effort (human oversight retained for resolution integrity in early phases).
5. **Sustainable resourcing** — Clear path to funding that preserves independence.

**Proposed OKRs (2026-06-08 to 2027-12-31)**

*Note: Baseline as of 2026-06-08 is 0 sign-ups. Phase 1 focuses exclusively on FIFA World Cup 2026 (English sources) to prove the core loop with high integrity before any expansion.*

**Objective 1: Validate demand and product-market fit**

- KR1.1: 500–1,000 unique “Express interest” sign-ups on the landing page by 2026-12-31 (stretch target: 5,000 if early traction accelerates).
- KR1.2: Net Promoter Score ≥ 35 from the first 100 engaged users (measured via survey; baseline measurement to begin once 50+ engaged users exist).
- KR1.3: At least 2 independent media or academic references to Trackrecord.info as a credible source by 2027-06-30.

**Objective 2: Achieve minimum viable coverage and data quality**

- KR2.1: 50+ high-quality resolved FIFA World Cup 2026 predictions (English sources) from ≥ 10 distinct figures by 2026-12-31, with strong progress toward broader targets in later phases.
- KR2.2: ≥ 95% of outcome linkages pass independent audit for source fidelity (first audit targeted by 2026-10).
- KR2.3: Average time from prediction publication to outcome resolution logging ≤ 30 days (rolling 90-day average; improve toward ≤ 21 days in later phases).

**Objective 3: Establish governance and operational foundations**

- KR3.1: Published, version-controlled verification methodology and editorial charter by 2026-09-30.
- KR3.2: Independent advisory board of ≥ 3 members with expertise in epistemology, data science, and journalism seated by 2026-12-31 (expand to ≥ 5 by mid-2027).
- KR3.3: Zero successful legal challenges or credible accusations of systematic bias in the first 12 months of public operation.

### 4. Scope and Boundaries

**In scope (MVP horizon — focused on proving core loop with integrity)**

- Collection, structured storage, and public display of FIFA World Cup 2026 predictions (English-language sources only).
- Systematic linkage of predictions to verifiable real-world outcomes with source citations and mandatory human review for resolution.
- Transparent methodology and audit documentation.
- Landing page and interest-capture mechanism.
- Basic public table of predictions and forecaster accuracy scores.
- Narrow initial topical focus on FIFA World Cup 2026 (English-language sources) to prove the core loop before any expansion.

**Out of scope (explicit boundaries for MVP)**

- Fact-checking of non-predictive claims (current events, historical assertions, value statements).
- Private or off-the-record predictions.
- **Fully automated scraping without human editorial oversight in the initial phase** (human review retained for all resolutions to protect verification integrity; automation limited to extraction prompts trained on gold-standard data).
- Real-time betting, prediction markets, or financial instruments.
- Legal liability for user decisions based on platform data.
- User-generated content moderation (separate workstream).
- Non-English language support before core English-language quality is proven.
- B2B or enterprise features prior to public beta stability.
- Broad international coverage or high-volume data ingestion before the core loop and small-scale demand are validated.

Any expansion beyond these boundaries will require a formal change-control process and an updated version of this document.

### Document Control

- **Version history**: v1.0 (2026-05-28) → v1.1 (2026-06-08) → v1.2 (2026-06-08) → v1.3 (2026-06-08) → v1.4 (2026-06-08) → v1.5 (2026-06-08)
- **Delta for v1.5 (Musk Algorithm simplifications)**:
    - Removed “Basic user accounts” and advanced “Search, filtering, and profile views” from MVP In-scope (deferred to later phases).
    - Simplified In-scope list to the absolute minimum needed to prove the core loop.
    - Slightly adjusted KR2.1 for realism in Phase 1 (WC2026 English focus).
    - Updated Evidence base reference and version/status accordingly.
    - Applied first three steps of Musk’s algorithm: questioned requirements, deleted non-essential features, and simplified scope for faster, higher-integrity execution.
- **Next scheduled review**: 2026-09-30 or upon reaching 500 sign-ups, whichever comes first.
- All changes must include a clear delta section and be validated against the original homepage statement.
- This document contains no subjective opinions — only evidence-based extensions of the publicly declared mission and current operational reality.

---

*Building transparent accountability for public predictions — starting from a clean, integrity-first foundation.*
