# Image Skeleton System — Phase 4/5/6 implementation log

Newest first. Each entry lists files, behaviour and the tests actually run.

## 6.1 — Full regression with skeletons active → `docs/skel-results-6-1.json` (all PASS); 6.2 — final report → `docs/skeleton/05-final-report.md`
- Test selector fix only (the mobile lightbox arrows are `display:none` at every tested width; desktop pair is used at all widths).

## 5.4 — Visual review of skeleton states (hero, about, team, memories; 390 + 1440)
Captures: `scripts/shot_skel_5_4.py` → `docs/screenshots/skel-5-4-{hero,about,team,memories}-{390,1440}.png` (all image requests held, gallery drawer open, lazy images forced to request).
- **Reviewed by eye:** hero (stage screen + audience dots + navy quarter, stickers, static yellow disc), about, team portraits (colour-blocked tint = card colour), memories collage and 11 gallery thumbs (taped frames, category-toned accents). No clipped or overlapping decorations, hard offset shadows only, cream stock + navy keyline, accent colour only on small marks.
- No code changes in this step. (The empty band between the collage and the gallery toggle in the memories capture is the existing scroll-reveal holding two polaroids at opacity 0 during the screenshot, not a skeleton issue.)

## 5.3 — Accessibility, keyboard, motion, failure & lightbox verification
Test: `scripts/test_skel_5_3.py` → `docs/skel-results-5-3.json` (all PASS). Screenshots: `skel-5-3-{lightbox-390,lightbox-1440,failed-390,forced-colors-1440}.png`.
- **Changes made because of what the tests showed**
  1. **80 ms grace before an overlay appears** (`GRACE` in `js/skeleton.js`). A cached image is often not yet `complete` when the script runs but is a frame or two away; the About skeleton lived 29 ms (a flicker). Now cached images never get an overlay; genuinely slow ones still get it after 80 ms. Boxes are reserved by `width/height`, so nothing shifts, and the image is never delayed. **Lightbox is exempt** (its stage collapses without the skeleton, so it appears from the first frame). `error` shows the failed state immediately.
  2. **Hero disc no longer pulses** (156 px fill breathing was too large for "restrained motion"). Rule now enforced by test: no animated skeleton element larger than 100×100 px; loops ≥1.8 s.
- **Verified:** overlays `aria-hidden`, no text/title/desc, nothing focusable, `pointer-events:none`, tab walk (66 stops) never lands in an overlay, alt/width/height untouched, accessibility tree has no skeleton content; axe WCAG 2.2 AA adds **0** violations vs. the same page without `skeleton.js` (@390) and 0 with the lightbox skeleton showing (@1440); reduced motion → 0 running skeleton animations at all five widths; JS off / `skeleton.js` blocked → no overlay, images normal, 0 page errors; forced-colours keeps a solid border; failed images → 51/51 static failed state, 0 animations, stable (no retry loop); slow image → skeleton → removed 0.09 s after bytes arrive; warm cache → 0 overlays created for in-viewport images; lightbox @320/390/768/1024/1440: skeleton ratio == photo ratio, within stage and ≤58vh, no overflow, controls not covered, rapid next×3 with all requests pending → exactly one skeleton and caption == new alt, after release no stuck state, Esc closes and focus returns to the trigger.
- **Note on the axe baseline:** the page *without* skeleton.js shows up to 11 contrast hits in the About cards when axe runs mid-fade of the GSAP entrance (timing artefact of the existing page, not the skeleton); the comparison is therefore "skeleton adds nothing", not "page is clean at that instant" (the full-page audit in `docs/accessibility-report.md` waits for the entrance).
- **Files:** `js/skeleton.js`, `scripts/test_skel_5_3.py`, `docs/skel-results-5-3.json`, screenshots. Tests 4.7, 5.1, 5.2 re-run after the change: PASS.

## 5.2 — Responsive verification (320 / 390 / 768 / 1024 / 1440)
Test: `scripts/test_skel_5_2.py` (Playwright/Chromium; held image requests → measure; release → CLS). Results: `docs/skel-results-5-2.json`, screenshots `docs/screenshots/skel-5-2-events-{320,390,768,1024,1440}.png`.
- **Found by the new geometry test (both were real, pre-existing):**
  1. **Event thumbs (`skel--mini`)** used one fixed 390:502 ratio but the four thumbs are 390×502 / 461 / 460 / 499 → skeleton up to ~16px off the real image. Now `setRatio()` (shared with lightbox/dialog) publishes each thumb's own `width/height` as `--skel-ar`; the overlay is `box-sizing:content-box` so the ratio applies to the same box the image's ratio applies to (image has a 2px border).
  2. **Team portraits (`skel--portrait`)**: `team.css` grows the photo mat from 4px to 8px at ≥600px, the skeleton inset stayed 4px → 4px too large per side at 768/1024/1440. Inset is now 8px from 600px.
- **Checked at every width:** skeleton box == image box (≤1px, 51 boxes measured with the gallery drawer open), no horizontal overflow (skeleton showing and after load), skeleton SVG never larger than its overlay, `hide-sm` decorations hidden <640px, **CLS 0** when images arrive, no skeleton left after load.
- **Files:** `js/skeleton.js`, `css/skeleton.css`, `scripts/test_skel_5_2.py`, `docs/skel-results-5-2.json`, `docs/screenshots/skel-5-2-*.png`.
- **Not covered here (next):** lightbox at all widths, keyboard/screen-reader, forced-colours, no-JS (5.3).

## 5.1 — Board-mix visual refinement (design pass over every variant)
Request: skeletons should feel like a **mix of the two reference boards** (`reference/ulearn_board-1…`, `…board-2…`).
- **Board 1 contributes:** colour-blocked cards (portrait skeletons are tinted with *their own card's colour* + a pale disc like the board's team cards), taped/tilted polaroid frames, sparkle + asterisk stickers.
- **Board 2 contributes:** heavy navy shapes (title bars, quarter-circles, the About "ink bar"), flat hard offset shadows under inner frames (no blur), indigo hard shadow on the dark lightbox stage.
- **Rules kept:** cream stock surface; tints are accent colour at low opacity (never a gradient, no new hex besides the two cream tints); strong colour only on small accents; large surfaces never animate; stickers *tilt* (±7°, 2.8 s) and accents *breathe*; mini + roster are static; everything off under `prefers-reduced-motion`.
- **Host-colour echo (automatic, no HTML change):** portraits ← `--card-bg`, roster ← `--mat`, poster art field ← event card `--card-bg`, mini ← `--tone`, gallery ← category tone, collage ← slot accent.
- **Bug found + fixed during review:** translucent tint showed the navy shadow rect through it → every frame now has an opaque cream base (`F()` helper).
- **Files:** `js/skeleton.js` (all variant templates + `F()`/`T()` helpers, `data-w` sticker flag), `css/skeleton.css` (tint/helper classes, tilt keyframes, host echoes, lightbox shadow), `scripts/test_skel_5_1.py`, `docs/skel-results-5-1.json`, `docs/screenshots/skel-5-1-lightbox-*.png`.
- **Tests:** 13/13 PASS (no gradient/blur/filter, hex budget, coverage counts hero 1/about 1/poster 3/mini 4/portrait 4/roster 21/collage 6/gallery 11, aria-hidden, computed tint colours vs real cards, motion on/off, lightbox skeleton at 1440 + 390). 4.7 suite re-run: PASS.

## 4.7 — Event-dialog photos (G2)
- **Files:** `js/skeleton.js` (new variant `dialog-photo`; `setRatio()` shared with the lightbox), `css/skeleton.css` (variant block), `scripts/skel_harness.py` (new test helper), `scripts/test_skel_4_7.py` (new), `docs/screenshots/skel-4-7-*.png`, `docs/skel-results-4-7.json`.
- **Behaviour:** photos created by `js/events.js render()` are attached by the existing dialog `MutationObserver`. Slow → overlay; cached/already loaded → no overlay; failed → static failed state. The overlay is locked to the photo's own ratio (`--skel-ar` from `width/height`) because the 2-column grid can make the figure taller than its image. The dialog **poster** intentionally has no skeleton (same URL as the card poster, already cached).
- **Tests (Playwright/Chromium, held / failed / normal requests):** one skeleton per photo, box == image box (<1px), aria-hidden + pointer-events none, alt kept, no duplicates on re-open, no skeleton for events without photos, removed after load, none for cached re-render, failed state static, 320px geometry + no overflow, 0 console errors → **14/14 PASS**.
