# HANDOFF — demo shoot 2026-09-15 (resume after Perplexity fix)

The Claude hero is DONE and delivered. The 6-provider mini take is SHOT and
cut-ready. The Perplexity PII leak + performance regression are FIXED in code
and EXEs (rebuild + PYZ-verify + push complete, tree clean). Next: Perplexity
re-shoot, then post. Everything below is decided — don't re-litigate.

## DECISIONS LOCKED (do not revisit)

1. **No 25 MB constraint.** Top-quality render → OneDrive "anyone with link"
   URL in the LS reply.
2. **Encode spec — LOCKED, "once and for all" (supersedes the 2-pass 10 Mbps
   draft).** Single-pass libx264 High, **CRF 10**, `aq-mode=0`, NO unsharp
   (A/B proved it hurts), 2292×1440 native, 30 fps, yuv420p, `+faststart`,
   `preset slow`, `-an`. Measured on the full hero: **SSIM 0.999842 / PSNR
   67.1 dB** vs the FFV1 master — visually lossless, 57 MB / 4:18.
   ```
   ffmpeg -y -i masters/<seg>.mkv \
     -vf "scale=2292:1440:flags=lanczos, fps=30" \
     -c:v libx264 -preset slow -crf 10 -x264-params "aq-mode=0" \
     -pix_fmt yuv420p -movflags +faststart -an out.mp4
   ```
   Minis: same spec + `setpts=PTS/1.5` in the filter. Final stitch =
   `-f concat -c copy`. **SSIM/PSNR harness:** force BOTH inputs to
   `fps=30,settb=1/30000` first — naive cross-container compare misaligns on
   1/1000 vs 1/15360 timebases and lies.
3. **Lull-cut policy (all 7 minis + hero):** cut the entire login sequence.
   Keep = `[provider-selected beat ~2.5s] → jump-cut → [download 1/N → N/N
   "Download complete!"]`. The popup / blow-up / grab-and-move / Windows
   Security all fall in the jump. DeepSeek's credential lull = human error,
   cut it too.
4. **End every take Connected.** Stop the take BEFORE disconnecting; a
   voluntary user disconnect at the very end is an acceptable trim point.
5. **Name hiding FINAL:** app folder + library at `C:\TotalRecalls` via
   `TR_DEMO_FOLDER`, launched through the "TotalRecalls (Shoot)" desktop
   shortcut. Breadcrumb = `This PC > Local Disk (C:) > TotalRecalls`.
   Logins parked off-camera RIGHT of the Explorer panel.
6. **PII fix (09-15, shipped):** Perplexity/ChatGPT/Claude `validate()`
   returned the real account email → leaked into the raw log console
   (`unified_export.py:433` prints `account.email` verbatim; `app_ui.html:692`
   has no masking). All three now report `X-session@local` (real email still
   read to confirm the session is live). DeepSeek is API-side masked;
   gemini/grok/mistral/qwen already used placeholders.
7. **Perplexity robustness (09-15, shipped — "alpha provider caught up"):**
   (a) stale CF cookies — the fast login hook (already-signed-in users) never
   saved `cf_clearance`/`__cf_bm` (only the CDP dump did) → 83 CF 403s in 10
   min, connect→first download 68–87s; the hook now saves CF cookies from the
   same request's Cookie header. (b) no cancellation — `stop_event` now
   threaded through Perplexity's http/discover/thread/adapter like ChatGPT's
   (interruptible sleeps; disconnect stops the worker in ~1s instead of
   riding out 60s backoffs). (c) no fast `count_conversations()` — every
   connect ran the full 5-source deep sweep; now a single-index count
   (ChatGPT shape), deep sweep still at export. Also: Perplexity 403 retry
   storms now surface to the UI via the retry sink (same as ChatGPT).
8. **Word content rule (hero):** ONE GENERAL conversation (done — hero is
   locked).

## STATE ON DISK (verify on resume)

- `C:\Users\break\demo-shoot\masters\seg1_claude_hero.mkv` = **LOCKED hero
  master**: 257.9 s, 2.11 GB, FFV1, 2292×1440@30. First frame = 5 s white
  logo intro; last frame = Connected + "Download complete!"; user's
  disconnect at t≈258 is outside the cut.
- `C:\Users\break\OneDrive\TotalRecalls-LS-demo\totalrecalls_demo_claude_hero.mp4`
  = **DELIVERED hero web file**: 57 MB, 4:17.9, 1.88 Mbps, CRF 10,
  SSIM 0.999842 / PSNR 67.1 dB. (The 96.7 MB 30 Mbps variant is superseded.)
- `masters\seg2_minis.mkv` = **6-provider mini take, SHOT**: 1288.8 s
  (21:28.8), 10.9 GB, FFV1. Order: Perplexity (~245–344) → Gemini
  (~356–420) → Grok (~492–585) → Mistral (~658–750) → Qwen (~766–903) →
  DeepSeek (~926–1145); dead head 0:00–~240 (app idle on Claude); tail
  disconnect ~1285–1288 (voluntary).
- **Perplexity's segment in that take is REJECTED** — log console shows
  `Connected as <real email> via perplexity` (t≈260–276). Only the
  Perplexity portion gets re-shot; the other 5 segments are verified clean.
- `compression-tests/webtest/takeA/EDL.txt` = 6 keep bands + 7 cut gaps
  (dead head, 5 login lulls, tail) — **Perplexity's keep band will be
  replaced by the re-shoot segment; re-derive it after the re-shoot.**
- `compression-tests/webtest/takeA/` = QC frames, montages,
  `detect_mess.py` (login-mess motion detector), `bar/timeline.txt`.
- **EXEs = 09-15 rebuild (PII fix + Perplexity robustness), PYZ-verified:**
  `dist\TotalRecalls-Pro.exe` (pro) + `dist\TotalRecalls.exe` (free),
  18.9 MB each. The Shoot shortcut launches the Pro build — **the user's
  app was closed for the rebuild; relaunch via the shortcut.** Perplexity
  session persists (session file), so re-connect is one click.
- Git: `fix/robust-auth-20260913` @ `a7073ac` = origin tip, **tree clean.**
  Commits since morning: `118e3c8` (PII placeholders) → `4deb792`
  (Perplexity robustness) → `a7073ac` (EXE rebuilds).
- `tools/_verify_robustness.py` = PYZ verifier (edition consts + PII
  placeholders + robustness symbols) — run after every future rebuild.
- `masters\seg2b_pplx.mkv` = aborted re-shoot attempt (5 failed tries on the
  OLD build) — delete before re-arming.

## NEXT (in order)

1. **Perplexity re-shoot** with the NEW build: relaunch via the Shoot
   shortcut → confirm Perplexity selected → pre-flight (layout 3440, no
   orphan ffmpeg) → arm `seg2b_pplx` (two_thirds) → user: log in (park popup
   off-camera right) → download to 44/44 → "stop". **Watch the log line: it
   must read `Connected as perplexity-session@local via perplexity`.**
   Expected: connect badge count in seconds (fast count), downloads without
   403 storms (fresh CF cookies), disconnect stops immediately.
2. QC the re-shoot (frames: PII, ending state) → trim to
   `[beat → jump → download → complete]` → **splice into the minis master in
   place of the old Perplexity band** (re-derive that EDL band from the new
   take).
3. Apply the full EDL (6 keeps, login lulls cut) at 1.5× → CRF 10 render →
   `OneDrive\TotalRecalls-LS-demo\` (name it `totalrecalls_demo_minis.mp4`).
4. **ChatGPT take** (`seg3_chatgpt`, separate video, longer) — same protocol;
   widen Explorer so its right edge meets the canvas edge (x=2292) so the
   parked popup zone is right of it.
5. **Logo outro** — user "has an idea"; discuss before building (intro =
   5 s dark wordmark on white, already in the hero).
6. LS reply (user sends; I draft): pricing, video link(s), social URLs,
   product description.

## SHOOT PROTOCOL (proven)

- Arm: `terminal(background=true)`:
  `cd /c/Users/break/demo-shoot && rm -f masters/<segname>.mkv && bash shoot.sh two_thirds <segname>`
  (re-probes layout; ABORTS if primary ≠ 3440@(0,0). `two_thirds` =
  2292×1440 canvas, 1148 px login zone.)
- Verify rolling: ~8 s, stat the master twice 3 s apart — must be GROWING
  (~6–7 MB/s). No file = launch failed, tell the user immediately.
- **STOP (two steps, never one):**
  1. `process_manage(action="kill", session_id=<shoot proc>)` — read the last
     `frame=` line for take length (do NOT ffprobe the GB master).
  2. `powershell -NoProfile -Command "Stop-Process -Name ffmpeg -Force"` —
     the ffmpeg child ORPHANS and keeps the master locked.
- Frame QC before locking: 4–5 frames at NATIVE resolution
  (`ffmpeg -ss T -i C:/…/master.mkv -frames:v 1 out.png`) — downscaling
  caused vision hallucinations once. Check PII (names/emails in the log
  console!), popups in canvas, ending state.
- Segment naming: ask/confirm — never infer from the screen.

## LESSONS (beyond the skill)

- **Trust app.log over memory when a regression is reported.** The Perplexity
  "it was fine before the email fix" claim turned out to be a stale-CF-cookie
  + missing-cancellation pair, fully exonerating the (string-only) PII
  change — the log timestamps + 403 counts + CF file mtime told the whole
  story.
- Perplexity = alpha provider: when hardening other adapters, port the
  pattern back to it (stop_event / retry sink / fast count / CF refresh).
  Verified parity: 221 tests + functional cancellation checks.
- ABR undershoots on screen content (30 Mbps → 3 Mbps actual); CRF is the
  answer. `unsharp` measurably HURTS screen fidelity (A/B'd).
- Downscaled montages make the vision model hallucinate provider states —
  use native-resolution app-window crops.
- The SSIM harness timebase bug (1/1000 vs 1/15360) reports 0.9949 for a
  near-perfect encode — fix the harness before blaming the encode.
- Stale binary copies are the footgun: after any rebuild, `dist\` must hold
  the new files (they do) and the user must relaunch (app was closed for
  this rebuild).
