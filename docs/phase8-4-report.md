# Phase 8.4 — Navigation, dialog & gallery interaction refinement

## Flow audit (all at 320/390/768/1024/1440)
Event dialog, gallery drawer + filters, lightbox, mobile menu were exercised by keyboard, touch emulation and mouse. Existing behaviour that already met the brief and was **left untouched**: showModal + inert page, Esc/Close/backdrop, Tab trap, focus restoration, body scroll lock, `panel.scrollTop=0` for event dialogs, cyclic prev/next + arrow keys, floating lightbox controls and their layering, mobile menu (Esc + focus return, outside/link close), sticky header, `aria-current`.

## Defects fixed
| # | Defect | Fix |
|---|---|---|
| F6a | Event dialog open/close GSAP tweens were not cancelled against each other | `killTweensOf(panel)` on open and close; verified 3 rapid open/Esc cycles at 5 widths leave no inline opacity/transform and focus on the trigger |
| F6b | Lightbox had no entrance motion (event dialog rises, lightbox only faded the backdrop) | Panel rises 16 px / 0.3 s with the shared easing (CSS, `prefers-reduced-motion:no-preference` only) |
| F6c | While the next photo loaded, the old photo sat under the new caption | `is-loading` dims the photo (opacity .55, size fixed by width/height → no shift); only the latest request clears it; verified after 24 rapid steps |
| — | Lightbox reopened at its previous scroll position | `panel.scrollTop = 0` on every opening (parity with event dialogs) |
| — | Filter changes were silent for screen readers | `#gallery-status` (`role=status`, visually hidden): "Showing 4 photos in Workshops" |
| F9 | Re-click during the 0.2 s close tween ignored | Left as is: unreachable (page is inert while the dialog is open) |

Correction to the 8.1 audit: the lightbox image's `transition:all` in F5 was the browser default (`all 0s`), not a rule. The real `transition:all` was on `.gallery-filter` (fixed in 8.3).

## Results — `scripts/test_phase8_dialogs.py` 70/70
Per width ×5: dialog rapid cycles, scroll reset, body lock, backdrop close, filter announcement, keyboard lightbox open + initial focus, every visible lightbox control hit-testable at its centre (layering), 24 rapid steps (image = counter, loading clears), Esc + focus return, lightbox reopen at top + scroll lock, Close button, zero console errors/overflow. Mobile menu 390: open, Esc + focus return, link tap closes + lands below header, sticky + `is-stuck`, `aria-current`, outside tap closes.
Regression: 8.2 suite 63/63 · 8.3 suite 26/26 · `test_phase4` 20/20 · `test_phase5` see state file (same single pre-existing failure as the original).
Files: `js/events.js`, `js/memories.js`, `css/sections/memories.css`, `index.html` (status region), `scripts/test_phase8_dialogs.py`.
