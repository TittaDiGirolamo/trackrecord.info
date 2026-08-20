# Trackrecord.info — 90-Day Demand Validation Plan

**Version:** 1.1  
**Date:** 2026-08-20  
**Period:** 2026-08-20 → 2026-11-18  
**Status:** Active  
**Aligned to:** NORTH_STAR.md v1.0 (2026-07-29), 90-DAY_RETROSPECTIVE.md v0.1 (2026-08-19), Problem & Vision Document v1.5, EDITORIAL_CHARTER.md v1.0, REQUIREMENTS_Profile_Surface.md v1.0.0, REQUIREMENTS_Prediction_Detail_UI.md  

**Change from v1.0:**  
- Elevated measurement validation to a hard Phase 0 gate.  
- Pre-registered decision criteria and objective kill triggers.  
- Removed affective language from kill criteria.  
- Explicit requirement to update the NORTH_STAR initiative tracking table before any Medium+ work.  
- Constrained friction work to existing requirements documents.  
- Added operational boundary rules for visibility actions.  
- Added explicit note on reconciliation with Problem & Vision Document v1.5 demand OKRs.  
- Acknowledged statistical power limitations of the observed base rate and adjusted interpretation rules accordingly.

---

## 1. Overall Goal

Generate enough completed accountability lookups and structured qualitative feedback to produce an **evidence-constrained** decision on whether the current product delivers sufficient value to:

- continue in current scope,  
- execute a small, tightly scoped pivot,  
- move to maintenance mode, or  
- pause.

Primary metric: weekly completed accountability lookups, exactly as defined in NORTH_STAR.md §2.

A completed accountability lookup is a single browser session in which a user:

1. Selects or searches for a public figure (forecaster),  
2. Views that figure’s accuracy profile page,  
3. Opens at least one resolved prediction detail page that displays the full evidence trail (original statement + source, resolution criteria, primary evidence, and final status).

Only unique sessions that complete this full sequence count. Pending predictions never count. Direct landings on a resolved detail page count only if the corresponding profile is also viewed in the same session.

---

## 2. Hard Constraints

- Maximum 8–12 hours per week, executed in approximately 2-hour blocks.  
- No large new features, domain expansions, major engineering, or new surface requirements.  
- Preserve high verification integrity and the non-promotional stance defined in EDITORIAL_CHARTER.md.  
- Every initiative must state an explicit hypothesis linking to completed lookups (or a clear funnel step) **and** update the NORTH_STAR.md initiative tracking table **before** work begins.  
- Active initiatives ≤ 3 at any time.  
- The operational definition of the North Star metric and the instrumentation that measures it must be validated and frozen before any friction or visibility work begins.  
- All decisions rest exclusively on verifiable data and pre-registered rules. Subjective emotional states have no weight.

---

## 3. Success / Decision Criteria (Pre-Registered)

**By 18 November 2026 the following must exist:**

1. A frozen, versioned operational definition of “completed accountability lookup” together with a documented weekly extraction method.  
2. A baseline weekly average calculated over a minimum 14-day window after the measurement freeze.  
3. At least 8–12 pieces of structured qualitative feedback obtained from people who completed the full path (or a documented reason why fewer were obtained).  
4. A short decision memo that applies the matrix below and records the chosen terminal state.

### Decision Matrix

| Observed trajectory (relative to frozen baseline) | Qualitative feedback | Required decision |
|---------------------------------------------------|----------------------|-------------------|
| Sustained ≥ 3× baseline average for ≥ 4 consecutive weeks | Supportive or neutral | Continue current scope |
| Clear upward movement (≥ 2×) sustained for ≥ 3 weeks, or strong evidence of a single addressable bottleneck | Identifies a concrete, small pivot | Small pivot (must be scoped ≤ 1 Medium initiative) |
| No meaningful sustained movement after controlled visibility efforts (Phase 2 completed) | Weak, absent, or indicates fundamental lack of interest | Maintenance mode or pause |
| Instrumentation cannot be validated within 7 days of plan start | N/A | Immediate pause and reassess |
| Time budget exceeded in ≥ 3 consecutive weeks | N/A | Mandatory mid-point review; scope reduction required |

“Meaningful sustained movement” is defined as a clear directional change that cannot be explained by a single external spike or by measurement noise at the observed volume. Because the current base rate is low (\~1.25 completed lookups per week in the 28 days preceding the retrospective), pure quantitative thresholds alone have limited statistical power. The decision memo must therefore explicitly combine the quantitative trajectory with the substance of the qualitative feedback and the observed funnel drop-offs. Numbers alone that fall in a grey zone do not justify “continue”.

### Kill / Pause Triggers (Objective)

- Phase 0 (measurement validation) fails to reach Pass within 7 calendar days of plan start.  
- Zero completed lookups recorded in any 4-week window after Phase 2 visibility actions have been executed.  
- Time budget (8–12 h/week) exceeded in three consecutive weeks.  
- Any initiative begins without a written hypothesis and corresponding row in the NORTH_STAR tracking table.

---

## 4. Non-Goals

- Building an X/Twitter prediction-tracking engine.  
- Logging historical figures or economy/interest-rate predictions.  
- User accounts, advanced search, major UI redesigns, or new surface requirements.  
- Broad marketing or growth tactics that compromise the project’s non-promotional character.  
- Expanding the public Resolution Audit Trail (this remains an open question from the retrospective and is out of scope for this plan).  
- Reconciling or rewriting Problem & Vision Document v1.5 demand OKRs beyond a single explicit note (see §8).

---

## 5. Phases & Initiatives

### Phase 0 — Measurement Validation & Freeze (Hard Gate, Days 1–7)

**Goal:** Make the North Star metric trustworthy before any demand work.

**Required outcomes (all must pass):**

1. Confirm that the three required Plausible events (`figure_selected`, `profile_viewed`, `prediction_detail_viewed` with `status = "resolved"`) fire correctly under real browser conditions.  
2. Validate sequence counting with at least three synthetic sessions that deliberately complete and fail the path, plus a small number of controlled real sessions.  
3. Document the exact weekly extraction method (query, filters, uniqueness rule, handling of edge cases).  
4. Freeze the operational definition of a completed accountability lookup and record the freeze date and version in this plan and in NORTH_STAR.md if needed.  
5. Establish the baseline measurement window (minimum 14 days after freeze).

**Exit criterion:** Explicit written Pass recorded in the NORTH_STAR initiative tracking table.  
**No Phase 1 or Phase 2 work may begin until this gate is passed.**

**Hypothesis:** Reliable measurement is a necessary condition for any subsequent claim about demand.

### Phase 1 — Frictionless Core Path (Weeks 1–3, only after Phase 0 Pass)

**Focus:** Reduce friction in the final steps of the North Star sequence, strictly constrained to existing requirements.

- **Initiative A (Tiny/Medium):** Review and tighten the search → profile → resolved-detail path (copy, visual hierarchy, mobile behaviour, loading states). Work is limited to implementing or polishing against the already-written REQUIREMENTS_Profile_Surface.md and REQUIREMENTS_Prediction_Detail_UI.md. No new requirements may be introduced.  

  **Hypothesis:** Reducing friction in the final two steps will raise the conversion rate from profile view to completed lookup.  

  **Required before start:** Hypothesis + size classification written into the NORTH_STAR tracking table.

- **Supporting activity:** Maintain the simple weekly dashboard/view of the funnel created in Phase 0. No additional instrumentation work unless a critical defect is discovered.

**Exit criterion:** Explicit go/no-go decision based on whether conversion from profile_viewed to prediction_detail_viewed (resolved) shows any measurable improvement or whether residual friction is still the dominant observable bottleneck.

### Phase 2 — Controlled Visibility Experiments (Weeks 4–10)

**Focus:** Place the existing high-integrity record in front of people who already care about prediction accuracy or public accountability, without spam or hard promotion.

- **Initiative C (Medium):** Execute 4–6 light, factual distribution actions. Permitted channels are limited to:  
  – factual posts on the project’s own X account,  
  – personal network (already partially exercised),  
  – one short factual note to journalists or forecasting-interested individuals who have previously shown interest in accountability or prediction accuracy,  
  – carefully selected, non-promotional participation in existing relevant communities/forums only where the project’s neutral character can be preserved.  

  **Operational boundary rules:**  
  – Language must remain strictly factual and non-advocacy.  
  – No calls to action beyond “the record is public”.  
  – No repeated posting in the same venue within 14 days.  
  – Any engagement that risks debate or promotional framing is terminated.  
  – Total volume capped at 6 discrete actions.  

  **Hypothesis:** Reaching people already interested in prediction accuracy or public accountability will produce completed lookups and qualitative reactions that can be examined against the decision matrix.

- Optional tiny follow-ups only if a clear, measured funnel bottleneck appears and can be addressed within the remaining time budget without exceeding the active-initiative limit.

**Exit criterion:** Phase 2 actions completed and at least two full weeks of post-action measurement recorded.

### Phase 3 — Evidence Review & Decision (Weeks 11–13)

1. Compile weekly completed-lookup numbers, funnel drop-offs, and all qualitative feedback against the pre-registered decision matrix.  
2. Write a short decision memo that explicitly applies the matrix and records the chosen terminal state (continue / small pivot / maintenance / pause).  
3. Update the NORTH_STAR initiative tracking table with final results.  
4. Archive this plan and the decision memo in the repository.  
5. If a small pivot is chosen, the pivot itself must be scoped as a single Medium initiative with its own hypothesis before any further work begins.

---

## 6. Operating Cadence

- **Weekly (15–20 min):** Review completed lookups and the relevant funnel steps first. Update initiative status in the NORTH_STAR tracking table.  
- **Every 2-hour block:** One clear outcome only.  
- **End of each phase:** Explicit go/no-go decision recorded in writing.  
- **Mid-point check (approximately Day 45):** Confirm time budget remains sustainable. If the budget has been exceeded in two or more of the preceding four weeks, mandatory scope reduction is required before continuing.  
- **Phase 0 gate:** Must be closed with a written Pass before any later phase work is started.

---

## 7. Statistical Power and Interpretation Rules

The observed base rate prior to this plan is approximately 1.25 completed lookups per week (5 in the 28 days preceding the retrospective). At this volume, 13 weeks of data have limited power to detect modest effects.  

Therefore:

- Pure quantitative movement in a grey zone is not sufficient for a “continue” decision.  
- The decision memo must weigh the quantitative trajectory together with the substance and consistency of qualitative feedback and the observed funnel behaviour.  
- External calendar effects (World Cup timeline, media cycles) must be noted when interpreting spikes.  
- The plan deliberately accepts this limitation rather than inventing higher-volume tactics that would compromise the non-promotional character.

---

## 8. Reconciliation with Problem & Vision Document v1.5

Problem & Vision Document v1.5 still lists sign-up volume as the primary demand Key Result under Objective 1. The retrospective (2026-08-19) and this plan treat completed accountability lookups as the superior early demand signal.  

This plan does not rewrite Problem & Vision. It records the supersession for the duration of the 90-day period and requires that any later update to Problem & Vision explicitly address the change in primary demand signal. No other reconciliation work is in scope.

---

## 9. Closing Principle

The previous 90 days proved that the verification system works under published standards.  

These 90 days test, under the same methodological discipline, whether anyone wants what was built.  

All work serves that single question. Measurement must be trustworthy before any claim about demand is made. Decisions must be constrained by pre-registered rules rather than post-hoc interpretation.

---

*End of 90-Day Demand Validation Plan v1.1*