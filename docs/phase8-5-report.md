# Phase 8.5 — Responsive motion & failure resilience

## Matrix (`scripts/test_phase8_resilience.py`, 39 checks, headless Chromium)
Six conditions × five widths (320/390/768/1024/1440) = 30 checks: **normal · touch emulation · reduced motion · GSAP blocked · ScrollTrigger blocked (init failure) · JavaScript disabled**. Each scrolls the whole page and asserts: no content left invisible, no stuck inline opacity/transform/visibility, no horizontal overflow, no console/page errors, CLS < 0.02, and — for the three failure/reduced modes — neither `js-motion` nor `pre-motion` is left on `<html>`. JS-off asserts all content visible with no overflow.
Plus: keyboard-only traversal ×5 widths (nav, all 7 event buttons, gallery toggle reachable) · gallery reopened ×5 (Enter on Next = 1 step; Space + ArrowRight = 2 more; lightbox stays open → no duplicated handlers) · event dialog ×8 open/close (one dialog node, clean styles) · resize 1440→390→1024→320→768→1440 during reveals · rapid scroll direction flips on touch 390.
**Result: all 39 pass** (run in two parts to fit tool time limits: 35 + 4; a single earlier CLS reading of 0.028 at 320 in the ScrollTrigger-blocked case did not reproduce — 16 further runs on both the original and this build measured 0).

## Defects found and fixed
| Defect | Impact | Fix |
|---|---|---|
| **Lightbox closed when Prev/Next (or any inner control) was activated by keyboard** (Enter/Space report click coordinates 0,0, which the backdrop check treated as "outside") — pre-existing since Phase 7.4 | Keyboard users could not step through photos with the buttons | Backdrop handler now acts only when the click target is the dialog element itself (`js/memories.js`) |
| No-JS fallback widened the page by 19 px at 320 px (CTA list item) | Horizontal overflow without JS | CTA wraps to its own full-width row (`css/sections/header.css`) |

Not an issue: with GSAP or ScrollTrigger unavailable, `pre-motion` and `js-motion` are cleared and everything is visible; reduced motion never downloads GSAP.
Regression: 8.2 suite 63/63 · 8.3 suite 26/26 · 8.4 suite 70/70 · `test_phase4` 20/20 · `test_motion_home` PASS (CLS 0.0002).
