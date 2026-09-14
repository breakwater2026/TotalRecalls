# HANDOFF — TotalRecalls website + apps (2026-09-07, ~23:40 EDT)

Purpose: context for the NEXT conversation. Repo: `C:/Users/break/Projects/TotalRecalls`,
branch **RedesignV9**, tip **974aa72**, working tree **clean**, pushed to origin.
Tests: **201/201** + `app.py --selftest` OK. Site builds: 52 pages, 0 dead links.

---
## ⚠️ SESSION 2026-09-12 (ChatGPT stall + login freeze + Pro entitlement) — UNCOMMITTED, AWAITING USER REVIEW

User was away ~6 h; work done autonomously per their directive. **Nothing committed or
pushed** — user must review the working tree first. Working tree carries ALL fixes below
plus the in-flight WIP (Bug C fast-count, `_stop_worker` cancellation) that was already
uncommitted when this session started.

### Fixed (all verified live, not asserted)
1. **ChatGPT "connected but doesn't download" stall.** Root cause proved with the user's
   own click in app.log (`11:22:24 startExport() called` → `11:22:42 chatgpt HTTP 500 …
   retry in 2s/4s/8s…`): OpenAI's `/backend-api/conversations` is storming 500s and the
   deep-list rode the unbounded backoff (2→4→8→16→32→45→45 s × 7 passes = up to 15+ min)
   while the UI sat frozen on "Preparing…" (retries only went to app.log). Extraction code
   itself works (headless run of the exact bridge path: validate 0.2 s / count 3.6 s /
   deep list 218 s → 105 convs / fetch 3.6 s, exit 0).
   - `adapters/chatgpt/http.py`: `request()` now takes `on_retry=(attempt, code, backoff)`
     callback + a contextvar sink (`set_retry_sink`/`reset_retry_sink`) so the bridge can
     surface every retry without threading a param through ~10 signatures.
   - `bridge.py _export_worker`: installs the sink inside the worker thread (contextvars
     do NOT cross threads — verified) and pushes `{"type":"status", text:"⏳ ChatGPT's
     servers are busy (HTTP 500) — retry N, next in Xs…"}` to the UI on every retry.
     `on_log` also mirrors to the status line until the first download starts.
   - `app_ui.html`: new `p.type === 'status'` handler → `#status-line`.
   - Live-verified: `tools/_test_retry_sink.py` reproduced the storm (7 retry notifications,
     218 s) and proved `sink → request() → on_retry` fires.
2. **Page-1 label desync (selector ChatGPT / button "Log in to Perplexity").** Bridge now
   restores the last-used provider from `session.json` at startup
   (`bridge.py __init__` reads `load_session()["provider"]`, validates via
   `get_adapter`, else keeps default). Re-applied the user's WIP UI hunk from
   `docs/WIP-RECOVERY-2026-09-08.md` (provider re-sync in the idle-disconnected branch) —
   it had never been re-applied after the Temp purge.
3. **Latent build-breaker:** `bridge.py` called `call_with_stop` (3×) without importing it
   → any rebuild of the WIP would NameError on every connect. Import added.
4. **ChatGPT login window "opens but freezes, never renders" (2026-09-12 12:44).**
   Root cause proved: 6 orphaned `msedgewebview2.exe` (parents dead) from repeatedly
   killing the app held `%APPDATA%\PerplexityExporter\login-webview-chatgpt` locked
   (mv test: Permission denied); `EnsureCoreWebView2Async` then hangs on a blank window.
   - `bridge.py _kill_orphan_webviews()`: startup sweep — wmic enumerates
     msedgewebview2.exe command lines, kills ONLY those referencing our
     `appdata_dir()` profile (other apps' WebView2 untouched). Called in
     `main.py` BEFORE the main window's WebView2 is created (sweeping at login time
     would kill the live main window — main window IS a WebView2).
   - `bridge.py _chatgpt_login_window_flow`: locked-profile fallback (rename probe →
     unique `login-webview-chatgpt-<pid>` folder) mirroring the generic flow.
   - Live-verified: `tools/_test_orphan_sweep.py` — fake orphan (our profile) killed,
     fake foreign (other profile) survived. Orphans were also manually cleared on this
     machine at 12:47; user's retry after that works.
5. **Pro build downgraded to Free at startup.** `check_entitlement()` returns False for a
   baked-in Pro build (no stored LS key) and `bridge._recheck_entitlement` then pushed a
   spurious "revoked Pro" license event → UI tier badge flipped to "Free" every launch
   (in app.log: "entitlement re-check revoked Pro" on the Pro EXE; user's session showed
   "Free tier: downloading the first 1 of 2"). Guard added: baked-in Pro edition skips
   the re-check (its entitlement IS the edition flag).
6. **License-key model confirmed as the user wants** (one app, key lifts limits): free
   build = 3 providers (perplexity/chatgpt/claude) + 5 convs (verified
   `tools/_verify_gating.py`); key slot exists in the UI (`#license-box` revealed via the
   "Upgrade to Pro" link `#btn-upgrade`, `activateLicense` → LS public API,
   `openBuyPage` → /buy). Keys are UUID-shaped (LS standard) — `TR-1234-ABCD`-style
   strings correctly rejected. **Known gaps to review:** no in-app "Deactivate / move to
   another device" (lib fn `deactivate_license()` exists but no UI + no bridge method),
   no "remaining activations" display, LS live-key path still untested (blocked on LS
   approval, unchanged).

### Rebuilt + verified (clean venv, PYZ const/name comparison — see totalrecalls skill)
- `dist/TotalRecalls.exe` (free, 18,881,143 B) SHA-256
  `f93ef897d6b48330ca0c3d6dd97c964af9d1814e450cb428e61e1f7d28f64774`
- `dist/TotalRecalls-Pro.exe` (pro, 18,881,095 B) SHA-256
  `49c18114bc988cdc72904ffcc06ee7e01115bd48d0a3c27c6c8fb8d7c584ea86`
- Both: edition const correct, all 5 fixes present (retry sink, `call_with_stop` import,
  provider restore, entitlement guard, orphan sweep at startup + locked-profile fallback),
  bundled `app_ui.html` byte-identical to repo (incl. status handler + WIP hunk).
- Tests: **203 passed, 2 deselected** (live/battery excluded). New/changed test:
  `tests/test_login_token_extraction.py` (2 tests made hermetic — Bridge() now reads the
  real session.json at construction). Pre-existing flake: pythonnet
  `NullReferenceException` at interpreter teardown (~1 in 2 runs, tests still pass) —
  NOT introduced by this session (reproduces with changes stashed).
- `edition.py` is back to `EDITION = "free"` in the tree (flipped only during builds).

### User-facing test checklist (for when they're back)
1. Double-click `dist/TotalRecalls-Pro.exe` (fresh login) → pick ChatGPT → Connect →
   "Download my conversations". Under the current OpenAI 500 storm it should show
   "⏳ ChatGPT's servers are busy (HTTP 500) — retry N, next in Xs…" in the status line
   (NOT a frozen "Preparing…") and eventually complete (worst case ~3–5 min per pass).
2. Login window must render ChatGPT (orphan sweep + fallback). If it ever blanks again:
   the app now self-heals on next launch.
3. Page 1: dropdown + "Log in to …" button + export dropdown all show the LAST provider
   used (ChatGPT in the user's case) — no more Perplexity desync.
4. Pro build: tier badge stays "Pro" on startup (no "Free" flash); free build: "Upgrade to
   Pro" link reveals the key slot.
5. ZIPs NOT yet repackaged (await review/commit). Free ZIP on site is the old 09-08 build.

### Files changed this session (working tree, uncommitted)
`totalrecalls/desktop/bridge.py` (call_with_stop import; provider restore in __init__;
entitlement guard; _kill_orphan_webviews + sweep call in main; retry sink install +
status/on_log mirroring in _export_worker; ChatGPT locked-profile fallback),
`totalrecalls/desktop/main.py` (sweep at startup + import),
`totalrecalls/adapters/chatgpt/http.py` (on_retry + contextvar sink),
`app_ui.html` (status handler; WIP provider-sync hunk re-applied),
`tests/test_login_token_extraction.py` (hermeticity), plus pre-existing WIP in
`adapters/base.py`, `adapters/chatgpt/{adapter,auth,conversations}.py`,
`core/unified_export.py`. New dev tools (keep or delete at review): `tools/_verify_exe.py`,
`tools/_test_retry_sink.py`, `tools/_test_orphan_sweep.py`, `tools/_verify_gating.py`,
`tools/_test_chatgpt_download_path.py`, `tools/_check_bundled_ui.py`.

### Website FULL AUDIT (2026-09-12) — findings + fixes (working tree, uncommitted)
Build: 52 pages, 0 dead internal links, sitemap 51 URLs, deploy gate INTACT
(wrangler `production_branch = RedesignV7`, `[assets] site/dist` — do NOT "fix").
- SEO: every page has `<title>`, meta description, `og:title`. 0 imgs missing alt,
  0 empty `<a></a>`. robots.txt + favicon.svg present.
- Copy (convention checks, all PASS): no "beta"; no stale "money-back/guarantee/14-day"
  (all "refund" mentions are the intentional Free-Tier-replaces-refunds policy);
  "download" not "export" in user-facing copy (only internal `export-*` URL slugs remain);
  version 1.0.0 everywhere; price $24 one-time, 8 providers / 3 free / 5 convs all
  consistent; `serve.py` GCP bot copy current (no drift).
- **FIX 1 — stale free ZIP.** `public/downloads/TotalRecalls-1.0.0-free-tier.zip` held
  the OLD Sept-8 EXE (SHA `5e0f98a6…`). Repackaged (zipfile level-9) with the NEW
  `dist/TotalRecalls.exe` + updated README. New SHA-256
  `2460eb02ef7c29a2a26768a5e22aef6674061312510c0b581c804067c5bdd685`, 17.8 MB
  (18,699,763 B). Old ZIP backed up to `…-free-tier.zip.bak-2026-09-08` (discard at
  review). `/download` page updated: SHA + date (September 12, 2026) + size (17.8 MB).
  Verified: dist ZIP SHA == page SHA; 0 dead links post-rebuild.
- **FIX 2 — README.txt factual error.** Said login "opens your browser" + "top-right Pro
  badge → Enter key". Reality: embedded sign-in window; key entered via the "Upgrade to
  Pro" link. Corrected.
- **FIX 3 — troubleshooting guide was wrong for the embedded-login model.** Old advice
  ("log in via your default browser", "disable ad blockers", "clear your browser cache")
  doesn't apply. Rewrote the "Download Fails or Returns Empty" section: embedded sign-in
  window; "servers are busy — retrying" (wait, it self-heals); blank window → relaunch
  (app now clears orphaned browser processes on startup); disconnect/reconnect.
- **NOT touched (per user):** the 80 MB landing demo video (user will redo it when the
  app works perfectly); deploy gate.
- Site `dist/` rebuilt after all fixes (52 pages). `site/dist` is gitignored — only
  `src/`, `public/downloads/` ZIP + README are the committable site artifacts.


---

## DONE (all committed + pushed)

### Delivery redesign (0bd8ebe)
- Single free-tier ZIP + **Lemon Squeezy license-key activation** (3 activations/purchase).
  Two-EXE distribution retired.
- `licensing.py` wired to LS **public** License API (no merchant secret in binary):
  POST `/v1/licenses/{activate,validate,deactivate}`. Per-endpoint success fields:
  activate→`activated`+`instance.id`; validate→`valid`; deactivate→`deactivated`.
- Offline grace: stored Pro never revoked on network error; hourly `check_entitlement()`
  revokes only on definitive `valid=False`. `machine_identity()` = pseudonymous `TR-<hex>`.

### Bug A — stale auth showed "Connected, 0 conversations" (146ad6a)
- All 8 adapters re-raise `auth-failed` on the PRIMARY request (were swallowing into `[]`).
- `bridge._count_worker` → clears session, pushes `login_expired`; `app_ui.html` handler
  resets to connect screen with "session expired, log in again".

### Bug B — selection card showed wrong provider (146ad6a)
- `refreshSelectionConversations()` filters rows to `currentProvider`; re-filters on
  provider change + on `connected` push.

### Bug C — ChatGPT 5-min login freeze (974aa72)
- Root cause: connect badge ran the 7-pass deep sweep (~28 requests × 3.0 s anti-429
  pacing) + HTTP-500 storms stacking the 6-retry backoff (live log: 3 m 39 s to count).
- Fix: `ChatGptAdapter.count_conversations()` reads the list endpoint's `total` field in
  ONE bounded request (`max_retries=1`); `auth-failed` still propagates (Bug A intact);
  non-auth errors degrade badge to 0. Bridge uses it when available.
- **Export unchanged**: full deep enumeration still runs at download — nothing dropped.
- **RULE: `DEFAULT_DELAY = 3.0` in `chatgpt/http.py` must NOT be reduced** (user's fix
  for prior 429 storms; verbatim instruction).
- 6 new regression tests (tests/test_chatgpt_adapter.py) + 2 bridge fast-path tests.

### Bug D — multi-org Claude 403 falsely expired live sessions (49033c1, live-verified 2026-09-08)
- Live E2E on the user's claude.ai account (adenis258@gmail.com): the chat
  session cookie gets a 403 `permission_error` ("Invalid authorization for
  organization") on the API "Individual Org" `chat_conversations` endpoint
  while the primary chat org returns 200 + data. Bug A's fix (146ad6a)
  collapsed EVERY 401/403 into `auth-failed`, so `list_conversations_multi`
  raised and the list died for every multi-org user with a perfectly live
  session.
- `claude/http.py`: new `classify_auth_error()` inspects the 403 body —
  `permission_error` / "Invalid authorization for organization" →
  `org-forbidden` (org-scoped, skip this org); anything else stays
  `auth-failed`. cffi path now preserves the 401/403 body as
  `HTTPError.body_text` so the retry loop can classify.
- `conversations.py` unchanged by design: only `auth-failed` is fatal;
  `org-forbidden` falls through the existing per-org skip.
- 4 regression tests (classifier shapes, multi-org skip-while-keep with the
  real account shape, true session-death still propagates). 205/205 pass.
- Verified live: full 5-step pipeline PASS, 37 conversations discovered.

### Builds + packaging (all verified via PYZ const/name comparison vs source)
- `dist/TotalRecalls.exe` (free, 19,612,455 B): edition=free, fast-count baked,
  licensing+Bug A/B baked, cryptography bundled. Clean-venv recipe (see totalrecalls
  skill — project `.venv` is polluted, NEVER build with it).
- `dist/TotalRecalls-Pro.exe` (18,873,462 B): edition=**pro** baked, same fixes.
  (The old Sept-3 Pro EXE backup in Temp was purged 09-08 — no loss: the new
  Pro EXE carries all fixes and strictly supersedes it.)
  **User has NOT yet live-tested this new Pro build** (their old instance was closed
  while idle for the rebuild — fresh login needed).
- Free ZIP: `site/public/downloads/TotalRecalls-1.0.0-free-tier.zip` 18.5 MB,
  SHA-256 `6b18e80976853b4628329a3267b768998e90b53942b52554822681ee6478a3af`.
  `/download` page SHA + size updated; site rebuilt.
- Pro ZIP refreshed: `release/TotalRecalls-1.0.0-pro.zip` (18,691,271 B,
  SHA `2eec55a7482804ed96e1a87773c8446123f02f9d7e1bdfe174d8cbfe5788e805`).

### Pre-launch audit items (docs/ACTION_PLAN-prelaunch-2026-09-06.md) — status verified today
- L1/L2 stale ZIPs → DONE (both repacked with current EXEs).
- L3 demo video 404 → DONE (`site/public/demo/totalrecalls-demo.mp4` 80.6 MB restored
  + `totalrecalls-lemon-squeezy-demo.mp4` 2.4 MB; locked ProductShowcase.jsx renders).
- L4 dead GitHub links (private repo) → DONE (removed from /download + /feature-requests;
  e-mail kept, per user comment "no GitHub, just e-mail").
- L5 free "Enter license key" flow → DONE (verifier wired at `licensing.py:151`;
  README points buyers to https://totalrecalls.app/buy/ → key by email → enter in app).
- H1 README "beta"/"export" terminology → DONE ("download" wording, no "beta").
- H2 free page provider clarity → DONE (page shows Free Tier + "Need all 8 providers?
  Upgrade to Pro — one-time $24"; README lists free = 3 providers).

## LEFT TO DO (in priority order)

1. **Live 8-provider E2E test — IN PROGRESS (2026-09-08, user pasted credentials;
   harness `tools/provider_e2e_harness.py`, 10 runs/provider, max 3 convs/run,
   reports in `%LOCALAPPDATA%\Temp\tr_e2e\reports\<provider>.json`):**
   - Perplexity ✅ 10/10 PASS (43 convs) · Gemini ✅ 10/10 PASS (85 convs)
   - Mistral ✅ 10/10 PASS (Ory Kratos session cookie; the value from DevTools
     is wrapped in literal double quotes — the adapter needs them preserved)
   - Claude ✅ 10/10 PASS (Bug D fix 49033c1 live-verified; 37 convs, 4 conv
     files + subset per run, consistent every run).
   - ChatGPT: the 10-run battery keeps dying SILENTLY mid-run01 (no crash
     event, no sleep event, power plan has sleep disabled on AC — the
     process is killed externally while in a 429 backoff; happens on
     OpenAI's 500/429 storm days). Fix: `tr_e2e/run_battery.py <provider>`
     (one process per run + per-run report files + resume) under
     `tr_e2e/supervise_battery.py <provider>` (watches, relaunches up to 12x,
     logs to reports/<provider>_supervisor.log). NOTE: the harness itself
     was fixed in 247af81 — old version ran the deep sweep TWICE per run
     (discover+export) and its subset assertion was blind (read top-level
     `messages` instead of `conversation.messages`; PASS gated on it now).
     Pre-247af81 PASS verdicts (Perplexity/Gemini/Mistral/Claude) — treat as
     "export data verified by hand, subset assertion blind"; post-fix runs
     (Qwen, any ChatGPT rerun) are genuine.
   - Qwen ✅ 10/10 PASS (genuine — fixed subset assertion; 24 convs, ~16 s/run,
     one 49 s outlier; consistent every run). Credential format found
     empirically: the JWT pasted from the web client must be sent as the
     cookie `token=<JWT>` — raw JWT alone returns `success=false`.
   - DeepSeek ✅ (battery running, run01 genuine PASS — 44 sessions, ~14 s/run).
     CREDENTIAL FORMAT FOUND: NOT a cookie (cookies → `api-40002: Missing
     Token`) and NOT a Network-tab Bearer — it's the `userToken` key in
     **localStorage** (JSON envelope `{"value":"…","__version":"0"}`; use the
     inner `value`). Console grab:
     `copy(JSON.parse(localStorage.getItem('userToken')).value)`
   - Grok ✅ (battery running). Credential = FULL cookie set from the
     logged-in browser — session lives in `sso` (+`sso-rw`) JWT cookies;
     `x-userid` alone (a bare UUID) is rejected; Cloudflare `cf_clearance`
     + `__cf_bm` ride along (grok.com is CF-fronted). `document.cookie`
     from the logged-in page works as-is (21 conversations verified).
     NOTE: `cf_clearance` is short-lived — a stale Grok battery fails
     auth-failed; re-grab `document.cookie` if that happens.
   - Credential files live in `%LOCALAPPDATA%\Temp\tr_e2e_creds\` (session
     cookies/tokens — purge after the E2E completes). Claude `sessionKey`
     pasted via Notepad: my own output masks `sk-ant-sid01-…` tokens
     (routingHint JWTs and bare numbers do NOT — control-tested).
   - NEVER fire hundreds of live calls without green light (rate-limit/
     account-flag risk). Playbook: totalrecalls skill
     `references/provider-e2e-harness-2026-09-07.md`.
2. **Side-by-side website + app GUI session** (user: starts AFTER testing).
   ⚠️ UPDATE 2026-09-08: the WIP backup dir
   `%LOCALAPPDATA%\Temp\tr_wip_backup_20260907\` was **PURGED by Windows** —
   do NOT look for it. Everything salvageable was recovered into
   `docs/WIP-RECOVERY-2026-09-08.md` (commit `e14ee91`): the verbatim
   `app_ui.html` provider-sync hunk (5 lines, inserted before
   `setPill('Not connected', false);` in the idle-disconnected else-branch)
   + the disposition of the other 6 WIP items (all trivial/recreatable/
   superseded). Re-apply the hunk from that doc at session start.
   User quote: "My WIP will resurface at that point."
3. **Lemon Squeezy live-key test** — blocked until LS approves the app (demo video
   outstanding on LS side). End-to-end activation with a REAL key is the only untested
   path in licensing.
4. **User live-test of the rebuilt Pro EXE** (Bug D + all fixes baked;
   verified via PYZ const/name comparison — edition ['pro'], all modules
   match source). Commit c9a72fa (2026-09-08) rebuilt BOTH EXEs in the
   clean venv + repackaged both ZIPs + updated /download SHA (441ea535…,
   18.7 MB, rebuilt site). GOTCHA: `tools/build_exe.py` hardcodes the
   POLLUTED `.venv` — its run produced a 34 MB EXE (discarded); the good
   Pro EXE was built by manual edition.py flip + clean-venv PyInstaller
   + restore (edition.py is back to `EDITION = "free"` in the tree).
5. **Decisions (2026-09-08, user):**
   - M2 RESOLVED: repo stays **PRIVATE** — commercialization is underway.
     Verified: anonymous GET github.com/breakwater2026/TotalRecalls → 404;
     site has zero github.com links (already stripped). No action needed.
   - M3 RESOLVED: the 80 MB landing demo video will be **redone by the user**
     once the app works perfectly — do not re-compress the current one.
     (Pending: user's Pro-EXE live test — Claude multi-org connect + ChatGPT
     under the 500 storm — before the re-recording.)
6. **Deployment gate (do NOT "fix"):** site is intentionally NOT deployed;
   `totalrecalls.app` 404s by design (fail-safe: wrangler `production_branch =
   "RedesignV7"` frozen). Going live later = point production branch at release branch
   + redeploy. `site/dist` is gitignored; `serve.py` GCP variant has drifting bot copy.

## RULES / GOTCHAS for next session
- AGENTS.md locks `site/src/components/landing/*`, `index.astro`, Nav.
- Stage ONLY changed files — never `git add -A` (untracked user notes live in docs/).
- Build EXEs ONLY with clean venv `$LOCALAPPDATA/tr-build-venv` (recipe + EXE-verification
  method in totalrecalls skill; verify PYZ consts AND names vs compiled source; assert
  const sets non-empty before declaring a match).
- `app_ui.html` is CRLF and will carry user WIP hunks again after step 2 — build shipping
  EXEs from a tree without unreviewed WIP, restore WIP after.
- ChatGPT `DEFAULT_DELAY = 3.0` is sacred (see Bug C).
- Version 1.0.0 (source of truth `site/src/data/releases.json`).

## Environment note (brief — GPU work is CLOSED per user)
- Both Vast 5090 instances destroyed 2026-09-07 (0 instances, no billing). The
  `unsloth` provider (localhost:8000 SSH tunnel) is DEAD; do not route chat through it.
- Tunnel watchdog scheduled task `TotalRecalls5090TunnelWatchdog` is DISABLED
  (script kept at `C:\Users\break\vast-tools\llama_tunnel_watchdog.sh` — if a 5090 is
  re-rented later: update host/port in the script, re-enable the task).
- This chat now runs on the alibaba-token-plan cloud model.
