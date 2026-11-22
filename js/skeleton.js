/* ==========================================================================
   skeleton.js — themed image skeletons (µLearn CHN)
   Attaches a decorative overlay (<span class="skel" aria-hidden="true">) to an
   image's existing host while the image loads. Nothing is required in the HTML,
   so the generated markup (build_events/team/memories) is untouched.
     • already-loaded / cached image  → no overlay at all
     • lazy / slow image              → overlay until `load`
     • failed image                   → static "failed" overlay (never an endless loader)
     • lightbox / event dialog        → handled when `src` changes / nodes are inserted
   The overlay is a sibling of the <img>: it never gates, delays or alters it.
   Without JS (html.no-js) nothing runs and images behave exactly as before.
   ========================================================================== */
(function () {
  "use strict";
  var root = document.documentElement;
  if (root.classList.contains("no-js") || !document.querySelectorAll) return;

  var VARIANTS = [];      // [selector, name] — first match wins
  var TEMPLATES = {};     // name → static SVG markup (flat shapes + sprite <use>)
  var FAILED = '<svg class="skel__ico" viewBox="0 0 24 24" focusable="false" aria-hidden="true"><use href="#i-image"/></svg>';

  /* register(name, selector, viewBox, shapes) */
  function V(name, selector, vb, shapes) {
    VARIANTS.push([selector, name]);
    TEMPLATES[name] = '<svg viewBox="' + vb + '" preserveAspectRatio="xMidYMid slice" focusable="false" aria-hidden="true">' + shapes + '</svg>';
  }
  /* sprite shape helper: <use> positioned in viewBox units */
  function U(id, x, y, s, cls, a) {
    return '<use href="#' + id + '" x="' + x + '" y="' + y + '" width="' + s + '" height="' + s + '" class="' + cls + '"' + (a === "w" ? ' data-w="1"' : a ? ' data-a="' + a + '"' : '') + '/>';
  }

  /* variants:start */
  /* Board-mix language (5.1): Board 1 = colour-blocked tints, tilted frames, sparkle/asterisk stickers;
     Board 2 = heavy navy shapes + hard offset shadows. Large surfaces stay cream; colour is a tint (class tn*, never a gradient),
     strong colour only on small accents (a1/a2/a3, data-a = breathes), stickers tilt gently (data-w). */
  /* F(): a frame with a hard offset shadow (flat navy rect behind, no blur) + keyline */
  function F(x, y, w, h, fill, o) {
    var g = ' x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '"';
    return '<rect class="ik" x="' + (x + o) + '" y="' + (y + o) + '" width="' + w + '" height="' + h + '"/>' +
           '<rect class="cr"' + g + '/>' +                                  // opaque cream base: tints are translucent and must not show the shadow
           (fill === "cr" ? "" : '<rect class="' + fill + '"' + g + '/>') +
           '<rect class="ln"' + g + '/>';
  }
  /* tape strip (polaroid / paste-up motif) */
  function T(x, y, w, rot, a) {
    return '<rect class="a1" x="' + x + '" y="' + y + '" width="' + w + '" height="6" transform="rotate(' + rot + ' ' + (x + w / 2) + ' ' + (y + 3) + ')"' + (a ? ' data-a="' + a + '"' : '') + '/>';
  }
  var SIL_HEAD = '<circle class="ik" cx="52.5" cy="49.5" r="17"/><circle class="sh" cx="50" cy="47" r="17"/><circle class="ln" cx="50" cy="47" r="17"/>';
  var SIL_BODY = '<path class="ik" transform="translate(2.5 2.5)" d="M14 120C14 92 30 74 50 74S86 92 86 120Z"/>' +
                 '<path class="sh" d="M14 120C14 92 30 74 50 74S86 92 86 120Z"/><path class="ln" d="M14 120C14 92 30 74 50 74S86 92 86 120"/>';
  var crowd = '';
  for (var r = 0; r < 3; r++) for (var c = 3; c < 13; c++) crowd += '<circle class="ik dim" cx="' + (4 + c * 7.8 + (r % 2) * 3.9) + '" cy="' + (67 + r * 8) + '" r="2.3"/>';

  /* A · hero — an auditorium paste-up: stage screen with hard shadow, audience dots, spotlight, navy quarter, stickers */
  V("hero", ".hero__figure img", "0 0 100 90",
    '<rect class="sh" x="0" y="58" width="100" height="32"/>' + crowd + '<path class="ln" d="M0 58H100"/>' +
    '<g class="hide-sm">' + F(10, 15, 46, 29, "tn3", 2.2) + '<rect class="a1" data-a="1" x="15" y="20" width="13" height="4"/><rect class="ik dim" x="15" y="28" width="30" height="3"/><rect class="ik dim" x="15" y="34" width="20" height="3"/></g>' +
    '<circle class="a1" cx="76" cy="26" r="12"/><circle class="ln" cx="76" cy="26" r="12"/>' +
    U("s-quarter", 0, 64, 26, "ik", 0) +
    U("s-asterisk", 30, 71, 15, "a3 ol", "w") + U("s-sparkle", 82, 42, 13, "ik", "w"));

  /* B · about — projector screen with hard shadow on a tinted wall, heavy navy bar (board 2) with a mint chip, sparkle sticker */
  V("about", ".about__figure img", "0 0 100 115",
    '<rect class="tn2" x="0" y="0" width="100" height="100"/>' +
    F(12, 14, 74, 46, "wh", 3) + '<rect class="tn3" x="19" y="21" width="30" height="32"/><rect class="ik dim" x="55" y="23" width="24" height="4"/><rect class="ik dim" x="55" y="32" width="18" height="4"/>' +
    '<path class="ln" d="M49 60V84M33 84H65"/>' +
    '<rect class="ik" x="0" y="98" width="100" height="17"/>' +
    '<circle class="a2" data-a="1" cx="84" cy="106.5" r="3.6"/><circle class="cr" cx="72" cy="106.5" r="2.2"/><circle class="cr" cx="63" cy="106.5" r="2.2"/>' +
    U("s-sparkle", 76, 2, 20, "a1 ol", "w"));

  /* C1 · event poster — heavy title bar + yellow chip, tinted art field (card colour) with white disc, navy quarter, tilted star sticker */
  V("poster", ".event-card__poster img", "0 0 100 120",
    '<rect class="ik" x="10" y="11" width="54" height="11"/><rect class="a1" data-a="1" x="70" y="11" width="20" height="11"/><rect class="ln" x="70" y="11" width="20" height="11"/>' +
    F(10, 30, 80, 54, "tn3", 3) + '<circle class="wh" cx="54" cy="53" r="14"/><circle class="ln" cx="54" cy="53" r="14"/>' + U("s-quarter", 10, 62, 22, "ik", 0) +
    '<path class="ln" d="M6 30v-4h4M94 30v-4h-4M6 84v4h4M94 84v4h-4"/>' +
    '<rect class="sh" x="10" y="95" width="52" height="4"/><rect class="sh" x="10" y="103" width="34" height="4"/>' +
    '<path class="ln hide-sm" d="M97 36h3M97 44h3M97 52h3M97 60h3M97 68h3M97 76h3"/>' +
    U("s-star", 72, 68, 24, "a1 ol", "w"));

  /* C2 · event thumb — bar / framed field / bar, one sticker; static (tiny surface, tone mat already coloured) */
  V("mini", ".event-mini__thumb img", "0 0 100 129",
    '<rect class="ik" x="12" y="12" width="50" height="8"/>' + F(12, 30, 76, 62, "tn", 2.5) + '<circle class="wh" cx="44" cy="61" r="14"/><circle class="ln" cx="44" cy="61" r="14"/>' +
    '<rect class="sh" x="12" y="102" width="44" height="6"/>' + U("s-asterisk", 66, 96, 22, "ik", 0));

  /* D1 · team portrait — Board-1 colour-blocked card: tint of the card's own colour, pale disc, silhouette with hard shadow (no face), dots + sticker */
  V("portrait", ".member-card__photo img", "0 0 100 120",
    '<rect class="tn" x="0" y="0" width="100" height="120"/><circle class="wh dim2" cx="50" cy="52" r="38"/>' +
    U("s-dots", 4, 5, 26, "ik dim", 0) + SIL_BODY + SIL_HEAD + U("s-asterisk", 76, 8, 17, "ik", "w"));

  /* D2 · roster thumb (72–84px) — tint of its mat + silhouette only, static */
  V("roster", ".roster__photo img", "0 0 100 120", '<rect class="tn" x="0" y="0" width="100" height="120"/>' + SIL_BODY + SIL_HEAD);

  /* E · memories collage — three taped frames with hard shadows; sparkles like Board 1's collage */
  V("collage-sq", ".polaroid--p6 .polaroid__photo img", "0 0 110 100",
    F(10, 10, 62, 50, "tn3", 2) + F(44, 38, 52, 40, "wh", 2) + T(30, 4, 24, -6, 1) +
    U("s-sparkle", 84, 8, 16, "ik", "w") + U("s-sparkle", 8, 72, 14, "a1 ol", "w"));
  V("collage", ".polaroid__photo img", "0 0 160 88",
    F(12, 10, 82, 54, "tn3", 2) + F(66, 30, 62, 42, "wh", 2) + F(112, 8, 38, 26, "tn", 2) + T(38, 4, 26, -6, 1) +
    U("s-sparkle", 4, 62, 18, "ik", "w") + U("s-sparkle", 136, 54, 16, "a1 ol", "w"));

  /* E2 · gallery thumb — one large taped frame + two small, 16:10 */
  V("gallery", ".gallery-card__thumb img", "0 0 160 100",
    F(12, 14, 92, 64, "tn3", 2.5) + F(114, 14, 34, 28, "tn", 2) + F(114, 50, 34, 28, "wh", 2) + T(36, 8, 26, -6, 1) +
    U("s-asterisk", 70, 82, 14, "ik", "w") + U("s-sparkle", 12, 82, 12, "a1 ol", "w"));

  /* G2 · event-dialog photo — runtime-created (js/events.js render()), 6px mat; the gallery board, reduced.
     (The dialog POSTER is deliberately not covered: it is the card poster's URL, already cached, and sits tilted/sticky.) */
  V("dialog-photo", ".event-dialog__photo img", "0 0 160 100",
    F(14, 14, 96, 62, "tn3", 2.5) + F(120, 14, 28, 28, "tn", 2) + T(38, 8, 26, -6, 1) + U("s-asterisk", 122, 56, 18, "ik", "w"));

  /* F · lightbox — registration board on the dark stage: framed disc + asterisk, navy quarter, tape + sparkle; box is sized from the NEW photo's width/height before its bytes arrive */
  V("lightbox", "#lightbox-image", "0 0 160 120",
    '<path class="ln" d="M8 20V8h12M152 20V8h-12M8 100v12h12M152 100v12h-12"/>' +
    F(26, 22, 108, 76, "tn3", 3) + '<circle class="wh" cx="80" cy="60" r="22"/><circle class="ln" cx="80" cy="60" r="22"/>' +
    U("s-asterisk", 65, 45, 30, "ik", "w") + U("s-quarter", 26, 76, 22, "ik", 0) + T(98, 15, 28, -5, 1) +
    U("s-sparkle", 120, 76, 20, "a1 ol", "w") + '<rect class="a2" data-a="2" x="52" y="106" width="30" height="4"/>');
  TEMPLATES.lightbox = TEMPLATES.lightbox.replace("slice", "meet");   // portrait photos must keep the whole composition
  /* variants:end */

  function variantFor(img) {
    for (var i = 0; i < VARIANTS.length; i++) { if (img.matches(VARIANTS[i][0])) return VARIANTS[i][1]; }
    return null;
  }

  function clear(img) {
    var st = img.__skel, host = img.parentNode;
    if (st && st.el && st.el.parentNode) st.el.parentNode.removeChild(st.el);
    if (st) st.el = null;
    if (host && host.removeAttribute) host.removeAttribute("data-skel-state");
  }

  function show(img, state) {
    var st = img.__skel, host = img.parentNode;
    clear(img);
    var el = document.createElement("span");
    el.className = "skel skel--" + st.name + (state === "failed" ? " is-failed" : "");
    el.setAttribute("aria-hidden", "true");
    el.innerHTML = state === "failed" ? FAILED : TEMPLATES[st.name];
    host.insertBefore(el, img.nextSibling);          // after the image, before badges/captions
    host.setAttribute("data-skel-state", state);
    st.el = el;
  }

  /* 5.3: a cached image is often not `complete` yet at the moment the script runs but is a frame or two away from it;
     showing a skeleton for 30 ms would only flicker. Boxes are reserved by width/height, so waiting GRACE ms before the
     overlay appears shifts nothing and never delays the image. The lightbox is the exception: its stage collapses while
     the photo is hidden, so its skeleton must hold the space from the first frame. */
  var GRACE = 80;
  function cancelGrace(st) { if (st.timer) { clearTimeout(st.timer); st.timer = 0; } }

  /* Evaluate the image's current request. Safe to call repeatedly (lightbox swaps `src`). */
  function evaluate(img) {
    var st = img.__skel;
    cancelGrace(st);
    if (!img.getAttribute("src")) { clear(img); return; }        // nothing requested yet
    if (st.onEvaluate) st.onEvaluate(img);
    if (img.complete) {
      if (img.naturalWidth > 0) clear(img); else show(img, "failed");
    } else if (st.name === "lightbox") {
      show(img, "loading");
    } else {
      st.timer = setTimeout(function () {
        st.timer = 0;
        if (img.getAttribute("src") && !img.complete) show(img, "loading");
      }, GRACE);
    }
  }

  function bind(img, name) {
    if (img.__skel) return;                                      // one set of listeners per element, ever
    img.__skel = { name: name, el: null, onEvaluate: null, timer: 0 };
    img.addEventListener("load", function () {
      cancelGrace(img.__skel); clear(img); img.setAttribute("data-skel-reveal", "");
    });
    img.addEventListener("error", function () {
      cancelGrace(img.__skel);
      if (img.getAttribute("src")) show(img, "failed");
    });
    img.addEventListener("animationend", function () { img.removeAttribute("data-skel-reveal"); });
  }

  function attach(img) {
    var name = variantFor(img);
    if (!name || img.__skel) return;
    bind(img, name);
    var st = img.__skel;
    if (name === "lightbox") hookLightbox(img, st);
    else if (name === "dialog-photo" || name === "mini") st.onEvaluate = setRatio;   // box follows the image's own width/height
    evaluate(img);
  }

  function attachTree(node) {
    if (!node || node.nodeType !== 1) return;
    if (node.nodeName === "IMG") { attach(node); return; }
    var list = node.querySelectorAll("img");
    for (var i = 0; i < list.length; i++) attach(list[i]);
  }

  /* The lightbox re-uses one <img> and swaps its `src` (js/memories.js). Each swap re-evaluates: a preloaded/cached photo
     shows no skeleton; otherwise the skeleton takes the new photo's ratio so the stage never jumps and the previous
     photo never lingers under the new caption. */
  /* publish the photo's own ratio on its host so the overlay can be exactly the image box (grid hosts may be taller than the image) */
  function setRatio(i) {
    var w = parseFloat(i.getAttribute("width")) || 4, h = parseFloat(i.getAttribute("height")) || 3;
    i.parentNode.style.setProperty("--skel-ar", (w / h).toFixed(4));
  }
  function hookLightbox(img, st) {
    st.onEvaluate = setRatio;
    observe(img, { attributes: true, attributeFilter: ["src"] }, function () { evaluate(img); });
  }

  function observe(el, opts, cb) {
    if (!el || !window.MutationObserver) return;
    new MutationObserver(cb).observe(el, opts);
  }

  function init() {
    attachTree(document.body);
    /* runtime-created images: the event dialog re-renders its photos on every open */
    observe(document.getElementById("event-dialog"), { childList: true, subtree: true }, function (recs) {
      for (var i = 0; i < recs.length; i++) for (var j = 0; j < recs[i].addedNodes.length; j++) attachTree(recs[i].addedNodes[j]);
    });
  }

  (window.MULEARN = window.MULEARN || {}).skeleton = { rescan: function () { attachTree(document.body); } };

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
