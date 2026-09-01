# TotalRecalls — Product Decisions

Recorded: 2026-08-09  
Source: user answers + agent recommendations locked in planning session.

## Brand & domain

| Item | Decision |
|------|----------|
| Product name | **TotalRecalls** |
| Domain | **totalrecalls.app** — **consumer front door** (download site). Currently served via GitHub Pages at `breakwater2026.github.io/TotalRecalls` until DNS CNAME is set. |
| Public install path | **Website only** — general users must never need GitHub |
| Tagline direction | Multi-assistant chat archives — your AI conversations, on your machine |
| GitHub | `breakwater2026/TotalRecalls` — source + silent file hosting for the Windows zip (not the consumer UI) |

## Architecture decisions

| # | Question | Decision | Rationale |
|---|----------|----------|-----------|
| 1 | Domain ready? | **Yes** — totalrecalls.app @ Cloudflare | User confirmed |
| 2 | Desktop shell | **Python + pywebview/WebView2 host first**; architecture stays shell-swappable for **Tauri later** | Preserves hard-won STA WebView2 login (primary product risk). Tauri rewrite of auth is deferred until adapters + React UI are stable. |
| 3 | `xref-PerplexityExporter.html` (52,250 lines) | **(A) Preserve as artifact / dependency map** — do **not** port into React as app source | File is PyInstaller modulegraph cross-reference HTML, not business logic. Real logic is `app.py` + `app_ui.html` + CLI lineage. Entire v1 folder including xref remains preserved. |
| 4 | Provider #2 | **ChatGPT** | User confirmed |
| 5 | Pricing | **$24 USD one-time Pro** + free tier (3 providers, 5 conversations per download) | Free trial replaces the 14-day refund policy (2026-08-31) |
| 6 | Payments | **Lemon Squeezy** (merchant of record) | Free download + $24 Pro unlocked by a license key (validated in-app) |

## Working trees

| Path | Role |
|------|------|
| `C:\Users\break\PerplexityExporter` | **Active engineering workdir** (prefer until monorepo move completes) |
| `C:\Users\break\Projects\TotalRecalls` | Canonical clone — keep synced to active workdir / origin |
| `artifacts` (future) | Frozen snapshots; v1 freeze also via git tag `v1.0.0-perplexity-stable` |

## Non-negotiables

1. Entire v1 project including `build/`, `dist/`, and xref HTML stays in git history / artifacts.
2. No cloud service that collects user session tokens.
3. API pacing stays conservative (≥3s delay; 429 backoff ≥20s) — session-kill is #1 fragility.
4. User-stated file intent overrides agent heuristics (see `user-intent-primacy` skill).
5. Sell **local ownership / migration UX**, not “we scrape providers for you as a hosted service.”

## Implementation sequence (locked)

0. Freeze v1 (tag) + fix hygiene — **DONE** (`v1.0.0-perplexity-stable`)
1. Marketing/signing foundation (parallel)
2. Decompose `app.py` into modules (still Python) — **DONE** (`totalrecalls/` package; thin `app.py` shim)
3. `ProviderAdapter` + unified schema — **DONE**
4. React + Vite UI — **DONE** (`apps/web-ui` → `ui/`)
5. Optional Tauri shell migration
6. ChatGPT adapter — **DONE**
7. Monetization + code signing + consumer website — **consumer download site live** (Pages); Release zip behind one-click Download; **DNS totalrecalls.app still open**; code signing + payments open
8. Claude / Gemini / Grok adapters — **DONE** (Gemini = Takeout-path primary)
9. CI — **DONE** (`.github/workflows/ci.yml` unit tests + selftest on Windows)

## Open (not blocking Phase 0–2)

- Paste Lemon Squeezy `lemonCheckoutUrl` into `site/public/js/config.js` after product creation (`docs/LEMON_SQUEEZY.md`)
- **DNS:** `totalrecalls.app` → Cloud Run custom domain records in Cloudflare
- Code-signing certificate vendor (required for SmartScreen / Smart App Control)
- Whether free CLI remains open-source as loss leader

## Consumer distribution (locked)

```
User → totalrecalls.app → Buy $24 (Lemon Squeezy) → zip on PC → TotalRecalls.exe
                              ↑
                     digital file also on GitHub Releases (silent host)
```

The **app is not deployed to a cloud server**. Only the **website** is hosted. The EXE always runs locally.

### Website host (Cloud Run path)

| Item | Decision |
|------|----------|
| GCP build type | **Dockerfile** (not Python/Node/Go *buildpacks* — we still use a Dockerfile; the image currently runs `python -m http.server` for reliability on Cloud Run) |
| Image | Static `site/` served on `$PORT` (default 8080) |
| Config | `Dockerfile` at repo root; optional `deploy/nginx.conf` if switching back to nginx |
| Pipeline | `cloudbuild.yaml` or Cloud Run “deploy from GitHub” |
| Guide | `docs/CLOUD_RUN.md` |
| DNS | Cloudflare records **copied from** Cloud Run custom-domain UI after first deploy |
