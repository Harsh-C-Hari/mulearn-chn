# NEXT_PHASE.md

> **Checkpoint:** Phase 5 Subphase 5.1 complete (`mulearn-chn_phase-05_subphase-01.zip`). **Next:** Subphase 5.2 — Featured event cards.

## 5.2 — Featured event cards (ODYSSEY, Buildathon, Build with AI)
Replace the placeholder featured markup in `scripts/build_events.js` with the real card (poster image in frame, title, concise verified descriptor, date where verified, "View details" button with `data-event`, `aria-haspopup="dialog"`). First repaint the Instagram "›" arrow in the ODYSSEY / Buildathon derivatives (see `docs/events-audit.md`). Then 5.3 compact entries, 5.4 dialogs (`js/events.js`, `<dialog>`), 5.5 integration QA. Do not start Phase 6.

## Open items for the client
© footer wording; unverified-live client URLs; Satoshi font files; Phase 1 tier-3 confirmations; Phase 5: Buildathon / Useless Projects / Web Slingers years; Build with AI location (Alappuzha vs CEC); ODYSSEY 32 h vs 24 h; Tech Forge details; Web Slingers venue/time reading.

## Rules to keep
Flat colour only; 2px navy lines; hard shadows; pill radius for buttons only; never uppercase text containing µ; stickers need a `position:relative` clip host; run `scripts/run_audit.sh index.html`, `scripts/test_phase4.py`, `scripts/test_phase5.py` after every change; regenerate cards with `node scripts/build_events.js`; ZIPs via `scripts/checkpoint.sh <name> <deploy-name>`.
