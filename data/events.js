/**
 * µLearn CHN — Events & Initiatives Data
 * Verified against original poster artwork and OCR extractions per Spec §7.4.
 *
 * Rules:
 * - Past events only (all events in materials occurred in the past; no 'upcoming' claims).
 * - Only facts printed on posters or verified independently are published.
 * - Missing years or venues are left null or noted explicitly.
 */
(function () {
  window.MULEARN = window.MULEARN || {};

  window.MULEARN.events = [
    // === FEATURED EVENTS (3) ===
    {
      id: "event-odyssey",
      slug: "odyssey",
      title: "ODYSSEY",
      tagline: "32 Hours. One Journey. Endless Possibilities.",
      format: "32-Hour Hackathon",
      date: "20–21 September 2026",
      year: 2026,
      venue: "College of Engineering Chengannur",
      prizePool: "₹15,000",
      registrationFee: "₹150",
      isFeatured: true,
      cardImage: "img/events/card-odyssey-405.webp",
      cardImageMax: "img/events/card-odyssey-600.webp",
      posterImage: "img/events/poster-odyssey.webp",
      galleryPhotos: [
        {
          src: "img/events/photo-odyssey-wrap.webp",
          caption: "ODYSSEY Hackathon Community Wrap Crowd"
        },
        {
          src: "img/events/photo-odyssey-stage.webp",
          caption: "ODYSSEY Speaker Session on Stage"
        }
      ],
      collaborators: [
        "IEDC BOOTCAMP CEC",
        "µLearn CHN",
        "Google for Developers"
      ],
      partners: [
        "MakeMyPass (Ticketing)",
        "Malabar Fresh (Food Partner)"
      ],
      winners: [
        { rank: "1st Place", team: "Team SPARX" },
        { rank: "1st Runner-Up", team: "Team Cypher" },
        { rank: "2nd Runner-Up", team: "Team Jijñāsus" }
      ],
      mentors: [
        "Jerry Sanju Joanes",
        "Abhijith J Nair",
        "Joe Abraham K"
      ],
      verified: true,
      notes: "Organised jointly by IEDC BOOTCAMP CEC and µLearn CHN with Google for Developers."
    },
    {
      id: "event-buildathon",
      slug: "buildathon",
      title: "Buildathon",
      tagline: "µFIFA × Gemma 4",
      format: "Overnight Hackathon",
      date: "17–18 July",
      year: null, // Year unconfirmed on supplied poster
      time: "5:00 PM – 9:00 AM",
      venue: "College of Engineering Chengannur",
      prizePool: "₹7,000*",
      isFeatured: true,
      cardImage: "img/events/card-buildathon-405.webp",
      cardImageMax: "img/events/card-buildathon-600.webp",
      posterImage: "img/events/poster-buildathon.webp",
      galleryPhotos: [
        {
          src: "img/events/photo-buildathon-podium.webp",
          caption: "First Place Podium — Team Frustrated Devs"
        }
      ],
      collaborators: [
        "µLearn CHN",
        "Google for Developers"
      ],
      partners: [
        "Blaze International Trading Academy (BITA - Title Sponsor)",
        "Mandi Mahal (Food Partner)",
        "The Chocolate Drop (Refreshment Partner)",
        "V Fit Fitness Hub (Fitness Partner)",
        "Juice It Up (Prize Sponsor)",
        "Spinners (Co-Food Partner)",
        "The Cowboy (Penalty Pursuit)"
      ],
      winners: [
        { rank: "1st Place", team: "Frustrated Devs" },
        { rank: "2nd Place", team: "Tek Knights" },
        { rank: "3rd Place", team: "Holo" }
      ],
      verified: true,
      notes: "Year not printed on posters; July 17-18 verified from poster."
    },
    {
      id: "event-bwai",
      slug: "bwai",
      title: "Build with AI",
      tagline: "Workshops, Vibe Coding & 16-Hour AI Hackathon",
      format: "Workshop Series & Hackathon",
      date: "31 March & 6–7 April 2026",
      year: 2026,
      venue: "MCA CC2 & Maker's Space / SDPK",
      prizePool: null,
      isFeatured: true,
      cardImage: "img/events/card-bwai-405.webp",
      cardImageMax: "img/events/card-bwai-600.webp",
      posterImage: "img/events/poster-bwai.webp",
      sessions: [
        {
          name: "Build a Gemini-Powered YouTube Summarizer",
          date: "31 March 2026",
          time: "4:00 PM – 5:30 PM",
          venue: "MCA CC2"
        },
        {
          name: "16-hr AI Hackathon",
          date: "6–7 April 2026",
          time: "5:00 PM – 9:00 AM",
          venue: "Maker's Space & SDPK"
        }
      ],
      galleryPhotos: [
        {
          src: "img/events/photo-bwai-group.webp",
          caption: "Build with AI Participants & Mentors Group"
        }
      ],
      collaborators: [
        "µLearn CHN",
        "Google for Developers"
      ],
      partners: [
        "MakeMyPass",
        "PRODDEC (Associate Partner)",
        "Notion"
      ],
      speakers: [
        "Vishnu Harikumar",
        "Swathy J"
      ],
      mentors: [
        "Abhijith J Nair",
        "Jithu Girish (Intro to Vibe Coding)"
      ],
      winners: [
        { rank: "Winners", team: "Phoenix" },
        { rank: "Creative Project", team: "Amingos" },
        { rank: "Innovative Project", team: "Bizzare" }
      ],
      verified: true,
      notes: "Two-stage event: technical workshop on 31 March, followed by overnight hackathon on 6-7 April."
    },

    // === COMPACT EVENTS (4) ===
    {
      id: "event-techforge",
      slug: "techforge",
      title: "Tech Forge 2.0",
      tagline: "Technical Innovation & Building Initiative",
      format: "Technical Initiative",
      date: null, // No dates on-screen
      year: null,
      venue: "College of Engineering Chengannur",
      prizePool: null,
      isFeatured: false,
      cardImage: "img/events/card-techforge-405.webp",
      cardImageMax: "img/events/card-techforge-405.webp",
      posterImage: "img/events/poster-techforge.webp",
      collaborators: [
        "µLearn CHN"
      ],
      partners: [],
      winners: [],
      verified: true,
      notes: "Visual asset extracted from official TECHFORGE 2.0 title frame recording. Dates unspecified."
    },
    {
      id: "event-typerace",
      slug: "typerace",
      title: "Type Race",
      tagline: "Where Speed Meets Precision",
      format: "Typing Speed Competition",
      date: "26/03/2026",
      year: 2026,
      time: "12:15 PM – 1:00 PM",
      venue: "CC2",
      prizePool: "₹1,500",
      registrationFee: "₹20 (Free for µLearners with 7K+ Karma & IEEE CS members)",
      isFeatured: false,
      cardImage: "img/events/card-typerace-405.webp",
      cardImageMax: "img/events/card-typerace-600.webp",
      posterImage: "img/events/poster-typerace.webp",
      collaborators: [
        "IEEE SB CEC",
        "IEEE Computer Society",
        "µLearn CHN"
      ],
      partners: [],
      winners: [
        "Christo Chery George",
        "Nevin Mathew",
        "Niranjan V Chandran"
      ],
      verified: true,
      notes: "Jointly organized with IEEE Student Branch CEC and IEEE Computer Society."
    },
    {
      id: "event-useless",
      slug: "useless",
      title: "Useless Projects 3.0",
      tagline: "The weirder the idea, the better your chances.",
      format: "Creative Hackathon",
      date: "September 11–12",
      year: null, // Year unconfirmed on poster
      venue: "College of Engineering Chengannur",
      prizePool: null,
      isFeatured: false,
      cardImage: "img/events/card-useless-405.webp",
      cardImageMax: "img/events/card-useless-600.webp",
      posterImage: "img/events/poster-useless.webp",
      galleryPhotos: [
        {
          src: "img/events/photo-useless-glimpses.webp",
          caption: "Useless Projects 3.0 Celebratory Evening Group"
        }
      ],
      collaborators: [
        "TinkerHub CE Chengannur",
        "µLearn CHN"
      ],
      partners: [],
      winners: [],
      verified: true,
      notes: "Celebrates creative engineering with deliberately non-useful software and hardware."
    },
    {
      id: "event-webslingers",
      slug: "webslingers",
      title: "Web Slingers",
      tagline: "Web Development Challenge",
      format: "Web Development Competition",
      date: "27th October",
      year: null,
      time: "4:00 PM – 5:15 PM",
      venue: "SDPK",
      prizePool: null,
      isFeatured: false,
      cardImage: "img/events/card-webslingers-405.webp",
      cardImageMax: "img/events/card-webslingers-600.webp",
      posterImage: "img/events/poster-webslingers.webp",
      collaborators: [
        "µLearn CHN"
      ],
      partners: [],
      winners: [
        { rank: "1st Place", team: "Marvel Jesus" },
        { rank: "2nd Place", team: "Titans" },
        { rank: "3rd Place", team: "Cosmopolitans" }
      ],
      verified: true,
      notes: "Verified via high-resolution OCR from poster artwork (venue SDPK, time 4:00 PM - 5:15 PM)."
    }
  ];
})();
