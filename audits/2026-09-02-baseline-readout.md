# Baseline readout — 2026-09-02

**Window:** Phase 0 freeze 2026-08-31 20:31 Europe/Amsterdam → 14-day baseline ends 2026-09-14  
**Timezone:** Europe/Amsterdam (literal from Plausible: `(GMT+02:00) Europe/Amsterdam`)  
**Funnel:** `Completed Accountability Lookup` (sequential, other activity allowed)  
**North Star number:** last-step unique visitors = `prediction_detail_viewed (resolved)`  
**Operator:** Titta (readout taken while 1 current visitor was on the site)

Do not treat these figures as demand. Pre-freeze Goal totals (e.g. 24 profile views) remain out of scope.

## Extraction

Plausible → trackrecord.info → FUNNELS → Completed Accountability Lookup → unique visitors on the right-hand step.

## Snapshots 2026-09-02 ~19:22 Europe/Amsterdam

| Period | profile_viewed (unique) | Last-step unique (North Star) | Conversion | Notes |
|--------|-------------------------|-------------------------------|------------|--------|
| Today 2026-09-02 | 1 | **0** | 0% | 1 current visitor during readout. Right-hand 0: no completed lookup today. Left-hand 1 is likely the operator (profile only). |
| Last 7 days (rolling, includes **pre-freeze**) | 2 | **2** | 100% | **Contaminated window.** Includes 2026-08-26…08-31 before property allowlist and freeze. Not the baseline. One of the two last-step uniques is the 2026-08-31 T-01 operator test. |
| Freeze → now (`2026-08-31`–`2026-09-02`) | — | **TBD** | — | Custom range not yet captured. Next readout should use this range, then weekly calendar weeks in Europe/Amsterdam. |

## How to read this

- **Today last-step = 0** is the honest post-freeze day-2 number (excluding Monday’s tester lookup, which sits on 2026-08-31).
- **Last 7 days last-step = 2** is not a weekly North Star. It mixes pre-freeze visits with the operator T-01.
- Next official weekly cell: calendar week 2026-08-31–2026-09-06, last-step unique visitors, taken on or after Sunday 6 Sep.

## Operator rule (rest of baseline)

Do not open live profiles or resolved details “to check.” Plausible-only is enough. If you must use the site as a reader, note it on the next row.
