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

## Week 1 official cell — 2026-09-06 ~20:04 Europe/Amsterdam

**Period:** `2026-08-31`–`2026-09-06` (custom range, Europe/Amsterdam)  
**North Star (last-step unique):** **2**  
**Known operator T-01 (31 Aug):** 1 of those 2  
**Unattributed last-step:** 1 — do **not** call this demand yet  

| Funnel step | Unique visitors | Conversion |
|-------------|-----------------|------------|
| profile_viewed | 4 | 100% of funnel starters |
| prediction_detail_viewed (resolved) | **2** | 50% |

Site-wide (not the North Star): 12 unique visitors, 13 visits, 42 pageviews. 1 current visitor during readout (treat 6 Sep dotted spike as operator).

### Sources week 1

| Channel | Visitors | Notes |
|---------|----------|--------|
| Direct | 9 | Still the bulk. NL 6. |
| AI Assistants | 4 | Same class as Grok (this chat / fetches). US 4 + HK 1 consistent with that. |
| Google / Bing / Twitter / GitHub | **0** | No row. |

Browsers: Chrome 9, Safari 3. Countries also: Serbia 1.  
New profile vs 2 Sep: `/forecasters/carl-anka.html` (1). Connor still the most-opened profile (4).

4 Sep and 5 Sep were **zero** uniques on the chart. Quiet days are the baseline, not the 12-visitor headline.

## Mid-window running total — 2026-09-10 ~19:40 Europe/Amsterdam

**Period:** `2026-08-31`–`2026-09-10`  
**North Star (last-step unique):** **2** (unchanged since week 1)  
1 current visitor during readout (operator).

| Funnel step | Unique visitors |
|-------------|-----------------|
| profile_viewed | 4 |
| prediction_detail_viewed (resolved) | **2** |

| Channel | Visitors | vs week 1 (6 Sep) |
|---------|----------|-------------------|
| Direct | 13 | 9 → 13 |
| AI Assistants | 6 | 4 → 6 |
| Google / X / GitHub | **0** | still 0 |

Homepage `/` visitors 12 → 18. Connor profile still 4; no new profile or resolved-detail rows. **6–10 Sep added visits, not completed lookups.**

## How to read this

- Week 1 North Star = **2** last-step uniques. Subtract the known operator test: **at most 1** unexplained completed lookup.
- 12 unique visitors is not 12 people who got value. Only 4 opened a profile; only 2 finished a resolved detail.
- Organic search/social still **0**. Direct + Grok is not a market.
- Next cell: Sunday **13 Sep** or Monday **14 Sep** (end of 14-day window), custom range **31 Aug – 13/14 Sep**, same two boxes + Channels.

## Operator rule (rest of baseline)

Do not open live profiles or resolved details “to check.” Plausible-only is enough. If you must use the site as a reader, note it on the next row.
