# NEXT_PHASE.md

> **Checkpoint:** Phase 3 Subphase 3.6 complete (`mulearn-chn_phase-03_complete.zip`). **Phase 3 is COMPLETE. Next planned phase: Phase 4 — What µLearn offers + Join + Footer.** Do not start Phase 4 until the client says so.

## Phase 4 — Offers + Join + Footer
Replace the anchor stubs after About with `<section id="offers">` (6 official labels, staggered sticker cards, links from `data/links.js` `offers.*`), `<section id="join">` (split card, register + Discord CTAs, 3 verified steps, socials, email) and `<footer>`. Events, Team, Memories remain Phases 5–7: keep their stubs until then.

## Open items for the client
Satoshi font files; Phase 1 tier-3 confirmations; confirm Offers link label; hero/About photo choices (hero crop changed to 30% 100%, 10:9).

## Read first
`docs/PROJECT_MASTER_SPEC.md`, `docs/PROJECT_STATE.md`, `docs/design-system.md`, `docs/design-audit.md`, `docs/ASSET_MAPPING.md`, `docs/accessibility-report.md`, `docs/phase3-report.md`.

## Rules to keep
Flat colour only; 2px navy lines; hard shadows; pill radius for buttons only; mono photos only on hero/About; text only on navy, cream, white, yellow, mint, lavender, coral or strong indigo (white). Run `scripts/run_audit.sh index.html` after every change. Never change verified team/event data. Full ZIP via `scripts/pack_checkpoint.py`, deployable via `scripts/pack_deploy.py`.
