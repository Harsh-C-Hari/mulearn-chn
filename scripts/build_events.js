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

/* Phase 5.3 compact entry: coloured thumbnail field (poster shown whole), number, title, printed descriptor, date only if verified, button. */
function compactCard(e) {
  const id = "event-" + e.slug, t = e.thumb;
  const lines = [
    `      <li class="event event--compact event--${e.slug}" data-event="${e.slug}">`,
    `        <article class="card event-mini event-mini--${e.tone}" aria-labelledby="${id}-title">`,
    `          <figure class="event-mini__thumb">`,
    `            <img src="${esc(t.src)}" srcset="${esc(t.srcset)}" sizes="(min-width:1024px) 220px, (min-width:700px) 300px, 130px" width="${t.width}" height="${t.height}" alt="${esc(e.image.alt)}" loading="lazy" decoding="async">`,
    `          </figure>`,
    `          <div class="event-mini__body">`,
    `            <span class="event-mini__num" aria-hidden="true">${pad(e.order)}</span>`,
    `            <h3 id="${id}-title" class="event-mini__title">${esc(e.title)}</h3>`,
    `            <p class="event-mini__desc">${esc(e.descriptor)}</p>`
  ];
  if (e.dateLabel) lines.push(`            <p class="event-mini__date"><span class="tag tag--ink">${esc(e.dateLabel)}</span></p>`);
  lines.push(
    `            <button type="button" class="btn btn--sm btn--neutral event-mini__btn" data-event-open="${e.slug}" aria-haspopup="dialog">View details<span class="sr-only"> for ${esc(e.title)}</span><svg class="icon" aria-hidden="true"><use href="#i-arrow-right"/></svg></button>`,
    `          </div>`,
    `        </article>`,
    `      </li>`);
  return lines.join("\n");
}

/* Phase 5.2 featured card: poster in a framed, tilted mat; coloured card body; "View details" button (dialog arrives in 5.4). */
const STK = { coral: ["sticker--yellow sticker--outlined", "s-star"], indigo: ["sticker--yellow sticker--outlined", "s-sparkle"], yellow: ["sticker--indigo", "s-asterisk"] };
function featuredCard(e) {
  const id = "event-" + e.slug, im = e.image.poster;
  const lines = [
    `      <li class="event event--featured event--${e.slug}" data-event="${e.slug}">`,
    `        <article class="card event-card event-card--${e.tone}" aria-labelledby="${id}-title">`,
    `          <span class="event-card__num" aria-hidden="true">${pad(e.order)}</span>`,
    `          <figure class="event-card__poster">`,
    `            <img src="${esc(im.src)}" width="${im.width}" height="${im.height}" alt="${esc(e.image.alt)}" loading="lazy" decoding="async">`,
    `          </figure>`,
    `          <div class="event-card__body">`,
    `            <h3 id="${id}-title" class="event-card__title">${esc(e.title)}</h3>`,
    `            <p class="event-card__blurb">${esc(e.blurb)}</p>`
  ];
  const tags = [e.dateLabel].concat(e.meta || []).filter(Boolean);
  if (tags.length) lines.push(`            <ul class="tag-list event-card__tags" role="list">`, ...tags.map((t, i) => `              <li><span class="tag${i === 0 ? " tag--ink" : ""}">${esc(t)}</span></li>`), `            </ul>`);
  lines.push(
    `            <button type="button" class="btn btn--sm event-card__btn" data-event-open="${e.slug}" aria-haspopup="dialog">View details<span class="sr-only"> for ${esc(e.title)}</span><svg class="icon" aria-hidden="true"><use href="#i-arrow-right"/></svg></button>`,
    `          </div>`,
    `          <span class="sticker ${STK[e.tone][0]} event-card__stk" aria-hidden="true"><svg><use href="#${STK[e.tone][1]}"/></svg></span>`,
    `        </article>`,
    `      </li>`);
  return lines.join("\n");
}
const card = e => (e.group === "featured" ? featuredCard(e) : compactCard(e));
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
