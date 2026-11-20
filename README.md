# µLearn CHN Website

Official website for the **µLearn chapter at College of Engineering Chengannur (CEC)**.

A playful neo-brutalist editorial static single-page web experience showcasing community offerings, technical events, community leads, interest groups, and milestone memories.

---

## Technology Stack

* **Markup & Structure**: Semantic HTML5 (native `<dialog>`, `<picture>`, `<svg>` symbols).
* **Styling**: Modern CSS with CSS custom properties (design tokens), CSS Grid, Flexbox, and fluid typography. Zero CSS frameworks.
* **Scripting**: Modular Vanilla JavaScript (ES modules and classic scripts). Zero frontend frameworks.
* **Motion**: Locally vendored GSAP 3.15.1 and ScrollTrigger with strict `prefers-reduced-motion` compliance.
* **Typography**: Self-hosted Plus Jakarta Sans (`.woff2` / `.woff`). Zero external font CDNs.
* **Assets**: Fully local WebP image derivatives and inline/symbol SVG icons. Zero third-party runtime requests.

---

## Repository Structure

```
.
├── index.html           # Production homepage
├── styleguide.html      # Living design system & accessibility showcase
├── css/                 # Design tokens, base, layout, components, and section CSS
├── js/                  # Interaction modules, lightbox, dialogs, motion guard
├── img/                 # 96 optimized WebP derivatives and UI SVG sprite
├── fonts/               # Self-hosted Plus Jakarta Sans font files
├── vendor/              # Vendored GSAP and ScrollTrigger libraries
├── data/                # Verified community data (events, team, memories, links)
├── docs/                # Architecture specifications, accessibility audits, logs
├── scripts/             # Deterministic verification and data build scripts
├── ASSET_MANIFEST.md    # Approved asset inventory and hashes
├── ASSET_MAPPING.md     # Source-to-derivative resolution mapping
├── .gitignore           # Repository ignore rules
└── README.md            # Project documentation
```

---

## Deployment Platform: Vercel

The website is designed for deployment on **Vercel** as a static site:

* **Framework Preset**: `Other`
* **Build Command**: None (leave empty)
* **Output Directory**: `.` (leave empty)
* **Install Command**: None (leave empty)

---

## Local Development & Preview

Serve the website locally with any static web server:

```bash
# Start a local HTTP server
python -m http.server 8000
```

Open `http://localhost:8000/` in your browser. The design system showcase is available at `http://localhost:8000/styleguide.html`.

---

## Verification & Integrity Checks

Run the verification suite from the project root:

```bash
# Verify 96/96 image derivatives and manifest integrity
python scripts/verify_project.py

# Verify synchronization between data/ and index.html
node scripts/build_events.js --check
node scripts/build_team.js --check
node scripts/build_memories.js --check
```

---

## Documentation

* [Master Project Specification](docs/PROJECT_MASTER_SPEC.md)
* [Current Project State](docs/PROJECT_STATE.md)
* [Change Log](docs/CHANGELOG.md)
* [Accessibility Report](docs/accessibility-report.md)
