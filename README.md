# TotalRecalls

**Domain:** [totalrecalls.app](https://totalrecalls.app)  
**Product:** Own your AI conversations — export them locally from multiple assistants into one archive you control.

This repository currently ships **provider #1: Perplexity** as a working Windows desktop app (formerly *Perplexity Exporter* v1.0.0). Multi-provider expansion (ChatGPT next, then Claude / Grok / Gemini) is underway — see `docs/DECISIONS.md` and `.hermes/plans/`.

## v1 desktop app (Perplexity) — working today

Downloads ALL your Perplexity conversations as Markdown + JSON. Login happens INSIDE the app (embedded browser) — no cookies to copy, no technical knowledge needed.

### Files
- `dist\PerplexityExporter.exe` — the app (double-click to run, ~40 MB, standalone)
- `app.py` — source code (engine + GUI bridge)
- `app_ui.html` — the interface (loaded by the app)
- `app.ico` — app icon
- `build\PerplexityExporter\xref-PerplexityExporter.html` — PyInstaller modulegraph cross-reference (dependency map artifact; preserved)
- `docs/DECISIONS.md` — locked product decisions

### How to run
Double-click `dist\PerplexityExporter.exe`. On first launch Windows SmartScreen may warn (the exe is unsigned) — click "More info" → "Run anyway".

### What it does
1. **Log in to Perplexity** — a window opens inside the app; sign in there. The app grabs your session automatically. (Advanced: paste a session cookie.)
2. **Choose a folder** — defaults to `C:\Users\<you>\Perplexity-export`.
3. **Export** — downloads every conversation with a progress bar. Re-running continues where it left off; tick "Re-export everything" to redo.

### Output
Per conversation: `conversation.md` / `thread.md` (readable) + `thread.json` (structured), plus `README.md` / `manifest.json` index, organized by Spaces/Home.

### Notes / limits
- Uses Perplexity's internal API — personal local export sits in a gray zone of their ToS; commercial redistribution of scraping-as-a-service is not the product model (see prior legal notes).
- Rate-limited: ~3s between requests by design; large libraries take a while.
- Sessions expire (~7 days); the app reconnects automatically while valid.
- App log: `%APPDATA%\PerplexityExporter\app.log`.

### Rebuilding the exe
```
python -m PyInstaller --onefile --windowed --name PerplexityExporter ^
  --icon app.ico --add-data "app_ui.html;." --collect-all curl_cffi ^
  --collect-all webview --collect-all pythonnet --noconfirm app.py
```
(run from this folder; requires the project venv python)

## Roadmap (summary)

1. Freeze v1 Perplexity ← **you are here**
2. Split `app.py` into adapter modules
3. React + Vite UI on the same Python host
4. ChatGPT adapter
5. Code-signed TotalRecalls installer + totalrecalls.app site
6. Claude, Grok, Gemini adapters
