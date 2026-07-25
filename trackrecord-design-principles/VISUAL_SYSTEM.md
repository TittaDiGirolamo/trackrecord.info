# Trackrecord.info — Visual system

Single source of truth for every public page (homepage, Predictions table, Prediction detail, Forecasters, future Share screen).

When a page diverges from this document, the document wins.

---

## 1. Foundation

### Typeface
- **Family:** Inter only
- **Weights allowed:** 400 (normal), 500 (medium) — **body text is always 400**
- **Weight 600 (semibold) is not used** anywhere — not on titles, not on labels, not on pills
- **Body / paragraph / evidence / verification / criteria / taglines / meta copy:** always `font-normal` (400)
- **Titles only** may use `font-medium` (500)
- Load: `Inter:wght@400;500`

### Colour tokens
| Role | Tailwind | Typical use |
|------|----------|-------------|
| Ink | `text-slate-900` | Titles, claim, body emphasis |
| Body | `text-slate-800` | Evidence, criteria, verification paragraphs |
| Secondary | `text-slate-600` | Taglines, forecaster name |
| Meta | `text-slate-500` | Published / Resolved / probability (mono) |
| Quiet | `text-slate-400` | Footnotes, data-source lines, statement ID |
| Accent | `text-emerald-700` / `hover:text-emerald-800` | All external source links |
| Eyebrow | `text-emerald-600` | Section labels (“Resolution criteria”, “High-visibility predictions”) |
| True | `bg-emerald-600 text-white` | Status pill (solid green) |
| False | `bg-rose-600 text-white` | Status pill (solid red) |
| Pending | `bg-amber-500 text-white` | Status pill (solid yellow) |
| Scorecard True | `bg-emerald-50` | Light green card background |
| Scorecard False | `bg-rose-50` | Light red card background |
| Scorecard Pending | `bg-amber-50` | Light yellow card background |
| Topic / Live | `bg-emerald-50 text-emerald-700` | Topic pill, Live pill |

### Radius
| Element | Class |
|---------|-------|
| Logo square | `rounded-lg` |
| Cards / soft panels | `rounded-2xl` or `rounded-3xl` |
| Pills | `rounded-full` |

### Case
- **Sentence case only** for every label, heading and nav item
- Never Title Case

### Borders
- **No grey horizontal rules or section borders** on content pages
- Spacing separates sections, not lines

---

## 2. Pills (one family)

All pills share the same structure. Only colour changes.

**Base structure**
```
inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-normal
```

| Pill | Classes |
|------|---------|
| **True** | `… bg-emerald-600 text-white` |
| **False** | `… bg-rose-600 text-white` |
| **Pending** | `… bg-amber-500 text-white` |
| **Topic** | `… bg-emerald-50 text-emerald-700` |
| **Live** | `… bg-emerald-50 text-emerald-700` (optional leading dot) |

**Version badge (v0.9)** — same visual weight, slightly larger padding so it can hold a pulse dot:
```
inline-flex items-center gap-x-2 px-3 py-1 rounded-full text-xs font-normal bg-white text-slate-600
```
(with optional `w-2 h-2 bg-emerald-500 rounded-full animate-pulse` inside)

Do not invent new pill shapes, paddings or font weights.

---

## 3. Typography scale

| Role | Classes | Example |
|------|---------|---------|
| **Page title / Claim** | `text-4xl md:text-5xl font-medium tracking-tight leading-tight text-slate-900` | Homepage hero, claim on detail page |
| **Section title** | `text-2xl md:text-3xl font-medium tracking-tight text-slate-900` | “Recent and notable claims” |
| **Tagline / forecaster name** | `text-lg font-normal text-slate-600 leading-relaxed` | Homepage subtitle, name under claim |
| **Body / evidence** | `font-normal text-slate-800 leading-relaxed` | Resolution criteria, primary evidence, verification note, claim cards |
| **Eyebrow / section label** | `text-sm font-normal text-emerald-600 mb-2` | “Resolution criteria”, “High-visibility predictions” |
| **Meta line** (Published, Resolved, probability) | `text-sm font-mono text-slate-500` | `Published: 6 December 2025` |
| **Footnote / data source** | `text-xs text-slate-400` | “Data source: predictions_v2.jsonl…” |
| **Statement ID** | `text-xs text-slate-400 font-mono` | `pred-2025-12-06-…` |

### Meta vs footnote (do not mix)

- **Meta lines** (dates, probability, statement ID) → `text-sm font-mono text-slate-500` (or `text-xs` for the ID only)
- **Footnotes** (data-source, “Scores calculated from…”, generation notes) → `text-xs text-slate-400`, **left-aligned**, never centred

Every footnote-style line on the site must use the same classes as:
```
Data source: predictions_v2.jsonl and resolved_details.jsonl (last major resolution batch 2026-07-21).
```
→ `text-xs text-slate-400` · left-aligned

---

## 4. Links

### External source links (Original source, Primary evidence source)
```
text-sm font-normal text-emerald-700 hover:text-emerald-800 transition-colors inline-flex items-center
```
- Always `target="_blank" rel="noopener noreferrer"`
- Always followed by the external-link icon (14×14 SVG arrow)

### Nav / internal links
```
font-normal text-slate-600 hover:text-slate-900 transition-colors
```

### Methodology / quiet text links
Same as external source links when they point off-site; same as nav when internal.

---

## 5. Navigation

Exact homepage structure on every page:

- Logo square (`w-7 h-7 bg-slate-900 rounded-lg`) + wordmark `text-lg font-normal tracking-tight text-slate-900`
- Desktop links: Predictions · Forecasters · Methodology
- Follow on X (desktop)
- Mobile hamburger + slide-down panel (same markup + toggle JS as homepage)
- No bottom border under the nav

Relative paths adjust per directory (`../` from `/predictions/`).

---

## 6. Prediction detail page — order of elements

1. Back link (“All predictions”)
2. **Scorecard** (status-tinted card: light green / red / yellow):
   - Forecaster name + status pill (solid green / red / yellow)
   - Literal claim (quotation marks, attribution brackets stripped)
   - Original source link ↗ (directly under the claim)
   - Real-world outcome text (only when resolved)
   - Primary evidence source link ↗ (directly under the outcome)
3. **Claim details** (merged claim details + outcome status, no doublings):
   - Published / stated probability / resolved / status as a borderless table, body text style (`font-normal text-slate-800`)
   - Topic pills
   - Resolution criteria
4. Verification (eyebrow + body)
5. Footer meta (footnote style)

No statement ID on the page surface (remains only in the audit-trail path).
No separate Primary evidence or Outcome status sections — those live in the scorecard / claim details.

Date format everywhere: `6 December 2025` (day + full month + year).

---

## 7. Explicit non-goals

- No second typeface
- No `font-semibold` / weight 600
- No Title Case labels
- No grey section borders or horizontal rules
- No centred footnotes
- No new pill colours without updating this document
- No inventing a “Reporter” label — only Predictor / forecaster name

---

## 8. Checklist before shipping a page

- [ ] Only Inter 400 / 500 — body text always 400 (`font-normal`)
- [ ] All pills use the shared base structure
- [ ] Section labels use the emerald eyebrow style
- [ ] Footnotes are `text-xs text-slate-400` and left-aligned
- [ ] Published / Resolved use `text-sm font-mono text-slate-500`
- [ ] External links have the icon and open in a new tab
- [ ] Nav matches homepage (including mobile)
- [ ] Sentence case throughout
- [ ] No grey lines

---

## 9. Forecaster Profile page

Layout (top → bottom):

1. Back link (“All forecasters”)
2. Section title **outside** the card: “Forecaster profile” (eyebrow, emerald)
3. Light-grey header block (`bg-slate-100 rounded-2xl`):
   - Deterministic initials badge (palette excludes the site primary emerald)
   - Name + subtitle “Public forecaster”
   - Overall score: numeric only if resolved ≥ 10; otherwise “Insufficient data”
   - Tracked / Resolved / Pending counts (no redundant “n = …” under the score)
4. Topic breakdown as short one-word pills (no borders); numeric topic score only if ≥ 5 resolved
5. Recent predictions (limit 8):
   - Statement in quotation marks
   - Outcome only via True / False / Pending pill + tinted card background (`bg-emerald-50` / `bg-rose-50` / `bg-amber-50`)
   - No numeric 0/100 next to the quote
6. Link to the full predictions table for this person
7. Neutrality + audit footer (methodology reference, data hash, permanent URL, copy-link)

### Directory (`forecasters.html`)

- Same nav and logo as `index.html` (T mark, Trackrecord.info wordmark, Follow on X)
- Card grid; whole card links to the Profile
- Same initials-badge colours and score thresholds as the Profile page
- Client-side name search; supports `?search=`

### Shared rules (already in this document)

- Inter 400/500 only; sentence case
- No grey horizontal rules or borders on pills/cards — spacing separates sections
- Status pill structure and colours unchanged
- Accent remains emerald; initials badges never use the primary emerald

*Living document. Update this file first, then the pages.*
