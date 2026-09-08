# HANDOFF — TotalRecalls website + apps (2026-09-07, ~23:40 EDT)

Purpose: context for the NEXT conversation. Repo: `C:/Users/break/Projects/TotalRecalls`,
branch **RedesignV9**, tip **974aa72**, working tree **clean**, pushed to origin.
Tests: **201/201** + `app.py --selftest` OK. Site builds: 52 pages, 0 dead links.

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

1. **Live 8-provider E2E test — BLOCKED on user's session cookies.**
   Harness ready + committed: `tools/provider_e2e_harness.py` (5-step pipeline:
   validate → count → export-all → verify files → subset re-export; 10 runs/provider
   agreed = 80 total). All 8 providers bot-wall scripted login (Cloudflare/CloudFront),
   and Edge 152 app-bound cookie encryption blocks local extraction. User pastes:
   `copy(document.cookie)` from DevTools console for Perplexity/ChatGPT/Claude/Gemini/
   Grok*/Mistral/Qwen; **Bearer token** from DevTools→Network for DeepSeek and Grok.
   Playbook: totalrecalls skill `references/provider-e2e-harness-2026-09-07.md`.
   NEVER fire hundreds of live calls without green light (rate-limit/account-flag risk).
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
4. **User live-test of the new Pro EXE** (all fixes are in it; not yet exercised by user).
5. **Open decisions (flag, don't auto-apply):**
   - M2: repo stays private (links removed) or go public (restore links)?
   - M3: 80 MB landing demo video — re-compress?
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
