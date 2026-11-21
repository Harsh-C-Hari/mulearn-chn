# Phase 8.1 — Motion & Interaction Audit

Audited: 2026-11-21 · Scope: `index.html`, `js/{motion-guard,motion-home,nav,events,memories,main}.js`, `css/*.css`, `css/sections/*.css`, `vendor/gsap` (GSAP + ScrollTrigger **3.15.1**).
Method: static reading of every motion file + empirical probes in headless Chromium (served over HTTP, 1440 and 390 wide; normal / reduced-motion / GSAP-blocked). No project file was changed in 8.1 other than this report and the PROJECT_STATE entry.

## 1. Motion architecture (what exists)
* `motion-guard.js` loads GSAP then ScrollTrigger (serially, after parse) **only if** `prefers-reduced-motion` is off; adds `html.js-motion` after both register; exposes `MULEARN.motion {ready, reduced, onReady}`; on a live switch to reduced it reverts `mm`, kills every ScrollTrigger and clears the global timeline.
* `motion-home.js` registers everything inside one `mm.add("(prefers-reduced-motion: no-preference)")`. Start states are applied by GSAP `.from()` (nothing hidden in CSS). Every timeline ends with `clearProps`.
* `events.js` animates the event dialog panel (open `fromTo` 0.35 s, close `to` 0.2 s) when `MULEARN.motion.ready && !reduced`.
* CSS only: hover/active transitions (`--t-fast .15s`, `--t-med .3s`, `--t-slow .7s`, `--ease-out cubic-bezier(.22,1,.36,1)`), header `.is-stuck` shadow, mobile menu `menu-in`, event-dialog backdrop fade, lightbox `lb-fade`.
* **27 ScrollTrigger instances**: About 1, Offers 1+6 cards, Events 1+3 cards, Team 1+4 cards+1 roster, Memories 1+6 polaroids, Join 1, Footer 1. No continuous animations (no `.sticker--spin/--bob` in the markup; 0 running CSS animations at rest).

### Existing motion inventory
| Area | Motion | Trigger | Timing / offset |
|---|---|---|---|
| Hero | title lines yPercent 70, intro y24, CTAs y20, figure y56 + rotate, stickers scale-pop | load | .05–1.1 s, power3.out, `back.out(2)` stickers |
| About | card y48, pair y28, facts/actions y16, figure y64, stickers | `top 75%`, once | .45–.9 s |
| Offers | head y32, stickers, note y24; each card y56 | `top 70%`; cards `top 88%` | .5–.8 s |
| Events | head y32, stickers; each featured card y56 | `top 70%`; cards `top 88%` | .55–.8 s |
| Team | head y32, stickers; 4 cards y48; roster panel y40 | `top 70%`; `top 90%`; `top 92%` | .55–.75 s |
| Memories | head y32, stickers, actions y24; 6 polaroids y48 | `top 70%`; `top 88%` | .5–.75 s |
| Join | banner y56, steps y24, CTAs y20, stickers | `top 70%` | .45–.8 s |
| Footer | big words yPercent 60, grid y24, bar y12, stickers | `top 85%` | .4–.7 s |
| Dialogs | event panel y28 fade; lightbox CSS fade only | click | .35 / .2 s |

### Existing interaction inventory
Hover lifts and hard-shadow growth are all gated by `(hover:hover) and (pointer:fine)`; `:active` presses exist for `.btn`, `a.card`, `.footer__tile`, nav links, gallery filters, toggle, lightbox close/nav. Focus ring is global (`:focus-visible`, surface-aware). Tap highlight is suppressed only on `.btn` and the topbar logo (component-specific; no global suppression). Event dialog: showModal, Esc/close/backdrop, Tab trap, focus return, `panel.scrollTop=0`. Lightbox: showModal, close, 4 nav buttons (desktop + mobile), arrows, cyclic, preload, backdrop click. Nav: disclosure with Esc/outside/link/focus-out close, IntersectionObserver `aria-current`, `.is-stuck`.

## 2. Findings

| # | Sev | Finding | Evidence |
|---|---|---|---|
| F1 | **High** | **Deep links do not scroll in normal-motion mode.** `/#team` loads at scrollY 0 (Team at 6407 px). Reduced-motion and GSAP-blocked land correctly. Cause: `html{scroll-behavior:smooth}` (`css/base.css:9`) fights ScrollTrigger's refresh (it jumps to 0 to measure, then restores). Forcing `scroll-behavior:auto` makes the deep link land (scrollY 6315, Team 92 px). | probe: normal `[0, 6407]`, reduced `[6315, 92]`, blocked `[6315, 92]` |
| F2 | Med | **First-paint flash in the hero.** Content is visible at ~125 ms, GSAP arrives (serial script load) and hides it at ~286 ms, then re-reveals until ~1 s. | rAF opacity timeline |
| F3 | Med | **Stale ScrollTrigger positions after layout change.** Opening the Memories drawer adds ~2.2 k px but `ScrollTrigger.refresh()` is never called: Join trigger stays at 10320 while Join is really at 12993, so Join/Footer reveals fire off-screen ahead of the user. Gallery filter also changes height. | `C_starts_*` |
| F4 | Med | **Inconsistent scroll motion:** start offsets 70/75/85/88/90/92 %, y offsets 12–64 px, durations .4–.9 s, three different card idioms; 27 triggers where 9 would do; every sticker pops with `back.out(2)` at different delays. | motion-home.js |
| F5 | Low | `transition:all` on `.gallery-filter` (memories.css:483) and on the lightbox image/nav rules; `will-change:transform` permanently on `.polaroid` (memories.css:96, 6 nodes); lightbox `transition: transform var(--t-fast), background-color var(--t-fast)` lacks the shared easing (memories.css:608). | grep |
| F6 | Low | Open/close motion is inconsistent: event dialog uses GSAP (and its in/out tweens are not cancelled against each other), lightbox uses a CSS fade and has no exit and no feedback when the photo changes. | events.js, memories.css |
| F7 | Low | Memories drawer toggle uses `scrollIntoView({behavior:"smooth"})` unconditionally (ignores reduced motion in JS; CSS rule only covers `scroll-behavior`). | memories.js |
| F8 | Low | Switching reduced→no-preference at runtime re-enables GSAP but the one-shot `onReady` callbacks are not re-run (content stays visible, so no breakage). | probe |
| F9 | Info | Event dialog: re-open during the 0.2 s close tween is ignored. Not reachable by a real user (page is inert). | probe E |

Verified OK: no console errors; reduced motion loads no GSAP and nothing is left hidden; 0 inline hidden styles after reveals; rapid scroll-to-bottom leaves nothing stuck; reload with restored scroll reveals everything above; focus returns to trigger after dialog/lightbox; lightbox is cyclic; mobile menu closes on link tap and lands with the header offset; `aria-current` updates.

## 3. Files / selectors needing attention
`css/base.css` (html scroll-behavior) · `js/motion-guard.js` · `js/motion-home.js` (all reveal blocks) · `js/memories.js` (drawer/filters → refresh, smooth scroll) · `js/nav.js` + new anchor handler · `js/events.js` (tween cancel) · `css/sections/memories.css` (:96, :483, :608, lightbox image) · `index.html` head (pre-hide guard).

## 4. Priority
8.2: F1, F2, F3, F4 (+F8) · 8.3: F5 and the button/card/control audit · 8.4: F6, F7, F9 · 8.5/8.6: resilience matrix and final regression.

Out of scope (per brief): the branded intro/loader.
