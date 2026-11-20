# µLearn CHN — ASSET_MAPPING.md (Final Phase 1 Mapping)

**Last updated:** 2026-11-20 · **Status:** ✅ FINAL APPROVED MAPPING FOR WEBSITE IMPLEMENTATION  
**Governing specification:** `PROJECT_MASTER_SPEC.md` §6, §7, §8, §9

---

## 1. Overview & Decisions Applied

During Phase 1, every asset was audited, measured, and processed into optimized web derivatives. The open questions from Phase 0 have been resolved as follows:

1. **Decision D1 (Event Imagery):**
   - Event cards use 4:3 framed previews that embed the entire poster artwork without destructive cropping.
   - Event dialogs display the full, uncropped poster artwork.
   - Five high-resolution genuine photographs (≥ 480 px wide) embedded inside posters were extracted as dedicated photo derivatives for event dialogs and the memories lightbox.
2. **Decision D2 (Team Roles):**
   - All 21 members are included in the team directory.
   - Role titles are published verbatim from filenames: "Lead Enabler", "Campus Lead", "Campus Co-Lead", "Creative Lead", "Operational Lead" (normalised from prototype's "Operations Lead"), "Technical Lead", "Media Lead", "Content Lead", "Designer", "Content Team", "Media Team", and "IG Lead – {AI, UI/UX, Cyber Security, Web, Entrepreneurship}".
   - "Lead Enabler" is published as stated without assuming faculty mentor status.
3. **Decision D7 (Logo & Branding):**
   - Header navigation uses the approved crisp SVG wordmark + asterisk lockup from the approved design.
   - The official gradient wordmark is optimized into `img/brand/logo.webp` and `logo.png` for brand references and footer display. No upscaling beyond its native 262px width.
4. **Decision D9 (Event Facts & Years):**
   - All facts printed on posters have been verified via RapidOCR.
   - Web Slingers date, time, and venue verified: 27th October, 4:00 PM – 5:15 PM at SDPK.
   - Unstated years (Buildathon, Useless Projects, Web Slingers) are explicitly left unstated (`null`); no years or dates were invented.
   - Tech Forge uses the extracted animated title card ("TECHFORGE 2.0") from its official video recording.

---

## 2. Verification Classification Framework

All assets, metadata, copy, and links are categorised into three explicit verification levels:

| Category | Verification Level | Scope in Dataset |
|---|---|---|
| **1. Technically Verified** | `TECHNICALLY_VERIFIED` | Derivative existence on disk, file formats (WebP/JPEG/PNG), dimensions, absence of upscaling, absence of EXIF orientation (`0x0112`) and GPS metadata (`0x8825`), performance budgets ($\le 180\text{ KB}$ hero, $\le 70\text{ KB}$ team, $\le 60\text{ KB}$ event cards), and live HTTP 200 endpoint checks. |
| **2. Source Document Verified** | `SOURCE_DOCUMENT_VERIFIED` | 21 team member names and roles matched verbatim to `sources/mulearn/Team/` filenames; 7 event initiatives, podiums, speakers, and sponsors extracted directly from poster artwork in `sources/mulearn/Events/`; external URLs matching `PROJECT_MASTER_SPEC.md` §8. |
| **3. Requiring Client Confirmation** | `CLIENT_CONFIRMATION_REQUIRED` | Information absent or unconfirmed in source documents: unstated event years (Buildathon, Useless Projects, Web Slingers), "Lead Enabler" status (faculty vs student), "Entrepreneurship" IG recognition, and prototype alternative URLs. |

---

## 3. Section-by-Section Final Asset Mapping

### 3.1 Hero Section (`#hero`)
- **Visual Target:** Tilted photo right, hard shadow, playful stickers and geometry.
- **Assigned Asset:** `img/hero/hero-1200.webp` (with `hero-900.webp` and `hero-600.webp` in `srcset`, plus `hero-1200.jpg` fallback).
- **Source:** `sources/mulearn/Memories/IMG_7789_qyh10e.jpg` (native 4032 × 3024).
- **Crop Box:** `(150, 180, 2750, 2910)` — aspect 1 : 1.05.
- **Alt Text:** "µLearn community members engaged in a hands-on technical workshop at College of Engineering Chengannur".
- **Verification:** `TECHNICALLY_VERIFIED` (JPEG 172.6 KB $\le$ 180 KB budget; EXIF stripped).
- **LCP Optimization:** `fetchpriority="high"`, `loading="eager"`.

### 3.2 About Section (`#about`)
- **Visual Target:** Tilted photo right, star decoration, authentic workshop view.
- **Assigned Asset:** `img/about/about-820.webp` (with `about-410.webp` in `srcset`).
- **Source:** `sources/mulearn/Memories/IMG_9798_mvknx7.jpg` (native 2268 × 4032).
- **Crop Box:** `(0, 350, 2268, 2958)` — aspect 4 : 4.6 (1 : 1.15).
- **Alt Text:** "Instructor conducting an Intro to Figma session projected on screen for µLearn students".
- **Verification:** `TECHNICALLY_VERIFIED`.

### 3.3 Events Section (`#events`)
Structured strictly around the **seven initiatives** defined in `PROJECT_MASTER_SPEC.md` §7.4: 3 Featured Events (asymmetric cards) + 4 Compact Events (scroll row). Every card opens an accessible `<dialog>` event archive.

| # | Event | Type | 4:3 Card Asset (`srcset`) | Dialog Poster Asset | Extracted Photos | Verification Status |
|---|---|---|---|---|---|---|
| 1 | **ODYSSEY** | Featured | `img/events/card-odyssey-405.webp`<br>`img/events/card-odyssey-600.webp` | `img/events/poster-odyssey.webp` | `img/events/photo-odyssey-wrap.webp` (615×352)<br>`img/events/photo-odyssey-stage.webp` (507×332) | `SOURCE_DOCUMENT_VERIFIED` (Yellow status: client to confirm year 2026 vs 2024 and 32h duration) |
| 2 | **Buildathon** | Featured | `img/events/card-buildathon-405.webp`<br>`img/events/card-buildathon-600.webp` | `img/events/poster-buildathon.webp` | `img/events/photo-buildathon-podium.webp` (521×312) | `SOURCE_DOCUMENT_VERIFIED` (Year unprinted; kept `null`) |
| 3 | **Build with AI** | Featured | `img/events/card-bwai-405.webp`<br>`img/events/card-bwai-600.webp` | `img/events/poster-bwai.webp` | `img/events/photo-bwai-group.webp` (618×342) | `SOURCE_DOCUMENT_VERIFIED` (Alappuzha vs Chengannur subtitle pending client confirmation) |
| 4 | **Tech Forge 2.0** | Compact | `img/events/card-techforge-405.webp` | `img/events/poster-techforge.webp` | Title frame from `Recording … 212924.mp4` | `SOURCE_DOCUMENT_VERIFIED` (Dates unstated in video; kept `null`) |
| 5 | **Type Race** | Compact | `img/events/card-typerace-405.webp`<br>`img/events/card-typerace-600.webp` | `img/events/poster-typerace.webp` | — | `SOURCE_DOCUMENT_VERIFIED` (All facts on poster) |
| 6 | **Useless Projects 3.0** | Compact | `img/events/card-useless-405.webp`<br>`img/events/card-useless-600.webp` | `img/events/poster-useless.webp` | `img/events/photo-useless-glimpses.webp` (554×330) | `SOURCE_DOCUMENT_VERIFIED` (Year unprinted; kept `null`) |
| 7 | **Web Slingers** | Compact | `img/events/card-webslingers-405.webp`<br>`img/events/card-webslingers-600.webp` | `img/events/poster-webslingers.webp` | Podium teams visible in poster | `SOURCE_DOCUMENT_VERIFIED` (OCR verified: 27th Oct, 4:00–5:15 PM, SDPK; year unprinted `null`) |

*Note on Extraneous Event Names:* Any references to "Git & GitHub", "E-Football", "Odyssey '24", or "Code In The Dark" were erroneous textual reporting artifacts. The seven initiatives above constitute the complete and sole official event register.

### 3.4 Team Section (`#team`)
- **Canonical Roster:** Exactly 21 members derived from `sources/mulearn/Team/` filenames: #1 Geetha S through #21 Swathy J.
- **Featured 4 (per Spec §7.7 and approved prototype):**
  1. Campus Lead (#2): `img/team/nithin-jayakumar-300.webp` / `600.webp`
  2. Technical Lead (#6): `img/team/amanul-farhan-300.webp` / `600.webp`
  3. Creative Lead (#4): `img/team/govind-j-s-300.webp` / `600.webp`
  4. Operational Lead (#5): `img/team/hanin-c-k-300.webp` / `600.webp`
- **Full Directory (21 Members via Dialog/Expandable Region):**
  - **Leadership:** Geetha S (Lead Enabler, 300/native), Nithin Jayakumar (Campus Lead), Divyalakshmi (Campus Co-Lead)
  - **Core Leads:** Govind J S (Creative Lead), Hanin C K (Operational Lead), Amanul Farhan (Technical Lead), Pavithra A (Media Lead), Albin Thomas (Content Lead)
  - **Operations & Creative:** Melwin Shibu Mathew (Operational Team), Sara Shaji (Operational Team), Afsal S (Designer), Vismaya Gawri Krishnan (Designer), Karthika S (Content Team), Sreelakshmi M (Content Team), Parvathy Vinayan (Media Team), Brijith K Reji (Media Team)
  - **Interest Group Leads:** Adhi Narayan (AI), Al Ameen (UI/UX), Amal S (Cyber Security), Abhiram J (Web), Swathy J (Entrepreneurship)
- **Verification Classifications:**
  - Names and roles: `SOURCE_DOCUMENT_VERIFIED` (from filenames verbatim).
  - Geetha S status as Faculty Mentor: `CLIENT_CONFIRMATION_REQUIRED` (keep title "Lead Enabler").
  - Swathy J "Entrepreneurship" IG: `CLIENT_CONFIRMATION_REQUIRED` (non-standard IG group).
  - Face-to-name accuracy: `CLIENT_CONFIRMATION_REQUIRED` (cannot be independently confirmed from unlabelled photographs alone).

### 3.5 Memories Section (`#memories`)
- **6-Frame Polaroid Collage:**
  - `p1` (1.8 aspect): `img/memories/collage-p1-460.webp` / `920.webp` — Lab Overview (`IMG_7834`)
  - `p2` (2.0 aspect): `img/memories/collage-p2-460.webp` / `920.webp` — Mentor Workshop (`IMG_9803`)
  - `p3` (1.9 aspect): `img/memories/collage-p3-460.webp` / `920.webp` — Crowd Gathering (`IMG_5086` crop)
  - `p4` (1.8 aspect): `img/memories/collage-p4-460.webp` / `920.webp` — Coding Collaboration (`IMG_7789` crop)
  - `p5` (1.76 aspect - Centerpiece): `img/memories/collage-p5-460.webp` / `920.webp` / `1200.webp` — Community Group Photo at CEC (`IMG_5086`)
  - `p6` (1.1 aspect): `img/memories/collage-p6-460.webp` / `920.webp` — Demo & Projector (`IMG_7844`)
- **Lightbox Gallery (11 Items):**
  - All 6 full community photographs (`IMG_5086`, `IMG_7789`, `IMG_7834`, `IMG_7844`, `IMG_9798`, `IMG_9803`) at max 1600 px long edge.
  - 5 extracted genuine event photographs (`photo-odyssey-wrap`, `photo-odyssey-stage`, `photo-buildathon-podium`, `photo-bwai-group`, `photo-useless-glimpses`).

### 3.6 External Links & Destinations
- **Canonical URLs:** Strictly maintained per `PROJECT_MASTER_SPEC.md` §8 (`register`, `discord`, `linkedin`, `instagram`, `email`, `mulearnOrg`, `offers.*`).
- **Unconfirmed Alternatives (from `reference.html` prototype):** Documented in `data/links.js` under `unconfirmedAlternatives` pending client confirmation.

---

## 4. Rejected & Excluded Assets

| File | Reason for Rejection | Handled In |
|---|---|---|
| `Memories/event5_zdu88j.jpg` | Promotional graphic poster ("Weekly Twitches"), not a community memory. | Excluded from Memories collage and gallery. |
| `Events/Odessey/Screenshot 2026-11-19 212307.png` | Low-resolution duplicate (400×500) of higher-res date poster. | Higher-res version used. |
| `Events/Odessey/Screenshot 2026-11-19 212314.png` | Low-resolution duplicate (407×507) of prize pool poster. | Higher-res version used. |
| 15 Excluded Sponsor/Teaser Slides | Pure sponsor logos, partner slides, registration teasers. | Excluded per Spec §9.2 Rule 7; not delivered in `Events1.zip`/`Events2.zip`. |
