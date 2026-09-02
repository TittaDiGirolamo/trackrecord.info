# Baseline readout — 2026-09-02

**Window:** Phase 0 freeze 2026-08-31 20:31 Europe/Amsterdam → 14-day baseline ends 2026-09-14  
**Timezone:** Europe/Amsterdam (literal from Plausible: `(GMT+02:00) Europe/Amsterdam`)  
**Funnel:** `Completed Accountability Lookup` (sequential, other activity allowed)  
**North Star number:** last-step unique visitors = `prediction_detail_viewed (resolved)`  
**Operator:** Titta

Do not treat these figures as demand. Pre-freeze Goal totals (e.g. 24 profile views) remain out of scope.

## Extraction

Plausible → trackrecord.info → FUNNELS → Completed Accountability Lookup → unique visitors on the right-hand step.

## Snapshots 2026-09-02 ~19:24 Europe/Amsterdam

| Period | profile_viewed (unique) | Last-step unique (North Star) | Conversion | Notes |
|--------|-------------------------|-------------------------------|------------|--------|
| Today 2026-09-02 | 1 | **0** | 0% | Operator opened a profile during readout; did not open a resolved detail. Right-hand 0 is correct. |
| Last 7 days (rolling, includes **pre-freeze**) | 2 | **2** | 100% | **Contaminated window.** Includes days before freeze. Not the baseline. |
| **Freeze → now** (`2026-08-31`–`2026-09-02`) | 2 | **1** | 50% | **This is the running baseline.** Last-step 1 = 2026-08-31 T-01 operator test. Second profile visitor = operator on 2026-09-02, dropped off (correctly not counted). |

## Traffic sources (same readout)

**Organic search (Google/Bing) = 0 in both windows. Twitter = 0. GitHub = 0.**

### Freeze window 31 Aug – 2 Sep (site-wide, not funnel-filtered)

| Channel / source | Visitors | Interpretation |
|------------------|----------|----------------|
| Direct / None | 5 | Typed URL, bookmark, or referrer stripped. Netherlands 5, Chrome. Operator-dominated. |
| AI Assistants → Grok | 2 | Referrer from Grok (this chat’s links and/or Grok fetching the live site). Not unpaid search. Not demand. |
| Google / Bing / Twitter / github.com | **0** | No row. |

Countries: NL 5, Hong Kong 1, US 1. HK/US with Grok is consistent with AI/crawler infrastructure, not a reader in those countries.

Top pages match operator tests: `/`, Connor profile, Senegal detail, plus one Richards Spain detail.

### Last 28 days (includes pre-freeze; not the North Star)

| Channel / source | Visitors | Interpretation |
|------------------|----------|----------------|
| Direct / None | 45 | Still the entire human-looking pile. |
| AI Assistants → Grok | 1 | Same class as above. |
| Google / Bing / Twitter / github.com | **0** | No row. |

Countries: NL 24, US 7, Anonymous VPN 5, DE 2, UK 2.  
Browsers: Chrome 43, Safari 3 (Safari is the only weak hint of a second device/person).

Top pages 28d: `/`, `index.html`, `predictions.html`, `forecasters.html`, Richards Spain, Sutton, Connor, Öztürk, Rooney. Öztürk matches an Aug 15 operator X reply with that profile URL. Do not read that as inbound demand.

## How to read this

- Running North Star since freeze: **1 unique completed lookup**, and it is the tester.
- Organic completed lookups since freeze: **0**.
- Organic *search* visitors: **0** (not “unknown” — the Sources list has no Google row).
- “Direct” is not organic Google. It is mostly the operator, plus anyone who typed the URL or whose referrer was stripped.
- Grok-sourced visits during this chat are operator-adjacent. Do not count them as discovered demand.
- Next official weekly cell: calendar week 2026-08-31–2026-09-06, last-step unique visitors, taken on or after Sunday 6 Sep. Subtract the known operator T-01 when interpreting demand; do not delete it from Plausible.

## Operator rule (rest of baseline)

Do not open live profiles or resolved details “to check.” Plausible-only is enough. If you must use the site as a reader, note it on the next row.
