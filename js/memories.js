/*!
 * memories.js — Community Gallery Drawer, Category Filters & Accessible Lightbox (Phase 7.3 & 7.4).
 * Classic script (defer). Pure vanilla JS, accessible modal dialog, focus trapping,
 * keyboard navigation (Esc, ArrowLeft, ArrowRight), and preloading.
 */
(function () {
  "use strict";

  var memData = window.MULEARN && window.MULEARN.memories;
  var gallery = (memData && memData.gallery) || [];
  var section = document.getElementById("memories");
  if (!section) return;

  var CAT_TONE = {
    "Community": "yellow",
    "Workshops": "mint",
    "Design": "lavender",
    "ODYSSEY": "coral",
    "Buildathon": "coral",
    "Build with AI": "coral",
    "Useless Projects": "coral"
  };

  // ==========================================================================
  // 1. Gallery Drawer Toggle (Subphase 7.3)
  // ==========================================================================
  // Phase 8.2: the drawer/filters change the page height, so pending scroll reveals below are re-measured (no-op without motion).
  // Always called BEFORE a smooth scroll starts so it can never cancel it. Reduced motion = instant scroll.
  function relayout() {
    var M = window.MULEARN && window.MULEARN.motion;
    if (M && typeof M.refresh === "function") M.refresh();
  }
  var reducedMq = window.matchMedia ? window.matchMedia("(prefers-reduced-motion: reduce)") : { matches: false };

  var toggleBtn = document.getElementById("memories-gallery-toggle");
  var drawer = document.getElementById("memories-gallery");
  var toggleText = toggleBtn ? toggleBtn.querySelector(".memories__toggle-text") : null;

  if (toggleBtn && drawer) {
    toggleBtn.addEventListener("click", function () {
      var isExpanded = toggleBtn.getAttribute("aria-expanded") === "true";
      var nextState = !isExpanded;

      toggleBtn.setAttribute("aria-expanded", String(nextState));
      drawer.hidden = !nextState;

      if (toggleText) {
        toggleText.textContent = nextState
          ? "Hide gallery"
          : "View full gallery (11 photos)";
      }

      relayout();
      if (nextState) {
        drawer.scrollIntoView({ behavior: reducedMq.matches ? "auto" : "smooth", block: "start" });
      }
    });
  }

  // ==========================================================================
  // 2. Category Filtering (Subphase 7.3)
  // ==========================================================================
  var filterBtns = section.querySelectorAll(".gallery-filter");
  var cards = section.querySelectorAll(".gallery-card");

  if (filterBtns.length && cards.length) {
    filterBtns.forEach(function (btn) {
      btn.addEventListener("click", function () {
        var filter = btn.getAttribute("data-filter");

        filterBtns.forEach(function (b) {
          var active = b === btn;
          b.setAttribute("aria-pressed", String(active));
          b.classList.toggle("is-active", active);
        });

        cards.forEach(function (card) {
          var cardCat = card.getAttribute("data-category");
          var match = filter === "all" || cardCat === filter;
          card.hidden = !match;
        });
        relayout();
        // 8.4: announce the result of a filter change (the grid change itself is silent for screen readers)
        var status = document.getElementById("gallery-status");
        if (status) {
          var n = 0;
          cards.forEach(function (c) { if (!c.hidden) n++; });
          status.textContent = "Showing " + n + (n === 1 ? " photo" : " photos") + (filter === "all" ? "" : " in " + btn.textContent.replace(/\s*\(\d+\)\s*$/, ""));
        }
      });
    });
  }

  // ==========================================================================
  // 3. Reusable Accessible Lightbox (Subphase 7.4)
  // ==========================================================================
  var dlg = document.getElementById("memories-lightbox");
  if (!dlg || !gallery.length) return;

  var panel = dlg.querySelector(".lightbox-dialog__panel");
  var imgEl = dlg.querySelector("#lightbox-image");
  var titleEl = dlg.querySelector("#lightbox-title");
  var captionEl = dlg.querySelector("#lightbox-caption");
  var counterEl = dlg.querySelector("#lightbox-counter");
  var mobCounterEl = dlg.querySelector("#lightbox-mob-counter");
  var catEl = dlg.querySelector("#lightbox-category");
  var dimsEl = dlg.querySelector("#lightbox-dims");
  var closeBtn = dlg.querySelector("#lightbox-close");
  var prevBtn = dlg.querySelector("#lightbox-prev");
  var nextBtn = dlg.querySelector("#lightbox-next");
  var mobPrevBtn = dlg.querySelector("#lightbox-mob-prev");
  var mobNextBtn = dlg.querySelector("#lightbox-mob-next");

  var currentIndex = 0;
  var lastTrigger = null;

  // Build ID lookup maps
  var byId = {};
  var indexOf = {};
  gallery.forEach(function (g, idx) {
    byId[g.id] = g;
    indexOf[g.id] = idx;
  });

  function preloadAdjacent(idx) {
    var prev = gallery[(idx - 1 + gallery.length) % gallery.length];
    var next = gallery[(idx + 1) % gallery.length];
    if (prev && prev.src) { var p = new Image(); p.src = prev.src; }
    if (next && next.src) { var n = new Image(); n.src = next.src; }
  }

  function showPhoto(idx) {
    currentIndex = (idx + gallery.length) % gallery.length;
    var item = gallery[currentIndex];
    if (!item) return;

    if (imgEl) {
      // 8.4: until the new photo has decoded, dim the old one (it would otherwise sit under the new caption); the
      // frame size is fixed by width/height so nothing shifts. Only the latest request may clear the state.
      imgEl.classList.add("is-loading");
      imgEl.onload = imgEl.onerror = function () { imgEl.classList.remove("is-loading"); };
      imgEl.src = item.src;
      imgEl.alt = item.title;
      imgEl.width = item.width;
      imgEl.height = item.height;
      if (imgEl.complete) imgEl.classList.remove("is-loading");
    }
    if (titleEl) titleEl.textContent = item.title;
    if (captionEl) captionEl.textContent = item.caption;
    if (counterEl) counterEl.textContent = "Photo " + (currentIndex + 1) + " of " + gallery.length;
    if (mobCounterEl) mobCounterEl.textContent = (currentIndex + 1) + " / " + gallery.length;
    if (catEl) {
      catEl.textContent = item.category;
      var tone = CAT_TONE[item.category] || "neutral";
      catEl.className = "tag tag--sm tag--" + tone;
    }
    if (dimsEl) dimsEl.textContent = item.width + " × " + item.height + " px";

    preloadAdjacent(currentIndex);
  }

  function openLightbox(id, trigger) {
    lastTrigger = trigger || document.activeElement;
    var idx = indexOf[id];
    if (idx == null) idx = 0;
    showPhoto(idx);

    if (typeof dlg.showModal === "function") {
      dlg.showModal();
    } else {
      dlg.setAttribute("open", "");
    }

    if (panel) panel.scrollTop = 0;   // 8.4: same guarantee as the event dialog — every opening starts at the top
    if (closeBtn) closeBtn.focus();
  }

  function closeLightbox() {
    if (typeof dlg.close === "function") {
      dlg.close();
    } else {
      dlg.removeAttribute("open");
    }

    if (lastTrigger && typeof lastTrigger.focus === "function") {
      lastTrigger.focus();
    }
  }

  if (closeBtn) closeBtn.addEventListener("click", closeLightbox);
  if (prevBtn) prevBtn.addEventListener("click", function () { showPhoto(currentIndex - 1); });
  if (nextBtn) nextBtn.addEventListener("click", function () { showPhoto(currentIndex + 1); });
  if (mobPrevBtn) mobPrevBtn.addEventListener("click", function () { showPhoto(currentIndex - 1); });
  if (mobNextBtn) mobNextBtn.addEventListener("click", function () { showPhoto(currentIndex + 1); });

  // Keyboard navigation inside lightbox
  dlg.addEventListener("keydown", function (e) {
    if (e.key === "ArrowLeft") {
      e.preventDefault();
      showPhoto(currentIndex - 1);
    } else if (e.key === "ArrowRight") {
      e.preventDefault();
      showPhoto(currentIndex + 1);
    }
  });

  // Backdrop click to close
  dlg.addEventListener("click", function (e) {
    if (!panel) return;
    // 8.5: only a click that lands on the dialog element itself (the backdrop) can be a "click outside". Clicks on the
    // controls inside — including keyboard/Space/Enter activation, which reports coordinates (0,0) — must never close it.
    if (e.target !== dlg) return;
    var rect = panel.getBoundingClientRect();
    var inDialog =
      rect.top <= e.clientY && e.clientY <= rect.top + rect.height &&
      rect.left <= e.clientX && e.clientX <= rect.left + rect.width;
    if (!inDialog) closeLightbox();
  });

  // Global delegation for opening lightbox from both collage and gallery buttons
  document.addEventListener("click", function (e) {
    var btn = e.target.closest("[data-lightbox-open]");
    if (btn) {
      e.preventDefault();
      var id = btn.getAttribute("data-lightbox-open");
      openLightbox(id, btn);
    }
  });
})();
