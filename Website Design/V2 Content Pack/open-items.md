# OPEN ITEMS — needs Andre's decision (respond tomorrow)

These are the areas where the thread left a gap or a decision that only Andre can make. Gemini should proceed with the stated default unless Andre overrides.

## A. Copy gaps (thread never produced body copy)

1. **How It Works page body** — the thread lists `/how-it-works/` as a top-level page but generated no standalone body. Default: Gemini expands the homepage's 4-step flow (01-homepage.md) + one-pager "How It Works" (17) into a full page. OK as default?
2. **RAG Containers preview page** (31) — no copy in thread, only roadmap/sitemap mentions. Default: Gemini drafts following the Obsidian/Notion + Semantic Search pattern, optional-upgrade framing, no over-promising. OK as default?
3. **Multi-Device Memory preview page** (31) — same as above. OK as default?
4. **New guide bodies (grok, library-format, smartscreen, troubleshooting)** — thread gives structures only. Default: Gemini writes fresh bodies from structures + assets (14, 15, 24). OK?
5. **Migrated guide bodies (the 5 V1 guides)** — thread gives structures + comparison claims only; V1's live guide pages contain the actual bodies. Default: migrate V1 bodies into V2 style (they're already SEO-tested), not invent new. OK?

## B. Product/business decisions

6. **Standalone `/contact/` page?** Thread's site map lists Contact (support + press emails). Implementation plan routes contact into `/support/`. Keep as planned (no separate contact page), or add one?
7. **"Why Official Exports Fall Short" deep-dive route** (20) — thread's micro-site places it under compare; implementation plan's routes use compare/why-local + why-multi-assistant + pricing. Keep deep-dive as a section of the compare overview, or give it a dedicated page?
8. **Terms of Use page** — thread's version is short-form (8 clauses). For a general-public paid product, recommend a lawyer review before launch. Proceed with thread version for now?
9. **Contact mailboxes** — support@, privacy@, press@, legal@totalrecalls.app are referenced throughout. Are any of these provisioned/forwarding today? (V1 only used support@ in HTML.) If not, what forwarding target?
10. **Press-kit screenshots** — thread leaves placeholders (app home, provider selection, export progress, Library folder). Can you supply real screenshots before launch, or should the /press/ page ship with placeholder text?
11. **Code-signing status** — several pages say "signing is on the roadmap". If a certificate is acquired before V2 ships, these sentences must be updated. Still on the roadmap?

## C. Process (for the record)

12. **Ingestion split (thread L8005+):** the pipeline should feed each model only what it needs (content pack → Gemini; structure/deployment → assembler). This pack + implementation plan follow that rule. Confirm the final handoff shape: (a) this pack + implementation plan to Gemini 3.5 Flash, (b) output assembled by the Astro build, (c) Cloud Build deploy — as the implementation plan §12 describes.
13. **"What's new" vs roadmap terminology** — kept identical across 07/09/22. If you adjust any feature name, tell me and I'll propagate.

## D. Things I flagged but did NOT change (need your OK)

14. **Provider order** — normalized to ChatGPT · Claude · Perplexity · Gemini (Takeout) · Grok everywhere (thread used two variants; V1 site used this order; implementation plan §9 requires it). OK?
15. **Footer disclaimer order** — "Not affiliated with OpenAI, Anthropic, Perplexity, Google, or xAI" (thread ASSET 14 order). OK?
