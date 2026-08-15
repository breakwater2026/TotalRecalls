# HANDOVER NOTE — TotalRecalls V7 Redesign Session

**Date:** August 15, 2026  
**Repository:** `C:\Users\break\Projects\TotalRecalls`  
**Active Branch:** `RedesignV7`  

---

## 1. Locked Navigation Header (UNTOUCHABLE)
- **File:** `site/src/components/landing/Nav.jsx`
- **Status:** **LOCKED & FROZEN**
- **Specs:**
  - Sticky header (`h-16`, `64px`)
  - Scaled logo (`/logo.png`, `39px` height, 1.5x scale)
  - Single-row layout containing logo, navigation links ("How It Works", "Providers", "Library", "Guides", "Pricing"), "Download", and "Buy — $24" CTA button.
  - **Do NOT modify without explicit user instruction.**

---

## 2. Complete Fresh 1:1 Base44 Architecture
- Pure React components mounted directly in Astro (`site/src/components/landing/*.jsx`):
  1. `ThreatFeed.jsx` — Live Feed ticker
  2. `Nav.jsx` — Navigation header (LOCKED)
  3. `SentinelHero.jsx` — Hero + `ConvergenceDiagram.jsx`
  4. `ResolutionPath.jsx` — Resolution Path · 01 + `DriveTree.jsx`
  5. `RiskMatrix.jsx` — Risk Matrix · 02 (with hover forensic inspector)
  6. `LibraryPreview.jsx` — Library · 03 split file tree + Markdown preview
  7. `Guides.jsx` — Guides · 04 (5 guide rows)
  8. `PricingSection.jsx` — Resolution · 05 ($24 launch pricing + Straight Talk)
  9. `SiteFooter.jsx` — 4-column footer
- All previous contaminated `.astro` components in `v6/` were purged.
- `@astrojs/react` and `tailwindcss` (v3.4) handle native hydration.

---

## 3. Verification & Build Status
- `npm run build` inside `site/` builds cleanly (exit code 0).
- Visually verified across all sections via `browser_vision`.
