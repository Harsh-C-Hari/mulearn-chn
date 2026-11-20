# CHANGELOG.md

Format: newest first. Each entry: date · phase · what changed · files · verification.

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
