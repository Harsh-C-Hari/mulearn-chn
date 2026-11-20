# NEXT_PHASE.md — Phase 3 (Header / navigation + Hero + About)

> **Checkpoint:** Phase 2 is complete (`mulearn-chn_phase-02_complete.zip`). Do **not** start Phase 3 until the client says so.
> Read first: `docs/PROJECT_MASTER_SPEC.md`, `docs/PROJECT_STATE.md`, `docs/design-audit.md`, `docs/design-system.md`, `docs/accessibility-report.md`, `docs/ASSET_MAPPING.md`.

## What Phase 2 delivered (reuse, don't rebuild)
- `css/tokens.css`, `base.css`, `layout.css`, `components.css`, `decor.css`, `utilities.css`, `css/sections/styleguide.css`
- `img/ui/sprite.svg` (icons + stickers; inline per page with `python3 scripts/sync_sprite.py <page>.html`)
- `js/motion-guard.js` (lazy-loads vendored GSAP 3.15.1 + ScrollTrigger only when motion is allowed; sets `html.js-motion`)
- `styleguide.html` — the visual reference; copy its markup patterns for sections

## Phase 3 scope (from the master plan)
`index.html` assembly: skip link, header/nav (mobile menu), Hero ("Learn. Build. Belong." with the hero photo frame + stickers), About. Use `data/links.js` for every CTA. No animations beyond what `motion-guard.js` enables (Phase 8 owns the motion layer).

## Rules to keep
- Flat colour only; 2px navy lines; hard shadows; pill radius for buttons only; mono photos only on hero/About (C5-A).
- Text only on navy, cream, white, yellow, mint, lavender, coral or strong indigo (white). Never text on `#6366F1`.
- Every new page: run `scripts/run_audit.sh <page>.html` (axe + keyboard + overflow + network) and `scripts/audit_focus.py`; keep 0 violations.
- Never change verified team/event data. Deliver a versioned full ZIP after every subphase (`scripts/pack_checkpoint.py`) and a deployable ZIP (`scripts/pack_deploy.py`).

## Open items for the client
Satoshi font files (optional; drop into `fonts/` per the note in `tokens.css`); Phase 1 tier-3 content confirmations listed in `PROJECT_STATE.md`.
