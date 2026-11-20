# PROJECT_STATE.md

**Last updated:** 2026-11-20 · **Current phase:** 0 (planning) — COMPLETE · **Next phase:** 1 (Asset pipeline & content data)
**Project status:** no website code exists yet. The only implementation artefact is the reference prototype.

## Phase status
| Phase | Name | Status |
|---|---|---|
| 0 | Master planning & audit | ✅ complete (this bundle) |
| 1 | Asset pipeline & content data | ⏳ not started |
| 2 | Scaffold & design foundation | ⏳ |
| 3 | Header/nav + Hero + About | ⏳ |
| 4 | Offers + Join + Footer | ⏳ |
| 5 | Events + dialogs | ⏳ |
| 6 | Team + directory | ⏳ |
| 7 | Memories + lightbox | ⏳ |
| 8 | Motion layer | ⏳ |
| 9 | QA / a11y / perf / SEO | ⏳ |
| 10 | Release & handoff | ⏳ |

## Files in this bundle and integrity
| File | SHA-256 |
|---|---|
| reference/ulearn_prototype_v1_UNMODIFIED.html | 333a447d23a3a2b1728069cf3aaa4bbad1b4f77470bb017659e0649a05cc555d |
| docs/ASSET_MAPPING.md | 1925744494eb9d1e90220dc4e2fc2fe8900bafff17d709ca17134e29be909dcc |

Originals (`mulearn.zip`, 85 files, 88 MB) are **not** in this bundle; the client keeps them. Phase 1 needs them re-uploaded.

## Decisions log (newest first; overrides the spec)
| Date | Decision | By |
|---|---|---|
| 2026-11-20 | Stack = no-build static HTML/CSS/vanilla JS (classic scripts), GSAP vendored, WebP derivatives, Vercel static | Phase 0 |
| 2026-11-20 | ODYSSEY spelling = "ODYSSEY" | Phase 0 (poster text + third-party listing) |
| 2026-11-20 | No statistics published (sources conflict) | Phase 0 |
| 2026-11-20 | Defaults D1–D15 in Spec §15 apply until the client answers | Phase 0 |

## Open client questions (see Spec §15 for defaults)
D1 event imagery · D2 team roles ("Lead Enabler", "Campus Co-Lead", "Operational/Operations", "IG Lead – Entrepreneurship") · D3 hero wording ("official") · D4 confirm LinkedIn/Instagram/email · D5 darker indigo for text fills · D6 Satoshi files · D7 logo · D8 permissions · D9 missing event facts · D10 event split · D11 stats · D12 credit/disclaimer · D13 video · D14 deploy URL · D15 reference image/Figma.

## Known issues carried forward
Prototype defects P1–P12 (see PHASE0_REPORT.md §1.4). Not accessible during Phase 0: Figma, LinkedIn, Instagram, body of mulearn-chn.vercel.app, Instagram captions.

## Environment facts verified in Phase 0 (Claude Web sandbox)
Playwright + headless Chromium launches; Node 22 / npm 10; ffmpeg + Pillow available; npm registry reachable (gsap 3.15.1, @fontsource/plus-jakarta-sans 5.3.0 present; no @fontsource/satoshi); Google Fonts, Fontshare, cdnjs are **not** reachable from the sandbox.
