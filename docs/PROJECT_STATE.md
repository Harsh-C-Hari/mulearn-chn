# PROJECT_STATE.md

**Last updated:** 2026-11-20 · **Current phase:** 1 (Asset pipeline & content data) — VERIFIED & CONSISTENT · **Next phase:** 2 (Scaffold & design foundation)  
**Project status:** Asset pipeline verified; content data reconciled with Project Master Spec §7, §8, §9; 3-tier verification framework established; ready for Phase 2 scaffolding.

## Phase status
| Phase | Name | Status |
|---|---|---|
| 0 | Master planning & audit | ✅ complete |
| 1 | Asset pipeline & content data | ✅ complete & reconciled |
| 2 | Scaffold & design foundation | ⏳ next |
| 3 | Header/nav + Hero + About | ⏳ |
| 4 | Offers + Join + Footer | ⏳ |
| 5 | Events + dialogs | ⏳ |
| 6 | Team + directory | ⏳ |
| 7 | Memories + lightbox | ⏳ |
| 8 | Motion layer | ⏳ |
| 9 | QA / a11y / perf / SEO | ⏳ |
| 10 | Release & handoff | ⏳ |

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
