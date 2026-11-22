# Image Skeleton System — Phase 2: Visual Design System

Status: specification only. No site code changed in this phase.

## 1. Principle — "an unfinished editorial layout"
The skeleton is the **paste-up board before the photo is pasted in**: cream stock, a navy keyline, a few flat registration marks. It is not a grey shimmer bar.

Shared rules (consistency comes from rules, not identical layouts):
1. **Surface** is muted warm cream (`--skel-base`), never white, never grey, never a gradient.
2. **Keyline**: same border as the image it stands in for (1px navy inside mats, 2px where the image itself has a 2px frame). Hosts keep their own 2px outline, mat and hard shadow — the skeleton never draws a second card.
3. **Shapes** are flat fills in `--skel-shape` (a slightly darker cream). They suggest *composition* (horizon, sun, figure, grid of frames) but never content (no text, no faces).
4. **Accents**: max **two** accent colours per skeleton, each < 6% of the area, always at the edge or a corner. Palette: yellow, mint, indigo (+ coral/lavender only where the host card already uses them as its mat).
5. **Motif**: the existing `#s-asterisk` / `#s-dots` / `#s-star` sprite symbols, reused — never a new icon family.
6. **No** gradients, blur, glass, rounded pills, 3D, shimmer sweeps.
7. **Motion**: one idea only — accent marks "breathe" (opacity .45 ↔ 1, 1.8 s, steps eased). Large surfaces never animate. `prefers-reduced-motion: reduce` → fully static.
8. Everything is `aria-hidden`, `pointer-events:none`.

## 2. Tokens (new, in `css/skeleton.css` `:root`; palette values reuse existing tokens)
```css
--skel-base:   #F1EADA;            /* cream, one step darker than --c-bg */
--skel-shape:  #E4DAC3;            /* internal shapes */
--skel-line:   var(--c-ink);
--skel-a1:     var(--c-accent);    /* yellow */
--skel-a2:     var(--c-mint);
--skel-a3:     var(--c-primary);   /* indigo */
--skel-pulse:  1.8s;
--skel-ease:   ease-in-out;
```
Only `--skel-base` and `--skel-shape` are new hex values (derived from cream; nothing in the locked palette is that muted). Everything else aliases existing tokens.

## 3. Variants

| Variant | Host / inset | Composition (flat shapes) | Accents | Shadow/border |
|---|---|---|---|---|
| **hero** | `.hero__figure`, inset 0 | Large "photograph" board: low horizon block across the bottom 38%, a big off-centre circle (sun/lens) top-right, two stepped rectangles left (screens), one asterisk bottom-left | yellow circle ring, indigo asterisk | host's 2px + shadow-9; no extra |
| **about** | `.about__figure`, inset 8px (yellow mat) | Projector-screen frame (rect with 2px inner keyline) + short "stand" bar; small dots cluster | mint dot cluster (one accent only – mat is already yellow) | 2px navy, radius 4 |
| **poster** | `.event-card__poster`, inset 8px | Poster layout: title block (thick bar) near top third, central square "art" field with diagonal-free corner marks, two thin bars at bottom, ruler ticks at the edges | host tone colours only: one small yellow block + one indigo star | 1px navy, radius 3 |
| **mini** | `.event-mini__thumb` (tone mat), inset 8px / centred 390:502 on mobile | Minimal poster: 1 bar + 1 field + 1 bar | none (mat provides colour); asterisk in ink | 2px navy, radius 3, shadow-3 |
| **portrait** | `.member-card__photo`, inset 4px | Head-and-shoulders silhouette from two flat shapes (circle + rounded-top block, **no face**) on a cream field; small corner asterisk | single yellow or mint corner block (by `:nth-child`) | 1px navy, radius 3 |
| **roster** | `.roster__photo`, inset 4px, 72–84px | Same silhouette, nothing else | none, **no animation** | 1px navy |
| **collage** | `.polaroid__photo`, inset 0 | Wide photo board: three overlapping frames of different sizes (varies per slot p1–p6 via rotation of layout presets), small dot strip | one accent per slot cycling yellow/mint/indigo | 1px navy (host has it) |
| **gallery** | `.gallery-card__thumb`, inset 0 | 16:10 board: one big frame + two small frames, tiny asterisk | one accent, by category tone | – |
| **lightbox** | `.lightbox-dialog__stage`, box sized to the *new* photo's ratio | Dark-stage–aware: cream board with 2px **white** keyline (matches the stage image border), big centred asterisk-ring, corner crop marks | yellow ring + mint corner tick | 2px `--c-surface`, radius 8 |
| **dialog-photo** | `.event-dialog__photo`, inset 6px | Same as gallery, reduced | none | 1px navy |

### Failed state
Static (animation off), `--skel-base` surface, the existing `#i-image` sprite icon centred in `--skel-shape` stroke ink at 60%, no pulse. The real `alt` remains on the `<img>` for assistive tech.

### Mobile
* Accent marks keep their size ratios (they are percentage-based inside the overlay's viewBox, so they scale with the image).
* On <640px: hero drops the stepped rectangles, poster drops the ruler ticks (calmer, as `.sticker--hide-sm` does elsewhere).
* roster/mini never animate on any width.

## 4. Motion spec
```css
@keyframes skel-breathe { 0%,100% { opacity:.45 } 50% { opacity:1 } }
.skel [data-a] { animation: skel-breathe var(--skel-pulse) var(--skel-ease) infinite }
.skel [data-a="2"] { animation-delay: -.6s }   /* desynchronised, still gentle */
@media (prefers-reduced-motion: reduce) { .skel [data-a] { animation:none; opacity:1 } }
```
Removal is instant on `load`; the revealed image gets a 160 ms opacity-in (motion-allowed only).

## 5. Rejected ideas (and why)
* Shimmer sweep — explicitly banned, and a gradient.
* Per-image blurhash — adds assets/tooling, blur is banned.
* Pulsing the whole surface — competes with content; only small accents move.
* Skeleton for dialog poster — already cached; no overlay geometry for a tilted sticky image.
