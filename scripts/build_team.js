#!/usr/bin/env node
/* Renders the no-JS HTML for the Team section from data/team.js into index.html (between marker comments).
 * Usage: node scripts/build_team.js [--check]. Text only goes through esc(). Phase 6.1: semantic structure only. */
const fs = require("fs"), path = require("path");
const root = path.resolve(__dirname, "..");
global.window = {}; require(path.join(root, "data/team.js"));
const T = window.MULEARN.team.slice().sort((a, b) => a.order - b.order);
const esc = s => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
const pad = n => String(n).padStart(2, "0");

/* Phase 6.2 / sticker anchoring: per-member map so all 4 featured cards have distinct shapes.
 * 1: Nithin (yellow) -> indigo asterisk (#s-asterisk)
 * 2: Amanul (indigo) -> yellow star (#s-star)
 * 3: Govind (mint) -> yellow sparkle (#s-sparkle)
 * 4: Hanin (yellow) -> coral bolt (#s-bolt, de-duplicated from Nithin's asterisk)
 * The sticker is placed inside <article> so it rides along on hover translate. */
const FEATURED_STK = {
  1: ["sticker--indigo", "s-asterisk"],
  2: ["sticker--yellow sticker--outlined", "s-star"],
  3: ["sticker--yellow sticker--outlined", "s-sparkle"],
  4: ["sticker--coral sticker--outlined", "s-bolt"]
};
const initials = n => n.split(/\s+/).map(w => w[0]).slice(0, 2).join("").toUpperCase();
function photoFigure(m, cls, sizes) {
  const ph = m.photo;
  if (!m.photoShown) return `          <div class="${cls} ${cls}--mono" aria-hidden="true"><span>${esc(initials(m.name))}</span></div>`;
  return [
    `          <figure class="${cls}">`,
    `            <img src="${esc(ph.src600)}" srcset="${esc(ph.src300)} ${ph.w300}w, ${esc(ph.src600)} ${ph.w}w" sizes="${sizes}" width="${ph.w300}" height="${ph.h300}" alt="Portrait of ${esc(m.name)}" style="object-position:${esc(ph.pos)}" loading="lazy" decoding="async">`,
    `          </figure>`
  ].join("\n");
}
function featuredItem(m) {
  const id = "member-" + m.id, stk = FEATURED_STK[m.featuredOrder] || ["sticker--indigo", "s-asterisk"];
  return [
    `      <li class="member member--featured member--${m.tone}" data-member="${m.id}">`,
    `        <article class="card member-card member-card--${m.tone}" aria-labelledby="${id}-name">`,
    photoFigure(m, "member-card__photo", "(min-width:1024px) 260px, (min-width:600px) 330px, 150px"),
    `          <div class="member-card__body">`,
    `            <h3 id="${id}-name" class="member-card__name">${esc(m.name)}</h3>`,
    m.roleLabel ? `            <p class="member-card__role">${esc(m.roleLabel)}</p>` : "",
    `          </div>`,
    `          <span class="sticker ${stk[0]} member-card__stk" aria-hidden="true"><svg><use href="#${stk[1]}"/></svg></span>`,
    `        </article>`,
    `      </li>`
  ].filter(Boolean).join("\n");
}
/* Phase 6.3 roster entry: all 21 in roster order, small portrait (decorative: the name is adjacent), numeral, name, role (held titles: none),
 * "Featured above" flag for the four cards so the count stays 21. */
function directoryItem(m) {
  const ph = m.photo, mono = !m.photoShown;
  return [
    `      <li class="roster__item${m.featured ? " roster__item--featured" : ""}" data-member="${m.id}">`,
    mono
      ? `        <div class="roster__photo roster__photo--mono" aria-hidden="true"><span>${esc(initials(m.name))}</span></div>`
      : `        <figure class="roster__photo"><img src="${esc(ph.src300)}" width="${ph.w300}" height="${ph.h300}" alt="" style="object-position:${esc(ph.pos)}" loading="lazy" decoding="async"></figure>`,
    `        <div class="roster__text">`,
    `          <span class="roster__num" aria-hidden="true">${pad(m.order)}</span>`,
    `          <span class="roster__name">${esc(m.name)}</span>`,
    m.roleLabel ? `          <span class="roster__role">${esc(m.roleLabel)}</span>` : "",
    m.featured ? `          <span class="roster__flag">Featured above</span>` : "",
    `        </div>`,
    `      </li>`
  ].filter(Boolean).join("\n");
}
const featured = T.filter(m => m.featured).sort((a, b) => a.featuredOrder - b.featuredOrder);
const blocks = { featured: featured.map(featuredItem).join("\n"), directory: T.map(directoryItem).join("\n") };

const file = path.join(root, "index.html");
let html = fs.readFileSync(file, "utf8"), out = html;
for (const g of ["featured", "directory"]) {
  const re = new RegExp(`(<!-- team:${g}:start[^>]*-->)[\\s\\S]*?(\\n\\s*<!-- team:${g}:end -->)`);
  if (!re.test(out)) { console.error("markers missing for", g); process.exit(2); }
  out = out.replace(re, (_, a, b) => a + "\n" + blocks[g] + b);
}
if (process.argv.includes("--check")) { if (out !== html) { console.error("index.html team markup is out of date: run scripts/build_team.js"); process.exit(1); } console.log("team markup up to date"); }
else { fs.writeFileSync(file, out); console.log("team markup written:", T.length, "members,", featured.length, "featured"); }
