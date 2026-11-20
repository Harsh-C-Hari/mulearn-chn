# design-audit.md — Phase 2 / Subphase 2.1

**Date:** 2026-11-20 · **Scope:** inspection and audit only. No design-system code has been written.
**Inputs read:** `PROJECT_MASTER_SPEC.md`, `PROJECT_STATE.md`, `NEXT_PHASE.md`, `ASSET_MAPPING.md`, `CHANGELOG.md`, `PHASE0_REPORT.md` §1, the unmodified prototype, and the two reference boards supplied for Phase 2.

Reference boards are now stored in `reference/` (additive; the prototype is untouched):

| File | Role | SHA-256 (first 12) |
|---|---|---|
| `reference/ulearn_board-1_bold-playful_APPROVED.png` | **Visual authority** (layout, composition, components) | `aa45dfb0997a` |
| `reference/ulearn_board-2_neo-brutalist_MIX.png` | **Mix source** — client wants "a mix of both" | `de11fed968b4` |
| `reference/ulearn_prototype_v1_UNMODIFIED.html` | Behavioural reference only | `333a447d23a3` |

---

## 1. Current project state

- Phase 0 and Phase 1 are complete. Phase 2 has not started: **no `css/`, `js/`, `fonts/`, `vendor/`, `index.html` or `styleguide.html` exist yet.**
- Present: `data/*.js` (4 modules), `img/` (96 derivatives), `docs/`, `scripts/`, `reference/`.
- The handoff ZIP does **not** contain `sources/` (originals), so nothing in this phase can touch them.

### Hygiene findings (not design, but they affect Phase 2)

| # | Finding | Impact | Proposed handling |
|---|---|---|---|
| H1 | `scripts/verify_project.py` hard-codes `BASE_DIR = r"D:\mulearn\website"` and looks for `sources/`. It fails in any other location (reproduced: "Manifest not found"). | Subphase 2.6 requires running it. | Make paths relative to the script and make the `sources/` check optional. Needs approval because it edits a verified Phase 1 script (logic unchanged). |
| H2 | The source ZIP was created on Windows (backslash path separators). | Some unzip tools warn or flatten paths. | All new ZIPs are built with forward slashes. |
| H3 | `ASSET_MANIFEST.md` and `ASSET_MAPPING.md` exist both at the root and in `docs/` (byte-identical). `README.md` still says "Phase 0 handoff bundle… planning documents only". | Confusing for a new session. | Keep `docs/` as canonical; propose removing the root duplicates and refreshing README in 2.6. |
| H4 | `docs/NEXT_PHASE.md` (Phase 2 scope) differs slightly from your Phase 2 brief (e.g. it lists `index.html` scaffold, `js/*` stubs, and event/team BEM components; your brief limits Phase 2 to the design foundation + styleguide). | Scope creep risk. | **Your brief wins.** Event/team/offer-specific cards and `index.html` assembly are deferred to Phases 3–7. See §6. |

---

## 2. Reference analysis — Board 1 (visual authority)

Board 1 is a composition sheet with a design-system column. Measured and observed characteristics:

**Palette (stated on the board, matches the spec):** Indigo `#6366F1` primary, Yellow `#FACC15` accent, Mint `#34D399` secondary, Navy `#0F172A` neutral on a warm cream field. The board also uses a lighter violet (≈ lavender, appears around the hero's top-right slab and the About star ring), which is a *tint of indigo*, not a new hue.

**Typography:** Heavy geometric grotesque for display (Satoshi Black-like). Hero headline is three stacked lines at roughly 0.85–0.9 line-height with tight tracking; the full stops are part of the design. Body is a clean humanist/geometric sans (Plus Jakarta Sans). Section titles ("About µLearn", "Events", "Meet the Team", "Memories") are bold ~2.5–3.5rem at desktop with a short, light lead line beneath.

**Composition patterns**
1. **Hero:** copy left, tilted (≈ 5°) black-and-white photo right, overlapping the headline's last word. Stickers cluster around the photo: indigo asterisk, yellow squiggle, mint triangle, indigo quarter-circle bottom, indigo slab top-right behind the "Join Us" button, faint dotted grid top-centre.
2. **About:** small text block left, tilted portrait photo right with a yellow star plus an indigo/yellow arc "ring" sweeping behind it.
3. **Events:** three compact tiles with a framed media area and a short title.
4. **Team:** four portrait cards on alternating colour backdrops (yellow, indigo with dots, yellow, mint with dots) with a label bar beneath.
5. **Memories:** loose polaroid collage; white frames, slight rotations, four-point sparkle stickers in yellow and navy; a faint dotted grid behind.
6. **Join:** split card — cream left, navy right with a diagonal/clipped edge, indigo and mint corner shapes, a hand-drawn loop line, yellow CTA.

**Component language**
- Buttons: yellow fill or white fill, navy text, bold, **pill-shaped** in the board, with a **hard offset navy shadow** (~5px).
- "Card": white, rounded (~12–14px), **thin** border, asterisk icon, ghost text lines; accompanied by a tilted photo.
- Brand-vibe chips: pills (internal vibe words; the spec forbids publishing them as copy).
- Section panels on the board have soft, thin cream borders. This is board chrome, not a component.

**Decorative vocabulary (to be built in 2.4):** asterisk (6–8 arms), squiggle/tilde, triangle, quarter-circle, slab (rotated rectangle/parallelogram), star (5-point and 4-point sparkle), dotted grid, arc ring, hand-drawn loop line, underline stroke.

**Observations that affect implementation**
- B&W treatment is applied to the **hero and About** photos only. Team portraits are colour on tinted backdrops. (Consistent with Phase 0 defect P5: the prototype wrongly greyscaled everything.)
- Hero photograph in the board is a packed auditorium. The project has no such photo; Phase 1 chose `hero-1200.webp` (IMG_7789). This is a known, accepted limitation.
- Copy on the board ("The official tech community…", "Operations Lead", the vibe words) conflicts with verified-content rules — see §5, C3.

---

## 3. Reference analysis — Board 2 (the "mix" source)

Board 2 is a three-page concept sheet plus swatches/buttons and three dark banner strips. **All text on it is garbled, AI-generated pseudo-text** (e.g. "Copesiroi", "Soeber"), so it is used for **shape, colour, and layout vocabulary only; no wording, logo, or type is taken from it.** The only legible text is the wordmark "µLearn" and "µLearn ChN".

**What it adds that Board 1 does not have**
| # | Pattern in Board 2 | Description |
|---|---|---|
| B2-1 | **Oversized black organic/angular shapes** | Huge navy-black blobs and slabs in the hero, overlapped by a yellow parallelogram or a sparkle. Much larger and heavier than Board 1's stickers. |
| B2-2 | **Full-bleed lavender hero field** | Entire hero in pale violet with a wavy cream edge dropping into the cream page. |
| B2-3 | **Ink bands and bars** | Black pill/swoosh band under the hero; full-width black info bars; black footer-like panels with a yellow badge. |
| B2-4 | **Colour-blocked photo cards of mixed sizes** | Tilted/stacked cards in coral, blush pink, indigo, mint, yellow, each with an inset photo and a small white action button. Staggered and varied, not a uniform grid. |
| B2-5 | **Numbered/tile modules** | Cream tiles with a big glyph or numeral (maps to the spec's "01–06 offer cards"). |
| B2-6 | **Ticket / label card** | Yellow rectangular card with a tab or notch used for metadata. |
| B2-7 | **Solid-circle panel with icon** | Navy panel with a large indigo circle holding a diamond/box outline icon. |
| B2-8 | **Extended palette** | Coral/salmon, blush pink, orange, a saturated royal/cobalt blue (buttons), mint-green, lavender, plus the Board 1 yellow and navy. |
| B2-9 | **Button range** | Black, cobalt-blue, yellow, indigo, and cream buttons with hard shadows and a small arrow glyph. |

**Observations**
- Some surfaces on Board 2 (lavender hero, coral hero blob) show soft tonal variation that reads as gradient/blur. That is a rendering artefact of the concept image; per spec it must be built as **flat colour only**.
- Board 2's overall feel is heavier, blockier, and more "poster-like". Board 1 is lighter, more playful, with thinner decoration.

---

## 4. "Mix of both" — proposed merge strategy (needs your approval)

**Principle:** Board 1 remains the visual authority for layout, hero composition, polaroid collage, team backdrops, and component shapes. Board 2 contributes **additive vocabulary** that makes sections more varied and bolder, **provided it stays inside the locked rules** (flat colour, 2px navy outlines, hard shadows, no gradients/blur) unless you approve palette extensions (C1).

| Board 2 idea | Where it lands | Implementation | Conflict? |
|---|---|---|---|
| B2-1 black blobs/slabs | Decorative library: `deco-blob-ink`, `deco-slab-ink` (used large behind hero photo, in Join panel) | Inline SVG, flat navy | None |
| B2-2 lavender hero field | **Hero/section variant** `.section--lavender` with a hard-edged scalloped or stepped divider | Flat tint of indigo | **C1** (new tint token) |
| B2-3 ink bands | `.band--ink` divider and footer/CTA panels; yellow label badge | CSS, navy fill, yellow tag | None |
| B2-4 colour-blocked mixed-size cards | `.card--yellow/--mint/--indigo/--lavender/--coral`; offsets and size variants (wide/narrow); inset photo via `.photo-frame` | CSS | Coral/lavender need **C1** |
| B2-5 numbered tiles | `.card--numbered` (big numerals 01–06) — directly supports the spec's offers section | CSS | None |
| B2-6 ticket/label card | `.tag` and `.card--ticket` for event metadata (date/venue) | CSS | None |
| B2-7 circle panel | Decorative `deco-circle` + icon holder in Join panel | SVG/CSS | None |
| B2-8 extended palette | Optional tokens | See C1 | **Yes** |
| B2-9 button range | `.btn--primary` (indigo-strong), `--accent` (yellow), `--neutral` (cream), `--ink` (navy) | CSS | Cobalt blue not adopted (C1) |

Skills consulted for this audit: **ui-ux-pro-max / design-system** (three-layer token architecture: primitive → semantic → component), **frontend-design** (commit to one distinctive point of view, avoid templated defaults), **industrial-brutalist-ui** (see C8: only the rigid-grid/oversized-numeral ideas are usable), **design-taste-frontend** (avoid generic card grids; vary composition).

---

## 5. Conflicts and decisions requiring approval

Each item lists a recommended default. **Nothing below has been implemented.** Items marked ⛔ block the relevant later subphase.

| ID | Conflict | Options | Recommendation |
|---|---|---|---|
| **C1** ⛔ (2.2) | Board 2's extra colours (coral, blush, orange, cobalt, lavender) vs. the locked palette ("no new colours", spec §13.2). | **A** Strict: no new colour tokens; lavender/coral/orange/cobalt from Board 2 are simply not used (the "mix" is limited to shapes and layout). **B** Two additive tokens only: `--c-lavender` (flat indigo tint, navy text 13:1) and `--c-coral` (one accent for a single card variant). Both must keep navy text ≥ 4.5:1. **C** Adopt Board 2's full palette. | **B.** It delivers the visible "mix" while keeping the identity. I will propose exact hex values and contrast results in 2.2 for you to approve before they are used. |
| **C2** (2.2) | **Button shape.** Board 1 buttons are pill-shaped; your brief says 8–14px radii and avoid excessive pills; spec/prototype use 8px. | A: 8–12px rect (brief). B: pill buttons only, everything else 8–14px (reference). | **B.** The reference is the visual authority and pills appear only on buttons. Tags use 8px, not pills. |
| **C3** (content) | Board 1 copy says "official tech community" and "Operations Lead", and shows the vibe-word pills. Spec says ❌ "official" unverified, role is "Operational Lead", vibe words are internal. | — | Styleguide and later sections use the spec wording. Board copy is treated as placeholder. |
| **C4** (2.2/2.3) | **Card borders.** Board 1's "card" has a thin soft border; brief requires strong 2px navy borders and hard shadows. | — | Follow the brief (2px navy + hard shadow). |
| **C5** (2.3) | **Photo treatment.** Board 1 shows hero/About photos in B&W. A CSS `grayscale(1)` filter is not a gradient or blur, but it is a presentation choice on real photos. | A: B&W on hero/About only (as board). B: colour everywhere. | **A**, implemented as an opt-in class `.photo--mono`, never on team/event photos. |
| **C6** (2.2) | **Satoshi** is not on npm; Fontshare is outside the sandbox's allowed network. Board 1's display type looks like Satoshi Black. Fallback (Plus Jakarta Sans 800) is slightly softer/wider. | A: ship fallback now. B: you supply `Satoshi-Black/Bold.woff2` + licence. | **A now**; `@font-face` for Satoshi is declared so B needs no code changes (decision D6). |
| **C7** (2.4) | **Decorative file location.** Spec §10.2 has no decor file. | Put in `components.css`, or add `css/decor.css` + `img/deco/*.svg`. | New `css/decor.css` and inline SVG symbols; flagged because it extends §10.2. |
| **C8** (info) | `industrial-brutalist-ui` skill says "pick one archetype… no mixing", prescribes CRT/scanline/halftone degradation and utilitarian muted palettes. | — | **Not adopted.** Only ruled dividers, rigid grid logic, and oversized numerals (useful for offers 01–06) are borrowed. No analog-degradation effects. |
| **C9** (2.4) | **Inline SVG sprite duplication.** External `<use href="sprite.svg#id">` is blocked on `file://` in Chromium; spec §10.3 requires an inline sprite in `index.html`. The styleguide would need a second copy. | A: duplicate by hand. B: one source file `img/ui/sprite.svg` + `scripts/sync_sprite.py` that injects it into both HTML files. | **B**, so there is a single source of truth. |
| **C10** (2.4) | **GSAP version.** | 3.15.1 (published 2026-11-04, 16 days old — passes the spec's "≥ 14 days" rule) vs 3.15.0 (2026-04-13). | **3.15.1** per the spec, with the exact version recorded in `vendor/gsap/VERSION`. Licence: GSAP "Standard no-charge licence" (to be vendored as `LICENSE`). |
| **C11** (2.6) | **H1** verify script edit (see §1). | — | Approve minimal path fix. |
| **C12** (2.5) | **Index/scope.** `NEXT_PHASE.md` also asks for an `index.html` scaffold and JS module stubs. | — | Not in your brief; deferred to Phase 3 unless you want it earlier. |

---

## 6. Design-system implementation plan (2.2 → 2.6)

### Token architecture (3 layers, all in `css/tokens.css`)
1. **Primitive:** raw values from spec §3 (`--c-bg`, `--c-ink`, `--c-primary`, `--c-primary-strong`, `--c-accent`, `--c-mint`, `--c-surface`, plus C1 additions once approved).
2. **Semantic:** purpose aliases (`--text`, `--surface-page`, `--surface-card`, `--border-color`, `--focus-ring`, `--link`).
3. **Component:** per-component hooks (`--btn-bg`, `--btn-fg`, `--card-shadow`) defined on the component, so variants only override variables.

Other token groups: type scale (fluid `clamp()` values from spec), weights (400/500/600/700/800; display 800–900 only if Satoshi present), line-heights (display 0.88–1.0, body 1.6), spacing (8px grid, `--s-0…--s-16`), borders (2px), radius (8/12/14 + pill for buttons, C2), hard shadows (5/6/7 px, plus a 3px "sm" and a 1px "pressed"), containers (1440 max, 1200 content, 720 prose), breakpoints (documented in a comment since CSS vars can't drive media queries: 640 / 1024 / 1280), z-index scale (deco 0, content 1, header 50, dialog 100).

### Subphase plan
| Subphase | Files created | Key outputs |
|---|---|---|
| **2.2** | `css/tokens.css`, `css/base.css`, `fonts/PlusJakartaSans-{400,500,600,700,800}.woff2` (from `@fontsource/plus-jakarta-sans@5.3.0`, latin subset), `fonts/README.md` (Satoshi drop-in notes) | `@font-face` with `font-display:swap`, reset, element defaults, skip-link style, `:focus-visible`, reduced-motion block, `text-wrap`. Zero external requests. Minimal `styleguide.html` stub is **not** created until 2.5. |
| **2.3** | `css/layout.css`, `css/components.css`, `css/utilities.css` | Containers, grids (4/8/12 col), split layouts, image frames, spacing utilities; buttons, links, nav links, cards (outlined, coloured, numbered, ticket), section label, tags, dividers, bands. |
| **2.4** | `css/decor.css`, `img/ui/sprite.svg`, `scripts/sync_sprite.py`, `vendor/gsap/{gsap.min.js,ScrollTrigger.min.js,LICENSE,VERSION}`, `js/motion-guard.js` | Sticker library (asterisk, star, sparkle, triangle, quarter-circle, slab, blob, squiggle, loop line, dotted grid, arc ring, circle+icon); GSAP loader that adds `html.js-motion` only if GSAP loads and motion is allowed; nothing hidden by default. |
| **2.5** | `styleguide.html` (+ styleguide-only CSS section file if needed) | Editorial showcase of all ten items in your list, driven by the real CSS. |
| **2.6** | `docs/responsive-report.md`, `docs/accessibility-report.md`, `docs/screenshots/styleguide-{320,390,768,1024,1440}.png`, fixed `verify_project.py` | Playwright overflow checks, axe-core (test-time only), keyboard walk, contrast table, network-request audit. Final ZIP `mulearn-chn_phase-02_complete.zip`. |

### Components and states (2.3)
- **Buttons:** `.btn` + `--primary | --accent | --neutral | --ink`, `--sm`; states default / hover (−2,−2 + shadow-7) / active (+4,+4 + 1px shadow) / focus-visible / disabled; min 44×44.
- **Links:** `.link` (underline-offset, arrow), `.nav-link` (+ `[aria-current]`).
- **Cards:** `.card` base, `--yellow | --mint | --indigo | --lavender* | --coral*` (*pending C1), `--numbered`, `--ticket`; text on indigo uses `--c-primary-strong`.
- **Frames:** `.photo-frame` (+ `--tilt-l/r`, `--mono`), `.polaroid`.
- **Misc:** `.section-label` (eyebrow), `.tag` (+ colours), `.divider` (ruled, dashed, band), `.sticker` wrapper (absolute, `aria-hidden`, `pointer-events:none`).

### Constraints I will enforce
Decorations never create overflow (contained with `overflow:clip`); text never sits directly on photos; `#6366F1` is never text colour; no `!important` outside the reduced-motion block; JS hooks via `data-js`; no inline event handlers.

---

## 7. Reusable resources already in the project

| Resource | Reuse |
|---|---|
| Spec §3 token block, §4 type rules, §10.4 button mechanics | Copied almost verbatim into 2.2/2.3 |
| Prototype CSS (`.btn`, `.card`, `.pol`, `.join` clip-path, reduced-motion block) and 7 inline SVG shapes | Starting point for components and decor (not copied blindly; P1–P10 defects avoided) |
| `img/brand/logo.{webp,png}` (262 px wide) | Footer/brand reference only (D7). Header uses a typographic lockup |
| `img/hero/*`, `img/about/*`, `img/team/*`, `img/events/*`, `img/memories/*` | Real imagery for styleguide frames, polaroids, and image-frame demos (no placeholders, no generated people) |
| `data/*.js` | Not consumed in Phase 2 components beyond sample data in the styleguide (kept verified) |
| npm `gsap@3.15.1`: `dist/gsap.min.js` (73,357 B), `dist/ScrollTrigger.min.js` (44,683 B) | Confirmed fetchable in the sandbox; to be vendored in 2.4 |
| npm `@fontsource/plus-jakarta-sans@5.3.0`: latin 400/500/600/700/800 woff2 | Confirmed available; µ (U+00B5) is in the Latin subset |
| Satoshi | **Not available** (not on npm; Fontshare blocked) |

### External dependencies found in the prototype (must not carry over)
Google Fonts `<link>` (lines 7–9) and cdnjs GSAP 3.12.5 (lines 205–206). Both are replaced by vendored copies.

---

## 8. Approvals I need before Subphase 2.2

Please reply with choices (or "go with recommendations"):

1. **C1** palette extension — A, **B (recommended)**, or C.
2. **C2** button shape — A or **B (recommended)**.
3. **C5** B&W only on hero/About — **A (recommended)** or B.
4. **C6** ship Plus Jakarta Sans fallback now — **A (recommended)** or provide Satoshi files.
5. **C7 / C9 / C10 / C11 / C12** — approve as recommended, or tell me what to change.

Nothing else is blocking.
