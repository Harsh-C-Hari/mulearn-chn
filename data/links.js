/**
 * µLearn CHN — External Links & Destinations
 * Canonical source of truth for external navigation and CTAs.
 *
 * Precedence & Verification Status:
 * - CANONICAL URLS: Restored and maintained strictly per PROJECT_MASTER_SPEC.md §8.
 *   These are the client-supplied URLs.
 * - UNCONFIRMED ALTERNATIVES: Documented separately from reference.html (prototype)
 *   awaiting client confirmation before any replacement.
 *
 * Verification Categories:
 * - [SOURCE_DOCUMENT_VERIFIED]: Found in PROJECT_MASTER_SPEC.md §8.
 * - [TECHNICALLY_VERIFIED]: Tested and HTTP 200 / valid live route.
 * - [CLIENT_CONFIRMATION_REQUIRED]: Blocked by anti-bot or campus-specific handle needing client sign-off.
 */
(function () {
  window.MULEARN = window.MULEARN || {};

  window.MULEARN.links = {
    // === PRIMARY CTAs (Client-Supplied per Spec §8) ===
    register: {
      label: "Create µLearn Account",
      url: "https://app.mulearn.org/register",
      verificationLevel: "TECHNICALLY_VERIFIED",
      status: "Verified live registration route",
      clientConfirmationRequired: false,
      description: "Official registration portal for µLearn ecosystem (Spec §8)."
    },
    discord: {
      label: "Join CHN Discord",
      url: "https://discord.gg/DfnDfBhGha",
      verificationLevel: "TECHNICALLY_VERIFIED",
      status: "Verified live invite ('Mulearn.CHN')",
      clientConfirmationRequired: false,
      description: "Official Discord server for µLearn CHN (College of Engineering Chengannur)."
    },

    // === COMMUNITY SOCIALS (Client-Supplied per Spec §8) ===
    linkedin: {
      label: "µLearn CHN on LinkedIn",
      url: "https://www.linkedin.com/company/gtech-mulearn-cec/",
      verificationLevel: "SOURCE_DOCUMENT_VERIFIED",
      status: "Client-supplied in Spec §8; LinkedIn login wall prevents crawler verification",
      clientConfirmationRequired: true,
      description: "College campus chapter LinkedIn presence."
    },
    instagram: {
      label: "µLearn CHN on Instagram",
      url: "https://www.instagram.com/mulearn.chn/",
      verificationLevel: "SOURCE_DOCUMENT_VERIFIED",
      status: "Client-supplied in Spec §8; Instagram login wall prevents crawler verification",
      clientConfirmationRequired: true,
      description: "College campus chapter Instagram updates."
    },
    email: {
      label: "Contact Email",
      url: "mailto:gtechmulearncec@gmail.com",
      verificationLevel: "SOURCE_DOCUMENT_VERIFIED",
      status: "Client-supplied in Spec §8",
      clientConfirmationRequired: true,
      description: "Campus chapter communication email."
    },

    // === NETWORK / ECOSYSTEM DESTINATIONS (Spec §8) ===
    mulearnOrg: {
      label: "µLearn Official Website",
      url: "https://mulearn.org/",
      verificationLevel: "TECHNICALLY_VERIFIED",
      status: "Verified live parent website",
      clientConfirmationRequired: false,
      description: "Parent organisation ecosystem site."
    },

    // === WHAT µLEARN OFFERS (Network-Level Links per Spec §8) ===
    offers: {
      community: {
        label: "µLearn Community",
        url: "https://app.mulearn.org/",
        verificationLevel: "TECHNICALLY_VERIFIED",
        clientConfirmationRequired: false
      },
      mentors: {
        label: "µLearn Mentors",
        url: "https://app.mulearn.org/dashboard/search/mentors",
        verificationLevel: "SOURCE_DOCUMENT_VERIFIED",
        clientConfirmationRequired: true
      },
      interestGroups: {
        label: "Interest Groups",
        url: "https://mulearn.org/interest-groups",
        verificationLevel: "TECHNICALLY_VERIFIED",
        clientConfirmationRequired: false
      },
      roadmaps: {
        label: "Learning Roadmaps",
        url: "https://app.mulearn.org/dashboard/mujourney",
        verificationLevel: "SOURCE_DOCUMENT_VERIFIED",
        clientConfirmationRequired: true
      },
      challenges: {
        label: "Challenges & Karma",
        url: "https://app.mulearn.org/dashboard/mujourney",
        verificationLevel: "SOURCE_DOCUMENT_VERIFIED",
        clientConfirmationRequired: true
      },
      opportunities: {
        label: "Career Opportunities",
        url: "https://mulearn.org/careers",
        verificationLevel: "SOURCE_DOCUMENT_VERIFIED",
        clientConfirmationRequired: true
      }
    },

    // === UNCONFIRMED ALTERNATIVES (Found in reference.html prototype) ===
    // These are documented for client review; canonical links above are preserved.
    unconfirmedAlternatives: {
      prototypeRegister: {
        label: "Join via mulearn.org/join",
        url: "https://mulearn.org/join",
        source: "reference.html prototype (line 35)",
        status: "Unconfirmed alternative to app.mulearn.org/register",
        clientConfirmationRequired: true
      },
      prototypeDiscord: {
        label: "Alternative Discord Invite",
        url: "https://discord.gg/gKNcvvdU",
        source: "reference.html prototype (line 69)",
        status: "Unconfirmed alternative to discord.gg/DfnDfBhGha",
        clientConfirmationRequired: true
      },
      prototypeLinkedin: {
        label: "Alternative LinkedIn Handle",
        url: "https://www.linkedin.com/company/mulearn-ceconline/",
        source: "reference.html prototype (line 882)",
        status: "Unconfirmed alternative to gtech-mulearn-cec/",
        clientConfirmationRequired: true
      },
      prototypeInstagram: {
        label: "Alternative Instagram Handle",
        url: "https://www.instagram.com/mulearn_chn/",
        source: "reference.html prototype (line 883)",
        status: "Unconfirmed alternative to mulearn.chn/ (underscore vs dot)",
        clientConfirmationRequired: true
      }
    }
  };
})();
