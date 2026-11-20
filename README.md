# µLearn CHN website

Static site for the µLearn community at College of Engineering Chengannur: HTML, CSS, vanilla JS (classic scripts), vendored GSAP 3.15.1 + ScrollTrigger, self-hosted Plus Jakarta Sans. No build step, no CDN.

**Status:** Phase 2 (design foundation) complete. `styleguide.html` is the live design-system reference. `index.html` is assembled from Phase 3.

## Run locally
`python3 -m http.server 8000` then open `http://localhost:8000/styleguide.html` (or open the file directly).

## Start here (new session)
1. `docs/PROJECT_STATE.md` · 2. `docs/NEXT_PHASE.md` · 3. `docs/PROJECT_MASTER_SPEC.md` · 4. `docs/design-system.md`, `docs/design-audit.md` · 5. `docs/accessibility-report.md`

## Layout
`css/` tokens, base, layout, components, decor, utilities, sections · `js/` motion guard · `vendor/gsap/` · `fonts/` · `img/` (96 optimised derivatives + UI sprite) · `data/` (verified links, team, events, memories) · `reference/` (approved boards, not deployed) · `docs/` · `scripts/` (verification, audits, packing).

## Checks
`python3 scripts/verify_project.py` (assets) · `scripts/run_audit.sh [page.html]` (axe, keyboard, overflow, network; needs Playwright + axe-core, dev-only) · `python3 scripts/test_motion.py` · `python3 scripts/pack_checkpoint.py <name>` (full ZIP) · `python3 scripts/pack_deploy.py <name>` (deployable ZIP: no docs/scripts/reference/sources).
