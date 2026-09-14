# STATUS — 2026-09-13 side-by-side website session (2h autonomous audit)

Branch: **RedesignV9** · No commit/push (user directive). Dev server: `cd site && npm run dev` → **http://localhost:4321/**.

## What the user reported (and what each was)

| Report | Root cause | Fix |
|---|---|---|
| First 3 provider icons "no logo, only colors" (landing animation box) | `ConvergenceDiagram.jsx` set glyph `color` == tile `bg` for ChatGPT/Claude/Perplexity → logo drawn in its own tile color = invisible | Glyphs → `#FFFFFF` on brand-color tile (white-on-brand, standard app-icon look). Other 5 untouched. **User-verified on refresh.** |
| In-app "Buy" button → **404** | `bridge.openBuyPage()` opened `https://totalrecalls.app/buy` — the whole production site is behind the frozen `RedesignV7` 404 deploy gate | `openBuyPage()` now opens `https://totalrecalls.lemonsqueezy.com` (always live; payment actually happens there) |
| "Stale ReadMe" in the buyer workflow | Two different READMEs: (a) the **download-ZIP README** was already the new "TotalRecalls" version (user's downloaded copy verified: first line `TotalRecalls 1.0.0 — Free Tier`); (b) the **app-generated export-folder README** (`export_fs.py`) still said `# Your Perplexity export` / manifest `"tool": "Perplexity Exporter"` | `build_root_readme`/`write_export_indexes` now take a `provider` param (default TotalRecalls); `bridge._export_worker` passes `adapter.display_name`; manifest `"tool": "TotalRecalls"`. The ZIP README's "Buy at:" URL also switched to the LS store (was the frozen .app URL) |
| `Get-FileHash TotalRecalls-v1.0.0-free-tier.zip` → path not found | Filename typo (`-v1.0.0` vs `-1.0.0`) + file lives in `Downloads\`, not home | Told user corrected command; verified hash matches published value |

## Full 2h audit (user: "check every button and URL… many more kinks")

- **Link crawl, all 52 built pages** (`tools/_audit_site_links.py`): 0 dead internal links, 0 missing assets, all 52 routes 200, 404 route works. External 403/404s = the frozen .app domain (by design) + bot-walls on third-party sites (deepseek/mistral/lemonsqueezy — real browsers are fine).
- **Orphan pages: 20 real pages unreachable from anywhere** (compare subpages, /help/, /press/, /feature-requests/, /windows-firewall/, /why-this-matters/, /guides/troubleshooting/, /guides/library-format/, /terms/, /thanks/). Fixed:
  - `compare/index.astro` — new "Head-to-head, by provider" card grid linking all 8 provider compare pages + pricing/why-local/why-multi-assistant.
  - `Footer.astro` — 4th **Support** column (Help, Windows Firewall, Feature Requests, Press, Buy); Product + Compare + Why This Matters; Guides + Troubleshooting + Library Format. Grid CSS → `1.2fr repeat(4, 1fr)`.
  - Remaining 3 "orphans" are correct: `/404.html` (auto route), `/thanks/` (LS post-purchase redirect — set in LS dashboard), `/terms/` (duplicate of `/legals/#terms`; both kept, footer points to legals anchor).
- **Copy sweep** (`tools/_sweep_site_copy.py`, 12 patterns): fixed 3 real issues —
  1. `releases.json` v1.0.0 date "August 2026" → **"September 12, 2026"** (release-notes + about pages render this).
  2. `pricing/index.astro` "We don't offer a 14-day money-back guarantee" → "We don't offer refunds — by design" (free-trial convention: never 14-day/money-back).
  3. `download/index.astro` "replacement for money-back refunds" → "answer to refunds".
  4. `legals/index.astro` "Version v1.0 · Last updated August 2026" → "v1.0.0 · September 12, 2026".
  - "No subscription / no refund" phrasing elsewhere = CORRECT free-trial voice, left alone. Price is consistently $24 everywhere.
- FAQ JSON-LD verified (price, no-subscription, 8 providers — all correct).

## Rebuilt + verified (all in working tree, uncommitted)

- **Both EXEs rebuilt** in clean venv (`tr-build-venv`) with ALL 09-12 + 09-13 fixes; PYZ-verified (`tools/_verify_exe_0913d.py`, 10/10 pass each):
  - `dist/TotalRecalls.exe` = FREE `47f39988c650…` (18,882,033 B)
  - `dist/TotalRecalls-Pro.exe` = PRO `a34cd4d26351…` ← **user should relaunch this** (has new Buy URL + provider-aware export README)
  - Checks: edition consts, openBuyPage→LS store, export_fs provider-aware (no "Perplexity Exporter"), no `order='created'` call site, adapter `limit=100`.
- **Free ZIP repackaged** (`tools/_repackage_free_zip.py`): new SHA **`dc2b76b3297870eb8ffde2ca659f13f454dd96855e1083d08c19bfe231881785`**, 17.8 MB, contains new free EXE + README with LS-store Buy URL.
- **Site rebuilt** (52 pages). `tools/_verify_site_final.py` (now reads page SHA from the page, no hardcoded constant): dist ZIP SHA == page SHA ✓, 0 dead links ✓. Dev server serves the new ZIP (probed, SHA match).
- **Tests: 205 passed, 2 deselected, 6 subtests** (hermetic — no real login windows).
- `edition.py` back to `free` (git-clean).

## Decisions made while you were away (flag if wrong)

1. In-app Buy → LS store URL (not `.app/buy`) — the gate makes `.app` 404 until V9 deploys; the store is where payment happens anyway. Site `/buy/` page unchanged (its checkout button already points to LS).
2. Orphan pages wired via Compare index + footer (kept pages; did not delete /terms/ or /thanks/).
3. ZIP README "Buy at:" → LS store URL.
4. Release date on download page = **September 13, 2026** (today, new ZIP); `releases.json` launch entry = September 12 (original launch).
5. The new free ZIP SHA `dc2b76b3…` is what's now on /download/ and served on localhost.

## Still open (needs you / a decision)

- **Deploy gate still frozen** (`production_branch = RedesignV7`) → totalrecalls.app stays 404. V9 goes live only when you say so.
- **/thanks/ redirect** is configured in the Lemon Squeezy dashboard (can't verify from here) — confirm it points to `https://totalrecalls.app/thanks/` (works once V9 deploys).
- Checkout URL `…/checkout/buy/03e11a51-…` couldn't be live-tested (bot wall + no browser tool this session) — worth one manual click in a real browser.
- Old ZIP in your Downloads (SHA `2460eb02…`) is superseded — re-download from /download/ when you want the current one.
- Demo video redo (yours, when the app feels final). LS live-key E2E still pending LS approval.

## Files changed this session (all uncommitted)

App: `totalrecalls/desktop/bridge.py` (Buy URL, provider param), `totalrecalls/core/export_fs.py` (provider-aware README + manifest).
Site: `ConvergenceDiagram.jsx`, `Footer.astro`, `compare/index.astro`, `download/index.astro`, `pricing/index.astro`, `legals/index.astro`, `releases.json`, `public/downloads/README.txt`, `public/downloads/TotalRecalls-1.0.0-free-tier.zip` (+ dist rebuild).
Tools added: `tools/_audit_site_links.py`, `tools/_sweep_site_copy.py`, `tools/_verify_exe_0913d.py` (and earlier `_audit_zip_placeholder.py`, `_repackage_free_zip.py`, `_verify_site_final.py` updated to read SHA from page).
Deleted: stale repo-root `AGENTS.md` (your call).
Backup: `%LOCALAPPDATA%\hermes\tr_free_0913.exe` (free build copy, `47f39988…`).
