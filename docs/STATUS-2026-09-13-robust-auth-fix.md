# STATUS — 2026-09-13 robust-auth fix (branch `fix/robust-auth-20260913`)

## ⚠ LIVE TEST RESULT 2026-09-13 20:03–20:07 → FOUND + FIXED

User live-tested the first fix build (stage Pro, sha 8be9de73…). Result: login
window opened, pointed at a different (auth) page, closed after ~3s,
"unable to log in". app.log (20:05:21/34, 20:07:27):
`localStorage[userToken] captured (30 chars)` → `validate → api-40003`.

**Root cause:** the DeepSeek web client writes a short opaque **nonce
(30 chars)** under the SAME localStorage key `userToken` on the auth-page
origin; the real long bearer (~400+ chars, validated live in the seg3
session) is only present on the app's home page after a real login. The first
fix captured the nonce on the first poll tick and closed the window before
the user could sign in (validate() correctly rejected it — fail-closed worked;
the capture gate was the missing piece).

**Fix (v2):** the localStorage capture now runs the candidate through the
provider's own `validate()` (`_local_storage_probe_ok`, background thread)
BEFORE closing the window — a nonce fails validation and the window stays
open; only a candidate that returns a live account connects. Superseded
candidates are dropped (probe-slot ownership + candidate equality). Paste
button remains the fallback. New log lines: `candidate captured (N chars) —
validating via provider` / `candidate validated by provider — connecting` /
`candidate failed provider validation — keeping window open`.

Rebuilt + re-verified BOTH EXEs (16/16 checks, now incl.
`_local_storage_probe_ok` in bridge):
- free `dist/TotalRecalls.exe` sha `4fe55ee93faf31bba91a4f527577d780e8d145b8e936c76f34dee16f6e5e29c3`
- pro `dist/stage/TotalRecalls-Pro.exe` sha `f8aef6a2051b48e4428051d848eb58b0a54c4a742cfd59717eb1b7835f7dc086`
  (also copied over `dist/TotalRecalls-Pro.exe` — was unlocked at build time)
Suite: 221 passed, 6 subtests (incl. 3 new probe-gate tests).

**User's next step:** fully CLOSE the app (it was running the OLD stage build
8be9de73…, PIDs on `dist/stage/TotalRecalls-Pro.exe`), relaunch
`dist/stage/TotalRecalls-Pro.exe` (now f8aef6a2… — the validated-gate build),
retry DeepSeek in-app login. Expected: window stays open on the auth page
until the user signs in, then connects with the real token (~45 conversations).

---

Implemented per user directive: "take a longer term perspective on issues and
seek as much as robustness as possible in the fixes." The DeepSeek in-app-login
bug is fixed as a **generic per-provider auth-robustness change**, not a
DeepSeek-only patch.

## What changed (all on branch `fix/robust-auth-20260913`, NOT yet committed)

1. **`totalrecalls/core/errors.py`** — added `AuthRejected` (typed exception) +
   `is_auth_rejected(e)` classifier: the single source of truth for
   "definitive credential rejection." Recognizes the legacy `"auth-failed"`
   string (all 7 providers that raise it), `AuthRejected` type, and
   DeepSeek's envelope/business rejections: `api-40002` (Missing Token),
   `api-40003` (Invalid Token), `http-401`, `http-403`. Network/5xx are NOT
   rejections (offline must not trigger re-auth).

2. **`totalrecalls/adapters/deepseek/adapter.py`** — `validate()` now FAILS
   CLOSED on a definitive rejection (raises) instead of the old broad
   `except DeepSeekApiError` → "optimistic accept" that let a dead token read
   as "Connected, 0 conversations". `list_conversations()` gate now uses
   `is_auth_rejected(e)` (uniform) instead of `"...auth-failed..." in str(e)`.

3. **`totalrecalls/desktop/bridge.py`** —
   - count-worker gate → `is_auth_rejected(e)` (was `"auth-failed" in str(e)`).
   - NEW `_handle_auth_rejection(e, phase=...)`: pushes the existing
     `login_expired` event (UI already renders "log in again") + a clear
     message. Wired into BOTH `_export_worker` except clauses, so a session
     that dies between connect and export prompts re-auth instead of a generic
     error.
   - **DeepSeek localStorage CDP capture** (the actual root-cause fix):
     `_start_generic_cookie_login`/`_generic_cookie_login_flow` gained a
     `local_storage_key` param; `connect()` passes `local_storage_key=
     "userToken"` for DeepSeek. An `on_tick` CDP poll does
     `Runtime.evaluate` of `localStorage.getItem('userToken')` (async
     start/collect pattern — never `Wait()`, which deadlocks the STA thread),
     then `_extract_local_storage_bearer()` (module fn) unwraps the
     `{"value": "<bearer>", "__version": "0"}` envelope. For localStorage-
     primary providers the CDP read is the SOLE capture path (`on_req` header
     capture is skipped) so the dead `ds_session_id` cookie can't race it.
     Paste button remains the fallback.

4. **`totalrecalls/desktop/bridge.py` (ChatGPT)** — closed the documented
   **chunked-cookie gap** (same class of bug): both the request hook and the
   CookieManager tick now match `__Secure-next-auth.session-token` **or any
   `...session-token.N` chunk** (was exact-name only, so chunked sessions —
   which is how OpenAI ships them — never fired; Bearer path had been masking
   it). The cookie exchange reassembles chunks (verified in `chatgpt/auth.py`).

5. **Tests** (`tests/test_auth_failure_propagation.py`, +13): `is_auth_rejected`
   classifier (each provider's rejection shape + network/5xx negative cases),
   DeepSeek `validate()` fail-closed (40002/40003/401/403 raise; network
   blip soft-accepts; live account accepts), DeepSeek `list_conversations`
   dead-session gate, bridge count-worker firing `login_expired` on a
   DeepSeek-shaped rejection, and the `_extract_local_storage_bearer` parser
   (envelope, bare token, missing key, malformed).

## Verification

- Full suite: **218 passed, 6 subtests** (baseline 205 + 13 new). Hermetic:
  STA CLR count in app.log unchanged (268) — no real login window spawned.
- Rebuilt both EXEs in the clean venv (`%LOCALAPPDATA%\tr-build-venv`,
  PyInstaller 6.22.2, ~80s each):
  - free `dist/TotalRecalls.exe` sha `affef72c8ee63b2e48c8b0b146357a021642a6fa0279b88644837787fff4a053`
  - pro `dist/stage/TotalRecalls-Pro.exe` sha `8be9de73d7622aa9bc51fa9daef6dff57fa98a24fdced4b860fe9ecfa9dbac50`
- **PYZ-verified both EXEs (15/15 checks each)** via
  `C:\Users\break\demo-shoot\verify_auth_fix_exe.py [EXE] [edition]`
  (PyInstaller.archive.readers): `is_auth_rejected`/`AuthRejected` +
  `api-40002/40003` consts in core.errors; call-site names in deepseek.adapter;
  `_extract_local_storage_bearer`/`_handle_auth_rejection`/`userToken`/
  chunked-cookie marker in bridge; correct edition const; app_ui.html bundled.

## Build scope note (important)

The working tree carried the **2026-09-12 session's uncommitted work**
(ChatGPT 500-storm retry sink, `order=created` removal, orphan-webview sweep,
Pro entitlement guard, app_ui.html status-handler + provider-sync hunks) —
all of which is already in the user's running EXE and has been exercised.
The build bundles the whole working tree, so the rebuilt EXEs =
(current tested state) + (this auth fix). `app_ui.html` was NOT modified by
this fix (reuses the existing `login_expired` UI path).

## Handoff / remaining (needs user)

1. **Swap the running Pro EXE**: close the app (PIDs holding
   `dist/TotalRecalls-Pro.exe`, pre-fix `a34cd4d2…`), then
   `copy /Y dist\stage\TotalRecalls-Pro.exe dist\TotalRecalls-Pro.exe`.
   (It is the user's live instance — deliberately not touched.)
2. **Live test the DeepSeek fix**: in-app DeepSeek login (sign in in the
   embedded window — it should now capture the real localStorage token
   automatically, no manual paste), Connect → expect N conversations (45 in
   the live account), then export. Also confirm a dead-token session now
   shows the re-auth prompt (not "Connected, 0").
3. **Commit** — the branch is uncommitted. Suggested scope: this fix's files
   (`core/errors.py`, `adapters/deepseek/adapter.py`, `desktop/bridge.py`,
   `tests/test_auth_failure_propagation.py`) can be committed independently;
   the 09-12 tree work is the user's call to review/commit. `dist/`+`build/`
   stay modified in the working tree per project convention.
4. Free ZIP repackage + `/download` SHA update is a SEPARATE delivery step
   (only if the free EXE is what ships; the Pro swap above is for the user's
   own machine).
5. X230 24/7 resilience cron (15-min provider auth health check) — still
   unbuilt, separate workstream (personal layer, not product).

## Files

- Verifier: `C:\Users\break\demo-shoot\verify_auth_fix_exe.py`
- Test venv (throwaway): `C:\Users\break\demo-shoot\_trtest`
- Free backup: `dist/stage/TotalRecalls-free-verified.exe` (= `dist/TotalRecalls.exe`)
