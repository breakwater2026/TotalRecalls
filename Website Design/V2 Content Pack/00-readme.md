# V2 Content Pack — README (read this first)

**Source:** `TR Website Rdesign V2.md` (the 8,282-line Copilot design conversation, read in full).
**Curated by:** Hermes Agent — extraction of conclusions per marketing item.
**Consumer:** Gemini 3.5 Flash, which assembles pages from this pack + `TR V2 Implementation Plan.md` (the build blueprint).

## How this pack is organized

One Markdown file per marketing item/page, numbered so Gemini can walk them in order:

| File | Page / item |
|---|---|
| 00-readme.md | This file |
| 01-homepage.md | Homepage (hero + value + CTA + mini how-it-works) |
| 02-download-page.md | Download page |
| 03-pricing-page.md | Pricing page |
| 04-faq-page.md | FAQ page |
| 05-lemon-checkout.md | Lemon Squeezy product description + checkout modal copy |
| 06-launch-announcement.md | Launch announcement (email + social) |
| 07-early-adopter-email.md | Early adopter email |
| 08-why-this-matters.md | "Why This Matters" page/section |
| 09-roadmap.md | Feature roadmap page |
| 10-press-kit.md | Press kit |
| 11-product-explainer.md | Product explainer |
| 12-demo-script.md | Short demo script |
| 13-footer-microcopy.md | Footer rewrite + microcopy pack |
| 14-takeout-troubleshooting.md | Gemini Takeout troubleshooting page |
| 15-smartscreen-help.md | SmartScreen help page |
| 16-docs-structure.md | Documentation site structure (reference) |
| 17-one-pager.md | Marketing one-pager |
| 18-comparison-page.md | Product comparison page (overview + per-provider) |
| 19-comparison-graphic.md | Comparison graphic spec (designer-ready) |
| 20-why-official-exports-fall-short.md | Deep-dive page |
| 21-positioning-brief.md | Competitive positioning brief |
| 22-release-notes-v130.md | "What's New in v1.3.0" |
| 23-feature-requests.md | Feature-request intake page |
| 24-help-smartscreen-full.md | Full "Help & SmartScreen" page rewrite |
| 25-guides-landing.md | Guides landing page |
| 26-support-page.md | Support page |
| 27-privacy-page.md | Privacy page |
| 28-terms-page.md | Terms of Use page |
| 29-obsidian-notion-preview.md | Obsidian/Notion integration preview page |
| 30-semantic-search-preview.md | Semantic search preview page |
| 31-rag-multidevice-preview.md | RAG + multi-device memory previews (⚠ needs copy decision) |
| 32-marketing-sitemap.md | Full marketing site map + structural summary |
| 33-rewrite-decision.md | Rewrite-vs-patch decision record + V2 folder structure + design system |
| open-items.md | Items needing Andre's decision |

## Global conventions (apply to every page)

1. **Pricing:** always `$49` normal price **struck through**, `$24` launch price beside it. One-time purchase. No subscription. (Confirmed at thread L842–848.)
2. **Provider order — always use exactly:** ChatGPT · Claude · Perplexity · Gemini (Takeout) · Grok. (Gemini is always labeled "(Takeout)" or "(via Google Takeout)".)
3. **Version line:** `Version v1.3.0 · Windows 10/11 · ~50 MB`.
4. **Voice:** clean, confident, privacy-first, utility-focused, minimal, technical-but-accessible. No hype, no fluff, no marketing clichés, no "Lorem ipsum", no filler.
5. **Legal line (footer):** "Not affiliated with OpenAI, Anthropic, Perplexity, Google, or xAI."
6. **Contact emails:** support@totalrecalls.app, privacy@totalrecalls.app, press@totalrecalls.app, legal@totalrecalls.app (⚠ see open-items — mailboxes may not be provisioned).
7. **ZIP contents (referenced in multiple places):** TotalRecalls.exe, README.txt, LICENSE.txt. "No installers, no background services, no telemetry."
8. **SmartScreen boilerplate:** unsigned build → "Windows protected your PC" → More info → Run anyway. Smart App Control on Surface devices may block with no override. Code-signing on the roadmap.
9. **Checkout:** "Secure checkout by Lemon Squeezy."
10. **Provider naming in comparisons:** ChatGPT Export · Claude Export · Perplexity Export · Gemini Takeout · Grok Export.

## What Gemini receives beyond this pack

- `TR V2 Implementation Plan.md` — architecture, routes (40), design tokens, component rules, deployment. This pack is the CONTENT source; the plan is the STRUCTURE source. Where the two conflict, the plan's structure wins but flag the conflict to Andre.
- The Design Thread itself (`TR Website Rdesign V2.md`) if needed for exact wording — every asset in this pack is quoted from it, so the thread is only needed as a cross-reference.
