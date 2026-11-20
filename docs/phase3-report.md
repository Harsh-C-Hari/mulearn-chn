# Phase 3 report — Header, Hero & About (living document)

Each subphase appends its section: what was built, decisions, test evidence, known issues.

## 3.1 Header & navigation
- Files: `index.html`, `css/sections/header.css`, `js/nav.js`, `js/main.js`, `scripts/test_header.py`.
- Evidence: `docs/screenshots/header-*.png`, `docs/screenshots/header-test.json`, `docs/audit-index.json`.
- Breakpoints: bar + disclosure panel below 1180px; single row at ≥1180px; Join in bar 640–1179px, inside panel below 640px, last nav item ≥1180px.
- Not tested: real devices, Safari/Firefox, screen readers.
- Open: nav targets `#offers #events #team #memories` do not exist until Phases 4–7.

## 3.2 Hero structure, content & assets
- Files: `css/sections/hero.css`; hero markup in `index.html`. Evidence: `docs/screenshots/hero-struct-*.png`.
- Content: h1 "Learn. Build. Belong."; lead = D3 safe wording; support sentence is generic voice only (no numbers/claims).
- Asset: `img/hero/hero-{600,900,1200}.webp` ← `Memories/IMG_7789_qyh10e.jpg` (per `ASSET_MANIFEST.json`); original not referenced or shipped.
- CTAs: Explore events (#events), Know more (#about), Discord link via `data-link`. The header Join pill carries the register URL.

## 3.3 Hero visual refinement & responsive
- Files: `css/sections/hero.css` (rewritten), hero markup in `index.html`. Evidence: `docs/screenshots/hero-{320,390,768,1024,1440}.png`, `hero-vs-reference-1440.png`.
- Compared with the approved Board 1 hero in headless Chromium screenshots (not code review): headline scale, stacked lines, tilted photo + hard shadow, asterisk/squiggle/triangle, lavender field + scallop. Differences are intentional: photo is a genuine workshop (no packed audience exists), copy uses the D3 identity line, Board 2 ink blob/indigo slab added per the client's "mix" request.
- Fixed during review: mobile triangle covering "Learn."; 1024 squiggle overlapping the support paragraph; asterisk hidden behind photo at 1440; wedge removed.

## 3.4 About section
- Files: `css/sections/about.css`, About markup + anchor stubs in `index.html`. Evidence: `docs/screenshots/about-*.png`, `docs/audit-index.json`.
- Content distinction: µLearn = network/organisation; µLearn CHN = campus student community. Wording traceable to Spec §7.1–7.2; nothing invented.
- Asset: `img/about/about-{410,820}.webp` ← `Memories/IMG_9798_mvknx7.jpg`, rendered mono.
- Anchor stubs for `#offers #events #team #memories #join` live after About; the "Our journey" CTA scrolls to the bottom of the page until Phase 7.

## 3.5 Motion & interactions
- Files: `js/motion-home.js`, `scripts/test_motion_home.py`, header scroll shadow + menu transition (`header.css`, `nav.js`). Evidence: `docs/motion-home-results.json` (17/17).
- Principles kept: once-only, transform+opacity, no layout shift (CLS 0.001), no scroll hijack, content visible without JS/GSAP/with reduced motion.
- Not tested: real-device performance, Safari/Firefox.

## 3.6 Integration, QA & completion
- Evidence: `docs/screenshots/full-*.png`, `docs/audit-index.json`, `docs/audit-focus-index.json`, `docs/motion-home-results.json`, Phase 3 sections of the responsive and accessibility reports.
- Phase 3 is complete; Phase 4 (Offers, Join, Footer) is next and has not been started.
- Open: nav targets (#offers #events #team #memories #join) are stubs; real-device/browser/screen-reader testing not done.
