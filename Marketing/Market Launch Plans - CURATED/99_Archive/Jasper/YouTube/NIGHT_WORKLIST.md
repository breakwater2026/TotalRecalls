# Night worklist — 2026-10-01 (user delegated: implement as many Jasper insights as possible)

## Videos (splice + upload, private)
- [x] A. Master video: ChatGPT shoot 0:30–4:20 @1.5× = **2:53** (under 3:00 ✓) → `videos/TR_yt_master_chatgpt_placeholder.mp4` → uploaded `Bphshxf4luQ`
- [x] B. 6 provider videos @1.5× from cutM_*.mkv → uploaded: pplx `ngEG1qGz7ds`, gemini `8Y8tyuQ9LDI`, grok `UeC-bBej8ho`, mistral `w2bStEH-xwk`, qwen `Mah9B9QIcks`, deepseek `reIGo_aryAU`
- [x] B2. ChatGPT standalone from shoot 0:30→1:34 @1.5× = 59 s → uploaded `TGkLPq4y7mU` (7 non-Claude providers = full set, per user's plan)
- [x] C. All 8 in playlist "Start Here" (`PLHGgAPo4_vi8`) + the earlier Claude hero `99xoJ6w3yXI` (9 total)
- [x] D. Descriptions per Jasper Template 2 (per-video hook + points + CTA + $24 price + hashtags)

## Channel (Jasper cookbook)
- [x] E. Banner 2560×1440 (safe-area text) — **APPLIED via `channelBanners.insert`** (verified bannerExternalUrl)
- [x] F. Channel icon 800×800 from real app mark — built `channel_icon_800.png` (48px QC ✓); Studio manual (API slot absent)
- [ ] F2. Channel description — paste in Studio (API `part=snippet` 400s on this discovery build); text in Master Launch Doc §1.4
- [x] G. Thumbnails: 10 built (Template 2, auto-fit, real app crop) — Studio manual set (API 403 phone-verify)
- [ ] H. Set thumbnails + icon + description in Studio (user, with phone verify)

## Convergence artifact
- [x] I. Recreate ConvergenceDiagram.jsx → 12 s MP4 (real logo paths, animated flows) — `videos/TR_yt_convergence.mp4`
- [x] J. Upload as trailer — **BLOCKED on new-channel daily upload quota** (9 units spent); script ready, retry tomorrow / after phone verify
- [x] J2. **Convergence = channel main video (user, 2026-10-02)** — plan: upload `videos/TR_yt_convergence.mp4` (thumbnail `thumbnails/tr_thumb_convergence.jpg` ready), move it to **position 1** of "Start Here", and in Studio pin it as the **channel trailer** (API `channels.update watch.trailer` returns 400 "Required" on this build — Studio only). Retried 2026-10-02 05:45 EDT: quota still active.
- [x] J3. **Swap DeepSeek → Claude (user, 2026-10-02)** — DONE via playlist surgery: `reIGo_aryAU` (DeepSeek) removed from "Start Here" (stays private pending weekend re-shoot), Claude hero `99xoJ6w3yXI` renamed to **"How to Save Your Claude Chats Locally — TotalRecalls (Windows)"** (was the generic "Save AI Chats from 8 Providers…") + Claude-style description/tags, re-inserted at **position 7** (DeepSeek's slot). Playlist = 8 videos.

## Docs
- [x] K. ONE master document: `Marketing/TotalRecalls Master Launch Document.md` (98 KB — results + plan + full Jasper playbook)
- [x] L. STATUS note updated with tonight's facts

## Verified by
- ffprobe on all 8 uploads (durations + specs), playlistItems.list (9 items), channels().list (banner set),
  vision QC on banner/icon/thumbnails/convergence frames.
