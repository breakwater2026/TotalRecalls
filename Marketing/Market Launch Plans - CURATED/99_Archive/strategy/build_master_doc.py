"""Assemble the ONE master launch document:
  0. Cover + How to use
  1. TODAY'S RESULTS (2026-10-01) — what got built/uploaded tonight
  2. Operational plan (Master Implementation Plan, full)
  3. YouTube playbook (Strategy, full)
  4. Channel style & spec (full)
  5. Description templates (full)
  6. Hook rankings guide (full)
"""
import os, re, datetime

ROOT = r"C:\Users\break\Projects\TotalRecalls\Marketing"
OUT = os.path.join(ROOT, "TotalRecalls Master Launch Document.md")


def read(rel):
    return open(os.path.join(ROOT, rel), encoding="utf-8").read().strip() + "\n"


def rebase(text, base):
    """Prefix every heading level with the parent number, keep the body intact."""
    out = []
    for line in text.splitlines():
        m = re.match(r"^(#{1,6})\s+", line)
        if m:
            lvl = len(m.group(1))
            out.append(f"{base}{'.'*0}{line}" if False else line)
        else:
            out.append(line)
    return "\n".join(out)


def demote(text, n=1):
    """Add n # to every heading so it nests under our section heading."""
    lines = text.splitlines()
    out = []
    for line in lines:
        m = re.match(r"^(#{1,6})\s+", line)
        if m:
            out.append("#" * min(6, len(m.group(1)) + n) + line[len(m.group(1)):])
        else:
            out.append(line)
    return "\n".join(out) + "\n"


# ---------- 1. Today's results ----------
today = f"""## 1. Today's Results — 2026-10-01 (overnight build, all verified)

Everything below was built and verified tonight per the Jasper cookbook.
Video uploads are PRIVATE in the "Start Here" playlist, pending review.

### 1.1 YouTube channel — OAuth + upload pipeline (RESOLVED)

- OAuth working: code-capture mode (dummy redirect `http://localhost:9/`), PKCE
  S256, `access_type=offline`. Token in `Marketing/Jasper/YouTube/yt-api/token.json`
  (auto-refresh verified).
- Upload pipeline: `yt-api/oauth_final.py` (auth), `yt-api/upload_batch.py`
  (batch insert + playlistItems.add + thumbnails.set).
- Channel: `UChO3ZyrGqRtBFHRuQx2qX1w` (@totalrecalls)
- Playlist "Start Here": `PLHGgAPo4_vi8`

### 1.2 Videos — 8 uploaded (private, in "Start Here")

Master (Claude hero 4:19 at 1.5x = 2:52, placeholder to be re-shot as ChatGPT
this weekend):

| # | File | Title | videoId |
|---|------|-------|---------|
| 1 | TR_yt_master_chatgpt_placeholder.mp4 | TotalRecalls — Every AI Chat, Saved Locally (Master Demo) | Bphshxf4luQ |

Provider videos (~1 min each, so a Qwen-only user never wades through 6
unrelated providers):

| # | File | Title | videoId |
|---|------|-------|---------|
| 2 | TR_yt_provider_chatgpt.mp4 | How to Save Your ChatGPT Chats as Local Files — TotalRecalls (Windows) | TGkLPq4y7mU |
| 3 | TR_yt_provider_pplx.mp4 | How to Save Your Perplexity Chats as Local Files — TotalRecalls (Windows) | ngEG1qGz7ds |
| 4 | TR_yt_provider_gemini.mp4 | How to Save Your Google Gemini Chats as Local Files — TotalRecalls (Windows) | 8Y8tyuQ9LDI |
| 5 | TR_yt_provider_grok.mp4 | How to Save Your Grok Chats as Local Files — TotalRecalls (Windows) | UeC-bBej8ho |
| 6 | TR_yt_provider_mistral.mp4 | How to Save Your Mistral Chats as Local Files — TotalRecalls (Windows) | w2bStEH-xwk |
| 7 | TR_yt_provider_qwen.mp4 | How to Save Your Qwen Chats as Local Files — TotalRecalls (Windows) | Mah9B9QIcks |
| 8 | TR_yt_provider_deepseek.mp4 | How to Save Your DeepSeek Chats as Local Files — TotalRecalls (Windows) | reIGo_aryAU |

Durations (verified): master 172.7s (2:53); chatgpt 55.3s; pplx 26.1s;
gemini 51.4s; grok 54.3s; mistral 16.9s; qwen 50.0s; deepseek 81.0s.
Encodes: 1440x900 h264 (crf 18, preset slow) + silent AAC.
Plan: `yt-api/uploads_plan.json` (titles/descriptions/tags from Jasper's
Description Templates).

### 1.3 Channel branding

- Banner 2560x1440 built from the real app icon (`build_channel_assets.py`),
  all text in the central 1546x423 safe area. Uploaded via
  `channelBanners.insert` — live `bannerExternalUrl` verified.
- Channel icon 800x800 (app mark) built; QC'd at 48px (recognizable).
  API icon slot (`brandingSettings.image`) not exposed on this discovery
  build — set in Studio.
- Palette (Jasper Channel Style): Obsidian #111315, Graphite #1A1D21,
  Paper #F3EFE7, Steel Blue #7A8FA6, Slate #2A2F36.

### 1.4 Thumbnails — 10 built, Template 2 (Product Proof)

`build_thumbnails.py` → `Marketing/Jasper/YouTube/thumbnails/` (1280x720).
Auto-fit headline fonts (100-120px, 3-5 words), top-left chip, headline,
bottom-left evidence chip, bottom-right keep-clear for the length stamp,
right-side real product-screenshot card (app window cropped per frame).
One per video + master + convergence.

### 1.5 Convergence animation (the old landing-page artifact, recovered)

`build_convergence_video.py` recreates `site/src/components/landing/ConvergenceDiagram.jsx`
as a 15s 1920x1080 MP4: 8 provider tiles with real logo paths
(from `RiskMatrix.LOGOS`), brand-color tiles, animated dashed data-flow
curves converging to the `C:\\TotalRecalls` folder, moving packets
(staggered 0.4s, 2.4s loop), sweep scanline, "8 SOURCES → 1 FOLDER".
Output: `Marketing/Jasper/YouTube/videos/TR_yt_convergence.mp4`.
Upload it as a channel trailer / pinned video once verified.

### 1.6 Remaining for the user (needs manual Studio / weekend)

- [ ] Review all 8 private videos; set publish times (stagger per Strategy §Schedule).
- [ ] Set custom thumbnails in Studio (API 403 — phone verification pending);
      files ready in `thumbnails/`.
- [ ] Set the channel icon in Studio (API slot not exposed); file ready
      (`channel_icon_800.png`).
- [ ] Verify the banner crop in Studio (desktop strip QC'd:
      `qc_banner_desktop_strip.png`).
- [ ] Re-shoot master as ChatGPT demo this weekend → replace video Bphshxf4luQ
      (keep the title/description/thumbnail).
- [ ] Convergence: review the MP4, upload as channel trailer.
"""

# ---------- assemble ----------
master_plan = read(r"strategy/TotalRecalls Master Implementation Plan.md")
yt_strategy = read(r"Jasper/YouTube/TotalRecalls YouTube Strategy.md")
channel_style = read(r"Jasper/YouTube/TotalRecalls YouTube Channel Style.md")
desc_templates = read(r"Jasper/YouTube/YouTube Description Templates.md")
hook_rankings = read(r"Jasper/YouTube/TotalRecalls Hook Rankings Guide.md")

cover = f"""# TotalRecalls — Master Launch Document

> ONE document: the operational plan + every Jasper insight, plus what was
> actually built and uploaded on 2026-10-01. This supersedes the separate
> Master Implementation Plan and the scattered YouTube docs (all of which are
> included verbatim below, in order).

**Product truth:** TotalRecalls downloads your AI conversations from eight
providers into local Markdown and JSON files — one-time $24 Pro, Free Tier to
try first.

## How to use this document

| Section | What it is | Read it when |
|---------|-----------|--------------|
| 1. Today's Results (2026-10-01) | What was built/uploaded + what's left | First — the current state |
| 2. Master Implementation Plan | 45-day operational command sheet | Daily — owners, status, KPIs |
| 3. YouTube Strategy | The YT playbook (strategy, schedule, hooks) | When touching YT |
| 4. YouTube Channel Style | Visual spec: palette, banner, thumbnails, layout | When making assets |
| 5. YouTube Description Templates | Copy-paste descriptions per video type | When writing descriptions |
| 6. Hook Rankings Guide | Ranked opening hooks per provider | When writing titles/hooks |

Status key: ⬜ Not started · 🟡 In progress · ✅ Done · ⏸ Blocked
"""

toc = """
---

"""

doc = (
    cover
    + toc
    + today
    + "\n---\n\n## 2. Master Implementation Plan (operational command sheet)\n\n"
    + demote(master_plan, 1)
    + "\n---\n\n## 3. YouTube Strategy (cookbook)\n\n"
    + demote(yt_strategy, 1)
    + "\n---\n\n## 4. YouTube Channel Style & Spec\n\n"
    + demote(channel_style, 1)
    + "\n---\n\n## 5. YouTube Description Templates\n\n"
    + demote(desc_templates, 1)
    + "\n---\n\n## 6. Hook Rankings Guide\n\n"
    + demote(hook_rankings, 1)
)

open(OUT, "w", encoding="utf-8").write(doc)
print("wrote", OUT, f"({len(doc):,} chars, {len(doc.splitlines()):,} lines)")
