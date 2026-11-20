# PROJECT_MASTER_SPEC.md — µLearn CHN Website

**Version 1.0 · written in Phase 0 · 2026-11-20 · status: DRAFT pending client answers in §15**

This is the single source of truth. A new Claude session with no prior history must be able to implement its phase from this file + the latest project ZIP + `NEXT_PHASE.md`.

**Precedence when documents disagree:** `PROJECT_STATE.md` → *Decisions log* (newest wins) › this spec › `NEXT_PHASE.md` › `ASSET_MAPPING.md` › the prototype. Never resolve a conflict silently: record it in `PROJECT_STATE.md`.

**Legend used throughout:** ✅ verified from a source I actually read · 🟡 client-supplied, not independently verifiable · ⚠️ uncertain/needs confirmation · ❌ must not be claimed.

---

## 1. Project overview

- **What:** a single-page, responsive website for **µLearn CHN**, the µLearn student community of the **College of Engineering Chengannur (CEC)**, Kerala. Built as part of a selection task.
- **Must communicate:** what µLearn CHN is · what learning opportunities µLearn provides · what the CHN community actually does · who runs it · how a student joins.
- **Must be:** visually distinctive (not a SaaS template, not a copy of mulearn.org or the existing CHN site), responsive, accessible, fast, professionally implemented.
- **No backend.** Static site. No forms that submit data. All CTAs are links to official destinations (§8).
- **Inputs a session may receive:** `ulearn.html` prototype (reference only), `reference visual image` (primary visual target), `mulearn.zip` asset archive (85 files, see `ASSET_MAPPING.md`), the latest project ZIP.
- **Current date context:** 2026-11-20. Every event in the supplied materials appears to be in the past → the site must **not** present any event as upcoming (§7.4).

### µLearn vs µLearn CHN (content rule that governs all copy)
| | **µLearn (organisation / ecosystem)** | **µLearn CHN (this site)** |
|---|---|---|
| Who | µLearn Foundation, Technopark Phase 1, Thiruvananthapuram ✅ | Student community at CEC ✅(from client brief + existing CHN site meta) |
| Offers | Community, Mentors, Interest Groups, Roadmaps, Challenges, Opportunities, Karma points, Career Labs ✅ (mulearn.org) | Events seen on supplied posters, a CHN Discord server ✅, a student team ✅(filenames, ⚠️ roles) |
| Rule | Describe as *"across the µLearn network"*; link to official pages | Claim only what a poster, the CHN Discord, or the client states. Never transfer org-level programmes (e.g. weekly Learning Circles, Permute/Mutate/Amuse, "Launchpad") to CHN as fact. |

---

## 2. Creative direction — "Playful Neo-Brutalist Editorial" (locked)

Bold editorial typography · playful geometric decorations (stars, circles, arcs, squiggles, arrows, dotted grids) · strong 2px navy outlines · hard offset shadows (no blur) · intentional asymmetry · authentic community photography · clear hierarchy · youthful, creative, tech-oriented.

**Forbidden:** other design systems, gradients (the palette is flat colour only), glassmorphism, generic SaaS 3-icon grids/pricing-style cards, 3D, stock/generated people, rounded pill-heavy "soft UI", drop shadows with blur. New visual ideas need a written justification in `PROJECT_STATE.md`.

The final site is an *evolution* of the approved reference board: same hero statement, same section vocabulary (About, Events, Team, Memories, Join), same polaroid collage, same sticker-like decorations.

**Prototype fidelity note:** `ulearn.html` captured the palette, type, buttons, borders, shadows, decorations and section order. It is **not** a complete spec (see Phase-0 report §1 for its defects, e.g. the hero photo drops *below* the headline instead of sitting beside it).

---

## 3. Design tokens (canonical — copy into `css/tokens.css`)

```css
:root{
  /* colour */
  --c-bg:#F8F3E9;            /* cream, dominant background */
  --c-ink:#0F172A;           /* navy: text + all outlines */
  --c-primary:#6366F1;       /* indigo: fills, decoration */
  --c-primary-strong:#4F46E5;/* PROPOSED (decision D5): indigo for fills that carry white text */
  --c-accent:#FACC15;        /* yellow */
  --c-mint:#34D399;          /* mint (token name "secondary" in the brief) */
  --c-surface:#FFFFFF;

  /* shape */
  --bw:2px;  --border:var(--bw) solid var(--c-ink);
  --r-sm:8px; --r-md:12px; --r-lg:14px;
  --shadow-5:5px 5px 0 var(--c-ink);
  --shadow-6:6px 6px 0 var(--c-ink);
  --shadow-7:7px 7px 0 var(--c-ink);

  /* spacing: base unit 8px */
  --s-0:4px; --s-1:8px; --s-2:16px; --s-3:24px; --s-4:32px; --s-5:40px; --s-6:48px; --s-8:64px; --s-10:80px; --s-12:96px; --s-16:128px;
  --gutter:clamp(20px,2.2vw + 12px,80px);   /* ≈20 mobile · 32 tablet · 64–80 desktop (verify at 390/820/1440) */
  --container:1440px;
  --section-y:clamp(64px,40px + 7vw,140px); /* 66px@375 · 112px@1024 · 140px@1440 */

  /* type */
  --font-display:"Satoshi","Plus Jakarta Sans",system-ui,sans-serif;
  --font-body:"Plus Jakarta Sans",system-ui,sans-serif;
  --fs-hero:clamp(4rem,2.2rem + 9vw,11.5rem);
  --fs-h2:clamp(2.75rem,1.6rem + 4.5vw,5.25rem);
  --fs-h3:clamp(1.25rem,1.1rem + .6vw,1.625rem);
  --fs-lead:clamp(1.125rem,1rem + .5vw,1.375rem);
  --fs-body:1.0625rem;  --fs-meta:.875rem;

  /* motion */
  --ease-out:cubic-bezier(.22,1,.36,1);
  --t-fast:.15s; --t-med:.3s; --t-slow:.7s;

  /* z-index scale */
  --z-deco:0; --z-content:1; --z-header:50; --z-dialog:100;
}
@media (max-width:1023px){ :root{ --container:100%; } }
```

### Breakpoints & grid
| Name | Range | Grid | Gutter | Notes |
|---|---|---|---|---|
| Mobile | ≤ 639px | 4 col | 20–24px | single column flow, section-y ≈ 64–80px |
| Tablet | 640–1023px | 8 col | ≈32px | 2-up cards, collage becomes 2-col grid |
| Desktop | ≥ 1024px | 12 col | 64–80px | max content width 1440px, asymmetric compositions |

### Contrast (computed WCAG 2.x ratios, verified in Phase 0)
| Pair | Ratio | Use |
|---|---|---|
| navy on cream | 16.14 | body text ✅ |
| navy on white | 17.85 | card text ✅ |
| navy on yellow | 11.66 | yellow buttons/stickers ✅ |
| navy on mint | 9.29 | mint surfaces ✅ |
| white on #6366F1 | **4.47** | ❌ fails AA for text < 18.66px bold / 24px |
| navy on #6366F1 | **4.00** | ❌ fails AA for normal text |
| white on #4F46E5 | 6.29 | ✅ proposed fill for primary button |
| #6366F1 on cream | 4.04 | decoration only — never for text |

**Rule:** `#6366F1` is a **decorative/fill colour**. Any indigo surface carrying text uses `--c-primary-strong` (if approved) **or** text ≥ 24px / ≥ 18.66px bold white. Never put small text on bare indigo. Never use indigo as text colour on cream.

---

## 4. Typography

| Role | Family | Weight | Notes |
|---|---|---|---|
| Display / hero / section titles | **Satoshi** → fallback Plus Jakarta Sans | 700–900 | letter-spacing −.035em, line-height .88–1.0 |
| Body | Plus Jakarta Sans | 400–600 | 17px / 1.6 |
| Card headings | Plus Jakarta Sans | 700–800 | |
| Metadata, tags, buttons | Plus Jakarta Sans | 600–700 | |

- **Satoshi cannot be fetched in the Claude sandbox** (not on npm; Fontshare is outside the allowed network list). Plan: `@font-face` for `fonts/Satoshi-*.woff2` declared in CSS; if the files are absent the stack falls back to Plus Jakarta Sans 800 and the site looks correct. The client may drop the files in later without code changes. Decision D6.
- **Plus Jakarta Sans** is self-hosted from the npm package `@fontsource/plus-jakarta-sans` (5.x, available), latin subset, weights 400/500/600/700/800, `font-display:swap`, preload the two most used weights.
- Never load Google Fonts / Fontshare from a `<link>` in the final build (privacy, CSP, offline preview).
- Use `text-wrap:balance` for headings, `text-wrap:pretty` for paragraphs.

---

## 5. Layout & responsive rules

1. Mobile-first CSS. Components must work at 320px without horizontal scroll (**test `document.documentElement.scrollWidth <= innerWidth` at 320/390/768/1024/1440**).
2. Decorations are `position:absolute`, `pointer-events:none`, `aria-hidden="true"`, and must never create overflow (contain with `overflow:clip` on the section or position inside the gutter).
3. Asymmetry: offset images with rotation ±2–5°, staggered card tops (≤ 40px), overlapping stickers. On mobile reduce rotation to ±2° and remove offsets > 16px.
4. Photo frames use `aspect-ratio` + `object-fit:cover` + per-image `object-position` from the manifest. Never stretch; never upscale beyond 1× native pixels for posters/crops.
5. Hero: copy and photo sit **side by side ≥ 900px**; stacked below. Fix the prototype bug by placing both in the same grid row (`grid-row:1`) or using flex.
6. Mobile nav: see §6.0. Sticky header height 76px desktop / 64px mobile; `scroll-padding-top` matches.
7. Collage: CSS grid with `grid-template-areas` per breakpoint (not percentage-absolute positioning), rotation applied with `transform` on items.

---

## 6. Website architecture

Single page, anchored sections, plus modal overlays. Nav order: **About · What µLearn offers · Events · Team · Memories · Join** (Join is a button).

| # | Section (id) | Purpose | Content | Visual composition | Interactions | Assets |
|---|---|---|---|---|---|---|
| 0 | Header (`#top`) | Wayfinding | Logo lockup, 5 links, "Join us" CTA | Cream bar, 2px bottom border, sticky | Smooth anchors, active-section highlight, accessible mobile menu (disclosure button, `aria-expanded`, Esc closes, focus returns) | Logo (decision D7) |
| 1 | Hero (`#hero`) | Identity in 5 seconds | "Learn. Build. Belong." + one-line intro + 2 CTAs | Giant stacked display type left, tilted photo right (rotate 4–5°, hard shadow), asterisk, squiggle, triangle, dotted grid | Staggered entrance | Hero photo (§9) |
| 2 | About (`#about`) | Who we are + relationship to µLearn | 2 short paragraphs + "Our journey" CTA (→ #memories). Must explain: CHN is the µLearn community at CEC, part of the wider µLearn network | Text left in big type; tilted photo right with star; 2 small facts (verified only) | Reveal | About photo |
| 3 | What µLearn offers (`#offers`) | Show the opportunities available *through µLearn* | Six items with official labels: **Community · Mentors · Interest Groups · Roadmaps · Challenges · Opportunities**; one sentence each (rephrase official text); each links to official destination (§8). Heading must say "across the µLearn network" | **Not a uniform 3×2 icon grid.** Staggered "sticker cards" in mixed sizes (e.g. 2 wide + 4 narrow), alternating yellow/mint/white/indigo-strong fills, big numerals 01–06, offset shadows | Hover lift, reveal | none (SVG stickers) |
| 4 | Events & initiatives (`#events`) | What CHN does | 7 events, **not all equal**: 3 **featured** (ODYSSEY, Buildathon, Build with AI) as large asymmetric cards; 4 **more** (Tech Forge, Type Race, Useless Projects 3.0, Web Slingers) as a compact scroll-snap row. Every card opens an **event dialog** (the archive): poster, poster-stated facts, partners, winners (if the poster lists them), extracted photos | Cards 4:3 media + title + one-line fact; featured cards offset | Hover lift; click/Enter opens `<dialog>`; arrow keys step between events | §9 |
| 5 | Team (`#team`) | People | Featured 4 (mirrors approved design) + **"View full team"** opening directory of all 21 grouped by role family | 4 portrait cards with coloured backdrops (yellow/indigo/mint rotation) and role label | Portrait hover tilt; directory is a `<dialog>`/expandable region with search-free grouped grid | Team portraits |
| 6 | Memories (`#memories`) | Proof of community | Editorial polaroid collage (6 frames) + "View gallery" | White band with 2px borders top/bottom, rotated polaroids, sparkles | Click opens lightbox (prev/next, Esc, caption, focus return) | Memories + extracted photos |
| 7 | Join (`#join`) | Convert | Heading "Be a part of µLearn!"; primary CTA create µLearn account; secondary CTA CHN Discord; 3 verified steps (§7.6); social links; email | Split card: white left, navy clipped right panel, squiggle arrow | CTA hover/active | none |
| 8 | Footer | Close | Nav links, social links, contact email, "Part of the µLearn network" link, credit line | Cream, brand tags (Bold · Playful · Community · Tech-Forward are *internal vibe words — do NOT publish them as content*) | — | — |

*Change from the brief's structure:* §3 "What µLearn Offers" is kept but demoted to a network-level explainer and placed **after About, before Events**; "Getting started" steps live inside Join rather than a new section; no stats/counter section (statistics are inconsistent across official pages — §7.5).

---

## 7. Verified content

### 7.1 Organisation-level facts (µLearn)
Sources read on 2026-11-20 unless stated.

| Claim (safe wording) | Status | Source |
|---|---|---|
| µLearn describes itself as a philosophy of education built on mutual learning through micro groups of peers | ✅ | mulearn.org meta description |
| µLearn Foundation is based at Technopark Phase 1, Thiruvananthapuram | ✅ | mulearn.org footer |
| Offerings and exact labels: **Community, Mentors, Interest Groups, Roadmaps, Challenges, Opportunities** | ✅ | mulearn.org "What µLearn offers" |
| Learning uses **Karma points** (gamified) | ✅ | mulearn.org comparison table |
| Interest Groups: you reach **Level 4** to unlock IG tasks, then choose a group; groups are grouped into Coders / Creatives / Makers / Managers | ✅ | mulearn.org/interest-groups |
| "IG" = **Interest Group** | ✅ | same page (resolves ASSET_MAPPING open question) |
| Account creation page exists at app.mulearn.org (email + password, or Google sign-in) | ✅ | app.mulearn.org/register |
| Official org social handles: LinkedIn `gtechmulearn`, Instagram `mulearn.official`, YouTube `mulearn`, Facebook `gtechmulearn` | ✅ | mulearn.org footer |
| Campus Chapter *model*: faculty mentor, campus lead, core team of 5–10 | ✅ model only | mulearn.org/be-a-part/campus |

### 7.2 Campus / CHN facts
| Claim | Status | Source |
|---|---|---|
| CEC was established in 1993 by the Government of Kerala under IHRD; AICTE-approved; KTU-affiliated; college code CHN | ✅ (search snippet of ceconline.edu — re-read the page in Phase 1 before publishing) | ceconline.edu |
| A CHN Discord server named "Mulearn.CHN" exists and the invite is live | ✅ | discord.gg/DfnDfBhGha resolves to discord.com/invite/DfnDfBhGha |
| Existing CHN site describes µLearn CHN as a student community around learning, innovation, technology, events, workshops, hackathons and peer growth | ✅ meta description only — page body is JS-rendered and unread ⚠️ | mulearn-chn.vercel.app |
| "CHN" suffix refers to the college code | ⚠️ inference | — |
| "The **official** tech community of CEC" (prototype hero line) | ❌ unverified — use "The µLearn community of College of Engineering, Chengannur" (D3) | — |

**Not inspectable (tool blocked):** LinkedIn page, Instagram page (robots disallowed). Their URLs are 🟡 client-supplied. Instagram captions, which likely contain event details, were never read.

### 7.3 Copy rules
1. Every sentence must be traceable to §7 or be generic non-factual voice ("We learn, build and grow together").
2. No numbers about members, events held, participants, prizes won, years active. **Exception:** facts printed on a poster, attributed to that event (e.g. "32 hours").
3. Rephrase official text; do not copy marketing paragraphs.
4. Do not call CHN "official" unless the client confirms.
5. Visible text uses "µ" (**standardise on U+00B5**, as in the client's own materials; mulearn.org mixes µ and μ U+03BC). Use `Mulearn` in URLs and file names.

### 7.4 Event register (poster-stated facts, 🟡 unless noted)
All facts below were read from supplied poster screenshots; none are confirmed by an official CHN source I could access. **Years that are not printed on a poster are not assumed.**

| Event (display name) | Poster-stated facts | Branding on posters | Status / open |
|---|---|---|---|
| **ODYSSEY** — spelling ✅ "ODYSSEY" on all 17 posters; the folder `Odessey` is a typo | 32 hours · 20–21 September 2026 · College of Engineering Chengannur · prize pool ₹15,000 · registration fee ₹150 ⚠️(small text) · ticketing MakeMyPass · food partner Malabar Fresh · Google for Developers (technology partner) · winners: 1st SPARX, 1st runner-up Cypher, 2nd runner-up Jijñāsus · mentors thanked: Jerry Sanju Joanes, Abhijith J Nair, Joe Abraham K | IEDC, µLearn CHN, Google for Developers | Third-party listing (Internshala) agrees: organised by IEDC BOOTCAMP CEC × µLearn CHN, 32 h, 20–21 Sept 2026, team size 2–4. A different listing (Luma) says "24-hour national-level" → conflicting; follow the poster. Past event. |
| **Buildathon** | "µFIFA × Gemma 4" · 17–18 July, 5 PM–9 AM · College of Engineering Chengannur · prize pool ₹7K* · partners: Mandi Mahal, BITA (title sponsor), The Chocolate Drop, V Fit Fitness Hub, Juice It Up, Spinners, The Cowboy ("Penalty Pursuit") · podium: 1st Frustrated Devs, 2nd Tek Knights, 3rd Holo | µLearn CHN, Google for Developers | **Year not on the posters** ⚠️; likely 2026 but unconfirmed. |
| **Build with AI** | Session "Build a Gemini-Powered YouTube Summarizer" 31 March 2026, 4.00–5.30 pm, MCA CC2 · 16-hr AI Hackathon 6–7 April 2026, 5.00 pm–9.00 am, Maker's Space & SDPK · speakers Vishnu Harikumar, Swathy J · thanks Abhijith J Nair & Jithu Girish ("Intro to Vibe Coding") · associate partner PRODDEC · project awards: Creative = Amingos, Innovative = Bizzare, Winners = Phoenix | µLearn, Google for Developers, MakeMyPass, Notion, PRODDEC | Later posts show a subtitle "Alappuzha" while earlier ones show "College of Engineering, Chengannur" ⚠️ clarify. |
| **Tech Forge** | Only fact: an animated title card reading "TECHFORGE 2.0" (video) | none visible | ⚠️ No dates, venue, format, winners. Must be supplied by client or described generically ("Tech Forge — second edition"? ❌ *do not infer*; show title only). |
| **Type Race** | CC2 · 26/03/2026 · 12:15–1:00 PM · prize pool ₹1500 · registration fee ₹20 · free entry for µLearners with 7K+ Karma points and IEEE CS members (5 seats) · winners Christo Chery George, Nevin Mathew, Niranjan V Chandran | IEEE SB CEC, IEEE Computer Society, µLearn CHN, IEEE | — |
| **Useless Projects 3.0** | "3rd edition" · September 11–12 (year not printed) ⚠️ · explainer text: creative, deliberately non-useful projects · no winners named on the image | TinkerHub CE Chengannur, µLearn CHN | Year unknown. |
| **Web Slingers** | Podium: 1st Marvel Jesus, 2nd Titans, 3rd Cosmopolitans · details poster has date/venue/time (≈ "27th October" — **not reliably read**) | µLearn CHN | ⚠️ Re-read the poster in Phase 1 at full zoom; if illegible ask the client. |

**Presentation rule:** show an event's display name, a one-line poster-verified descriptor, and its partner/collaborator line "in collaboration with …" **only as printed**. Do not label events as workshop/hackathon/competition unless the poster says so (Odyssey = "32-hour" event; Type Race = prize-pool competition per poster; Build with AI includes a "16-hr AI Hackathon"). Past/present tense only. No "upcoming".

### 7.5 Statistics policy
Official figures conflict: **60,000+** learners (mulearn.org home), **64,000+** (campus page), **46,786 learners in 23 groups** (interest-groups page), CHN Discord shows **320** members at fetch time. → **Publish no numbers** unless the client supplies a dated, sourced figure; a figure, if added, must be labelled with source and "as of".

### 7.6 "Getting started" (inside Join) — all steps verified
1. **Create your µLearn account** → app.mulearn.org/register ✅
2. **Join the CHN Discord** → discord.gg/DfnDfBhGha ✅
3. **Explore Interest Groups** — unlocked at Level 4 → mulearn.org/interest-groups ✅

### 7.7 Team register (from filenames — roles ⚠️, face↔name unverifiable)
Source folder `mulearn/Team/`. Full table with dimensions and notes: `ASSET_MAPPING.md` §2.

| # | Name | Role (filename) | File |
|---|---|---|---|
| 1 | Geetha S | Lead Enabler ⚠️ | `1_geetha_s__Lead_Enabler.jpg` |
| 2 | Nithin Jayakumar | Campus Lead | `2_Nithin_Jayakumar__Campus_Lead.jpg` |
| 3 | Divyalakshmi | Campus Co-Lead ⚠️ | `3_Divyalakshmi__Campus_Co-Lead.jpg` |
| 4 | Govind J S | Creative Lead | `4_govind_j_s__Creative_Lead.webp` |
| 5 | Hanin C K | Operational Lead ⚠️ ("Operations Lead" in the prototype) | `5_Hanin_C_K__Operational_Lead.jpg` |
| 6 | Amanul Farhan | Technical Lead | `6_Amanul_Farhan__Technical_Lead.jpg` |
| 7 | Pavithra A | Media Lead | `7_Pavithra_A__Media_Lead.jpg` |
| 8 | Albin Thomas | Content Lead | `8_Albin_Thomas__Content_Lead.jpg` |
| 9 | Melwin Shibu Mathew | Operational Team | `9_Melwin_Shibu_Mathew__Operational_Team.jpg` |
| 10 | Sara Shaji | Operational Team | `10_Sara_Shaji__Operational_Team.jpg` |
| 11 | Afsal S | Designer | `11_Afsal_S__Designer.png` |
| 12 | Vismaya Gawri Krishnan | Designer | `12_Vismaya_Gawri_Krishnan__Designer.jpg` |
| 13 | Karthika S | Content Team | `13_Karthika_S__Content_Team.jpg` |
| 14 | Sreelakshmi M | Content Team | `14_Sreelakshmi_M__Content_Team.jpg` |
| 15 | Parvathy Vinayan | Media Team | `15_Parvathy_Vinayan__Media_Team.jpg` |
| 16 | Brijith K Reji | Media Team | `16_Brijith_K_Reji__Media_Team.jpg` |
| 17 | Adhi Narayan | IG Lead – AI | `17_Adhi_Narayan__IG_Lead-AI.jpg` |
| 18 | Al Ameen | IG Lead – UI/UX | `18_Al_Ameen__IG_Lead-UI_UX.jpg` (EXIF rotate 90°) |
| 19 | Amal S | IG Lead – Cyber Security | `19_Amal_S__IG_Lead-Cyber_Security.jpg` |
| 20 | Abhiram J | IG Lead – Web | `20_Abhiram_J__IG_Lead-Web.jpg` |
| 21 | Swathy J | IG Lead – Entrepreneurship ⚠️ | `21_Swathy_J__IG_Lead-Entrepreneurship.jpg` |

**Terminology findings.** "IG Lead" = Interest Group Lead ✅ (official IG page). AI, Web, UI/UX, Cyber Security exist as official groups ✅; **"Entrepreneurship" is not among the 23 groups listed on mulearn.org on 2026-11-20** ⚠️. "Lead Enabler" does not appear on any µLearn page I read; the official chapter model has a **Faculty Mentor** and a **Campus Lead** — whether "Lead Enabler" is the faculty role, a CHN-specific title or something else is **unknown**; do not display it as "Faculty" and do not assume affiliation. "Operational" vs "Operations", "Co-Lead" spelling: ask client.

**Display plan.** Featured four on the page (default, matching the approved design): Campus Lead (#2), Technical Lead (#6), Creative Lead (#4), Operational Lead (#5). Directory groups (labels derived from filenames only): *Leadership* (#1, #2, #3) · *Leads* (#4–#8) · *Teams* (#9–#16) · *Interest Group Leads* (#17–#21). Group label "Leadership" is a presentation choice, ⚠️ confirm.

Poster-named people (speakers, mentors, winners) are **not** team members unless the client says so. "Swathy J" appears both as a Build with AI speaker and as team file #21 — plausible match, ❓ unconfirmed; never merge identities from faces.

---

## 8. External destinations

| Label | URL | Use | Status |
|---|---|---|---|
| Create µLearn account | `https://app.mulearn.org/register` (given as http; use https) | Primary CTA (header + Join section) | ✅ live, resolves |
| CHN Discord | `https://discord.gg/DfnDfBhGha` | Secondary CTA, footer | ✅ live ("Mulearn.CHN") |
| µLearn CHN LinkedIn | `https://www.linkedin.com/company/gtech-mulearn-cec/` | Social, footer | 🟡 not inspectable |
| µLearn CHN Instagram | `https://www.instagram.com/mulearn.chn/` | Social, footer | 🟡 not inspectable |
| Email | `mailto:gtechmulearncec@gmail.com` | Footer, Join | 🟡 client-supplied |
| µLearn official site | `https://mulearn.org/` | "Part of µLearn" link, footer | ✅ |
| Offers → Community | `https://app.mulearn.org/` | Offer card link | ✅ (as linked by mulearn.org) |
| Offers → Mentors | `https://app.mulearn.org/dashboard/search/mentors` | Offer card link | ✅ link seen on mulearn.org; target page not opened |
| Offers → Interest Groups | `https://mulearn.org/interest-groups` | Offer card + Join step 3 | ✅ |
| Offers → Roadmaps & Challenges | `https://app.mulearn.org/dashboard/mujourney` | Offer cards | ✅ link seen; target not opened |
| Offers → Opportunities | `https://mulearn.org/careers` | Offer card | ✅ link seen; target not opened |

All external links: `target="_blank" rel="noopener noreferrer"`, visible "opens in new tab" affordance (icon + visually hidden text). Social links need accessible names ("µLearn CHN on Instagram").
Phase 9 must run a link check; mark any non-200 and report.

---

## 9. Assets

### 9.1 Facts (see `ASSET_MAPPING.md` for the per-file inventory)
- Archive: 85 files — logo 1, team 21, memories 7 (6 photos + 1 poster graphic), event PNGs 50, event MP4 6. Tech Forge has **no still**.
- Event PNGs are **Instagram screenshots** (all captured 2026-11-19 21:35–21:42): posters, sponsor cards, winners cards, "glimpses" collages. Genuine photos exist inside them at roughly 300–600 px wide (never measured precisely — measure in Phase 1).
- Videos are small (≈ 480–508 px wide), 6 files, 2.3–7.7 MB.

### 9.2 Strategy (non-negotiable rules)
1. Originals live in `_sources/` (git-ignored, **never** edited, never in deploy). Derivatives go to `img/`.
2. **Never fabricate or generate photographs or people.** No upscaling above 1× native; if a crop is too small for its slot, switch slot or use the poster as a poster.
3. **Posters are displayed as posters** (full artwork, no crop that cuts text) in event dialogs and as event-card media **only** if a 4:3 crop would not destroy meaning; otherwise cards use a letterboxed poster inside a coloured frame (the colour frame comes from the design, the poster stays whole).
4. **Embedded photos** (podium teams, group shots, glimpses collages) may be cropped out as separate derivatives when ≥ 480 px wide and clean of text/overlays; label them with the event name in captions; record the crop rectangle in the manifest.
5. **Instagram chrome** (carousel arrows, profile glyph, borders) must be cropped out or the image rejected. Known: Buildathon `…213523`, Odessey `…213205` `…213254`, Useless `…213414` `…213837` `…213851`, Buildathon `…213607`.
6. **Video:** extract poster frames (ffmpeg, available in sandbox) for thumbnails; do **not** embed playback in v1 (permission + weight). Frames ≥ 480px wide are usable only at ≤ 480 CSS px or ≤ 0.5× density.
7. **Never use:** `Memories/event5_zdu88j.jpg` as a memory (it is a poster graphic); the low-res duplicates `Odessey/…212307.png` and `…212314.png`; sponsor-only posters as imagery (logos may appear only in an event dialog's partner list and only if permitted); B&W Type Race winner portraits as standalone images.
8. EXIF: apply orientation, then **strip all metadata** (GPS) from every derivative. `Team/18_Al_Ameen…` is stored landscape with EXIF rotate-90.

### 9.3 Derivative specs
| Slot | CSS size (max) | Export widths | Format | Budget |
|---|---|---|---|---|
| Hero photo | ≈ 600 px | 600/900/1200 | WebP q78 (+JPG fallback for OG) | ≤ 180 KB @1200 |
| About photo | ≈ 410×470 | 410/820 | WebP | ≤ 120 KB @820 |
| Event card (4:3) | ≈ 405×304 | 405/810 | WebP | ≤ 90 KB |
| Event dialog poster | ≤ 560 px wide | native (≤ 700) — **no upscale** | WebP q85 | ≤ 140 KB |
| Team portrait (3:3.6) | ≈ 300×360 | 300/600 face-centred | WebP | ≤ 70 KB @600 |
| Collage frame | ≤ 460 px wide | 460/920 (main 1200) | WebP | ≤ 110 KB (main ≤ 160 KB) |
| Lightbox | ≤ 1600 px long edge | 1200/1600 | WebP | ≤ 250 KB |
| OG image | 1200×630 | — | JPG q85 | ≤ 200 KB |

Every `<img>`: `width`/`height` attributes, `alt`, `decoding="async"`, `loading="lazy"` except the LCP hero image (`fetchpriority="high"`). Use `srcset`/`sizes`.

### 9.4 Placement defaults (replace after Phase 1 crop tests)
| Slot | Default asset | Notes |
|---|---|---|
| Hero | `Memories/IMG_7789_qyh10e.jpg` | square-ish crop anchored left-centre; alternative `IMG_5086` (community group, crowd small). Reference shows a packed audience — none exists. |
| About | `Memories/IMG_9798_mvknx7.jpg` | portrait, "Intro to Figma"; crop centre-top |
| Collage main | `IMG_5086_tm6kwh.jpg` | 6000×4000 |
| Collage medium | `IMG_9803_ixchge.jpg`, `IMG_7834_xrr7b7.jpg` | |
| Collage small | `IMG_7844_lclzmf.jpg`; two more = new crops of `IMG_5086` / `IMG_7789` or poster-embedded photos (decision D1) | six genuine photos for eight slots |
| Event cards | Build with AI `…213938`; ODYSSEY `…213134`/`…213144`; Buildathon `…213523`; Type Race `…213923`; Useless `…213404`; Web Slingers `…213322`; Tech Forge = frame from `Tech forge/Recording …212924.mp4` | all portrait posters → cards use whole-poster-in-frame (rule 3) |
| Team featured | #2, #6, #4, #5 | |

### 9.5 Manifest (`docs/ASSET_MANIFEST.json`) — required schema
```json
{ "id":"team-02-nithin","source":{"path":"mulearn/Team/2_Nithin_Jayakumar__Campus_Lead.jpg","sha256":"…","width":1000,"height":1500,"bytes":0},
  "crop":{"x":0,"y":0,"w":1000,"h":1200},
  "derivatives":[{"path":"img/team/nithin-300.webp","width":300,"height":360,"bytes":0}],
  "usage":["team.featured","team.directory"],"alt":"…","objectPosition":"50% 25%",
  "permission":"unverified|confirmed|needs-consent","notes":"" }
```

### 9.6 Permission flags (must be cleared by the client before public launch)
Student/member faces (team portraits, lab photos, group photos) · named winners' portraits embedded in posters · partner/sponsor/third-party logos (Google for Developers, IEEE, IEEE Computer Society, TinkerHub, Notion, MakeMyPass, BITA, etc.) · posters as artwork (µLearn CHN designers) · Instagram content reuse. Default posture: use team portraits and community photos (client collected them), **omit third-party logos as standalone elements**, show partner *names* as text.

---

## 10. Technical architecture

### 10.1 Decision: **no-build static site** (HTML + CSS + vanilla JS, classic scripts), GSAP vendored
Why (against React/Vite): content site with ~9 sections; no routing/state; Claude Web sessions can't run a persistent dev server or deploy, but **can** zip and run headless Chromium (verified: Playwright launches in the sandbox) — a no-build site is previewable by opening files, deployable to Vercel as-is, and the next session can edit any file without a toolchain. Classic `<script defer>` instead of ES modules so the site works from `file://` and can be inlined into one HTML file for Artifact preview. Revisit only if a genuine need appears (e.g. >20 pages).

### 10.2 Folder structure
```
mulearn-chn/
  index.html
  css/ tokens.css · base.css · layout.css · components.css · sections/{header,hero,about,offers,events,team,memories,join,footer}.css · utilities.css
  js/  main.js · nav.js · dialog.js · lightbox.js · events.js · team.js · memories.js · motion.js · util.js
  data/ links.js · events.js · team.js · memories.js          (window.MULEARN.* — single source of truth for repeated content)
  img/  hero/ about/ events/ team/ memories/ brand/ og/        (derivatives only)
  fonts/ PlusJakartaSans-*.woff2 · Satoshi-*.woff2 (client-supplied, optional)
  vendor/gsap/ gsap.min.js · ScrollTrigger.min.js · LICENSE
  scripts/ build_assets.py · extract_embedded.py · extract_frames.py · inline_preview.py · verify_project.py · link_check.py · screenshot.py
  docs/ PROJECT_MASTER_SPEC.md · PROJECT_STATE.md · CHANGELOG.md · NEXT_PHASE.md · ASSET_MAPPING.md · ASSET_MANIFEST.json
  reference/ ulearn_prototype_v1_UNMODIFIED.html (+ reference image if supplied)
  dist-preview/ preview.html  (single-file, for Artifact publish; generated)
  vercel.json · README.md · .gitignore   (ignores _sources/)
```
`_sources/` (originals, 88 MB) is **not** in the handoff ZIP; a phase that needs originals asks the client to re-upload `mulearn.zip`.

### 10.3 Dependencies (pin exact versions; none needing a build)
- **GSAP + ScrollTrigger**: npm `gsap` (3.15.1 was current on 2026-11-20 — choose a release ≥ 14 days old at install time), copy `dist/gsap.min.js` and `dist/ScrollTrigger.min.js` into `vendor/gsap/`. No CDN at runtime.
- **Plus Jakarta Sans**: npm `@fontsource/plus-jakarta-sans` 5.x → copy latin `woff2` files into `fonts/`.
- **Icons**: inline SVG sprite embedded once in `index.html` (hand-copied Lucide-style paths: arrow-right, arrow-up-right, x, menu, chevron-left/right, mail, external-link; custom simple linkedin/instagram/discord glyphs). No icon library.
- **Python** (available in sandbox): Pillow, ffmpeg for assets; Playwright (Chromium) for screenshots/QA.
- ❌ No Tailwind, no React/Vue, no jQuery, no animation libraries other than GSAP, no CSS frameworks.

### 10.4 Conventions
**HTML:** semantic landmarks (`header`, `nav`, `main`, `section[aria-labelledby]`, `footer`), one `h1`, headings in order, skip link first in `body`. JS hooks via `data-js="…"`, never styling classes.
**CSS:** BEM (`.card`, `.card__title`, `.card--yellow`), tokens only (no hard-coded colours/spacings outside `tokens.css`), logical properties where easy, mobile-first `min-width` queries, no `!important` except in the reduced-motion block, one section file per section, components shared in `components.css`. Class prefix none (small project).
**JS:** vanilla ES2020 in IIFEs attached to `window.MULEARN`; no globals other than `MULEARN`; every feature guarded (`if(!el) return`); no `localStorage`/cookies; no external requests; all behaviour progressive enhancement (the page is readable and navigable with JS disabled except dialogs/lightbox/animation).
**Data-driven repeated content:** `data/events.js`, `data/team.js`, `data/memories.js` define items; `js/*.js` render cards/dialog content from them into containers that already contain a `<noscript>` fallback list of names. Editing a role or event fact = editing one data entry.
**Components** (build in Phase 2): `btn` (primary/accent/neutral, sm), `tag`, `card`, `photo-frame`, `polaroid`, `sticker` (SVG decoration), `section-head`, `event-card`, `team-card`, `offer-card`, `dialog`, `lightbox`, `nav`, `social-link`.
**Buttons:** Primary = `--c-primary-strong` (or indigo with ≥ 18.66px bold white) + white text + navy outline + `--shadow-5`; Accent = yellow + navy text; Neutral = cream/white + navy text. Hover: translate(−2px,−2px) + `--shadow-7`; Active: translate(4px,4px) + 1px shadow; **Focus-visible: 3px solid `--c-primary-strong`, offset 3px, plus 2px cream gap; on navy surfaces use yellow ring.** Minimum target 44×44px.

### 10.5 Deployment
Vercel static project from repo root, no build command, output `.`, `vercel.json` with `cleanUrls`, long-cache immutable headers for `/img`, `/fonts`, `/vendor`, `no-cache` for `/index.html`, security headers (`X-Content-Type-Options`, `Referrer-Policy`, a CSP allowing `self`, inline styles only if unavoidable, `frame-src` none, `img-src 'self' data:`). Claude cannot deploy; the client deploys the final ZIP (instructions in README, Phase 10). Existing site `mulearn-chn.vercel.app` is a separate project: **do not overwrite**; ask which URL to use (D14).

### 10.6 Preview & QA tooling inside Claude Web
`scripts/inline_preview.py` inlines CSS/JS/fonts/images as data URIs into `dist-preview/preview.html` (target ≤ 12 MB, hard limit 16 MB) → publish via the Artifact tool for client review. `scripts/screenshot.py` uses Playwright Chromium at 320/390/768/1024/1440 + prints overflow metrics. Sandbox limitation: outbound network is restricted, so external fonts/CDNs never load — another reason everything is vendored.

---

## 11. Accessibility requirements (WCAG 2.2 AA target)
1. Semantic structure, landmarks, one `h1`, no skipped heading levels, skip-to-content link.
2. Contrast per §3 table; test every text/background pair incl. text over images (put text on solid blocks, never directly on photos).
3. Keyboard: all interactions reachable and operable; visible focus (§10.4); logical tab order; no keyboard traps; Esc closes menu/dialog/lightbox and returns focus to the trigger.
4. Mobile nav: `<button aria-expanded aria-controls>`; panel not `display:none`-hidden from AT incorrectly; links ≥ 44px.
5. Dialogs: native `<dialog>` + `showModal()`, `aria-labelledby`, focus first heading/close button, restore focus; `body` scroll lock via CSS `:has(dialog[open])`.
6. Images: informative `alt` (describe what is visible; for posters, include the key printed facts; for people use "Portrait of {Name}, {Role}" only once names are confirmed); decorative SVG `aria-hidden="true"`; no identity claims for unnamed people.
7. Motion: respects `prefers-reduced-motion` (§12); no auto-playing media; no flashing.
8. Links: distinguish new-tab links; descriptive names; icons never the only label.
9. Language: `<html lang="en">`; "µ" announced acceptably — add `aria-label="MuLearn"` where the logo wordmark is the only text.
10. Target size ≥ 24px (AA), 44px for primary controls; text resizable to 200% without loss; reflow at 320px.
11. Test: automated axe-core (loaded in sandbox via npm for tests only) + manual keyboard walkthrough + screenshot review.

---

## 12. Animation rules (GSAP 3 + ScrollTrigger + CSS/SVG)
- Animate only `transform` and `opacity` (plus SVG `stroke-dashoffset`). Durations 0.5–0.9s; ease `power3.out`/`--ease-out`; stagger 0.08–0.14s.
- **Initial hidden states must be applied only by JS** after confirming GSAP loaded and motion is allowed (`html.js-motion`); with JS or GSAP failure everything stays visible. (The prototype's `gsap.from` pattern risks flashing/hiding; do not replicate without the guard.)
- Hero: staggered line reveal (3 headline lines → intro → CTAs → photo), squiggle draw, decorations float ≤ 6px, once.
- Sections: one reveal per block with `ScrollTrigger({start:"top 85%", once:true})`. No scrub, no pinning, no horizontal-scroll hijack, no smooth-scroll libraries, no parallax > 24px.
- Cards: CSS hover/active transitions (0.15s). Team portraits: scale/rotate ≤ 1.5° on hover/focus. Collage: staggered pop-in from `scale .9 + rotate±6°` once; hover straightens (CSS).
- Use `gsap.matchMedia()`: `(prefers-reduced-motion: no-preference)` → full animation; `reduce` → **no transforms, no stagger; at most a 150ms opacity fade or nothing**; CSS transitions also disabled via the reduced-motion media query.
- Kill/refresh: call `ScrollTrigger.refresh()` after images/fonts load; never leave inline `visibility:hidden`.
- Budget: JS parse + execution must keep main-thread work < 50ms at idle after load; GSAP files ≈ 110 KB minified total.

---

## 13. Implementation restrictions (hard rules)
1. Do not invent dates, statistics, achievements, designations, claims, registration steps or contact details. Mark uncertainty in `data/*.js` with `verified:false` and in `PROJECT_STATE.md`.
2. Do not redesign the approved visual identity; no new colours (only §3 tokens), no gradients, no glass, no blur shadows.
3. Do not modify or delete originals; never overwrite `reference/*`.
4. Do not upscale images; do not use unverified-permission third-party logos as standalone elements.
5. Do not add a backend, tracking, analytics, cookies, localStorage, external fonts/CDNs, or form submissions.
6. Do not switch framework. Do not add dependencies without recording why in `PROJECT_STATE.md`.
7. No `<form>`; no `eval`; no inline event handlers; no `!important` outside the reduced-motion block.
8. Never leave the project in a non-working state at the end of a phase.
9. Never rely on conversation history: read the ZIP + `docs/*` first.
10. Never present Instagram screenshots as candid photographs; label posters as posters.
11. Do not claim anything is "official" about CHN without confirmation.
12. Keep the "vibe" words (Bold, Playful, Community, Tech-Forward) and design-system notes out of public copy.

---

## 14. Roadmap & completion criteria (details: Phase-0 report §6)
| Phase | Name | Done when |
|---|---|---|
| 1 | Asset pipeline & content data | All derivatives + `ASSET_MANIFEST.json` + `data/*.js` skeletons; review contact sheet; no upscales; budgets met |
| 2 | Scaffold & design foundation | Folder structure, tokens, fonts, vendor, components, `styleguide.html`, scripts; axe clean |
| 3 | Header/nav + Hero + About | Section QA at 5 widths, mobile menu works, no overflow |
| 4 | Offers + Join + Footer | All CTAs functional, link table implemented |
| 5 | Events + event dialogs | 7 events, dialog a11y, poster rules obeyed |
| 6 | Team + directory | Featured 4 + 21 directory, roles per decisions |
| 7 | Memories + lightbox | Responsive collage, lightbox a11y |
| 8 | Motion layer | Reduced-motion verified, no content hidden on failure |
| 9 | QA, a11y, performance, SEO | Lighthouse-style targets met, links checked, report |
| 10 | Release & handoff | Final ZIP, README, Vercel config, client checklist |

**Definition of done for every phase:** site opens from `index.html`; `scripts/verify_project.py` passes; screenshots at 320/390/768/1024/1440 reviewed with no horizontal overflow; axe has no serious/critical issues; the five handoff docs updated; ZIP verified with `unzip -t`; `NEXT_PHASE.md` written.

---

## 15. Open decisions (defaults apply if the client does not answer — record the actual answer in `PROJECT_STATE.md`)
| ID | Question | Default |
|---|---|---|
| D1 | Event imagery: posters as-is, crops of embedded photos, or client supplies originals? | whole posters in frames + embedded crops only when ≥ 480 px |
| D2 | Team roles: confirm "Lead Enabler", "Campus Co-Lead", "Operational vs Operations", "IG Lead – Entrepreneurship", group labels | show filename roles verbatim except normalising punctuation; hide nothing |
| D3 | Hero line wording ("official"?) | "The µLearn community of College of Engineering, Chengannur." |
| D4 | Confirm LinkedIn, Instagram, email; supply Instagram captions/event details | use client URLs; add no facts |
| D5 | Accept darker indigo `#4F46E5` for text-bearing indigo fills? | yes, as `--c-primary-strong` |
| D6 | Supply Satoshi `.woff2` files (Fontshare, free licence) | fallback to Plus Jakarta Sans |
| D7 | Logo: transparent/SVG wordmark? Keep asterisk+text lockup from the approved design, or the supplied gradient wordmark (262×112 PNG, opaque white bg)? | typographic lockup in header; real wordmark never upscaled |
| D8 | Permissions: faces, winners, third-party logos | proceed with portraits/photos; omit standalone third-party logos |
| D9 | Missing event facts: years (Buildathon, Useless Projects), Web Slingers details, Tech Forge details, Alappuzha subtitle | omit what is unknown |
| D10 | Seven events: featured 3 + 4 more (default) or another split | as stated |
| D11 | Show any member/Discord statistic? | no |
| D12 | Credit/disclaimer line (e.g. "Student-built; not an official µLearn Foundation site")? | none until confirmed |
| D13 | Include any video playback? | no (poster frames only) |
| D14 | Deployment URL / Vercel owner; replace the existing CHN site? | do not overwrite existing |
| D15 | Provide the original reference image/Figma again if a session needs pixel-level checks (Figma was never accessible to me) | prototype + this spec |

*End of PROJECT_MASTER_SPEC.md*
