/**
 * µLearn CHN — Team Member Data
 * Verified against asset archive filenames per Spec §7.7 and ASSET_MAPPING.md §2.
 * Roles and names are derived verbatim from client-supplied filenames.
 *
 * Precedence / Decisions:
 * - Decision D2: Role labels reflect filenames verbatim; no identities or roles invented.
 * - Lead Enabler: Title kept as filename states (not equated with faculty mentor).
 * - "Operational" vs "Operations": Filename uses "Operational Lead" (prototype used Operations Lead).
 * - IG Lead: Interest Group Lead across AI, UI/UX, Cyber Security, Web, Entrepreneurship.
 */
(function () {
  window.MULEARN = window.MULEARN || {};

  window.MULEARN.team = [
    // --- 1. Leadership ---
    {
      id: "team-01-geetha",
      name: "Geetha S",
      role: "Lead Enabler",
      roleFamily: "Leadership",
      image300: "img/team/geetha-s-300.webp",
      image600: "img/team/geetha-s-native.webp", // Capped at native resolution 377px without upscaling
      featured: false,
      verified: true, // Name and role verified from filename; organizational status unverified
      notes: "Lead Enabler per filename; low-res passport-style source; no upscaling applied."
    },
    {
      id: "team-02-nithin",
      name: "Nithin Jayakumar",
      role: "Campus Lead",
      roleFamily: "Leadership",
      image300: "img/team/nithin-jayakumar-300.webp",
      image600: "img/team/nithin-jayakumar-600.webp",
      featured: true,
      verified: true,
      notes: "Campus Lead; featured in approved prototype."
    },
    {
      id: "team-03-divyalakshmi",
      name: "Divyalakshmi",
      role: "Campus Co-Lead",
      roleFamily: "Leadership",
      image300: "img/team/divyalakshmi-300.webp",
      image600: "img/team/divyalakshmi-600.webp",
      featured: false,
      verified: true,
      notes: "Campus Co-Lead per filename."
    },

    // --- 2. Core Functional Leads ---
    {
      id: "team-04-govind",
      name: "Govind J S",
      role: "Creative Lead",
      roleFamily: "Core Leads",
      image300: "img/team/govind-j-s-300.webp",
      image600: "img/team/govind-j-s-600.webp",
      featured: true,
      verified: true,
      notes: "Creative Lead; featured in approved prototype."
    },
    {
      id: "team-05-hanin",
      name: "Hanin C K",
      role: "Operational Lead",
      roleFamily: "Core Leads",
      image300: "img/team/hanin-c-k-300.webp",
      image600: "img/team/hanin-c-k-600.webp",
      featured: true,
      verified: true,
      notes: "Operational Lead per filename (prototype labelled as Operations Lead)."
    },
    {
      id: "team-06-amanul",
      name: "Amanul Farhan",
      role: "Technical Lead",
      roleFamily: "Core Leads",
      image300: "img/team/amanul-farhan-300.webp",
      image600: "img/team/amanul-farhan-600.webp",
      featured: true,
      verified: true,
      notes: "Technical Lead; featured in approved prototype."
    },
    {
      id: "team-07-pavithra",
      name: "Pavithra A",
      role: "Media Lead",
      roleFamily: "Core Leads",
      image300: "img/team/pavithra-a-300.webp",
      image600: "img/team/pavithra-a-600.webp",
      featured: false,
      verified: true,
      notes: "Media Lead per filename."
    },
    {
      id: "team-08-albin",
      name: "Albin Thomas",
      role: "Content Lead",
      roleFamily: "Core Leads",
      image300: "img/team/albin-thomas-300.webp",
      image600: "img/team/albin-thomas-600.webp",
      featured: false,
      verified: true,
      notes: "Content Lead per filename."
    },

    // --- 3. Operational & Creative Teams ---
    {
      id: "team-09-melwin",
      name: "Melwin Shibu Mathew",
      role: "Operational Team",
      roleFamily: "Operations & Creative",
      image300: "img/team/melwin-shibu-mathew-300.webp",
      image600: "img/team/melwin-shibu-mathew-600.webp",
      featured: false,
      verified: true,
      notes: "Operational Team per filename."
    },
    {
      id: "team-10-sara",
      name: "Sara Shaji",
      role: "Operational Team",
      roleFamily: "Operations & Creative",
      image300: "img/team/sara-shaji-300.webp",
      image600: "img/team/sara-shaji-600.webp",
      featured: false,
      verified: true,
      notes: "Operational Team per filename."
    },
    {
      id: "team-11-afsal",
      name: "Afsal S",
      role: "Designer",
      roleFamily: "Operations & Creative",
      image300: "img/team/afsal-s-300.webp",
      image600: "img/team/afsal-s-600.webp",
      featured: false,
      verified: true,
      notes: "Designer per filename (cut-out portrait style)."
    },
    {
      id: "team-12-vismaya",
      name: "Vismaya Gawri Krishnan",
      role: "Designer",
      roleFamily: "Operations & Creative",
      image300: "img/team/vismaya-gawri-krishnan-300.webp",
      image600: "img/team/vismaya-gawri-krishnan-600.webp",
      featured: false,
      verified: true,
      notes: "Designer per filename."
    },
    {
      id: "team-13-karthika",
      name: "Karthika S",
      role: "Content Team",
      roleFamily: "Operations & Creative",
      image300: "img/team/karthika-s-300.webp",
      image600: "img/team/karthika-s-native.webp",
      featured: false,
      verified: true,
      notes: "Content Team per filename."
    },
    {
      id: "team-14-sreelakshmi",
      name: "Sreelakshmi M",
      role: "Content Team",
      roleFamily: "Operations & Creative",
      image300: "img/team/sreelakshmi-m-300.webp",
      image600: "img/team/sreelakshmi-m-600.webp",
      featured: false,
      verified: true,
      notes: "Content Team per filename."
    },
    {
      id: "team-15-parvathy",
      name: "Parvathy Vinayan",
      role: "Media Team",
      roleFamily: "Operations & Creative",
      image300: "img/team/parvathy-vinayan-300.webp",
      image600: "img/team/parvathy-vinayan-600.webp",
      featured: false,
      verified: true,
      notes: "Media Team per filename (distinct from Pavithra A)."
    },
    {
      id: "team-16-brijith",
      name: "Brijith K Reji",
      role: "Media Team",
      roleFamily: "Operations & Creative",
      image300: "img/team/brijith-k-reji-300.webp",
      image600: "img/team/brijith-k-reji-600.webp",
      featured: false,
      verified: true,
      notes: "Media Team per filename."
    },

    // --- 4. Interest Group (IG) Leads ---
    {
      id: "team-17-adhi",
      name: "Adhi Narayan",
      role: "IG Lead – AI",
      roleFamily: "Interest Group Leads",
      image300: "img/team/adhi-narayan-300.webp",
      image600: "img/team/adhi-narayan-600.webp",
      featured: false,
      verified: true,
      notes: "Interest Group Lead for Artificial Intelligence."
    },
    {
      id: "team-18-al-ameen",
      name: "Al Ameen",
      role: "IG Lead – UI/UX",
      roleFamily: "Interest Group Leads",
      image300: "img/team/al-ameen-300.webp",
      image600: "img/team/al-ameen-600.webp",
      featured: false,
      verified: true,
      notes: "Interest Group Lead for UI/UX Design; source had EXIF rotation 6 (corrected)."
    },
    {
      id: "team-19-amal",
      name: "Amal S",
      role: "IG Lead – Cyber Security",
      roleFamily: "Interest Group Leads",
      image300: "img/team/amal-s-300.webp",
      image600: "img/team/amal-s-600.webp",
      featured: false,
      verified: true,
      notes: "Interest Group Lead for Cyber Security."
    },
    {
      id: "team-20-abhiram",
      name: "Abhiram J",
      role: "IG Lead – Web",
      roleFamily: "Interest Group Leads",
      image300: "img/team/abhiram-j-300.webp",
      image600: "img/team/abhiram-j-native.webp",
      featured: false,
      verified: true,
      notes: "Interest Group Lead for Web Development."
    },
    {
      id: "team-21-swathy",
      name: "Swathy J",
      role: "IG Lead – Entrepreneurship",
      roleFamily: "Interest Group Leads",
      image300: "img/team/swathy-j-300.webp",
      image600: "img/team/swathy-j-600.webp",
      featured: false,
      verified: true,
      notes: "Interest Group Lead for Entrepreneurship (Note: Entrepreneurship is a CHN-specific group, not in official 23 org groups)."
    }
  ];
})();
