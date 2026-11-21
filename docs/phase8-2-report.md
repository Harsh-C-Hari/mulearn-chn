# Phase 8.2 — Scroll-based motion standardisation

## Before → after
| Topic | Before (8.1 finding) | After |
|---|---|---|
| Deep links (`/#team`, shared section URLs) | **Did not scroll** in normal-motion mode (CSS `scroll-behavior:smooth` vs ScrollTrigger refresh) — F1 | Land under the header at 320/390/768/1024/1440 (tested `#offers #team #join`). CSS smooth scroll removed; `js/nav.js` does smooth in-page scrolling (reduced motion = instant), updates the hash (Back works) and sets the focus starting point like native anchors. Skip link stays native. |
| Hero first paint | Visible at ~125 ms → hidden at ~286 ms → re-revealed (flash) — F2 | No flash. Inline head script (motion allowed only) pre-hides the hero via `html.pre-motion`, preloads GSAP, and **always** releases within 1.2 s; entrance tweens use `lazy:false` so release can't expose a frame. If GSAP is slower than 1.2 s the hero is left alone (no late re-hide). Never applies without JS / with reduced motion / GSAP failure. |
| Layout changes (gallery drawer, filters) | ScrollTrigger positions stale: Join/Footer reveals fired ~2.7 k px early, off-screen — F3 | `MULEARN.motion.refresh()` called after drawer toggle and filter change, **before** any smooth scroll starts. Footer trigger re-measured 11612 → 13655 in test. |
| Reveal vocabulary | start 70/75/85/88/90/92 %, y 12–64, 3 card idioms, stickers with differing pops — F4 | One token set `T` in `motion-home.js`: ease `power3.out`; blocks `.7s`/text `.5s`; rise 48 / 24 px; stagger `.08`; section timelines at `top 80%`, items at `top 90%`, footer `top 92%`; single sticker pop. Two helpers (`intro`, `rise`) replace eight bespoke blocks. Same selectors/same elements as before. |
| Leftover triggers | `once` only killed a trigger at its *end* (never at page bottom) | Each reveal kills its own trigger the moment it fires: 0 live ScrollTriggers after a full scroll. |
| Reduced motion in JS scroll | Drawer `scrollIntoView` always smooth — F7 | Honours `prefers-reduced-motion`. |

Not changed on purpose: F8 (runtime reduced→no-preference re-arm) — content stays fully visible, and replaying entrances on an OS-setting toggle would be worse than not.

## Files changed
`css/base.css` · `css/sections/hero.css` · `index.html` (head script) · `js/motion-guard.js` · `js/motion-home.js` (rewritten, same selectors) · `js/nav.js` · `js/memories.js` · tests: `scripts/test_phase8_scroll.py` (new), `scripts/test_phase4.py` + `scripts/test_phase5.py` (anchor tests now wait for the scroll to settle).

## Results
* `scripts/test_phase8_scroll.py` **63/63** — deep links ×15, no content hidden above viewport ×15, console clean ×15, hero flash ×2 widths, slow-GSAP release/no re-hide, reduced / GSAP-blocked / JS-off visibility, rapid scroll leaves 0 inline styles and 0 triggers, drawer refresh + smooth scroll, nav click (smooth, hash, focus, header offset), Back, reduced-motion instant jump, keyboard anchor focus/no section ring.
* `test_motion_home` PASS (CLS 0.0002) · `test_motion` PASS · `test_phase4` 20/20 · `verify_project` PASS · `test_phase5` 281/282 · `test_phase6` / `test_phase7`: **identical failures to the untouched original** (pre-existing "markup generated from data" / Phase 7 asset-data checks; not caused by Phase 8).
