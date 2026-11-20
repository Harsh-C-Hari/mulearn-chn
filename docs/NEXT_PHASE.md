# NEXT_PHASE.md — Phase 1: Asset pipeline & content data

**You are a new Claude session with no prior history.** Read `docs/PROJECT_MASTER_SPEC.md` (esp. §7, §9), `docs/PROJECT_STATE.md`, `docs/ASSET_MAPPING.md`, `docs/PHASE0_REPORT.md` §3 and §6 (Phase 1). Then ask the client to upload `mulearn.zip` (originals) if it is not attached.

## Objective
Produce every derivative image, the asset manifest and the data files, so later phases only place assets.

## Do
1. Extract originals to `_sources/` (never edit; never ship). Record sha256 for each used source.
2. Build `scripts/build_assets.py`, `extract_embedded.py`, `extract_frames.py` (Pillow, ffmpeg).
3. Derivatives per Spec §9.3 into `img/{hero,about,events,team,memories,brand,og}/` — WebP, srcset widths, EXIF rotate + strip, **no upscaling**.
4. Crop test and decide: hero, about, collage (6 frames incl. the 2 open slots), team featured four (#2,#6,#4,#5) plus the other 17 portraits, 7 event cards + dialog posters, extractions of embedded photos ≥ 480 px wide (remove Instagram chrome), video poster frames (Tech Forge title frame, others as available).
5. Re-read at full zoom: Web Slingers date/venue/time poster; ODYSSEY registration fee; any posters with small text. Update Spec §7.4 only via `PROJECT_STATE.md` decisions log.
6. Re-read ceconline.edu for the college facts (§7.2).
7. Write `docs/ASSET_MANIFEST.json` (schema in Spec §9.5) and `data/{team,events,memories,links}.js` skeletons with `verified` flags — **no invented facts**.
8. Generate `docs/asset-review.html` contact sheet; publish via Artifact for client review.
9. Create `scripts/verify_project.py` (checks listed in PHASE0_REPORT §8).

## Do not
Start site markup/CSS; modify `reference/*`; generate or fabricate photos; upscale; add third-party logos as standalone images; guess identities.

## Acceptance
Every manifest entry complete · budgets met · no derivative exceeds its source in pixels · no metadata in derivatives · every slot in Spec §9.4 decided or listed as open · contact sheet reviewed · all handoff docs updated · ZIP verified.

## Open decisions that affect this phase
D1, D7, D8, D9 (Spec §15). Apply defaults and log them if unanswered.

## Known risks
Embedded photos may be < 480 px; only six genuine photographs for eight slots; originals must be re-uploaded.

## Required output
`mulearn-chn_phase-01_<YYYYMMDD>.zip` (complete project) + updated `PROJECT_STATE.md`, `CHANGELOG.md`, `NEXT_PHASE.md` (for Phase 2), `PROJECT_MASTER_SPEC.md` (only if decisions changed), `ASSET_MANIFEST.json`.
