# Accessibility report — Phase 2.6

**Date:** 2026-11-20 · **Target:** WCAG 2.2 AA · **Page:** `styleguide.html` · **Tools:** axe-core (dev-only, not shipped) with tags wcag2a, wcag2aa, wcag21a, wcag21aa, wcag22aa and best-practice; custom Playwright scripts `scripts/audit_a11y.py`, `scripts/audit_focus.py`. Raw output: `docs/audit-results.json`, `docs/audit-focus.json`.

## Summary
| Check | Result |
|---|---|
| axe-core violations at 320 / 390 / 768 / 1024 / 1440 | **0 / 0 / 0 / 0 / 0** (after fixes below) |
| Keyboard: tab stops reached | 58 at 1440, 49 at 390 (nav collapses on mobile); no keyboard traps; every stop has a ≥2 px outline |
| Skip link | First Tab stop "Skip to content" → `#main`, target exists |
| Focus visible ring contrast (1.4.11) | minimum **3.27:1** against the adjacent surface across all stops, both widths |
| Focus not obscured by sticky header (2.4.11) | 0 obscured stops at 1440 and 390 |
| Target size (2.5.8) | 0 controls under 24×24 px; buttons 44–48 px |
| Semantics | `lang="en"`, one `<h1>`, 38 headings with **0 level skips**, one `<main>`, 3 `<nav>`s with labels, one `<footer>`, 0 images without `alt`, viewport meta present |
| Text contrast | All text pairings ≥ 4.5:1 (see table). Sub-AA pairings are listed in the styleguide only as labelled "fails" chips on a neutral surface |
| Reduced motion | `prefers-reduced-motion: reduce` → GSAP is **never requested**, `html.js-motion` absent, longest transition/animation 0.01 ms |
| No JavaScript | 7,595 characters of text rendered, 0 hidden sections (content never depends on JS) |
| Local fonts | Plus Jakarta Sans 400/500/600/700/800 loaded from `fonts/`; 0 Google/CDN requests |
| Local GSAP | GSAP 3.15.1 + ScrollTrigger load from `vendor/gsap/` when motion is allowed |
| Console | 0 errors/warnings at all widths |
| External network requests | 0 (all requests same-origin or `file://`) |
| Banned styling | no gradients, blur, backdrop-filter or soft shadows found in css/js/html |

## Defects found and fixed in 2.6
| # | Finding | Fix |
|---|---|---|
| A1 | `color-contrast` (serious): failing-pair demo chips rendered real text on sub-AA colours | Failing pairs now show a neutral white chip with a colour dot and "✗ fails" |
| A2 | `color-contrast` (serious): "Back to top" yellow button in the footer inherited cream link colour (1.38:1) from `.sg-footer a` | `.sg-footer a:not(.btn)`; `.btn` now sets its own colour (also for `:visited`) so ancestor link rules can never override a button |
| A3 | Hard shadow on buttons inside navy sections was navy-on-navy (invisible) | `.on-ink .btn` uses an indigo shadow |
| A4 | Focus ring on "Read more" inside the strong-indigo card was **1:1**, on the coral card **2.79:1** | Focus ring and the gap around it are now surface-aware custom properties (`--focus-ring`, `--focus-gap`): yellow on indigo/ink cards, navy on coral; the gap takes the card colour instead of always cream |

## Token contrast (computed from the hex values)
| Foreground on background | Ratio | Use |
|---|---|---|
| Navy on cream | 16.14 | body text |
| Navy on white | 17.85 | cards |
| Navy on yellow | 11.66 | accent buttons/cards |
| Navy on mint | 9.29 | mint cards/tags |
| Navy on lavender | 12.86 | Board 2 field |
| Navy on coral | 7.92 | coral card |
| White on strong indigo `#4F46E5` | 6.29 | primary button |
| Cream on navy | 16.14 | ink bands |
| Navy on indigo `#6366F1` | 4.00 | **not allowed for text** |
| White on indigo `#6366F1` | 4.47 | **not allowed for text** (use strong indigo) |
| Strong indigo ring on cream | 5.69 | default focus ring |
| Strong indigo ring on mint | 3.27 | focus ring (≥3:1) |
| Yellow ring on strong indigo | 4.11 | ring in indigo cards |
| Strong indigo ring on coral | 2.79 | **not allowed** → navy ring used |

## Limits of this audit
- Automated tools find roughly a third of accessibility issues. No screen-reader pass (NVDA/VoiceOver) was possible here; do one in Phase 9.
- Only Chromium was tested. Windows High Contrast / forced-colors mode was not tested.
- Only `styleguide.html` exists; every Phase 3+ page must be re-audited with `scripts/run_audit.sh <page>.html`.
