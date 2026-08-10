# TotalRecalls skill — commercial multi-provider AI conversation exporter

## When to use
User asks about TotalRecalls, PerplexityExporter, exporting AI chats, totalrecalls.app,
or work in `C:\Users\break\PerplexityExporter` / `Projects\TotalRecalls`.

## Canonical paths
- Active workdir: `C:\Users\break\PerplexityExporter`
- Clone: `C:\Users\break\Projects\TotalRecalls`
- Repo: https://github.com/breakwater2026/TotalRecalls
- Domain: totalrecalls.app (Cloudflare Pages from `site/`)
- EXE: `dist\TotalRecalls.exe` (+ legacy `PerplexityExporter.exe`)
- Release: tag `v1.3.0` with zip asset

## Commands
```bash
cd /c/Users/break/PerplexityExporter
python -m unittest discover -s tests -q
python app.py --selftest
python app.py

# UI rebuild
cd apps/web-ui && npm run build && rm -rf ../../ui && mkdir ../../ui && cp -r dist/* ../../ui/

# EXE rebuild
.venv/Scripts/python.exe -m PyInstaller PerplexityExporter.spec --noconfirm
cp -f dist/PerplexityExporter.exe dist/TotalRecalls.exe

# Site deploy (requires wrangler login)
npx wrangler pages deploy site --project-name=totalrecalls-site
```

## Architecture
- `totalrecalls/adapters/*` — ProviderAdapter per provider
- `totalrecalls/core/schema.py` + `unified_export.py` — Library/<provider>/ layout
- `totalrecalls/desktop/bridge.py` + React `apps/web-ui` → `ui/`
- Gemini = Takeout path (chooseTakeoutPath / paste path); not live cookie list
- Never host session tokens off-device
- Preserve `build/`, `dist/`, xref HTML artifact

## Product constraints
- Price target one-time ~$19–29
- Shell: Python + pywebview/WebView2 first
- User intent overrides agent file heuristics (entire PerplexityExporter tree is source)

## Open ship items
- Cloudflare Pages deploy (needs `wrangler login`)
- Code signing
- Payments checkout
