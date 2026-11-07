# HANDOFF — 2026-11-07: Website Launch-Ready & Demo Videos Remake Setup

> **Read this first in any new session.** All facts below are verified on disk and live via real tools.  
> **Topic of Next Session**: Remaking the TotalRecalls promotional & walkthrough demo videos (Landing Page Scroller Demo + YouTube promotional assets + `/see-it-work/` provider takes).

---

## 1. Current Website & Catalog State (LOCKED & PRE-DEPLOYED)

- **Repo Root**: `C:\Users\break\Projects\TotalRecalls-Source Code`
- **Astro App Root**: `C:\Users\break\Projects\TotalRecalls-Source Code\site`
- **Dev Server**: Running on `http://localhost:4321/` (verified 200 OK)
- **Build Status**: `npm run build` cleanly compiles **61 static routes with 0 errors / 0 warnings**, generating 60 sitemap URLs.

### Canonical Pricing Ladder & Live Paddle Billing Wiring
- **Downloader Pro**: Regular `$48 USD`, Launch Price **`$24 USD`** (one-time purchase, 8 providers, up to 3 PC activations, free bug-fix updates for life).
  - Price ID: `pri_01m37qpx77bst2w1gnf3zkf4zd` ($48.00)
  - Discount ID: `dsc_01m39879ga7pv9zg0gsvzqsmjw` (50% off, `expires_at: null`) $\rightarrow$ **`$24.00 USD`**
- **Smart Search Engine (SSE) Add-on**: Regular `$58 USD`, Launch Price **`$29 USD`** (requires Downloader Pro, 7-day refund policy).
  - Price ID: `pri_01m6qftvhs2yt7c0yrgr0xy5tg` ($58.00)
  - Discount ID: `dsc_01m39879ga7pv9zg0gsvzqsmjw` (50% off, `expires_at: null`) $\rightarrow$ **`$29.00 USD`**
- **Pro + SSE Bundle**: Regular `$98 USD`, Launch Price **`$49 USD`** (one checkout, both products).
  - Price ID: **`pri_01m6w18jd6qtnr0e40b5kf7m0b`** ($98.00)
  - Discount ID: `dsc_01m39879ga7pv9zg0gsvzqsmjw` (50% off, `expires_at: null`) $\rightarrow$ **`$49.00 USD`**
- **Free Tier**: ChatGPT, Claude, and Perplexity with **5 conversations per provider** (never "per download").
- **Webhook Fulfillment**: `paddle-fulfillment-worker/src/worker.js` recognizes `pri_01m6w18jd6qtnr0e40b5kf7m0b` in `PADDLE_BUNDLE_IDS` and issues both Pro and SSE keys upon purchase.
- **Button Routing**: All buy buttons across `/#pricing`, `/smart-search/`, and `/buy/` are tested and verified in Chromium to resolve to their exact Paddle prices.
- **Standalone `/pricing/`**: 301 redirected straight to `/#pricing`.

### Landing Page Scroller Architecture (Alternating Palette Strictly Enforced)
1. `Hero` (`bg-tr-obsidian`)
2. `How It Works` (`bg-tr-graphite` — Box 01 $24 chip, Box 03 8 providers + arrow bridge to `/providers/`, Box 04 arrow bridge to `/library/`, Box 05 regular search vs SSE $29 chip)
3. `Demo` (`bg-tr-obsidian` — "Watch TotalRecalls (Pro + SSE) in action" + arrow bridge to `/see-it-work/`)
4. `Ownership / Why` (`bg-tr-graphite` — sensitive personal data examples: medical, financial, psychological, relationships + arrow bridge to `/library/`)
5. `Smart Search Engine (SSE)` (`bg-tr-obsidian` — Semantic Vector search & RAG storage, local C:\TotalRecalls\Library\ + arrow bridge to `/smart-search/`)
6. `Pricing` (`bg-tr-graphite` — 4 cards: Free, Downloader Pro $24, SSE add-on $29, Bundle $49)
7. `Straight Talk / Trust` (`bg-tr-obsidian` — Card 1: "No download on our servers")
8. `FAQ` (`bg-tr-graphite`)
9. `Site Documentation & Resource Index` (`bg-tr-obsidian` — 5 live link columns covering all 42 standalone pages)
10. `Footer` (`bg-tr-graphite`)

---

## 2. Next Session Focus: Remaking the Demo Videos

### Locations & Rig Specs
- **Primary Filming Workspace**: **`C:\Users\break\demo-shoot\`** (NOT in the website repo).
- **Authoritative Rig Spec**: Read **`C:\Users\break\demo-shoot\RIG.md`**.
- **Display Canvas**:
  - Primary Canvas: **`3440×1440`** (21:9 ultrawide)
  - Secondary Login Zone: `2560` width
- **Four Panel Layout (Watchdog Grid)**:
  1. Word / Text Viewer: `(0, 0, 817, 1440)`
  2. Windows File Explorer: `(817, 0, 857, 1440)`
  3. TotalRecalls App: `(1674, 0, 842, 1440)`
  4. TotalRecalls Marketing Website: `(2516, 0, 924, 1440)` (snapped by `window_watchdog.py`, 1 zoom step out so `$24` price sits inside frame).

### Core Rig Scripts (`C:\Users\break\demo-shoot\`)
- `shoot.sh`: Main recording coordinator (note: python on PATH, not stale venv path).
- `window_watchdog.py`: Keeps the 4 panels locked to exact pixel coordinates.
- `demo-license-stub.py`: Local license verification server on `:8788`.
- `reset-to-free.ps1`: Resets TotalRecalls app state back to Free Tier for clean takes.
- `_purge_chatgpt_login.ps1`: Purges browser session/cookies for fresh login flows.

### Technical Video Specifications (Locked Standards)
- **Resolution**: `3440×1440`
- **Framerate**: `30 fps`
- **Encoding**: `yuv420p`, **CRF 10** (`render_final_top.sh`), faststart, no audio for embed takes or synced narration audio for YouTube.
- **Redaction / Masking**: Title mask `x=1290-1674, y=210-1440 boxblur=20:3` applied once conversation titles appear in Explorer.
- **Hold Rules**: Start 3.0s BEFORE clicking "Download free" on website; end 3.0s after final cursor movement of `.json` scroll (Document1 `.md` displayed first, `.json` displayed last).

### User Preferences for Video & Audio Production
- **Narration Voice**: Prefers male "guy" voice (**`en-US-GuyNeural`**) via Edge/TTS over robotic voices.
- **Editing Process**: Interactive, iterative video editing with frame previews before finalizing renders.
- **Card Designs & Scripts**: The user prefers to review scripts and create title/outro cards in Canva personally before final assembly.

### Relevant Skills to Load
- `demo-video-production-package`: Produce TotalRecalls demo videos, script to ship.
- `kokoro-tts` / `text_to_speech`: Narration audio synthesis.
- `youtube-content`: YouTube script structure and hooks.
- `astro-marketing-pages`: Marketing pages and video embed integration.

---

## 3. Quick-Start Commands for Next Session

```bash
# 1. Inspect demo shoot workspace
cd "C:/Users/break/demo-shoot"
ls -la

# 2. Check rig documentation
cat RIG.md

# 3. Check existing rendered masters & cuts
ls -la renders/
```
