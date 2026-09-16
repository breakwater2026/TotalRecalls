# HANDOFF — TotalRecalls demo 2026-09-15 (ALL POST DONE — R2 upload + LS reply remain)

EVERYTHING SHOT AND CUT. ALL 3 FINAL VIDEOS RENDERED + VERIFIED (09-15 evening).
Remaining: (1) user uploads the 3 MP4s + 52 site screenshots to the
Cloudflare R2 bucket (`tmt-storage-drive`) with read-view access for the
user and Lemon Squeezy; (2) fill the R2 URLs + socials into
`C:\Users\break\demo-shoot\ls_reply_draft.md` and send.
Next session (~09-16 morning, +8h): **marketing plan** (user's words).
Everything below is decided — don't re-litigate.

## DELIVERED FILES (locked spec: H.264 High, CRF10, aq-mode=0, 2292×1440,
30fps, yuv420p, +faststart, -an)

In `C:\Users\break\OneDrive\TotalRecalls-LS-demo\` (→ re-upload to R2):

| File | Dur | Size | Contents |
|---|---|---|---|
| `totalrecalls_demo_claude_hero.mp4` | 4:18.9 | 60.8 MB | 6 s animated logo intro → full Claude journey (37 convs) 1× → ends Connected + "Download complete!" |
| `totalrecalls_demo_minis_6providers.mp4` | 4:39.5 | 36.8 MB | Pplx→Gemini→Grok→Mistral→Qwen→DeepSeek, 1.5× (on-screen "1.5x speed" badge top-left) |
| `totalrecalls_demo_chatgpt.mp4` | 8:15.6 | 48.6 MB | ChatGPT 105-conversation export 1× → 6 s logo outro |

Quality (vs FFV1 masters, harness below): logo card **SSIM 0.999961 /
PSNR 69.4 dB**; chatgpt body **SSIM 0.999802 / PSNR 61.0 dB**; hero body
previously measured 0.999842 / 67.1 dB. All visually lossless.
(`totalrecalls_demo_claude_hero_30mbps.mp4` in the same folder =
superseded 30 Mbps variant — do not deliver.)

## LOGO (settled after user correction 09-15)

- **Canonical brand logo = `docs/brand/logo_Final.png`** (user-supplied;
  byte-identical to `site/public/logo.png`, sha ff1e887f…): brain-squircle
  icon (dark navy tile, blue brain outline, cyan node squares, mint
  chevron) + wordmark "Total" black / "Recalls" blue + "AI CHAT
  RETRIEVER" tagline. For dark video: white→transparent, "Total"
  black→white (processed copy at `demo-shoot/logo/logo_dark.png`).
- **`site/public/logo-full.svg` (speech-bubble mark) is NOT the brand
  icon** — it was used by mistake in the first card version; user
  rejected it ("it not our logo icon"). Never use it for branding.
- **Animated card** = `demo-shoot/logo/logo_card.html` (faithful replica
  of the landing `ConvergenceDiagram.jsx`: 8 provider tiles → dashed
  curves with moving packets → `C:\TotalRecalls\Library\` folder card;
  `tr-scanline` 3s + `tr-flow` 2s loops → 6 s capture = LCM loop).
- **Capture method (proven, deterministic):** headless Edge
  (`--headless=new --remote-debugging-port=9333`) + Python
  `websockets` → CDP: `document.getAnimations().forEach(a=>{a.pause();
  a.currentTime=i/30})` + `svg.setCurrentTime(i/30)` per frame,
  `Page.captureScreenshot` PNG (2292×1440 via
  `Emulation.setDeviceMetricsOverride`), 180 frames → `ffmpeg
  -framerate 30` → FFV1 master → CRF10. ~0.75 s/frame, perfectly smooth.
  Script: `demo-shoot/logo/capture_logo.py` (repo copy:
  `tools/demo-video/capture_logo_cdp.py`). Do NOT use gdigrab+kiosk for
  browser content: kiosk windows don't enumerate by title and can land on
  a non-primary monitor; the CDP path needs no window placement at all.

## POST PIPELINE FACTS (this session)

- **Claude video trims the hero master's first 5 s** — the FFV1 hero
  opens with a STATIC WHITE logo card (t=0…5.0 s, the shoot's
  placeholder). Frame-exact boundary found by pixel measurement (center
  white-fraction flips at frame 150 = 5.0 s). Re-encode body with
  `-ss 5.0` so the animated card is the only intro.
- **Minis cut:** `masters/seg2_minis_cut.mkv` = 419.198 s, 6 stream-copy
  bands (Perplexity band = accepted `seg2b_pplx` re-shoot: beat t=70 →
  complete t=109; others per EDL). Final render =
  `scale=2292:1440:flags=lanczos,setpts=PTS/1.5,fps=30` + badge
  `overlay=40:40`. **Badge spot proof:** left black region x=0–740,
  y=0–260 has ZERO bright pixels in all 6 bands (pixel-measured, not
  eyeballed). Badge = PIL-rendered 223×64 PNG (Segoe UI Bold 34 "1.5x"
  white + regular 34 "speed" gray, dark translucent fill, blue border) —
  `demo-shoot/logo/badge_1.5x_speed.png` (maker:
  `tools/demo-video/make_badge.py`).
- **ChatGPT cut:** `masters/seg3_chatgpt_cut.mkv` = 489.566 s (beat
  t=112–115 → jump → t=200–686 "Download complete!" + Connected).
- **Assemble = stream-copy concat** (`-f concat -c copy`) of same-spec
  segments (logo_h264 + body). PITFALL HIT: paths in the .txt list are
  **relative to the list file's directory**, not the cwd —
  `renders/renders/...` error.
- **SSIM/PSNR harness (WORKING syntax for this ffmpeg; the naive
  `[a][b]ssim;[a][b]psnr` form FAILS — labels are consumed once):**
  ```
  ffmpeg -i render.mp4 -i master.mkv -filter_complex \
   "[0:v]fps=30,settb=1/30000,split=2[va][vb];[1:v]fps=30,settb=1/30000,split=2[wa][wb];[va][wa]ssim;[vb][wb]psnr" -f null -
  ```
  (fps+settb on BOTH inputs first — 1/1000 vs 1/15360 timebase
  misalignment lies; ~58–60 fps harness speed on this CPU.)
- **Master cuts:** stream-copy trims (`-ss X -t Y -c copy -avoid_negative_ts
  make_zero`), then `-f concat -c copy`. FFV1 masters decode ~30 fps for
  pixel measurements (numpy on rawvideo gray).
- Full render script: `demo-shoot/render_final.sh` (repo copy:
  `tools/demo-video/render_final.sh`) — 6 steps: logo h264 → minis body
  (1.5×+badge) → claude body (trimmed) → chatgpt body → concats → verify.
  Encode rates measured on this CPU (CRF10/slow, 2292×1440): minis body
  (8385 f) ~4 min, claude body (7737 f) ~3.5 min, chatgpt body (14685 f)
  ~6 min.

## STATE ON DISK

- `demo-shoot/masters/`: `seg1_claude_hero.mkv` (257.9 s),
  `seg2_minis.mkv` (21:28.8), `seg2_minis_cut.mkv` (419.198 s),
  `seg2b_pplx.mkv` (accepted re-shoot), `seg3_chatgpt.mkv` (11:40.9),
  `seg3_chatgpt_cut.mkv` (489.566 s). All FFV1.
- `demo-shoot/logo/`: logo_card.html, logo_final.png (user's file, =
  repo docs/brand/logo_Final.png), logo_dark.png, frames_intro/ (180
  PNGs), logo_master.mkv (6.000 s FFV1), badge_1.5x_speed.png,
  capture_logo.py, cdp_grab2.py (attach variant), bench/still images.
- `demo-shoot/renders/`: logo_h264.mp4 (292 KB), minis_body.mp4 (36 MB),
  claude_body_trimmed.mp4, chatgpt_body.mp4 (47 MB), concat lists.
- `demo-shoot/final_qc/`: seam/badge/end frames (verified via vision).
- `demo-shoot/ls_reply_draft.md`: LS reply (pricing $24 launch / $49
  normal, free tier 3 providers/5 convs, 3 activations; product desc;
  video links [R2 URLs TBD]; screenshots [TBD]; contact
  press@/support@totalrecalls.app; socials TBD — repo has NO social
  handles, only those emails).
- 52 site screenshots (user will upload): `site/docs-screenshots/`
  (`01-home.png` … `52-not-found-404.png`).
- EXEs = 09-15 rebuild (PII fix + Perplexity robustness), PYZ-verified,
  222 tests. `dist\TotalRecalls.exe` (free, the customer deliverable) +
  `dist\TotalRecalls-Pro.exe` (internal-only).
- **Delivery model changed 09-15 evening:** OneDrive "anyone link" plan
  SUPERSEDED — user set up a **Cloudflare R2 bucket**
  (`tmt-storage-drive`, dash id 348a35e7f66ce14d4033030a7f16d1f2);
  user + LS get read-view access to videos + screenshots. User uploads;
  agent fills URLs in the draft.
- Git: branch `fix/robust-auth-20260913`; this handoff + logo_Final.png +
  `tools/demo-video/` committed + pushed (see git log).

## OPEN (non-blocking)

1. R2 upload (user) → read-view URLs → fill `ls_reply_draft.md` → user
   sends the LS reply.
2. **Marketing plan** — user's next task (~09-16 morning).
3. Code follow-ups (deferred, documented earlier): ChatGPT export
   fail-fast on definitive auth-failed (+ status/endpoint logging);
   WebView2 orphan sweep mid-session (currently startup-only).

## SHOOT PROTOCOL (proven — unchanged)

- Arm: `cd demo-shoot && rm -f masters/<seg>.mkv && bash shoot.sh
  two_thirds <seg>` (ABORTS if primary ≠ 3440@(0,0); canvas 2292×1440,
  login zone right 1148 px).
- Verify rolling: stat master twice 3 s apart, must GROW (~6–7 MB/s).
- STOP = two steps: kill the session, THEN
  `Stop-Process -Name ffmpeg -Force` (orphaned child locks the master).
- QC frames at NATIVE resolution (downscaled reads hallucinate).
- Monitor layout (09-15): single 3440×1440 ultrawide @ (0,0), primary.

## LESSONS (this session, beyond the skills)

- **A master may open with a placeholder the post pipeline must remove.**
  The hero FFV1 carried a 5 s static white logo card; prepending the new
  animated card without trimming = double logo. Measure the boundary in
  pixels (center white-fraction per frame), don't eyeball.
- **Vision on downscaled frames invents.** "VLC in the left panel" was
  actually a black desktop region + app at x≈787. Native-resolution
  crops (or numpy pixel metrics) before any geometry decision.
- **Deterministic > real-time for animation capture.** Pausing CSS
  animations + SMIL (`getAnimations().forEach(a=>a.currentTime=t)` +
  `svg.setCurrentTime(t)`) and stepping i/30 gives a stutter-free 30 fps
  clip with no window placement, no cursor, no monitor assumptions.
  (CDP gotchas: initial target may be a sync dialog — open the URL, find
  the page target via `:9333/json`; `awaitPromise` on rAF hangs in
  headless — don't await rAF; kill by profile match, never
  `Stop-Process -Name msedge` — it takes the user's Edge too.)
- **Concat list paths are relative to the list file**, not the cwd.
- **PIL badge over the black region** beats drawing text in ffmpeg for a
  styled chip (rounded rect + two weights + border + translucency).
- **Stream-copy concat is safe only when every segment is the same
  codec params** (same CRF10 spec) — re-encode bodies from the FFV1
  masters rather than mixing in differently-encoded intermediates.
