#!/usr/bin/env node
/* Renders the no-JS HTML for the Events section from data/events.js into index.html (between the marker comments).
 * Usage: node scripts/build_events.js [--check]   (--check exits 1 if index.html is out of date)
 * Phase 5.1: minimal semantic cards. 5.2 upgrades featured markup, 5.3 compact markup. Text only goes through esc(). */
const fs = require("fs"), path = require("path");
const root = path.resolve(__dirname, "..");
global.window = {}; require(path.join(root, "data/events.js"));
const E = window.MULEARN.events.slice().sort((a, b) => a.order - b.order);
const esc = s => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
const pad = n => String(n).padStart(2, "0");

function card(e) {
  const id = "event-" + e.slug;
  const lines = [
    `      <li class="event event--${e.group} event--${e.slug}" data-event="${e.slug}">`,
    `        <article class="card event__card" aria-labelledby="${id}-title">`,
    `          <span class="card__num event__num" aria-hidden="true">${pad(e.order)}</span>`,
    `          <h3 id="${id}-title" class="card__title event__title">${esc(e.title)}</h3>`,
    `          <p class="event__descriptor">${esc(e.descriptor)}</p>`
  ];
  if (e.dateLabel) lines.push(`          <p class="event__date">${esc(e.dateLabel)}</p>`);
  lines.push(`        </article>`, `      </li>`);
  return lines.join("\n");
}
const block = g => E.filter(e => e.group === g).map(card).join("\n");

const file = path.join(root, "index.html");
let html = fs.readFileSync(file, "utf8"), out = html;
for (const g of ["featured", "compact"]) {
  const re = new RegExp(`(<!-- events:${g}:start[^>]*-->)[\\s\\S]*?(\\n\\s*<!-- events:${g}:end -->)`);
  if (!re.test(out)) { console.error("markers missing for", g); process.exit(2); }
  out = out.replace(re, (_, a, b) => a + "\n" + block(g) + b);
}
if (process.argv.includes("--check")) { if (out !== html) { console.error("index.html events markup is out of date: run scripts/build_events.js"); process.exit(1); } console.log("events markup up to date"); }
else { fs.writeFileSync(file, out); console.log("events markup written:", E.length, "events"); }
