# PROJECT_STATE.md

**Last updated:** 2026-11-20 · **Current phase:** 2 (Design foundation) — **COMPLETE** (Subphase 2.6 done) · **Next:** Phase 3 (Header/nav + Hero + About) — awaiting client go-ahead  
**Project status:** Design system built and audited (axe-core 0 violations at 5 widths, WCAG 2.2 focus checks pass, 0 console errors, 0 external requests); `styleguide.html` is the reference for every Phase 3+ section.

## Phase status
| Phase | Name | Status |
|---|---|---|
| 0 | Master planning & audit | ✅ complete |
| 1 | Asset pipeline & content data | ✅ complete & reconciled |
| 2 | Design foundation (subphased) | ✅ complete — final ZIP `mulearn-chn_phase-02_complete.zip` |
| 3 | Header/nav + Hero + About | ⏳ |
| 4 | Offers + Join + Footer | ⏳ |
| 5 | Events + dialogs | ⏳ |
| 6 | Team + directory | ⏳ |
| 7 | Memories + lightbox | ⏳ |
| 8 | Motion layer | ⏳ |
| 9 | QA / a11y / perf / SEO | ⏳ |
| 10 | Release & handoff | ⏳ |

## Phase 2 progress (subphase checkpoints)
| Subphase | Name | Status | ZIP |
|---|---|---|---|
| 2.1 | Project inspection & design audit | ✅ complete | `mulearn-chn_phase-02_subphase-01.zip` |
| 2.2 | Design tokens & typography | ✅ complete | `mulearn-chn_phase-02_subphase-02.zip` |
| 2.3 | Layout & reusable components | ✅ complete | `mulearn-chn_phase-02_subphase-03.zip` |
| 2.4 | Decorative library & GSAP foundation | ✅ complete | `mulearn-chn_phase-02_subphase-04.zip` |
| 2.5 | Styleguide implementation | ✅ complete | `mulearn-chn_phase-02_subphase-05.zip` |
| 2.6 | Final responsive & accessibility audit | ✅ complete | `mulearn-chn_phase-02_complete.zip` (+ deployable `mulearn-chn_phase-02_deploy.zip`) |

Phase 2 working rules (from the client brief, override `NEXT_PHASE.md` where they differ): one subphase at a time, stop for approval after each, versioned full-project ZIP after each, `index.html` assembly deferred to Phase 3.
Client note (2026-11-20): wants a **mix** of Board 1 (authority) and Board 2 (additive vocabulary). Merge plan in `docs/design-audit.md` §4.

New files in 2.1: `docs/design-audit.md`, `reference/ulearn_board-1_bold-playful_APPROVED.png`, `reference/ulearn_board-2_neo-brutalist_MIX.png`, `reference/SHA256SUMS.txt`. No design code written yet. No existing file other than docs was changed.

## Files in this bundle and integrity
| File | Status / Verification |
|---|---|
| `reference/ulearn_prototype_v1_UNMODIFIED.html` | ✅ Unmodified reference visual prototype (SHA-256 verified) |
| `docs/ASSET_MANIFEST.json` | ✅ 49 manifest entries covering all 96 derivatives |
| `docs/ASSET_MANIFEST.md` | ✅ Complete inventory, audit, and derivative documentation |
| `docs/ASSET_MAPPING.md` | ✅ Final section mapping, 3-tier verification framework, and resolution of D1, D2, D7, D9 |
| `docs/asset-review.html` | ✅ Visual contact sheet for visual review (49 img elements, 0 broken) |
| `data/links.js` | ✅ Canonical destinations per Spec §8; unconfirmed prototype alternatives documented |
| `data/team.js` | ✅ Canonical 21-member roster (#1 Geetha S to #21 Swathy J); featured 4 per Spec §7.7 |
| `data/events.js` | ✅ Exactly the 7 specified initiatives per Spec §7.4; unstated years kept null |
| `data/memories.js` | ✅ 6-frame polaroid collage + 11-item lightbox gallery |
| `img/{hero,about,events,team,memories,brand,og}/` | ✅ 96 derivatives, 4.17 MB total, 0 EXIF, 0 upscaled |
| `scripts/{build_assets,extract_embedded,extract_frames,verify_project,independent_verification}.py` | ✅ Reproducible pipeline and test scripts |

Originals (`sources/mulearn`, 74 files) remain 100% untouched and are excluded from deployable bundles.

## Content Verification Framework
All project content is tracked under three explicit tiers:
1. **Technically Verified:** Derivative file existence, decodability, pixel dimensions, zero upscaling, stripped EXIF/GPS metadata, byte size budgets ($\le 180\text{ KB}$ hero, $\le 70\text{ KB}$ team, $\le 60\text{ KB}$ event cards), and live HTTP route validity.
2. **Source Document Verified:** 21 team member names and roles matched verbatim to `sources/mulearn/Team/` filenames; 7 event initiatives, podiums, speakers, and sponsors extracted from poster artwork in `sources/mulearn/Events/`; external URLs matching `PROJECT_MASTER_SPEC.md` §8.
3. **Information Requiring Client Confirmation:** Unstated event years (Buildathon, Useless Projects, Web Slingers), "Lead Enabler" organizational role definition, "Entrepreneurship" IG official recognition, and prototype alternative URLs.

## Decisions log (newest first; overrides the spec)
| Date | Decision | By |
|---|---|---|
| 2026-11-20 | 2.6: Focus ring + gap are surface-aware custom properties (`--focus-ring`, `--focus-gap`); yellow on indigo/ink, navy on coral, gap = card colour. `.btn` owns its text colour so ancestor `a{}` rules can't override it. Sub-AA colour pairs appear in the styleguide only as labelled "fails" chips on a neutral surface. Header nav shows from 1180px. `verify_project.py` now resolves paths relative to itself (H1 closed); root duplicate docs removed (H3 closed); stale `pack_bundles.py` replaced by `pack_deploy.py`. | Phase 2.6 |
| 2026-11-20 | 2.5: Team portraits are full-background photos (not cut-outs), so Board 1's coloured backdrop is realised as a coloured **mat** around an inset photo, with a dot pattern on two of four. Portrait captions use roles only (face↔name linkage still needs client confirmation). Styleguide uses only existing sample copy/data (event titles, formats, roles); no new facts. Board 2 wave edge realised as hard scallop mask (`.edge`). Ink/indigo cards force inherited link colour (accessibility fix). | Phase 2.5 |
| 2026-11-20 | 2.4: Sprite is single source (`img/ui/sprite.svg`) inlined per page by `sync_sprite.py` (C9-B). `motion-guard.js` lazily loads GSAP only when reduced-motion is off (saves ~118 KB for those visitors); `js-motion` class set only after both libraries register. Board 2 "wave" edge built as hard-edged scallop/zigzag masks (flat, no curves-with-gradient). GSAP licence note written by hand (npm tarball ships no LICENSE file). | Phase 2.4 |
| 2026-11-20 | Client approved audit recommendations C1-B (lavender #DDD6FE + coral #FB8F7C flat tints, navy text only), C2-B (pill buttons only), C5-A, C6-A, C7, C9–C12; instructed to continue through all subphases delivering a ZIP after each without waiting. | Client / 2.2 |
| 2026-11-20 | Subphase 2.1 audit: Board 1 = visual authority; Board 2 = additive vocabulary (shapes, ink bands, colour-blocked cards) pending palette approval C1. Board 2 text is garbled AI pseudo-text and is never used as content. GSAP 3.15.1 (16 days old) and @fontsource/plus-jakarta-sans 5.3.0 confirmed fetchable; Satoshi unavailable (fallback stays, D6). `verify_project.py` has a hard-coded `D:\\` path (H1) — fix proposed for 2.6. | Phase 2.1 |
| 2026-11-20 | Content Consistency Audit: Resolved reporting anomalies; confirmed canonical 21-member roster (#1 Geetha S to #21 Swathy J) and 7 specified initiatives; preserved client Spec §8 URLs; documented prototype alternatives in `data/links.js`. | Phase 1 Audit |
| 2026-11-20 | Web Slingers poster details verified via RapidOCR: Date 27th October, Venue SDPK, Time 4:00 PM – 5:15 PM. No year invented. | Phase 1 |
| 2026-11-20 | Tech Forge represented via extracted title frame ("TECHFORGE 2.0") from source video; no dates or venue invented. | Phase 1 |
| 2026-11-20 | 5 genuine event photos (≥ 480px wide) extracted from posters into dedicated derivatives for dialogs and lightbox gallery. | Phase 1 |
| 2026-11-20 | Event cards use 4:3 framed previews to preserve full poster artwork without destructive text cuts. | Phase 1 |
| 2026-11-20 | Team portraits: all 21 members included; filename roles used verbatim per D2; `18_Al_Ameen` rotated 90° CW; `1_geetha_s` kept unupscaled. | Phase 1 |
| 2026-11-20 | Memories collage: 6 authentic photo frames assigned (`p1`–`p6`); `event5_zdu88j.jpg` rejected as non-photographic. | Phase 1 |
| 2026-11-20 | All EXIF and GPS location metadata stripped from all derivatives across the board for privacy and performance. | Phase 1 |
| 2026-11-20 | College facts verified: CEC established in 1993 by Government of Kerala under IHRD, AICTE-approved, KTU-affiliated, college code CHN. | Phase 1 |
| 2026-11-20 | Stack = no-build static HTML/CSS/vanilla JS (classic scripts), GSAP vendored, WebP derivatives, Vercel static | Phase 0 |
| 2026-11-20 | ODYSSEY spelling = "ODYSSEY" | Phase 0 |
| 2026-11-20 | No statistics published (sources conflict) | Phase 0 |
| 2026-11-20 | Defaults D1–D15 in Spec §15 apply until the client answers | Phase 0 |

## Verification results
`scripts/verify_project.py` executed:
- Total derivatives checked: 96
- Total size: 4.17 MB (down from 88 MB originals)
- Dimension errors: 0
- Upscaling errors: 0
- EXIF/GPS leaks: 0
- Budget violations: 0
- Raw source leaks into `img/`: 0
- Status: ✅ ALL CHECKS PASSED


## Phase 2.6 verification (re-run in this session)
- `scripts/verify_project.py` (path fixed): 96 derivatives, 4.17 MB, 0 errors, 0 warnings — **re-verified**.
- `scripts/run_audit.sh`: axe-core 0 violations at 320/390/768/1024/1440; 0 console errors; 0 non-local requests; fonts + GSAP local; reduced motion and no-JS behave.
- `scripts/audit_focus.py`: 58 tab stops, min ring contrast 3.27:1, 0 obscured, skip link OK.
- `scripts/test_motion.py`: PASS. Reports: `docs/responsive-report.md`, `docs/accessibility-report.md`; screenshots in `docs/screenshots/`.
- Not covered: real devices, Safari/Firefox, screen readers, forced-colors mode (see accessibility report).

## Known issues / items needing client confirmation (carried forward)
Satoshi still not available (fallback Plus Jakarta Sans 800, D6). Phase 1 content items in the Verification Framework tier 3 remain open.
