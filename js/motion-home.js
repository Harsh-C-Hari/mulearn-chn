/*!
 * motion-home.js — page reveal system (Phase 3.5 → standardised in Phase 8.2). Classic script; talks only to MULEARN.motion.
 * Rules (Master Spec §12): subtle, once-only, transform + opacity only (no layout shift), no scroll hijack, nothing hidden in
 * CSS (the hero's brief pre-hide is the one guarded exception, see index.html head), start states are applied here and only
 * after GSAP + ScrollTrigger registered and the visitor allows motion. Everything lives inside mm.add(), so a reduced-motion
 * switch reverts it and leaves content visible.
 *
 * One vocabulary for every section (change a value in T and the whole page follows):
 *   intro(section, steps, stickers)  one timeline per section: heading group → blocks → stickers, fired once at T.headStart
 *   rise(elements)                   items that enter on their own as they approach the viewport (T.itemStart), once each
 *   stickers always pop the same way (T.pop); text rises T.riseSm, blocks/figures/cards rise T.rise.
 */
(function () {
  "use strict";
  var M = window.MULEARN && window.MULEARN.motion;
  if (!M) return;
  var root = document.documentElement;

  M.onReady(function (gsap, ScrollTrigger, mm) {
    if (!gsap || !ScrollTrigger || !mm) { root.classList.remove("pre-motion"); return; }

    mm.add("(prefers-reduced-motion: no-preference)", function () {
      var q = function (sel, ctx) { return [].slice.call((ctx || document).querySelectorAll(sel)); };

      // ---------------- shared motion tokens ----------------
      var T = {
        ease: "power3.out",
        dur: .7, durSm: .5,           // blocks / text
        rise: 48, riseSm: 24,         // px travelled (transform only)
        stagger: .08,
        headStart: "top 80%",         // a section's own timeline
        itemStart: "top 90%",         // individual cards / panels
        footStart: "top 92%",
        popAt: .3,                    // stickers join the section timeline here
        pop: { scale: 0, rotation: 30, transformOrigin: "50% 50%", duration: .5, ease: "back.out(1.6)", stagger: .06 }
      };
      var CLEAR = "opacity,visibility,transform";
      var clear = function (els) { if (els.length) gsap.set(els, { clearProps: CLEAR }); };

      // One timeline per section. steps: [{ sel, y, d, stagger, rot, yPercent, at }]; all start states removed on completion.
      function intro(sec, steps, stickerSel, start) {
        var all = [];
        var tl = gsap.timeline({ defaults: { ease: T.ease }, paused: true, onComplete: function () { clear(all); } });
        steps.forEach(function (s) {
          var els = q(s.sel, sec);
          if (!els.length) return;
          all = all.concat(els);
          var v = { opacity: 0, duration: s.d || T.durSm, stagger: s.stagger || 0 };
          if (s.yPercent != null) v.yPercent = s.yPercent; else v.y = s.y == null ? T.riseSm : s.y;
          if (s.rot) v.rotation = s.rot;
          tl.from(els, v, s.at || 0);
        });
        var st = stickerSel ? q(stickerSel, sec) : [];
        if (st.length) {
          all = all.concat(st);
          tl.from(st, { scale: 0, rotation: T.pop.rotation, transformOrigin: T.pop.transformOrigin, duration: T.pop.duration, ease: T.pop.ease, stagger: T.pop.stagger }, T.popAt);
        }
        // fire once, then remove the trigger immediately (`once` alone only kills it when its END is reached,
        // which never happens for sections near the bottom of the page)
        ScrollTrigger.create({ trigger: sec, start: start || T.headStart, once: true, onEnter: function (self) { tl.play(); self.kill(); } });
        return tl;
      }

      // Items that rise on their own as they near the viewport (so lower cards are never animated off-screen).
      function rise(els, y) {
        els.forEach(function (el) {
          var tw = gsap.from(el, { y: y == null ? T.rise : y, opacity: 0, duration: T.dur, ease: T.ease, clearProps: CLEAR, paused: true });
          ScrollTrigger.create({ trigger: el, start: T.itemStart, once: true, onEnter: function (self) { tw.play(); self.kill(); } });
        });
      }

      // ---------------- Hero entrance (plays once, on load) ----------------
      // Only when the pre-hide is still active: if GSAP arrived after the 1.2 s release the hero is already on screen and is left alone
      // (an entrance then would hide visible content).
      var hero = document.getElementById("hero");
      if (hero && root.classList.contains("pre-motion")) {
        var heroEls = q(".hero__title span, .hero__intro > *, .hero__actions > *, .hero__discord, .hero__figure, .hero .sticker > svg", hero);
        // lazy:false → the start states are written to the elements synchronously, so releasing the CSS pre-hide on the next
        // line can never expose a frame of un-hidden content (GSAP otherwise defers from() start states to its next tick).
        var tl = gsap.timeline({ defaults: { ease: T.ease, lazy: false }, onComplete: function () { clear(heroEls); } });
        tl.from(q(".hero__title span", hero), { yPercent: 70, opacity: 0, duration: T.dur + .1, stagger: .12 }, .05)
          .from(q(".hero__figure", hero), { y: T.rise + 8, opacity: 0, rotation: "+=4", duration: .9 }, .25)
          .from(q(".hero__intro > *", hero), { y: T.riseSm, opacity: 0, duration: .6, stagger: T.stagger }, .45)
          .from(q(".hero__actions > *, .hero__discord", hero), { y: T.riseSm, opacity: 0, duration: T.durSm, stagger: T.stagger }, .65)
          .from(q(".hero .sticker > svg", hero), { scale: 0, rotation: -T.pop.rotation, transformOrigin: T.pop.transformOrigin, duration: T.pop.duration, ease: T.pop.ease, stagger: T.pop.stagger }, .6);
      }
      root.classList.remove("pre-motion");   // start states are now inline (GSAP), so the CSS pre-hide can go

      // ---------------- About ----------------
      var about = document.getElementById("about");
      if (about) {
        intro(about, [
          { sel: ".about__card", y: T.rise, d: T.dur },
          { sel: ".about__figure", y: T.rise, d: T.dur, rot: "-=5", at: .2 },
          { sel: ".about__pair .card", stagger: T.stagger, at: .35 },
          { sel: ".about__facts, .about__actions", stagger: T.stagger, at: .6 }
        ], ".about .sticker > svg");
      }

      // ---------------- Offers ----------------
      var offers = document.getElementById("offers");
      if (offers) {
        intro(offers, [
          { sel: ".offers__head > *", stagger: .1 },
          { sel: ".offers__note", at: .9 }
        ], ".offers .sticker > svg");
        rise(q(".offer__card", offers));
      }

      // ---------------- Events ----------------
      var events = document.getElementById("events");
      if (events) {
        intro(events, [{ sel: ".events__head > *", stagger: .1 }], ".events .sticker > svg");
        rise(q(".event--featured .event-card", events));
      }

      // ---------------- Team (the 21-entry directory enters as ONE block, never entry by entry) ----------------
      var team = document.getElementById("team");
      if (team) {
        intro(team, [{ sel: ".team__head > *", stagger: .1 }], ".team > .sticker > svg, .member-card__stk > svg");
        rise(q(".team__featured .member-card", team));
        rise(q(".roster-panel", team));
      }

      // ---------------- Memories ----------------
      var memories = document.getElementById("memories");
      if (memories) {
        intro(memories, [
          { sel: ".memories__head > *", stagger: .1 },
          { sel: ".memories__actions", at: .7 }
        ], ".memories > .sticker > svg");
        rise(q(".memories__collage .polaroid", memories));
      }

      // ---------------- Join ----------------
      var join = document.getElementById("join");
      if (join) {
        intro(join, [
          { sel: ".join__banner", y: T.rise, d: T.dur },
          { sel: ".join__step", stagger: .12, at: .35 },
          { sel: ".join__ctas > *", stagger: .1, at: .6 }
        ], ".join .sticker > svg");
      }

      // ---------------- Footer ----------------
      var foot = document.querySelector(".site-footer");
      if (foot) {
        intro(foot, [
          { sel: ".footer__big span", yPercent: 60, d: T.dur, stagger: .1 },
          { sel: ".footer__grid > *", stagger: .1, at: .3 },
          { sel: ".footer__bar", y: 12, d: .4, at: .6 }
        ], ".site-footer .sticker > svg", T.footStart);
      }
    });
  });
})();
