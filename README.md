# TotalRecalls

**Domain:** [totalrecalls.app](https://totalrecalls.app)  
**Product:** Own your AI conversations — export them locally from multiple assistants into one archive you control.

**Version:** **1.3.0** (`all-providers-v1`)

## Providers

| Provider | Status | Auth |
|----------|--------|------|
| Perplexity | Live | Embedded login / session cookie |
| ChatGPT | Live | Embedded login / Bearer or cookie |
| Claude | Live | Embedded login / sessionKey |
| Gemini | Live | **Google Takeout path** (folder or JSON) |
| Grok | Live | Embedded login / Bearer or cookie |

## Run from source

```bash
python app.py
```

Loads the React UI from `ui/`. Falls back to legacy `app_ui.html` if `ui/` is missing.

### Rebuild the React UI
```bash
cd apps/web-ui
npm install
npm run build
rm -rf ../../ui && mkdir ../../ui && cp -r dist/* ../../ui/
```

## Windows EXE

```
dist\TotalRecalls.exe
dist\PerplexityExporter.exe   # same build, legacy name
```

Rebuild:
```bash
.venv\Scripts\python.exe -m PyInstaller PerplexityExporter.spec --noconfirm
copy /Y dist\PerplexityExporter.exe dist\TotalRecalls.exe
```

> EXE is currently **unsigned**. Windows SmartScreen may warn; code signing is on the ship checklist (`docs/RELEASE.md`).

## Layout

| Path | Role |
|------|------|
| `app.py` | Thin entry / re-exports |
| `totalrecalls/` | Python package (core, adapters, desktop) |
| `apps/web-ui/` | React + Vite source |
| `ui/` | Built web UI for pywebview |
| `site/` | Marketing site for totalrecalls.app |
| `docs/` | Decisions, adapter specs, **RELEASE.md** |

## Export output (default)

```
TotalRecalls-export/
  Library/<provider>/Home|Spaces/.../<Title -- id>/
    conversation.md
    conversation.json
  README.md
  manifest.json
```

Classic layout: set `TOTALRECALLS_CLASSIC_EXPORT=1`.

## Tests

```bash
python -m unittest discover -s tests -q
python app.py --selftest
```

## Site deploy

### GitHub Pages (automatic — live)
Push to `main` deploys `site/` via `.github/workflows/pages.yml`.  
**Live:** https://breakwater2026.github.io/TotalRecalls/  

Custom domain later: add DNS `CNAME totalrecalls.app → breakwater2026.github.io`, then restore `site/CNAME`.

### Cloudflare Pages (optional alternate)
```bash
npx wrangler login
npx wrangler pages deploy site --project-name=totalrecalls-site
```
