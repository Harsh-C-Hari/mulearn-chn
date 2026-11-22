# Image Skeleton System — Phase 3: Technical Architecture

Status: specification only. No site code changed in this phase.

## 1. Constraint that shapes everything
Image markup is **generated** (`build_events.js`, `build_team.js`, `build_memories.js`) or **created at runtime** (`js/events.js`, `js/memories.js`). So the system is *attached from outside*: no per-image HTML changes, no required classes, nothing the builders must emit.

## 2. Components
```
css/skeleton.css   tokens + overlay base + one block per variant + failed state + reduced-motion
js/skeleton.js     engine: VARIANTS (selector → name), TEMPLATES (name → static SVG string), state machine
index.html         +1 <link> (after decor.css) +1 <script defer> (after memories.js). Nothing else.
```
The overlay is **one `<span class="skel skel--VARIANT" aria-hidden="true">`** inserted right after the `<img>` inside the existing host, containing one inline `<svg>` made only of flat shapes + `<use href="#s-asterisk|#s-dots|#s-star|#i-image">`. No new assets, no dependencies, no gradients.

## 3. State machine (per `<img>`)
```
            ┌── complete && naturalWidth>0 ───────────────► (nothing — no skeleton, no work)
 attach ────┤
            ├── complete && naturalWidth==0 && src ───────► FAILED
            └── otherwise ───────────────► LOADING ──load──► LOADED (overlay removed, 160ms reveal)
                                              └──error──► FAILED (static overlay + #i-image)
 lightbox:  src attribute mutation ► reset to LOADING / nothing (cached) ► LOADED / FAILED
```
* Host gets `data-skel-state="loading|failed"` (removed when loaded). CSS keys off it.
* **Cached / already-complete** images are detected synchronously with `img.complete` → never get an overlay.
* **Lazy** images: `complete` is false until fetched → overlay shows until the browser actually loads them. We never change `loading=`; native lazy-loading is untouched. The skeleton can never delay an image: it is a sibling overlay, not a gate.
* **Failed**: `error` → overlay switches to static failed look; no infinite pulse. The `<img>` keeps its `alt`.
* **No duplicate listeners**: `img.__skel` token set once per element; listeners use `{once:true}`; lightbox uses a per-request counter so a stale `load` from photo N-1 cannot clear photo N's state.
* **Dynamic insertion**: one `MutationObserver` on `#event-dialog` (childList, subtree) attaches new `<img>`; one attribute observer on `#lightbox-image` (`src`). No global body observer.
* Initial scan runs once on `DOMContentLoaded`/immediately (script is `defer`): iterate `VARIANTS`, `querySelectorAll`.

## 4. Layout rules
* Overlay `position:absolute; inset:var(--skel-inset)`, where inset = host mat width, border/radius copied from the image rule → box identical to the image box. Images already reserve space via `width/height` + `aspect-ratio`, so **no shift**.
* Hosts that are `position:static` (`.event-mini__thumb`, `.event-dialog__photo`, `.lightbox-dialog__stage`) get `position:relative` in `skeleton.css` only.
* Overlay is inserted after the `<img>` and before badges, so existing badges/captions paint above it.
* Lightbox is the exception: the overlay is **in flow** with `aspect-ratio:var(--skel-ar)` (from the new photo's `width/height`) while the `<img>` is `display:none`; it swaps 1:1 on load so the stage never jumps, and the *old photo never lingers under the new caption*.

## 5. Accessibility
* Overlay `aria-hidden="true"`, `pointer-events:none`, no text, no focusable children.
* `alt`, `width`, `height`, `src`, `loading` on images are never altered.
* No JS → `html.no-js` / script missing → no overlay is ever created → images behave exactly as today.
* Reduced motion → all skeleton animation off (`prefers-reduced-motion: reduce`), reveal fade off.
* Forced-colours: overlay uses real borders so it stays visible; decorative fills may flatten, acceptable.

## 6. Error strategy
`error` event + `complete&&naturalWidth==0` check. Failed state is static and quiet. No retry loops, no network calls.

## 7. Files and sequence
1. 4.1 foundation: `skeleton.css` (tokens/base/failed/reduced-motion), `skeleton.js` (engine, empty variant tables), wiring in `index.html`.
2. 4.2 hero + about.  3. 4.3 posters + mini thumbs.  4. 4.4 portraits + roster.
5. 4.5 collage + gallery thumbs.  6. 4.6 lightbox.  7. 4.7 event-dialog photos.
8. Phase 5 responsive/a11y/motion verification (Playwright).  9. Phase 6 regression + final report.
Each step re-packs the project zip.
