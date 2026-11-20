# µLearn CHN — ASSET_MAPPING.md

**Stage 02 · Asset inspection & mapping.** Inspection only: no HTML/CSS/JS was changed, nothing was renamed, moved, resized or discarded. The archive was extracted to a scratch folder purely so files could be viewed; all paths below are relative to the ZIP (`mulearn.zip`, root folder `mulearn/`).

**Legend.** ✅ **Verified** = directly stated by a filename, folder name, or text visible in the image/video. ⚠️ **Assumption** = my inference; needs your confirmation. ❓ **Unknown** = no evidence in the archive.

## Key findings (read first)

- **Event media are mostly Instagram-post screenshots, not raw photographs.** 50 PNGs named `Screenshot 2026-11-19 …` (all captured 21:35–21:42) are promo posters, sponsor cards, winner cards and “glimpses” collages. Genuine photographs appear only *inside* those posters, at ~300–600 px wide, except for one landscape frame (`Odessey/Screenshot 2026-11-19 212606.png`, 507×332). The design system says event cards should use genuine event photographs. **Decision needed** (see §6).
- **Tech Forge has zero still images.** Its only asset is one 15 s video whose sampled frames show an animated “TECHFORGE 2.0” title card.
- **The prototype’s three event cards are 4:3 landscape; every event image is portrait** (≈ 0.83 w/h). Cover-cropping will cut ~35% of each poster’s height.
- **Only 6 real photographs exist for 8 photo slots that want landscape/portrait photography** (hero, about, 6 collage frames) — plus 1 poster graphic. Some reuse (different crops) or poster-embedded crops will be required.
- **Existing CSS applies `filter:grayscale(1)` to every `.photo` except the collage.** Colour event posters and colour team portraits would render black-and-white; your reference board shows colour in the Events and Team cards. Not changed — flagged for a decision.
- **The real logo (`mulearn_logo.png`) is 262×112 with an opaque white background** and a blue→purple gradient. The prototype’s nav uses an SVG asterisk + text, not this file.
- **Spelling mismatch:** folder `Odessey` vs. poster text “ODYSSEY” (all Odyssey posters). Prototype/brief use “Odessey”.
- **Prototype event subtitles** (“Hands-on · Open to all”, “Teams of 4 · 24 hours”, “Solo · Fastest fingers win”) were placeholder copy I wrote; nothing in the archive supports them. Treat as unverified and replace.

## 1. Complete asset inventory

85 files in 11 folders · 86.1 MB total. Counts: logo 1 · Team 21 · Memories 7 · Event PNG screenshots 50 · Event MP4 6. Folder sizes: Team 23.2 MB, Memories 18.7 MB, Events 44.2 MB.

### 1.1 Logo / branding

| Path | Dimensions | Orientation | Size | Notes |
|---|---|---|---|---|
| `mulearn/mulearn_logo.png` | 262×112 | landscape | 7 KB | ✅ Wordmark “µlearn CHN”, blue→purple gradient; opaque white background (alpha present but corner pixel is opaque white); low-res |

No other logo/branding files (no SVG, no favicon, no brand guide). Partner/sponsor logos exist only embedded in posters.

### 1.2 Team photographs (21)

| Path | Dimensions | Orientation | Size | Notes |
|---|---|---|---|---|
| `mulearn/Team/1_geetha_s__Lead_Enabler.jpg` | 400×514 | portrait | 81 KB | Passport-style, plain background; low-res |
| `mulearn/Team/2_Nithin_Jayakumar__Campus_Lead.jpg` | 1000×1500 | portrait | 109 KB |  |
| `mulearn/Team/3_Divyalakshmi__Campus_Co-Lead.jpg` | 1180×1572 | portrait | 212 KB |  |
| `mulearn/Team/4_govind_j_s__Creative_Lead.webp` | 1273×1662 | portrait | 142 KB | WebP (others JPG/PNG); foliage background |
| `mulearn/Team/5_Hanin_C_K__Operational_Lead.jpg` | 1653×1989 | portrait | 732 KB |  |
| `mulearn/Team/6_Amanul_Farhan__Technical_Lead.jpg` | 1000×1500 | portrait | 154 KB |  |
| `mulearn/Team/7_Pavithra_A__Media_Lead.jpg` | 1756×3021 | portrait | 1.1 MB | Tall ~0.58 ratio |
| `mulearn/Team/8_Albin_Thomas__Content_Lead.jpg` | 2268×4032 | portrait | 3.4 MB | Very tall 9:16 crop; 3.5 MB |
| `mulearn/Team/9_Melwin_Shibu_Mathew__Operational_Team.jpg` | 1892×2168 | portrait | 1.3 MB |  |
| `mulearn/Team/10_Sara_Shaji__Operational_Team.jpg` | 2268×4032 | portrait | 507 KB | Very tall 9:16 crop |
| `mulearn/Team/11_Afsal_S__Designer.png` | 896×1152 | portrait | 1.1 MB | Cut-out style on white; PNG, 1.1 MB |
| `mulearn/Team/12_Vismaya_Gawri_Krishnan__Designer.jpg` | 1200×1600 | portrait | 307 KB |  |
| `mulearn/Team/13_Karthika_S__Content_Team.jpg` | 780×1040 | portrait | 90 KB |  |
| `mulearn/Team/14_Sreelakshmi_M__Content_Team.jpg` | 3120×4160 | portrait | 1.8 MB |  |
| `mulearn/Team/15_Parvathy_Vinayan__Media_Team.jpg` | 900×1600 | portrait | 150 KB | Tall 9:16 crop |
| `mulearn/Team/16_Brijith_K_Reji__Media_Team.jpg` | 768×1344 | portrait | 597 KB | Tall 9:16 crop; seated, indoor |
| `mulearn/Team/17_Adhi_Narayan__IG_Lead-AI.jpg` | 2056×2176 | portrait | 3.0 MB |  |
| `mulearn/Team/18_Al_Ameen__IG_Lead-UI_UX.jpg` | 4000×3000 (EXIF rot=6) | landscape | 6.4 MB | Stored landscape with EXIF rotate-90°; displays upright in browsers but rotated in tools that ignore EXIF; 6.7 MB |
| `mulearn/Team/19_Amal_S__IG_Lead-Cyber_Security.jpg` | 2805×3000 | portrait | 1.9 MB |  |
| `mulearn/Team/20_Abhiram_J__IG_Lead-Web.jpg` | 1023×1018 | landscape | 111 KB | Near-square (1023×1018) |
| `mulearn/Team/21_Swathy_J__IG_Lead-Entrepreneurship.jpg` | 960×1173 | portrait | 89 KB |  |

### 1.3 Memories / community photographs (7)

| Path | Dimensions | Orientation | Size | Notes |
|---|---|---|---|---|
| `mulearn/Memories/IMG_5086_tm6kwh.jpg` | 6000×4000 | landscape | 4.0 MB | ✅ Large group photo in front of the College of Engineering Chengannur building; people seated on tarmac; wide-angle |
| `mulearn/Memories/IMG_7789_qyh10e.jpg` | 4032×3024 | landscape | 2.6 MB | Computer lab session; standing speaker (white shirt) at left, students in blue uniforms |
| `mulearn/Memories/IMG_7834_xrr7b7.jpg` | 4032×3024 | landscape | 3.7 MB | Computer lab, wide room view, students at desks |
| `mulearn/Memories/IMG_7844_lclzmf.jpg` | 4032×3024 | landscape | 3.1 MB | Computer lab with projected screen; two instructors standing |
| `mulearn/Memories/IMG_9798_mvknx7.jpg` | 2268×4032 | portrait | 1.5 MB | Portrait; projector shows “Intro to Figma”; instructor + students |
| `mulearn/Memories/IMG_9803_ixchge.jpg` | 5712×3213 | landscape | 3.9 MB | Computer lab; woman instructor standing at left; 16:9 |
| `mulearn/Memories/event5_zdu88j.jpg` | 1024×1280 | portrait | 113 KB | NOT a photograph: orange promo graphic “What’s scarier, failure or regret?”, Wednesday 8.00 PM, “Weekly Twitches · salt-mango Tree”, #lobby voice channel |

### 1.4 Event assets (56)


**Build with AI** — folder `mulearn/Events/build with ai/`

| Path | Dimensions | Orientation | Size | Content (what is visible) |
|---|---|---|---|---|
| `mulearn/Events/build with ai/Screenshot 2026-11-19 213938.png` | 693×826 | portrait | 516 KB | Title poster: "Build a Gemini-Powered YouTube Summarizer", 4.00–5.30 pm, 31 March 2026, MCA CC2 |
| `mulearn/Events/build with ai/Screenshot 2026-11-19 213945.png` | 695×817 | portrait | 737 KB | "Glimpses" poster with an embedded photo collage of lab sessions |
| `mulearn/Events/build with ai/Screenshot 2026-11-19 213958.png` | 692×827 | portrait | 573 KB | Speakers poster (Vishnu Harikumar, Swathy J) with portrait photos |
| `mulearn/Events/build with ai/Screenshot 2026-11-19 214015.png` | 697×818 | portrait | 469 KB | "16-hr AI Hackathon" poster, 6–7 April 2026 |
| `mulearn/Events/build with ai/Screenshot 2026-11-19 214025.png` | 692×817 | portrait | 494 KB | Associate partner poster (PRODDEC) |
| `mulearn/Events/build with ai/Screenshot 2026-11-19 214034.png` | 690×822 | portrait | 691 KB | "That's a wrap!" poster with embedded group photo |
| `mulearn/Events/build with ai/Screenshot 2026-11-19 214156.png` | 687×820 | portrait | 619 KB | Thank-you poster (Abhijith J Nair, Jithu Girish – "Intro to Vibe Coding") |
| `mulearn/Events/build with ai/Screenshot 2026-11-19 214200.png` | 692×813 | portrait | 492 KB | Creative Project – team "Amingos" (embedded photo) |
| `mulearn/Events/build with ai/Screenshot 2026-11-19 214204.png` | 697×810 | portrait | 548 KB | Innovative Project – team "Bizzare" (embedded photo) |
| `mulearn/Events/build with ai/Screenshot 2026-11-19 214208.png` | 698×786 | portrait | 471 KB | Winners – team "Phoenix" (embedded photo) |
| `mulearn/Events/build with ai/Recording 2026-11-19 214133.mp4` | 490×818 | portrait | 7.3 MB | MP4 (H.264 + AAC), 32.3 s |

**Buildathon** — folder `mulearn/Events/Buildathon/`

| Path | Dimensions | Orientation | Size | Content (what is visible) |
|---|---|---|---|---|
| `mulearn/Events/Buildathon/Screenshot 2026-11-19 213523.png` | 693×821 | portrait | 380 KB | Teaser poster (trophy), 17–18 July, 5PM–9AM, COE Chengannur; "µFIFA x Gemma 4" branding |
| `mulearn/Events/Buildathon/Screenshot 2026-11-19 213528.png` | 695×812 | portrait | 342 KB | Prize pool poster (₹7K*) |
| `mulearn/Events/Buildathon/Screenshot 2026-11-19 213532.png` | 685×817 | portrait | 364 KB | Registrations closed poster |
| `mulearn/Events/Buildathon/Screenshot 2026-11-19 213538.png` | 685×798 | portrait | 385 KB | Food partner – Mandi Mahal |
| `mulearn/Events/Buildathon/Screenshot 2026-11-19 213543.png` | 696×802 | portrait | 282 KB | Title sponsor – Blaze International Trading Academy (BITA) |
| `mulearn/Events/Buildathon/Screenshot 2026-11-19 213548.png` | 692×797 | portrait | 350 KB | Refreshment partner – The Chocolate Drop |
| `mulearn/Events/Buildathon/Screenshot 2026-11-19 213552.png` | 688×776 | portrait | 307 KB | Fitness partner – V Fit Fitness Hub |
| `mulearn/Events/Buildathon/Screenshot 2026-11-19 213556.png` | 686×792 | portrait | 371 KB | Prize sponsor – Juice It Up |
| `mulearn/Events/Buildathon/Screenshot 2026-11-19 213600.png` | 695×797 | portrait | 292 KB | Co-food partner – Spinners |
| `mulearn/Events/Buildathon/Screenshot 2026-11-19 213607.png` | 701×863 | portrait | 762 KB | "Penalty Pursuit" poster, powered by The Cowboy |
| `mulearn/Events/Buildathon/Screenshot 2026-11-19 213801.png` | 693×852 | portrait | 491 KB | Third place – Holo (embedded photo) |
| `mulearn/Events/Buildathon/Screenshot 2026-11-19 213807.png` | 695×865 | portrait | 619 KB | First place – Frustrated Devs (embedded photo) |
| `mulearn/Events/Buildathon/Screenshot 2026-11-19 213812.png` | 695×861 | portrait | 639 KB | Second place – Tek Knights (embedded photo) |
| `mulearn/Events/Buildathon/Recording 2026-11-19 213740.mp4` | 480×818 | portrait | 7.3 MB | MP4 (H.264 + AAC), 33.9 s |

**Odessey** — folder `mulearn/Events/Odessey/`

| Path | Dimensions | Orientation | Size | Content (what is visible) |
|---|---|---|---|---|
| `mulearn/Events/Odessey/Screenshot 2026-11-19 212307.png` | 400×500 | portrait | 224 KB | Date poster 20–21 Sept 2026 (low-res near-duplicate of 213134) |
| `mulearn/Events/Odessey/Screenshot 2026-11-19 212314.png` | 407×507 | portrait | 230 KB | Prize pool ₹15,000 poster (low-res near-duplicate of 213156) |
| `mulearn/Events/Odessey/Screenshot 2026-11-19 212606.png` | 507×332 | landscape | 213 KB | Raw-looking photo: speaker at front under an ODYSSEY banner, audience (landscape; same scene as video 212656) |
| `mulearn/Events/Odessey/Screenshot 2026-11-19 213134.png` | 697×816 | portrait | 458 KB | Date poster 20–21 Sept 2026 |
| `mulearn/Events/Odessey/Screenshot 2026-11-19 213144.png` | 650×792 | portrait | 353 KB | "Set to sail" poster (website odysseycec.in) |
| `mulearn/Events/Odessey/Screenshot 2026-11-19 213150.png` | 680×816 | portrait | 498 KB | Registrations open poster |
| `mulearn/Events/Odessey/Screenshot 2026-11-19 213156.png` | 695×782 | portrait | 444 KB | Prize pool ₹15,000 poster |
| `mulearn/Events/Odessey/Screenshot 2026-11-19 213205.png` | 688×805 | portrait | 529 KB | "The Journey Within" teaser |
| `mulearn/Events/Odessey/Screenshot 2026-11-19 213211.png` | 696×812 | portrait | 500 KB | Registrations closed poster |
| `mulearn/Events/Odessey/Screenshot 2026-11-19 213218.png` | 690×822 | portrait | 500 KB | Technology partner – Google for Developers |
| `mulearn/Events/Odessey/Screenshot 2026-11-19 213225.png` | 688×817 | portrait | 485 KB | Ticketing partner – MakeMyPass |
| `mulearn/Events/Odessey/Screenshot 2026-11-19 213232.png` | 693×815 | portrait | 494 KB | Food partner – Malabar Fresh Haute Cuisine |
| `mulearn/Events/Odessey/Screenshot 2026-11-19 213238.png` | 683×795 | portrait | 533 KB | Winners: 2nd Runner-Up – Team Jijñāsus (embedded photo) |
| `mulearn/Events/Odessey/Screenshot 2026-11-19 213243.png` | 688×801 | portrait | 524 KB | Winners: 1st Place – Team SPARX (embedded photo) |
| `mulearn/Events/Odessey/Screenshot 2026-11-19 213249.png` | 688×811 | portrait | 588 KB | Winners: 1st Runner-Up – Team Cypher (embedded photo) |
| `mulearn/Events/Odessey/Screenshot 2026-11-19 213254.png` | 677×787 | portrait | 618 KB | "That's a wrap!" poster with embedded crowd group photo |
| `mulearn/Events/Odessey/Screenshot 2026-11-19 213303.png` | 687×772 | portrait | 519 KB | Thank-you-to-mentors poster (Jerry Sanju Joanes, Abhijith J Nair, Joe Abraham K) with portraits |
| `mulearn/Events/Odessey/Recording 2026-11-19 212442.mp4` | 504×296 | landscape | 2.2 MB | MP4 (H.264 + AAC), 23.3 s |
| `mulearn/Events/Odessey/Recording 2026-11-19 212656.mp4` | 508×330 | landscape | 463 KB | MP4 (H.264 + AAC), 3.8 s |
| `mulearn/Events/Odessey/Recording 2026-11-19 212743.mp4` | 504×290 | landscape | 493 KB | MP4 (H.264 + AAC), 4.3 s |

**Tech Forge** — folder `mulearn/Events/Tech forge/`

| Path | Dimensions | Orientation | Size | Content (what is visible) |
|---|---|---|---|---|
| `mulearn/Events/Tech forge/Recording 2026-11-19 212924.mp4` | 496×638 | portrait | 2.7 MB | MP4 (H.264 + AAC), 15.1 s |

**Type Race** — folder `mulearn/Events/Type Race/`

| Path | Dimensions | Orientation | Size | Content (what is visible) |
|---|---|---|---|---|
| `mulearn/Events/Type Race/Screenshot 2026-11-19 213923.png` | 696×822 | portrait | 852 KB | Event poster: CC2, 26/03/2026, 12:15–1:00 PM; IEEE branding |
| `mulearn/Events/Type Race/Screenshot 2026-11-19 213929.png` | 697×802 | portrait | 894 KB | Winners poster (Christo Chery George, Nevin Mathew, Niranjan V Chandran) – B&W portraits |

**Useless** — folder `mulearn/Events/Useless/`

| Path | Dimensions | Orientation | Size | Content (what is visible) |
|---|---|---|---|---|
| `mulearn/Events/Useless/Screenshot 2026-11-19 213404.png` | 692×816 | portrait | 259 KB | Date poster "Useless Projects 3.0", September 11–12 |
| `mulearn/Events/Useless/Screenshot 2026-11-19 213414.png` | 692×805 | portrait | 340 KB | "What is useless projects?" explainer poster |
| `mulearn/Events/Useless/Screenshot 2026-11-19 213434.png` | 685×807 | portrait | 270 KB | "Registration closes tomorrow" poster |
| `mulearn/Events/Useless/Screenshot 2026-11-19 213837.png` | 697×823 | portrait | 541 KB | "Celebratory Evening Glimpses" with embedded group photo |
| `mulearn/Events/Useless/Screenshot 2026-11-19 213851.png` | 696×828 | portrait | 247 KB | Winners poster (no winners named on image) |

**Web Slingers** — folder `mulearn/Events/Web slingers/`

| Path | Dimensions | Orientation | Size | Content (what is visible) |
|---|---|---|---|---|
| `mulearn/Events/Web slingers/Screenshot 2026-11-19 213322.png` | 656×822 | portrait | 595 KB | Podium poster: Marvel Jesus / Titans / Cosmopolitans (embedded photos) |
| `mulearn/Events/Web slingers/Screenshot 2026-11-19 213328.png` | 650×831 | portrait | 662 KB | Event details poster (date/venue/time; text partly small) |
| `mulearn/Events/Web slingers/Screenshot 2026-11-19 213334.png` | 646×825 | portrait | 775 KB | "Glimpses" poster with embedded photo collage |

**Near-duplicates (kept, not discarded):** `Odessey/…212307.png` ≈ `…213134.png` (same date poster; 212307 is lower-res) and `Odessey/…212314.png` ≈ `…213156.png` (same prize-pool poster; 212314 is lower-res).

**Screenshot artefacts:** carousel-arrow overlays are visible on at least Buildathon `…213523`, Odessey `…213205` and `…213254`, and Useless `…213414`, `…213837`, `…213851`. These would need cropping or masking if the posters are shown as-is.

### 1.5 Video content (sampled every ~6 s; descriptions approximate)

| Path | Folder says | Visible evidence | Event confidence |
|---|---|---|---|
| `mulearn/Events/Buildathon/Recording 2026-11-19 213740.mp4` | Buildathon | Lab audience, girl speaking into a microphone, night scene with people at laptops, closing card listing sponsor logos (Juice It Up, Mandi Mahal, BITA, V Fit, Spinners) that match the Buildathon posters | ✅ High |
| `mulearn/Events/Odessey/Recording 2026-11-19 212442.mp4` | Odessey | Black-and-white cinematic clips, a printed “20–21 September 2026” poster; landscape | ✅ High (poster date matches Odyssey) |
| `mulearn/Events/Odessey/Recording 2026-11-19 212656.mp4` | Odessey | Room with ODYSSEY banner and a speaker — same scene as still `…212606.png` | ✅ High |
| `mulearn/Events/Odessey/Recording 2026-11-19 212743.mp4` | Odessey | Two men seated at a table; no on-screen event identifier | ⚠️ Folder only |
| `mulearn/Events/Tech forge/Recording 2026-11-19 212924.mp4` | Tech forge | Animated title card “TECHFORGE 2.0” on dark purple | ✅ High (on-screen text) |
| `mulearn/Events/build with ai/Recording 2026-11-19 214133.mp4` | build with ai | Students in a lab, speakers with a microphone/phone, code on screens, group pose at a projector; no on-screen “Build with AI” text in sampled frames | ⚠️ Folder only (content consistent) |

## 2. Team member mapping

Names and roles below are read **only from filenames** (underscores → spaces; capitalisation normalised; `__` separates name from role). No accompanying roster, caption or document exists in the archive. I did not (and cannot) confirm that a face matches the name in its filename, so “Verified?” means *the filename states it* — nothing more.

| Person | Role | Image filename | Verified? |
|---|---|---|---|
| Geetha S | Lead Enabler | `mulearn/Team/1_geetha_s__Lead_Enabler.jpg` | Filename only (filename is lowercase; spelling normalised ⚠️) |
| Nithin Jayakumar | Campus Lead | `mulearn/Team/2_Nithin_Jayakumar__Campus_Lead.jpg` | Filename only |
| Divyalakshmi | Campus Co-Lead | `mulearn/Team/3_Divyalakshmi__Campus_Co-Lead.jpg` | Filename only |
| Govind J S | Creative Lead | `mulearn/Team/4_govind_j_s__Creative_Lead.webp` | Filename only (lowercase; “J S” read as initials ⚠️) |
| Hanin C K | Operational Lead | `mulearn/Team/5_Hanin_C_K__Operational_Lead.jpg` | Filename only; role reads “Operational Lead” (prototype says “Operations Lead”) |
| Amanul Farhan | Technical Lead | `mulearn/Team/6_Amanul_Farhan__Technical_Lead.jpg` | Filename only |
| Pavithra A | Media Lead | `mulearn/Team/7_Pavithra_A__Media_Lead.jpg` | Filename only |
| Albin Thomas | Content Lead | `mulearn/Team/8_Albin_Thomas__Content_Lead.jpg` | Filename only |
| Melwin Shibu Mathew | Operational Team | `mulearn/Team/9_Melwin_Shibu_Mathew__Operational_Team.jpg` | Filename only |
| Sara Shaji | Operational Team | `mulearn/Team/10_Sara_Shaji__Operational_Team.jpg` | Filename only |
| Afsal S | Designer | `mulearn/Team/11_Afsal_S__Designer.png` | Filename only |
| Vismaya Gawri Krishnan | Designer | `mulearn/Team/12_Vismaya_Gawri_Krishnan__Designer.jpg` | Filename only |
| Karthika S | Content Team | `mulearn/Team/13_Karthika_S__Content_Team.jpg` | Filename only |
| Sreelakshmi M | Content Team | `mulearn/Team/14_Sreelakshmi_M__Content_Team.jpg` | Filename only |
| Parvathy Vinayan | Media Team | `mulearn/Team/15_Parvathy_Vinayan__Media_Team.jpg` | Filename only |
| Brijith K Reji | Media Team | `mulearn/Team/16_Brijith_K_Reji__Media_Team.jpg` | Filename only |
| Adhi Narayan | IG Lead – AI | `mulearn/Team/17_Adhi_Narayan__IG_Lead-AI.jpg` | Filename only; “IG” is not expanded anywhere in the archive |
| Al Ameen | IG Lead – UI/UX | `mulearn/Team/18_Al_Ameen__IG_Lead-UI_UX.jpg` | Filename only; “IG” is not expanded anywhere in the archive |
| Amal S | IG Lead – Cyber Security | `mulearn/Team/19_Amal_S__IG_Lead-Cyber_Security.jpg` | Filename only; “IG” is not expanded anywhere in the archive |
| Abhiram J | IG Lead – Web | `mulearn/Team/20_Abhiram_J__IG_Lead-Web.jpg` | Filename only; “IG” is not expanded anywhere in the archive |
| Swathy J | IG Lead – Entrepreneurship | `mulearn/Team/21_Swathy_J__IG_Lead-Entrepreneurship.jpg` | Filename only; a “Swathy J” also appears as a Build with AI speaker poster — plausibly the same person, ❓ unconfirmed |

**Ambiguities to resolve:** (a) `Pavithra A` (Media Lead) vs `Parvathy Vinayan` (Media Team) are different filenames and I treat them as two people. (b) Spelling of `Divyalakshmi`, `Vismaya Gawri Krishnan`, `Brijith K Reji` is as typed in filenames. (c) “Lead Enabler” has no explanation; I make no assumption about the person’s affiliation. (d) Photo treatment is inconsistent (cut-out, passport, outdoor, indoor, mixed ratios); the reference shows uniform framing with coloured backdrops.

**Prototype’s four team cards → files** (labels from the prototype; ✅ role label in filename matches or ⚠️ differs):

| Prototype label | Matching file | Match |
|---|---|---|
| Campus Lead | `Team/2_Nithin_Jayakumar__Campus_Lead.jpg` (1000×1500) | ✅ exact |
| Technical Lead | `Team/6_Amanul_Farhan__Technical_Lead.jpg` (1000×1500) | ✅ exact |
| Creative Lead | `Team/4_govind_j_s__Creative_Lead.webp` (1273×1662) | ✅ exact |
| Operations Lead | `Team/5_Hanin_C_K__Operational_Lead.jpg` (1653×1989) | ⚠️ filename says “Operational Lead”; confirm wording |

The other 17 members have no slot in the prototype (its “View All” button implies a fuller team view that is not built).

## 3. Event media mapping

Every event is identified by **both** its folder name and branding/text visible on the images (✅). The one exception is noted. Dates/details shown are *as printed on the posters* and are unverified beyond that.

| Event | Stills | Videos | Evidence | Best still (portrait posters) | Genuine photos available |
|---|---|---|---|---|---|
| Build with AI | 10 (`Events/build with ai/`) | 1 | ✅ “Build with AI” on all posters | `…213938.png` (title) | Embedded in `…213945` (glimpses), `…214034` (group), `…213958`/`…214156` (portraits), `…214200/204/208` (teams) |
| Buildathon | 13 (`Events/Buildathon/`) | 1 | ✅ “BUILDATHON” (µFIFA × Gemma 4) | `…213523.png` (trophy teaser) | Embedded in `…213801/807/812` (podium teams) |
| Odessey | 17 (`Events/Odessey/`) | 3 | ✅ posters say “ODYSSEY” (folder spelling differs) | `…213134.png` (date) or `…213144.png` | `…212606.png` raw landscape frame; embedded in `…213254` (crowd), `…213238/243/249` (teams), `…213303` (mentors) |
| Tech Forge | **0** | 1 (`Events/Tech forge/`) | ✅ “TECHFORGE 2.0” on-screen | **none** | none |
| Type Race | 2 (`Events/Type Race/`) | 0 | ✅ “Type Race” | `…213923.png` | none (winner portraits are B&W, embedded in `…213929`) |
| Useless | 5 (`Events/Useless/`) | 0 | ✅ “Useless Projects 3.0” | `…213404.png` | Embedded in `…213837` (group) |
| Web Slingers | 3 (`Events/Web slingers/`) | 0 | ✅ “WEB SLINGERS” | `…213322.png` (podium photos) | Embedded in `…213322`, `…213334` (glimpses collage) |

Full per-file descriptions are in §1.4 and video evidence in §1.5. No image was assigned to an event on filename alone: the folder name was cross-checked against on-image text for every folder except the three-clip `Odessey` videos and the Build with AI video noted as “folder only”.

### Event-card mapping for the prototype (3 cards)

| Card | Primary candidate | Alternate | Issue |
|---|---|---|---|
| Build with AI | `Events/build with ai/Screenshot 2026-11-19 213938.png` | `…214034.png` (group photo inside poster) | Poster, not a photograph |
| Tech Forge | *No still.* Video `Events/Tech forge/Recording 2026-11-19 212924.mp4` | — | Needs a still/poster frame (see §6) |
| Type Race | `Events/Type Race/Screenshot 2026-11-19 213923.png` | `…213929.png` (winners) | Poster, not a photograph |

The brief lists **seven** events; the prototype shows **three** cards. Cards for Buildathon, Odessey, Useless and Web Slingers do not exist in the approved design — confirm whether to add them or keep three featured events.

## 4. Memories photograph mapping

The collage slots are landscape-leaning (≈1.8–2.0 w/h) except `p6` (≈1.1); `p5` is the largest. Approximate inner image sizes are computed at a 1440 px viewport from the prototype CSS.

| Role | Recommended file | Why | Orientation / crop note |
|---|---|---|---|
| **Main feature** (`p5`, largest) | `Memories/IMG_5086_tm6kwh.jpg` (6000×4000) | Only whole-community group photo; identifies the institution (College of Engineering Chengannur); highest resolution | Landscape 3:2 → slot ≈1.76; light top/bottom crop; keep the seated crowd band |
| **Medium** (`p2`) | `Memories/IMG_9803_ixchge.jpg` (5712×3213) | Wide 16:9 lab scene, instructor at left | Slot ≈2.0 → minimal crop; anchor left |
| **Medium** (`p1`) | `Memories/IMG_7834_xrr7b7.jpg` (4032×3024) | Full-room view of a session | Slot ≈1.8; crop top/bottom |
| **Small** (`p6`, near-square) | `Memories/IMG_7844_lclzmf.jpg` (4032×3024) ⚠️ or `IMG_9798_mvknx7.jpg` (portrait) | Close to instructors + projected screen | Needs ≈1.1 crop; `IMG_9798` is portrait 9:16 and would crop to its middle band |
| **Small** (`p3`) | ❓ open | No spare unique photo | Options: second crop of `IMG_5086` (crowd close-up; ample resolution) or a crop from a poster-embedded photo (low-res) |
| **Small** (`p4`) | ❓ open | No spare unique photo | Option: different crop of `IMG_7789` |
| Unassigned | `Memories/event5_zdu88j.jpg` | It is a poster graphic, not a memory photograph | Kept in inventory; fits an Events/community-activity context better |

`IMG_7789_qyh10e.jpg` is the proposed **hero** (see §5), and `IMG_9798` the proposed **about** image, so six genuine photos cover eight slots only with reuse or open choices above.

## 5. Placeholder → real asset mapping

Source: `ulearn.html` (read only). Each placeholder is a `div.photo.ph` using `background-size:cover; background-position:center` with `--img:url('assets/…')` and a striped/gradient fallback. **No `<img>` or `<video>` elements exist.** Slot sizes are approximate at 1440 px.

| # | Placeholder (`--img` path) | Slot / aspect | Proposed real asset | Status |
|---|---|---|---|---|
| 1 | Hero — `assets/hero.jpg` (rotated 5°, offset shadow) | ≈600 px wide, 1 : 1.05 | `Memories/IMG_7789_qyh10e.jpg`; square-ish crop anchored left-centre on the speaker | ⚠️ no auditorium/packed-audience photo exists; best available |
| 2 | About — `assets/about.jpg` (rotated −4°) | ≈410×470, 4 : 4.6 | `Memories/IMG_9798_mvknx7.jpg`; centre-top crop on instructor + projector | ⚠️ portrait source fits slot; heavy vertical crop |
| 3 | Event 1 — `assets/event1.jpg` | ≈405×304, 4 : 3 | `Events/build with ai/Screenshot 2026-11-19 213938.png` | ⚠️ poster; portrait→landscape crop |
| 4 | Event 2 — `assets/event2.jpg` | ≈405×304, 4 : 3 | None for stills; video `Events/Tech forge/Recording 2026-11-19 212924.mp4` | ❓ missing still |
| 5 | Event 3 — `assets/event3.jpg` | ≈405×304, 4 : 3 | `Events/Type Race/Screenshot 2026-11-19 213923.png` | ⚠️ poster |
| 6 | Team 1 — `assets/team1.jpg` “Campus Lead” | ≈299×359, 3 : 3.6 | `Team/2_Nithin_Jayakumar__Campus_Lead.jpg` | ✅ role matches |
| 7 | Team 2 — `assets/team2.jpg` “Technical Lead” | same | `Team/6_Amanul_Farhan__Technical_Lead.jpg` | ✅ role matches |
| 8 | Team 3 — `assets/team3.jpg` “Creative Lead” | same | `Team/4_govind_j_s__Creative_Lead.webp` | ✅ role matches |
| 9 | Team 4 — `assets/team4.jpg` “Operations Lead” | same | `Team/5_Hanin_C_K__Operational_Lead.jpg` | ⚠️ label wording |
| 10 | Collage `p1` — `assets/m1.jpg` | ≈415×230 | `Memories/IMG_7834_xrr7b7.jpg` | ⚠️ proposal |
| 11 | Collage `p2` — `assets/m2.jpg` | ≈441×220 | `Memories/IMG_9803_ixchge.jpg` | ⚠️ proposal |
| 12 | Collage `p3` — `assets/m3.jpg` | ≈313×160 | ❓ open (crop of `IMG_5086` or poster-embedded photo) | ❓ decision |
| 13 | Collage `p4` — `assets/m4.jpg` | ≈338×190 | ❓ open (alternate crop of `IMG_7789`) | ❓ decision |
| 14 | Collage `p5` — `assets/m5.jpg` (largest) | ≈441×250 | `Memories/IMG_5086_tm6kwh.jpg` | ⚠️ proposal |
| 15 | Collage `p6` — `assets/m6.jpg` | ≈262×230 | `Memories/IMG_7844_lclzmf.jpg` | ⚠️ proposal |

**Non-photo elements:** the nav logo is an inline SVG asterisk + text (not `mulearn_logo.png`); the stars, triangles, squiggle and dot-grids are decorative SVG/CSS and need no assets. **No video slots exist**, so all 6 videos are currently unplaced.

**Things the real images will change (not applied):** (1) `aria-label`s like “Stage lights”, “Speaker on stage”, “Audience” describe the placeholders, not the real photos; (2) `.photo{filter:grayscale(1)}` would turn colour posters and portraits black-and-white; (3) the cover crop is `center`, so portrait posters in 4:3 slots will lose top/bottom — per-slot focal points or pre-cropped derivatives are needed; (4) the collage’s grayscale is already off, so those will render in colour.

## 6. Missing assets and uncertain identifications

- **Event photographs.** Original, full-resolution event photos (and a Tech Forge still) are not in the archive. *Options:* (A) use posters as-is; (B) crop the photos embedded in posters (≈300–600 px, soft at 2× retina); (C) you supply originals. The “Screenshot … 2026-11-19” naming suggests originals exist elsewhere (Instagram source/designer files).
- **Tech Forge still.** Needs your choice: a frame extracted from the video (derivative of your own asset) or a supplied image.
- **Packed-audience hero.** The reference hero is an auditorium crowd; none exists. Confirm using a lab-session photo or supplying one.
- **Team roster/captions.** No roster file, so names/roles are filename-derived only; confirm spellings, the role wording “Operational” vs “Operations”, and what “IG” and “Lead Enabler” mean for display.
- **People named on posters** (e.g. Swathy J, Abhijith J Nair, winner names) are *not* mapped to team files except the flagged “Swathy J” possibility. No identities were inferred from faces.
- **Logo.** Need a transparent/SVG, higher-resolution version, and a decision on whether the gradient wordmark replaces the prototype’s asterisk logo.
- **Event facts.** Dates, venues and categories (e.g. “workshop”, “hackathon”) must come from you; poster text was only used to confirm which event an image belongs to. Odessey/Odyssey spelling needs a ruling.
- **Seven vs three event cards**, and which team members appear beyond the four shown.
- **Memories gaps:** two collage slots lack unique photos; `event5_zdu88j.jpg` is not a photograph.
- **Consent/privacy:** many images show students; confirm permission for web use. Phone photos may carry EXIF location data (not inspected).

## 7. Recommended image optimisation requirements

Originals stay untouched in the archive; produce web derivatives into a new folder.

| Asset group | Display size (max) | Export (2× retina) | Format / budget |
|---|---|---|---|
| Hero | ≈600 px wide | 1200×1260 | AVIF/WebP + JPG fallback, ≤ 180 KB |
| About | ≈410×470 | 820×940 | WebP, ≤ 120 KB |
| Event cards (4:3) | ≈405×304 | 810×608 (pre-cropped from posters) | WebP, ≤ 90 KB each |
| Team portraits (3:3.6) | ≈299×359 | 600×720, face-centred | WebP, ≤ 70 KB; **apply EXIF rotation to `18_Al_Ameen…`**; upscaling `1_geetha_s…` (400×514) will look soft |
| Collage | ≤ ≈460 px wide | 920 px wide; main feature 1200 px | WebP, ≤ 110 KB (≤ 160 KB main) |
| Logo | ≈140 px wide | SVG, or PNG ≥ 600 px wide, transparent | — |
| Videos | cards ≤ ~400 px | Re-encode H.264 MP4 + WebM, source is only 480–508 px wide; add poster images | ≤ 1.5 MB each, muted/`playsinline`, lazy-loaded, no autoplay with sound |

**Also:** strip all EXIF/GPS metadata; use `loading="lazy"` and explicit width/height to avoid layout shift; the largest originals (`Team/18_Al_Ameen…` 6.7 MB, `Memories/IMG_5086…` 4 MB, `Team/8_Albin_Thomas…` 3.5 MB) must never ship unprocessed; keep the real filenames in a manifest so derivatives stay traceable; screenshot posters need carousel-arrow artefacts cropped out.

## Summary

The archive holds 1 logo, 21 team portraits (all with name + role in the filename), 7 memories files (6 photos + 1 poster graphic), 50 event poster screenshots and 6 event videos across all seven events — except that **Tech Forge has only a video**. The four prototype team cards map cleanly (one role-wording check); the memories collage can be filled for four of six slots plus hero and about with reuse caveats; event cards will use posters rather than photographs unless you choose otherwise.
