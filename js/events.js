/*!
 * events.js — accessible event-detail dialog (Phase 5.4). Classic script (defer). Needs data/events.js.
 * One reusable native <dialog id="event-dialog">; every [data-event-open="<slug>"] button fills it from window.MULEARN.events.
 * Safe rendering: only createElement + textContent (no innerHTML). Unknown fields are never rendered; `open` notes are internal.
 * Keyboard: Esc / Close button / backdrop click close it; Tab is trapped inside; focus returns to the trigger.
 * Motion: restrained GSAP via window.MULEARN.motion when allowed; nothing depends on it (reduced motion / no GSAP = instant).
 */
(function () {
  "use strict";
  var data = (window.MULEARN && window.MULEARN.events) || [];
  var dlg = document.getElementById("event-dialog");
  if (!dlg || !data.length) return;
  var byslug = {};
  data.forEach(function (e) { byslug[e.slug] = e; });
  if (typeof dlg.showModal !== "function") { document.documentElement.classList.add("no-dialog"); return; }  // buttons are hidden by CSS

  var panel = dlg.querySelector(".event-dialog__panel");
  var closeBtn = dlg.querySelector(".event-dialog__close");
  var posterWrap = dlg.querySelector(".event-dialog__poster");
  var titleEl = dlg.querySelector("#event-dialog-title");
  var descEl = dlg.querySelector("#event-dialog-desc");
  var bodyEl = dlg.querySelector(".event-dialog__sections");
  var lastTrigger = null, closing = false, downOnBackdrop = false;

  function h(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null && text !== "") n.textContent = text;
    return n;
  }
  function dl(facts) {
    var d = h("dl", "event-dialog__facts");
    facts.forEach(function (f) {
      var row = h("div", "event-dialog__fact");
      row.appendChild(h("dt", "", f.label));
      row.appendChild(h("dd", "", f.value));
      d.appendChild(row);
    });
    return d;
  }
  function section(title) {
    var s = h("section", "event-dialog__block");
    if (title) s.appendChild(h("h3", "event-dialog__h", title));
    return s;
  }

  function render(e) {
    titleEl.textContent = e.title;
    descEl.textContent = e.blurb || e.descriptor || "";
    dlg.setAttribute("data-tone", e.tone || "lavender");
    // poster (whole, never cropped)
    posterWrap.textContent = "";
    var p = e.image && e.image.poster;
    if (p) {
      var img = h("img");
      img.src = p.src; img.width = p.width; img.height = p.height; img.alt = e.image.alt || ""; img.decoding = "async";
      posterWrap.appendChild(img);
    }
    bodyEl.textContent = "";
    if (e.printed && e.printed !== descEl.textContent) {
      var pr = h("p", "event-dialog__printed");
      pr.appendChild(h("span", "event-dialog__printed-label", "As printed on the poster"));
      pr.appendChild(h("q", "", e.printed));
      bodyEl.appendChild(pr);
    }
    if (e.facts && e.facts.length) { var s0 = section("Details"); s0.appendChild(dl(e.facts)); bodyEl.appendChild(s0); }
    (e.parts || []).forEach(function (part) {
      var s = section(part.title); s.appendChild(dl(part.facts)); bodyEl.appendChild(s);
    });
    (e.lists || []).forEach(function (l) {
      if (!l.items || !l.items.length) return;
      var s = section(l.label), ul = h("ul", "event-dialog__list");
      ul.setAttribute("role", "list");
      l.items.forEach(function (it) {
        var li = h("li");
        if (it.role) li.appendChild(h("span", "event-dialog__role", it.role));
        li.appendChild(h("strong", "", it.name));
        ul.appendChild(li);
      });
      s.appendChild(ul); bodyEl.appendChild(s);
    });
    if (e.branding && e.branding.length) {
      var sb = section("Branding on the poster"), tl = h("ul", "tag-list"); tl.setAttribute("role", "list");
      e.branding.forEach(function (b) { var li = h("li"); li.appendChild(h("span", "tag", b)); tl.appendChild(li); });
      sb.appendChild(tl); bodyEl.appendChild(sb);
    }
    if (e.photos && e.photos.length) {
      var sp = section("From the event"), wrap = h("div", "event-dialog__photos");
      e.photos.forEach(function (ph) {
        var f = h("figure", "event-dialog__photo"), im = h("img");
        im.src = ph.src; im.width = ph.width; im.height = ph.height; im.alt = ph.alt || ""; im.decoding = "async";
        f.appendChild(im); wrap.appendChild(f);
      });
      sp.appendChild(wrap); bodyEl.appendChild(sp);
    }
    if (e.dialogNote) bodyEl.appendChild(h("p", "event-dialog__note", e.dialogNote));
    panel.scrollTop = 0;
  }

  function canAnimate() {
    var M = window.MULEARN && window.MULEARN.motion;
    return !!(M && M.ready && !M.reduced && window.gsap);
  }

  function open(slug, trigger) {
    var e = byslug[slug];
    if (!e || dlg.open) return;
    lastTrigger = trigger || document.activeElement;
    closing = false;
    render(e);
    dlg.classList.remove("is-closing");
    dlg.showModal();
    if (canAnimate()) {
      window.gsap.fromTo(panel, { y: 28, opacity: 0 }, { y: 0, opacity: 1, duration: .35, ease: "power3.out", clearProps: "transform,opacity" });
    }
  }

  function finish() {
    if (dlg.open) dlg.close();
    dlg.classList.remove("is-closing");
    closing = false;
    if (lastTrigger && document.contains(lastTrigger) && typeof lastTrigger.focus === "function") lastTrigger.focus();
  }
  function requestClose() {
    if (!dlg.open || closing) return;
    closing = true;
    if (canAnimate()) {
      dlg.classList.add("is-closing");
      window.gsap.to(panel, { y: 16, opacity: 0, duration: .2, ease: "power2.in", onComplete: function () { window.gsap.set(panel, { clearProps: "transform,opacity" }); finish(); } });
    } else finish();
  }

  // open from any trigger (delegated so it works for all seven)
  document.addEventListener("click", function (ev) {
    var b = ev.target.closest && ev.target.closest("[data-event-open]");
    if (b) { ev.preventDefault(); open(b.getAttribute("data-event-open"), b); }
  });
  closeBtn.addEventListener("click", requestClose);
  dlg.addEventListener("cancel", function (ev) { ev.preventDefault(); requestClose(); });   // Esc
  dlg.addEventListener("pointerdown", function (ev) { downOnBackdrop = ev.target === dlg; });
  dlg.addEventListener("click", function (ev) { if (ev.target === dlg && downOnBackdrop) requestClose(); downOnBackdrop = false; });
  dlg.addEventListener("close", function () { closing = false; dlg.classList.remove("is-closing"); });
  // Tab trap (native modal already makes the page inert; this keeps focus off the browser UI)
  dlg.addEventListener("keydown", function (ev) {
    if (ev.key !== "Tab") return;
    var f = [].filter.call(dlg.querySelectorAll("a[href],button:not([disabled]),[tabindex]:not([tabindex='-1'])"), function (n) { return n.offsetParent !== null || n === document.activeElement; });
    if (!f.length) return;
    var first = f[0], last = f[f.length - 1];
    if (ev.shiftKey && document.activeElement === first) { ev.preventDefault(); last.focus(); }
    else if (!ev.shiftKey && document.activeElement === last) { ev.preventDefault(); first.focus(); }
  });
})();
