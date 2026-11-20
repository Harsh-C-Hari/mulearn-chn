# NEXT_PHASE.md

> **Current Checkpoint:** Phase 7 complete (`mulearn-chn_phase-07_complete.zip`, deployable `mulearn-chn_phase-07_deploy.zip`). **Next:** Phase 8 — Motion Layer Integration & Sitewide Refinement.

## Phase 7 — Memories & Gallery (COMPLETE)

| Subphase | Name | Scope | Status |
|---|---|---|---|
| **7.1** | **Memory Asset Audit & Section Structure** | Comprehensive audit of 11 gallery items & 6 collage mappings in `data/memories.js`, exclusion of promo graphics, semantic `#memories` `<section>` in `index.html`, `css/sections/memories.css`, anchor connection, and verification suite. | ✅ Complete |
| **7.2** | **Six-Frame Editorial Collage** | Responsive polaroid collage (1 main `p5`, 2 medium `p1/p2`, 3 small `p3/p4/p6`), Playful Neo-Brutalist asymmetrical rotations, hard offset shadows, zero image distortion, non-interfering decorative sparkles, and generator `scripts/build_memories.js`. | ✅ Complete |
| **7.3** | **11-Item Gallery Grid & Drawer Filter** | Accessible community gallery drawer (`#memories-gallery`), category metadata & tones, live category filter chips (All, Community, Workshops, Events, Design), no-JS fallback resilience, and `js/memories.js`. | ✅ Complete |
| **7.4** | **Reusable Accessible Lightbox** | Modal dialog with focus trap, Esc to close, previous/next controls, keyboard navigation (ArrowLeft/ArrowRight), image preloading, no-JS fallback, and focus restoration. | ✅ Complete |
| **7.5** | **Motion, Visual QA & Final Phase 7 Delivery** | Restrained entrance reveals (`js/motion-home.js`), 5-viewport visual audit (320, 390, 768, 1024, 1440), zero overflow, packaging & final Phase 7 ZIP. | ✅ Complete |

---

## Phase 8 — Motion Layer Integration & Sitewide Refinement
- Fine-tune global GSAP & ScrollTrigger scroll interactions.
- Refine subtle interactive micro-animations (stickers, hover lifts, link arrows).
- Ensure strict adherence to `prefers-reduced-motion: reduce`.
- Full-site lighthouse performance, accessibility, and SEO audit.

---

## Open items for the client
- © footer wording confirmation.
- Unverified-live client URLs (LinkedIn/Instagram login walls).
- Satoshi font files (optional).
- Phase 1 tier-3 confirmations.
- Phase 5: Buildathon / Useless Projects / Web Slingers unstated event years (kept `null`).
- Phase 6: Face-to-name pairing confirmation for roster portraits.

## Core Rules to Maintain
- Flat colour only; 2px navy lines; hard shadows; pill radius for buttons only.
- Never uppercase text containing µ.
- Authentic photography only — no promotional posters, sponsor slides, or stock photography.
- Zero horizontal overflow across all 5 standard viewports (320, 390, 768, 1024, 1440).
