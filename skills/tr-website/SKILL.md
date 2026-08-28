---
name: tr-website
description: Use when working on the TotalRecalls marketing website (Astro 5 + React + Tailwind in site/, totalrecalls.app on Cloudflare Pages). Covers local dev, the locked landing components, brand tokens, content/page authoring, sitemap, and the deploy pipeline. Distinct from the `totalrecalls` skill which is the Python app.
---

# tr-website — TotalRecalls marketing site

The website at totalrecalls.app. Static Astro 5 + React 19 + Tailwind 3 build
that lives under `site/`, deployed to Cloudflare Pages.

## When to load

- Any work inside `site/src/` (components, pages, layouts, styles)
- Adding/editing landing-page sections, guides, compare pages
- Brand, copy, or pricing changes
- Cloudflare Pages deploy / build issues
- Local dev loop at http://localhost:4321
- Locked-component questions (which are frozen, which can be edited)

Do NOT load for the Python app — that is the `totalrecalls` skill.

## Canonical paths

- Site source: `<repo>/site/` (relative to the project root)
- Astro entry: `site/src/pages/index.astro` (LOCKED — see below)
- Layouts: `site/src/layouts/{BaseLayout,PageLayout}.astro`
- Landing components: `site/src/components/landing/*.jsx` (12 files; mostly LOCKED)
- Styles: `site/src/styles/{main.css,variables.css}`
- Tailwind config: `site/tailwind.config.mjs`
- Astro config: `site/astro.config.mjs` (React + Tailwind integrations)
- Sitemap: `site/scripts/gen-sitemap.mjs` (runs as part of `npm run build`)
- Wrangler: `<repo>/wrangler.toml` (root, NOT in site/)
- Build output: `site/dist/`
- Live domain: https://totalrecalls.app (+ www redirect)
- Cloudflare Pages project: `totalrecalls` (git-connected)
- Production branch in CF dashboard: `RedesignV7`
- Build command: `cd site && npm ci --legacy-peer-deps && npm run build`
- Output dir: `site/dist`

## Commands

```bash
# Local dev (http://localhost:4321)
cd site && npm ci --legacy-peer-deps && npm run dev

# Production build (writes site/dist/ + site/dist/sitemap.xml)
cd site && npm run build

# Preview the built output
cd site && npm run preview

# Validate build output (counts pages, checks footer presence)
ls site/dist/   # should contain index.html + all per-page directories
find site/dist -name "*.html" | wc -l   # 51 expected as of 2026-08-27
```

## Locked components (per `AGENTS.md`)

**The 12 landing components and the homepage are FROZEN.** Editing any of these
without explicit user direction is a violation. If a user request seems to ask
for a layout change, surface the lock and ask before touching.

| Component | File | Locked? |
|---|---|---|
| Nav (header) | `components/landing/Nav.jsx` | LOCKED — 1.5x logo (39px), single row, homepage-prefixed links |
| ThreatFeed | `components/landing/ThreatFeed.jsx` | LOCKED |
| SentinelHero | `components/landing/SentinelHero.jsx` | LOCKED |
| ConvergenceDiagram | `components/landing/ConvergenceDiagram.jsx` | LOCKED |
| ResolutionPath | `components/landing/ResolutionPath.jsx` | LOCKED |
| DriveTree | `components/landing/DriveTree.jsx` | LOCKED |
| RiskMatrix | `components/landing/RiskMatrix.jsx` | LOCKED — "Five AI providers" headline; "many more to come" tile is intentional |
| LibraryPreview | `components/landing/LibraryPreview.jsx` | LOCKED — `max-w-3xl`, "your own tools." no-wrap |
| Guides | `components/landing/Guides.jsx` | LOCKED — "Free reading." headline |
| PricingSection | `components/landing/PricingSection.jsx` | LOCKED |
| SiteFooter | `components/landing/SiteFooter.jsx` | LOCKED |
| LegalSection | `components/landing/LegalSection.jsx` | (LOCKED via landing suite) |
| MicrosoftWarningSection | `components/landing/MicrosoftWarningSection.jsx` | (LOCKED via landing suite) |
| Homepage | `pages/index.astro` | LOCKED |

**Safe to edit** without lock worries: `pages/{compare,guides}/<provider>/index.astro`,
`pages/{how-it-works,faq,pricing,why-this-matters,download,support,terms,privacy,legals}/index.astro`,
and any new page you create under `pages/`.

## Brand tokens (do not deviate)

- "Total" → `#000000` (pure black)
- "Recalls" → `#2F7BFF` (electric blue)
- Subtitle "AI CHAT RETRIEVER" → `#64748B` (slate)
- Logo assets: `site/public/{logo.png,logo-full.svg}`
- Brand variables also defined in `src/styles/variables.css` (midnight, electric, slate, soft, emerald)
- Tailwind `primary` token = `217 100% 59%` ≈ electric blue

## Pricing rules

- Price is **$24 USD**, one-time. Never use `$19`, `$29`, or `$49`.
- Always show as `$24` (NOT `$24.00`).
- On every pricing CTA the label must read: **`$24 USD` (or `$24USD`) — "discounted launch price"`**.
- Lemon Squeezy checkout link is wired (test mode was on as of 2026-08-17).
- Legal pages: governed by **laws of Canada**. NO operator disclosure required (Canadian-resident seller).

## Authoring a new provider page

Pattern for adding e.g. a new DeepSeek guide (use this exact template):

1. **Guide:** `site/src/pages/guides/<provider>/index.astro`
   ```astro
   ---
   import PageLayout from "../../../layouts/PageLayout.astro";
   ---
   <PageLayout title="Export <Provider> Chats" description="..."
     breadcrumbs={[{ label: "Guides", href: "/guides/" }, { label: "<Provider>" }]}>
     <h1>Exporting <Provider> Conversations</h1>
     <p>TotalRecalls reads your local <Provider> session and exports every conversation.</p>
     <h2>Steps</h2>
     <ol>
       <li>Open <a href="https://<provider>.com"><provider>.com</a> and sign in.</li>
       <li>Launch TotalRecalls. Select <strong>"<Provider>"</strong> as the provider.</li>
       <li>Click <strong>Scan Chats</strong>. TotalRecalls reads your session cookie.</li>
       <li>Choose which chats to export.</li>
       <li>Select format: <strong>Markdown + JSON</strong> and pick a destination folder.</li>
       <li>Click <strong>Export</strong>.</li>
     </ol>
     <h2>Notes</h2>
     <ul>
       <li>Per-provider gotcha 1.</li>
       <li>Per-provider gotcha 2.</li>
     </ul>
   </PageLayout>
   ```

2. **Compare:** `site/src/pages/compare/<provider>/index.astro` (same shape; usually shorter)

3. **Content pages** (FAQ, how-it-works, why-this-matters) — update provider enumeration
   if it says "five providers" or lists 5 names. New providers go at the END of the list:
   ChatGPT, Claude, Perplexity, Gemini, Grok, then the new ones.
   Change "five companies" → "eight companies" (or current count).

4. **`compare/index.astro` table** — "All N providers in one app" cell.

5. **DO NOT** add a card to `RiskMatrix.jsx` (LOCKED). The "many more to come" tile
   is the design-intended way to indicate expansion.

6. **DO NOT** add an entry to `Guides.jsx` (LOCKED). Per-provider guide pages are
   still useful for SEO but the homepage card grid is frozen.

7. **FAQ JSON-LD** in `pages/faq/index.astro` is duplicated: an inline `set:html`
   script AND a `jsonLd` const at the top of the file. Both must be updated in
   sync — Google will index whichever is rendered.

8. Run `cd site && npm run build` to confirm 51+ pages render and sitemap updates.

## Footer / layout coverage

- The locked `SiteFooter.jsx` is the global footer for the landing page.
- Per-page layouts inherit from `PageLayout.astro` which wraps content in
  `BaseLayout.astro`. Both use the same global styles.
- Verify all generated HTML contains the footer by spot-checking 2-3 pages
  in `site/dist/<page>/index.html` after `npm run build`. If footer is missing
  on a tall page but present on a short one, the user is reviewing in a
  constrained viewport — verify in a full window before flagging.

## Deploy

```bash
# Automatic via CF Pages git-connected build
git push origin RedesignV7   # triggers CF Pages build (the Production branch)

# Manual one-off (requires wrangler login)
npx wrangler pages deploy site/dist --project-name=totalrecalls
```

`wrangler.toml` is at the **repo root** (not in `site/`) and points at
`site/dist` via `[assets] directory = "site/dist"`. CF Pages dashboard settings:
production branch = `RedesignV7`, root directory = empty, build command =
`cd site && npm ci --legacy-peer-deps && npm run build`, output dir = `site/dist`.

CF Pages auto-deploy = GitHub App (empty repo webhook list NORMAL).

## Pitfalls

- **Tailwind v3 not v4.** Astro config uses `@astrojs/tailwind`, not `@tailwindcss/vite`.
  v4-style `@import "tailwindcss"` will silently produce NO utilities.
- **Trailing slashes everywhere.** `trailingSlash: "always"` in astro.config — never link to `/foo` (will 301-redirect to `/foo/`, which is ugly in tests).
- **`output: "static"` + `build.format: "directory"`** → all pages render as `index.html` inside a per-page folder. TotalRecalls is a static site, no SSR.
- **Visual review in browser, side-by-side with VS Code.** The user reviews
  changes in a browser (not the preview pane). The commit gate is **never push
  to `RedesignV7` until visually approved on localhost**. Pushing auto-deploys
  LIVE.
- **OneDrive between PCs is broken** — don't ship site changes by syncing
  through OneDrive; commit + push to the CF Pages branch.
- **Skill-website drift:** if you change locked-component copy, the changes
  won't be reflected in the `library-format` guide or the `own-your-ai-chat-data`
  guide unless you update those too. The two are independent pages.

## Related skills

- `totalrecalls` — the Python app + EXE build
- `cloudflare-pages-deploy` / `cloudflare-pages-deployment` — CF Pages ops
- `cloudflare-pages-ops` — webhook + deploy diagnostic playbook
- `github-pr-workflow` — branch + PR hygiene for the website branch
