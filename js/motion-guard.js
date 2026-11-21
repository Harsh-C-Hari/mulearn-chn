/*!
 * motion-guard.js — safe animation-loading foundation (Phase 2.4)
 * Classic script. Include once, with `defer`, near the end of <body>:
 *     <script defer src="js/motion-guard.js"></script>
 *
 * Contract (Master Spec §12):
 *  1. Nothing is hidden by default. Content is fully visible with no JS, no GSAP, or a failed load.
 *  2. GSAP + ScrollTrigger are loaded only when the visitor has not asked for reduced motion
 *     (so reduced-motion visitors do not even download ~118 KB).
 *  3. <html class="js-motion"> is added only after BOTH libraries loaded and registered. Initial "hidden"
 *     states may only be applied by JS after that moment (never in CSS).
 *  4. If the visitor switches reduced-motion ON later, everything is reverted and the class is removed.
 *  5. Page code talks to this module only through window.MULEARN.motion (below); it never assumes `gsap` exists.
 *
 * Public API  (window.MULEARN.motion)
 *   .ready        boolean — true once GSAP + ScrollTrigger are registered and motion is allowed
 *   .reduced      boolean — current prefers-reduced-motion state
 *   .refresh()    re-measure pending ScrollTriggers after a layout-height change (safe no-op without motion)
 *   .onReady(fn)  fn(gsap, ScrollTrigger, mm) runs once motion is ready (immediately if already ready).
 *                 `mm` is a gsap.matchMedia() context: put animations inside mm.add("(min-width:…)", () => {…})
 *                 so they are reverted automatically on breakpoint change or when motion is disabled.
 *   event         document fires "mulearn:motion-ready" and "mulearn:motion-off"
 */
(function () {
  "use strict";
  var root = document.documentElement;
  var w = window;
  w.MULEARN = w.MULEARN || {};

  var mq = w.matchMedia ? w.matchMedia("(prefers-reduced-motion: reduce)") : { matches: false };
  var state = { ready: false, reduced: !!mq.matches, loading: false, failed: false, mm: null, queue: [] };

  // Where are the vendor files? Resolve relative to this script so any page depth works.
  var me = document.currentScript;
  var base = me && me.src ? me.src.replace(/js\/motion-guard\.js(\?.*)?$/, "") : "";
  var FILES = [base + "vendor/gsap/gsap.min.js", base + "vendor/gsap/ScrollTrigger.min.js"];

  function load(src) {
    return new Promise(function (resolve, reject) {
      var s = document.createElement("script");
      s.src = src; s.async = false;
      s.onload = resolve;
      s.onerror = function () { reject(new Error("motion-guard: failed to load " + src)); };
      document.head.appendChild(s);
    });
  }

  function flush() {
    var q = state.queue.splice(0);
    q.forEach(function (fn) {
      try { fn(w.gsap, w.ScrollTrigger, state.mm); } catch (e) { if (w.console) console.warn("motion-guard: onReady callback failed", e); }
    });
  }

  function enable() {
    if (state.ready || state.loading || state.failed || state.reduced) return;
    state.loading = true;
    load(FILES[0]).then(function () { return load(FILES[1]); }).then(function () {
      if (!w.gsap || !w.ScrollTrigger) throw new Error("motion-guard: GSAP globals missing");
      if (state.reduced) { state.loading = false; return; }          // visitor switched to reduced while loading
      w.gsap.registerPlugin(w.ScrollTrigger);
      state.mm = w.gsap.matchMedia();
      state.ready = true; state.loading = false;
      MOTION.ready = true;
      root.classList.add("js-motion");
      document.dispatchEvent(new CustomEvent("mulearn:motion-ready"));
      flush();
      // pre-motion (hero pre-hide) is released by motion-home once its entrance has taken over; this is only the safety net
      w.setTimeout(function () { root.classList.remove("pre-motion"); }, 0);
    }).catch(function (err) {
      state.failed = true; state.loading = false;
      root.classList.remove("js-motion", "pre-motion");
      if (w.console) console.info(String(err.message || err));       // info, not error: failure is a supported state
    });
  }

  function disable() {
    if (state.mm) { try { state.mm.revert(); } catch (e) {} state.mm = null; }
    if (w.ScrollTrigger) { try { w.ScrollTrigger.getAll().forEach(function (t) { t.kill(); }); } catch (e) {} }
    if (w.gsap) { try { w.gsap.globalTimeline.clear(); } catch (e) {} }
    state.ready = false; MOTION.ready = false;
    root.classList.remove("js-motion", "pre-motion");
    document.dispatchEvent(new CustomEvent("mulearn:motion-off"));
  }

  function onChange(e) {
    state.reduced = e.matches; MOTION.reduced = e.matches;
    if (e.matches) disable(); else enable();
  }

  var MOTION = w.MULEARN.motion = {
    ready: false,
    reduced: state.reduced,
    // Re-measure pending scroll triggers after the page height changed (gallery drawer / filters). Synchronous on purpose:
    // callers refresh BEFORE starting a smooth scroll so the refresh can never cancel it. No-op when motion is off.
    refresh: function () {
      if (!state.ready || !w.ScrollTrigger) return;
      try { w.ScrollTrigger.refresh(); } catch (e) {}
    },
    onReady: function (fn) {
      if (typeof fn !== "function") return;
      if (state.ready) { try { fn(w.gsap, w.ScrollTrigger, state.mm); } catch (e) { if (w.console) console.warn(e); } }
      else state.queue.push(fn);
    }
  };

  root.classList.add("js");            // plain "JS is running" hook (not a hidden-state hook)
  if (mq.addEventListener) mq.addEventListener("change", onChange);
  else if (mq.addListener) mq.addListener(onChange);

  if (!state.reduced) enable();
})();
