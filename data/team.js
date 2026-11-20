/**
 * µLearn CHN — Team data (Phase 6.1, reconciled). Single source of truth for the Team section.
 * Rendered into index.html (no-JS safe) by scripts/build_team.js; never edit the generated markup by hand.
 *
 * SOURCES: names and recorded roles = client-supplied filenames in sources/mulearn/Team/ (Spec §7.7, 21 members).
 * Pairing of face to name rests ONLY on those client filenames. It was not (and must not be) checked by comparing faces.
 *
 * FIELDS
 *   role         recorded role, verbatim from the filename (internal record; never rewritten)
 *   roleStatus   "recorded" = shown publicly | "unconfirmed" = the title is in doubt, so it is NOT shown (name only)
 *   roleLabel    the text shown publicly (null when roleStatus is "unconfirmed"); "IG" is expanded to "Interest Group"
 *   roleNote     why a title is held back / what is open (internal)
 *   photo        derivative files that exist in img/team/ (never upscaled; w/h = real pixel size of src600)
 *   photoShown   false = neutral monogram instead of the portrait (kill-switch if a pairing is ever disputed)
 *   featured     featuredOrder 1..4 for the four cards, in page order
 *   tone         card backdrop colour for the featured cards (yellow / indigo / mint rotation, Board 1)
 *
 * No hierarchy is implied: the directory is one list in roster order; `kind` is only the role's own wording.
 */
(function () {
  window.MULEARN = window.MULEARN || {};
  function P(slug, w, h, pos) {
    return { src300: "img/team/" + slug + "-300.webp", src600: "img/team/" + slug + (w === 377 ? "-native" : "-600") + ".webp", w300: 300, h300: 360, w: w, h: h, pos: pos || "50% 25%" };
  }
  function M(n, id, name, role, slug, opts) {
    opts = opts || {};
    var unconfirmed = !!opts.unconfirmed;
    var ig = /^IG Lead – /.test(role);
    return {
      id: "team-" + (n < 10 ? "0" : "") + n + "-" + id,
      order: n,
      name: name,
      role: role,
      roleStatus: unconfirmed ? "unconfirmed" : "recorded",
      roleLabel: unconfirmed ? null : (ig ? role.replace("IG Lead", "Interest Group Lead") : role),
      roleNote: opts.note || "",
      kind: ig ? "interest-group-lead" : /Lead$/.test(role) ? "lead" : /Team$|Designer$/.test(role) ? "team" : "other",
      photo: P(slug, opts.w || 600, opts.h || 720, opts.pos),
      photoShown: true,
      featured: !!opts.fo,
      featuredOrder: opts.fo || 0,
      tone: opts.tone || ""
    };
  }
  window.MULEARN.team = [
    M(1, "geetha", "Geetha S", "Lead Enabler", "geetha-s", { w: 377, h: 452, unconfirmed: true,
      note: "Open: what \"Lead Enabler\" means is unknown (not in the µLearn chapter model). Not shown as Faculty; title held back until the client confirms." }),
    M(2, "nithin", "Nithin Jayakumar", "Campus Lead", "nithin-jayakumar", { fo: 1, tone: "yellow" }),
    M(3, "divyalakshmi", "Divyalakshmi", "Campus Co-Lead", "divyalakshmi", { unconfirmed: true,
      note: "Open: client to confirm the title and its spelling (Co-Lead vs Co Lead). Held back until confirmed." }),
    M(4, "govind", "Govind J S", "Creative Lead", "govind-j-s", { fo: 3, tone: "mint" }),
    M(5, "hanin", "Hanin C K", "Operational Lead", "hanin-c-k", { fo: 4, tone: "yellow",
      note: "Wording only: the prototype said \"Operations Lead\"; the client filename and this brief say \"Operational Lead\", which is shown. Client may confirm the preferred wording." }),
    M(6, "amanul", "Amanul Farhan", "Technical Lead", "amanul-farhan", { fo: 2, tone: "indigo" }),
    M(7, "pavithra", "Pavithra A", "Media Lead", "pavithra-a"),
    M(8, "albin", "Albin Thomas", "Content Lead", "albin-thomas"),
    M(9, "melwin", "Melwin Shibu Mathew", "Operational Team", "melwin-shibu-mathew"),
    M(10, "sara", "Sara Shaji", "Operational Team", "sara-shaji"),
    M(11, "afsal", "Afsal S", "Designer", "afsal-s"),
    M(12, "vismaya", "Vismaya Gawri Krishnan", "Designer", "vismaya-gawri-krishnan", { pos: "50% 12%" }),
    M(13, "karthika", "Karthika S", "Content Team", "karthika-s"),
    M(14, "sreelakshmi", "Sreelakshmi M", "Content Team", "sreelakshmi-m"),
    M(15, "parvathy", "Parvathy Vinayan", "Media Team", "parvathy-vinayan"),
    M(16, "brijith", "Brijith K Reji", "Media Team", "brijith-k-reji"),
    M(17, "adhi", "Adhi Narayan", "IG Lead – AI", "adhi-narayan"),
    M(18, "al-ameen", "Al Ameen", "IG Lead – UI/UX", "al-ameen"),
    M(19, "amal", "Amal S", "IG Lead – Cyber Security", "amal-s"),
    M(20, "abhiram", "Abhiram J", "IG Lead – Web", "abhiram-j"),
    M(21, "swathy", "Swathy J", "IG Lead – Entrepreneurship", "swathy-j", { unconfirmed: true,
      note: "Open: \"Entrepreneurship\" is not among the official µLearn Interest Groups listed on mulearn.org (checked 2026-11-20); may be a CHN-specific group. Title held back until confirmed. (Swathy J also appears as a Build with AI speaker; identity not merged from faces.)" })
  ];
})();
