# µLearn CHN — Phase 0 Report (Master Planning & Project Audit)

2026-11-20 · Read together with `PROJECT_MASTER_SPEC.md` (section 9 of the requested output; it is delivered as its own file because it is the file future sessions will load). No code was written for the site; the prototype and assets were not modified.

**Inspection limits — stated up front.** I could *not* open: the Figma file (never supplied/accessible), LinkedIn and Instagram (robots-blocked), the body of the existing CHN site `mulearn-chn.vercel.app` (JavaScript-rendered; only its meta description was readable), Instagram captions, `odysseycec.in`. No "existing project ZIP" was supplied. I *did* read: mulearn.org (home, campus-chapter, interest-groups), app.mulearn.org/register, the CHN Discord invite page, search results for CEC and ODYSSEY, the asset archive (every image and a 6-second frame sample of every video), `ulearn.html` (source and headless-Chromium renders at 390/820/1440 px).

---

## 1. Project audit

### 1.1 Supplied files
| Item | State |
|---|---|
| Reference image (board by the client) | seen in conversation; primary visual target; **not a file in the ZIP** — re-supply if pixel checks are needed |
| `ulearn.html` prototype (16.5 KB, 1 file) | in `reference/`, unmodified (SHA-256 recorded in `PROJECT_STATE.md`) |
| `mulearn.zip` | 85 files / 11 folders / 88 MB: logo 1, Team 21, Memories 7, Event PNG 50, Event MP4 6 — full inventory in `docs/ASSET_MAPPING.md` |
| `ASSET_MAPPING.md` | accurate for filenames/dimensions (generated from the file tree); event content descriptions are from my visual review |
| Existing project ZIP | none |
| Figma | not accessible |

### 1.2 Current implementation technology
Hand-written single-file **vanilla HTML + CSS + JS**; GSAP 3.12.5 + ScrollTrigger from cdnjs; Plus Jakarta Sans from Google Fonts; no build step, no framework, no assets folder (every photo is a `div.photo.ph` with `--img:url('assets/…')` over a striped fallback).

### 1.3 Prototype components (what exists)
Sticky header (logo = inline SVG asterisk + text, 4 links, indigo "Join Us") · Hero (3-line display headline, intro, 2 buttons, tilted photo, asterisk, squiggle, triangle, dot-grid) · About (tilted photo + star) · Events (3 cards) · Team (4 cards) · Memories (6 absolutely-positioned polaroids) · Join (white + clipped navy split card) · footer (tags + tagline) · token set, button styles, hard-shadow cards, reduced-motion CSS, GSAP reveals.

### 1.4 Measured defects (headless Chromium, fonts/CDN blocked in sandbox so type metrics are fallback-font)
| # | Finding | Evidence | Severity |
|---|---|---|---|
| P1 | **Hero photo renders below the headline, not beside it** — `.hero-copy` (cols 1–8) and `.hero-photo` (cols 7–13) overlap, so grid auto-placement pushes the photo to a second row. The approved reference has them side by side. | screenshot @1440 | High (fidelity) |
| P2 | **No mobile navigation**: `.links{display:none}` ≤ 760 px and no menu button exists. | source + render | High |
| P3 | **Horizontal overflow on mobile**: `scrollWidth 400 > clientWidth 390` (decorative blob/SVGs); a blob also pokes out at 820 px. `body{overflow-x:hidden}` hides it on desktop but not reliably on iOS. | measured | Medium |
| P4 | White text on `#6366F1` = 4.47:1 (AA needs 4.5) on the primary button and "Join Us". | computed | Medium |
| P5 | `.photo{filter:grayscale(1)}` applies to event cards and team portraits; the reference shows colour there. | source vs reference | Medium |
| P6 | All CTAs are in-page anchors (Join Now → `#top`); no external link exists. | source | High (functionality) |
| P7 | Event subtitles ("Hands-on · Open to all", "Teams of 4 · 24 hours", "Solo · Fastest fingers win") were **placeholder copy I wrote**; unsupported by any source. Hero line says "official" — unverified. | review | High (content) |
| P8 | Collage uses absolute percentage positions with fixed pixel heights → fragile between 700–1100 px. | source | Medium |
| P9 | `gsap.from` hides elements until animated; if GSAP loads late/fails, content can flash or stay hidden. No `.js` guard. | source | Medium |
| P10 | Depends on two external hosts (cdnjs, Google Fonts) at runtime; Satoshi never loaded (fallback in use). | source | Medium |
| P11 | No offers section, no lightbox/dialogs, no team directory, no real footer (socials, contact), no meta/OG tags, no `<noscript>`, alt text describes placeholders ("Stage lights"). | review | High (scope) |
| P12 | The prototype was published without a browser-render check; first real visual QA happened now. | process | — |

### 1.5 Reusable vs rebuild
**Reuse:** token values; border/shadow/radius language; button hover/active mechanics; SVG decoration shapes (asterisk, star, squiggle, triangle); section order and headings; polaroid styling; Join split-card with `clip-path`; reduced-motion block; fluid-type approach.
**Rebuild:** layout engine for hero/collage (grid areas), mobile nav, all content, offers section, dialogs/lightbox, team directory, footer, image pipeline, animation guard, file structure.

### 1.6 Missing functionality
Mobile menu · working CTAs · event archive dialogs · team directory · lightbox · active-section nav state · image `srcset` pipeline · `<noscript>` fallbacks · SEO/OG/favicon · link check · automated overflow/axe/screenshot QA.

### 1.7 Technical risks (carried to §7)
Unreadable/insufficient event imagery (posters, ≈300–600 px embedded photos) · six genuine photographs for eight slots · contrast of indigo · Satoshi unobtainable in sandbox · permission to publish faces/logos · unverifiable roles/dates · multi-session drift · 16 MB Artifact preview limit · all events appear past (no "upcoming").

---

## 2. Content verification
Full register with sources and wording rules is **Spec §7–8**. Summary:

**Verified (read today):**
- µLearn's own description (peer learning in micro groups); µLearn Foundation at Technopark Phase 1, Thiruvananthapuram; offering labels *Community, Mentors, Interest Groups, Roadmaps, Challenges, Opportunities*; Karma-point gamification; Interest Groups unlock at Level 4 and span Coders/Creatives/Makers/Managers; "IG" = Interest Group.
- `app.mulearn.org/register` is a live account-creation page. The CHN Discord invite is live and titled "Mulearn.CHN".
- CEC: established 1993 by Government of Kerala under IHRD, AICTE-approved, KTU-affiliated, college code CHN (search snippet — re-read page in Phase 1).
- ODYSSEY spelling: **ODYSSEY** (poster text on all 17 posters; a third-party listing agrees, naming the organisers as IEDC BOOTCAMP CEC × µLearn CHN, 32 h, 20–21 Sept 2026). A second listing claims "24-hour national-level" — conflicting, not used.

**µLearn vs µLearn CHN:** µLearn = Foundation/platform (accounts, IGs, roadmaps, karma, mentors). µLearn CHN = the CEC campus community (Discord, events, team). Rule: org-level features are described "across the µLearn network"; campus claims come only from posters, the Discord, or the client. The chapter *model* page (faculty mentor, campus lead, weekly circles, flagships) is **not** evidence of what CHN does.

**Event data (poster-stated; 🟡):** register in Spec §7.4. Unknown: year for Buildathon (17–18 July) and Useless Projects 3.0 (September 11–12); Web Slingers date/venue unreadable; Tech Forge has no facts beyond "TECHFORGE 2.0"; Build with AI subtitle switches between "College of Engineering, Chengannur" and "Alappuzha".

**Uncertain designations:** "Lead Enabler" (not a µLearn term I found; official chapter model uses *Faculty Mentor* — do not equate), "Campus Co-Lead", "Operational Lead" vs prototype "Operations Lead", "IG Lead – Entrepreneurship" (not among the 23 official IGs on 2026-11-20). Names/roles come from filenames only; faces cannot be matched to names.

**Inconsistent statistics (so none are published):** 60,000+ (home), 64,000+ (campus page), 46,786 (IG page), CHN Discord 320 at fetch time.

**Missing information:** items D1–D15 in Spec §15.

**External destinations:** table in Spec §8 (account, Discord, LinkedIn, Instagram, email, mulearn.org, five offer destinations). Verified live: register, Discord, mulearn.org pages; **not inspectable:** LinkedIn, Instagram; email is client-supplied.

---

## 3. Asset strategy
Rules in Spec §9. Highlights:

**Section → image choices.** Hero `IMG_7789` · About `IMG_9798` · Collage main `IMG_5086`, mediums `IMG_9803`/`IMG_7834`, small `IMG_7844` + two open slots · Team featured #2/#6/#4/#5 · Event cards use whole posters in frames (all event stills are portrait ≈0.83; 4:3 cover-crops would cut ~35% of the artwork). Details and focal points tuned in Phase 1 with rendered crop tests.

**Quality limits.** Only six genuine photographs; no packed-auditorium photo (reference hero); embedded event photos are small; videos are 480–508 px wide; `Team/1_geetha_s…` is 400×514 (soft above ~200 CSS px); `Team/18_Al_Ameen…` needs EXIF rotation; large originals (up to 6.7 MB) must never ship.

**Useful video frames (sampled every ~6 s; timestamps approximate, confirm in Phase 1).** Buildathon `…213740.mp4`: lab audience (t≈0), girl at microphone (t≈6), night scene with laptops (t≈24). ODYSSEY `…212442.mp4`: B&W cinematic frames, printed 20–21 Sept poster (t≈18); `…212656.mp4`: ODYSSEY banner room (same scene as the still `…212606.png`). Tech Forge `…212924.mp4`: title card "TECHFORGE 2.0" (only visual for that event). Build with AI `…214133.mp4`: students at benches (t≈0), speakers (t≈6–12), group pose at the projector (t≈30). All frames are small → thumbnails ≤ 480 CSS px only.

**Do not use:** `event5_zdu88j.jpg` as a memory; low-res duplicates `Odessey/…212307`, `…212314`; the Buildathon closing card listing sponsor logos; Instagram-chrome-contaminated crops; sponsor-only posters as imagery; B&W winner portraits as standalone images; anything from `Odessey/…212606` as a *hero* (507×332).

**Dimensions, crops, optimisation:** Spec §9.3 (WebP, srcset, budgets, EXIF strip, no upscaling). **Permission flags:** Spec §9.6.

---

## 4. Final website architecture
Defined in Spec §6. Refinements to the proposed structure and why:
1. **Order: Hero → About → What µLearn offers → Events → Team → Memories → Join → Footer** — the brief's sequence, kept; "What µLearn offers" is explicitly framed as *network* content so it cannot be misread as CHN activity.
2. **Offers is not a 3×2 icon grid** (generic SaaS risk): staggered sticker-cards, big numerals, mixed widths and fills.
3. **Events: 3 featured + 4 "more"**, every one opening a dialog (the archive). Avoids an overcrowded seven-card wall and lets Tech Forge (no stills) sit in the compact row without exposing the asset gap.
4. **Team: featured 4 (matches the approved design) + full 21-person directory dialog**, grouped from filename roles.
5. **Memories: responsive grid-area collage + lightbox**, including extracted event photos with event-name captions.
6. **Join carries the "Getting started" steps** (account → Discord → Interest Groups at Level 4) — all verified — instead of a new section. No stats section.
7. Footer carries nav, socials, email and a "part of µLearn" link; the design-system "vibe" tags are *not* shown.

## 5. Technical architecture
Full specification in Spec §10. Decision: **no-build static HTML/CSS/vanilla JS, GSAP vendored.**
- *Maintainability:* one data file per repeated content type; BEM CSS with tokens; no toolchain to break between sessions.
- *Claude Web fit:* sandbox can run Python/Pillow/ffmpeg/Node and **headless Chromium launches (verified)** → real screenshot/overflow/axe QA is possible; the site can be zipped and inlined into one HTML for Artifact preview. A Vite/React project would add install/build steps with no functional gain.
- *Performance:* WebP derivatives, `srcset`, GSAP ≈110 KB, no runtime third-party hosts.
- *Accessibility:* native `<dialog>`, semantic HTML, JS-optional core content.
- *Deployment:* Vercel static from repo root, `vercel.json` headers; Claude cannot deploy — client uploads the final ZIP.
- *Why classic scripts not ES modules:* `file://` compatibility and trivial inlining.
- Not available in sandbox: Satoshi font (not on npm, Fontshare off the allow-list) → fallback + optional client-supplied files. Available: `gsap` (3.15.1 on npm today), `@fontsource/plus-jakarta-sans` 5.3.0.

---

## 6. Implementation roadmap
Every phase: starts by reading the latest ZIP + `docs/*`; ends in a working site + the five handoff documents + verified ZIP. Common testing: `verify_project.py`, screenshots at 320/390/768/1024/1440, overflow check, axe, keyboard pass.

### Phase 1 — Asset pipeline & content data
1. **Objective:** produce every derivative image, the manifest and data files so later phases only place assets.
2. **Scope:** derivatives for hero, about, 4 featured team + 17 directory portraits, collage (incl. 2 open slots), 7 event poster cards + dialog posters, embedded-photo extractions, video poster frames, OG image, logo handling; update `data/*.js` skeletons with `verified` flags.
3. **Files:** `img/**`, `docs/ASSET_MANIFEST.json`, `data/{team,events,memories,links}.js`, `scripts/{build_assets,extract_embedded,extract_frames}.py`, `docs/asset-review.html` (contact sheet).
4. **Dependencies:** client re-uploads `mulearn.zip`; Spec §9.
5. **Requirements:** EXIF rotate+strip; no upscaling; crop rectangles recorded; Instagram chrome removed; poster whole-art rule; sha256 for each source; measure embedded-photo pixel sizes and re-read Web Slingers poster at full zoom; resolve hero/about/collage crops with rendered tests.
6. **Acceptance:** every manifest entry complete; budgets in Spec §9.3 met; every slot in §9.4 has a decision or a documented open item; contact sheet reviewed.
7. **Testing:** script asserts dimensions ≥ declared, no derivative larger than source in pixels, file sizes within budget, no EXIF.
8. **Deliverables:** ZIP, docs, manifest, contact sheet.
9. **Risks:** embedded photos too small; fewer unique photos than slots; missing originals if ZIP not re-uploaded.

### Phase 2 — Scaffold & design foundation
1. **Objective:** project skeleton + design system as code.
2. **Scope:** structure, `tokens.css`, `base.css`, fonts, vendored GSAP, components (btn, tag, card, photo-frame, polaroid, sticker, section-head), SVG decoration library, SVG icon sprite, `styleguide.html`, QA scripts, `vercel.json`, `README.md`.
3. **Files:** whole tree in Spec §10.2 (empty section stubs allowed).
4. **Dependencies:** Phase 1 optional (styleguide uses placeholders); npm access for `gsap`, `@fontsource/plus-jakarta-sans`.
5. **Requirements:** tokens exactly per Spec §3; primary button per decision D5; focus states; reduced-motion CSS; `inline_preview.py`, `screenshot.py`, `verify_project.py`.
6. **Acceptance:** `styleguide.html` shows every component in every state at 3 widths; fonts load locally (Plus Jakarta Sans); no external requests; contrast table reproduced by a script.
7. **Testing:** screenshots, axe on the styleguide, grep for hard-coded colours outside tokens.
8. **Deliverables:** ZIP, docs, preview HTML published for review.
9. **Risks:** Satoshi absent; token drift.

### Phase 3 — Header/nav, Hero, About
1. **Objective:** first screen and mobile navigation, fixing P1–P3.
2. **Scope:** skip link, sticky header, desktop nav, mobile menu, active-section highlight, hero (side-by-side grid ≥ 900 px), About.
3. **Files:** `index.html`, `css/sections/{header,hero,about}.css`, `js/{main,nav}.js`.
4. **Dependencies:** Phases 1–2; decisions D3, D7.
5. **Requirements:** hero line per D3; hero image `fetchpriority="high"`; decorations inside the section's clip; About states CHN ↔ µLearn relationship from §7 only.
6. **Acceptance:** hero photo beside headline at ≥ 900 px; no overflow at 320–1440; menu operable by keyboard/Esc; LCP image < 250 KB.
7. **Testing:** overflow script, axe, keyboard walk, screenshots.
8. **Deliverables:** as standard.
9. **Risks:** hero photo not matching the reference's crowd; type sizing without Satoshi.

### Phase 4 — What µLearn offers, Join, Footer
1. **Objective:** make the page functional end-to-end.
2. **Scope:** six offer cards linked per Spec §8; Join section with verified steps and CTAs; footer with socials/email.
3. **Files:** `css/sections/{offers,join,footer}.css`, `data/links.js`, `index.html`.
4. **Dependencies:** Phase 2; D4, D5.
5. **Requirements:** official labels; rephrased sentences; "across the µLearn network" framing; links `rel` + new-tab hint; social accessible names.
6. **Acceptance:** every external link resolves to its Spec §8 URL; unverified links flagged `data-verified="false"` in data; no stats.
7. **Testing:** `link_check.py` (note sandbox network limits: verify via Python `requests` only if domain allowed, otherwise manual list), axe, focus order.
8. **Deliverables:** standard.
9. **Risks:** offers section reading as generic; LinkedIn/Instagram URLs unverified.

### Phase 5 — Events & event dialogs
1. **Objective:** present the seven events honestly and richly.
2. **Scope:** 3 featured + 4 compact cards; `<dialog>` per event with poster, poster-stated facts, partners, winners, extracted photos; prev/next within dialog.
3. **Files:** `css/sections/events.css`, `js/{events,dialog}.js`, `data/events.js`.
4. **Dependencies:** Phase 1 images; D1, D9, D10.
5. **Requirements:** use only the Spec §7.4 facts; no "upcoming"; Tech Forge shows title + frame + "details coming" **only if** client OKs, else title only; posters shown whole.
6. **Acceptance:** each card opens/closes via mouse, keyboard, Esc; focus returns; alt text includes poster facts; no fact absent from §7.4.
7. **Testing:** keyboard test, axe on open dialog, screenshots incl. open dialog at 390/1440.
8. **Deliverables:** standard.
9. **Risks:** poster legibility in dialogs; weak imagery for Tech Forge.

### Phase 6 — Team & directory
1. **Objective:** featured leadership + accessible full directory.
2. **Scope:** 4 featured cards (default #2/#6/#4/#5), directory dialog for 21 grouped by role family.
3. **Files:** `css/sections/team.css`, `js/team.js`, `data/team.js`.
4. **Dependencies:** Phase 1 portraits; D2.
5. **Requirements:** consistent portrait crop (face-centred, same backdrop rotation yellow/indigo/mint); roles verbatim from Spec §7.7 until D2 answered; EXIF-corrected #18.
6. **Acceptance:** all 21 visible in the directory with correct file; alt text "Portrait of {Name}, {Role}"; no overflow.
7. **Testing:** data-vs-DOM count check, axe, screenshots.
8. **Deliverables:** standard.
9. **Risks:** portrait inconsistency (cut-out, passport, outdoor); low-res #1.

### Phase 7 — Memories & lightbox
1. **Objective:** editorial collage with an accessible gallery.
2. **Scope:** 6-frame grid-area collage; lightbox for all gallery items (photos + extracted event photos, captioned).
3. **Files:** `css/sections/memories.css`, `js/{memories,lightbox}.js`, `data/memories.js`.
4. **Dependencies:** Phase 1; D1.
5. **Requirements:** captions never invent places/dates (only "Community photo" or event name); keyboard arrows, Esc, focus return; swipe optional.
6. **Acceptance:** collage holds at 390/768/1024/1440 without overlap that hides content; lightbox operable by keyboard.
7. **Testing:** axe, keyboard, screenshots.
8. **Deliverables:** standard.
9. **Risks:** too few distinct photos → repetition.

### Phase 8 — Motion layer
1. **Objective:** purposeful animation without risk.
2. **Scope:** hero stagger, section reveals, collage pop-in, squiggle draw, team/event micro-motions, reduced-motion path.
3. **Files:** `js/motion.js`, small CSS additions.
4. **Dependencies:** Phases 3–7.
5. **Requirements:** Spec §12 (JS-applied hidden states, `gsap.matchMedia`, once-only triggers, no pinning/scrub).
6. **Acceptance:** with GSAP blocked, page is fully visible; with `prefers-reduced-motion`, no transforms animate; no layout shift.
7. **Testing:** Playwright with `reduced_motion='reduce'` and with the GSAP script route-blocked; CLS check.
8. **Deliverables:** standard.
9. **Risks:** ScrollTrigger refresh after lazy images.

### Phase 9 — QA, accessibility, performance, SEO
1. **Objective:** make it shippable.
2. **Scope:** full responsive audit (320/390/768/1024/1440/1920), axe + manual keyboard/screen-reader-style review, link check, image weights, meta/OG/Twitter tags, favicon, `robots.txt`, sitemap.
3. **Files:** fixes anywhere; `docs/QA_REPORT.md`.
4. **Dependencies:** all prior phases.
5. **Requirements:** page weight target ≤ 1.5 MB transferred on first load (images lazy); LCP image ≤ 250 KB; zero horizontal overflow; no console errors; every fact traceable to Spec §7.
6. **Acceptance:** QA report with before/after evidence; no serious/critical axe issues.
7. **Testing:** as listed.
8. **Deliverables:** standard + QA report.
9. **Risks:** late discovery of content errors.

### Phase 10 — Release & handoff
1. **Objective:** deliverable for deployment.
2. **Scope:** final ZIP, README (deploy steps), `vercel.json` check, `dist-preview/preview.html`, client checklist (permissions, unverified facts remaining).
3. **Files:** `README.md`, `vercel.json`, docs.
4. **Dependencies:** Phase 9.
5. **Requirements:** remove unused CSS/JS; record unresolved items.
6. **Acceptance:** fresh unzip opens via `index.html`; README steps reproducible.
7. **Testing:** `unzip -t`, verify script, final screenshots.
8. **Deliverables:** final ZIP + docs.
9. **Risks:** client-side deployment issues (Vercel config).

---

## 7. Risks and unresolved decisions
**Unresolved decisions:** D1–D15 in Spec §15, each with a default. Highest impact: **D1** event imagery approach, **D2** team roles ("Lead Enabler"), **D8** permissions, **D9** missing event facts, **D7** logo.

**Risks**
| Risk | Impact | Mitigation |
|---|---|---|
| Event "photos" are Instagram screenshots | weakens "authentic photography" | whole-poster frames, embedded-photo extraction ≥ 480 px, ask for originals |
| Six photos, eight slots | repetition | different crops; ask for more; allow fewer collage frames |
| Unverifiable roles/dates | factual errors on a public site | `verified` flags, defaults in §15, no invention |
| Instagram/LinkedIn unreachable | wrong URLs | client confirmation (D4) |
| Indigo contrast | accessibility failure | D5 / §3 rule |
| Satoshi missing | typographic difference vs reference | fallback tested; optional drop-in |
| Permissions (faces, winners, logos) | legal/reputational | D8, omit third-party logos |
| Session drift across Claude sessions | inconsistency | spec precedence + state log + verify script |
| Artifact 16 MB preview limit | preview fails | WebP budgets, preview-only smaller derivatives |
| All events are past | page looks inactive | frame as "what we've done"; Join CTA primary; optional "next event" only if client provides |
| Possible stale facts (event details change) | misinformation | data files + dated register |

## 8. ZIP handoff protocol
**Required output of every phase** (all inside the ZIP root unless noted): the complete working project; `docs/PROJECT_MASTER_SPEC.md`; `docs/PROJECT_STATE.md`; `docs/CHANGELOG.md`; `docs/NEXT_PHASE.md`; updated `docs/ASSET_MANIFEST.json` when assets change. Name: `mulearn-chn_phase-<NN>_<YYYYMMDD>.zip`. The ZIP contains the **whole** project (never a diff), excludes `_sources/` and `node_modules/`, and is verified with `unzip -t` plus `scripts/verify_project.py` (required files exist, every `img`/`href`/`src` target exists, no `localStorage`, no external hosts except links, no hard-coded colours outside tokens, tokens file hash matches the spec).

**Session start checklist (new session):** (1) read `docs/PROJECT_MASTER_SPEC.md`, `PROJECT_STATE.md`, `NEXT_PHASE.md`, `CHANGELOG.md`; (2) unzip the latest ZIP and run `verify_project.py`; (3) confirm the phase number matches `NEXT_PHASE.md`; (4) list conflicts or unanswered decisions and apply defaults, recording them; (5) do **not** edit before this.

**Session end checklist:** run the tests; update the four docs + manifest; write `NEXT_PHASE.md` with exact scope, files, open decisions, known bugs; bump `PROJECT_STATE.md` (phase status table, decisions log, file hashes of `tokens.css`, verification results, screenshots reviewed); build the ZIP; verify it; `present_files` the ZIP; if out of budget, produce a **`…_WIP`** ZIP and mark the phase "in progress" with a precise resume list.

**Copy-paste prompt for the next session:** *"You are continuing the µLearn CHN website. Upload attached: latest project ZIP (and mulearn.zip only if NEXT_PHASE.md says originals are needed). Do not use any prior conversation. First read docs/PROJECT_MASTER_SPEC.md, PROJECT_STATE.md, NEXT_PHASE.md, CHANGELOG.md in the ZIP, run scripts/verify_project.py, then implement exactly the phase in NEXT_PHASE.md. Follow the spec's restrictions. End with the full ZIP and updated docs."*

Initial `PROJECT_STATE.md`, `CHANGELOG.md`, `NEXT_PHASE.md` (for Phase 1) are included in the bundle.

## 9. Complete PROJECT_MASTER_SPEC.md
See the separate file `docs/PROJECT_MASTER_SPEC.md` in this bundle (it is the authoritative, complete document).
