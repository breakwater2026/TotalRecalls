# 32 — Full Marketing Site Map (structural summary)

**Source:** Thread "Full Marketing Site Map" (L3598–3844). Curated reference — this is the thread's complete architecture conclusion. The implementation plan's §4 route inventory (40 routes) is the operational version; use this as the narrative map.

## Group 1 — Top-Level Pages (primary navigation)
Home · How It Works · Guides · Pricing · Download · Help / Support · Buy

## Group 2 — Secondary Pages (footer navigation)
Privacy · Terms of Use · Release Notes · Feature Requests · Roadmap · Contact

## Group 3 — Comparison Pages (SEO + conversion)
Compare (overview) · Compare/ChatGPT · Compare/Claude · Compare/Perplexity · Compare/Gemini · Compare/Grok · Compare/Why Local · Compare/Why Multi-Assistant · Compare/Pricing

## Group 4 — Guides (SEO + onboarding)
ChatGPT Export Guide · Claude Export Guide · Perplexity Export Guide · Gemini Takeout Guide · Grok Export Guide · Multi-Assistant Workflows · Library Format Guide · SmartScreen Guide · Troubleshooting Guide

## Group 5 — Product Deep-Dive Pages (marketing + vision)
Why This Matters · Obsidian Integration Preview · Notion Integration Preview · Semantic Search Preview · RAG Container Preview · Multi-Device Memory Preview

## Group 6 — Purchase Funnel Pages
Buy · Checkout Modal Copy · Lemon Squeezy Product Page · Download After Purchase

## Group 7 — Marketing & Communication Pages
Launch Announcement · Early Adopter Email · Press Kit · One-Pager · Release Notes

## Group 8 — Optional Future Pages (scalable add-ons)
Integrations · API Preview · Changelog · Blog · Case Studies

## Structural summary (sitemap format, from thread)

```
/
├── Home
├── How It Works
├── Guides
│   ├── ChatGPT · Claude · Perplexity · Gemini · Grok
│   ├── Multi-Assistant Workflows · Library Format · SmartScreen · Troubleshooting
├── Compare
│   ├── ChatGPT · Claude · Perplexity · Gemini · Grok
│   ├── Why Local · Why Multi-Assistant · Pricing
├── Pricing · Buy · Download · Help · Support
├── Privacy · Terms · Release Notes · Feature Requests · Roadmap
├── Why This Matters
├── Obsidian Preview · Notion Preview · Semantic Search Preview
├── RAG Container Preview · Multi-Device Memory Preview
```

## Curation notes

- Contact page: thread lists "Contact — Support email, press email" — implementation plan routes this into `/support/` (no separate /contact/ route). Flag if Andre wants a standalone contact page.
- "How It Works" is a top-level page in the thread; implementation plan §4 has `/how-it-works/`. Content = the 4-step flow from 01-homepage.md (expanded). ⚠ Thread generated no standalone How-It-Works body copy — Gemini should expand the homepage's 4 steps + the one-pager's How It Works into a full page. See open-items.
