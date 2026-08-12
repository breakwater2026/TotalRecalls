# HANDOVER MEMO — TotalRecalls Website V2 (for Gemini 3.5 Flash)

**To:** Gemini 3.5 Flash (implementer — you are receiving this as a cold-start: you have no prior knowledge of this website or project)
**From:** Andre (project owner) · Hermes Agent (orchestrator/content curator) · Qwen 3.8 Max (implementation planner)
**Date:** 2026-08-12
**Subject:** Mandate to combine two prior work products and build TotalRecalls Site V2

---

## 0. THE MANDATE (your job, in one paragraph)

Two documents were produced by two different AI models before you. **Qwen 3.8 Max** produced an *Implementation Plan* (the architecture blueprint: routes, design system, deployment, wiring). **Hermes Agent** produced a *Curated Content Pack* (the final, approved copy for every page/section). Your mandate: **read both products, treat them as a single specification, and produce the complete V2 website** — a multi-page Astro site replacing the current single-page marketing site — following the plan's structure and the content pack's copy, wired and deployable exactly as the plan specifies. Where the two documents conflict, **the Implementation Plan's structure wins** and the discrepancy must be flagged in your delivery notes (do not silently pick one).

---

## 1. WHAT TOTALRECALLS IS (context you need before reading anything)

- **Product:** TotalRecalls — a small **Windows app** that exports the user's AI chat conversations from ChatGPT, Claude, Perplexity, Gemini, and Grok into a **private local folder** as readable **Markdown + JSON** files the user keeps forever.
- **Website:** totalrecalls.app — a marketing/documentation site for this product. The current live site (V1) is a single HTML page; V2 is a full multi-page site.
- **Pricing:** normal price **$49 one-time**, launch price **$24 one-time** (always shown with $49 struck through). No subscription.
- **Backend note (do not build this):** the multi-model export logic lives in the **Windows app**, NOT in the website. The website is static marketing content. There is **no `/app/` runtime page** in V2.
- **Live infra (keep unchanged):** Google Cloud Run service `totalrecalls-web`, region `us-central1`, port 8080, unauthenticated, **HTTP/2 end-to-end OFF** (violating this caused production 502s before). Deploy via the existing repo-root `Dockerfile` + `cloudbuild.yaml` (Cloud Build). **The live V1 site deploys from branch `website-v1`** — that branch stays frozen and deployable until V2 replaces it.

---

## 2. THE TWO WORK PRODUCTS (who did what, where it is)

### 2a. Qwen 3.8 Max — Implementation Plan (the STRUCTURE)

| Item | Value |
|---|---|
| File | `TR V2 Implementation Plan.md` (518 lines) |
| Location | `Website Design/` folder (see §3 for full paths) |
| Contents | Canonical product facts table · locked decisions & decision points (DP-1…DP-5) · verified current repo state · target Astro architecture (40 routes) · design-system tokens (colors/typography/spacing/components) · navigation/footer spec · content inventory mapping every approved asset → page · commerce wiring spec (TR_CONFIG + data-tr-* attributes) · QA gate checklist · Cloud Run deployment spec · migration/redirect spec · execution workflow (phases) · definition of done · full sitemap appendix |
| Role for you | **Follow this for: what to build, in what order, with what tokens, and how to deploy.** |

### 2b. Hermes Agent — Curated Content Pack (the CONTENT)

| Item | Value |
|---|---|
| Folder | `V2 Content Pack/` (35 Markdown files, numbered 00–33 + open-items.md) |
| Location | `Website Design/V2 Content Pack/` (see §3 for full paths) |
| Contents | One file per page/section with the **final approved copy**, extracted verbatim from the original design discussion (now archived — this pack is the sole authoritative copy source): homepage, download, pricing, FAQ, Lemon Squeezy + checkout, launch announcement, early-adopter email, why-this-matters, roadmap, press kit, product explainer, demo script, footer + microcopy pack, Takeout troubleshooting, SmartScreen help, docs structure, one-pager, comparison page + graphic + deep-dive, positioning brief, release notes v1.3.0, feature requests, full Help page, guides landing, support, privacy, terms, Obsidian/Notion preview, semantic search preview, RAG/multi-device previews, marketing sitemap, rewrite decision + design system record, open items |
| Role for you | **Follow this for: the exact words on every page. Do not rewrite, paraphrase, or "improve" the copy.** |

**Order of operations:** read `00-readme.md` in the Content Pack first (it explains the pack and the global conventions), then the Implementation Plan, then walk the content files in numeric order.

---

## 3. INPUT FILE LOCATIONS (all paths)

**Local clones (Mini-PC):**
```
C:\Users\break\Projects\TotalRecalls\      ← canonical clone — WORK HERE (on branch Redesign)
├── Website Design\
│   ├── TR V2 Implementation Plan.md          ← Qwen 3.8 Max (structure)
│   ├── Google Cloud Assist Mandate.md        ← Cloud Build/Run mandate (reference)
│   ├── V2 Content Pack\                      ← Hermes (content — sole authoritative copy source)
│   │   ├── 00-readme.md  (READ FIRST)
│   │   ├── 01-homepage.md … 33-rewrite-decision.md
│   │   └── open-items.md  (items needing Andre's decisions)
│   ├── HANDOVER MEMO — Gemini 3.5 Flash.md   ← this document
│   └── (logo assets: *.gif/*.mp4/*.py, credit confirmation png)
├── site\                      ← V1 website — ALREADY IN YOUR WORKING TREE (identical to website-v1)
│                                (YOUR OUTPUT REPLACES THIS; migrate the 5 guide bodies + js/config.js)
├── Dockerfile                 ← keep; may need the two-stage build from plan §10
├── cloudbuild.yaml            ← keep (deploys totalrecalls-web)
└── docs\                      ← deployment docs (update CLOUD_RUN.md at the end)

C:\Users\break\TotalRecalls\    ← V1 workspace (renamed from PerplexityExporter; venv + dev tooling)
                                 — read-only reference for you; do NOT build here
```

**Git (canonical, all inputs committed):**
- Repo: `github.com/breakwater2026/TotalRecalls`
- **Branch `website-v1`** (default) — the **V1 website**, frozen and live. Never modify it. (Renamed from `main`; all V1 CI + the Cloud Build trigger now watch `website-v1`.)
- **Branch `Redesign`** — the **V2 branch**. All planning inputs (this memo, plan, content pack) are committed here. **Work exclusively on `Redesign`** (or a child branch of it); **never checkout or modify `website-v1`.**
- Verified: the full V1 `site/` tree on `Redesign` is **byte-identical** to `website-v1` (branched at `95c577f`) — so V1's architecture is already in your working tree; you do not need to fetch, copy, or switch branches to study it.

---

## 4. HOW TO COMBINE THE TWO PRODUCTS (assembly rules)

0. **Work on ONE branch: `Redesign` — always.** Study V1 from your working tree (`site/`), never by switching to `website-v1`. Do **not** copy V1 into V2 (no `v1-reference/`, no duplicate trees) — V1 already lives in your working tree and in git history; copying creates drift. When V2 passes QA, Andre merges `Redesign` into `website-v1` — the old V1 remains preserved in git history.
1. **Structure from the plan:** create the Astro project inside `site/` exactly per Implementation Plan §4 (page tree, components, layouts, styles, utils). All 40 routes from the plan's route inventory + Appendix A sitemap.
2. **Copy from the pack:** for each page, take the matching numbered content file's copy verbatim (H1s, subheads, bullets, CTAs, FAQ answers, tables). Map: `V2 Content Pack/01-homepage.md` → `/`, `02-download-page.md` → `/download/`, `18-comparison-page.md` → `/compare/` + per-provider pages, `25-guides-landing.md` → `/guides/` + guide pages, etc. The readme's file→page table is your map.
3. **Design tokens from the plan §5** (which matches Content Pack `33-rewrite-decision.md`): Midnight `#0A1A2F`, Electric `#2F7BFF`, Slate `#4A5568`, Soft `#E2E8F0`, Emerald `#10B981`, Amber `#F59E0B`, Crimson `#DC2626`, White/Off-White. Inter (400–700) + IBM Plex Mono. Spacing 4/8/12/16/24/32/48/64. Components per §5.
4. **Commerce wiring from plan §8:** port `site/js/config.js`'s `TR_CONFIG` + `data-tr-buy`/`data-tr-download`/`data-tr-price` wiring into `site/public/js/config.js`; add `data-tr-normal-price` for the struck-through $49. Load with `is:inline` in BaseLayout. **Do not convert to an Astro island/framework component.**
5. **Legacy URLs from plan §11:** keep `/thanks.html` (Lemon Squeezy post-payment redirect target) answering — real page or meta-refresh redirect; add redirect pages for `/privacy.html`, `/support.html`, and the 5 legacy guide slugs.
6. **SEO continuity:** the 5 existing guides in `site/guides/` (export-chatgpt-conversations, export-claude-chat-history, backup-perplexity-threads, gemini-takeout-archive, own-your-ai-chat-data) keep their **legacy slugs**; migrate their existing body content into the new layout (do not invent new guide bodies). The 4 new guides (grok, library-format, smartscreen, troubleshooting) are written from the structures in Content Pack `25-guides-landing.md` + supporting assets (14, 15, 24).
7. **Non-web assets:** create the `marketing/` folder with the Markdown assets per plan §7.5 (launch announcement, early adopter email, one-pager, demo script, microcopy pack, comparison graphic spec, positioning brief, press-kit long form).

---

## 5. NON-NEGOTIABLE RULES (violating any of these = failed delivery)

1. **Copy fidelity:** every word on the pages comes from the Content Pack. Do not paraphrase pricing, provider lists, or legal/privacy claims. Do not invent product claims (retention periods, feature dates, provider behaviors) not present in the pack.
2. **Pricing display:** $49 struck through + $24 launch price everywhere a price appears. One-time. No subscription.
3. **Provider order — always exactly:** ChatGPT · Claude · Perplexity · Gemini (Takeout) · Grok. Gemini is always labeled "(Takeout)".
4. **Version line:** `Version v1.3.0 · Windows 10/11 · ~50 MB` where the pack specifies it.
5. **Voice:** clean, confident, privacy-first, utility-focused, minimal, technical-but-accessible. No hype, no fluff, no marketing clichés, no "Lorem ipsum", no placeholder text, no operator/dev notes in rendered HTML (the V1 "Operator note" line must NOT appear on any page).
6. **Footer legal line (every page):** "Not affiliated with OpenAI, Anthropic, Perplexity, Google, or xAI."
7. **Deployment invariants:** Cloud Run service `totalrecalls-web`, us-central1, port 8080, unauthenticated, HTTP/2 end-to-end OFF.
8. **Commerce must work in both states:** `lemonCheckoutUrl` set → buttons link to Lemon Squeezy; empty → buttons scroll to buy section + "checkout pending" banner shows. ZIP download link = `https://github.com/breakwater2026/TotalRecalls/releases/download/v1.3.0/TotalRecalls-windows-x64-v1.3.0.zip`.
9. **No `/app/` page.** No embedded JS app runtime. The website is static marketing content.
10. **Self-host fonts** via `@fontsource/inter` + `@fontsource/ibm-plex-mono` — no Google Fonts CDN link (privacy-first product).
11. **Branch discipline:** commit only to `Redesign` (or a child branch). Never push to `website-v1`. Never merge `website-v1` into your work. If you believe V2 is ready to go live, say so in your delivery notes — Andre handles the merge.

---

## 6. YOUR DELIVERABLES

1. **Working Astro site in `site/`** — `npm install && npm run build` exits 0; all 40 routes render.
2. **`sitemap.xml` + `robots.txt`** with `https://totalrecalls.app` canonical URLs.
3. **`marketing/` folder** (10 Markdown files per plan §7.5).
4. **Deployment files per plan §10** — root `Dockerfile` (two-stage: node build → python http.server runtime), `cloudbuild.yaml` kept as-is; do not change service/project/region.
5. **Delivery notes** listing: every page built, every content-pack file used, every open item you flagged, and any plan-vs-pack conflict you resolved (with the resolution).

**Verification checklist before delivery (plan §9):** build exits 0 · one H1 per page · unique title + meta description per page · zero 404s on `npm run preview` (link check) · no Lorem ipsum / no operator notes / no V1 dark-theme leftovers · price shows struck $49 + $24 on `/`, `/pricing/`, `/buy/`, `/download/` · mobile-readable at 375px · `/thanks/` renders.

---

## 7. OPEN ITEMS (do NOT block the build — flag in delivery notes)

From `V2 Content Pack/open-items.md` (Andre answers these tomorrow):
- How-It-Works page body (expand the 4-step flow from the homepage pack — safe default)
- RAG Containers + Multi-Device Memory preview copy (draft per the pattern in the other previews — safe default)
- Standalone `/contact/` page? (default: no — contact lives in `/support/`)
- Deep-dive page dedicated route? (default: section of compare overview)
- Mailboxes (support@/privacy@/press@/legal@totalrecalls.app) provisioning
- Press-kit screenshots (placeholders until Andre supplies)
- Code-signing status (currently "on the roadmap" — update if changed)

---

## 8. FINAL NOTE

This website has a real audience and a real checkout. Copy is **approved copy** — your job is assembly and faithful implementation, not creative rewriting. If something in the Content Pack seems wrong or missing, **ask in your delivery notes** rather than improvising. Build clean, build consistent, and ship it.

*— Handover prepared by Hermes Agent, 2026-08-12, on branch `Redesign`. V1 lives on `website-v1` (frozen, live); V2 replaces it after QA — one branch, no copying, no branch-hopping.*
