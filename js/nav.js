/*!
 * nav.js — header menu + active-section highlight (Phase 3.1). Classic script, namespace MULEARN.nav
 * Progressive enhancement: with JS off the nav is a plain wrapped row of links (CSS keys off html.js).
 * Hooks: [data-js="menu-toggle"] button · [data-js="site-nav"] nav · [data-js="site-header"] header
 */
(function () {
  "use strict";
  var w = window; w.MULEARN = w.MULEARN || {};
  var header = document.querySelector('[data-js="site-header"]');
  var toggle = document.querySelector('[data-js="menu-toggle"]');
  var nav = document.querySelector('[data-js="site-nav"]');
  if (!header || !toggle || !nav) return;

  var DESKTOP = w.matchMedia ? w.matchMedia("(min-width:1180px)") : { matches: false };
  var open = false;

  function setOpen(next, returnFocus) {
    open = !!next && !DESKTOP.matches;
    nav.classList.toggle("is-open", open);
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    if (!open && returnFocus) toggle.focus();
  }

  toggle.addEventListener("click", function () { setOpen(!open); });

  // Escape closes the panel and returns focus to the button (only when focus is inside the header)
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && open) { e.preventDefault(); setOpen(false, true); }
  });
  // Picking a link closes the panel; the browser then performs the anchor jump
  nav.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("a");
    if (a && open) setOpen(false);
  });
  // Keyboard users tabbing out of the open panel/button close it (no trap, no orphaned panel)
  header.addEventListener("focusout", function (e) {
    if (open && e.relatedTarget && !header.contains(e.relatedTarget)) setOpen(false);
  });
  // Tapping outside the header closes it
  document.addEventListener("click", function (e) {
    if (open && !header.contains(e.target)) setOpen(false);
  });
  // Crossing into desktop layout resets state
  var onMq = function () { if (DESKTOP.matches) setOpen(false); };
  if (DESKTOP.addEventListener) DESKTOP.addEventListener("change", onMq); else if (DESKTOP.addListener) DESKTOP.addListener(onMq);

  // ---------- Active-section highlight (only for sections that exist on the page) ----------
  var links = [].slice.call(nav.querySelectorAll('a[href^="#"]'));
  var map = [];
  links.forEach(function (a) {
    var id = a.getAttribute("href").slice(1);
    var el = id && document.getElementById(id);
    if (el && el.tagName !== "SPAN") map.push({ a: a, el: el });
  });
  if (map.length && "IntersectionObserver" in w) {
    var current = null;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        var item = map.filter(function (m) { return m.el === en.target; })[0];
        if (!item) return;
        item.visible = en.isIntersecting;
      });
      var hit = map.filter(function (m) { return m.visible; })[0];
      if (hit !== current) {
        map.forEach(function (m) { m.a.removeAttribute("aria-current"); });
        if (hit) hit.a.setAttribute("aria-current", "true");
        current = hit;
      }
    }, { rootMargin: "-40% 0px -55% 0px", threshold: 0 });
    map.forEach(function (m) { io.observe(m.el); });
  }

  // ---------- Header gets a flat hard shadow once the page has scrolled (class only; no layout change) ----------
  var ticking = false;
  function onScroll() {
    if (ticking) return; ticking = true;
    w.requestAnimationFrame(function () { header.classList.toggle("is-stuck", (w.pageYOffset || 0) > 8); ticking = false; });
  }
  w.addEventListener("scroll", onScroll, { passive: true }); onScroll();

  w.MULEARN.nav = { open: function () { setOpen(true); }, close: function () { setOpen(false); } };
})();
