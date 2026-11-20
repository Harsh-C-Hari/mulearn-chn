# NEXT_PHASE.md — Phase 2: Scaffold & Design Foundation

**You are continuing the µLearn CHN website implementation.**  
Read `docs/PROJECT_MASTER_SPEC.md` (esp. §2, §3, §4, §10), `docs/PROJECT_STATE.md`, `docs/ASSET_MAPPING.md`, `docs/ASSET_MANIFEST.md`, and `docs/CHANGELOG.md`.

---

## 1. Objective of Phase 2

Scaffold the website architecture, vendor runtime dependencies, configure typography and design tokens, and build the reusable component design foundation and `styleguide.html` so subsequent phase sessions (Phases 3–7) can assemble sections directly.

Do not write full section copy or implement page-level layouts during Phase 2. Focus on the foundational design system as code.

Ensure that all design tokens, component markup, and script scaffolding strictly consume the canonical data files (`data/links.js`, `data/team.js`, `data/events.js`, `data/memories.js`) adhering to the 3-tier verification framework established in Phase 1.

---

## 2. Phase 2 Scope & Tasks

1. **Folder Scaffolding:**
   Create the directory architecture per Spec §10.2:
   - `css/` (`tokens.css`, `base.css`, `layout.css`, `components.css`, `utilities.css`, `sections/`)
   - `js/` (`main.js`, `nav.js`, `dialog.js`, `lightbox.js`, `events.js`, `team.js`, `memories.js`, `motion.js`, `util.js`)
   - `fonts/` (self-hosted `@fontsource/plus-jakarta-sans` woff2 files)
   - `vendor/gsap/` (`gsap.min.js`, `ScrollTrigger.min.js`, `LICENSE`)

2. **Design Tokens (`css/tokens.css`):**
   Copy the canonical tokens from Spec §3 verbatim:
   - Colors: `--c-bg: #F8F3E9`, `--c-ink: #0F172A`, `--c-primary: #6366F1`, `--c-primary-strong: #4F46E5` (Decision D5 for text on indigo), `--c-accent: #FACC15`, `--c-mint: #34D399`, `--c-surface: #FFFFFF`.
   - Borders: 2px solid navy (`var(--c-ink)`).
   - Shadows: `--shadow-5: 5px 5px 0 var(--c-ink)`, `--shadow-6: 6px 6px 0 var(--c-ink)`, `--shadow-7: 7px 7px 0 var(--c-ink)`.
   - Typography variables: Satoshi with Plus Jakarta Sans fallback; fluid clamp font sizes.
   - Spacing: 8px base grid, fluid gutter, container max 1440px.

3. **Vendored Dependencies:**
   - Install/vendor `gsap` (3.x) and `ScrollTrigger` into `vendor/gsap/` without runtime CDN dependencies.
   - Self-host Plus Jakarta Sans (400, 500, 600, 700, 800) woff2 files in `fonts/`. Declare `@font-face` with `font-display: swap`.
   - Declare `@font-face` fallback for Satoshi so optional client-supplied files work without code changes.

4. **Component Foundation (`css/components.css`):**
   Implement BEM components styled to the Playful Neo-Brutalist Editorial direction:
   - Buttons: `.btn`, `.btn--primary` (indigo strong + white text), `.btn--accent` (yellow + navy text), `.btn--neutral` (cream/white), `.btn--sm`. Hover: translate(-2px, -2px) + shadow-7. Active: translate(4px, 4px) + 1px shadow. Focus-visible: 3px solid outline, offset 3px.
   - Tags & Badges: `.tag`, `.tag--yellow`, `.tag--mint`, `.tag--indigo`.
   - Cards: `.card` with 2px navy border and hard offset shadows.
   - Photo Frame: `.photo-frame` with hard shadow and border.
   - Polaroid: `.polaroid` with white padding, border, hard shadow, and tilt transform.
   - Section Header: `.section-head` with eyebrow badge, bold display title, and descriptive lead text.
   - SVG Decorative Stickers: inline SVG definitions for Asterisk, Star, Triangle, Squiggle, and Dotted Grids.
   - SVG Icon Sprite: inline Lucide-style SVG icons (`arrow-right`, `arrow-up-right`, `x`, `menu`, `chevron-left/right`, `mail`, `external-link`).

5. **Data Integration Preparation:**
   Ensure components are designed to accept data from `window.MULEARN`:
   - Links: Primary CTAs consume `window.MULEARN.links.register` and `.discord`; socials consume `.linkedin`, `.instagram`, `.email`.
   - Events: Event cards and dialogs consume `window.MULEARN.events` (supporting 3 featured cards + 4 compact cards; displaying unstated years gracefully without placeholder text).
   - Team: Team grid consumes `window.MULEARN.team` (displaying 4 featured members on page; modal/expanded directory displaying all 21 members).
   - Memories: Collage consumes `window.MULEARN.memories.collageFrames`; lightbox consumes `window.MULEARN.memories.lightboxGallery`.

6. **Styleguide & Component Test Page (`styleguide.html`):**
   Build `styleguide.html` showcasing all tokens, font hierarchy, contrast checks, every component in all interactive states (default, hover, active, focus, disabled), and responsive views.

7. **Accessibility & Quality Checks:**
   - Verify WCAG 2.2 AA contrast across all token pairs.
   - Ensure touch targets meet minimum 44×44px for primary controls.
   - Test `styleguide.html` with axe-core / Playwright; zero critical/serious issues.
   - Verify zero horizontal overflow at 320px, 390px, 768px, 1024px, 1440px.

---

## 3. Deliverables for Phase 2

1. Complete file tree per Spec §10.2.
2. `css/tokens.css`, `css/base.css`, `css/components.css`, `css/layout.css`, `css/utilities.css`.
3. `vendor/gsap/` containing local vendored minified files.
4. `fonts/` containing self-hosted woff2 files.
5. `styleguide.html` component gallery.
6. `index.html` scaffold with semantic landmarks and skip link.
7. Updated `docs/PROJECT_STATE.md`, `docs/CHANGELOG.md`, and `docs/NEXT_PHASE.md` (for Phase 3).

---

## 4. Restrictions & Guardrails

- Do NOT start section layout copy or full page assembly (deferred to Phases 3–7).
- Do NOT use Tailwind, React, Vue, jQuery, or CSS frameworks.
- Do NOT introduce gradients, blurred drop shadows, or glassmorphism.
- Do NOT add runtime external CDN links. All assets and vendor scripts must be self-hosted.
- Keep reduced-motion media query active.
- Do NOT invent or alter content facts, dates, names, or URLs.
