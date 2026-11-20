# design-system.md — implementation reference (living document)

Direction: **Playful Neo-Brutalist Editorial** — Board 1 is the visual authority, Board 2 contributes additive vocabulary (decisions C1-B, C2-B, C5-A, C6-A in `PROJECT_STATE.md`). Flat colour only; 2px navy outlines; hard offset shadows; no gradients, blur, glass or 3D.

## Load order (every page)
```html
<link rel="stylesheet" href="css/tokens.css">    <!-- fonts + tokens -->
<link rel="stylesheet" href="css/base.css">      <!-- reset, element defaults, focus, reduced-motion -->
<link rel="stylesheet" href="css/layout.css">    <!-- containers, grids, splits -->
<link rel="stylesheet" href="css/components.css">
<link rel="stylesheet" href="css/decor.css">     <!-- stickers, edges, backdrops (2.4) -->
<link rel="stylesheet" href="css/utilities.css">
<body>
<!-- sprite:start --><!-- sprite:end -->           <!-- filled by scripts/sync_sprite.py -->
…
<script defer src="js/motion-guard.js"></script>
```

## Tokens (css/tokens.css)
Colour: `--c-bg #F8F3E9` · `--c-ink #0F172A` · `--c-primary #6366F1` (fill only) · `--c-primary-strong #4F46E5` (white text) · `--c-accent #FACC15` · `--c-mint #34D399` · `--c-surface #FFF` · `--c-lavender #DDD6FE` · `--c-coral #FB8F7C`.
Spacing `--s-0…--s-16` (4→128px). Radius 8/12/14 (+pill for buttons). Shadows `--shadow-1/3/5/6/7/9`. Type `--fs-hero/h2/h3/lead/body/meta/micro`. Z: deco 0 · content 1 · raised 10 · header 50 · dialog 100 · toast 200. Breakpoints 640 / 900 / 1024 / 1280 (literal in `@media`).

## Components (css/components.css)
`.btn` (+`--primary --accent --neutral --ink --sm --block`) · `.link` · `.nav-link` · `.card` (+`--yellow --mint --lavender --coral --cream --indigo --ink --flush --sm --lg --ticket`, `.card__num`) · `.photo-frame` (+tilt/mono/mat/backdrop) · `.polaroid` · `.section-label` · `.section-head` · `.tag` · `.meta` · `.divider` · `.band`.

## Decorative library (css/decor.css + img/ui/sprite.svg) — 2.4
**Sticker symbols** (`<svg><use href="#id"/></svg>` inside `.sticker`): `s-asterisk` `s-asterisk-6` `s-star` `s-sparkle` `s-triangle` `s-quarter` `s-slab` `s-blob-ink` `s-wedge-ink` `s-squiggle` `s-loop` `s-underline` `s-arc` `s-circle-diamond` `s-dots` `s-grid` `s-bolt`.
**Icon symbols** (inside `.icon`): `i-arrow-right` `i-arrow-up-right` `i-x` `i-menu` `i-chevron-left` `i-chevron-right` `i-mail` `i-external-link` `i-check` `i-calendar` `i-pin` `i-image`.
**Placement vars** on `.sticker`: `--x --r --y --b` (inline-start / inline-end / top / bottom), `--size`, `--rot`. Colour modifiers `.sticker--indigo|yellow|mint|lavender|coral|ink|cream`, `--outlined`, `--faint`, sizes `--xs…--xl`, `--hide-sm`. Opt-in idle motion `--spin`, `--bob` (CSS, only when motion allowed).
**CSS shapes:** `.deco-circle`, `.deco-ring`, `.deco-pill` (Board 2 ink swoosh). **Backdrops:** `.bg-dots`, `.bg-grid`. **Edges:** `.edge` (scallop) / `.edge--zigzag`, colour `--lavender|yellow|mint|ink|white|cream|indigo`. **Panels:** `.clip-diag`, `.clip-diag-r`, `.clip-slab`, `.ink-bar`, `.hl` (flat marker highlight).
Rules: decorations are `aria-hidden`, `pointer-events:none`, live in a `.deco-host`/`.section--clip` parent so they cannot cause horizontal overflow, and never carry content.

## Motion foundation (js/motion-guard.js + vendor/gsap/) — 2.4
GSAP 3.15.1 + ScrollTrigger vendored in `vendor/gsap/` (licence note + VERSION). `motion-guard.js` loads them **only** if the visitor has not requested reduced motion, then adds `html.js-motion`. Nothing is hidden by CSS; if JS or GSAP fails, content stays visible. API: `MULEARN.motion.ready | .reduced | .onReady((gsap, ScrollTrigger, mm) => …)`; events `mulearn:motion-ready`, `mulearn:motion-off`. Put animations inside `mm.add(…)` so they auto-revert. Verified by `scripts/test_motion.py`.

## Styleguide (styleguide.html + css/sections/styleguide.css) — 2.5
Open `styleguide.html` directly (file:// works; no server, no network). It loads the same seven stylesheets as any page plus `css/sections/styleguide.css`, which only adds page chrome (swatch blocks, spacing bars, and `.is-hover / .is-active / .is-focus` helpers that apply the exact component state values so states can be shown side by side). Edit components in `components.css`, never in the styleguide. After editing `img/ui/sprite.svg` run `python3 scripts/sync_sprite.py`.
Team portraits: photos are not cut-outs, so the coloured backdrop is a mat (`.sg-portrait`); promote it to `components.css` as `.portrait` in Phase 6.
Checks: `scripts/screenshot.py` (5 widths, overflow, console, network), `scripts/test_keyboard.py` (tab walk + focus ring), `scripts/test_motion.py` (3 motion scenarios).

## Focus tokens (added in 2.6)
`:focus-visible` draws a 3px outline (offset 3px) plus a 5px gap. Both follow the surface: `--focus-ring` (default strong indigo) and `--focus-gap` (default cream). `.on-ink` / `[data-surface="ink"]` switch to yellow ring + navy gap; `.card--indigo`, `.card--ink` use a yellow ring and `.card--coral` a navy ring; every `.card` sets its gap to its own fill. Rule: the ring must reach 3:1 against the adjacent surface. New coloured surfaces must set these two properties.
