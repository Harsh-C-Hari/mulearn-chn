# Phase 8.3 — Micro-interaction refinement

## Audit → fix
| Gap found | Fix |
|---|---|
| Memories photo triggers (`.polaroid__action`, `.gallery-card__action`) had no pressed state on touch | `:has(...:active)` press (translate + shadow shrink; polaroid keeps its tilt via `rotate(var(--rot))`) |
| Text links, desktop `.nav-link`, footer list links, brand mark had no `:active` | Pressed states mirror their hover states (underline weight/colour, lavender underline, yellow rule, mark rotation) |
| Card press used the 0.3 s hover transition (felt laggy) | `a.card:active` uses `--t-fast` |
| `transition: all` on `.gallery-filter`; permanent `will-change:transform` on polaroids; transitions without shared easing | Explicit properties; will-change removed; `--ease-out` added |
| Default browser tap highlight showed on controls that draw their own press state | Suppressed **per component** (links, nav links, footer tiles/links, photo triggers, lightbox nav) — never globally; topbar-logo fix untouched |
| No `touch-action`, controls selectable on double-tap | `touch-action:manipulation` on `a, button, [role=button], summary, label` (pinch-zoom unaffected); `user-select:none` on control chrome only |

Unchanged on purpose: all `(hover:hover) and (pointer:fine)` gating, `:focus-visible` rings and `:has(:focus-visible)` lifts, existing `.btn`/footer-tile/lightbox pressed states.

## Results — `scripts/test_phase8_micro.py` 26/26 (settled-state comparison, transitions frozen)
Touch (390 mobile emulation): hover media false; for 8 control types, forced `:hover` changes nothing and forced `:active` does; tap highlight not global; logo suppression intact; `touch-action` set. Mouse: hover feedback present; zero `transition:all`; zero `will-change`. Keyboard: 45 consecutive tab stops all show a ≥2px ring, none under the sticky header, order follows the page.
Regression: `test_phase8_scroll` 63/63 · `test_phase4` 20/20 · `test_motion_home` PASS (CLS 0.0002).
Files: `css/components.css`, `css/sections/{memories,header,footer}.css`, new `scripts/test_phase8_micro.py`.
