/**
 * µLearn CHN — Memories & Community Photography Data
 * Curated from authentic community photographs taken at College of Engineering Chengannur.
 *
 * Rules:
 * - Only authentic photographs are included (graphic poster event5_zdu88j.jpg is rejected from memories).
 * - All GPS and camera metadata stripped in derivatives.
 * - Captions describe observable scenes accurately without inventing dates or achievements.
 */
(function () {
  window.MULEARN = window.MULEARN || {};

  window.MULEARN.memories = {
    // 6-frame editorial polaroid collage
    collage: [
      {
        slot: "p1",
        label: "Lab Session Overview",
        caption: "Hands-on coding session in the CEC computer lab",
        rotation: -4,
        aspect: 1.8,
        src460: "img/memories/collage-p1-460.webp",
        src920: "img/memories/collage-p1-920.webp",
        lightboxId: "lightbox-img-7834",
        alt: "Wide view of students engaged in coding session in the CEC computer lab"
      },
      {
        slot: "p2",
        label: "Mentored Workshop",
        caption: "Mentors guiding students through technical concepts",
        rotation: 3,
        aspect: 2.0,
        src460: "img/memories/collage-p2-460.webp",
        src920: "img/memories/collage-p2-920.webp",
        lightboxId: "lightbox-img-9803",
        alt: "Mentor guiding students in lab workstations during µLearn technical workshop"
      },
      {
        slot: "p3",
        label: "Community Gathering",
        caption: "Passionate learners gathered on campus",
        rotation: -3,
        aspect: 1.9,
        src460: "img/memories/collage-p3-460.webp",
        src920: "img/memories/collage-p3-920.webp",
        lightboxId: "lightbox-img-5086",
        alt: "Close-up of enthusiastic µLearn community members gathered on campus"
      },
      {
        slot: "p4",
        label: "Peer Collaboration",
        caption: "Students collaborating on projects and peer learning",
        rotation: 3,
        aspect: 1.8,
        src460: "img/memories/collage-p4-460.webp",
        src920: "img/memories/collage-p4-920.webp",
        lightboxId: "lightbox-img-7789",
        alt: "Students collaborating at computer desks during hands-on lab workshop"
      },
      {
        slot: "p5",
        label: "µLearn CHN Community",
        caption: "µLearn CHN community members at College of Engineering Chengannur",
        rotation: -2,
        aspect: 1.76,
        isMain: true,
        src460: "img/memories/collage-p5-460.webp",
        src920: "img/memories/collage-p5-920.webp",
        src1200: "img/memories/collage-p5-1200.webp",
        lightboxId: "lightbox-img-5086",
        alt: "µLearn CHN community group photo in front of College of Engineering Chengannur main building"
      },
      {
        slot: "p6",
        label: "Technical Demo",
        caption: "Live demonstrations and projector walkthroughs",
        rotation: 5,
        aspect: 1.1,
        src460: "img/memories/collage-p6-460.webp",
        src920: "img/memories/collage-p6-920.webp",
        lightboxId: "lightbox-img-7844",
        alt: "Instructors presenting technical demonstration on projector screen"
      }
    ],

    // Complete Lightbox Gallery (Full photographs + genuine event extractions)
    gallery: [
      {
        id: "lightbox-img-5086",
        title: "µLearn CHN Community Group",
        caption: "µLearn CHN student community members gathered in front of the College of Engineering Chengannur main building.",
        src: "img/memories/lightbox-img-5086.webp",
        width: 1600,
        height: 1067,
        category: "Community"
      },
      {
        id: "lightbox-img-7789",
        title: "Computer Lab Technical Session",
        caption: "Students participating in a hands-on technical workshop guided by student mentors.",
        src: "img/memories/lightbox-img-7789.webp",
        width: 1600,
        height: 1200,
        category: "Workshops"
      },
      {
        id: "lightbox-img-7834",
        title: "Computer Lab Working Session",
        caption: "Peer learning and collaborative development inside the college computer centre.",
        src: "img/memories/lightbox-img-7834.webp",
        width: 1600,
        height: 1200,
        category: "Workshops"
      },
      {
        id: "lightbox-img-7844",
        title: "Interactive Workshop & Demo",
        caption: "Live screen projections and interactive mentoring session for engineering students.",
        src: "img/memories/lightbox-img-7844.webp",
        width: 1600,
        height: 1200,
        category: "Workshops"
      },
      {
        id: "lightbox-img-9798",
        title: "Intro to Figma UI/UX Workshop",
        caption: "Design session focusing on Figma fundamentals and interface creation.",
        src: "img/memories/lightbox-img-9798.webp",
        width: 900,
        height: 1600,
        category: "Design"
      },
      {
        id: "lightbox-img-9803",
        title: "Mentored Coding Session",
        caption: "Hands-on coding and problem-solving with community mentors.",
        src: "img/memories/lightbox-img-9803.webp",
        width: 1600,
        height: 900,
        category: "Workshops"
      },
      // Genuine extracted event photographs
      {
        id: "photo-odyssey-wrap",
        title: "ODYSSEY Community Wrap",
        caption: "Hackathon participants and organizers celebrate at the conclusion of 32-hour ODYSSEY.",
        src: "img/events/photo-odyssey-wrap.webp",
        width: 615,
        height: 352,
        category: "ODYSSEY"
      },
      {
        id: "photo-odyssey-stage",
        title: "ODYSSEY Stage Session",
        caption: "Speaker addressing participants during ODYSSEY opening session.",
        src: "img/events/photo-odyssey-stage.webp",
        width: 507,
        height: 332,
        category: "ODYSSEY"
      },
      {
        id: "photo-buildathon-podium",
        title: "Buildathon Winners — Frustrated Devs",
        caption: "First place team Frustrated Devs receiving recognition at Buildathon (µFIFA × Gemma 4).",
        src: "img/events/photo-buildathon-podium.webp",
        width: 521,
        height: 312,
        category: "Buildathon"
      },
      {
        id: "photo-bwai-group",
        title: "Build with AI Group",
        caption: "Participants and mentors after the Build with AI workshop and hackathon.",
        src: "img/events/photo-bwai-group.webp",
        width: 618,
        height: 342,
        category: "Build with AI"
      },
      {
        id: "photo-useless-glimpses",
        title: "Useless Projects 3.0 Celebratory Evening",
        caption: "Participants sharing humorous and creative inventions during Useless Projects 3.0.",
        src: "img/events/photo-useless-glimpses.webp",
        width: 554,
        height: 330,
        category: "Useless Projects"
      }
    ]
  };
})();
