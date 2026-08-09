# Perplexity Exporter v1.0.0

Desktop app that downloads ALL your Perplexity conversations to your computer
as Markdown + JSON. Login happens INSIDE the app (embedded browser) — no
cookies to copy, no technical knowledge needed.

## Files
- `dist\PerplexityExporter.exe`  — the app (double-click to run, ~40 MB, standalone)
- `app.py`                        — source code (engine + GUI logic)
- `app_ui.html`                   — the interface (loaded by the app)
- `app.ico`                       — app icon
- `_build.log`                    — last PyInstaller build log

## How to run
Double-click `dist\PerplexityExporter.exe`. On first launch Windows SmartScreen
may warn (the exe is unsigned) — click "More info" -> "Run anyway".

## What it does
1. **Log in to Perplexity** — a window opens inside the app; sign in there.
   The app grabs your session automatically. (Advanced: paste a session cookie.)
2. **Choose a folder** — defaults to `C:\Users\<you>\Perplexity-export`.
3. **Export** — downloads every conversation with a progress bar.
   Re-running continues where it left off; tick "Re-export everything" to redo.

## Output
Per conversation: `thread.md` (readable) + `thread.json` (structured),
plus `manifest.json` (index) and `profile/user.json` (account).

## Notes / limits
- The export uses Perplexity's internal API — a tool like this sits in a gray
  zone of their ToS (personal use is fine; commercial redistribution is not).
- Rate-limited: ~3s between requests by design; large libraries take a while.
- Sessions expire (~7 days); the app reconnects automatically while valid.
- App log: `%APPDATA%\PerplexityExporter\app.log`.

## Rebuilding the exe
`python -m PyInstaller --onefile --windowed --name PerplexityExporter
 --icon app.ico --add-data "app_ui.html;." --collect-all curl_cffi
 --collect-all webview --collect-all pythonnet --noconfirm app.py`
(run from this folder; requires the hermes venv python)
