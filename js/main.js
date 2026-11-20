/*!
 * main.js — page glue (Phase 3.1). Binds every [data-link="key"] to its canonical URL in data/links.js
 * so URLs live in one place; the hard-coded href in the HTML is only the no-JS fallback.
 */
(function () {
  "use strict";
  var L = window.MULEARN && window.MULEARN.links;
  if (!L) return;
  [].forEach.call(document.querySelectorAll("[data-link]"), function (a) {
    var item = L[a.getAttribute("data-link")];
    if (item && item.url) a.setAttribute("href", item.url);
  });
})();
