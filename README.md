# TotalRecalls

**Domain:** [totalrecalls.app](https://totalrecalls.app)  
**Product:** Own your AI conversations — export them locally from multiple assistants into one archive you control.

**Version:** 1.1.0 (`react-ui-v1`) — React desktop UI + ProviderAdapter export path.

Provider **#1: Perplexity** is live. ChatGPT is next — see `docs/DECISIONS.md`.

## Run from source

```bash
python app.py
```

Loads the React UI from `ui/` (built assets). Falls back to legacy `app_ui.html` if `ui/` is missing.

### Rebuild the React UI
```bash
cd apps/web-ui
npm install
npm run build
# copy into host path
rm -rf ../../ui && mkdir ../../ui && cp -r dist/* ../../ui/
```

## Packaged EXE (v1 freeze still in repo)

- `dist\PerplexityExporter.exe` — last PyInstaller build (may still be v1 UI until rebuilt)
- Rebuild with `PerplexityExporter.spec` (includes `totalrecalls` + `ui/` when present)

## Layout

| Path | Role |
|------|------|
| `app.py` | Thin entry / re-exports |
| `totalrecalls/` | Python package (core, adapters, desktop) |
| `apps/web-ui/` | React + Vite source |
| `ui/` | Built web UI consumed by pywebview |
| `app_ui.html` | Legacy UI fallback |
| `docs/` | Decisions, adapter + schema specs |

## Export output (default)

```
TotalRecalls-export/
  Library/perplexity/...
  README.md
  manifest.json
```

Classic layout: set `TOTALRECALLS_CLASSIC_EXPORT=1`.

## Tests

```bash
python -m unittest discover -s tests -v
python app.py --selftest
```
