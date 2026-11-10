# TotalRecalls Pre-Launch Action Plan — 2026-09-06

Scope: final pass on the **website** (`site/`) and the **two desktop apps**
(`dist/TotalRecalls.exe` Free Tier, `dist/TotalRecalls-Pro.exe` Pro).
Prepared and executed autonomously per user authorization (away 6-8h).

## Baseline (verified)
- App unit tests: **166/166 pass**; `app.py --selftest` OK.
- Site: `npm run build` → **52 pages, 51 sitemap URLs**, clean.
- Lemon Squeezy checkout: **LIVE** (302 → 200). Billing portal 403 = bot wall (not an outage).
- All internal site links resolve (11 "dead" hits were `mailto:` false positives).
- Refund sweep: only *intentional* "no refund / in lieu of refunds" framing — no stale 14-day guarantee.
- Provider count "five" is gone (8 everywhere). User-facing copy says "download."
- Comment-file items already applied: Ownership Path, "Simple as ABCD", 9th box "more features to come", Linux/Apple FAQ, Lemon Squeezy /buy page.
- GitHub repo `breakwater2026/TotalRecalls` is **PRIVATE (404)** — dead for visitors.
- `dist/` EXEs are **code-current** (built 09-03 13:37/13:39, after the `app_ui.html` provider-select fix at 13:09). `edition.py` restored to `free`.

## Findings & disposition

### LAUNCH-BLOCKING (implement now)
- **L1 — Free ZIP stale EXE.** `site/public/downloads/TotalRecalls-1.0.0-free-tier.zip`
  wraps a 09-01 build (18,153,291 B); current free build is 09-03 (18,243,034 B).
  → Rebuild free EXE via `tools/build_exe.py --edition free`, repackage ZIP,
    recompute SHA-256, update `/download` page SHA + size.
- **L2 — Pro ZIP stale EXE.** `release/TotalRecalls-1.0.0-pro.zip` wraps a 09-02 build.
  → Rebuild pro EXE via `--edition pro --name TotalRecalls-Pro.exe`, repackage ZIP.
- **L3 — Landing demo video 404.** `ProductShowcase.jsx` (locked landing component)
  references `/demo/totalrecalls-demo.mp4`; the `.mp4` was deleted (dir empty).
  → Restore the committed 80 MB demo asset from git HEAD so the locked component
    renders as designed (zero component change). Flag size to user.
- **L4 — Dead GitHub links (private repo 404)** on `/download` + `/feature-requests`.
  → Remove the GitHub references (keep e-mail). Honors user comment "no GitHub, just e-mail."
- **L5 — Free "Enter license key" flow non-functional.** `activate_license` requires a
  Lemon Squeezy `verifier` that is not wired; the free app returns
  "License validation is not configured yet." Pro ships as a **baked-in Pro EXE**
  (no key needed), so the free app's key box is a broken secondary path.
  → Fix free-ZIP README to point buyers at the Pro EXE download (`/buy/`), not
    "enter a key in the free app." Flag verifier wiring as a store-side follow-up.

### HIGH (user-facing copy)
- **H1 — Free ZIP README stale terminology.** Says "We are in beta" (beta labels were
  removed in `a93d03e`) and "click Export / multi-format export / per-conversation
  and bulk export." → Rewrite to "download" terminology, drop "beta."
- **H2 — /download "How to Use" step 3 lists all 8 providers on the FREE page.**
  Free = 3 providers. → Clarify free (3) vs Pro (8) on the free download page.

### MEDIUM / FLAG (user decision or follow-up — NOT auto-applied)
- **M1 — Lemon Squeezy license verifier not wired.** By design Pro = baked-in EXE, so
  key entry is secondary; but if the store expects key redemption, `activate_license`
  needs an LS `verifier`. Needs an LS API key + contract → **flag, don't guess.**
- **M2 — GitHub repo public-ification.** Alternative to L4 (I removed the links). If the
  user wants the repo public, restore the links.
- **M3 — 80 MB demo video.** Large for a landing page; consider re-compressing. Flag.

## Verification (each fix)
- Rebuild free+pro EXE; confirm `edition.py` restored to `free`; scan binaries for
  all 8 provider ids; confirm new EXE sizes/mtimes.
- Repackage both ZIPs; verify ZIP contents = current EXE + README.
- Recompute free-ZIP SHA-256; confirm `/download` page SHA matches the file exactly.
- Restore demo mp4; rebuild site; confirm no `/demo/*.mp4` 404 (file present in dist).
- Re-grep: no `github.com/breakwater` refs remain; no "in beta" in README; no stale
  provider-count on free page.
- Re-run `npm run build` + dead-link check; confirm 52 pages / 51 sitemap URLs.

## Commit hygiene
- Stage ONLY changed files (never `git add -A`): app_ui.html, tools/build_exe.py,
  .gitignore, .vscode/settings.json (user WIP), dist/ EXEs + build/ intermediates,
  release/ ZIP, site/public/downloads/* (ZIP + README), site/public/demo/*.mp4,
  site/src/pages/download/index.astro, site/src/pages/feature-requests/index.astro,
  site/dist/ (rebuilt). Do NOT commit untracked user notes (docs/*.md) or the
  Lemon Squeezy evaluation reply without a clear signal.
