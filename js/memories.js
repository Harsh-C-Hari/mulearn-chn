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

      if (nextState) {
        drawer.scrollIntoView({ behavior: "smooth", block: "start" });
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
      imgEl.src = item.src;
      imgEl.alt = item.title;
      imgEl.width = item.width;
      imgEl.height = item.height;
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
