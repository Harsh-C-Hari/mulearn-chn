/**
 * µLearn CHN — External Links & Destinations
 * Canonical source of truth for external navigation and CTAs.
 * Verified per Project Master Spec §8.
 */
(function () {
  window.MULEARN = window.MULEARN || {};

  window.MULEARN.links = {
    // Primary CTAs
    register: {
      label: "Create µLearn Account",
      url: "https://app.mulearn.org/register",
      verified: true,
      description: "Official registration portal for µLearn ecosystem."
    },
    discord: {
      label: "Join CHN Discord",
      url: "https://discord.gg/DfnDfBhGha",
      verified: true,
      description: "Official Discord server for µLearn CHN (College of Engineering Chengannur)."
    },

    // Community Socials
    linkedin: {
      label: "µLearn CHN on LinkedIn",
      url: "https://www.linkedin.com/company/gtech-mulearn-cec/",
      verified: false, // Client-supplied; robots blocked automated crawler
      description: "College campus chapter LinkedIn presence."
    },
    instagram: {
      label: "µLearn CHN on Instagram",
      url: "https://www.instagram.com/mulearn.chn/",
      verified: false, // Client-supplied; robots blocked automated crawler
      description: "College campus chapter Instagram updates."
    },
    email: {
      label: "Contact Email",
      url: "mailto:gtechmulearncec@gmail.com",
      verified: false, // Client-supplied
      description: "Campus chapter communication email."
    },

    // Network / Ecosystem Destinations
    mulearnOrg: {
      label: "µLearn Official Website",
      url: "https://mulearn.org/",
      verified: true,
      description: "Parent organisation ecosystem site."
    },

    // What µLearn Offers (Network-Level Links)
    offers: {
      community: {
        label: "µLearn Community",
        url: "https://app.mulearn.org/",
        verified: true
      },
      mentors: {
        label: "µLearn Mentors",
        url: "https://app.mulearn.org/dashboard/search/mentors",
        verified: true
      },
      interestGroups: {
        label: "Interest Groups",
        url: "https://mulearn.org/interest-groups",
        verified: true
      },
      roadmaps: {
        label: "Learning Roadmaps",
        url: "https://app.mulearn.org/dashboard/mujourney",
        verified: true
      },
      challenges: {
        label: "Challenges & Karma",
        url: "https://app.mulearn.org/dashboard/mujourney",
        verified: true
      },
      opportunities: {
        label: "Career Opportunities",
        url: "https://mulearn.org/careers",
        verified: true
      }
    }
  };
})();
