# PERPLEXITY EXPORTER — HANDOFF (UPDATED)
Date: 2026-08-07 ~15:13 | Status: LOGIN CAPTURE FIXED (cdp-login-v3-noblock)

## MISSION RESULT
The blue-button login path now captures the Perplexity session token.

### Proven in loginprobe (same code path as the UI button)
```
login: STA CLR thread started
login: WebView2 request hook registered
login: CDP Network.enable issued (async)
login: navigated embedded browser to Perplexity
login: intercepted Perplexity request with session token
login: captured session token via WebResourceRequested: eyJhbGci...
login: accepted session token for breakwatercap@outlook.com
connected: breakwatercap@outlook.com, 55 threads
```


## HOTFIX 2026-08-07 ~15:25 — `connect is not a function` + .NET crash dialog
**Build tag: `bridge-fix-v4`**

### Cause
pywebview's `get_functions()` recursively walks **all public attributes** of the
`js_api` object. We passed the whole `Bridge` (with `.window`, threads, etc.).
That broke JS bridge injection → UI saw `api` without `connect` →
`TypeError: a.connect is not a function`. Separate issue: running
`_accept_token` (network) on the WinForms UI thread caused .NET
"Not Responding" / unhandled exception dialogs.

### Fix
- `JsApi` facade: only the 10 bridge methods are exposed to JS
- pywebview window stored as `Bridge._window` (private, not walked)
- Token accept always on a background thread
- WinForms `ThreadException` handled (no stock .NET crash dialog)
- UI waits until `typeof api.connect === 'function'` before calling it

### User verify
1. Kill every PerplexityExporter.exe
2. Launch `dist\PerplexityExporter.exe` (footer: bridge-fix-v4)
3. Click **Log in to Perplexity** — must NOT show "connect is not a function"
4. Sign-in window opens; on success main UI shows Connected


## What was wrong (design bugs)
1. **Connect no longer opened embedded login** — it opened the system browser and tried
   disk cookie decryption (dead end under Chromium app-bound encryption).
2. **CookieManager path used `task.Wait()` on the UI thread** — WebView2 async
   completions marshal back to the UI thread, so Wait() deadlocks (seen as
   "CDP getCookies wait timed out" forever). Prior "validated" Wait pattern was wrong.
3. **`extract_session_token_from_cookie_records` only accepted dicts** — WebView2 returns
   COM objects with `.Name`/`.Value`, so even a successful GetCookiesAsync would miss the token.
4. **UI design bug**: login errors went to `#err` inside the *export* screen (hidden during
   login). Blue button failures were silent. `applyState` also full-reset the connect UI every
   2s poll, flashing the button.
5. **Login thread was MTA** — Python `threading.Thread` is MTA; WinForms/WebView2 need STA
   (`RPC_E_CHANGED_MODE` without CLR STA thread).

## Fix (build tag `cdp-login-v3-noblock`)
- Blue button → `_start_embedded_login()` → **CLR `System.Threading.Thread` + STA**
- Capture order:
  1. **WebResourceRequested** Cookie header (HttpOnly included) — *proven working*
  2. **CDP** `CallDevToolsProtocolMethodAsync("Network.getCookies")` — non-blocking
     IsCompleted poll on WinForms Timer (no Wait on UI thread)
  3. **CookieManager.GetCookiesAsync** — same non-blocking collect; COM .Name/.Value OK
- Navigate only after CoreWebView2 init success
- Connect-screen error box `#err-connect`; applyState no longer thrash-resets during sign-in
- Paste-cookie fallback retained

## Build / paths
- Source: `C:\Users\break\PerplexityExporter\app.py`
- UI: `C:\Users\break\PerplexityExporter\app_ui.html`
- EXE: `C:\Users\break\PerplexityExporter\dist\PerplexityExporter.exe`
- Log: `C:\Users\break\AppData\Roaming\PerplexityExporter\app.log`
- Session now saved after probe (may auto-reconnect on next launch)

## How user should verify
1. Kill any running PerplexityExporter.exe
2. Launch `dist\PerplexityExporter.exe` (or Desktop shortcut after refresh)
3. Footer should mention build `cdp-login-v3-noblock`
4. If auto-reconnected: Disconnect, then click **Log in to Perplexity**
5. Sign-in window opens; after login, main UI should show Connected + thread count
6. On failure, red error appears *on the connect card* (not silently)

## Verify recipes
```
taskkill /IM PerplexityExporter.exe /F
python -m unittest discover -s tests -v
dist\PerplexityExporter.exe --selftest
dist\PerplexityExporter.exe --loginprobe   # must log token capture if profile already signed in
```

## DO NOT
- Navigate the pywebview main window to perplexity.ai
- `task.Wait()` any WebView2 async call on the UI thread
- Rely on DPAPI disk cookie decryption (app-bound JWE)
- Hammer the API with live tokens after login

## Still open / product next
- Code-sign the exe (Smart App Control / SmartScreen on SP8)
- If login-webview profile is cold (logged out), user must complete interactive login once
- Optional: clear login-webview on Disconnect for account switch
