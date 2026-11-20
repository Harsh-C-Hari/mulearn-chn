# CHANGELOG.md

Format: newest first. Each entry: date · phase · what changed · files · verification.

## 2026-11-20 — Release Preparation / Stage 1 (GitHub Readiness)
- **GitHub Readiness Audit & Documentation:**
  - Audited full repository structure at `D:\mulearn\website`: identified deployment root (`mulearn-chn/`), source archive assets (`sources/`), and historical checkpoint archives (`phase/`).
  - Created root [README.md](file:///d:/mulearn/website/README.md) covering project purpose, tech stack, directory structure, local preview, and Vercel static deployment settings.
  - Updated [mulearn-chn/README.md](file:///d:/mulearn/website/mulearn-chn/README.md) with Phase 7 completion status.
  - Enhanced root [.gitignore](file:///d:/mulearn/website/.gitignore) with standard OS, IDE, environment, Python cache, and `.vercel` exclusions while ensuring all website production assets and documentation remain tracked.
  - Scanned all 388 tracked repository files for secrets, tokens, credentials, and API keys (0 secrets found).
  - Verified project asset integrity (`verify_project.py` 96/96 derivatives PASS, data synchronizers PASS).
- **Files:** `README.md`, `.gitignore`, `mulearn-chn/README.md`, `mulearn-chn/docs/CHANGELOG.md`, `mulearn-chn/docs/PROJECT_STATE.md`.

## 2026-11-20 — Hotfix: Continuous Link Underlines (text-decoration-skip-ink: none)
- **Link Underline Gap Fix ([commit f184170]):**
  - Diagnosed browser default `text-decoration-skip-ink: auto` creating gaps under descender characters (`g`, `y`, `j`, `p`, `q`, `@`, `.`).
  - Added `text-decoration-skip-ink: none;` across `css/base.css` (`a`), `css/components.css` (`.link`, `.link:hover`), and `css/sections/footer.css` (`.site-footer a:hover`, `.footer__org`, `.footer__top`).
  - Verified all 7 target links visually across standard (1280px), 200% zoom, and mobile (375px) viewports with zero gaps and zero stray ticks.
- **Files:** `css/base.css`, `css/components.css`, `css/sections/footer.css`.

## 2026-11-20 — Phase 7 / Subphase 7.5 (Motion, Visual QA & Phase 7 Completion) — PHASE 7 COMPLETE
- **Motion Layer Integration ([js/motion-home.js]):**
  - Added restrained ScrollTrigger entrance timeline for `#memories`: section head and sparkles enter at 70% viewport, followed by each of the 6 collage polaroids rising gently at 88% viewport.
  - Complete `clearProps: "all"` cleanup on animation completion leaves zero leftover inline styles in DOM.
  - Full reduced-motion compliance: strictly wrapped in `mm.add('(prefers-reduced-motion: no-preference)')`; zero animation or layout shift when reduced motion is preferred.
- **Visual QA & Integrity:**
  - Audited across 5 viewports (320, 390, 768, 1024, 1440): zero horizontal overflow, zero console errors, zero external network requests.
  - Verified 96/96 image derivatives (`py scripts/verify_project.py` PASS).
  - Verified generator sync (`node scripts/build_memories.js --check` PASS).
- **Packaging & Delivery:**
  - Updated root archive `mulearn-chn.zip`.
  - Generated phase checkpoints: `phase/mulearn-chn_phase_7.zip`, `phase/mulearn-chn_phase-07_complete.zip`, and deployable package `phase/mulearn-chn_phase-07_deploy.zip`.
- **Files:** `js/motion-home.js`, `index.html`, `css/sections/memories.css`, `js/memories.js`, `scripts/build_memories.js`, `scripts/test_phase7.py`, `docs/PROJECT_STATE.md`, `docs/NEXT_PHASE.md`, `docs/CHANGELOG.md`.

## 2026-11-20 — Phase 7 / Subphase 7.4 (Reusable Accessible Lightbox)
- **Reusable Accessible Lightbox Modal (`<dialog id="memories-lightbox">`):**
  - Implemented the accessible lightbox dialog in `index.html` and `css/sections/memories.css`.
  - Supports `showModal()` with native focus trapping and backdrop styling (`rgba(15, 23, 42, 0.78)`).
  - Navigation controls: Previous/Next buttons (`#lightbox-prev`, `#lightbox-next`), mobile touch-friendly navigation bar (`#lightbox-mob-prev`, `#lightbox-mob-next`), and close button (`#lightbox-close`).
  - Keyboard navigation: Escape key closes the dialog, Left arrow (`ArrowLeft`) steps backward, Right arrow (`ArrowRight`) steps forward.
  - Focus restoration: upon closing (via Escape, Close button, or backdrop click), keyboard focus returns directly to the button that triggered the modal.
  - Image display & Preloading: displays full resolution photograph with native dimensions (`#lightbox-dims`), category badge (`#lightbox-category`), position counter (`#lightbox-counter`, e.g. "Photo 3 of 11"), and preloads adjacent photos in memory for instantaneous stepping.
- **Global Event Delegation ([js/memories.js]):**
  - Integrated click delegation for all `[data-lightbox-open]` triggers across both the 6 polaroids in the collage and the 11 cards in the gallery.
- **Verification ([scripts/test_phase7.py]):**
  - Added end-to-end browser tests verifying opening from collage cards, opening from gallery cards, next/prev button clicks, arrow key navigation, Escape closing, and focus return.
- **Files:** `index.html`, `css/sections/memories.css`, `js/memories.js`, `scripts/test_phase7.py`, `docs/NEXT_PHASE.md`, `docs/CHANGELOG.md`, `docs/PROJECT_STATE.md`.

## 2026-11-20 — Phase 7 / Subphase 7.3 (11-Item Gallery Display & Drawer Filter)
- **11-Item Community Gallery Display:** Implemented the accessible gallery drawer (`#memories-gallery`) containing all 11 verified community photographs and authentic event extractions, with full responsive layouts (3 cols desktop, 2 cols tablet, 1 col mobile).
  - Cards feature thumbnail preview with badge, category tag with color tone (yellow/mint/coral/lavender), image dimensions, verified title, and observable caption.
  - Action trigger `<button type="button" class="gallery-card__action" data-lightbox-open="..." aria-haspopup="dialog">` with visually hidden text and focus ring.
- **Drawer Toggle & Category Filtering ([js/memories.js]):**
  - Added accessible disclosure toggle button (`#memories-gallery-toggle`, `aria-expanded`, `aria-controls="memories-gallery"`).
  - Built interactive category filtering with 5 buttons (`All (11)`, `Community (1)`, `Workshops (4)`, `Events (5)`, `Design (1)`), updating `aria-pressed`, active styling, and card visibility.
  - No-JS resilience: with JavaScript disabled (`.no-js`), toggle button is hidden and gallery drawer is displayed by default (`.no-js .memories__drawer[hidden] { display: block !important; }`).
- **Generator & Verification Integration:**
  - Extended `scripts/build_memories.js` to render both collage and gallery cards from `data/memories.js` (`--check` mode verified).
  - Updated `scripts/test_phase7.py` to assert 11 gallery cards, drawer toggle functionality, and category filter behavior.
- **Files:** `scripts/build_memories.js`, `js/memories.js`, `css/sections/memories.css`, `index.html`, `scripts/test_phase7.py`, `docs/NEXT_PHASE.md`, `docs/CHANGELOG.md`, `docs/PROJECT_STATE.md`.

## 2026-11-20 — Phase 7 / Subphase 7.2 (Six-Frame Editorial Collage)
- **Six-Frame Editorial Polaroid Collage:** Implemented the responsive 6-frame collage in `css/sections/memories.css` and `index.html` via `scripts/build_memories.js`.
  - Dominant centerpiece `p5` (`polaroid--main` with "Featured moment" tag) spanning 8 columns on desktop and full width on tablet/mobile with `src1200` high-res derivative.
  - Two medium frames `p1` (Lab Session Overview, 1.8:1) and `p2` (Mentored Workshop, 2.0:1) with subtle alternating tilts (-3° / +2.5°).
  - Three small frames `p3` (Community Gathering, 1.9:1), `p4` (Peer Collaboration, 1.8:1), and `p6` (Technical Demo, 1.1:1).
- **Playful Neo-Brutalist Styling & Interactions:** Pure flat white polaroids with 2px navy borders, hard offset shadows (`var(--shadow-5)` / `var(--shadow-7)`), interactive hover/focus straightening and lift (`scale(1.015)` and `var(--shadow-9)`), and yellow-to-mint interactive badge snap.
- **Accessibility & Touch Targets:** Every polaroid includes a fully accessible stretched `<button type="button" class="polaroid__action" data-lightbox-open="..." aria-haspopup="dialog">` with visually hidden screen-reader label, visible focus ring (`outline: 3px solid var(--c-primary)`), and WCAG AAA compliance.
- **Automation & Test Guard:** Created `scripts/build_memories.js` to render markup from `data/memories.js` (with `--check` flag). Updated `scripts/test_phase7.py` to assert collage structure, slots, dimensions, non-upscaling, and lightbox trigger targets.
- **Files:** `scripts/build_memories.js`, `css/sections/memories.css`, `index.html`, `scripts/test_phase7.py`, `docs/NEXT_PHASE.md`, `docs/CHANGELOG.md`, `docs/PROJECT_STATE.md`.

## 2026-11-20 — Phase 7 / Subphase 7.1 (Memory Asset Audit & Section Structure)
- **Asset Audit & Inventory:** Performed full technical audit of all 6 editorial collage mappings (13 derivatives) and 11 lightbox gallery items (6 community photos + 5 extracted genuine event photos) in `data/memories.js`. All derivatives verified present in `img/memories/` and `img/events/` as clean WebP with stripped EXIF/GPS metadata and non-upscaled resolutions. Explicitly documented exclusion of promotional poster `Memories/event5_zdu88j.jpg` ("Weekly Twitches / Salt-Mango Tree"), low-res duplicate screenshots, and sponsor slides in `docs/memories-audit.md`.
- **Semantic Memories Section:** Created `css/sections/memories.css` adhering to Playful Neo-Brutalist design tokens (white surface band, 2px navy borders top/bottom, subtle grid background, responsive headings, container rules). Replaced `<div class="anchor-stubs"><span id="memories"></span></div>` in `index.html` with `<section id="memories" class="section section--clip section--ruled section--white memories" aria-labelledby="memories-title">`, containing kicker tag, `h2#memories-title`, verified lead copy, and structural placeholders for the collage and gallery.
- **Anchor & Test Integration:** Connected navigation anchors (`header a[href="#memories"]`, About CTA `a[href="#memories"]`, and footer link `a[href="#memories"]`). Updated `scripts/test_phase4.py` and `scripts/test_phase6.py` section order assertions to recognize the real `#memories` section. Created `scripts/test_phase7.py` covering asset validity, DOM semantics, content rules, and multi-viewport responsive layout.
- **Files:** `data/memories.js`, `css/sections/memories.css`, `index.html`, `scripts/test_phase4.py`, `scripts/test_phase6.py`, `scripts/test_phase7.py`, `docs/memories-audit.md`, `docs/NEXT_PHASE.md`, `docs/CHANGELOG.md`.

## 2026-11-20 — Phase 6 / Fix-01 (Sticker anchoring + roster decoration)
- **Featured Team Stickers (Phase 1):** Anchored stickers inside `<article class="card member-card">` so they translate with card on hover (`translate(-3px, -3px)`), matching Offers cards. De-duplicated Hanin C K's sticker from `#s-asterisk` to `#s-bolt` with `sticker--coral sticker--outlined`, giving 4 completely distinct shapes across the 4 featured leads (asterisk, star, sparkle, bolt).
- **Featured Event Stickers (Phase 2):** Anchored stickers inside `<article class="card event-card">` for the 3 featured cards (ODYSSEY, Buildathon, Build with AI) so they move with cards on hover.
- **Roster Card Decoration (Phase 3):** Filled all 21 directory cards (`.roster__item`) moderately with one sticker and one CSS-only geometric accent (`::before`). Enforced strict distance rules: shape repeat distance >= 6 (cycles 7 shapes), color repeat distance >= 4 (cycles 6 colors), color never equals photo mat, and accent color never equals sticker or mat. Added `.roster__item { position: relative; overflow: hidden; isolation: isolate; }`, `.roster__text, .roster__photo { position: relative; z-index: 1; }`, and `.roster__text { padding-inline-end: var(--s-3); }` so text and photos always sit above decorations with zero text-bounding-box collisions.
- **Motion Scope (Phase 4):** Scoped `.team .sticker > svg` in `js/motion-home.js` to `.team > .sticker > svg, .member-card__stk > svg` so the 21 roster stickers enter as one unit with `.roster-panel` rather than triggering an elongated 21-element sequential stagger cascade.
- **Verification & QA (Phase 5):** Added new assertions to `scripts/test_phase6.py` (116/116 passed) and `scripts/test_phase5.py` (282/282 passed). All existing suites green: `test_phase4.py` (20/20), `test_motion.py` (PASS), `test_motion_home.py` (PASS, CLS = 0.0024), `verify_project.py` (PASS), `independent_verification.py` (PASS). Zero horizontal overflow, zero console errors, zero external requests.
- **Files:** `scripts/build_team.js`, `scripts/build_events.js`, `css/sections/team.css`, `index.html`, `js/motion-home.js`, `scripts/test_phase5.py`, `scripts/test_phase6.py`, `docs/PROJECT_STATE.md`, `docs/CHANGELOG.md`.

## 2026-11-20 — Phase 6 / Subphase 6.5 (Integration, visual QA & Phase 6 completion) — PHASE 6 COMPLETE
- Reviewed the Team section in full-page context at 1440 and 390 (`docs/screenshots/team-6-5-{1440,390}.png`): lavender "The people" label, "Meet the team" headline with yellow underline, four colour-blocked portrait cards (yellow/indigo/mint/yellow) with white label bars, Board 2 grid + stickers, lavender roster panel with 21 numbered entries and four "Featured above" flags. Matches the Board 1 + Board 2 mix; **no visual changes were needed**.
- Verified every role label and image-to-name pairing against `data/team.js` (21 unique names/roles in order, held titles for Geetha S / Divyalakshmi / Swathy J not shown, Hanin = Operational Lead). Portrait pairings remain filename-based (see `docs/team-audit.md`) and are listed as open client confirmations.
- Final gates: test_phase6 104/104; test_phase5 278/278; test_phase4 20/20; motion tests PASS (CLS 0.001); axe 0 violations at 320/390/768/1024/1440; no overflow, console errors or external requests; verify_project PASS; deployable ZIP has no sources/docs/scripts/reference; both final ZIPs extracted fresh and re-tested.
- Phase 6 marked complete; Phase 7 — Memories & Gallery is next (not started).

## 2026-11-20 — Phase 6 / Subphase 6.4 (Interaction & motion refinement)
- Decision (recorded): **no filters, search or category navigation** (21 people fit on one scan; filtering would only hide people and add state) and **no member dialogs/profile pages** (no biographies or links exist in the content register). The roster stays a plain, fully visible list.
- Added: Team reveal in `js/motion-home.js` (inside the existing `mm.add('(prefers-reduced-motion: no-preference)')`): section head + stickers timeline (once), each featured card rises as it nears the viewport, the directory panel enters as one block (the 21 entries are not animated individually). Transform + opacity only, `clearProps` on completion, nothing hidden in CSS. 6.4 checks in `scripts/test_phase6.py`, `docs/audit-results-phase6-4.json`, `docs/screenshots/team-6-4-{1440,390}.png`.
- Unchanged by design: hover/focus feedback (card lift + photo straightening, roster lift) already in `css/sections/team.css`; no control depends on hover; no focusable controls in the Team section (nothing dead to tab to).
- Verified: test_phase6 104/104 (normal, reduced-motion, GSAP blocked and JS-disabled all show 21 + 4 fully visible with no leftover inline styles; no layout shift); test_phase5 278/278; test_phase4 20/20; motion PASS (CLS 0.001); axe 0 ×5; no overflow/console errors/external requests; verify_project PASS.

## 2026-11-20 — Phase 6 / Subphase 6.3 (Complete 21-member directory)
- Added: complete directory (`directoryItem()` in `scripts/build_team.js`, "Directory" block in `css/sections/team.css`), section decorations (grid, triangle, star, asterisk, squiggle), directory note, 6.3 checks in `scripts/test_phase6.py`, `docs/audit-results-phase6-3.json`.
- Design: one ordered list of all 21 in roster order inside a Board 2 lavender panel; white Board 1-style entries with a small framed portrait on a rotating colour mat (yellow/mint/coral/indigo), numeral, name and role; the four featured are marked with the text flag "Featured above" so the count stays 21. 1 column <700, 2 columns 700–1023, 3 columns ≥1024. No group headings (they would imply a hierarchy). Held titles show the name only. Directory thumbnails use empty alt (the name is adjacent).
- Verified: test_phase6 91/91; test_phase5 278/278; test_phase4 20/20; motion PASS (CLS 0.001); axe 0 ×5; no overflow/console errors/external requests; verify_project PASS.

## 2026-11-20 — Phase 6 / Subphase 6.2 (Featured team cards)
- Added: four featured team cards (`featuredItem()` in `scripts/build_team.js`, "Featured cards" block in `css/sections/team.css`), 6.2 checks in `scripts/test_phase6.py`, `docs/audit-results-phase6-2.json`.
- Design: Board 1 portrait cards on yellow / indigo / mint backdrops with a white label bar (name + role), Board 2 hard shadows, ±1.5° tilt that straightens on hover/focus, flat corner stickers, desktop vertical stagger. 1 column (horizontal card) <600px, 2×2 at 600–1023, 4 across ≥1024. Portraits are the 300/600 derivatives via `srcset`, whole 5:6 frame, never upscaled. `photoShown:false` renders a neutral monogram instead of a portrait.
- Verified: test_phase6 61/61; test_phase5 278/278; test_phase4 20/20; motion PASS (CLS 0.001); axe 0 ×5; no overflow/console errors/external requests; verify_project PASS.

## 2026-11-20 — Phase 6 / Subphase 6.1 (Roster audit & section structure)
- Added: `docs/team-audit.md`, `scripts/build_team.js`, `scripts/test_phase6.py`, `css/sections/team.css`, real `#team` section (head + featured list + 21-entry roster, generated from data, no-JS safe), `docs/audit-results-phase6-1.json`, `docs/phase6-results.json`.
- Changed: `data/team.js` rewritten to a reconciled schema (display `roleLabel`, `roleStatus`, `photo`, `photoShown`, `featuredOrder`, `tone`); fixed two non-existent image paths; held titles for Geetha S, Divyalakshmi, Swathy J; `#team` stub removed; `scripts/test_phase4.py` order/stat assertions updated for Team; `css/sections/events.css` thumbnail layout-shift fix.
- Verified: test_phase6 31/31; test_phase5 278/278; test_phase4 20/20; motion PASS (CLS 0.001); axe 0 ×5; no overflow/console errors/external requests; verify_project PASS.

## 2026-11-20 — Phase 5 / Subphase 5.5 (Integration, visual QA & Phase 5 completion) — PHASE 5 COMPLETE
- Reviewed the Events section in the full page (desktop/tablet/mobile screenshots) against Board 1 + Board 2: hierarchy, spacing, poster legibility, featured vs compact subordination and decoration all accepted; no code changes were required. Phase 5 content/asset/dialog code is unchanged from 5.4.
- Added: `docs/phase5-report.md`, `docs/audit-results-phase5-5.json`, `docs/audit-results-phase5-5-dialogs.json`, `docs/screenshots/events-5-5-{1440,390}.png`.
- Verified: test_phase5 278/278; test_phase4 20/20; test_motion_home + test_motion PASS (CLS 0.001); axe 0 violations (page ×5, each of 7 dialogs × 5 widths = 35 runs); no overflow, 0 console errors, 0 external requests; verify_project PASS; fresh-extract checks of both final ZIPs.
- Deliverables: `mulearn-chn_phase-05_complete.zip`, `mulearn-chn_phase-05_deploy.zip`.

## 2026-11-20 — Phase 5 / Subphase 5.4 (Accessible event-detail dialogs)
- Added: `js/events.js`, `css/sections/event-dialog.css`, dialog shell in `index.html`, `dialogNote` (Tech Forge) in `data/events.js`, dialog tests in `scripts/test_phase5.py`, `docs/audit-results-phase5-4.json`, `docs/audit-results-phase5-4-dialogs.json`, `docs/screenshots/dialog-*.png`.
- Verified: all seven triggers individually ×5 widths; Esc/Close/backdrop + focus return; reduced-motion, GSAP-blocked, JS-disabled; test_phase5 278/278; axe 0 (page ×5, dialogs ×35); test_phase4 20/20; motion PASS; verify_project PASS.

## 2026-11-20 — Phase 5 / Subphase 5.3 (Compact event entries)
- Added: compact entry markup/CSS (`compactCard()`, events.css compact block), 8 thumbnail derivatives `img/events/thumb-*`, `tone`/`thumb` fields in `data/events.js`, compact checks in `scripts/test_phase5.py`, `docs/audit-results-phase5-3.json`, `docs/screenshots/events-5-3a-*.png`.
- Changed: Tech Forge descriptor → "TECHFORGE 2.0"; squiggle sticker hidden <1024px; upscale test uses the real file width from `currentSrc`.
- Verified: test_phase5 93/93; test_phase4 20/20; motion PASS; axe 0 ×5; no overflow; 0 console errors; 0 external requests; verify_project PASS.

## 2026-11-20 — Phase 5 / Subphase 5.2 (Featured event cards)
- Added: real featured cards (`css/sections/events.css` featured block; `featuredCard()` in `scripts/build_events.js`), `blurb`/`tone`/`meta` fields in `data/events.js`, Events reveal in `js/motion-home.js`, per-width featured checks in `scripts/test_phase5.py`, `docs/audit-results-phase5-2.json`, `docs/screenshots/events-5-2a-*.png`.
- Changed: Instagram "›" chip removed from `img/events/poster-{odyssey,buildathon}.webp` and `card-{odyssey,buildathon}-{405,600,810}.webp` (inpainted, same filenames); `scripts/shot_events.py` forces eager images.
- Verified: test_phase5 65/65; test_phase4 20/20; motion PASS; axe 0 ×5; no overflow; 0 console errors; 0 external requests; verify_project PASS.

## 2026-11-20 — Phase 5 / Subphase 5.1 (Event data audit & section structure)
- Added: `css/sections/events.css`, real `#events` section in `index.html` (label, h2, lead, note, Featured/More groups, generated placeholder cards), `scripts/build_events.js`, `scripts/test_phase5.py`, `scripts/shot_events.py`, `docs/events-audit.md`, `docs/phase5-results.json`, `docs/audit-results-phase5-1.json`, `docs/screenshots/events-5-1-*.png`.
- Changed: `data/events.js` reconciled to the master-prompt accuracy rules (unsupported venues/labels removed, schema = group/order/facts/lists/parts); `#events` anchor stub removed; `scripts/test_phase4.py` order assertion includes `events`.
- Verified: `test_phase5` 41/41, axe 0 ×5, no overflow, 0 console errors, 0 external requests, `test_phase4` 20/20, motion pass (CLS 0.001), `verify_project.py` pass.

## 2026-11-20 — Phase 4 / Subphase 4.5 (Integration, visual QA & completion) — PHASE 4 COMPLETE
- Added: `scripts/test_phase4.py`, `docs/phase4-results.json`, `docs/audit-results-phase4.json`, `docs/audit-focus-phase4.json`, Phase 4 sections in `docs/responsive-report.md`, `docs/accessibility-report.md`, `docs/phase4-report.md`; refreshed `docs/screenshots/full-*.png`.
- Verified: axe 0 ×5, no overflow, 0 console errors, 0 external requests, integration 20/20, motion 17/17, `verify_project.py` pass. Phase 5 not started.

## 2026-11-20 — Phase 4 / Subphase 4.4 (Footer)
- Added: `css/sections/footer.css`, `<footer>` in `index.html`, footer reveal in `js/motion-home.js`, `docs/screenshots/footer-{320,390,768,1024,1440}.png`.
- Verified: axe 0 violations ×5, no overflow, 0 console errors, 0 external requests, 0 targets <24px, 41 keyboard stops all with visible focus, 24 `data-link` anchors match `data/links.js`, all anchors resolve, `_blank` links compliant, motion tests pass (CLS 0.001), `verify_project.py` pass.

## 2026-11-20 — Phase 4 / Subphase 4.3 (Join section)
- Added: `css/sections/join.css`, `#join` section in `index.html` (after the Events/Team/Memories stubs), Join reveal in `js/motion-home.js`, `docs/screenshots/join-{320,390,768,1024,1440}.png`.
- Changed: `#join` anchor stub removed (real section now).
- Verified: axe 0 violations ×5, no overflow, 0 console errors, 0 external requests, 0 targets <24px, 28 keyboard stops all with visible focus, every `data-link` href equals `data/links.js`, all `_blank` links have noopener/noreferrer + sr-only note, all anchors resolve, motion tests pass (CLS 0.001).

## 2026-11-20 — Phase 4 / Subphase 4.2 (Offers: visual & responsive refinement)
- Rewrote `css/sections/offers.css` (stagger, tilt, stickers, ink bar, responsive); added corner stickers + decor layer + `.ink-bar` note to `#offers` in `index.html`; Offers reveal in `js/motion-home.js`.
- Changed: `css/components.css` `.link{min-height:44px}` (touch target fix, also lifts hero/About links).
- Verified: axe 0 violations at 320/390/768/1024/1440, 0 targets under 24px, no overflow, 0 console errors, 0 external requests, motion tests 17/17 (CLS 0.001), screenshots refreshed (offers/hero/about ×5).

## 2026-11-20 — Phase 4 / Subphase 4.1 (What µLearn offers: content & structure)
- Added: `css/sections/offers.css`, `#offers` section in `index.html`, `scripts/shot_section.py`, `scripts/checkpoint.sh`, `docs/screenshots/offers-{320,390,768,1024,1440}.png`.
- Changed: `js/main.js` (dotted `data-link` paths); `#offers` anchor stub removed.
- Verified: axe 0 violations ×5 widths, no overflow, 0 console errors, 0 external requests, every `data-link` href equals its `data/links.js` URL, all anchors resolve, `verify_project.py` pass.

## 2026-11-20 — Phase 3 / Subphase 3.6 (Integration, visual QA & completion) — PHASE 3 COMPLETE
- Added: `scripts/screenshot_full.py`, `docs/screenshots/full-*.png`, `docs/audit-focus-index.json`, Phase 3 sections in `docs/responsive-report.md` and `docs/accessibility-report.md`, Phase 3 section in `docs/design-system.md`.
- Changed: `scripts/audit_focus.py` honours `FOCUS_OUT`; removed superseded `page-*.png` screenshots.
- Verified: see accessibility report. Phase 3 complete; Phase 4 not started.

## 2026-11-20 — Phase 3 / Subphase 3.5 (Motion & interactions)
- Added: `js/motion-home.js`, `scripts/test_motion_home.py`, `docs/motion-home-results.json`; header scroll shadow + menu transition in `header.css` / `nav.js`; `motion-home.js` script tag in `index.html`.
- Changed: `scripts/audit_a11y.py` waits 2.6s after load.
- Verified: `test_motion_home.py` 17/17 (normal entrance runs and ends clean; About reveals on scroll at 1280 and 390; reduced motion = GSAP never requested, content visible; GSAP blocked and JS disabled = content visible; CLS 0.001; 0 external requests; no page errors); `test_motion.py index.html` PASS; header test unchanged; axe 0 violations ×5 after the entrance completes.
- Known: the only console line in the GSAP-blocked scenario is the browser logging the request the test blocks on purpose.

## 2026-11-20 — Phase 3 / Subphase 3.4 (About section)
- Added: `css/sections/about.css`, About markup + anchor stubs in `index.html`, `docs/screenshots/about-{320,390,768,1024,1440}.png`.
- Fixed during review: fact tag overflowed the card at 320/390 (tags may wrap), unverified phrase "run by students for students" removed, faint ink dots replace near-invisible yellow dots.
- Verified: no page overflow ×5 (only clipped decorations extend past the viewport), axe 0 violations ×5, 0 console errors, 0 external requests, 13 tab stops all with visible focus ring.

## 2026-11-20 — Phase 3 / Subphase 3.3 (Hero visual refinement & responsive)
- Changed: `css/sections/hero.css` rewritten (per-breakpoint composition, tuned headline scale, photo crop); hero sticker markup in `index.html` now uses `.hero__s-*` classes (adds ink blob, sparkle, indigo quarter; removes inline style placement).
- Added: `docs/screenshots/hero-{320,390,768,1024,1440}.png`, `docs/screenshots/hero-vs-reference-1440.png`.
- Verified: no overflow ×5; axe 0 violations ×5; 0 console errors; 0 external requests; visual review of every width against the approved reference.

## 2026-11-20 — Phase 3 / Subphase 3.2 (Hero structure, content & assets)
- Added: `css/sections/hero.css`, hero markup in `index.html` (replaces the 3.1 stub), `docs/screenshots/hero-struct-{320,390,768,1024,1440}.png`.
- Removed: temporary `.stub` rule from `header.css`.
- Verified: no overflow ×5 widths, 0 console errors, 0 external requests; hero image loads from `img/hero/` derivatives only (no source file referenced).

## 2026-11-20 — Phase 3 / Subphase 3.1 (Header & navigation)
- Added: `index.html`, `css/sections/header.css`, `js/nav.js`, `js/main.js`, `scripts/test_header.py`, `docs/screenshots/header-{320,390,768,1024,1180,1440}.png` (+ `-menu-open`, `-nojs`), `docs/audit-index.json`.
- Changed: `scripts/audit_a11y.py` / `run_audit.sh` accept `AUDIT_OUT` so a page audit no longer overwrites Phase 2 results.
- Verified (headless Chromium): menu open/Esc/focus-return/link-close/outside-close at 320/390/768/1024; sticky top = 0; no overflow at 320/390/768/1024/1180/1440 (open and closed); desktop nav on one row at 1180 and 1440; no-JS page keeps links + CTA; axe 0 violations ×5; 0 console errors; 0 external requests; `verify_project.py` PASS.

## 2026-11-20 — Phase 2 / Subphase 2.6 (final responsive & accessibility audit) — PHASE 2 COMPLETE
- Added: `docs/responsive-report.md`, `docs/accessibility-report.md`, `docs/screenshots/styleguide-{320,390,768,1024,1440}.png`, `docs/audit-results.json`, `docs/audit-focus.json`, `scripts/audit_a11y.py`, `scripts/audit_focus.py`, `scripts/run_audit.sh`, `scripts/pack_deploy.py`.
- Fixed (a11y): failing-contrast demo chips; yellow footer button inheriting cream text (1.38:1); invisible navy shadow on buttons in ink sections; focus ring 1:1 on indigo card and 2.79:1 on coral card (now surface-aware `--focus-ring`/`--focus-gap`).
- Fixed (responsive): hero asterisk over lead text at 768; squiggle clash at 1024; header CTA wrapping at 1024 (nav now from 1180px); 320px overflow introduced and caught during the fix.
- Fixed (tooling): `verify_project.py` hard-coded `D:\` path (H1); removed duplicate root `ASSET_MANIFEST.md`, `ASSET_MAPPING.md`, `LICENSE-PlusJakartaSans.txt` (H3, byte-identical copies remain in `docs/` and `fonts/`); replaced stale `pack_bundles.py`.
- Verified: see `docs/accessibility-report.md` (axe 0 violations ×5 widths, 58 tab stops, min focus-ring contrast 3.27:1, 0 console errors, 0 external requests, reduced-motion + no-JS OK), `verify_project.py` PASS (96 derivatives), `test_motion.py` PASS.

## 2026-11-20 — Phase 2 / Subphase 2.5 (styleguide)
- Added: `styleguide.html` (hero on lavender field with scalloped Board 2 edge, ink jump bar, 10 sections: colour with computed contrast chips, typography specimens, spacing scale, borders/radii/shadows, buttons × states (default/hover/pressed/focus/disabled) for accent/neutral/indigo plus sizes, links, nav links, cards (colour-blocked, numbered, link, ticket, media with real event art, tags, dividers), image frames (mono tilt, coloured mats, caption bar, team portraits on coloured mats, polaroid collage from real photos), stickers (two composed fields + full index of 15 shapes), responsive grids (breakpoints, spans, auto-fit/stagger, editorial split), focus-visible demo incl. on-ink; closing Join banner rebuilt from Board 1), `css/sections/styleguide.css` (page chrome only), `scripts/test_keyboard.py`.
- Fixed during review: links on `.card--ink` / `.card--indigo` inherited navy (invisible / 2.84:1) → now inherit card text colour; screenshot script now forces lazy images to load; 320px overflow in button matrix and spacing rows; ink button demo placed on an ink surface (invisible) → moved.
- Verified (headless Chromium): overflow none at 320/390/768/1024/1440; 0 console errors; 0 external requests; keyboard walk: 58 tab stops, 0 without a visible ≥2px focus ring; `test_motion.py` PASS on the styleguide; no gradient/blur functions in any CSS. Visual review of all sections at 1440 plus mobile layout metrics.

## 2026-11-20 — Phase 2 / Subphase 2.4 (decorative library & GSAP foundation)
- Added: `img/ui/sprite.svg` (12 icons + 17 flat stickers), `scripts/sync_sprite.py` (inlines the sprite into pages between `sprite:start/end` markers, C9-B), `css/decor.css` (sticker wrapper + colour/size modifiers, CSS shapes, dotted/grid backdrops, scallop/zigzag edges, clip panels, ink bar, flat highlight), `vendor/gsap/{gsap.min.js,ScrollTrigger.min.js,LICENSE,VERSION}` (GSAP 3.15.1), `js/motion-guard.js`, `scripts/test_motion.py`, `scripts/pack_checkpoint.py`, `docs/decor-sheet.html` (dev reference), `docs/design-system.md`.
- Changed: `.sticker` wrapper moved from `components.css` to `decor.css` (now supports end/bottom placement).
- Verified (headless Chromium): `test_motion.py` PASS in 3 scenarios — normal (GSAP 3.15.1 + ScrollTrigger load locally, `html.js-motion` set), reduced-motion (GSAP never requested, class absent), GSAP blocked (class absent, 0 hidden elements, page intact). 0 external requests. Sprite XML valid; decor sheet reviewed visually. No page animations implemented.

## 2026-11-20 — Phase 2 / Subphase 2.3 (layout & components)
- Added: `css/layout.css` (containers, sections incl. colour variants, 4/8/12 grid, auto grids, splits, editorial, stack/cluster), `css/components.css` (buttons primary/accent/neutral/ink/sm with all states, text link, nav link, cards: outlined, yellow/mint/lavender/coral/indigo/ink/cream, numbered, ticket, flush; photo frames incl. tilt/mono/backdrop/mat; polaroid; section label/head; tags; meta; divider; bands; sticker wrapper; prose), `css/utilities.css`, `scripts/screenshot.py`.
- Verified (Chromium, 320/390/768/1024/1440): 0 horizontal overflow, 0 console errors, 0 external requests; visual review of 1440 render. Fixed frames/polaroids stretching in grids (align-self:start). Removed a gradient-based divider (forbidden).

## 2026-11-20 — Phase 2 / Subphase 2.2 (tokens & typography)
- Added: `css/tokens.css` (3-layer tokens: primitive → semantic; colour, spacing, radius, hard shadows, type scale, layout, motion, z-index, breakpoints doc), `css/base.css` (reset, element defaults, focus-visible, skip link, sr-only, dialog scroll lock, reduced-motion), `fonts/PlusJakartaSans-{400,500,600,700,800}.woff2` + OFL licence + `fonts/README.md`.
- Decisions applied: C1-B (lavender #DDD6FE, coral #FB8F7C), C2-B (pill radius for buttons only), C5-A (opt-in mono photos, later), C6-A (Satoshi fallback).
- Verified (headless Chromium, file://): Plus Jakarta Sans 400/700/800 load locally, µ glyph present, h1 resolves display stack, 0 external requests, 0 console errors, no horizontal overflow at 1440. Satoshi uses local() only to avoid 404s.



## 2026-11-20 — Phase 2 / Subphase 2.1 (design audit)
- Added: `docs/design-audit.md` (reference analysis of two boards, mix strategy, conflicts C1–C12, implementation plan 2.2–2.6, reuse inventory, approvals needed).
- Added: `reference/ulearn_board-1_bold-playful_APPROVED.png`, `reference/ulearn_board-2_neo-brutalist_MIX.png`, `reference/SHA256SUMS.txt`.
- Updated: `docs/PROJECT_STATE.md`, `docs/NEXT_PHASE.md`.
- Verified: project structure inspected; npm availability of gsap 3.15.1 and Plus Jakarta Sans 5.3.0 confirmed; ZIP integrity tested. `verify_project.py` could not run (hard-coded path) — see state file.
- No design code written.

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
