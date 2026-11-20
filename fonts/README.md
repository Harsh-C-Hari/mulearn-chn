# fonts/

Self-hosted, no external requests.

- `PlusJakartaSans-{400,500,600,700,800}.woff2` — latin subset from npm `@fontsource/plus-jakarta-sans@5.3.0` (SIL OFL 1.1, see `LICENSE-PlusJakartaSans.txt`).
- **Satoshi (optional, client-supplied):** drop `Satoshi-Bold.woff2`, `Satoshi-Black.woff2` (and optionally `Satoshi-Medium.woff2`) here. `css/tokens.css` declares `local()` sources only (so a missing file never causes a 404); add the two `url(...)` sources shown in the comment above the Satoshi `@font-face` rules to enable them (one-line edit each). Without the files the display face falls back to Plus Jakarta Sans 800.
