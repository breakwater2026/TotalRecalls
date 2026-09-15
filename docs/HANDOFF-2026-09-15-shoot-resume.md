# HANDOFF — shoot night 2026-09-14 → resume 2026-09-15 (morning)

User ended the shoot night tired, with execution slips in the last two takes
(confidential conversation opened in Word; app left on "Not connected").
Decision: **start over tomorrow morning** with a fresh, well-rested run.
Everything below is decided — don't re-litigate, just execute.

## DISCOVERIES / DECISIONS LOCKED TODAY (do not revisit)

1. **No 25 MB constraint exists.** It was our own email-attachment assumption.
   LS's review letter asks only for "a video demonstrating the functionality
   and features" (plus: pricing breakdown, social URLs for KYB/KYC, product
   description — see "LS reply" below). → **Top-quality render, delivered as
   a OneDrive "anyone with link" URL.** No more bitrate budgeting.
2. **Per-provider recording (user's idea, adopted):** Claude = one full hero
   take (~4 min, 1× speed, includes opening the save-conversation folders in
   Explorer). The other 7 providers = individual 1–2 min minis (login →
   download → done, **no conversation displays**), 1.5× in post. Stitch with
   `concat` + **stream copy** (zero quality loss; stitching itself never adds
   or costs quality — the win is per-clip speed + not showing conversations).
3. **Render spec (final):** native 2292×1440 (canvas res — no downscale =
   sharpest text), 2-pass libx264, preset slow, ~10 Mbps, light unsharp,
   per-clip `setpts` speed, 30 fps. Script: `demo-shoot/render_final_top.sh`
   (fill CUTS after watching takes). Expect ~7–9 GB final file — fine for a
   link.
4. **Name hiding — FINAL (supersedes the symlink idea):** the
   `C:\Users\Profile` alias was a DEAD END — Explorer always renders the
   profile folder (and everything under it) as the account display name
   ("Andre Denis") regardless of reparse points. Working fix = export folder
   + library at **`C:\TotalRecalls`** (C: root) via `TR_DEMO_FOLDER` env var
   (bridge.py priority 1), launched through the desktop shortcut
   **"TotalRecalls (Shoot)"** (→ `launch-hidden.vbs` →
   `Start-TotalRecalls-SHOOT.bat`). Verified on-camera: breadcrumb reads
   `This PC > Local Disk (C:) > TotalRecalls`. The old library was MOVED from
   `C:\Users\break\TotalRecalls-export` to `C:\TotalRecalls` (Library/,
   manifest.json, uuid_index.json, Selected exports/, README.md).
   The `C:\Users\Profile` symlink still exists — optional cleanup:
   `rmdir C:\Users\Profile` from an admin cmd (removes the link only).
5. **Eye toggle (page-2 account email mask) — shipped, user-confirmed
   working.** Keep it masked during takes.
6. **App window placement:** user keeps the app window open between takes in
   its center position (Word left / app center / Explorer right). Don't
   reposition it between takes.
7. **Hero-take ending state (the recurring defect):** the take MUST end
   **Connected + download done + export folder open in Explorer** (Word may
   show ONE general conversation thread as the payoff). Takes 3–5 all ended
   on "Not connected" — user habit: disconnecting Claude at the end, or the
   session lapsing. Tomorrow: **stop the take BEFORE disconnecting**, or
   reconnect/hold connected until the last frame.
8. **Word content rule:** pick a GENERAL conversation (nothing trading/breach
   /work-specific). Take 5 showed a "hard breach notice" trading thread —
   that's the class of slip to avoid.

## SHOOT PROTOCOL (proven tonight)

- Arm: `terminal(background=true)`:
  `cd /c/Users/break/demo-shoot && rm -f masters/<segname>.mkv && bash shoot.sh two_thirds <segname>`
  (shoot.sh re-probes layout; ABORTS if primary ≠ 3440@(0,0). Preset
  `two_thirds` = 2292×1440 canvas, 1148px login zone — the user-approved one.)
- Verify rolling: wait ~8s, stat the master twice 3s apart — must be GROWING
  (~7 MB/s). If NO FILE: the launch failed, tell the user immediately.
- **STOP (two steps, never one):**
  1. `process_manage(action="kill", session_id=<shoot proc>)` — read the last
     `frame=` line for the take length (do NOT ffprobe the GB master).
  2. `powershell -NoProfile -Command "Stop-Process -Name ffmpeg -Force"` —
     **the ffmpeg child ORPHANS when the session is killed and keeps the
     master file locked** ("Device or resource busy" on rm). Both steps,
     every time.
- Frame QC before locking a take: extract 4–5 frames
  (`ffmpeg -ss T -i C:/…/master.mkv -frames:v 1 out.png` — NATIVE paths) and
  vision-check: PII (names/emails), login popups in canvas, Quick-Access
  personal folders (acceptable per user so far), and **the ending state**
  (item 7).
- **Segment naming: ask/confirm — never infer from the screen.** Tonight I
  filed a Claude redo as `seg_perplexity` from a pre-arm frame (app happened
  to show Perplexity); the user corrected it. Pre-arm frame = context only.
- Master files: `masters/<segname>.mkv` FFV1. Old takes are deleted between
  retakes (user says "redo" → kill, Stop-Process ffmpeg, rm the master,
  re-probe layout, then wait for "start").

## STATE ON DISK (verify on resume)

- `masters/seg1_claude.mkv` = **take 5, 4:31, 2.4 GB — NOT LOCKED** (defects:
  ends "Not connected"; Word shows the breach/trading thread). Redo in the
  morning; delete it when the good take replaces it.
- `masters/seg1_claude_full.mkv`, `seg2b_perplexity_qwen.mkv`,
  `seg2c_chatgpt.mkv`, `seg3_deepseek_redo.mkv` = **09-13 superseded takes**
  (kept as reference; can be deleted once the new masters are locked — ~18 GB).
- App EXE = 09-14 Pro build (sha `3fd8fd10…`), launched via the Shoot
  shortcut; eye toggle + clean breadcrumb verified.
- Git: `fix/robust-auth-20260913` pushed to origin (09-15 am snapshot
  `f0a8f73` + the doc-fix commit on top). Working tree CLEAN — nothing
  uncommitted.
- `demo-shoot/`: shoot.sh (native-path fixed), shoot_config.json,
  render_final_top.sh, blur_mask.py v3, PRE-SHOOT-CHECKLIST-2026-09-14.md
  (checklist §"name hiding" now matches the C:\TotalRecalls fix),
  compression-tests/webtest/ = tonight's QC frames (take3/, take5/,
  cmp_*.mp4 bitrate comparisons — no longer relevant to the deliverable,
  keep for reference).

## TOMORROW'S PLAN (in order)

1. Re-probe layout (3440@(0,0), 2560 OFF, 100% scaling — user's physical
   steps).
2. **Claude hero redo**: general conversation in Word; end Connected +
   export folder open; stop before disconnecting. QC frames → lock.
3. The 7 minis (per-provider, ~1–2 min each, logins in the right zone, no
   conversation displays): Perplexity, Gemini, Grok, Mistral, Qwen, ChatGPT,
   DeepSeek (manual-token-paste scenario).
4. Post: fill CUTS in `render_final_top.sh` → top-quality render →
   `C:\Users\break\OneDrive\TotalRecalls-LS-demo\final_totalrecalls_demo.mp4`
   → user shares "anyone with link".
5. LS reply (user sends; I can draft): (1) pricing breakdown, (2) the video
   link, (3) business & personal social URLs (KYB/KYC), (4) product
   description.

## LESSONS (tonight, beyond the skill)

- Tired execution: 4 Claude retakes in one evening; the defects were human
  (wrong conversation, ending state), not tooling. Rest > more retakes.
- `bash ... &` in the terminal tool is rejected — use background=true.
- `cmd //c` with escaped backslashes in bash spawns a bare interactive cmd
  (silent no-op) — run .bat/.vbs chains via `powershell -Command "& '…'"` or
  `wscript`.
- ffmpeg 7 (this build): `-f null -` not `NUL` for throwaway outputs;
  single-pass for quick test clips, 2-pass for finals; input-seek
  `-ss T -i in` is fine on FFV1 masters.
