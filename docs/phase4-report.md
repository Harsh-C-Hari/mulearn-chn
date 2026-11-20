# Phase 4 report — Offers, Join & Footer

## Subphase 4.1 — Offers: content & structure
- Section `#offers` implemented between About and the Events stub; six cards with verified copy (Spec §7.1) and links from `data/links.js`.
- Distinction kept: heading label "Across the µLearn network"; lead states these belong to the wider µLearn ecosystem; CHN = campus doorway.
- Shared destination: Roadmaps and Challenges → `https://app.mulearn.org/dashboard/mujourney` (visible note under the grid).
- Checks: axe 0 violations at 320/390/768/1024/1440, no horizontal overflow, 0 console errors, 0 external requests, 20 keyboard tab stops all with visible focus outline, heading order OK, no-JS content visible, reduced motion OK.
- Link status: all six offer URLs + mulearn.org are client-supplied (Spec §8); live reachability of the three "link seen, target not opened" pages was not independently verified.

## Subphase 4.2 — Offers: visual & responsive refinement
- Composition: lavender field + Board 2 ink blob/sparkle/grid/squiggle; six colour-blocked cards (indigo, yellow, white, mint, coral, cream) in a 7/5 staggered tilted layout; corner stickers; ink info bar.
- Real-browser screenshots at 320/390/768/1024/1440 (`docs/screenshots/offers-*.png`) reviewed; no text/sticker overlap; no horizontal overflow (after fixing the unpositioned clip host).
- Responsive behaviour: 1 col <700, 2 col (light stagger) 700–1023, 12-col staggered ≥1024.
- Axe 0 violations ×5; 0 interactive targets <24px; keyboard 20 tab stops with visible outline; motion tests 17/17; CLS 0.001.

## Subphase 4.3 — Join section
- `#join` placed after the Events/Team/Memories stubs (master order kept); steps from Spec §7.6; destinations from `data/links.js`.
- Registration vs Discord distinction stated explicitly; no invented requirements.
- Screenshots `docs/screenshots/join-*.png` at 320/390/768/1024/1440 reviewed; 1024 layout rebalanced after CTA/email wrapping was seen in the screenshot.
- Axe 0 violations ×5; 0 targets <24px; no overflow; keyboard 28 stops with visible outline; motion tests pass.

## Subphase 4.4 — Footer
- `<footer>` with brand/association, six-link in-page nav (future sections kept), Discord/LinkedIn/Instagram/email tiles, official µLearn link, accurately-worded © line (flagged for client confirmation).
- Screenshots `docs/screenshots/footer-*.png` at all five widths reviewed; decoration collisions with the dashed rule / "Back to top" found in the 1440 screenshot and fixed.
- Axe 0 violations ×5; no overflow; 41 keyboard stops with visible outline; motion tests pass.

## Subphase 4.5 — Integration, QA and completion
- Integration tests (`scripts/test_phase4.py`, `docs/phase4-results.json`): 20/20 pass — canonical URLs, anchor landing below the sticky header, header nav order, section order, mobile menu at 390/768, µ hygiene, no invented stats.
- Final axe 0 violations ×5; no overflow; 0 console errors; 0 external requests; local Plus Jakarta Sans and GSAP 3.15.1 load; reduced motion and no-JS behave; motion tests 17/17; `verify_project.py` pass.
- Final screenshots: `docs/screenshots/full-{320,390,768,1024,1440}.png`.
- Open items for the client: confirm the © wording; LinkedIn/Instagram/email and the Mentors/Roadmaps/Challenges/Careers URLs are client-supplied and not independently verified live; Events/Team/Memories nav links land on empty anchors until Phases 5–7.
