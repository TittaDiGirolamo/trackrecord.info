# Phase 0 measurement validation log

**Status:** **Pass**. Frozen.  
**Prepared:** 2026-08-29  
**Updated:** 2026-08-31  
**Freeze timestamp:** 2026-08-31 20:31 **Europe/Amsterdam** (literal from Plausible General → Reporting timezone: `(GMT+02:00) Europe/Amsterdam`)  
**Browser / device:** Chrome, Windows, Incognito used for T-01/T-02/T-06/T-03; first property ingest in a normal window  
**Content blocker:** extensions reviewed/disabled for the live tests  
**Snippet family observed after regen:** `https://plausible.io/js/pa-MQu87Y2WzO-sB_YzB2L-N.js`  
**ASS-M-003:** `status=resolved` visible on Properties. `status=pending` not observable (0 pending records). `figure_id` and `prediction_id` visible on the same `prediction_detail_viewed (resolved)` event.  
**Fallback §7.3 adopted:** no

## Frozen counting rule

A completed accountability lookup is a unique Plausible visit that completes the sequential funnel **Completed Accountability Lookup**:

1. `profile_viewed`
2. `prediction_detail_viewed (resolved)` — custom event `prediction_detail_viewed` filtered `status is resolved`

Other activity between steps is allowed. `figure_selected` is diagnostic only. Direct landings on a resolved detail do not complete the funnel unless `profile_viewed` also fires in that visit.

Weekly extraction: Plausible → site trackrecord.info → period = calendar week in timezone Europe/Amsterdam → FUNNELS → Completed Accountability Lookup → last-step unique visitors.

## Dataset note

`predictions_v2.jsonl` contains 102 records, all resolved, 0 pending. T-05 and the `status=pending` half of T-13 cannot be executed until a genuine pending record exists. None was invented.

## Live tests 2026-08-31 (after property allowlist: `figure_id`, `prediction_id`, `status`)

| ID | Expected | Observed | Pass/Fail |
|----|----------|----------|-----------|
| T-01 | counts | Incognito: Connor profile → Senegal resolved detail. Funnel Today: 1 visitor both steps, 100% conversion | Pass |
| T-02 | counts as one | Same visit, F5 on detail. Funnel still 1 visitor both steps | Pass |
| T-03 | counts | Homepage Top 3 click fired `figure_selected` (Today: 1 unique / 1 total) | Pass |
| T-04 | event counts; lookup does not without profile | Direct resolved landing produced `prediction_detail_viewed (resolved)` with props; funnel unique lookups stayed 1 after T-01 only | Pass |
| T-05 | does not count | no pending page in dataset | blocked (data) |
| T-06 | does not count | Homepage-only Incognito; funnel remained 1 visitor | Pass |
| T-07 | does not count | not separately executed; homepage negative covered by T-06 | not run |
| T-08 | figure_id not figure | Live Properties: `figure_id` = `connor-o-halloran` | Pass |
| T-09 | record slug, no regex | search uses `f.slug` only (static + live figure_id) | Pass |
| T-10 | contract survives regen | `python3 regenerate_all.py` + `ci/check_score_consistency.py` passed 2026-08-31; live Pages served regenerated HTML | Pass |
| T-11 | no double-fire unique | T-02 unique stayed 1 | Pass |
| T-12 | evidence-trail sections present | live Senegal detail: statement, source, criteria, primary evidence, status | Pass |
| T-13 | properties visible | `status=resolved`, `figure_id=connor-o-halloran`, `prediction_id=pred-2026-06-10-ohalloran-senegal-deep`. pending half blocked (data) | Pass (resolved); pending blocked |
| T-14 | funnel last step matches T-01 vs T-06 | last step +1 on T-01, unchanged on T-06 | Pass |

Score consistency: **PASSED** (32 forecasters).

## Decision

Phase 0 status: **Pass**  
Defect if Blocked: T-05 / T-13 pending — no genuine pending prediction; do not invent one. Re-run those two tests when a real pending record is logged.  
Freeze timestamp if Pass: **2026-08-31 20:31 Europe/Amsterdam**  
14-day baseline window: starts at freeze timestamp (not part of Pass).  
Pre-freeze 28-day goal totals (e.g. profile_viewed 24) are **not** the North Star and must not be used as the baseline.

Next required human step: do not start Phase 1 until the NORTH_STAR table already shows Pass (this commit). Then run the 14-day baseline by reading the official funnel last step weekly. No Medium+ work without a new table row.
