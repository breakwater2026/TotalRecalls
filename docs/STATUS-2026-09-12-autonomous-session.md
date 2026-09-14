# STATUS — autonomous session 2026-09-12 (user away ~6h)

Directive received: finish the app, then full website audit. Implement changes but
**do NOT commit/push** — awaiting your review. **Nothing has been committed or pushed.**

## What you'll test when back

**The customer app is ONE binary: `dist\TotalRecalls.exe`** (the free build, SHA
`f93ef897…`). Double-click it. A pasted license key lifts the limits — there is no
separate "Pro app" for customers.
(`dist\TotalRecalls-Pro.exe` still sits next to it as a tracked artifact from the old
two-EXE model — it is **not** a customer deliverable. See decision #5: keep-internal
or delete.)

Fresh login (old session may be stale), in `TotalRecalls.exe`:

1. **ChatGPT download stall fixed.** Connect → "Download my conversations". Under the
   current OpenAI 500-storm you should now see
   `⏳ ChatGPT's servers are busy (HTTP 500) — retry N, next in Xs…` in the status line
   (NOT a frozen "Preparing…"). It completes on its own (worst case ~3–5 min/pass).
2. **ChatGPT login window renders.** 6 orphaned WebView2 processes were holding the
   profile lock (the freeze). They're cleared; the app now self-heals on every launch
   + falls back to a temp profile folder if a lock survives.
3. **Page 1 no longer desyncs.** Dropdown / "Log in to …" button / export dropdown all
   start on your last-used provider (ChatGPT).
4. **Pro tier badge stays "Pro"** (was flashing "Free" on startup).
5. Free build: "Upgrade to Pro" link → license-key slot (the model you asked for:
   one app, key lifts the 3-provider / 5-conversation limits).

## App — fixes (all live-verified, details in docs/HANDOFF-website-apps-2026-09-07.md)

| # | Bug | Root cause (evidence) | Fix |
|---|-----|----------------------|-----|
| 1 | ChatGPT "connected, doesn't download" | OpenAI 500-storm + unbounded backoff, retries only in log (your click at 11:22:24 in app.log; headless run: 218s deep-list → 105 convs, exit 0) | Retry notifications pushed to UI via contextvar sink (set inside worker thread — contextvars don't cross threads) |
| 2 | Page-1 ChatGPT/Perplexity desync | Bridge never restored last provider; user's WIP UI hunk never re-applied after Temp purge | `session.json` provider restore in `Bridge.__init__` + WIP hunk re-applied from WIP-RECOVERY doc |
| 3 | Latent build-breaker | `bridge.py` called `call_with_stop` 3× without import → NameError on every rebuild | Import added |
| 4 | ChatGPT login window blank/frozen | 6 orphaned `msedgewebview2.exe` locked `login-webview-chatgpt` (mv test: Permission denied) | Startup sweep (kills only processes referencing OUR profile) + locked-profile fallback in ChatGPT flow |
| 5 | Pro build downgraded to Free at startup | `check_entitlement()` False for baked-in Pro (no LS key) → spurious "revoked" push | Baked-in Pro skips the re-check |

- Tests: **203 passed** (2 live-battery deselected). `edition.py` restored to `free`.
- Both EXEs rebuilt in the clean venv and verified by PYZ const/name comparison:
  - `dist/TotalRecalls.exe` (free) `f93ef897…` · `dist/TotalRecalls-Pro.exe` (pro) `49c18114…`
- License model gaps flagged for you: no in-app "deactivate / move to another device"
  (`deactivate_license()` exists in the lib but no UI or bridge method), no
  "remaining activations" display, LS live-key path still untested (blocked on LS).

## Website — full audit (results + 3 fixes)

Build clean: 52 pages, 0 dead internal links, sitemap 51 URLs, deploy gate intact
(`production_branch = RedesignV7` — untouched). SEO complete (title/description/og on
all pages; 0 imgs missing alt). Copy checks all PASS (no "beta", no stale refund/guarantee
wording, "download" not "export", version 1.0.0, $24 one-time / 8 / 3 / 5 consistent,
serve.py bot copy current).

Fixes (working tree):
1. **Free ZIP was stale** (held the Sept-8 EXE). Repackaged with the new EXE + updated
   README → SHA `2460eb02…`, 17.8 MB. `/download` page SHA/size/date updated; verified
   page SHA == ZIP SHA. Old ZIP backed up as `…-free-tier.zip.bak-2026-09-08`.
2. **README.txt factual errors** ("opens your browser", "Pro badge → Enter key") →
   corrected to embedded sign-in window + "Upgrade to Pro" link.
3. **Troubleshooting guide** advised legacy browser-login steps → rewritten for the
   embedded-login model (incl. the new "servers busy — retrying" and blank-window advice).

Not touched per your earlier decisions: the 80 MB demo video (you're redoing it),
deploy gate, repo privacy.

## Decisions waiting on you

1. **Review + commit** the working tree (app fixes + WIP + site fixes). Suggested split:
   one commit per concern (app fixes / site audit) or one combined — your call.
   Stage only the listed files (`git add -A` would sweep untracked user files:
   `Videos/`, `demo_perplexity_script.py`, `docs/AUDIT-2026-09-09.md`).
2. **Keep or delete** the `tools/_*.py` dev scripts (EXE verifier, retry-sink test,
   orphan-sweep test, gating verifier, ZIP repackage + site audit tools).
3. **License-mechanic gaps**: add in-app deactivate/move-device + remaining-activations
   display now, or later? (Lib fn exists; ~small bridge+UI addition.)
4. **AGENTS.md pointer** couldn't be updated — it's a protected file and the approval
   prompt timed out while you were away. The handoff doc (which it points to) carries
   the full state; if you want the pointer text refreshed, approve it next time.
5. **The Pro EXE is now an internal-only artifact** (one-app model: customers get only
   `TotalRecalls.exe`). `dist/TotalRecalls-Pro.exe` + the tracked
   `release/TotalRecalls-1.0.0-pro.zip` (Sept-8, stale) are leftovers from the old
   two-EXE model. I removed the untracked `dist/stage/` intermediates. Recommend:
   stop tracking the Pro EXE/ZIP (or move Pro to a clearly-internal path) so the
   "double-click the wrong one" footgun can't recur. Your call — I won't `git rm`
   tracked artifacts without your go-ahead.
6. **Demo video**: ready to re-record once you've live-tested the free EXE (ChatGPT under
   the 500-storm is the money shot — the status line now shows the retry progress).

## Resumable state

- Branch `RedesignV9`, HEAD unchanged (no commits this session).
- Full file-by-file change list: top of `docs/HANDOFF-website-apps-2026-09-07.md`.
- App log: `%APPDATA%\PerplexityExporter\app.log` (diagnose there first, per project rule).
- If the login window ever blanks again: relaunch the app (sweep runs at startup), or
  Task Manager → end all `msedgewebview2.exe`.
