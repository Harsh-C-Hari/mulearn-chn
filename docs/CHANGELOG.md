# CHANGELOG.md

Format: newest first. Each entry: date · phase · what changed · files · verification.

## 2026-11-20 — Phase 2 / Subphase 2.6 (final responsive & accessibility audit) — PHASE 2 COMPLETE
- Added: `docs/responsive-report.md`, `docs/accessibility-report.md`, `docs/screenshots/styleguide-{320,390,768,1024,1440}.png`, `docs/audit-results.json`, `docs/audit-focus.json`, `scripts/audit_a11y.py`, `scripts/audit_focus.py`, `scripts/run_audit.sh`, `scripts/pack_deploy.py`.
- Fixed (a11y): failing-contrast demo chips; yellow footer button inheriting cream text (1.38:1); invisible navy shadow on buttons in ink sections; focus ring 1:1 on indigo card and 2.79:1 on coral card (now surface-aware `--focus-ring`/`--focus-gap`).
- Fixed (responsive): hero asterisk over lead text at 768; squiggle clash at 1024; header CTA wrapping at 1024 (nav now from 1180px); 320px overflow introduced and caught during the fix.
- Fixed (tooling): `verify_project.py` hard-coded `D:\` path (H1); removed duplicate root `ASSET_MANIFEST.md`, `ASSET_MAPPING.md`, `LICENSE-PlusJakartaSans.txt` (H3, byte-identical copies remain in `docs/` and `fonts/`); replaced stale `pack_bundles.py`.
- Verified: see `docs/accessibility-report.md` (axe 0 violations ×5 widths, 58 tab stops, min focus-ring contrast 3.27:1, 0 console errors, 0 external requests, reduced-motion + no-JS OK), `verify_project.py` PASS (96 derivatives), `test_motion.py` PASS.

## 2026-11-20 — Phase 2 / Subphase 2.5 (styleguide)
- Added: `styleguide.html` (hero on lavender field with scalloped Board 2 edge, ink jump bar, 10 sections: colour with computed contrast chips, typography specimens, spacing scale, borders/radii/shadows, buttons × states (default/hover/pressed/focus/disabled) for accent/neutral/indigo plus sizes, links, nav links, cards (colour-blocked, numbered, link, ticket, media with real event art, tags, dividers), image frames (mono tilt, coloured mats, caption bar, team portraits on coloured mats, polaroid collage from real photos), stickers (two composed fields + full index of 15 shapes), responsive grids (breakpoints, spans, auto-fit/stagger, editorial split), focus-visible demo incl. on-ink; closing Join banner rebuilt from Board 1), `css/sections/styleguide.css` (page chrome only), `scripts/test_keyboard.py`.
- Fixed during review: links on `.card--ink` / `.card--indigo` inherited navy (invisible / 2.84:1) → now inherit card text colour; screenshot script now forces lazy images to load; 320px overflow in button matrix and spacing rows; ink button demo placed on an ink surface (invisible) → moved.
- Verified (headless Chromium): overflow none at 320/390/768/1024/1440; 0 console errors; 0 external requests; keyboard walk: 58 tab stops, 0 without a visible ≥2px focus ring; `test_motion.py` PASS on the styleguide; no gradient/blur functions in any CSS. Visual review of all sections at 1440 plus mobile layout metrics.

## 2026-11-20 — Phase 2 / Subphase 2.4 (decorative library & GSAP foundation)
- Added: `img/ui/sprite.svg` (12 icons + 17 flat stickers), `scripts/sync_sprite.py` (inlines the sprite into pages between `sprite:start/end` markers, C9-B), `css/decor.css` (sticker wrapper + colour/size modifiers, CSS shapes, dotted/grid backdrops, scallop/zigzag edges, clip panels, ink bar, flat highlight), `vendor/gsap/{gsap.min.js,ScrollTrigger.min.js,LICENSE,VERSION}` (GSAP 3.15.1), `js/motion-guard.js`, `scripts/test_motion.py`, `scripts/pack_checkpoint.py`, `docs/decor-sheet.html` (dev reference), `docs/design-system.md`.
- Changed: `.sticker` wrapper moved from `components.css` to `decor.css` (now supports end/bottom placement).
- Verified (headless Chromium): `test_motion.py` PASS in 3 scenarios — normal (GSAP 3.15.1 + ScrollTrigger load locally, `html.js-motion` set), reduced-motion (GSAP never requested, class absent), GSAP blocked (class absent, 0 hidden elements, page intact). 0 external requests. Sprite XML valid; decor sheet reviewed visually. No page animations implemented.

## 2026-11-20 — Phase 2 / Subphase 2.3 (layout & components)
- Added: `css/layout.css` (containers, sections incl. colour variants, 4/8/12 grid, auto grids, splits, editorial, stack/cluster), `css/components.css` (buttons primary/accent/neutral/ink/sm with all states, text link, nav link, cards: outlined, yellow/mint/lavender/coral/indigo/ink/cream, numbered, ticket, flush; photo frames incl. tilt/mono/backdrop/mat; polaroid; section label/head; tags; meta; divider; bands; sticker wrapper; prose), `css/utilities.css`, `scripts/screenshot.py`.
- Verified (Chromium, 320/390/768/1024/1440): 0 horizontal overflow, 0 console errors, 0 external requests; visual review of 1440 render. Fixed frames/polaroids stretching in grids (align-self:start). Removed a gradient-based divider (forbidden).

## 2026-11-20 — Phase 2 / Subphase 2.2 (tokens & typography)
- Added: `css/tokens.css` (3-layer tokens: primitive → semantic; colour, spacing, radius, hard shadows, type scale, layout, motion, z-index, breakpoints doc), `css/base.css` (reset, element defaults, focus-visible, skip link, sr-only, dialog scroll lock, reduced-motion), `fonts/PlusJakartaSans-{400,500,600,700,800}.woff2` + OFL licence + `fonts/README.md`.
- Decisions applied: C1-B (lavender #DDD6FE, coral #FB8F7C), C2-B (pill radius for buttons only), C5-A (opt-in mono photos, later), C6-A (Satoshi fallback).
- Verified (headless Chromium, file://): Plus Jakarta Sans 400/700/800 load locally, µ glyph present, h1 resolves display stack, 0 external requests, 0 console errors, no horizontal overflow at 1440. Satoshi uses local() only to avoid 404s.



## 2026-11-20 — Phase 2 / Subphase 2.1 (design audit)
- Added: `docs/design-audit.md` (reference analysis of two boards, mix strategy, conflicts C1–C12, implementation plan 2.2–2.6, reuse inventory, approvals needed).
- Added: `reference/ulearn_board-1_bold-playful_APPROVED.png`, `reference/ulearn_board-2_neo-brutalist_MIX.png`, `reference/SHA256SUMS.txt`.
- Updated: `docs/PROJECT_STATE.md`, `docs/NEXT_PHASE.md`.
- Verified: project structure inspected; npm availability of gsap 3.15.1 and Plus Jakarta Sans 5.3.0 confirmed; ZIP integrity tested. `verify_project.py` could not run (hard-coded path) — see state file.
- No design code written.

## 2026-11-20 — Phase 1 (Asset pipeline & content data)
- Added: Complete derivative image pipeline producing 96 optimized WebP, JPEG, and PNG images across `img/{hero,about,events,team,memories,brand,og}/`. Total asset weight 4.17 MB (down from 88 MB originals).
- Added: Data modules `data/links.js`, `data/team.js`, `data/events.js`, `data/memories.js` attached to `window.MULEARN` with explicit `verified` flags and zero invented facts.
- Added: `docs/ASSET_MANIFEST.json` and `docs/ASSET_MANIFEST.md` containing exhaustive file inventory, SHA-256 hashes, crop rectangles, dimensions, and usage tags.
- Added: Automation scripts `scripts/build_assets.py`, `scripts/extract_embedded.py`, `scripts/extract_frames.py`, `scripts/verify_project.py`, `scripts/generate_contact_sheet.py`.
- Added: Visual contact sheet at `docs/asset-review.html` for complete visual QA.
- Updated: `docs/ASSET_MAPPING.md` with final resolved asset-to-section mappings.
- Updated: `docs/PROJECT_STATE.md` (Phase 1 marked complete, decisions logged).
- Updated: `docs/NEXT_PHASE.md` detailing Phase 2 scope and requirements.
- Verified: All 96 derivatives verified with `scripts/verify_project.py` (0 errors, 0 warnings). Zero upscaling. All EXIF and GPS tags removed. EXIF orientation corrected for Al Ameen (code 6). All file size budgets met.

## 2026-11-20 — Phase 0 (planning)
- Added: `docs/PROJECT_MASTER_SPEC.md`, `docs/PHASE0_REPORT.md`, `docs/PROJECT_STATE.md`, `docs/CHANGELOG.md`, `docs/NEXT_PHASE.md`, `docs/ASSET_MAPPING.md` (copied from Stage 02).
- Added: `reference/ulearn_prototype_v1_UNMODIFIED.html` (byte-identical copy of the approved prototype).
- Changed: nothing else. No site code written. No assets moved or renamed.
- Verified: official sources (mulearn.org pages, register page, CHN Discord); prototype rendered in headless Chromium at 390/820/1440; WCAG contrast ratios computed.
