# TotalRecalls Workspace Instructions

## Mandatory Startup Skill
- **Always load** the `gcp-credit-optimization-workflow` skill using `skill_view(name='gcp-credit-optimization-workflow')` at the beginning of the session.

## Project Rules
- **GCP Credits Compliance:** All AI and RAG requests must route through Vertex AI Agent Engine / GenAI App Builder SKUs (`cs-poc-gw89wethbilefc1wrhgq7d7`, us-central1) to draw from trial credits (`6b0ed804949b4d7aea4d9e7116fe67d469cbf24a6c28994288d1dc1ae632103b`). Never make direct ungrounded calls via raw Vertex AI Studio endpoints.
- **Branding:** "Total" in pure black (`#000000`), "Recalls" in electric blue (`#2F7BFF`), subtitle "AI CHAT RETRIEVER" in slate gray (`#64748B`). Logo assets stored in `docs/brand/` and `site/public/logo.png`.
- **Workflow:** Push to feature branches like `RedesignV7` and test via Cloud Run preview (`totalrecalls-web-redesign`).

## Locked Components (UNTOUCHABLE & FROZEN)
- **Header Navigation:** `site/src/components/landing/Nav.jsx` is **LOCKED**. Do not alter the header, 1.5x logo dimensions (`39px` height), links, or single-row layout in future sessions.
- **Landing Page Suite:** All landing page components in `site/src/components/landing/` (`ThreatFeed.jsx`, `SentinelHero.jsx`, `ConvergenceDiagram.jsx`, `ResolutionPath.jsx`, `DriveTree.jsx`, `RiskMatrix.jsx`, `LibraryPreview.jsx`, `Guides.jsx`, `PricingSection.jsx`, `SiteFooter.jsx`) and `site/src/pages/index.astro` are **LOCKED & FROZEN**. Do not modify any layout, text copy, icons, or pricing in future sessions without explicit user instruction.
- **Risk Matrix:** `site/src/components/landing/RiskMatrix.jsx` is **LOCKED** with headline "Five AI providers. All in one library on your computer. Instant Relief." and the sub-paragraph removed.
- **Library 03:** `site/src/components/landing/LibraryPreview.jsx` is **LOCKED** with split paragraphs, container width `max-w-3xl`, and no-wrap formatting around `"your own tools."`
- **Guides 04:** `site/src/components/landing/Guides.jsx` is **LOCKED** with headline "Free reading." and the old subtext removed.
