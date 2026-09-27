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

## 14-day close-out — 2026-09-14 ~19:17 Europe/Amsterdam

**Window closed.** Freeze 2026-08-31 20:31 → 2026-09-14, timezone Europe/Amsterdam.  
1 current visitor during readout (operator). Do not treat the 14 Sep dotted point as demand.

### Official baseline (the North Star)

| Period | profile_viewed | Last-step unique | Conversion |
|--------|----------------|------------------|------------|
| Week 1 (31 Aug–6 Sep) | 4 | **2** | 50% |
| Running (31 Aug–10 Sep) | 4 | **2** | 50% |
| **Full window (31 Aug–14 Sep)** | **6** | **2** | **33.3%** |

**Baseline last-step = 2 unique completed lookups in 14 days.**  
Of which known operator T-01 (31 Aug) = 1. Unattributed = 1.  
**Weekly rate (raw):** 1.0 last-step unique / week.  
**Weekly rate (minus known tester):** 0.5 / week.  
**Organic completed lookups (search or social referrer):** **0** (no Google/X/GitHub row in any snapshot).

10–14 Sep: profile_viewed 4 → 6; last-step stayed 2. Two more profile visits, both dropped off. Homepage `/` 18 → 23. Connor 4 → 6.

### Sources 31 Aug – 14 Sep (site-wide)

| Channel | Visitors |
|---------|----------|
| Direct | 17 |
| AI Assistants | 7 |
| Google / Bing / Twitter / GitHub | **0** |

Countries: NL 10, US 7, DE 2, HK 1, Serbia 1, Singapore 1, UK 1.  
Browsers: Chrome 16, Safari 7.

Safari 7 and non-NL countries are compatible with AI/crawler plus some other devices. They did **not** produce extra last-step completions.

### What this baseline is not

- Not “12 or 23 people got the core value.”
- Not a reason to claim demand, nor to claim the product is disproven (n is still tiny; discovery is zero).
- Not a reason to ship a new topic tonight.

## How to read this

- **14-day baseline is closed.** Last-step unique = **2**. Minus known operator = **1** unexplained completion. Search/social = **0**.
- Week 2 added homepage and profile traffic (Direct + Grok); it did not add completed lookups. Conversion 50% → 33% because the left box grew and the right box did not.
- Next step is a **written choice**, not a rebuild: Phase 1 friction (NORTH_STAR row first), pause/maintenance, or a scoped topic pivot (also a NORTH_STAR row first).

## Operator rule (closed window)

Baseline measurement window is finished. Further operator clicks still contaminate the weekly series; log them if they happen. Do not delete Plausible history.

## Phase 2 early readout — 2026-09-27

**Period:** `2026-09-21`–`2026-09-27` (custom range, Europe/Amsterdam). One day short of the scheduled 2026-09-28 cell.  
**0 current visitors** at readout.  
**Not a demand claim.**

| Funnel step | Unique visitors | Conversion |
|-------------|-----------------|------------|
| profile_viewed | **4** | 100% of funnel starters |
| prediction_detail_viewed (resolved) | **2** | **50%** |

**North Star for this window = 2 last-step uniques in 7 days.** Raw rate ~2/week, against baseline raw ~1/week and operator-adjusted ~0.5/week. n is too small for “moved the needle.”

Known contamination: operator phone walk 2026-09-21 ~19:46–19:48 Europe/Amsterdam is inside the window (Sutton search, profile, Japan detail). It is not separable from this screenshot. If that walk is one of the two completions, the unattributed rate is ~1/week, which is the raw baseline, not above it.

### Sources (site-wide, not funnel-filtered)

| Channel | Visitors | Notes |
|---------|----------|--------|
| Direct | 9 | Still the bulk. |
| AI Assistants | 2 | Same class as prior Grok/fetch traffic. Not search. |
| Organic Search | **1** | New row versus the baseline’s 0. One visitor is not a channel opening. |
| X / Twitter / GitHub | **no row** | Phase 2 action 1 did not appear as an X referrer. |

Visible top pages (screenshot truncated): `/` 9, `forecasters.html` 3, Connor profile 3, Adam Burke 2, Wayne Rooney 2, Sutton Argentina detail 2, Sutton profile 1, Tom Hamilton 1, `predictions.html` 1. Sutton Argentina detail (2) is higher than Sutton profile (1); detail-only landings do not count unless the profile is in the same visit. The official 2 already come from the sequential funnel, not from page totals. The Japan detail URL used in the X post is not in the visible top-page list; the list may be cut off, so do not record that page as zero.

Countries panel was partial: one view showed Netherlands 1, Singapore 1, United Kingdom 1; another showed Anonymous VPN 2, China 2, then cut off. Browsers: Chrome 11, Safari 1.

X post engagement at readout (not the metric): 6 views, 0 likes, 0 replies.
