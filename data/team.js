/**
 * µLearn CHN — Team Member Data
 * Verified against asset archive filenames per Spec §7.7 and ASSET_MAPPING.md §2.
 * Roles and names are derived verbatim from client-supplied filenames in sources/mulearn/Team/.
 *
 * Precedence / Verification Rules:
 * - CANONICAL ROSTER: 21 members strictly starting with #1 Geetha S and ending with #21 Swathy J.
 *   (References to any alternative names such as 'Abhiram V' or 'Aswin Sreekumar' are invalid).
 * - FEATURED SELECTION: Exactly four members per Spec §7.7 and approved prototype:
 *   1. Campus Lead (#2 Nithin Jayakumar)
 *   2. Technical Lead (#6 Amanul Farhan)
 *   3. Creative Lead (#4 Govind J S)
 *   4. Operational Lead (#5 Hanin C K)
 * - VERIFICATION LEVELS:
 *   [TECHNICALLY_VERIFIED]: Derivative image exists, dimensions/budget verified, EXIF stripped.
 *   [SOURCE_DOCUMENT_VERIFIED]: Name and role match client filename on disk verbatim.
 *   [CLIENT_CONFIRMATION_REQUIRED]: Face-to-name linkage, Lead Enabler status, and non-standard IG groups.
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
      image600: "img/team/geetha-s-native.webp", // Native source is 377px; capped to prevent upscaling
      featured: false,
      verificationLevel: "SOURCE_DOCUMENT_VERIFIED",
      clientConfirmationRequired: true,
      notes: "Lead Enabler per filename; organizational title unconfirmed (not in standard µLearn chapter model; do not assume Faculty Mentor)."
    },
    {
      id: "team-02-nithin",
      name: "Nithin Jayakumar",
      role: "Campus Lead",
      roleFamily: "Leadership",
      image300: "img/team/nithin-jayakumar-300.webp",
      image600: "img/team/nithin-jayakumar-600.webp",
      featured: true,
      verificationLevel: "SOURCE_DOCUMENT_VERIFIED",
      clientConfirmationRequired: false,
      notes: "Campus Lead per filename; featured in approved prototype and Spec §7.7."
    },
    {
      id: "team-03-divyalakshmi",
      name: "Divyalakshmi",
      role: "Campus Co-Lead",
      roleFamily: "Leadership",
      image300: "img/team/divyalakshmi-300.webp",
      image600: "img/team/divyalakshmi-600.webp",
      featured: false,
      verificationLevel: "SOURCE_DOCUMENT_VERIFIED",
      clientConfirmationRequired: true,
      notes: "Campus Co-Lead per filename; spelling 'Co-Lead' vs 'Co Lead' to be confirmed by client."
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
      verificationLevel: "SOURCE_DOCUMENT_VERIFIED",
      clientConfirmationRequired: false,
      notes: "Creative Lead per filename; featured in approved prototype and Spec §7.7."
    },
    {
      id: "team-05-hanin",
      name: "Hanin C K",
      role: "Operational Lead",
      roleFamily: "Core Leads",
      image300: "img/team/hanin-c-k-300.webp",
      image600: "img/team/hanin-c-k-600.webp",
      featured: true,
      verificationLevel: "SOURCE_DOCUMENT_VERIFIED",
      clientConfirmationRequired: true,
      notes: "Operational Lead per filename (prototype used 'Operations Lead'); client to confirm exact title preference."
    },
    {
      id: "team-06-amanul",
      name: "Amanul Farhan",
      role: "Technical Lead",
      roleFamily: "Core Leads",
      image300: "img/team/amanul-farhan-300.webp",
      image600: "img/team/amanul-farhan-600.webp",
      featured: true,
      verificationLevel: "SOURCE_DOCUMENT_VERIFIED",
      clientConfirmationRequired: false,
      notes: "Technical Lead per filename; featured in approved prototype and Spec §7.7."
    },
    {
      id: "team-07-pavithra",
      name: "Pavithra A",
      role: "Media Lead",
      roleFamily: "Core Leads",
      image300: "img/team/pavithra-a-300.webp",
      image600: "img/team/pavithra-a-600.webp",
      featured: false,
      verificationLevel: "SOURCE_DOCUMENT_VERIFIED",
      clientConfirmationRequired: false,
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
      verificationLevel: "SOURCE_DOCUMENT_VERIFIED",
      clientConfirmationRequired: false,
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
      verificationLevel: "SOURCE_DOCUMENT_VERIFIED",
      clientConfirmationRequired: false,
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
      verificationLevel: "SOURCE_DOCUMENT_VERIFIED",
      clientConfirmationRequired: false,
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
      verificationLevel: "SOURCE_DOCUMENT_VERIFIED",
      clientConfirmationRequired: false,
      notes: "Designer per filename (cut-out portrait style in source)."
    },
    {
      id: "team-12-vismaya",
      name: "Vismaya Gawri Krishnan",
      role: "Designer",
      roleFamily: "Operations & Creative",
      image300: "img/team/vismaya-gawri-krishnan-300.webp",
      image600: "img/team/vismaya-gawri-krishnan-600.webp",
      featured: false,
      verificationLevel: "SOURCE_DOCUMENT_VERIFIED",
      clientConfirmationRequired: false,
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
      verificationLevel: "SOURCE_DOCUMENT_VERIFIED",
      clientConfirmationRequired: false,
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
      verificationLevel: "SOURCE_DOCUMENT_VERIFIED",
      clientConfirmationRequired: false,
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
      verificationLevel: "SOURCE_DOCUMENT_VERIFIED",
      clientConfirmationRequired: false,
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
      verificationLevel: "SOURCE_DOCUMENT_VERIFIED",
      clientConfirmationRequired: false,
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
      verificationLevel: "SOURCE_DOCUMENT_VERIFIED",
      clientConfirmationRequired: false,
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
      verificationLevel: "SOURCE_DOCUMENT_VERIFIED",
      clientConfirmationRequired: false,
      notes: "Interest Group Lead for UI/UX Design; EXIF rotation 6 orientation corrected."
    },
    {
      id: "team-19-amal",
      name: "Amal S",
      role: "IG Lead – Cyber Security",
      roleFamily: "Interest Group Leads",
      image300: "img/team/amal-s-300.webp",
      image600: "img/team/amal-s-600.webp",
      featured: false,
      verificationLevel: "SOURCE_DOCUMENT_VERIFIED",
      clientConfirmationRequired: false,
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
      verificationLevel: "SOURCE_DOCUMENT_VERIFIED",
      clientConfirmationRequired: false,
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
      verificationLevel: "SOURCE_DOCUMENT_VERIFIED",
      clientConfirmationRequired: true,
      notes: "Interest Group Lead for Entrepreneurship (Note: Entrepreneurship is a CHN campus-specific group; not in the 23 official central org groups per mulearn.org)."
    }
  ];
})();
