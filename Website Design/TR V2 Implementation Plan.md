# TotalRecalls Site V2 — Implementation Plan
**Implementer: Gemini 3.5 Flash** · **Orchestrator: Andre (human) + Hermes Agent** · **Date: 2026-08-11**

This document converts the original design discussion into an executable build plan. The approved copy from that discussion has been extracted into the **V2 Content Pack** (`Website Design/V2 Content Pack/`, 35 files), which is the sole authoritative copy source. The original discussion is archived and no longer referenced. This document tells you **exactly how to build, wire, validate, and deploy it**.

> **Input pair:** You should receive (1) this Implementation Plan and (2) the V2 Content Pack. This plan references approved assets by name; their exact copy lives in the Content Pack's numbered files. If a referenced asset is missing from the Content Pack, stop and flag it — do not invent copy.

---

## 0. Mission & Ground Rules

**Mission:** Replace the current single-page marketing site at `site/` in repo `breakwater2026/TotalRecalls` with a complete multi-page Astro site ("V2"), then deploy it to the **existing** Cloud Run service `totalrecalls-web`.

### Ground rules (non-negotiable)

1. **Copy fidelity.** All page copy comes from the approved assets listed in §7 (exact copy lives in the V2 Content Pack). Do not paraphrase pricing, provider lists, or legal/privacy claims. Do not invent new product claims (e.g., do not add retention periods, feature dates, or provider behaviors not present in the approved copy or the current site).
2. **Preserve commerce wiring.** The Lemon Squeezy checkout flow (`site/js/config.js` + `data-tr-buy` attributes + `/thanks.html` redirect target) must keep working. Details in §8.
3. **Preserve deployment invariants.** Cloud Run service `totalrecalls-web`, region `us-central1`, container port **8080**, unauthenticated, **HTTP/2 end-to-end OFF** (see §10 — violating this caused production 502s before).
4. **No operator notes in production pages.** The current live page contains a visible "Operator note: paste your Lemon Squeezy checkout URL…" line. That is dev communication; in V2 it belongs in `site/README.md`, never in rendered HTML.
5. **SEO continuity.** Existing guide URLs carry SEO value. Migrate the 5 existing guide bodies into the new layout; keep their slugs (see §7.2 and §11).
6. **Work on a branch.** Build in branch `site-v2`. Do not touch `main` until the QA checklist (§9) passes. **Always `git pull` before pushing** — Andre sometimes commits hotfixes directly on GitHub's web UI, so the branch can be behind `origin/main` without warning.
7. **Phase gates.** Each phase in §13 has acceptance criteria. Do not advance past a gate with failing criteria; report the failure instead.

### Definition of done

- `npm run build` succeeds in `site/` with zero errors.
- Every page in the §7 inventory exists, has exactly one H1, a unique `<title>`, and a meta description.
- Buy buttons resolve correctly in both states (checkout URL set / not set).
- The site deploys to the existing `totalrecalls-web` Cloud Run service and serves over HTTPS with HTTP 200 on `/`, `/pricing/`, `/guides/`, `/thanks/`.
- Old public URLs either resolve or redirect (see §11).

---

## 1. Canonical product facts (use these exact values)

| Fact | Value |
|---|---|
| Product | TotalRecalls — Windows app exporting AI chats to local Markdown + JSON |
| Tagline | "Own every AI conversation." |
| Providers (exact order) | ChatGPT · Claude · Perplexity · Gemini (Takeout) · Grok |
| Current version | v1.3.0 |
| Platforms | Windows 10/11 only (Mac "later if demand is real"; no mobile) |
| App size | ~50 MB ZIP |
| Normal price | **$49** (one-time) |
| Launch price | **$24** (one-time; displayed with $49 struck out) |
| Payment processor | Lemon Squeezy |
| ZIP download URL | `https://github.com/breakwater2026/TotalRecalls/releases/download/v1.3.0/TotalRecalls-windows-x64-v1.3.0.zip` |
| Domain | `https://totalrecalls.app` (canonical origin for all metadata) |
| Live preview URL | `https://totalrecalls-web-96283906207.us-central1.run.app` |
| GCP project | `cs-poc-gw89wethbilefc1wrhgq7d7` |
| Cloud Run service | `totalrecalls-web` (us-central1) |
| Emails | support@totalrecalls.app · press@totalrecalls.app · privacy@totalrecalls.app · legal@totalrecalls.app |
| Repo | `github.com/breakwater2026/TotalRecalls` |
| Refund policy | 14 days if the app doesn't work for the buyer's setup |

**Privacy claims (repeat verbatim where used):** local-only; we never host your chats or session tokens; no cloud locker; no telemetry; no TotalRecalls account required; sign-in happens locally in an embedded window; exports land in a folder the user chooses.

**Trust & limits facts (from current site — keep, do not embellish):**
- Windows app today (WebView2). Mac later if demand is real.
- Gemini uses the user's Google Takeout folder/JSON (most reliable path).
- Unsigned builds may show Windows SmartScreen ("More info → Run anyway") until code-signed.
- Smart App Control on some Surface devices blocks unsigned apps with no override; signing is on the roadmap.
- Users must follow each AI provider's terms for their own account use.
- No ad clutter: "This site sells a tool, not pageviews."

**Footer legal line (must appear site-wide):** "Not affiliated with OpenAI, Anthropic, Perplexity, Google, or xAI."

---

## 2. Decisions locked in by the design discussion

1. **Full rewrite**, not a patch of V1 (explicit recommendation accepted by Andre).
2. **Pricing display:** $49 struck through + $24 launch price everywhere a price appears. $24 is what's charged at Lemon Squeezy checkout; $49 is display-only anchoring ("price returns to $49 after the launch window").
3. **Framework: Astro** (static output). Accepted over Next.js/Hugo/plain HTML.
4. **Voice:** clean, confident, privacy-first, utility-focused, minimal, technical-but-accessible. No hype, no filler, no marketing clichés.
5. **Sitemap:** the full marketing sitemap from the design discussion (reproduced in Appendix A) — 40 web routes plus non-web marketing documents.
6. **Design system:** the light-theme system specified in the design discussion (Inter, midnight/electric-blue palette) — see §5. **Decision point DP-1:** the current live site is dark-themed. The approved plan is the light system; tokens live in one file (`variables.css`), so if Andre later wants dark back, it is a one-file change. Default: **build the approved light system**.
7. **Fonts:** self-host via npm (`@fontsource/inter`, `@fontsource/ibm-plex-mono`). **Do not** add a Google Fonts CDN `<link>` — a privacy-first product should not leak visitor IPs to a font CDN.
8. **Honest comparison pages:** implement the comparison table and per-provider pages exactly as written in the approved copy. They are approved marketing claims; do not add new factual claims beyond them.

### Decision points (defaults apply unless Andre overrides before Phase 1)

| ID | Decision | Default |
|---|---|---|
| DP-1 | Light theme (approved) vs keep current dark theme | **Light**, per approved design system |
| DP-2 | Astro vs plain static HTML | **Astro** |
| DP-3 | Keep GitHub Pages mirror workflow | **Remove** `.github/workflows/pages.yml`; Cloud Run is the canonical host (CNAME already removed from Pages) |
| DP-4 | `/buy/` page behavior | Keep current dual behavior: if `lemonCheckoutUrl` is set → button links straight to Lemon Squeezy; if empty → button scrolls to the buy section and a "checkout pending" banner shows |
| DP-5 | Font delivery | **Self-hosted** (@fontsource) |

---

## 3. Current state of the repo (verified 2026-08-11)

```
breakwater2026/TotalRecalls  (local clone: C:\Users\break\Projects\TotalRecalls)
├── site/                        ← V1 marketing site (to be replaced)
│   ├── index.html               (landing + buy card, dark theme)
│   ├── privacy.html, support.html, thanks.html
│   ├── guides/                  (index + 5 SEO guides, real content — MIGRATE, don't discard)
│   │   ├── export-chatgpt-conversations.html
│   │   ├── export-claude-chat-history.html
│   │   ├── backup-perplexity-threads.html
│   │   ├── gemini-takeout-archive.html
│   │   └── own-your-ai-chat-data.html
│   ├── assets/site.css          (dark theme — replaced by V2 design system)
│   └── js/config.js             (TR_CONFIG + buy-button wiring — PORT to V2, see §8)
├── Dockerfile                   (repo root; python:3.12-alpine static server, PORT 8080)
├── cloudbuild.yaml              (build → push → deploy totalrecalls-web; keep)
├── deploy/nginx.conf            (reference only; production uses python http.server)
├── .github/workflows/pages.yml  (GitHub Pages deploy of site/ — remove per DP-3)
├── .github/workflows/ci.yml     (app CI — leave untouched)
└── docs/CLOUD_RUN.md            (deployment doc — update at the end)
```

**Key behaviors to preserve:**
- `js/config.js` reads `window.TR_CONFIG` and wires `[data-tr-buy]`, `[data-tr-download]`, `[data-tr-price]` elements, plus a `#checkout-pending` banner that shows when `lemonCheckoutUrl` is empty.
- Lemon Squeezy's post-payment redirect points at **`/thanks.html`** (`thanksPath`). V2 must keep that URL answering (either a real page or a redirect) or purchasers hit a 404 after paying.
- The ZIP is both (a) linked on-site for testing and (b) attached inside Lemon Squeezy as the digital download.

**Environment facts:**
- Node v22.23.2 / npm 10.9.8 available on the build machine. No Docker locally — container builds happen in Google Cloud Build. Validate with `npm run build` + `npm run preview`, never with local Docker.
- The machine is Windows with a bash (MSYS) shell available.

---

## 4. Target architecture

- Astro project lives **inside `site/`** (replacing V1 content). The repo-root `Dockerfile` builds it (multi-stage, §10). This keeps `cloudbuild.yaml` and the Cloud Run continuous-deploy connection unchanged.
- Astro static output (`output: 'static'`, default), directory-format URLs (`/pricing/` → `pricing/index.html`).
- Shared chrome (nav, footer, head/SEO, config script) lives in one layout; pages contain content only.
- Commerce wiring stays vanilla JS in `public/js/config.js` (served as-is, loaded with `is:inline`). Astro components render the `data-tr-*` attributes; no Astro island JS is needed anywhere in V2. There is **no** embedded "app runtime" page — an earlier `app/index.astro` idea from the design discussion was based on a misconception; the multi-model integration lives in the Windows app, not the website. **Do not create `/app/`.**

### Route inventory (40 routes)

Top level (16): `/` · `/how-it-works/` · `/pricing/` · `/faq/` · `/buy/` · `/download/` · `/help/` · `/support/` · `/privacy/` · `/terms/` · `/release-notes/` · `/feature-requests/` · `/roadmap/` · `/why-this-matters/` · `/thanks/` · `/press/`

Guides (10): `/guides/` index + 5 migrated guides keeping legacy slugs (`export-chatgpt-conversations`, `export-claude-chat-history`, `backup-perplexity-threads`, `gemini-takeout-archive`, `own-your-ai-chat-data`) + 4 new pages (`grok`, `library-format`, `smartscreen`, `troubleshooting`)

Compare (9): `/compare/` index + `chatgpt` · `claude` · `perplexity` · `gemini` · `grok` · `why-local` · `why-multi-assistant` · `pricing`

Previews (5): `/previews/obsidian/` · `notion` · `semantic-search` · `rag-containers` · `multi-device-memory`

**Non-web assets** (repo `marketing/` folder as Markdown, NOT routes): launch announcement, early adopter email, one-pager, demo script, microcopy pack, comparison graphic spec, competitive positioning brief. The press kit becomes the `/press/` page; its long-form version also goes to `marketing/press-kit.md`.

### Astro page tree

```
site/
├── astro.config.mjs  package.json  tsconfig.json  .gitignore  README.md
├── public/
│   ├── favicon.svg
│   ├── js/config.js            (ported commerce wiring — §8)
│   └── robots.txt
├── src/
│   ├── layouts/BaseLayout.astro
│   ├── components/  Nav.astro  Footer.astro  PriceTag.astro  CTAButton.astro
│   ├── styles/  variables.css  main.css
│   └── pages/
│       ├── index.astro
│       ├── how-it-works/index.astro   pricing/index.astro   faq/index.astro
│       ├── buy/index.astro            download/index.astro  help/index.astro
│       ├── support/index.astro        privacy/index.astro   terms/index.astro
│       ├── release-notes/index.astro  feature-requests/index.astro
│       ├── roadmap/index.astro        why-this-matters/index.astro
│       ├── thanks/index.astro         press/index.astro
│       ├── guides/  index.astro + 9 pages (legacy slugs preserved for the 5 migrated guides — see §7.2)
│       ├── compare/ index.astro + 8 pages
│       └── previews/ 5 pages
```

Note: the 5 migrated guides keep their legacy slugs for SEO: `guides/export-chatgpt-conversations.astro`, `guides/export-claude-chat-history.astro`, `guides/backup-perplexity-threads.astro`, `guides/gemini-takeout-archive.astro`, `guides/own-your-ai-chat-data.astro`. New guide pages use the short slugs listed above (`grok`, `library-format`, `smartscreen`, `troubleshooting`), and the `/guides/` index links all of them.

---

## 5. Design system (implement exactly)

From the design discussion. All tokens go in `src/styles/variables.css`; component styles in `src/styles/main.css`. **No inline styles** except where V1 content migration genuinely requires them (minimize).

### Color tokens

```css
:root {
  --color-midnight: #0A1A2F;   /* headers, hero text, strong anchors */
  --color-electric: #2F7BFF;   /* links, CTAs, highlights */
  --color-slate:    #4A5568;   /* body text, secondary labels */
  --color-soft:     #E2E8F0;   /* backgrounds, cards, dividers */
  --color-emerald:  #10B981;   /* success states, local-only trust indicators */
  --color-amber:    #F59E0B;   /* warnings (SmartScreen, Takeout issues) */
  --color-crimson:  #DC2626;   /* critical errors */
  --color-bg:       #FAFAFA;   /* page background */
  --color-surface:  #FFFFFF;   /* cards */
}
```

### Typography
- Primary: **Inter** (self-hosted), weights 400/500/600/700.
- Mono: **IBM Plex Mono** for code, folder paths, JSON examples.
- Body 16px/1.6; H1 clamp(2rem, 5vw, 2.85rem); H2 1.35rem; section max-width 900px.

### Spacing scale
`4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 px` mapped to `--space-1` ... `--space-8`. Base 16px, sections 24px, major blocks 32–48px, hero vertical 64px.

### Components
- **Primary button:** electric-blue bg, white text, radius 6px, padding 12px 20px.
- **Secondary button:** 1px `--color-soft` border, midnight text, white bg.
- **Cards:** white, 1px soft border, radius 8px, shadow `0 1px 3px rgba(0,0,0,.08)`.
- **Price tag:** large `--color-electric` "$24" with struck-through `$49` (gray, `text-decoration: line-through`) beside/above it, and the label "one-time launch price".
- **Nav:** sticky top, white bg, 1px soft bottom border, links Home · How it works · Guides · Compare · Pricing · Download, plus right-aligned primary **Buy** button. Mobile: collapsible.
- **Footer:** midnight bg, white text, 24px vertical padding; links Privacy · Terms · Support · Guides · Release notes · Roadmap; plus the §1 legal line and "© TotalRecalls".
- **Warning callout** (amber left border) for SmartScreen / Smart App Control blocks; **trust badge** (emerald) for local-only/privacy statements.

---

## 6. Navigation & footer

Primary nav (all pages): Home · How it works · Guides · Compare · Pricing · Download · **Buy** (primary button).
Footer (all pages): Privacy · Terms · Support · Guides · Release notes · Roadmap · Feature requests · Press · "Not affiliated with OpenAI, Anthropic, Perplexity, Google, or xAI."

Breadcrumbs on guides/compare/previews sub-pages (`Home › Guides › ChatGPT`). Each page sets canonical URL `https://totalrecalls.app/<path>/`.

---

## 7. Content inventory — where every approved asset goes

**Source of truth:** the V2 Content Pack (`Website Design/V2 Content Pack/`). For each route below, the listed asset is the content to render (the numbered pack file is the exact copy). Keep headings as H2s under the page H1; keep lists as lists; keep tables as HTML tables.

### 7.1 Core pages

| Route | Source asset (V2 Content Pack) |
|---|---|
| `/` | **ASSET 1 — Homepage** (hero + sub-hero value + primary CTA + providers + mini how-it-works + footer CTA). Use the $49-strike/$24 price block. |
| `/how-it-works/` | The 4-step "How it works" flow from the landing-page rewrite + the "official bulk exports vs usable archive" note. Expand each step into a short section. |
| `/pricing/` | **ASSET 3 — Pricing Page** (launch price card, "what you get", why one-time, why $24, simple commercial deal, CTA). |
| `/faq/` | **ASSET 4 — FAQ Page** (render as `<details>/<summary>` accordion, no JS). |
| `/download/` | **ASSET 2 — Download Page** (ZIP download via `data-tr-download`, what's inside, SmartScreen notice, how to use, privacy and security, help links, buy CTA). |
| `/buy/` | Buy card: price block, Lemon Squeezy button (`data-tr-buy`), "already purchased → download", `#checkout-pending` banner div, providers + version line. |
| `/help/` | **Help and SmartScreen rewrite asset** — SmartScreen warning steps, Surface Smart App Control note, general installation help (6 steps), troubleshooting list, contact. |
| `/support/` | **Support Page** asset (common topics, contact email + what to include, refunds 14 days, feature requests, known limitations). |
| `/privacy/` | **Privacy Page** asset (stores nothing; local-only; session tokens; crash logs; third parties: Lemon Squeezy + WebView2; contact privacy@). |
| `/terms/` | **Terms of Use** asset (8 numbered sections). |
| `/release-notes/` | **"What's New in v1.3.0"** asset (new features, UI/UX, performance, bug fixes, known issues, roadmap pointer). |
| `/feature-requests/` | **Feature-Request Intake** asset (what to send, how to submit — email + GitHub Issues link, principles). |
| `/roadmap/` | **ASSET 10 — Roadmap** (available today / coming soon / planned upgrades / principles). |
| `/why-this-matters/` | **ASSET 9 — Why This Matters**. |
| `/thanks/` | Post-purchase page: thank-you, "your download link was emailed by Lemon Squeezy; direct ZIP here too (`data-tr-download`)", quick-start pointer to `/how-it-works/` and `/help/`. **This URL must exist** (Lemon redirect target). |
| `/press/` | **ASSET 11 — Press Kit** (tagline, short/long descriptions, key features, screenshots placeholder block, contact press@). |

### 7.2 Guides

Index `/guides/` = **Guides Landing Page** asset, listing all guide pages with one-line descriptions.

| Route | Source |
|---|---|
| `/guides/export-chatgpt-conversations/` | **Migrate body** from V1 `site/guides/export-chatgpt-conversations.html`; restyle to V2 layout; merge in the ChatGPT guide bullets from the Guides Landing asset. |
| `/guides/export-claude-chat-history/` | Migrate V1 `export-claude-chat-history.html`, same treatment. |
| `/guides/backup-perplexity-threads/` | Migrate V1 `backup-perplexity-threads.html`. |
| `/guides/gemini-takeout-archive/` | Migrate V1 `gemini-takeout-archive.html` + merge the **Google Takeout Troubleshooting** asset as a "Troubleshooting" section. |
| `/guides/own-your-ai-chat-data/` | Migrate V1 `own-your-ai-chat-data.html`. |
| `/guides/grok/` | New — write from Grok section of Guides Landing asset + §1 product facts (embedded login, Markdown + JSON, folder structure). |
| `/guides/library-format/` | New — from Library Format bullets in Guides Landing asset: Library/ folder, naming, Markdown structure, JSON, metadata, backups. |
| `/guides/smartscreen/` | **ASSET 17 — SmartScreen Help Page**. |
| `/guides/troubleshooting/` | Consolidate troubleshooting bullets from the Help and SmartScreen asset + release-notes known issues. |

**Migration rule:** read each V1 guide's body content, keep the prose, strip V1 chrome (header/nav/footer), wrap in V2 layout. Do not rewrite their substance — they are live SEO pages.

### 7.3 Compare

| Route | Source |
|---|---|
| `/compare/` | **Product Comparison Page** asset: overview table (render as HTML table with ✔/✖) + per-provider verdict summaries. |
| `/compare/chatgpt/` … `/compare/grok/` | The five per-provider sections of that asset, one page each (official export bullets vs TotalRecalls bullets + verdict). |
| `/compare/why-local/` | From "Why TotalRecalls Wins" + Why-This-Matters themes (durability, portability, independence, backups, privacy). |
| `/compare/why-multi-assistant/` | From the multi-assistant bullets (switching providers, cross-assistant workflows, unified library). |
| `/compare/pricing/` | Free-but-limited official exports vs one-time $24/$49 utility framing. |

### 7.4 Previews

Five pages from the approved assets: **Obsidian/Notion Integration Preview** (split into two pages), **Semantic Search Preview**, plus **RAG Containers** and **Multi-Device Memory** previews. The Content Pack defines Obsidian/Notion and Semantic Search in full; for RAG Containers and Multi-Device Memory the pack notes the original discussion only listed them in roadmaps — so each of those two pages is a short "preview" page built from the roadmap bullet points (local vector store / personal memory engine; syncing archives across devices, optional paid upgrade), clearly labeled "planned — not shipped". Do not invent specifics beyond the approved copy.

### 7.5 Non-web marketing assets → `marketing/` folder (Markdown)

| File | Source asset |
|---|---|
| `marketing/launch-announcement.md` | ASSET 7 (email version A + social version B) |
| `marketing/early-adopter-email.md` | ASSET 8 |
| `marketing/one-pager.md` | Marketing One-Pager |
| `marketing/demo-script.md` | ASSET 13 — Short Demo Script |
| `marketing/microcopy-pack.md` | ASSET 15 — buttons, tooltips, warnings |
| `marketing/comparison-graphic-spec.md` | Comparison Graphic (designer-ready text spec) |
| `marketing/positioning-brief.md` | Competitive Positioning Brief |
| `marketing/press-kit.md` | ASSET 11 long form |
| `marketing/product-comparison.md` | Full comparison page text (canonical copy backup) |
| `marketing/docs-site-structure.md` | Documentation Site Structure (reference for future docs hub) |

---

## 8. Commerce wiring (port from V1 — critical)

Create `site/public/js/config.js` adapted from V1 `site/js/config.js`:

```js
window.TR_CONFIG = {
  priceLabel: "$24",
  priceNote: "one-time launch price",
  normalPriceLabel: "$49",          // NEW: struck-through anchor
  lemonCheckoutUrl: "",             // PASTE Lemon checkout URL here before launch
  thanksPath: "/thanks/",           // NOTE: V2 URL; update Lemon redirect to match (see §11)
  windowsZipUrl: "https://github.com/breakwater2026/TotalRecalls/releases/download/v1.3.0/TotalRecalls-windows-x64-v1.3.0.zip",
  versionLabel: "v1.3.0",
};
```

Keep the V1 wiring IIFE (querySelectorAll for `[data-tr-buy]`, `[data-tr-download]`, `[data-tr-price]`) plus:
- NEW: `[data-tr-normal-price]` → set to `normalPriceLabel`.
- Buy-button states: with checkout URL → real href, remove `.is-pending`; without → href to `#get-totalrecalls` (or `/buy/`), add `.is-pending`, unhide `#checkout-pending` banner.
- In `BaseLayout.astro`, load it with `<script is:inline src="/js/config.js"></script>` at end of `<body>` so it runs on every page.

Astro pages use the attributes (`data-tr-buy`, `data-tr-price`, etc.) — the vanilla script does the rest. **Do not** convert this into an Astro island/framework component.

The `checkout-pending` banner text (shown only when URL unset): "Checkout link not configured yet — the button below scrolls to the purchase section. The ZIP download works for testing." This replaces the V1 operator note; it is user-facing and acceptable during beta.

---

## 9. QA checklist (phase gate before deploy)

**Build**
- [ ] `npm install` and `npm run build` exit 0, no warnings about missing imports.
- [ ] `dist/` contains an `index.html` for every route in §4 (Astro directory format).

**Per page (spot-check all, script what you can)**
- [ ] Exactly one `<h1>`; H2 hierarchy sane.
- [ ] Unique `<title>` and meta description containing page topic; canonical set.
- [ ] Nav + footer render; all internal links resolve (run a link checker against `npm run preview`, e.g. `npx linkinator http://localhost:4321 --skip "lemonsqueezy|github.com"`); zero 404s.
- [ ] No "Lorem ipsum", no "operator note", no V1 dark-theme leftovers, no placeholder TODO text.
- [ ] Price appears as struck $49 + $24 on `/`, `/pricing/`, `/buy/`, `/download/` and in nav Buy button.

**Commerce**
- [ ] With `lemonCheckoutUrl: ""`: buy buttons scroll/point to buy section, banner visible.
- [ ] With a test URL pasted: buttons take the URL, banner hidden. (Revert to "" after testing.)
- [ ] `data-tr-download` links resolve to the v1.3.0 ZIP URL (HTTP 200).
- [ ] `/thanks/` renders.

**Legal/brand**
- [ ] Privacy, Terms, disclaimer line present and match §7 assets.
- [ ] Provider list always in order ChatGPT · Claude · Perplexity · Gemini (Takeout) · Grok.

**Responsive**
- [ ] At 375px viewport: nav collapses, tables scroll horizontally, hero readable.

---

## 10. Deployment (Cloud Run — same service, same pipeline as V1)

The site already runs on Cloud Run as **totalrecalls-web** (project `cs-poc-gw89wethbilefc1wrhgq7d7`, us-central1). Verified current pipeline: **repo-root `Dockerfile`** (python:3.12-alpine running `python -m http.server $PORT` over `site/`, non-root user, port 8080) built by **`cloudbuild.yaml`** (Cloud Build → Artifact Registry → deploy to `totalrecalls-web`). `deploy/nginx.conf` + `deploy/docker-entrypoint.sh` exist in the repo but are **not** the production path — treat as reference. **Do not change the service, project, region, or port.** V2 only changes what the Dockerfile builds.

### Root Dockerfile — replace with a two-stage build

`cloudbuild.yaml` builds with context = repo root, so the root Dockerfile must COPY `site/` in:

```dockerfile
# --- Stage 1: build the Astro site ---
FROM node:20-alpine AS build
WORKDIR /app
COPY site/package.json site/package-lock.json* ./
RUN npm ci || npm install
COPY site/ .
RUN npm run build

# --- Stage 2: serve dist/ exactly like V1 does ---
FROM python:3.12-alpine
ENV PORT=8080 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /srv
COPY --from=build /app/dist /srv/
RUN adduser -D -u 10001 web && chown -R web:web /srv
USER web
EXPOSE 8080
CMD ["sh", "-c", "echo \"TotalRecalls V2 static site on 0.0.0.0:${PORT}\" && exec python -m http.server \"${PORT}\" --bind 0.0.0.0"]
```

This keeps the runtime **identical to production V1** (python http.server, HTTP/1.1, non-root). Astro's directory output (`pricing/index.html`) works with `http.server`: `/pricing/` serves the index, `/pricing` gets a 301 to `/pricing/`. No gzip/caching from http.server — acceptable for launch (same as V1 today).

**Optional upgrade (NOT part of V2 launch):** swap stage 2 for `nginx:stable-alpine` using the existing `deploy/nginx.conf` + `deploy/docker-entrypoint.sh` (PORT-aware) to gain gzip + cache headers. Only if Andre approves; it changes runtime behavior and needs its own smoke test.

### Cloud Run settings (do NOT change)
- HTTP/2 end-to-end: **OFF** (known requirement — H2C causes 502 with the HTTP/1.1 static server).
- Port: **8080**. Auth: allow unauthenticated (public site).
- Service **totalrecalls-web**, region **us-central1**.

### cloudbuild.yaml
Keep as-is. It already builds the root Dockerfile, pushes, and deploys `totalrecalls-web` (there is also a documented console alternative: "Build type = Dockerfile"). Preferred path per prior decision: **Cloud Build** — no Docker needed on the Mini-PC (Docker is not installed there).

### Custom domain
`totalrecalls.app` DNS is via Cloudflare after the Cloud Run custom-domain setup (already planned/started). V2 ships under the same domain — verify `gcloud run domain-mappings list` before launch.

---

## 11. Migration & redirects

1. **Deploy V2 to the same Cloud Run service** (totalrecalls-web). The old site is replaced entirely (agreed decision: full rewrite, not a patch).
2. **Live V1 URLs that need continuity** (verified against the repo): `/` (index), `/privacy.html`, `/support.html`, `/thanks.html`, and the five guides `/guides/export-chatgpt-conversations.html`, `/guides/export-claude-chat-history.html`, `/guides/backup-perplexity-threads.html`, `/guides/gemini-takeout-archive.html`, `/guides/own-your-ai-chat-data.html`. V2 uses directory URLs (`/privacy/`, `/guides/<slug>/`, …), so every legacy `.html` URL needs a redirect.
3. **Redirect mechanism (works with any static server, no server config):** add tiny static redirect pages under `site/public/` — Astro copies them verbatim into `dist/`. One per legacy URL, e.g. `public/privacy.html`:

```html
<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8">
<meta http-equiv="refresh" content="0; url=/privacy/">
<link rel="canonical" href="https://totalrecalls.app/privacy/">
<title>Moved — TotalRecalls</title>
<script>location.replace("/privacy/")</script>
</head><body><p>Moved to <a href="/privacy/">/privacy/</a>.</p></body></html>
```

Required redirect pages: `privacy.html → /privacy/` · `support.html → /help/` (V1's support.html is the Help page) · `thanks.html → /thanks/` · `guides/export-chatgpt-conversations.html`, `guides/export-claude-chat-history.html`, `guides/backup-perplexity-threads.html`, `guides/gemini-takeout-archive.html`, `guides/own-your-ai-chat-data.html` → their `/guides/<slug>/` equivalents. (If the optional nginx runtime is adopted later, replace these with proper 301 `rewrite` rules.)
4. **Lemon Squeezy post-payment redirect:** V1's `thanksPath` is `/thanks.html`. Keep `/thanks.html` answering (via the redirect page above) so buyers are never broken regardless of what Lemon's dashboard currently points at; when convenient, Andre updates Lemon's redirect to `https://totalrecalls.app/thanks/` and the ZIP attachment link stays the v1.3.0 release asset.
5. **README** (`site/README.md`): update with the Astro dev/build commands (`npm install`, `npm run dev`, `npm run build`) and the config.js checkout-URL instructions (the operator note moves here, out of page HTML).

---

## 12. Execution workflow (who does what, and in what order)

Condensed from the design discussion's orchestration material, adapted for reality: **Gemini 3.5 Flash is the sole implementer** (content + Astro code + deployment files). Hermes/Andre orchestrate, review, and deploy. The multi-model Grok/Gemini split from the discussion is *not* required — Gemini can play both roles — but the phase boundaries still apply as commit checkpoints.

**Phase 1 — Scaffold (commit 1).** Create branch `site-v2`. Generate the Astro project per §3–4: config files, layouts, components, styles, empty page shells for every route in §4. Verify `npm run build` passes with shells.

**Phase 2 — Content (commits 2–4).** Fill pages in this order, committing after each group so progress is reviewable:
1. Core commerce pages: `/`, `/buy/`, `/download/`, `/pricing/`, `/faq/`, `/how-it-works/`.
2. Trust + legal + support: `/help/`, `/support/`, `/privacy/`, `/terms/`, `/roadmap/`, `/release-notes/`, `/feature-requests/`, `/why-this-matters/`, `/thanks/`, `/press/`.
3. Guides (migrate 5 from V1 + write 4 new), Compare (9 pages), Previews (5 pages).
4. `marketing/` folder (10 Markdown files).

**Phase 3 — Wiring + deployment files (commit 5).** `public/js/config.js` (§8), BaseLayout script include, root Dockerfile (§10), `sitemap.xml`, `robots.txt`, favicon, `public/` redirect pages (§11).

**Phase 4 — QA (commit 6 if fixes needed).** Run every item in §9. Fix until clean.

**Phase 5 — Review + deploy (Andre/Hermes).**
- Andre reviews the branch (or a local `npm run preview`).
- Merge to `main` (or push branch for Cloud Build review).
- Trigger Cloud Build → deploys to `totalrecalls-web`.
- Smoke-test live: homepage, one guide, `/buy/` button state, download ZIP link, `/thanks/`, mobile viewport.
- Update Lemon Squeezy redirect (§11.3). Announce per `marketing/launch-announcement.md`.

**Ingestion rule (still valid):** work one page or one small page-group at a time against this plan + the V2 Content Pack; do not regenerate content already committed; do not restructure routes without updating §4 and the sitemap.

---

## 13. Open items & decisions needed (flag to Andre; do not block the build)

1. **Press-kit screenshots** — placeholders only; Andre supplies real screenshots later (app home, provider selection, export progress, Library folder).
2. **support@ / privacy@ / legal@ / press@totalrecalls.app** — assets reference these mailboxes; confirm they forward somewhere before launch (currently likely unprovisioned).
3. **Lemon Squeezy checkout URL** — currently empty in V1 config ("Lemon $24" is set up per project notes but the URL was never pasted into config.js). Needed for the real buy flow and the redirect update.
4. **Code-signing status** — several pages say "signing is on the roadmap". If a certificate is bought before V2 ships, those sentences must be updated.
5. **Astro version** — skeleton said `^4.0.0`; Gemini may use current Astro (5.x) — fine, keep static output mode.
6. **Analytics** (Plausible/Umami) and blog — deferred by design; do not add in V2.

---

## 14. Definition of done

- All 40 routes build, render, link-check clean, mobile-readable, with V2 design system applied.
- Commerce wiring works in both states (URL unset → banner + scroll; URL set → checkout).
- Five migrated guides keep their content and URLs.
- Deployed to Cloud Run service `totalrecalls-web` behind totalrecalls.app with HTTP/2-off setting preserved.
- Repo README updated; marketing folder committed.

*End of plan.*

---

## Appendix A — Full sitemap (from the design discussion, adapted)

```
/                                 Home (hero, value props, pricing card, mini how-it-works, CTA)
/how-it-works/                    4-step flow + compliance-vs-archive note
/pricing/                         $49→$24, what you get, why one-time, why $24
/faq/                             Trust + friction removal (from FAQ asset)
/buy/                             Buy card + checkout-pending fallback
/download/                        ZIP contents, SmartScreen, how-to-use, privacy bullets
/help/                            Help & SmartScreen full page (rewritten asset)
/support/                         Contact + refunds + known limitations
/privacy/                         Local-only policy
/terms/                           License + provider-terms responsibility
/release-notes/                   v1.3.0 notes
/feature-requests/                Intake page
/roadmap/                         Near/mid/long-term + principles
/why-this-matters/                Emotional/practical ownership case
/thanks/                          Post-purchase confirmation
/press/                           Press kit page
/guides/                          Guides hub (all 9 guides linked)
/guides/export-chatgpt-conversations/
/guides/export-claude-chat-history/
/guides/backup-perplexity-threads/
/guides/gemini-takeout-archive/
/guides/own-your-ai-chat-data/
/guides/grok/                     NEW
/guides/library-format/           NEW
/guides/smartscreen/              NEW (help page content or link from /help/)
/guides/troubleshooting/          NEW
/compare/                         Overview table
/compare/chatgpt/
/compare/claude/
/compare/perplexity/
/compare/gemini/
/compare/grok/
/compare/why-local/
/compare/why-multi-assistant/
/compare/pricing/
/previews/obsidian/
/previews/notion/
/previews/semantic-search/
/previews/rag-containers/
/previews/multi-device-memory/
```

Plus `marketing/` non-web documents (Appendix B list in §7.3).
