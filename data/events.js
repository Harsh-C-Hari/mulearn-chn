/**
 * µLearn CHN — Events & Initiatives data (Phase 5.1 reconciliation)
 * Single source of truth for the seven canonical events (Master Spec §7.4). Cards (5.2/5.3) and the detail dialog (5.4)
 * are rendered from this file; scripts/build_events.js writes the no-JS HTML between the markers in index.html.
 *
 * Rules
 *  - Past events only. Facts are poster-stated (Spec §7.4 + docs/events-audit.md). Nothing is inferred.
 *  - A field that is not known is OMITTED (never null placeholders in the UI, never invented years, venues or formats).
 *  - `dateLabel` is the short date shown on cards; `facts` / `lists` / `parts` are what the dialog may show.
 *  - `printed` = a line that is printed on the poster (quoted as printed).
 *  - `open` = unresolved questions. Internal: never rendered.
 *  - Images: derivatives only (img/events/*). `card` is the whole poster inside a 4:3 cream frame (Spec §9.4 rule 3).
 */
(function () {
  window.MULEARN = window.MULEARN || {};

  var CEC = "College of Engineering, Chengannur";

  window.MULEARN.events = [
    /* ======================= FEATURED (3) ======================= */
    {
      id: "event-odyssey", slug: "odyssey", title: "ODYSSEY", group: "featured", order: 1,
      descriptor: "A 32-hour event",
      printed: "32 hours. One journey. Endless possibilities.",
      dateLabel: "20–21 September 2026",
      facts: [
        { label: "Date", value: "20–21 September 2026" },
        { label: "Duration", value: "32 hours" },
        { label: "Venue", value: CEC },
        { label: "Prize pool", value: "₹15,000" },
        { label: "Registration fee", value: "₹150" },
        { label: "Registration", value: "MakeMyPass" }
      ],
      lists: [
        { label: "Podium", items: [
          { role: "Winner", name: "SPARX" },
          { role: "First runner-up", name: "Cypher" },
          { role: "Second runner-up", name: "Jijñāsus" } ] },
        { label: "Partners", items: [
          { role: "Technology partner", name: "Google for Developers" },
          { role: "Food partner", name: "Malabar Fresh" } ] },
        { label: "Mentors thanked", items: [
          { name: "Jerry Sanju Joanes" }, { name: "Abhijith J Nair" }, { name: "Joe Abraham K" } ] }
      ],
      branding: ["IEDC", "µLearn CHN", "Google for Developers"],
      image: {
        card: { src: "img/events/card-odyssey-405.webp", srcset: "img/events/card-odyssey-405.webp 405w, img/events/card-odyssey-600.webp 600w, img/events/card-odyssey-810.webp 810w", width: 405, height: 304 },
        poster: { src: "img/events/poster-odyssey.webp", width: 688, height: 805 },
        alt: "ODYSSEY poster: a rider and horse looking out over water at sunset, with the title ODYSSEY and the line “The Journey Within”."
      },
      photos: [
        { src: "img/events/photo-odyssey-stage.webp", width: 507, height: 332, alt: "A speaker at a podium beneath an ODYSSEY sign, with students seated in the foreground." },
        { src: "img/events/photo-odyssey-wrap.webp", width: 615, height: 352, alt: "A large group of ODYSSEY participants posed together in an open hall, many seated on the floor." }
      ],
      open: [
        "Duration: poster says 32 hours; a third-party Luma listing says 24 hours. Poster figure used (Spec §7.4).",
        "Registration fee ₹150 is small print on the poster (⚠️ Spec §7.4).",
        "Third-party listing names IEDC BOOTCAMP CEC as organiser: not on the poster, so not published; poster branding says IEDC."
      ]
    },
    {
      id: "event-buildathon", slug: "buildathon", title: "Buildathon", group: "featured", order: 2,
      descriptor: "µFIFA × Gemma 4",
      printed: "µFIFA × Gemma 4",
      dateLabel: "17–18 July",
      facts: [
        { label: "Date", value: "17–18 July" },
        { label: "Time", value: "5 PM – 9 AM" },
        { label: "Venue", value: CEC },
        { label: "Prize pool", value: "₹7K*" }
      ],
      lists: [
        { label: "Podium", items: [
          { role: "First place", name: "Frustrated Devs" },
          { role: "Second place", name: "Tek Knights" },
          { role: "Third place", name: "Holo" } ] },
        { label: "Partners", items: [
          { role: "Title sponsor", name: "BITA" },
          { name: "Mandi Mahal" }, { name: "The Chocolate Drop" }, { name: "V Fit Fitness Hub" },
          { name: "Juice It Up" }, { name: "Spinners" }, { name: "The Cowboy (“Penalty Pursuit”)" } ] }
      ],
      branding: ["µLearn CHN", "Google for Developers"],
      image: {
        card: { src: "img/events/card-buildathon-405.webp", srcset: "img/events/card-buildathon-405.webp 405w, img/events/card-buildathon-600.webp 600w, img/events/card-buildathon-810.webp 810w", width: 405, height: 304 },
        poster: { src: "img/events/poster-buildathon.webp", width: 693, height: 821 },
        alt: "Buildathon poster: µFIFA × Gemma 4, a golden trophy, and the venue, date (17–18 July) and time (5 PM–9 AM)."
      },
      photos: [
        { src: "img/events/photo-buildathon-podium.webp", width: 521, height: 312, alt: "Three students wearing lanyards, arms around each other, in front of large gold lettering on a wall." }
      ],
      open: [
        "Year is not printed on any poster. None is shown.",
        "The asterisk on ₹7K* is printed on the poster with no explanation: kept as printed, no explanation invented.",
        "BITA expanded name (Blaze International Trading Academy) is in earlier data but the spec lists only 'BITA (title sponsor)': only the short form is published."
      ]
    },
    {
      id: "event-bwai", slug: "bwai", title: "Build with AI", group: "featured", order: 3,
      descriptor: "A session and a 16-hour AI hackathon",
      dateLabel: "31 March and 6–7 April 2026",
      parts: [
        { title: "Session: Build a Gemini-Powered YouTube Summarizer",
          facts: [
            { label: "Date", value: "31 March 2026" },
            { label: "Time", value: "4–5:30 PM" },
            { label: "Venue", value: "MCA CC2" },
            { label: "Speakers", value: "Vishnu Harikumar and Swathy J" } ] },
        { title: "16-hour AI hackathon",
          facts: [
            { label: "Date", value: "6–7 April 2026" },
            { label: "Time", value: "5 PM – 9 AM" },
            { label: "Venue", value: "Maker’s Space & SDPK" },
            { label: "Duration", value: "16 hours" } ] }
      ],
      lists: [
        { label: "Project awards", items: [
          { role: "Winners", name: "Phoenix" },
          { role: "Creative", name: "Amingos" },
          { role: "Innovative", name: "Bizzare" } ] },
        { label: "Partners", items: [
          { role: "Associate partner", name: "PRODDEC" } ] }
      ],
      branding: ["µLearn", "Google for Developers", "MakeMyPass", "Notion", "PRODDEC"],
      image: {
        card: { src: "img/events/card-bwai-405.webp", srcset: "img/events/card-bwai-405.webp 405w, img/events/card-bwai-600.webp 600w, img/events/card-bwai-810.webp 810w", width: 405, height: 304 },
        poster: { src: "img/events/poster-bwai.webp", width: 693, height: 826 },
        alt: "Build with AI poster for the session “Build a Gemini-Powered YouTube Summarizer”, 31 March, 4.00–5.30 p.m., MCA CC2."
      },
      photos: [
        { src: "img/events/photo-bwai-group.webp", width: 618, height: 342, alt: "A large group of participants posed together in a hall, some standing and some seated on the floor." }
      ],
      open: [
        "Location conflict: a later poster shows the subtitle 'Alappuzha', earlier ones 'College of Engineering, Chengannur'. Unresolved → neither is published; only each activity's own printed venue (MCA CC2; Maker's Space & SDPK) is shown.",
        "Source does not establish the session and the hackathon as one continuous event: they are presented as two separate activities under one name.",
        "Thanks to Abhijith J Nair and Jithu Girish ('Intro to Vibe Coding') appear in the source but their role is a thank-you line; not published as speakers/mentors."
      ]
    },

    /* ======================= COMPACT (4) ======================= */
    {
      id: "event-techforge", slug: "techforge", title: "Tech Forge", group: "compact", order: 4,
      descriptor: "Title card: TECHFORGE 2.0",
      printed: "TECHFORGE 2.0",
      dateLabel: "",
      facts: [],
      image: {
        card: { src: "img/events/card-techforge-405.webp", srcset: "img/events/card-techforge-405.webp 405w, img/events/card-techforge-810.webp 810w", width: 405, height: 304 },
        poster: { src: "img/events/techforge-title.webp", width: 496, height: 638 },
        alt: "An animated title card reading TECHFORGE 2.0 in glowing orange pixel letters on a dark background."
      },
      open: [
        "The only verified fact is the title card text 'TECHFORGE 2.0'. No date, venue, format, description or winners are known: none are published. Earlier data carried a venue (CEC) that no source supports: removed in 5.1."
      ]
    },
    {
      id: "event-typerace", slug: "typerace", title: "Type Race", group: "compact", order: 5,
      descriptor: "Where speed meets precision",
      printed: "Where speed meets precision",
      dateLabel: "26 March 2026",
      facts: [
        { label: "Date", value: "26 March 2026" },
        { label: "Time", value: "12:15–1 PM" },
        { label: "Venue", value: "CC2" },
        { label: "Prize pool", value: "₹1,500" },
        { label: "Registration fee", value: "₹20" },
        { label: "Free entry", value: "µLearners with 7K+ Karma points and IEEE CS members (5 seats)" }
      ],
      lists: [
        { label: "Winners", items: [
          { name: "Christo Chery George" }, { name: "Nevin Mathew" }, { name: "Niranjan V Chandran" } ] }
      ],
      branding: ["IEEE SB CEC", "IEEE Computer Society", "µLearn CHN"],
      image: {
        card: { src: "img/events/card-typerace-405.webp", srcset: "img/events/card-typerace-405.webp 405w, img/events/card-typerace-600.webp 600w, img/events/card-typerace-810.webp 810w", width: 405, height: 304 },
        poster: { src: "img/events/poster-typerace.webp", width: 696, height: 822 },
        alt: "Type Race poster: a blueprint-style design with a keyboard, the title Type Race and the line “Where speed meets precision”."
      },
      open: [
        "Eligibility wording must stay as printed: free for µLearners with 7K+ Karma points and IEEE CS members, five seats. The poster does not say whether the five seats are shared or per group."
      ]
    },
    {
      id: "event-useless", slug: "useless", title: "Useless Projects 3.0", group: "compact", order: 6,
      descriptor: "Third edition · creative, deliberately non-useful projects",
      dateLabel: "11–12 September",
      facts: [
        { label: "Edition", value: "Third edition" },
        { label: "Date", value: "11–12 September" },
        { label: "Theme", value: "Creative, deliberately non-useful projects" }
      ],
      branding: ["TinkerHub CE Chengannur", "µLearn CHN"],
      image: {
        card: { src: "img/events/card-useless-405.webp", srcset: "img/events/card-useless-405.webp 405w, img/events/card-useless-600.webp 600w, img/events/card-useless-810.webp 810w", width: 405, height: 304 },
        poster: { src: "img/events/poster-useless.webp", width: 692, height: 816 },
        alt: "Useless Projects 3.0 poster with colourful falling blocks and the dates September 11–12."
      },
      photos: [
        { src: "img/events/photo-useless-glimpses.webp", width: 554, height: 330, alt: "Students in matching light-blue shirts standing in rows in a classroom for a group photo." }
      ],
      open: [
        "Year is not printed: none is shown.",
        "No winners are named in the source material.",
        "Earlier data listed the venue as CEC; no source states it: removed in 5.1."
      ]
    },
    {
      id: "event-webslingers", slug: "webslingers", title: "Web Slingers", group: "compact", order: 7,
      descriptor: "Podium: Marvel Jesus, Titans, Cosmopolitans",
      dateLabel: "27 October",
      facts: [
        { label: "Date", value: "27 October" },
        { label: "Time", value: "4:00–5:15 PM" },
        { label: "Venue", value: "SDPK Room 204" }
      ],
      lists: [
        { label: "Podium", items: [
          { role: "First place", name: "Marvel Jesus" },
          { role: "Second place", name: "Titans" },
          { role: "Third place", name: "Cosmopolitans" } ] }
      ],
      branding: ["µLearn CHN"],
      image: {
        card: { src: "img/events/card-webslingers-405.webp", srcset: "img/events/card-webslingers-405.webp 405w, img/events/card-webslingers-600.webp 600w, img/events/card-webslingers-810.webp 810w", width: 405, height: 304 },
        poster: { src: "img/events/poster-webslingers.webp", width: 650, height: 831 },
        alt: "Web Slingers poster with the title in red-and-white web lettering over a blue map-style panel."
      },
      open: [
        "Year is not printed: none is shown.",
        "Poster text for date/time/venue is small and was read by OCR (Spec §7.4 'not reliably read'); the register values (27 October, 4:00–5:15 PM, SDPK Room 204) are used. Client to confirm."
      ]
    }
  ];
})();
