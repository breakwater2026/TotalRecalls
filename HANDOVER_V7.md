# HANDOVER NOTE — TotalRecalls V7 Redesign Session

**Date:** August 15, 2026  
**Repository:** `C:\Users\break\Projects\TotalRecalls`  
**Active Branch:** `RedesignV7`  

---

## 1. Locked Navigation Header & Landing Page (UNTOUCHABLE & FROZEN)
- **Header:** `site/src/components/landing/Nav.jsx` (LOCKED)
  - 1.5x scaled logo (`39px` height)
  - Single-row alignment
  - `Buy — $24USD` + `discounted launch price` subtext
- **Landing Page Suite:** All 9 components in `site/src/components/landing/` and `site/src/pages/index.astro`:
  1. `ThreatFeed.jsx` — Live Feed ticker
  2. `Nav.jsx` — Header (LOCKED)
  3. `SentinelHero.jsx` — Hero with CTA buttons and `discounted launch price · one-time` subtext
  4. `ConvergenceDiagram.jsx` — Live schematic with centered `CONVERGENCE · LIVE`, zero-gap flow lines, and authentic provider brand logos/colors (ChatGPT, Claude, Perplexity, Gemini, Grok)
  5. `ResolutionPath.jsx` — Resolution Path 01 4-step grid + sticky `DriveTree.jsx`
  6. `RiskMatrix.jsx` — Risk Matrix 02 3-column matrix
  7. `LibraryPreview.jsx` — Library 03 split file explorer + Markdown preview
  8. `Guides.jsx` — Guides 04 (5 guide rows)
  9. `PricingSection.jsx` — Resolution 05 ($24USD + electric blue `DISCOUNTED LAUNCH PRICE`)
  10. `SiteFooter.jsx` — 4-column footer
- **Directive:** **Do NOT modify any header or landing page components in future sessions without explicit user instruction.**

---

## 2. Build & Preview Status
- `npm run build` inside `site/` passes cleanly (exit code 0).
- Local preview server running via `python site/serve_nocache.py` on `http://localhost:4321/` with no-cache headers.
