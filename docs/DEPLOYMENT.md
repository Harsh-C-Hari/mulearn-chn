# µLearn CHN — Vercel Deployment Guide & Handoff

**Project:** µLearn CHN Official Community Website  
**Repository:** [https://github.com/Harsh-C-Hari/mulearn-chn](https://github.com/Harsh-C-Hari/mulearn-chn)  
**Production Branch:** `main`  
**Hosting Target:** Vercel (Static Web Architecture)  
**Date:** 2026-11-20  

---

## 1. Verified Vercel Configuration Settings

Because the GitHub repository `Harsh-C-Hari/mulearn-chn` is a standalone repository with `index.html` at the top level, Vercel requires **zero build tooling and zero runtime dependencies**.

| Setting | Value / State | Verification Note |
|---|---|---|
| **Framework Preset** | `Other` | Static site without a build step or framework wrapper |
| **Root Directory** | `./` (leave blank) | `index.html` resides directly at repository root |
| **Build Command** | *None* (override / empty) | No build step, bundler, or compiler is required |
| **Output Directory** | *None* / `.` (override / empty) | Static root is served directly |
| **Install Command** | *None* (override / empty) | No `npm install` or package manager required |
| **Node.js Version** | Default | No serverless functions or Node scripts execute at runtime |
| **Environment Variables** | *None* | Zero API keys, database credentials, or runtime secrets required |

---

## 2. Path & Asset Architecture Audit

* **Static Asset Paths**: All CSS, JS, font, image, and data references in `index.html` and `styleguide.html` are strictly relative (`css/...`, `js/...`, `fonts/...`, `img/...`, `data/...`, `vendor/...`). Zero root-relative paths (`/css/...`) are used, ensuring the site works flawlessly on custom domains or preview staging URLs.
* **Fonts**: Self-hosted Plus Jakarta Sans WOFF2/WOFF files in `fonts/`. Zero Google Fonts or external CDN requests.
* **Motion**: Vendored GSAP 3.15.1 and ScrollTrigger in `vendor/gsap/`. Zero CDN runtime dependencies.
* **Images**: 96 pre-rendered WebP derivatives in `img/` matching approved responsive breakpoints (480w, 800w, 1200w). Zero external image hosting.
* **Secondary Pages**: Living design system accessible at `/styleguide.html`.

---

## 3. Optional `vercel.json` Security & Cache Configuration

A `vercel.json` is **not required** for deployment because Vercel automatically serves static HTML, CSS, JS, and image assets with standard MIME types and automatic HTTPS.

However, if you wish to enforce hardened security headers and immutable asset caching, the following minimal, verified `vercel.json` may be added:

```json
{
  "cleanUrls": true,
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "X-Frame-Options", "value": "SAMEORIGIN" },
        { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" },
        { "key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=()" }
      ]
    },
    {
      "source": "/(fonts|img|vendor)/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }
      ]
    },
    {
      "source": "/(.*).(html)?$",
      "headers": [
        { "key": "Cache-Control", "value": "public, max-age=0, must-revalidate" }
      ]
    }
  ]
}
```

> **Security Note:** Content Security Policy (CSP) is intentionally omitted from the initial headers to prevent accidental disruption of inline SVG symbols, theme scripts, and motion timelines.

---

## 4. Manual Deployment Instructions for Vercel

Follow these exact steps in your Vercel Dashboard when ready to deploy:

1. **Log in to Vercel**: Navigate to [vercel.com](https://vercel.com) and log in with your GitHub account (`Harsh-C-Hari`).
2. **Add New Project**:
   - Click **Add New...** → **Project**.
   - Under **Import Git Repository**, locate `mulearn-chn` and click **Import**.
3. **Configure Project**:
   - **Project Name**: `mulearn-chn` (or your preferred project slug).
   - **Framework Preset**: Select **Other**.
   - **Root Directory**: Leave as `./` (default).
   - **Build and Output Settings**:
     - *Build Command*: Leave empty (or toggle Override on with empty input).
     - *Output Directory*: Leave empty.
     - *Install Command*: Leave empty (or toggle Override on with empty input).
   - **Environment Variables**: Leave empty.
4. **Deploy**:
   - Click **Deploy**.
   - Deployment typically takes under 15 seconds for this static site.
5. **Custom Domain Setup (Optional)**:
   - Navigate to **Project Settings** → **Domains**.
   - Add your custom domain (e.g., `mulearn.ceconline.edu` or `mulearn-chn.org`).
   - Configure the DNS `CNAME` or `A` records per Vercel's prompt. SSL certificates are provisioned automatically.

---

## 5. Post-Deployment Verification Checklist

Upon deployment, verify the live deployment against this checklist:

- [ ] **Home Page Loads**: Confirm `https://<project-slug>.vercel.app/` renders with warm cream background, bold typography, and navy outlines.
- [ ] **No Console Errors**: Open DevTools Console; confirm 0 JavaScript errors and 0 missing file warnings.
- [ ] **Navigation & Smooth Scrolling**: Click header links (`About`, `Offers`, `Events`, `Team`, `Memories`, `Join`); confirm in-page smooth scrolling to each section.
- [ ] **Event Detail Modal**: Click "View Details" on any event card; confirm `<dialog id="event-dialog">` opens with background backdrop, focus trap, and closes on `Esc` or close button.
- [ ] **Team Directory Filter**: In the Team section, click "View all 21 members"; filter by roles (`All`, `Core`, `Leads`, `Content & Media`, `Design`, `Interest Groups`).
- [ ] **Memories Collage & Lightbox**: In the Memories section, click any photo in the 6-frame collage or open the 11-item community gallery drawer; confirm the `<dialog id="memories-lightbox">` opens, arrow keys (`←`/`→`) step through images, and image preloading functions smoothly.
- [ ] **Living Styleguide**: Visit `https://<project-slug>.vercel.app/styleguide.html` and confirm design tokens, components, and accessibility chips render properly.
- [ ] **Continuous Link Underlines**: Hover links (Offers, Join, Footer) and confirm continuous underline through descenders (`g`, `y`, `p`, `q`, `@`, `.`) with zero gaps.

---

## 6. Rollback & Redeployment Procedures

* **Automatic Continuous Deployment**: Every normal `git push` to `main` on GitHub triggers an instant preview and production deployment.
* **Instant Rollback**: If an unexpected regression occurs in production, open the **Deployments** tab in the Vercel Dashboard, locate the previous stable deployment, click the `...` menu, and select **Rollback to this Deployment**. Rollback takes effect globally within 1 second.
