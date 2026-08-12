# 33 — Rewrite Decision Record + V2 Folder Structure + Design System

**Source:** Thread "Rewrite vs patch" advice (L3864–4124), V2 folder structure (L4153–4258), Design System (L4260–4417), Astro skeleton (L5487–5785). Curated conclusions.

## Decision: complete rewrite, not patch

The thread's explicit conclusion (L3875–3876, L4122–4124): **do a complete rewrite from scratch.** Not because V1 is bad, but because V2 changes positioning, pricing, narrative, trust model, roadmap, SEO strategy, conversion funnel, and documentation structure. Patching would create duplicated sections, mismatched tone, inconsistent navigation, broken flow, and SEO fragmentation.

**Workflow conclusions (thread L4662–4674, L7350–7353):**
- Gemini (2.5 Pro / now 3.5 Flash) = content generation engine
- Grok = architecture, code, deployment
- DeepSeek = optional reasoning specialist (debugging)
- Copilot/Hermes = orchestration, QA, consistency

**Ingestion rule (thread L8005–8233):** never feed models the whole project at once — feed each model exactly what it needs per step (streams: static assets / content blocks / pipeline instructions / deployment artifacts).

## V2 Folder Structure (from thread; Astro variant)

```
totalrecalls-site-v2/
├── astro.config.mjs        (site: https://totalrecalls.app)
├── package.json            (astro ^4.0.0 or current; dev/build/preview scripts)
├── public/                 (favicon.svg, logo.svg, images/)
├── src/
│   ├── components/         (Nav.astro, Footer.astro, PageLayout.astro)
│   ├── layouts/            (BaseLayout.astro — head meta, CSS links, nav, footer, <slot />)
│   ├── pages/              (per site map: guides/, compare/, previews/, pricing/, buy/, download/, help/, support/, privacy/, terms/, release-notes/, feature-requests/, roadmap/, why-this-matters/)
│   ├── styles/             (variables.css, main.css)
│   └── utils/              (seo.js)
├── sitemap.xml
└── robots.txt
```

⚠ **Thread divergence:** the thread (L6797–6806, L6982–7027) suggests embedding the current JS multi-model app as `src/pages/app/index.astro` + `src/integrations/`. **This is based on a misconception** — the multi-model integration lives in the WINDOWS APP, not the website (the website is marketing/static). Implementation plan §4 explicitly says: **Do not create `/app/`.** Follow the implementation plan.

## Design System (from thread L4265–4417; also implementation plan §5)

### Color palette
- **Primary:** Midnight Blue `#0A1A2F` (headers, hero text, strong anchors); Electric Blue `#2F7BFF` (links, CTAs, highlights)
- **Secondary:** Slate Gray `#4A5568` (body text, secondary labels); Soft Gray `#E2E8F0` (backgrounds, cards, dividers)
- **Accent:** Emerald `#10B981` (success states, "local-only" trust indicators); Amber `#F59E0B` (warnings: SmartScreen, Takeout issues)
- **Error:** Crimson `#DC2626` (critical errors, failed exports)
- **Background:** White `#FFFFFF`, Off-White `#FAFAFA`

### Typography
- **Primary:** Inter — weights 400/500/600/700
- **Secondary (optional):** IBM Plex Mono — code snippets, folder paths, JSON examples, technical notes

### Spacing scale
4 · 8 · 12 · 16 · 24 · 32 · 48 · 64 px
Base 16px · sections 24px · major blocks 32–48px · hero vertical 64px

### Components
- **Buttons:** Primary — Electric Blue bg, white text, radius 6px, padding 12px 20px. Secondary — 1px Soft Gray border, Midnight text, white bg.
- **Cards:** white bg, 1px Soft Gray border, radius 8px, subtle shadow (0 1px 3px rgba(0,0,0,0.08))
- **Navigation:** sticky top, white bg, 1px Soft Gray bottom border, 16px vertical padding
- **Footer:** Midnight Blue bg, white text, 24px vertical padding, minimal links

### Brand personality
Utility (clean, minimal, functional) · Durability (local files, long-term ownership) · Privacy (trust, calm colors, no hype) · Technical clarity (mono font for code, structured guides) · Confidence (bold headers, strong CTAs)

## Curation notes

- The thread's design system is the implementation plan's §5 source — the two match. Use the implementation plan's tokens for build; this file is the rationale record.
- Version note: thread said "Gemini 2.5 Pro"; Andre's actual implementer is **Gemini 3.5 Flash** — the roles/conventions carry over unchanged.
