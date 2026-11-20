/*!
 * motion-home.js — header / hero / About motion (Phase 3.5). Classic script; talks only to MULEARN.motion.
 * Rules (Master Spec §12, brief §3.5): subtle, once-only, transform+opacity only (no layout shift), no scroll hijack,
 * nothing hidden in CSS — start states are applied here, and only after GSAP + ScrollTrigger registered and the visitor
 * allows motion. Everything lives inside mm.add(), so a reduced-motion switch reverts it and leaves content visible.
 */
(function () {
  "use strict";
  var M = window.MULEARN && window.MULEARN.motion;
  if (!M) return;

  M.onReady(function (gsap, ScrollTrigger, mm) {
    if (!gsap || !ScrollTrigger || !mm) return;

    mm.add("(prefers-reduced-motion: no-preference)", function () {
      var q = function (sel, root) { return [].slice.call((root || document).querySelectorAll(sel)); };
      var EASE = "power3.out";

      // ---------------- Hero entrance (plays once, on load) ----------------
      var hero = document.getElementById("hero");
      if (hero) {
        var lines = q(".hero__title span", hero);
        var tl = gsap.timeline({ defaults: { ease: EASE }, onComplete: function () {
          gsap.set(q(".hero__title span, .hero__intro > *, .hero__actions > *, .hero__discord, .hero__figure, .hero .sticker > svg", hero), { clearProps: "opacity,visibility,transform" });
        }});
        tl.from(lines, { yPercent: 70, opacity: 0, duration: .8, stagger: .12 }, .05)
          .from(q(".hero__intro > *", hero), { y: 24, opacity: 0, duration: .6, stagger: .08 }, .45)
          .from(q(".hero__actions > *, .hero__discord", hero), { y: 20, opacity: 0, duration: .5, stagger: .07 }, .65)
          .from(q(".hero__figure", hero), { y: 56, opacity: 0, rotation: "+=4", duration: .9 }, .25)
          .from(q(".hero .sticker > svg", hero), { scale: 0, rotation: -40, transformOrigin: "50% 50%", duration: .6, ease: "back.out(2)", stagger: .07 }, .6);
      }

      // ---------------- About reveal (once, when it scrolls into view) ----------------
      var about = document.getElementById("about");
      if (about) {
        var at = gsap.timeline({ defaults: { ease: EASE }, paused: true, onComplete: function () {
          gsap.set(q(".about__card, .about__pair .card, .about__facts, .about__actions, .about__figure, .about .sticker > svg", about), { clearProps: "opacity,visibility,transform" });
        }});
        at.from(q(".about__card", about), { y: 48, opacity: 0, duration: .8 }, 0)
          .from(q(".about__pair .card", about), { y: 28, opacity: 0, duration: .55, stagger: .1 }, .35)
          .from(q(".about__facts, .about__actions", about), { y: 16, opacity: 0, duration: .45, stagger: .08 }, .6)
          .from(q(".about__figure", about), { y: 64, opacity: 0, rotation: "-=5", duration: .9 }, .2)
          .from(q(".about .sticker > svg", about), { scale: 0, rotation: 30, transformOrigin: "50% 50%", duration: .55, ease: "back.out(2)", stagger: .08 }, .7);
        ScrollTrigger.create({ trigger: about, start: "top 75%", once: true, onEnter: function () { at.play(); } });
      }
    });
  });
})();
