# PROJECT_STATE.md

**Last updated:** 2026-11-20 · **Current phase:** 5 (Events & Initiatives) — Subphase 5.1 **complete** · **Next:** Subphase 5.2 — Featured event cards  
**Project status:** Phase 3 complete: header/navigation, hero and About assembled in `index.html`, with motion. Audited at 320/390/768/1024/1440 (axe 0 violations, no overflow, 0 console errors, 0 external requests, motion tests 17/17). Offers, Events, Team, Memories, Join and Footer are Phases 4–7.

## Phase status
| Phase | Name | Status |
|---|---|---|
| 0 | Master planning & audit | ✅ complete |
| 1 | Asset pipeline & content data | ✅ complete & reconciled |
| 2 | Design foundation (subphased) | ✅ complete — final ZIP `mulearn-chn_phase-02_complete.zip` |
| 3 | Header/nav + Hero + About | ✅ complete |
| 4 | Offers + Join + Footer | ✅ complete |
| 5 | Events + dialogs | 🔄 in progress (5.1 done) |
| 6 | Team + directory | ⏳ |
| 7 | Memories + lightbox | ⏳ |
| 8 | Motion layer | ⏳ |
| 9 | QA / a11y / perf / SEO | ⏳ |
| 10 | Release & handoff | ⏳ |

## Phase 5 progress (subphase checkpoints)
| Subphase | Name | Status | ZIP |
|---|---|---|---|
| 5.1 | Event data audit & section structure | ✅ complete | `mulearn-chn_phase-05_subphase-01.zip` (+ `mulearn-chn_phase-05_subphase-01_deploy.zip`) |
| 5.2 | Featured event cards | ⏳ | |
| 5.3 | Compact event entries | ⏳ | |
| 5.4 | Accessible event-detail dialogs | ⏳ | |
| 5.5 | Integration, visual QA & completion | ⏳ | |

Phase 5 working rules (client, 2026-11-20): run all five subphases in order **without stopping for approval** (overrides the master prompt's "stop" lines); deliver the versioned full + deployable ZIP after each; never overwrite a checkpoint; look = mix of Board 1 + Board 2.

### 5.1 notes
`data/events.js` rewritten to the reconciled schema (see `docs/events-audit.md`): 3 featured + 4 compact, unknown fields omitted, invented labels/venues removed (Tech Forge venue, Useless venue, "Overnight Hackathon", "Team" prefixes, third-party organiser), disputed Build with AI location omitted, Buildathon `₹7K*` kept. Real `#events` section (`css/sections/events.css`): lavender label "Looking back", h2 "Events & initiatives", lead, honesty note (posters' printed details; no guessed years), "Featured events" / "More events" groups, placeholder numbered cards. Cards are generated into `index.html` by `scripts/build_events.js` (markers `events:featured|compact`), so they exist without JS. `#events` stub removed; `#team #memories` stubs remain; order Offers → Events → stubs → Join. `data/events.js` is loaded (defer) ready for 5.4. New: `scripts/test_phase5.py` (41/41), `scripts/shot_events.py`, `docs/phase5-results.json`, `docs/audit-results-phase5-1.json` (axe 0 ×5). `scripts/test_phase4.py` section-order assertion updated to include `events`. Known: placeholder card styling only; Instagram arrow artefact in ODYSSEY/Buildathon derivatives to fix in 5.2.

## Phase 4 progress (subphase checkpoints)
| Subphase | Name | Status | ZIP |
|---|---|---|---|
| 4.1 | What µLearn offers: content & structure | ✅ complete | `mulearn-chn_phase-04_subphase-01.zip` (+ `mulearn-chn_phase-04_subphase-01_deploy.zip`) |
| 4.2 | What µLearn offers: visual & responsive refinement | ✅ complete | `mulearn-chn_phase-04_subphase-02.zip` (+ `mulearn-chn_phase-04_subphase-02_deploy.zip`) |
| 4.3 | Join section | ✅ complete | `mulearn-chn_phase-04_subphase-03.zip` (+ `mulearn-chn_phase-04_subphase-03_deploy.zip`) |
| 4.4 | Footer | ✅ complete | `mulearn-chn_phase-04_subphase-04.zip` (+ `mulearn-chn_phase-04_subphase-04_deploy.zip`) |
| 4.5 | Integration, visual QA & completion | ✅ complete | `mulearn-chn_phase-04_complete.zip` (+ `mulearn-chn_phase-04_deploy.zip`) |

Phase 4 working rules (client, 2026-11-20): run all five subphases in order **without stopping for approval**; deliver a versioned full ZIP + deployable ZIP after each; never overwrite a checkpoint; look = mix of Board 1 + Board 2.

### 4.1 notes
Offers section added (`#offers`, `css/sections/offers.css`): lavender field with scallop edges top/bottom, Board 2 ink label *"Across the µLearn network"*, h2 "What µLearn offers", lead that says the six items belong to the wider µLearn ecosystem and CHN is the campus doorway (no claim that CHN runs them). Six `<li><article class="card">` cards in a `<ul role=list>`: 01 Community · 02 Mentors · 03 Interest Groups (Level 4 unlock + Coders/Creatives/Makers/Managers tags) · 04 Roadmaps · 05 Challenges (Karma points) · 06 Opportunities. Copy rephrased from Spec §7.1 only; no numbers, no CHN programmes. Each card has one explicit text link bound via `data-link="offers.*"` (`js/main.js` now resolves dotted paths into `data/links.js`; the HTML href is the no-JS fallback). Roadmaps and Challenges share one URL in the spec; both cards link to it and a visible note says so (no URL invented, `links.js` unchanged). "µ" must never be uppercased (renders Greek capital Mu): the label is `text-transform:none`. Initial styling = 7/5 alternating 12-col grid (≥1024), 2-col (≥700), 1-col below; fills indigo/yellow/white/mint/coral/cream. Anchor stub `#offers` removed (real section); `#events #team #memories #join` stubs remain. Visual composition (stagger, stickers, tilt, reveal) arrives in 4.2.

### 4.2 notes
Offers refined to the mixed Board 1 + Board 2 look. Cards: 12-col wide/narrow alternation (7/5, 5/7, 7/5) with desktop vertical stagger and ±0.6–1.2° tilt on the `<li>` wrappers (hover lift is on the inner card, so tilt and lift never fight); numerals 3.5–6rem with a rule above the hook line; one decorative corner sticker per card (asterisk, circle-diamond, bolt, squiggle, star, sparkle) poking out of the top-right corner; hover/focus-within lifts the card to the 9px hard shadow. Section: Board 2 ink blob + yellow sparkle (≥900), faint grid, squiggle (≥1024), mint triangle + indigo quarter (≥640); all decorations are in the clipped, *positioned* `.offers` host (`position:relative` is required — `overflow:clip` alone does not clip absolutely-positioned stickers whose containing block is outside; this caused a false 50px overflow before it was fixed). The 4.1 plain note became a Board 2 `.ink-bar` ("Good to know" badge + shared-destination note + mulearn.org link, cream link colour on navy). Motion: `motion-home.js` Offers reveal (head + stickers once at 70% viewport, each card at 88%, note), transform/opacity only, `clearProps` afterwards, reduced-motion untouched. Global fix found while auditing: `.link` now has `min-height:44px` (hero Discord link and About link were 22/27px tall).

### 4.3 notes
Join section added (`#join`, `css/sections/join.css`) **after** the `#events #team #memories` anchor stubs (final master order preserved: Phases 5–7 will insert their sections between Offers and Join; the `#join` stub was removed, the other three remain). Composition = Board 1 "Be a part of µLearn!" banner: one outlined white card with a 9px hard shadow; left = mint label "Join µLearn CHN", h2 with yellow marker on "µLearn!", lead, and an `<ol role=list>` of the three verified steps (Spec §7.6) with colour-blocked numerals 01/02/03 AND text titles (understandable without colour); right = Board 2 navy panel clipped on a diagonal (≥1024; stacks below with a top rule on smaller screens) holding "Start here", the prominent yellow **Create µLearn account** CTA (60px), a white **Join the CHN Discord** CTA, contact email (`mailto:`), LinkedIn and Instagram, with yellow sparkle and a cream loop arrow. Copy states plainly that creating an account does not add you to the Discord (separate step) and that Interest Group tasks unlock at Level 4; no approval/onboarding/membership rules were invented. All links bound via `data-link` (register, discord, offers.interestGroups, linkedin, instagram, email); external ones are `_blank` + `rel="noopener noreferrer"` + sr-only "(opens in a new tab)". Columns: 1.15fr/1fr at 1024, 1.4fr/1fr from 1360 (a 1.5fr/1fr split at 1024 wrapped the CTAs and email). Join reveal added to `motion-home.js`.

### 4.4 notes
Footer added (`<footer class="site-footer on-ink">` after `</main>`, `css/sections/footer.css`). Composition: cream→navy flipped zigzag edge (Board 2), closing tagline "Learn. Build. Belong." in cream/yellow/mint at up to 8.5rem (echoes the hero), three columns — brand (asterisk lockup, "The µLearn community of College of Engineering, Chengannur. A student community connected to the wider µLearn network.", **Part of the µLearn network: mulearn.org**), **On this page** nav (About · Offers · Events · Team · Memories · Join — all six kept; Events/Team/Memories resolve to the existing anchor stubs), **Connect with us** tiles (Discord, LinkedIn, Instagram, `mailto:` email) with indigo hard shadows turning yellow on hover; bottom bar with © line and Back to top. Credit wording: "© 2026 µLearn CHN, College of Engineering, Chengannur." — deliberately makes no ownership/trademark claim about µLearn and no "official" claim; flagged for client confirmation. Brand "vibe words" are not published (Spec §6). All links from `data/links.js` via `data-link`; external ones `_blank` + `noopener noreferrer` + sr-only "(opens in a new tab)"; the email tile has an sr-only "Email us at" prefix. Social/email URLs are client-supplied and **not independently verified for live reachability** (LinkedIn/Instagram login walls). Footer reveal added to `motion-home.js`. Decorations are in the `deco-host` (positioned clip host).

### 4.5 notes
Integration QA of header + hero + About + Offers + Join + footer together (see `docs/phase4-report.md`, `docs/responsive-report.md`, `docs/accessibility-report.md`). New: `scripts/test_phase4.py` (20/20), `docs/phase4-results.json`, `docs/audit-results-phase4.json`, `docs/audit-focus-phase4.json`, refreshed `docs/screenshots/full-*.png`. Final page order in `main`: hero → About → Offers → anchor stubs (#events #team #memories) → Join, then footer. **Phase 4 is complete.** Open client items: © line wording; unverified-live client URLs; Satoshi font files; Phase 1 tier-3 confirmations.

## Phase 3 progress (subphase checkpoints)
| Subphase | Name | Status | ZIP |
|---|---|---|---|
| 3.1 | Header & navigation | ✅ complete | `mulearn-chn_phase-03_subphase-01.zip` (+ `mulearn-chn_phase-03_subphase-01_deploy.zip`) |
| 3.2 | Hero structure, content & assets | ✅ complete | `mulearn-chn_phase-03_subphase-02.zip` (+ `mulearn-chn_phase-03_subphase-02_deploy.zip`) |
| 3.3 | Hero visual refinement & responsive | ✅ complete | `mulearn-chn_phase-03_subphase-03.zip` (+ `mulearn-chn_phase-03_subphase-03_deploy.zip`) |
| 3.4 | About section | ✅ complete | `mulearn-chn_phase-03_subphase-04.zip` (+ `mulearn-chn_phase-03_subphase-04_deploy.zip`) |
| 3.5 | Motion & interactions | ✅ complete | `mulearn-chn_phase-03_subphase-05.zip` (+ `mulearn-chn_phase-03_subphase-05_deploy.zip`) |
| 3.6 | Integration, visual QA & completion | ✅ complete | `mulearn-chn_phase-03_complete.zip` (+ `mulearn-chn_phase-03_deploy.zip`) |


Phase 3 working rules (client, 2026-11-20): run all six subphases in order **without stopping for approval**; deliver a versioned full ZIP + deployable ZIP after each; never overwrite a checkpoint. Client wants the look to be a **mix of Board 1 and Board 2** (see `docs/design-audit.md` §4).

### 3.1 notes
`index.html` created (skip link, sticky header, `<main>` with a temporary build stub replaced in 3.2). Header = asterisk + µLearn lockup with a small CHN tag, five links (About · Offers · Events · Team · Memories) and a yellow **Join us** pill (→ `data/links.js` `register`, bound by `js/main.js`, hard-coded href is the no-JS fallback). One `<nav aria-label="Main">` serves both layouts: horizontal row ≥1180px (Join is the last `<li>`, so DOM order = visual order), disclosure panel below (button `aria-expanded`/`aria-controls`, Esc closes + returns focus, link/outside click and focus-leave close, no trap). 640–1179px shows Join in the bar beside the Menu button; <640px Join sits inside the panel. Nav targets #offers/#events/#team/#memories do not exist until Phases 4–7 — the links work as anchors but scroll nowhere until then (anchor stubs are added after About in 3.4).

### 3.2 notes
Hero section added to `index.html` (`#hero`, `aria-labelledby=hero-title`): h1 "Learn. Build. Belong." (three block spans), lead "The µLearn community of College of Engineering, Chengannur." (D3 safe wording, no "official"), one generic supporting sentence (no stats/claims), CTAs **Explore events** (→ #events) and **Know more** (→ #about) as in the approved reference, plus a text link **Join the CHN Discord** bound to `data-link="discord"` (`data/links.js`). Photo = `img/hero/hero-{600,900,1200}.webp` (derivative of `IMG_7789_qyh10e.jpg`, alt from manifest, `fetchpriority=high`, 1200×1260 attrs, mono per C5-A). First-pass stickers + scallop edge in place; composition tuned in 3.3. `css/sections/hero.css` added.

### 3.3 notes
Hero composition refined against the approved Board 1 hero (+ Board 2 vocabulary). Headline: three stacked lines at `clamp(3.75rem,1.2rem+14vw,8rem)` (<900) / `clamp(5.5rem,10.2vw,10.5rem)` (≥900) / `clamp(9rem,11vw,11.5rem)` (≥1280), line-height .88. Photo: `.photo-frame--mono--tilt-r` with `--shadow-9`, ratio 10/9, `object-position:30% 100%` (trims ceiling, keeps mentor + students). Decorations are positioned per breakpoint via `.hero__s-*` classes so none overlap text: mobile = triangle + asterisk top-right of the headline, sparkle on the photo corner, indigo quarter bottom-left, grid + slab top-right; tablet adds squiggle; ≥900 adds the Board 2 ink blob (bottom-right) and gutter shapes; squiggle only ≥1280 (collided with copy at 900–1279). Lavender field ends in the Board 2 scallop edge into cream. Comparison image: `docs/screenshots/hero-vs-reference-1440.png`.

### 3.4 notes
About section added (`#about`, `css/sections/about.css`): white outlined card (label, h2 "About µLearn CHN" with lavender highlight, two paragraphs, yellow "µLearn — the network" / mint "µLearn CHN — our campus" explainer cards, two fact tags, **Our journey** → #memories + text link to mulearn.org via `data-link="mulearnOrg"`), and a tilted mono photo on a yellow mat with star, loop and faint dots. Photo `img/about/about-{410,820}.webp` (derivative of `IMG_9798_mvknx7.jpg`, alt from manifest, lazy). Copy is derived only from Spec §7.1/§7.2 (peer learning in small groups; offerings list; CHN = campus community; CEC est. 1993) — no numbers, no programmes attributed to CHN, no "official". Anchor stubs `#offers #events #team #memories #join` added after About (empty aria-hidden spans) so nav and CTA anchors resolve until Phases 4–7 replace them.

### 3.5 notes
Motion added with the Phase 2 foundation. `js/motion-home.js` (inside `MULEARN.motion.onReady` + `mm.add('(prefers-reduced-motion: no-preference)')`): hero entrance once on load (headline lines rise, intro, CTAs, photo, then sticker pop); About reveal once via ScrollTrigger (`top 75%`, `once`): card, explainer cards, tags/CTAs, photo, stickers. Only transform + opacity; `clearProps` after each timeline so no inline styles remain. CSS-only: header gets a flat 4px hard shadow after 8px scroll (`.is-stuck`, class toggled in `nav.js`), menu panel fades/slides in (≤1179px). No continuous loops, no scroll hijack. Nothing hidden in CSS: start states are applied by JS after GSAP registers (brief first-paint then entrance on load is expected). Reduced motion: GSAP is never requested and global transition rule neutralises CSS motion. `scripts/test_motion_home.py` covers normal / reduced / GSAP blocked / JS disabled / 390px / CLS (results in `docs/motion-home-results.json`).

### 3.6 notes
Integration QA of header + hero + About together (see `docs/phase3-report.md`, `docs/responsive-report.md`, `docs/accessibility-report.md`). Final-state screenshots `docs/screenshots/full-{320,390,768,1024,1440}.png`. Link check: every `data-link` href equals its `data/links.js` URL; all in-page anchors resolve (stubs after About); 19 local refs exist; no `sources/` references; every `_blank` link has `rel=noopener noreferrer` + sr-only "opens in a new tab". Focus audit: 13 tab stops (1440) / 8 (390), min ring contrast 4.53:1, none obscured, skip link OK.

## Phase 2 progress (subphase checkpoints)
| Subphase | Name | Status | ZIP |
|---|---|---|---|
| 2.1 | Project inspection & design audit | ✅ complete | `mulearn-chn_phase-02_subphase-01.zip` |
| 2.2 | Design tokens & typography | ✅ complete | `mulearn-chn_phase-02_subphase-02.zip` |
| 2.3 | Layout & reusable components | ✅ complete | `mulearn-chn_phase-02_subphase-03.zip` |
| 2.4 | Decorative library & GSAP foundation | ✅ complete | `mulearn-chn_phase-02_subphase-04.zip` |
| 2.5 | Styleguide implementation | ✅ complete | `mulearn-chn_phase-02_subphase-05.zip` |
| 2.6 | Final responsive & accessibility audit | ✅ complete | `mulearn-chn_phase-02_complete.zip` (+ deployable `mulearn-chn_phase-02_deploy.zip`) |

Phase 2 working rules (from the client brief, override `NEXT_PHASE.md` where they differ): one subphase at a time, stop for approval after each, versioned full-project ZIP after each, `index.html` assembly deferred to Phase 3.
Client note (2026-11-20): wants a **mix** of Board 1 (authority) and Board 2 (additive vocabulary). Merge plan in `docs/design-audit.md` §4.

New files in 2.1: `docs/design-audit.md`, `reference/ulearn_board-1_bold-playful_APPROVED.png`, `reference/ulearn_board-2_neo-brutalist_MIX.png`, `reference/SHA256SUMS.txt`. No design code written yet. No existing file other than docs was changed.

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
| 2026-11-20 | 5.1: Event cards are generated from `data/events.js` into `index.html` (no-JS safe) by `scripts/build_events.js`; unknown fields omitted; Build with AI shows no venue beyond each activity's own printed venue (Alappuzha/CEC conflict unresolved); Web Slingers uses register values (27 October, 4:00–5:15 PM, SDPK Room 204); master-prompt grouping (3 featured / 4 compact) unchanged. | Phase 5.1 |
| 2026-11-20 | 3.1: One `<nav>` for desktop row + mobile disclosure (no duplicated link lists); nav row from 1180px (Phase 2.6); Join CTA is the last nav `<li>` on desktop for correct tab order; link label "Offers" used for the spec's "What µLearn offers" to fit one row; CTA hrefs come from `data/links.js` via `data-link` (HTML href is the no-JS fallback). | Phase 3.1 |
| 2026-11-20 | 2.6: Focus ring + gap are surface-aware custom properties (`--focus-ring`, `--focus-gap`); yellow on indigo/ink, navy on coral, gap = card colour. `.btn` owns its text colour so ancestor `a{}` rules can't override it. Sub-AA colour pairs appear in the styleguide only as labelled "fails" chips on a neutral surface. Header nav shows from 1180px. `verify_project.py` now resolves paths relative to itself (H1 closed); root duplicate docs removed (H3 closed); stale `pack_bundles.py` replaced by `pack_deploy.py`. | Phase 2.6 |
| 2026-11-20 | 2.5: Team portraits are full-background photos (not cut-outs), so Board 1's coloured backdrop is realised as a coloured **mat** around an inset photo, with a dot pattern on two of four. Portrait captions use roles only (face↔name linkage still needs client confirmation). Styleguide uses only existing sample copy/data (event titles, formats, roles); no new facts. Board 2 wave edge realised as hard scallop mask (`.edge`). Ink/indigo cards force inherited link colour (accessibility fix). | Phase 2.5 |
| 2026-11-20 | 2.4: Sprite is single source (`img/ui/sprite.svg`) inlined per page by `sync_sprite.py` (C9-B). `motion-guard.js` lazily loads GSAP only when reduced-motion is off (saves ~118 KB for those visitors); `js-motion` class set only after both libraries register. Board 2 "wave" edge built as hard-edged scallop/zigzag masks (flat, no curves-with-gradient). GSAP licence note written by hand (npm tarball ships no LICENSE file). | Phase 2.4 |
| 2026-11-20 | Client approved audit recommendations C1-B (lavender #DDD6FE + coral #FB8F7C flat tints, navy text only), C2-B (pill buttons only), C5-A, C6-A, C7, C9–C12; instructed to continue through all subphases delivering a ZIP after each without waiting. | Client / 2.2 |
| 2026-11-20 | Subphase 2.1 audit: Board 1 = visual authority; Board 2 = additive vocabulary (shapes, ink bands, colour-blocked cards) pending palette approval C1. Board 2 text is garbled AI pseudo-text and is never used as content. GSAP 3.15.1 (16 days old) and @fontsource/plus-jakarta-sans 5.3.0 confirmed fetchable; Satoshi unavailable (fallback stays, D6). `verify_project.py` has a hard-coded `D:\\` path (H1) — fix proposed for 2.6. | Phase 2.1 |
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


## Phase 2.6 verification (re-run in this session)
- `scripts/verify_project.py` (path fixed): 96 derivatives, 4.17 MB, 0 errors, 0 warnings — **re-verified**.
- `scripts/run_audit.sh`: axe-core 0 violations at 320/390/768/1024/1440; 0 console errors; 0 non-local requests; fonts + GSAP local; reduced motion and no-JS behave.
- `scripts/audit_focus.py`: 58 tab stops, min ring contrast 3.27:1, 0 obscured, skip link OK.
- `scripts/test_motion.py`: PASS. Reports: `docs/responsive-report.md`, `docs/accessibility-report.md`; screenshots in `docs/screenshots/`.
- Not covered: real devices, Safari/Firefox, screen readers, forced-colors mode (see accessibility report).

## Known issues / items needing client confirmation (carried forward)
Satoshi still not available (fallback Plus Jakarta Sans 800, D6). Phase 1 content items in the Verification Framework tier 3 remain open.
