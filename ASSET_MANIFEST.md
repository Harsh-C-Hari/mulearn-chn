# µLearn CHN — ASSET_MANIFEST.md

**Phase 1 Deliverable · Complete Inventory, Audit & Usage Mapping**  
**Date:** 2026-11-20  
**Status:** ✅ PHASE 1 COMPLETE  
**JSON Machine-Readable Manifest:** `docs/ASSET_MANIFEST.json`  
**Visual Contact Sheet:** `docs/asset-review.html`  

---

## 1. Executive Summary

This manifest documents the exhaustive audit, processing, and section mapping for all visual and media assets of the µLearn CHN website.

- **Original Sources Audited:** 74 files in `sources/mulearn/` (1 wordmark logo, 21 team portraits, 7 memories items, 41 event screenshots/recordings, and 4 archive packages).
- **Original Source Integrity:** 100% preserved. Zero files inside `sources/mulearn/` were modified, moved, or overwritten.
- **Website Derivatives Produced:** 96 optimized WebP, JPEG, and PNG derivatives in `mulearn-chn/img/` (Total footprint: 4.17 MB).
- **Quality & Safety Gates Passed:**
  - Zero upscaling beyond native pixels across all derivatives.
  - Complete removal of EXIF metadata and GPS location tags (privacy protection).
  - EXIF rotation corrected (`Team/18_Al_Ameen__IG_Lead-UI_UX.jpg` rotated 90° CW to upright orientation).
  - Strict compliance with file size budgets per Spec §9.3.
  - Zero source files or raw screenshots deployed into `img/`.

---

## 2. Source Archive Inventory & Audit

### 2.1 Logo & Brand Asset
| Relative Path | Format | Native Resolution | File Size | SHA-256 (prefix) | Notes & Status |
|---|---|---|---|---|---|
| `mulearn_logo.png` | PNG (RGBA) | 262 × 112 | 7,206 B | `d4e5f487...` | Wordmark "µlearn CHN" in blue-purple gradient. Opaque white background. Native 262px width preserved; unupscaled. |

### 2.2 Team Portraits (21 Members)
All team portraits were audited for dimensions, orientation, and GPS metadata.

| # | Filename | Format | Native Dimensions | Size | EXIF Orientation | GPS Tags | Derived Name & Role |
|---|---|---|---|---|---|---|---|
| 1 | `1_geetha_s__Lead_Enabler.jpg` | JPEG | 400 × 514 | 83.7 KB | 1 (normal) | None | Geetha S · Lead Enabler *(Low-res; no upscale)* |
| 2 | `2_Nithin_Jayakumar__Campus_Lead.jpg` | JPEG | 1000 × 1500 | 111.6 KB | 1 (normal) | None | Nithin Jayakumar · Campus Lead *(Featured)* |
| 3 | `3_Divyalakshmi__Campus_Co-Lead.jpg` | JPEG | 1180 × 1572 | 217.8 KB | 1 (normal) | None | Divyalakshmi · Campus Co-Lead |
| 4 | `4_govind_j_s__Creative_Lead.webp` | WEBP | 1273 × 1662 | 145.4 KB | 1 (normal) | None | Govind J S · Creative Lead *(Featured)* |
| 5 | `5_Hanin_C_K__Operational_Lead.jpg` | JPEG | 1653 × 1989 | 750.3 KB | 1 (normal) | None | Hanin C K · Operational Lead *(Featured)* |
| 6 | `6_Amanul_Farhan__Technical_Lead.jpg` | JPEG | 1000 × 1500 | 158.5 KB | 1 (normal) | None | Amanul Farhan · Technical Lead *(Featured)* |
| 7 | `7_Pavithra_A__Media_Lead.jpg` | JPEG | 1756 × 3021 | 1.15 MB | 1 (normal) | **Present** | Pavithra A · Media Lead *(GPS stripped)* |
| 8 | `8_Albin_Thomas__Content_Lead.jpg` | JPEG | 2268 × 4032 | 3.56 MB | 1 (normal) | None | Albin Thomas · Content Lead |
| 9 | `9_Melwin_Shibu_Mathew__Operational_Team.jpg` | JPEG | 1892 × 2168 | 1.34 MB | 1 (normal) | None | Melwin Shibu Mathew · Operational Team |
| 10 | `10_Sara_Shaji__Operational_Team.jpg` | JPEG | 2268 × 4032 | 519.7 KB | 1 (normal) | None | Sara Shaji · Operational Team |
| 11 | `11_Afsal_S__Designer.png` | PNG | 896 × 1152 | 1.15 MB | 1 (normal) | None | Afsal S · Designer *(Cut-out portrait)* |
| 12 | `12_Vismaya_Gawri_Krishnan__Designer.jpg` | JPEG | 1200 × 1600 | 315.3 KB | 1 (normal) | None | Vismaya Gawri Krishnan · Designer |
| 13 | `13_Karthika_S__Content_Team.jpg` | JPEG | 780 × 1040 | 92.7 KB | 1 (normal) | None | Karthika S · Content Team |
| 14 | `14_Sreelakshmi_M__Content_Team.jpg` | JPEG | 3120 × 4160 | 1.85 MB | 1 (normal) | None | Sreelakshmi M · Content Team |
| 15 | `15_Parvathy_Vinayan__Media_Team.jpg` | JPEG | 900 × 1600 | 153.7 KB | 1 (normal) | None | Parvathy Vinayan · Media Team |
| 16 | `16_Brijith_K_Reji__Media_Team.jpg` | JPEG | 768 × 1344 | 611.7 KB | 1 (normal) | None | Brijith K Reji · Media Team |
| 17 | `17_Adhi_Narayan__IG_Lead-AI.jpg` | JPEG | 2056 × 2176 | 3.20 MB | 1 (normal) | None | Adhi Narayan · IG Lead – AI |
| 18 | `18_Al_Ameen__IG_Lead-UI_UX.jpg` | JPEG | 4000 × 3000 | 6.71 MB | **6 (Rotate 90° CW)** | None | Al Ameen · IG Lead – UI/UX *(Rotated & stripped)* |
| 19 | `19_Amal_S__IG_Lead-Cyber_Security.jpg` | JPEG | 2805 × 3000 | 2.00 MB | 1 (normal) | **Present** | Amal S · IG Lead – Cyber Security *(GPS stripped)* |
| 20 | `20_Abhiram_J__IG_Lead-Web.jpg` | JPEG | 1023 × 1018 | 113.7 KB | 1 (normal) | None | Abhiram J · IG Lead – Web |
| 21 | `21_Swathy_J__IG_Lead-Entrepreneurship.jpg` | JPEG | 960 × 1173 | 92.0 KB | 1 (normal) | None | Swathy J · IG Lead – Entrepreneurship |

### 2.3 Community Photography & Memories (7 Items)
| Filename | Native Dimensions | File Size | Content Classification | GPS Tags | Website Usability Assessment |
|---|---|---|---|---|---|
| `IMG_5086_tm6kwh.jpg` | 6000 × 4000 | 4.15 MB | Genuine Community Photograph | **Present** | **Hero/Collage Main.** Large group in front of CEC campus main building. Highest quality community anchor. |
| `IMG_7789_qyh10e.jpg` | 4032 × 3024 | 2.68 MB | Genuine Community Photograph | **Present** | **Primary Hero Asset.** Speaker in white shirt standing in computer lab with students coding. High dynamic energy. |
| `IMG_7834_xrr7b7.jpg` | 4032 × 3024 | 3.88 MB | Genuine Community Photograph | **Present** | **Collage P1 & Lightbox.** Full lab room overview with students coding. |
| `IMG_7844_lclzmf.jpg` | 4032 × 3024 | 3.20 MB | Genuine Community Photograph | **Present** | **Collage P6 & Lightbox.** Projector screen demonstration and standing mentors. |
| `IMG_9798_mvknx7.jpg` | 2268 × 4032 | 1.53 MB | Genuine Community Photograph | None | **About Section Photo.** Mentor with projected "Intro to Figma" slide. Perfect fit for About. |
| `IMG_9803_ixchge.jpg` | 5712 × 3213 | 4.06 MB | Genuine Community Photograph | None | **Collage P2 & Lightbox.** 16:9 lab workshop with mentor assisting students. |
| `event5_zdu88j.jpg` | 1024 × 1280 | 116.3 KB | Promotional Graphic Poster | None | **REJECTED from Memories.** Orange text graphic ("Weekly Twitches / Salt-Mango Tree"). Not an authentic community photo. |

### 2.4 Event Media (41 Files Across 7 Initiatives)
The event files are Instagram promotion screenshots and short MP4 recordings.
- **Genuine Photos Inside Event Posters:** Located, measured, and cropped when ≥ 480 px wide.
- **Instagram UI Artefacts:** Carousel arrow buttons and indicator dots identified on Buildathon, Odyssey, and Useless Projects screenshots. Cleaned in derivatives.
- **Text & Facts Extraction:** Verified via RapidOCR. Web Slingers confirmed for 27th October, 4:00 PM – 5:15 PM at SDPK.

---

## 3. Derivative Generation & Section Mapping

### 3.1 Hero Section
- **Slot Requirements:** ~600 px CSS width, 1 : 1.05 aspect ratio, max 180 KB @ 1200 px.
- **Source Asset:** `Memories/IMG_7789_qyh10e.jpg` (native 4032 × 3024).
- **Crop Coordinates:** `(150, 180, 2750, 2910)` (2600 × 2730 px). Anchored on standing speaker and engaged students.
- **Generated Derivatives:**
  - `img/hero/hero-600.webp` (600 × 630, 24.3 KB)
  - `img/hero/hero-900.webp` (900 × 945, 47.9 KB)
  - `img/hero/hero-1200.webp` (1200 × 1260, 78.4 KB) — Budget: ≤ 180 KB ✅
  - `img/hero/hero-1200.jpg` (1200 × 1260, 172.6 KB) — Fallback / Open Graph ✅

### 3.2 About Section
- **Slot Requirements:** ~410 × 470 px CSS (4 : 4.6 aspect ratio), max 120 KB @ 820 px.
- **Source Asset:** `Memories/IMG_9798_mvknx7.jpg` (native 2268 × 4032).
- **Crop Coordinates:** `(0, 350, 2268, 2958)` (2268 × 2608 px).
- **Generated Derivatives:**
  - `img/about/about-410.webp` (410 × 472, 19.8 KB)
  - `img/about/about-820.webp` (820 × 943, 62.1 KB) — Budget: ≤ 120 KB ✅

### 3.3 Events Section (7 Events)
Per Spec §9.2 rule 3, portrait posters are preserved in full artwork without aggressive cropping. Card derivatives provide 4:3 framed previews, and poster derivatives provide clean dialog artwork.

| Event | Display Name | Card Derivatives (4:3) | Dialog Poster Derivative | Extracted Genuine Photos (≥ 480 px) |
|---|---|---|---|---|
| **ODYSSEY** | ODYSSEY (32h Hackathon) | `card-odyssey-405.webp` (19.4 KB)<br>`card-odyssey-600.webp` (36.1 KB) | `poster-odyssey.webp` (542.4 KB) | `photo-odyssey-wrap.webp` (615×352, 41.2 KB)<br>`photo-odyssey-stage.webp` (507×332, 15.1 KB) |
| **Buildathon** | Buildathon (µFIFA × Gemma 4) | `card-buildathon-405.webp` (16.2 KB)<br>`card-buildathon-600.webp` (29.8 KB) | `poster-buildathon.webp` (390.1 KB) | `photo-buildathon-podium.webp` (521×312, 26.6 KB) |
| **Build with AI** | Build with AI (Gemini & Hackathon) | `card-bwai-405.webp` (21.7 KB)<br>`card-bwai-600.webp` (40.9 KB) | `poster-bwai.webp` (529.3 KB) | `photo-bwai-group.webp` (618×342, 50.3 KB) |
| **Tech Forge** | Tech Forge 2.0 | `card-techforge-405.webp` (13.3 KB) | `poster-techforge.webp` (13.3 KB) | Video title frame (496×638) |
| **Type Race** | Type Race | `card-typerace-405.webp` (26.4 KB)<br>`card-typerace-600.webp` (51.2 KB) | `poster-typerace.webp` (873.4 KB) | — (winner portraits B&W in poster) |
| **Useless Projects** | Useless Projects 3.0 | `card-useless-405.webp` (12.8 KB)<br>`card-useless-600.webp` (23.5 KB) | `poster-useless.webp` (265.7 KB) | `photo-useless-glimpses.webp` (554×330, 35.6 KB) |
| **Web Slingers** | Web Slingers | `card-webslingers-405.webp` (24.1 KB)<br>`card-webslingers-600.webp` (46.8 KB) | `poster-webslingers.webp` (678.8 KB) | Podium teams visible in poster |

### 3.4 Team Section (21 Members)
- **Slot Requirements:** 3 : 3.6 portrait aspect ratio (300 × 360 px and 600 × 720 px), max 70 KB @ 600 px.
- **Featured 4:** Nithin Jayakumar (`team-02`), Amanul Farhan (`team-06`), Govind J S (`team-04`), Hanin C K (`team-05`).
- **Full Directory:** All 21 members processed with face-centered crops and zero upscaling.
  - `geetha-s`: Native 400×514 -> exported as `geetha-s-300.webp` (13.2 KB) and `geetha-s-native.webp` (21.4 KB). No upscale to 600!
  - `al-ameen`: Rotated 90° CW to upright orientation before export.
  - All 600 px derivatives strictly comply with the ≤ 70 KB budget (e.g. `sreelakshmi-m-600.webp` at 69.1 KB).

### 3.5 Memories Section (Collage & Lightbox Gallery)
- **Collage Frame P1 (1.8 aspect):** `collage-p1-460.webp` (26.1 KB), `collage-p1-920.webp` (74.2 KB)
- **Collage Frame P2 (2.0 aspect):** `collage-p2-460.webp` (23.9 KB), `collage-p2-920.webp` (71.5 KB)
- **Collage Frame P3 (1.9 aspect):** `collage-p3-460.webp` (31.4 KB), `collage-p3-920.webp` (98.6 KB) — Crowd close-up
- **Collage Frame P4 (1.8 aspect):** `collage-p4-460.webp` (24.8 KB), `collage-p4-920.webp` (76.1 KB) — Lab collaboration
- **Collage Frame P5 (1.76 aspect - Main):** `collage-p5-460.webp` (32.1 KB), `collage-p5-920.webp` (104.2 KB), `collage-p5-1200.webp` (154.6 KB) — Full community group
- **Collage Frame P6 (1.1 aspect):** `collage-p6-460.webp` (28.4 KB), `collage-p6-920.webp` (89.2 KB) — Projection room
- **Lightbox Gallery (11 items):**
  - 6 full community photographs (`IMG_5086`, `IMG_7789`, `IMG_7834`, `IMG_7844`, `IMG_9798`, `IMG_9803`) scaled to max 1600 px long edge (WebP q82, all ≤ 250 KB).
  - 5 extracted genuine event photographs (`odyssey-wrap`, `odyssey-stage`, `buildathon-podium`, `bwai-group`, `useless-glimpses`).

### 3.6 Brand & Open Graph
- `img/brand/logo.webp` (262 × 112, 3.8 KB)
- `img/brand/logo.png` (262 × 112, 7.2 KB)
- `img/og/og-image.jpg` (1200 × 630, 84.6 KB)
- `img/og/og-image.webp` (1200 × 630, 48.2 KB)

---

## 4. Verification & Integrity Checklist

- [x] All 96 derivatives exist on disk and open without errors.
- [x] Zero upscaling beyond native pixels across any derivative.
- [x] All EXIF and GPS location metadata stripped from derivatives.
- [x] `Team/18_Al_Ameen` EXIF orientation code 6 corrected to upright.
- [x] Zero original source files modified or relocated in `sources/mulearn/`.
- [x] Zero raw original files deployed into `img/`.
- [x] All budgets specified in Spec §9.3 met.
- [x] Verified via `scripts/verify_project.py` with 0 errors.
