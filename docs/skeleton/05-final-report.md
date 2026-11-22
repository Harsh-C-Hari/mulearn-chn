# µLearn CHN — Themed image skeleton system · Final report (Phase 6)

Verdict: **PASS with the limitations listed in §8.** Every check below was run in headless Chromium (Playwright) against the project served locally. Nothing was tested on real devices, real networks, Safari or Firefox.

## 1. The system
A skeleton is a temporary, decorative overlay (`.skel`, `aria-hidden`, `pointer-events:none`) drawn over the existing image box. Cream stock, 2px navy keyline where the real component has one, hard offset shadows only, small indigo/yellow/mint marks, no gradients/blur/shimmer. Colour tokens come from the existing design tokens. Large surfaces never animate; only small marks pulse or tilt (loops ≥1.8 s), all disabled under `prefers-reduced-motion`.

## 2. Variants implemented
Hero · About · Event poster · Event mini-thumb (own ratio per thumb) · Event-dialog photo · Team portrait (card-colour tint) · Team roster silhouette · Memories collage tile · Gallery thumb (category-toned) · Lightbox (in-flow, ratio from the incoming photo).

## 3. Files
`js/skeleton.js` (≈14 KB), `css/skeleton.css` (≈8 KB). No new assets, dependencies, or network requests. Tests and logs under `scripts/`, `docs/`.

## 4. Loading and failure behaviour
- Complete image → no overlay. Not yet complete → overlay after an 80 ms grace (lightbox: immediately). `load` → overlay removed. `error` → static failed state (no animation, no retry loop), alt text untouched.
- Lazy images get their overlay on init and lose it when the browser loads them. Lightbox: one overlay at a time, caption always equals the visible photo, rapid next/prev while pending is safe.
- JS off or `skeleton.js` blocked → no overlay, images behave exactly as before.

## 5. Responsive results (320/390/768/1024/1440)
51 skeleton boxes match their image boxes within 1 px at every width; no horizontal overflow (skeleton showing or loaded); CLS 0 when images arrive; lightbox skeleton ratio, caps and controls correct at all five widths. Two real defects were found by this test and fixed (see `04-implementation.md` §5.2).

## 6. Accessibility results
Overlays hidden from assistive tech, no text/title/desc, nothing focusable, tab walk never enters one; axe WCAG 2.2 AA: skeletons add 0 violations (390 page, 1440 lightbox); reduced motion → 0 skeleton animations at all five widths; forced-colours keeps solid borders on bordered variants.

## 7. Regression (this pass)
`test_skel_6_1`: normal / lazy-scroll / slow (400 ms) / failed loading; nav, team directory, event dialogs (open, Esc, reopen, no duplicate overlays), gallery filters (11/4/5/1/1), lightbox next/prev with skeleton showing; GSAP motion intact; reduced motion intact; 0 console/page errors; 0 external requests — all PASS at 390 and 1440. Existing suites with skeletons active: motion, home motion, 70/70 dialogs, 63/63 scroll, 26/26 micro, 25/25 final phase-8 QA, header test; resilience 39/39 on two clean runs (see limitation 2).
Performance (local server, informational): LCP 544 ms with skeleton vs 608 ms without — no measurable cost; skeleton footprint ≈22 KB raw.

## 8. Remaining limitations (not hidden)
1. Chromium only; no Safari/Firefox, no real-device or throttled-network testing.
2. One earlier run of the existing resilience suite failed a single check (ScrollTrigger blocked @1024, CLS 0.087 vs 0.02). The original 5.1 code passed 39/39 and the current code passed 39/39 on its next run; I did not reproduce the failure and did not find a skeleton-related cause, so I treat it as load-dependent flakiness of that scenario, but it was not proven.
3. `scripts/test_keyboard.py` is hard-wired to `styleguide.html` (`#focus`) and was not run against `index.html`; keyboard behaviour was covered by the 5.3 tab-walk and Phase 8 suites instead.
4. axe on the page without skeleton.js reports up to 11 contrast hits in About cards when sampled mid-entrance (existing GSAP fade); the check is "skeleton adds nothing", not "page is clean at that instant".
5. The 80 ms grace means a very slow-to-start image shows its cream image background for 80 ms before the overlay; boxes are reserved so nothing shifts.
6. Skeletons are not shown for images that were never given a `src` (nothing to wait for).
