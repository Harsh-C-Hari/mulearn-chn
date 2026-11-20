# events-audit.md — Phase 5.1 event data audit

Source of truth: `docs/PROJECT_MASTER_SPEC.md` §7.4 (poster-stated facts) + the Phase 5 master prompt §4. Data: `data/events.js`
(rendered into `index.html` by `scripts/build_events.js`; guarded by `scripts/test_phase5.py`).

## Reconciliation of the seven canonical events
| # | Event | Group | Published (facts) | Removed / not published | Open |
|---|---|---|---|---|---|
| 1 | ODYSSEY | featured | 20–21 Sep 2026 · 32 hours · College of Engineering, Chengannur · prize ₹15,000 · fee ₹150 · MakeMyPass · podium SPARX / Cypher / Jijñāsus · Google for Developers (technology partner) · Malabar Fresh (food partner) · mentors thanked · poster line "32 hours. One journey. Endless possibilities." | "Team " prefix on winners; "organised by IEDC BOOTCAMP CEC" (third-party listing only; poster branding says IEDC); 24-hour figure | Poster 32 h vs Luma 24 h (poster used); ₹150 is small print |
| 2 | Buildathon | featured | µFIFA × Gemma 4 · 17–18 July · 5 PM–9 AM · College of Engineering, Chengannur · prize ₹7K* · podium Frustrated Devs / Tek Knights / Holo · partners as in Spec §7.4 | "Overnight Hackathon" format label (not poster text); ₹7,000 expansion of "₹7K*"; BITA long name | **Year not printed**; meaning of the asterisk unknown |
| 3 | Build with AI | featured | Two separate parts. Session "Build a Gemini-Powered YouTube Summarizer": 31 Mar 2026, 4–5:30 PM, MCA CC2, speakers Vishnu Harikumar and Swathy J. 16-hour AI hackathon: 6–7 Apr 2026, 5 PM–9 AM, Maker's Space & SDPK. Awards: Phoenix (winners), Amingos (creative), Bizzare (innovative). Associate partner PRODDEC | Any "CEC" or "Alappuzha" location; "Workshop Series" label; mentors list (thank-you line only) | **Location conflict unresolved** (Alappuzha vs CEC) → omitted |
| 4 | Tech Forge | compact | Title card text "TECHFORGE 2.0" only | Venue (was "College of Engineering Chengannur", unsupported), format, tagline "Technical Innovation & Building Initiative" | Date, venue, format, winners: client must supply |
| 5 | Type Race | compact | CC2 · 26 Mar 2026 · 12:15–1 PM · prize ₹1,500 · fee ₹20 · free entry for µLearners with 7K+ Karma points and IEEE CS members (5 seats) · winners Christo Chery George, Nevin Mathew, Niranjan V Chandran | "Typing Speed Competition" label | Poster does not say if the five seats are shared |
| 6 | Useless Projects 3.0 | compact | Third edition · 11–12 September · creative, deliberately non-useful projects | Venue "CEC" (unsupported), "Creative Hackathon" label | **Year not printed**; no winners named |
| 7 | Web Slingers | compact | 27 October · 4:00–5:15 PM · SDPK Room 204 · podium Marvel Jesus / Titans / Cosmopolitans | — | **Year not printed**; poster text small, OCR-read (Spec "not reliably read") → client to confirm |

## Asset findings (for 5.2)
- Cards are whole-poster-in-frame (4:3 cream canvas, Spec §9.4 rule 3). Posters: no text cropped.
- **Instagram carousel chrome** (a small "›" arrow on the right edge) is visible in `poster-odyssey.webp`, `card-odyssey-*.webp` and `card-buildathon-*.webp`. Fix in 5.2 by repainting the arrow area in the derivatives (flat background patch), not by cropping.
- `photo-buildathon-podium.webp` shows partial signage lettering behind three students; its alt text describes only what is visible. Not used as proof of venue.
- Tech Forge frame is a video still; used as a title-card treatment.

## Data-structure decisions (5.1)
- Group + order in data (`group: featured|compact`, `order`), so the page, dialog and tests share one source.
- Unknown values are omitted, never `null` in the UI. `dateLabel` empty for Tech Forge.
- `facts[]` {label,value}; `lists[]` {label, items[{role?,name}]}; `parts[]` for Build with AI; `open[]` internal only.
- No-JS fallback: `scripts/build_events.js` writes the cards into `index.html` between markers; 5.4 adds the dialog layer in JS on top.
- Instagram "›" chip removed from the ODYSSEY and Buildathon poster/card derivatives in 5.2 (inpainted, same filenames).
