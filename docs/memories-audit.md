# µLearn CHN — Memories & Community Photography Audit (Phase 7.1)

**Audit Date:** 2026-11-20  
**Status:** ✅ TECHNICALLY VERIFIED & APPROVED FOR IMPLEMENTATION  
**Governing Documents:** `PROJECT_MASTER_SPEC.md` §6, §7.5, §9; `ASSET_MAPPING.md` §3.5, §4; `ASSET_MANIFEST.md` §2.3; `data/memories.js`

---

## 1. Executive Summary

Phase 7.1 establishes the foundational asset audit and semantic section structure for **Memories & Gallery** (`#memories`) on the µLearn CHN community website.

Every asset incorporated into this section was physically inspected, measured, and verified on disk. The collection exclusively contains **authentic community photography** taken at College of Engineering Chengannur (CEC) and genuine event photographs extracted from high-resolution poster artwork. No promotional graphic posters, duplicate screenshots, sponsor-only slides, or stock photography are used.

All image derivatives have been stripped of EXIF orientation tags (`0x0112`) and GPS coordinates (`0x8825`) to guarantee absolute privacy and clean rendering.

---

## 2. Six-Frame Editorial Collage Mappings

The editorial collage features six asymmetric polaroid-style frames adhering to the Playful Neo-Brutalist design tokens.

| Frame | Label | Visual Scene & Description | Aspect Ratio | Dimensions (1x / 2x) | Size (1x / 2x) | Target Lightbox ID | Source Original Asset |
|---|---|---|---|---|---|---|---|
| **p1** | Lab Session Overview | Hands-on coding session in the CEC computer lab | 1.80 : 1 | 460×256 / 920×511 | 23.8 KB / 84.2 KB | `lightbox-img-7834` | `Memories/IMG_7834_xrr7b7.jpg` |
| **p2** | Mentored Workshop | Mentors guiding students through technical concepts | 2.00 : 1 | 460×230 / 920×460 | 22.2 KB / 72.3 KB | `lightbox-img-9803` | `Memories/IMG_9803_ixchge.jpg` |
| **p3** | Community Gathering | Enthusiastic learners gathered on campus | 1.90 : 1 | 460×242 / 920×483 | 18.3 KB / 60.7 KB | `lightbox-img-5086` | `Memories/IMG_5086_tm6kwh.jpg` |
| **p4** | Peer Collaboration | Students collaborating at computer lab workstations | 1.80 : 1 | 460×255 / 920×511 | 17.5 KB / 58.0 KB | `lightbox-img-7789` | `Memories/IMG_7789_qyh10e.jpg` |
| **p5** (Center) | µLearn CHN Community | Large group photograph in front of CEC main building | 1.76 : 1 | 460×261 / 920×521 / 1200×680 | 22.7 KB / 72.7 KB / 109.5 KB | `lightbox-img-5086` | `Memories/IMG_5086_tm6kwh.jpg` |
| **p6** | Technical Demo | Instructors presenting live demonstration on projector | 1.10 : 1 | 460×418 / 920×836 | 30.7 KB / 101.6 KB | `lightbox-img-7844` | `Memories/IMG_7844_lclzmf.jpg` |

*Verification Check:* All 13 collage derivative files physically exist in `img/memories/`, are properly formatted in WebP, and meet the strict performance budget.

---

## 3. Approved 11-Item Lightbox Gallery Register

The lightbox collection consists of exactly 11 items: 6 full-resolution community photographs and 5 genuine event photos extracted from high-resolution poster artwork.

| Item ID | Category | Title | Dimensions | File Size | Source / Origin | Observable Scene Description |
|---|---|---|---|---|---|---|
| `lightbox-img-5086` | Community | µLearn CHN Community Group | 1600 × 1067 | 210.9 KB | `IMG_5086_tm6kwh.jpg` | Large student group photo in front of the College of Engineering Chengannur main building. |
| `lightbox-img-7789` | Workshops | Computer Lab Technical Session | 1600 × 1200 | 199.8 KB | `IMG_7789_qyh10e.jpg` | Students participating in a hands-on technical workshop guided by student mentors. |
| `lightbox-img-7834` | Workshops | Computer Lab Working Session | 1600 × 1200 | 216.8 KB | `IMG_7834_xrr7b7.jpg` | Peer learning and collaborative development inside the college computer centre. |
| `lightbox-img-7844` | Workshops | Interactive Workshop & Demo | 1600 × 1200 | 219.3 KB | `IMG_7844_lclzmf.jpg` | Live screen projections and interactive mentoring session for engineering students. |
| `lightbox-img-9798` | Design | Intro to Figma UI/UX Workshop | 900 × 1600 | 98.2 KB | `IMG_9798_mvknx7.jpg` | Design session focusing on Figma fundamentals and interface creation. |
| `lightbox-img-9803` | Workshops | Mentored Coding Session | 1600 × 900 | 196.9 KB | `IMG_9803_ixchge.jpg` | Hands-on coding and problem-solving with community mentors at computer desks. |
| `photo-odyssey-wrap` | ODYSSEY | ODYSSEY Community Wrap | 615 × 352 | 41.2 KB | Extracted from ODYSSEY artwork | Hackathon participants and organizers celebrate at conclusion of 32-hour ODYSSEY. |
| `photo-odyssey-stage` | ODYSSEY | ODYSSEY Stage Session | 507 × 332 | 15.1 KB | Extracted from ODYSSEY artwork | Speaker addressing participants during ODYSSEY opening ceremony. |
| `photo-buildathon-podium` | Buildathon | Buildathon Winners — Frustrated Devs | 521 × 312 | 26.6 KB | Extracted from Buildathon artwork | First place team Frustrated Devs receiving recognition at Buildathon (µFIFA × Gemma 4). |
| `photo-bwai-group` | Build with AI | Build with AI Group | 618 × 342 | 50.3 KB | Extracted from Build with AI artwork | Participants and mentors after the Build with AI workshop and hackathon. |
| `photo-useless-glimpses` | Useless Projects | Useless Projects 3.0 Celebratory Evening | 554 × 330 | 35.6 KB | Extracted from Useless Projects artwork | Participants sharing humorous and creative inventions during Useless Projects 3.0. |

*Verification Check:* All 11 lightbox assets physically exist, are non-upscaled genuine photographs, and are registered in `data/memories.js`.

---

## 4. Explicitly Excluded & Rejected Assets

Per `PROJECT_MASTER_SPEC.md` §9.2 and `ASSET_MAPPING.md` §4, the following items are strictly barred from the Memories section:

1. **`sources/mulearn/Memories/event5_zdu88j.jpg`:**
   - *Status:* **REJECTED from Memories.**
   - *Reason:* Promotional graphic poster ("Weekly Twitches / Salt-Mango Tree", orange artwork, text-only graphic). It is not a community photograph.
2. **`sources/mulearn/Events/Odessey/Screenshot 2026-11-19 212307.png` & `212314.png`:**
   - *Status:* **REJECTED.**
   - *Reason:* Low-resolution duplicate screenshots (400×500 and 407×507) of posters already available at higher resolution.
3. **Sponsor-Only Slides:**
   - *Status:* **REJECTED.**
   - *Reason:* 15 sponsor-only logos, partner slides, and registration teasers excluded per Spec §9.2 Rule 7.
4. **B&W Type Race Winner Portraits:**
   - *Status:* **REJECTED from Memories.**
   - *Reason:* B&W cutout portraits belong strictly to Type Race event details, not standalone community memories.
5. **Instagram Screenshots:**
   - *Status:* **REJECTED.**
   - *Reason:* No images with visible Instagram UI chrome, like counts, or profile headers are included.

---

## 5. Technical Verification & Integrity Checks

- **Zero Upscaling:** Every derivative width/height is less than or equal to the native source asset.
- **Metadata Protection:** All EXIF metadata (orientation tag `0x0112`) and geolocation coordinates (GPS tag `0x8825`) stripped during derivative generation.
- **Source Protection:** Source directory `sources/mulearn/` remains pristine and untouched. No deployable HTML or CSS references `sources/`.
- **Project Verification:** `py scripts/verify_project.py` confirmed 96/96 derivatives valid, with 0 errors and 0 warnings.

---

## 6. Semantic Section Structure (`#memories`)

The `#memories` section replaces the previous anchor stub:

- **Element:** Semantic `<section id="memories" class="section section--clip section--ruled section--white memories" aria-labelledby="memories-title">`
- **Heading:** `h2#memories-title` ("Captured memories" with accent highlight)
- **Kicker:** `<span class="section-label section-label--mint">Community moments</span>`
- **Lead Text:** Verified copy describing community moments at College of Engineering Chengannur without unverified dates or claims.
- **Anchors Connected:**
  - Header Nav: `.site-nav__link[href="#memories"]`
  - About CTA: `a[href="#memories"]` ("Our journey")
  - Footer Nav: `.footer__nav-link[href="#memories"]`
- **Responsive Layout:** Contained within `.container.container--content.layer`, with `.section--clip` guaranteeing zero horizontal scroll across 320px, 390px, 768px, 1024px, and 1440px viewports.
