# Phase 0 — North Star Measurement Validation & Freeze

**Document Version:** 1.0.0  
**Date:** 2026-08-26  
**Status:** Ready for Implementation (Phase 0 still **In progress** until acceptance in §14)  
**Project:** trackrecord.info  
**Repo:** https://github.com/TittaDiGirolamo/trackrecord.info  
**Analytics:** Plausible (`trackrecord.info`)  
**Governing docs:** `NORTH_STAR.md` v1.0 (2026-07-29), `90-DAY_DEMAND_VALIDATION_PLAN_v1.1.md` (Phase 0 hard gate)  
**Initiative already in the tracking table:** Phase 0 — Measurement Validation & Freeze (`In progress`)

**Scope boundary:** This document covers **measurement definition, instrumentation contract, dashboard configuration, validation protocol, and weekly extraction**. It does not authorise UX redesign, visibility work, new product surfaces, scoring changes, dataset changes, or Problem & Vision OKR rewrites.

**Methodology:** Trackrecord Principles — Methodological Rigor, Granularity & Nuance, Zero-Assumption Validation, Strict Scope Discipline, Transparency & Independence, Evidence-Based Decisions, Long-Term Vision with Short-Term Discipline.

**How this version was produced:** The prior draft was interrogated with Musk’s first three production steps (question every requirement; delete every part that cannot justify itself; simplify what remains). Frozen decisions from that interrogation are in §3. Live-repo observations that justify those decisions are in Appendix A.

---

## 1. Purpose

Make the weekly North Star number a trustworthy count of one thing: whether a visitor, in a single Plausible visit, inspected a forecaster’s accuracy profile and opened at least one **resolved** prediction detail.

Until this document’s acceptance list is complete, no funnel conversion rate, no “1 completed lookup”, and no last-N-days unique-visitor figure may be treated as demand evidence.

Phase 1 and Phase 2 must not start until the Phase 0 row in `NORTH_STAR.md` is **Pass**.

---

## 2. Explicit Assumptions (Zero-Assumption Validation)

Every assumption is stated. None may be used as if proven.

**ASS-M-001: Plausible visit ≈ session for this volume**  
Assumption: At the observed volume (single-digit weekly unique visitors), Plausible’s visit / unique-visitor funnel count is an acceptable operational substitute for “unique browser sessions” as written in `NORTH_STAR.md` v1.0 §2.  
**Validation required:** Record the exact Plausible metric used (see §9). Do not claim the number is a raw session count. Re-open this assumption only if weekly unique visitors exceed 50 and repeat visits inside a week become material.

**ASS-M-002: Same-figure join is not enforceable in the Plausible funnel**  
Assumption: Plausible sequential funnels can require event order inside one visit. They cannot require `figure_id` on step 1 to equal `figure_id` on step 2. Mixed-figure paths (profile A + resolved detail B) will therefore count.  
**Validation required:** State this as a known overcount risk in `NORTH_STAR.md`. Do not invent a client-side compositor or a second analytics tool in Phase 0 to close it.

**ASS-M-003: Custom properties are available on the live plan**  
Assumption: The live Plausible site can store and filter custom properties (`figure_id`, `prediction_id`, `status`).  
**Validation required:** After one real page load of a resolved detail, Plausible → Goals → `prediction_detail_viewed` → Properties must show `status=resolved` (not only `(none)`). If properties are unavailable, Phase 0 is **blocked** unless the documented fallback in §7.3 is activated. Do not invent extra event names before that test is recorded.

**ASS-M-004: `status` on the event equals visible page status**  
Assumption: Generator logic `resolved` iff `outcome is not None` matches the status the visitor sees on the detail page.  
**Validation required:** Spot-check ≥ 3 resolved and ≥ 1 pending generated pages. Event `status` and on-page status label must match.

**ASS-M-005: Ad-blockers undercount; they do not redefine the metric**  
Assumption: Visitors with content blockers that strip Plausible produce silent misses. The North Star is “completed lookups among instrumented visits”, not “completed lookups among all humans”.  
**Validation required:** Record this limitation in the extraction method. Do not add a second tracker.

**ASS-M-006: Evidence-trail completeness is a page contract, not an event**  
Assumption: `NORTH_STAR.md` v1.0 prose requires the resolved detail to display original statement + source, resolution criteria, primary evidence, and final status. That cannot be observed from the event name.  
**Validation required:** One static template check (see §10, case T-12). Do not add events for each section.

**ASS-M-007: Calendar week uses the Plausible site timezone**  
Assumption: The Plausible site timezone is the week boundary.  
**Validation required:** Read the timezone from Plausible site settings and write the literal value into `NORTH_STAR.md` at freeze. Do not assume CEST, UTC, or the operator’s laptop timezone.

---

## 3. Requirements interrogation — frozen decisions

### 3.1 Question every requirement

| Prior requirement | Question | Frozen decision |
|---|---|---|
| Three-step sequence must include `figure_selected` | Does “selects or searches” measure the user outcome, or only one acquisition path? `NORTH_STAR.md` §2 lists selection first. The 90-day plan says a direct land on a resolved detail **does** count if the matching profile is also viewed. Those two texts conflict. Value delivered is profile + resolved evidence. Selection is a path. | **Counting rule = two events in one visit:** `profile_viewed` + `prediction_detail_viewed` with `status=resolved`. `figure_selected` remains mandatory instrumentation and a diagnostic funnel step. It is **not** required for a completed lookup. This is a documented amendment to `NORTH_STAR.md` §2, not a silent drift. |
| “Unique sessions” as the official unit | Plausible reports unique visitors on a funnel for a period, not a first-party session table. | Official number = unique visitors on the last step of the frozen funnel for the calendar week. Language in `NORTH_STAR.md` must stop saying “sessions” as if that table exists. |
| Unbounded “every way to select a figure” | An open-ended list is not testable. | Replace with a finite surface inventory (§8) produced from the live generators. Missing inventory item = defect. Surfaces that do not exist are not in scope. |
| Last-7-day traffic snapshot inside the requirements | The prior draft forbade using that window as a baseline, then embedded the numbers in the spec. | Deleted from this document. Dated observations belong in a validation log, not in a freeze spec. |
| Shared `window.trTrack` helper | A helper prevents name drift; it is not the measurement. | Optional implementation constraint, not an acceptance criterion. |
| 14-day baseline **inside** the 7-day Phase 0 window | Physically impossible. The plan mixed “freeze the definition” with “collect the baseline”. | Phase 0 Pass = definition frozen + instrumentation validated + extraction method written. The 14-day baseline **starts at the freeze timestamp** and is collected after Pass. |
| Funnel step 3 filtered by a global `status=resolved` dashboard filter | A global filter would shrink every step. | Forbidden. Filter exists only on the resolved-detail goal. |
| Kill date 2026-08-27 (7 days from plan start 2026-08-20) | This rewrite is dated 2026-08-26. Deploy + live validation cannot honestly finish inside the remaining calendar day. Passing by pretending would violate the plan’s own evidence rule. | Do not silently slip. Record an explicit time-box exception in the tracking table: Phase 0 Pass required by **2026-09-02**, reason = definition conflict between `NORTH_STAR.md` and the 90-day plan discovered during measurement validation. If Pass is not recorded by that date → pause and reassess, per the plan’s kill trigger, not a third silent extension. |

### 3.2 Delete every part that cannot justify itself

Deleted from the prior draft:

- Chat-ops “implementation notes for the executing chat”.
- Ephemeral Plausible snapshot (6 UV / 2→2→1 / 50% CR).
- “Any other homepage figure link” and “search UI on other pages if it can open a figure” as unbounded clauses.
- Requirement to fire `figure_selected` on browser back/forward (already correctly excluded; restated once).
- Separate `MEASUREMENT.md` unless `NORTH_STAR.md` becomes unreadable. Default: one new section in `NORTH_STAR.md`.
- Cosmetic cleanup of stale comments as an acceptance gate (do the cleanup; do not block Pass on comment text).
- Test cases that only restate another test.
- Any work whose sole purpose is to make last week’s incomplete instrumentation look complete.

### 3.3 Simplify what remains

1. One Plausible snippet on every generated page family.  
2. One property key for a figure: `figure_id`. The key `figure` is a defect.  
3. One official counting instrument: the funnel named in §9.  
4. One validation log, dated, with the cases in §10.  
5. One Pass / Blocked status in the tracking table. No third status such as “mostly working”.

---

## 4. Operational definition (to freeze)

### 4.1 Completed accountability lookup

A **completed accountability lookup** is one Plausible **visit** in which both of the following fire:

1. `profile_viewed`
2. `prediction_detail_viewed` with property `status` exactly equal to `resolved`

Pending details never count.  
Multiple resolved details in the same visit still count as **one** lookup.  
A direct land on a resolved detail counts **only if** `profile_viewed` also fires in that visit.  
A direct land on a profile that then opens a resolved detail **does** count.  
`figure_selected` is not part of the counting rule.

### 4.2 Weekly North Star number

**Source of truth:** Plausible funnel `Completed Accountability Lookup`, last-step unique visitors, period = calendar week in the Plausible site timezone (literal timezone written at freeze).

That number **is** weekly completed lookups for this project. No other query may be substituted.

### 4.3 What this number is not

- Not unique browser sessions in a first-party sense.  
- Not same-figure-guaranteed (ASS-M-002).  
- Not “lookups by people whose clients send events” plus “lookups by people whose clients block Plausible”.  
- Not proof that the evidence trail was read, only that the resolved detail page loaded.  
- Not demand evidence until freeze + the post-freeze baseline window exists.

### 4.4 Definition version

`completed_accountability_lookup` **v1.1** — counting rule as §4.1.  
Supersedes the three-event counting implication in `NORTH_STAR.md` v1.0 §2 and aligns the operational rule with the 90-day plan’s direct-landing clause.

---

## 5. Out of scope

- New pages, search UX, profile/detail redesign  
- Marketing / distribution / Phase 1–2 work  
- Expanding the audit trail  
- Changing scoring or prediction data  
- Rewriting Problem & Vision OKRs  
- Using any pre-freeze window as a demand baseline  
- Adding a second analytics vendor  
- Building a same-figure compositor  
- Collecting the 14-day baseline as a Phase 0 task (the window *starts* at freeze; collection is subsequent)

---

## 6. Event contract

Use these event names and property keys everywhere. Do not invent aliases. Do not send `figure` as a property key.

| Event | When to fire | Required props | Allowed values |
|---|---|---|---|
| `figure_selected` | User chooses a figure (click or search selection) **before** navigation to that figure’s profile | `figure_id` (slug) | Profile filename slug, e.g. `connor-o-halloran` |
| `profile_viewed` | Forecaster profile page has loaded | `figure_id` | Same slug |
| `prediction_detail_viewed` | Prediction detail page has loaded | `prediction_id`, `figure_id`, `status` | `status` is lowercase `resolved` or `pending` only |

Canonical calls:

```javascript
plausible('figure_selected', { props: { figure_id: 'connor-o-halloran' } });
plausible('profile_viewed', { props: { figure_id: 'connor-o-halloran' } });
plausible('prediction_detail_viewed', {
  props: {
    prediction_id: 'pred-2026-06-10-ohalloran-senegal-deep',
    figure_id: 'connor-o-halloran',
    status: 'resolved'
  }
});
```

**Identity rules**

- `figure_id` = profile filename slug (`forecasters/{slug}.html`). The value must come from the same slug function the generators already use. Client-side regex slugification on the homepage search is forbidden; use the slug already present on the forecaster record.  
- `prediction_id` = stable id used in the dataset and in the detail URL.

**Hard rules**

- Fire each event at most once per page load.  
- `figure_selected` is a choice event. Do not fire it on profile load, back/forward onto a profile, or a direct URL / Google landing on a profile.  
- Do not fire `figure_selected` for typing without a selection, or for a click that does not open a figure.  
- Guard every call: `if (window.plausible) { plausible(...) }`.  
- `status` must be taken from the record at generation time, never hardcoded, never `Resolved` / `RESOLVED` / `complete` / empty / omitted.  
- Tracking belongs in the **generator or template** (`regenerate_all.py` pipeline). One-off edits to live HTML are defects if the next regen wipes them.

**Known live contract breaks (must be gone before Pass)**

Observed 2026-08-26 on `main` / live pages:

| Location | Break |
|---|---|
| Homepage Top 3 (`scripts/generate_homepage_scorecards.py` and live `index.html`) | Sends `props.figure`, not `figure_id` |
| Homepage hero search | Sends `props.figure` from a client-side slug regex; also fires a separate `Search` event (diagnostic only; not part of this contract) |
| `forecasters.html` rows | Sends `props.figure`, not `figure_id` |
| Profile generator | Sends `profile_viewed` with `props.figure`; missing `figure_id` |
| Detail generator | Sends `prediction_detail_viewed` with `prediction_id` + `status`; **omits `figure_id`** |
| Snippet | Homepage uses `https://plausible.io/js/script.js`. Profiles and details use `https://plausible.io/js/pa-MQu87Y2WzO-sB_YzB2L-N.js`. Two snippets on one site is a defect |

The existing `Search` event may remain. It is not a North Star event and must not enter the official funnel.

---

## 7. Snippet, properties, fallback

### 7.1 Snippet

One snippet family on homepage, forecasters index, profiles, and details.

The live snippet must actually deliver custom properties on custom events. Confirm by test, not by reading a vendor marketing page.

### 7.2 Property registration

In Plausible site settings, register at least: `figure_id`, `prediction_id`, `status`.

After a real resolved-detail load, Goals → `prediction_detail_viewed` → Properties must list `status` values including `resolved` and, after a pending load, `pending`.

### 7.3 Fallback (only if ASS-M-003 fails)

If custom properties cannot be stored or filtered on the live plan:

1. Stop. Record Phase 0 **Blocked**: “custom properties unavailable”.  
2. Only then may a second event name be introduced: `prediction_detail_viewed_resolved`, fired **instead of** (not in addition to) `prediction_detail_viewed` on resolved pages. Pending pages keep `prediction_detail_viewed` with no resolved alias.  
3. The official funnel last step becomes that event.  
4. The fallback and the date it was adopted must be written into `NORTH_STAR.md` before any number is extracted.

Preferred path remains one event + property filter. The fallback is a recorded exception, not a convenience.

---

## 8. Finite surface inventory

`figure_selected` must fire on every surface in this table. If a row cannot be found in the repo, the row is removed from the inventory in the validation log — it is not left as an eternal “any other link” clause.

| ID | Surface | Generator / file | Required event |
|---|---|---|---|
| S1 | Homepage hero search: choosing a suggestion | `index.html` search handler | `figure_selected` + `figure_id` from record slug |
| S2 | Homepage hero search: Enter that resolves to exactly one figure | same | same |
| S3 | Homepage Top 3 / scorecards | `scripts/generate_homepage_scorecards.py` | `figure_selected` + `figure_id` |
| S4 | Forecasters index rows/cards | `scripts/generate_forecasters_list.py` → `forecasters.html` | `figure_selected` + `figure_id` |
| S5 | Prediction-list / table links that open a **figure profile** (not a detail) | `scripts/generate_prediction_tables.py` and any homepage module that links to `/forecasters/{slug}.html` | `figure_selected` + `figure_id` |
| S6 | Related-figure / other-figure blocks on profile or detail templates, if they exist | profile + detail generators | `figure_selected` + `figure_id` |

If S5 or S6 has no such control after a repo check, mark the row `N/A — control absent` in the validation log. That is not a defect.

`profile_viewed` on every page emitted by `scripts/generate_forecaster_profiles.py`.  
`prediction_detail_viewed` on every page emitted by `scripts/generate_prediction_details.py`, status from the record, `figure_id` present.

After `python regenerate_all.py`, a grep of the generated tree must show:

- `figure_id` on all three events  
- zero live `props:{figure:` or `props: {figure:` payloads  
- `status: 'resolved'` or `status: 'pending'` on every detail

---

## 9. Goals and funnel

Keep unfiltered diagnostic goals. Add one filtered goal for the counting last step.

**Goals**

| Goal | Event | Property filter |
|---|---|---|
| `figure_selected` | `figure_selected` | none |
| `profile_viewed` | `profile_viewed` | none |
| `prediction_detail_viewed` | `prediction_detail_viewed` | none (includes pending; diagnostic) |
| `prediction_detail_viewed (resolved)` | `prediction_detail_viewed` | `status` is `resolved` |

If fallback §7.3 is active, replace the last row with the fallback event and no property filter.

**Official funnel name:** `Completed Accountability Lookup`

| Step | Goal |
|---|---|
| 1 | `profile_viewed` |
| 2 | `prediction_detail_viewed (resolved)` |

Type: **Sequential** (other activity allowed between steps). Not strict-order-only-adjacent.

A separate **diagnostic** funnel may exist:

1. `figure_selected`  
2. `profile_viewed`  
3. `prediction_detail_viewed (resolved)`  

The diagnostic funnel is not the North Star.

Do **not** apply a global dashboard filter `status=resolved`.

---

## 10. Validation protocol

Run in a real browser with the content blocker off. Confirm in Plausible Realtime first, then in the funnel after the visit closes.

Record for every case: date (`YYYY-MM-DD`), browser, path, expected, observed, pass/fail. Store the log at `audits/YYYY-MM-DD-phase0-measurement-validation.md`.

### Counting cases

| ID | Path | Must count as completed lookup? |
|---|---|---|
| T-01 | Search or card → profile loads → open a **resolved** detail | Yes |
| T-02 | Same as T-01, then open a second resolved detail | Yes, still **one** |
| T-03 | Same as T-01 with an extra page in between (e.g. `/predictions.html`) | Yes (sequential funnel) |
| T-04 | Direct land on a profile → open a resolved detail (no `figure_selected`) | **Yes** under v1.1 |
| T-05 | Select figure → profile → open a **pending** detail only | No |
| T-06 | Direct land on a resolved detail; no profile in that visit | No |
| T-07 | Figure click that 404s / does not open a profile | No |

### Instrumentation cases

| ID | Check |
|---|---|
| T-08 | Homepage card click sends `figure_id`, not `figure` |
| T-09 | Search selection uses the record slug, not a local regex |
| T-10 | After `regenerate_all.py`, generated HTML still matches §6 |
| T-11 | No double-fire of any contract event on a single page load |
| T-12 | A resolved detail template contains original statement, source, resolution criteria, primary evidence, and final status (static read; not an event) |
| T-13 | Properties tab shows `status=resolved` and `status=pending` on `prediction_detail_viewed` (or fallback §7.3 is recorded) |
| T-14 | Official two-step funnel last step increments on T-01 and T-04 and does not increment on T-05 or T-06 |

Minimum volume: **three** synthetic visits that must count (include T-01 and T-04), **two** synthetic visits that must not count (include T-05 and T-06), plus at least one controlled real visit after deploy. Realtime observation is required before anyone calls the funnel “fixed”.

---

## 11. Weekly extraction method (to write into `NORTH_STAR.md`)

Procedure to freeze:

1. Open Plausible → Funnels → `Completed Accountability Lookup`.  
2. Set period to the calendar week. Timezone = the value recorded at freeze.  
3. Read unique visitors on step 2. That integer is the week’s North Star.  
4. Write the integer, the period dates, and the timezone into the weekly note. No mental arithmetic.

**Secondary diagnostics (may not replace step 3):**

- Site unique visitors for the same week  
- Unfiltered `prediction_detail_viewed`  
- Diagnostic three-step funnel (`figure_selected` → profile → resolved detail)  
- Conversion `profile_viewed` → resolved detail  
- Explore journeys that start on a profile or a detail  

**Edge handling:**

- `status` missing on a detail event → that event cannot enter the resolved goal. Treat as broken instrumentation, not as zero demand.  
- Property key typo (`figure` instead of `figure_id`) → broken instrumentation. Do not interpret an empty property breakdown as “nobody came”.  
- Pre-freeze dates → test data. Do not average them into the baseline.

**Baseline window:** starts at the freeze timestamp. Minimum **14 days**. No demand claim uses a shorter post-freeze window.

---

## 12. Docs / repo updates required for Pass

- `NORTH_STAR.md`: bump version; freeze date; timezone; property keys (`figure_id` only); official two-step funnel name; diagnostic three-step funnel name; extraction method; definition v1.1; ASS-M-002 overcount note; Phase 0 row → **Pass** or **Blocked** with the concrete defect.  
- `90-DAY_DEMAND_VALIDATION_PLAN_v1.1.md`: one short note that the operational counting rule is v1.1 (profile + resolved detail) and that Phase 0 Pass does not include finishing the 14-day baseline. Do not rewrite the plan.  
- Generators listed in §8: emit the contract; then `regenerate_all.py`.  
- Tracking-table exception for the Pass deadline: **2026-09-02**, with the reason in §3.1.

Do not start any other Medium initiative until that row is Pass.

---

## 13. Implementation constraints (not acceptance criteria)

These constrain how the work is done. Failure to follow them is sloppy, not a separate Pass item.

- Site remains static HTML from the Python generators.  
- Public site stays non-promotional; this work is invisible except for JS events.  
- A single shared helper is permitted if it reduces name drift. It is not required.  
- Do not patch one live card and call the surface done.

---

## 14. Acceptance criteria (all required)

- [ ] §4 definition v1.1 written into `NORTH_STAR.md` with freeze date and timezone  
- [ ] Surfaces S1–S4 fire `figure_selected` with `figure_id`; S5–S6 either fire it or are logged `N/A`  
- [ ] Every generated profile fires `profile_viewed` with `figure_id`  
- [ ] Every generated detail fires `prediction_detail_viewed` with `prediction_id`, `figure_id`, and lowercase `status` from the record  
- [ ] No live `figure` property key remains on contract events  
- [ ] One snippet family on homepage, index, profiles, and details  
- [ ] Regenerated HTML still contains the contract  
- [ ] ASS-M-003 passed, or fallback §7.3 recorded in `NORTH_STAR.md`  
- [ ] Goal `prediction_detail_viewed (resolved)` exists (or fallback event) and is official funnel step 2  
- [ ] Official funnel is the two-step funnel in §9  
- [ ] Validation log exists; T-01–T-14 recorded; pass/fail cases behave as specified  
- [ ] Extraction method written  
- [ ] Phase 0 row in `NORTH_STAR.md` set to **Pass**, or **Blocked** with a concrete defect  
- [ ] Time-box exception to 2026-09-02 written in the tracking table

Until that list is complete, do not treat funnel CR, completed-lookup counts, or unique visitors as demand evidence.

---

## Appendix A — Live observations used in this rewrite (2026-08-26)

These are evidence for the interrogation. They are not a baseline.

- Homepage snippet: `https://plausible.io/js/script.js` plus queue shim.  
- Profile and detail snippet: `https://plausible.io/js/pa-MQu87Y2WzO-sB_YzB2L-N.js`.  
- Homepage Top 3 and hero search send `props.figure`. Search also sends a `Search` event. Search slug is derived in the browser with a local regex.  
- `forecasters.html` row clicks send `props.figure`.  
- Profiles send `profile_viewed` with `props.figure`.  
- Details send `prediction_detail_viewed` with `prediction_id` and `status`, and omit `figure_id`.  
- `status` in the detail generator is `"resolved" if outcome is not None else "pending"`.  
- Generators involved: `scripts/generate_homepage_scorecards.py`, `scripts/generate_forecaster_profiles.py`, `scripts/generate_forecasters_list.py`, `scripts/generate_prediction_details.py`, orchestrated by `regenerate_all.py`.  
- `NORTH_STAR.md` v1.0 (2026-07-29) still describes a three-step sequence and “unique sessions”, and allows `figure_id (or slug)` as the property description — that parenthetical is what permitted `figure` to ship.  
- Custom properties on Plausible are a Business-plan feature. Whether the live site is on that plan is **unvalidated** (ASS-M-003).

---

## Appendix B — Alignment with existing quality system

This document does not alter `LOGGING_CHECKLIST.md`, `RESOLUTION_CHECKLIST.md`, or `EDITORIAL_CHARTER.md`. Those govern prediction integrity. This document governs whether the demand metric that *depends* on that integrity is itself countable.

---

*End of REQUIREMENTS_Phase0_Measurement.md v1.0.0*
