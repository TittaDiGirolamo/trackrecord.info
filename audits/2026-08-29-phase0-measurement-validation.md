# Phase 0 measurement validation log

**Status:** Instrumentation regenerated 2026-08-31. Live Plausible T-01–T-14 not yet run. Phase 0 remains **In progress**.  
**Prepared:** 2026-08-29  
**Updated:** 2026-08-31  
**Browser / device:** Generator grep + static HTML inspection in sandbox (not Plausible Realtime)  
**Content blocker:** n/a for static inspection  
**Plausible timezone (literal, from site settings):** not yet read  
**Snippet family observed after regen:** `https://plausible.io/js/pa-MQu87Y2WzO-sB_YzB2L-N.js` on homepage, `forecasters.html`, all 32 profiles, all 102 details  
**ASS-M-003 (properties tab shows status=resolved and status=pending):** unvalidated — requires Plausible dashboard  
**Fallback §7.3 adopted:** no

## Dataset note

`predictions_v2.jsonl` currently contains 102 records, all resolved, 0 pending. T-05 and the `status=pending` half of T-13 cannot be executed against a live pending page until a genuine pending record exists. Do not invent one.

Orphan test pages removed from the generated tree (not in `predictions_v2.jsonl`): `forecasters/person-test.html`, `predictions/pred-2026-08-01-test-france-wins-fifa-world-cup-2026.html`.

## Surface inventory

| ID | Result |
|----|--------|
| S1 | Homepage search suggestion — generator/index patched: `figure_selected` + `figure_id` from `f.slug` only; regex slug removed |
| S2 | Homepage search Enter — patched: fires `figure_selected` + `figure_id` only when a hit with slug exists |
| S3 | Homepage Top 3 — regenerated: `figure_id` on onclick |
| S4 | `forecasters.html` rows — regenerated: `figure_id` on onclick |
| S5 | N/A — control absent (prediction cards link to details, not profiles) |
| S6 | Instrumented: predictor name and “View updated profile” on detail pages fire `figure_selected` + `figure_id` |

## Static contract checks (T-08–T-12, T-10) after `regenerate_all.py`

| ID | Expected | Observed | Pass/Fail |
|----|----------|----------|-----------|
| T-01 | counts | requires Plausible | not run |
| T-02 | counts as one | requires Plausible | not run |
| T-03 | counts | requires Plausible | not run |
| T-04 | counts (no figure_selected required) | requires Plausible | not run |
| T-05 | does not count | no pending page in dataset | blocked (data) |
| T-06 | does not count | requires Plausible | not run |
| T-07 | does not count | requires Plausible | not run |
| T-08 | figure_id not figure | Top 3 and list emit `figure_id`; zero live `props.figure` | Pass (static) |
| T-09 | record slug, no regex | search uses `f.slug` only | Pass (static) |
| T-10 | contract survives regen | `python3 regenerate_all.py` + `ci/check_score_consistency.py` passed 2026-08-31 | Pass |
| T-11 | no double-fire | one `DOMContentLoaded` handler per profile/detail; one onclick per choice | Pass (static) |
| T-12 | evidence-trail sections present | resolved detail contains statement, source, criteria, primary evidence, status | Pass (static, Sutton Belgium group) |
| T-13 | properties visible | requires Plausible | not run |
| T-14 | official funnel last step matches T-01/T-04 vs T-05/T-06 | requires Plausible | not run |

Score consistency: **PASSED** (32 forecasters).

## Decision

Phase 0 status: In progress  
Defect if Blocked:  
Freeze timestamp if Pass:  
Next required human step: push this commit to `main`, then in Plausible register properties, create the two-step funnel, run T-01–T-14 in a real browser with the content blocker off.
