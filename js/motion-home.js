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

      // ---------------- Offers reveal (once, when it scrolls into view) ----------------
      var offers = document.getElementById("offers");
      if (offers) {
        var cards = q(".offer__card", offers);
        var ot = gsap.timeline({ defaults: { ease: EASE }, paused: true, onComplete: function () {
          gsap.set(q(".offers__head > *, .offer__card, .offers__note, .offers .sticker > svg", offers), { clearProps: "opacity,visibility,transform" });
        }});
        ot.from(q(".offers__head > *", offers), { y: 32, opacity: 0, duration: .65, stagger: .1 }, 0)
          .from(q(".offers .sticker > svg", offers), { scale: 0, rotation: 30, transformOrigin: "50% 50%", duration: .55, ease: "back.out(2)", stagger: .05 }, .35)
          .from(q(".offers__note", offers), { y: 24, opacity: 0, duration: .5 }, .9);
        ScrollTrigger.create({ trigger: offers, start: "top 70%", once: true, onEnter: function () { ot.play(); } });
        // each card reveals as it nears the viewport (so lower cards are not animated off-screen)
        cards.forEach(function (c) {
          gsap.from(c, { y: 56, opacity: 0, duration: .8, ease: EASE, scrollTrigger: { trigger: c, start: "top 88%", once: true }, clearProps: "opacity,visibility,transform" });
        });
      }
      // ---------------- Events reveal (once; transform + opacity only, nothing is hidden in CSS) ----------------
      var events = document.getElementById("events");
      if (events) {
        var et = gsap.timeline({ defaults: { ease: EASE }, paused: true, onComplete: function () {
          gsap.set(q(".events__head > *, .events .sticker > svg", events), { clearProps: "opacity,visibility,transform" });
        }});
        et.from(q(".events__head > *", events), { y: 32, opacity: 0, duration: .65, stagger: .1 }, 0)
          .from(q(".events .sticker > svg", events), { scale: 0, rotation: 30, transformOrigin: "50% 50%", duration: .55, ease: "back.out(2)", stagger: .05 }, .35);
        ScrollTrigger.create({ trigger: events, start: "top 70%", once: true, onEnter: function () { et.play(); } });
        // each event card rises as it nears the viewport (staggered naturally by its position)
        q(".event--featured .event-card", events).forEach(function (c) {
          gsap.from(c, { y: 56, opacity: 0, duration: .8, ease: EASE, scrollTrigger: { trigger: c, start: "top 88%", once: true }, clearProps: "opacity,visibility,transform" });
        });
      }
      // ---------------- Join reveal (once) ----------------
      var join = document.getElementById("join");
      if (join) {
        var jt = gsap.timeline({ defaults: { ease: EASE }, paused: true, onComplete: function () {
          gsap.set(q(".join__banner, .join__step, .join__ctas > *, .join .sticker > svg", join), { clearProps: "opacity,visibility,transform" });
        }});
        jt.from(q(".join__banner", join), { y: 56, opacity: 0, duration: .8 }, 0)
          .from(q(".join__step", join), { y: 24, opacity: 0, duration: .5, stagger: .12 }, .35)
          .from(q(".join__ctas > *", join), { y: 20, opacity: 0, duration: .45, stagger: .1 }, .6)
          .from(q(".join .sticker > svg", join), { scale: 0, rotation: 30, transformOrigin: "50% 50%", duration: .55, ease: "back.out(2)", stagger: .08 }, .7);
        ScrollTrigger.create({ trigger: join, start: "top 70%", once: true, onEnter: function () { jt.play(); } });
      }
      // ---------------- Footer reveal (once) ----------------
      var foot = document.querySelector(".site-footer");
      if (foot) {
        var ft = gsap.timeline({ defaults: { ease: EASE }, paused: true, onComplete: function () {
          gsap.set(q(".footer__big span, .footer__grid > *, .footer__bar, .site-footer .sticker > svg", foot), { clearProps: "opacity,visibility,transform" });
        }});
        ft.from(q(".footer__big span", foot), { yPercent: 60, opacity: 0, duration: .7, stagger: .1 }, 0)
          .from(q(".footer__grid > *", foot), { y: 24, opacity: 0, duration: .5, stagger: .1 }, .3)
          .from(q(".footer__bar", foot), { y: 12, opacity: 0, duration: .4 }, .6)
          .from(q(".site-footer .sticker > svg", foot), { scale: 0, rotation: 30, transformOrigin: "50% 50%", duration: .5, ease: "back.out(2)", stagger: .06 }, .5);
        ScrollTrigger.create({ trigger: foot, start: "top 85%", once: true, onEnter: function () { ft.play(); } });
      }
    });
  });
})();
