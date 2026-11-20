# Responsive test report — Phase 2.6

**Date:** 2026-11-20 · **Page under test:** `styleguide.html` (the only page that exists before Phase 3) · **Browser:** headless Chromium (Playwright), served from localhost and from `file://`
**Reproduce:** `python3 scripts/screenshot.py styleguide.html docs/screenshots styleguide` and `scripts/run_audit.sh`

## Results

| Width | Horizontal overflow | Console errors/warnings | Non-local requests | Page height | Screenshot |
|---|---|---|---|---|---|
| 320 | none (scrollWidth 320) | 0 | 0 | 28,803 px | `docs/screenshots/styleguide-320.png` |
| 390 | none | 0 | 0 | 27,167 px | `docs/screenshots/styleguide-390.png` |
| 768 | none | 0 | 0 | 22,408 px | `docs/screenshots/styleguide-768.png` |
| 1024 | none | 0 | 0 | 17,594 px | `docs/screenshots/styleguide-1024.png` |
| 1440 | none | 0 | 0 | 18,243 px | `docs/screenshots/styleguide-1440.png` |

Interactive controls smaller than 24×24 px: **0** at every width. Primary buttons are 48 px tall (small variant 44 px).
Decorative stickers that deliberately bleed off the edge (`.sticker--hide-sm`, 768–1440) are clipped by their parent; the document never scrolls sideways (`scrollWidth == innerWidth`).

## Defects found and fixed in 2.6

| # | Width | Defect | Fix |
|---|---|---|---|
| R1 | 768 | Indigo asterisk sticker sat on top of the hero lead paragraph | Sticker position is now a custom property: 80% at <900px, 47% at ≥900px |
| R2 | 1024 | Yellow squiggle clipped the end of the lead text, then (after a first fix) hid half behind the photo | Moved at ≥1280px; hidden at 900–1279px where there is no clear gap |
| R3 | 1024 | Header nav (9 links) + CTA wrapped the CTA to two lines and crowded the bar | Nav now appears at ≥1180px (was 1024); CTA is `nowrap` at ≥640px only |
| R4 | 320 | Intermediate fix for R3 made the header overflow by 22 px | `nowrap` scoped to ≥640px; label may wrap below that. Caught by re-running the overflow check |

## Visual review
Contact sheets of the 320 px and 768 px full pages and close-ups of the 768/1024/1440 hero were reviewed. Typography scales with the fluid tokens, spacing follows the 8 px scale, and cards/buttons/frames/stickers stay consistent from 320 to 1440. The Board 1 + Board 2 mix (cream editorial base, lavender hero field with scalloped edge, colour-blocked cards, ink bands, hard 2px navy lines and offset shadows) holds at every width.

## Not tested (honest scope)
- Real devices and Safari/Firefox: only Chromium was available.
- Pages other than the styleguide: none exist until Phase 3.

## Phase 3 — index.html (header, hero, About)
Tested in headless Chromium at 320 / 390 / 768 / 1024 / 1440 (header also 1180). Results: `docs/screenshots/header-test.json`, `docs/audit-index.json`, `docs/screenshots/full-*.png`.
| Check | Result |
|---|---|
| Horizontal overflow (page) | none at any width; menu open or closed |
| Header | one row ≥1180px (nav on a single line at 1180 and 1440); disclosure panel below; 66px (<1024) / 78px (≥1024) tall; sticky top = 0 |
| Hero | stacked <900, split ≥900; no decoration on text at any width after fixes (mobile triangle, 1024 squiggle) |
| About | single column <900, card + tilted photo ≥900; fact tags wrap at 320/390 |
| Clipped decorations | slab/blob/grid extend past the viewport but are clipped by `.section--clip` (no scroll) |
Not covered: real devices, landscape phones, Safari/Firefox, zoom ≥200%.

## Phase 4 (Offers, Join, Footer) — responsive results
Tested in Chromium at 320 / 390 / 768 / 1024 / 1440 with `scripts/run_audit.sh index.html` (results: `docs/audit-results-phase4.json`) and screenshots (`docs/screenshots/{offers,join,footer,full}-*.png`).
- Horizontal overflow: none at any width. Console errors: 0. Non-local requests: 0. Interactive targets under 24px: 0.
- Offers: 1 column <700, 2 columns with light stagger 700–1023, 12-column staggered/tilted layout ≥1024. Stickers hidden or resized on small screens; none overlap text.
- Join: stacked (white story, then navy panel) <1024; diagonal-clipped split ≥1024 (1.15fr/1fr, 1.4fr/1fr from 1360). CTAs stay on one line from 1024.
- Footer: single column on phones (nav in 2 columns, tiles full width), 2 columns on tablet, 3 columns ≥1024.
- Defects found and fixed during QA: unpositioned clip host (false overflow), Join column ratio at 1024, footer decorations touching the dashed rule, 22–27px link targets.
- Not covered: real devices, Safari, Firefox.
