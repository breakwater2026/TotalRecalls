# TotalRecalls — Master Launch Document

> ONE document: the operational plan + every Jasper insight, plus what was
> actually built and uploaded on 2026-10-01. This supersedes the separate
> Master Implementation Plan and the scattered YouTube docs (all of which are
> included verbatim below, in order).
>
> 2026-10-03 ingest: §2 replaced by Master Implementation Plan V3 (dated
> 2026-10-03); §7 YouTube Implementation Plan and §8 Master Plan V2 (kept as
> reference, superseded by V3) added; §9 adds all ten Jasper blog posts.

**Product truth:** TotalRecalls downloads your AI conversations from eight
providers into local Markdown and JSON files — one-time $24 Pro, Free Tier to
try first.

## How to use this document

| Section | What it is | Read it when |
|---------|-----------|--------------|
| 1. Today's Results (2026-10-01) | What was built/uploaded + what's left; 1.7 = 2026-10-03 ingest status + open decision items | First — the current state |
| 2. Master Implementation Plan V3 | Operational command sheet, V3 (2026-10-03) — adds blog series tracker, KPI ladder | Daily — owners, status, KPIs |
| 3. YouTube Strategy | The YT playbook (strategy, schedule, hooks) | When touching YT |
| 4. YouTube Channel Style | Visual spec: palette, banner, thumbnails, layout | When making assets |
| 5. YouTube Description Templates | Copy-paste descriptions per video type | When writing descriptions |
| 6. Hook Rankings Guide | Ranked opening hooks per provider | When writing titles/hooks |
| 7. YouTube Implementation Plan | Week-by-week channel build & run, blog series plan, KPI ladder | When executing YT work |
| 8. Master Implementation Plan V2 | Superseded consolidated plan (2026-10-02), kept for reference | Reference |
| 9. Blog Series | All 10 Jasper blog posts, verbatim | When writing/publishing content |

Status key: ⬜ Not started · 🟡 In progress · ✅ Done · ⏸ Blocked

---

## 1. Today's Results — 2026-10-01 (overnight build, all verified)

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
| 1 | TR_yt_master_chatgpt_placeholder.mp4 | See TotalRecalls in Action — Every AI Chat, Saved Locally (Master) | Bphshxf4luQ |

Provider videos (~1 min each, so a Qwen-only user never wades through 6
unrelated providers):

| # | File | Title | videoId |
|---|------|-------|---------|
| 2 | TR_yt_provider_chatgpt.mp4 | How to Save Your ChatGPT Chats as Local Files — TotalRecalls (Windows)| TGkLPq4y7mU |
| 3 | TR_yt_provider_pplx.mp4 | How to Save Your Perplexity Chats Locally — TotalRecalls (Windows)| ngEG1qGz7ds |
| 4 | TR_yt_provider_gemini.mp4 | How to Save Your Gemini Conversations Locally — TotalRecalls (Windows)| 8Y8tyuQ9LDI |
| 5 | TR_yt_provider_grok.mp4 | How to Save Your Grok Chats Locally — TotalRecalls (Windows)| UeC-bBej8ho |
| 6 | TR_yt_provider_mistral.mp4 | How to Save Your Mistral Chats Locally — TotalRecalls (Windows)| w2bStEH-xwk |
| 7 | TR_yt_provider_qwen.mp4 | How to Save Your Qwen Chats Locally — TotalRecalls (Windows)| Mah9B9QIcks |
| 8 | TR_yt_provider_deepseek.mp4 | How to Save Your DeepSeek Chats Locally — TotalRecalls (Windows)| reIGo_aryAU |

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
as a 12s 1280x720 MP4: 8 provider tiles with real logo paths
(from `RiskMatrix.LOGOS`), brand-color tiles, animated dashed data-flow
curves converging to the `C:\TotalRecalls` folder, moving packets
(staggered 0.4s, 2.4s loop), sweep scanline, "8 SOURCES → 1 FOLDER".
Output: `Marketing/Jasper/YouTube/videos/TR_yt_convergence.mp4` (12.0s, verified).
Thumbnail ready: `thumbnails/tr_thumb_convergence.jpg`.
⏸ Upload BLOCKED on the new-channel daily upload quota (see 1.6) — file +
upload script ready (`yt-api/upload_convergence.py`, title "How TotalRecalls
Works — 8 AI Providers Into One Local Folder"). Upload tomorrow or after phone
verification; pin as channel trailer.

### 1.6 Remaining for the user (needs manual Studio / weekend)

- [ ] Review all 8 private videos; set publish times (stagger per Strategy §Schedule).
- [ ] Upload the convergence MP4 (blocked on quota today) → pin as channel trailer.
- [ ] Set custom thumbnails in Studio (API 403 — phone verification pending);
      files ready in `thumbnails/` (10 total: 9 videos + convergence).
- [ ] Set the channel icon in Studio (API slot not exposed); file ready
      (`channel_icon_800.png`).
- [ ] Verify the banner crop in Studio (desktop strip QC'd:
      `qc_banner_desktop_strip.png`).
- [ ] Re-shoot master as ChatGPT demo this weekend → replace video Bphshxf4luQ
      (keep the title/description/thumbnail). The original Claude hero
      (`99xoJ6w3yXI`, "Save AI Chats from 8 Providers to One Folder") stays in
      the playlist as a bonus video.

### 1.7 Status update — 2026-10-03 (Jasper ingest complete)

Jasper access is ending; every remaining Jasper output is now downloaded and
embedded in this document, so the compendium is self-contained.

- §2 replaced by **Master Implementation Plan V3** (dated 2026-10-03); the old
  45-day plan is superseded.
- §7 (**YouTube Implementation Plan**) and §8 (**Master Plan V2**, superseded,
  reference) added.
- §9: all **10 blog posts** embedded verbatim; canonical copies in
  `Jasper/YouTube/Blog/`.

⚠ Verification findings — decision items, none resolved silently:

1. **V3's blog tracker is stale.** V3 says "the series is 9 posts. There is no
   Blog 10" and marks Blogs 6–9 pending. All 10 posts exist in `Blog/` and are
   written (plus a Markdown-vs-JSON explainer). Flip the tracker statuses before
   running against V3.
2. **Filename convention mismatch.** V3 §5 mandates dated kebab-case
   (`YYYY-MM-DD-<slug>.md`); actual files use mixed names without dates. Decide:
   rename now or amend the convention.
3. **Duplicate blog copies.** The 10 blog files exist hash-identical at both
   `Jasper/YouTube/` root and `Jasper/YouTube/Blog/`. `Blog/` is treated as
   canonical; delete the root copies once Jasper access ends.
4. **Library path inconsistency.** V3 example paths use
   `C:\Users\break\Library\TotalRecalls`; the app's demo/real library lives at
   `C:\TotalRecalls`. Blogs' example filenames are internally consistent but not
   with either path as written.
5. **KPI ladder start date open.** Both plans carry the same 8-week KPI ladder
   (Week 4: 100 subs / 1,000 views; Week 8: 1,000 subs / 10,000 views / 50
   emails). If launch-day = Week 1 of that ladder, blog publish dates follow from
   it.
6. **Blog-side critical path.** All 10 written → next actions are the V3 §5
   fixes (second-person review, Blog 4 first), publish Blogs 1–2, then the
   staggered schedule. YT build side is done except §1.6 user items.

---

## 2. Master Implementation Plan V3 (operational command sheet)

> Supersedes the previous 45-day plan (embedded in the 2026-10-01 edition of this
> document). Dated 2026-10-03. Blog tracker below reflects status at write time:
> all ten blog posts now exist in `Blog/` (see §9).

## TotalRecalls Master Implementation Plan V3

**Status:** Current operating document. Replaces the previous "TotalRecalls Master Implementation Plan."\
**Status date:** October 3, 2026\
**Key update:** The 9-post blog series is now partly written. Blogs 3, 4, 5, and 9 are complete as standalone assets. Blogs 6, 7, and 8 are still pending.\
**Built for:** A founder-led team that records, writes, and publishes in small batches.

TotalRecalls makes one promise: **your AI conversations, saved to your own PC as Markdown and JSON files.** This plan shows how the website, guides, blog, YouTube channel, social posts, and email support that promise. It covers what's done, what's left, and the order for the remaining work.

---

### Status Legend

These markers are used throughout the plan:

| Marker           | Meaning                                                              |
| ---------------- | -------------------------------------------------------------------- |
| ✅ **Complete**   | Written or built as a final asset                                    |
| 🔄 **In review** | Written, but waiting on an accuracy check or a fix before publishing |
| ⏳ **Pending**    | Not yet started or not yet written                                   |
| 🔍 **Confirm**   | Status or detail needs to be checked before work continues           |

---

### 1. How to Use This Plan

This document is the single source of truth for priorities and timing. The supporting documents hold the detail.

| Document                                           | What It Covers                                     | Status                       |
| -------------------------------------------------- | -------------------------------------------------- | ---------------------------- |
| **Master Implementation Plan V3** (this document)  | Decisions, blog status, timeline, guardrails       | ✅ Current                    |
| **Content Audit Plan V2**                          | Keep, update, merge, create, and retire decisions  | ✅ Current                    |
| **TotalRecalls YouTube Strategy** (latest version) | Channel setup, video types, playlists, cadence     | ✅ Current                    |
| **YouTube Description Templates**                  | Description structure, UTM naming, pinned comments | ✅ Current                    |
| **Footer Signup Success Messages**                 | Post-signup copy                                   | 🔄 Final corrections pending |
| **Blog 3: Markdown vs JSON Explainer**             | Which saved file to use                            | ✅ Written                    |
| **Blog 4: Privacy Explainer**                      | What "not sent to our servers" means               | ✅ Written                    |
| **Blog 5: Backup Library Folder**                  | How to back up saved chats                         | ✅ Written                    |
| **Blog 9: VS Code Workflow**                       | Using saved chats in VS Code                       | ✅ Written                    |
| **Library Folder Explainer Blog**                  | Where TotalRecalls saves your files                | 🔍 Confirm its series number |

**Precedence rule:** If two documents disagree, this plan wins.

**Superseded documents:** The first "TotalRecalls YouTube Channel Strategy" draft and the previous Master Implementation Plan are replaced. Archive them so nobody works from old versions.

---

### 2. Finalized Decisions

These decisions are closed. Reopen one only if the trigger in the last column happens.

| Area                  | Decision                                                                                    | Reopen Only If                                                                                     |
| --------------------- | ------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| **Blog spotlights**   | **Option A approved.** No standalone provider spotlight articles.                           | A clearly different search intent appears that no guide covers. Even then, test one article first. |
| **Blog series scope** | **9 posts total.** Explainers, ownership, and workflow topics only. No provider spotlights. | Never expand past 9 without a new decision.                                                        |
| **Provider coverage** | **One written guide and one YouTube guide video per provider**, plus a short Proof Demo.    | A provider is added or removed.                                                                    |
| **Email signup**      | **Sitewide footer only.** One form per page. No popups, sticky bars, or exit-intent modals. | Footer signups stay near zero after 90 days.                                                       |
| **CTA order**         | Download free first, Pro or pricing second, email updates third.                            | Never.                                                                                             |
| **Channel role**      | YouTube is a **public evidence library**, not an ad channel or creator brand.               | Never.                                                                                             |
| **Trailer**           | A 45–60 second cut of the See It Work demo. No brand film.                                  | Never.                                                                                             |
| **Archive Amber**     | Reserved for **Download free** and **Buy Pro** on the website only.                         | Never.                                                                                             |
| **Platforms**         | Windows 10 and 11. macOS and Linux are "in development," with no dates.                     | A version actually ships.                                                                          |

**Note on series length:** An earlier message mentioned a "Blog 10." The series is 9 posts. There is no Blog 10.

---

### 3. Core Message Rules

#### One Job Per Asset

Each page, guide, blog post, and video has one clear job. If two assets do the same job, merge them. This is why the spotlight series was cancelled, and why each blog post covers one topic that no guide already handles.

#### Call-to-Action Hierarchy

| Priority | Action                                  | Where It Appears                                          |
| -------- | --------------------------------------- | --------------------------------------------------------- |
| **1**    | **Download free**                       | Every page, guide, blog post, video, and description      |
| **2**    | **Buy Pro** or **Compare Free and Pro** | Pricing, Pro guides, Going Pro videos                     |
| **3**    | **Get product updates** (email)         | Site footer, Product Update videos, YouTube About section |

Every blog post ends with a single ask: **Download free at totalrecalls.app.** The four finished posts already follow this rule.

#### Brand Colors Across Channels

| Token             | Hex       | Use                                                           |
| ----------------- | --------- | ------------------------------------------------------------- |
| **Obsidian**      | `#111315` | Backgrounds on the site footer, banner, thumbnails, end cards |
| **Paper**         | `#F3EFE7` | Headlines, wordmark, thumbnail text                           |
| **Mist**          | `#D9D4CB` | Body copy, success messages                                   |
| **Steel Blue**    | `#7A8FA6` | Eyebrows, file paths, series markers, focus states            |
| **Archive Amber** | Reserved  | Download free and Buy Pro on the website only                 |

---

### 4. Blog Series Status

The blog fills the real content gap identified in the audit: explainers, ownership, and workflow content. It replaces the time the spotlight series would have taken.

#### Progress at a Glance

|            | Count                     |
| ---------- | ------------------------- |
| ✅ Written  | 4 of 9 (Blogs 3, 4, 5, 9) |
| ⏳ Pending  | 3 of 9 (Blogs 6, 7, 8)    |
| 🔍 Confirm | 2 of 9 (Blogs 1, 2)       |
| Published  | 0 of 9                    |

#### Series Tracker

| #     | Topic                                                             | Type      | Status     | Paired Video                                     | Next Step                                                        |
| ----- | ----------------------------------------------------------------- | --------- | ---------- | ------------------------------------------------ | ---------------------------------------------------------------- |
| **1** | To confirm                                                        | —         | 🔍 Confirm | —                                                | Confirm topic and draft status                                   |
| **2** | To confirm (likely the Library Folder explainer)                  | Ownership | 🔍 Confirm | Where TotalRecalls Saves Your Files (launch set) | Confirm whether the Library Folder explainer is Blog 1 or Blog 2 |
| **3** | Markdown vs JSON: Which Saved File Should You Use?                | Explainer | ✅ Written  | Markdown vs JSON video                           | Accuracy review, then schedule                                   |
| **4** | What "Not Sent to Our Servers" Means in TotalRecalls              | Explainer | ✅ Written  | "Not sent to our servers" video                  | **Second-person privacy review required**                        |
| **5** | How to Back Up Your AI Conversation Library                       | Ownership | ✅ Written  | Backup video                                     | Accuracy review, then schedule                                   |
| **6** | Proposed: Searching saved chats with Windows search               | Ownership | ⏳ Pending  | Windows search workflow video                    | Write by Week 6                                                  |
| **7** | Proposed: Organizing saved chats by project                       | Ownership | ⏳ Pending  | Organizing workflow video                        | Write by Week 7                                                  |
| **8** | Proposed: Using saved chats in a note-taking app such as Obsidian | Workflow  | ⏳ Pending  | Note-taking app workflow video                   | Write by Week 8                                                  |
| **9** | How to Use Your Saved AI Chats in VS Code                         | Workflow  | ✅ Written  | VS Code workflow video (after day 90)            | Accuracy review, then schedule                                   |

The proposed topics for Blogs 6, 7, and 8 come from the content audit's ownership list. Blog 9 also points readers to search, organizing, and Obsidian, so these three topics would close the loop. Confirm them before writing starts.

#### What Changed from V2

The earlier plan scheduled these pieces later. Writing has moved ahead of schedule:

| Piece                              | Planned Before | Actual Status |
| ---------------------------------- | -------------- | ------------- |
| Markdown vs JSON (Blog 3)          | Weeks 7–8      | ✅ Written     |
| "Not sent to our servers" (Blog 4) | Weeks 7–8      | ✅ Written     |
| Backup (Blog 5)                    | Weeks 11–12    | ✅ Written     |
| VS Code / editor workflow (Blog 9) | After day 90   | ✅ Written     |

That frees writing time in Weeks 7–12. Use it for Blogs 6–8 and for upgrading the eight provider guides.

#### Standard Blog Structure

Blogs 6, 7, and 8 should match the structure the finished posts already use, so the series reads as one set:

1. **Meta title and meta description**
2. **Opening:** what the post covers, reading time, and what you'll learn
3. **The Short Answer:** three points
4. **Main sections**, each ending with a bold **Takeaway**
5. **A side-by-side or task table**
6. **Common Questions**
7. **The Recommendation for Most People:** three plain steps
8. **Closing section** with the Free Tier note and **Download free at totalrecalls.app**

#### Blog Rules

- One topic per post. No overlap with a provider guide.
- No provider spotlights, logos, or implied partnerships.
- Third-party apps, such as VS Code or Obsidian, are named as plain text only.
- Each post links to its matching guide and, once live, embeds its matching video.
- Every post gets a second-person accuracy check against Section 14 before publishing.

---

### 5. Blog Consistency Fixes

Reviewing the finished posts side by side turned up a few details that need one agreed answer. Fix these before any blog goes live.

| Issue                           | Where It Appears                                                                                             | Action                                                                                     | Status     |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ | ---------- |
| **Saved filename format**       | Blog 3 shows `quarterly-report-draft.md`. Blog 9 says filenames start with a date, such as `2026-09-18-...`. | Confirm the real format in the app, then update every post, guide, and thumbnail to match. | 🔍 Confirm |
| **Default Library folder path** | Blog 9 uses `C:\TotalRecalls\Library\`                                                                       | Confirm the real default path in the released app.                                         | 🔍 Confirm |
| **Pro license check wording**   | Blog 4 says the license check sends only the license key                                                     | Confirm this matches how activation actually works.                                        | 🔍 Confirm |
| **Gemini Takeout conversion**   | Blog 4 says conversion happens on the user's PC                                                              | Confirm this matches the released app.                                                     | 🔍 Confirm |
| **Example dates**               | Blogs 3 and 9 use example dates in 2026                                                                      | Fine as examples. Keep them consistent across posts.                                       | ✅ OK       |

These are small edits, but they matter. A reader who opens their Library folder and sees a different filename format will question everything else.

---

### 6. Website Implementation

The website explains the details and handles the download. Everything else sends people here.

#### Page-by-Page Plan

| Page                    | Job                                       | Matching Video                   | Action                        | Status            |
| ----------------------- | ----------------------------------------- | -------------------------------- | ----------------------------- | ----------------- |
| **Homepage**            | Explain the product, drive Free downloads | 60-second demo                   | Embed demo                    | ⏳ Pending         |
| **See It Work**         | Prove the app works                       | 60-second demo, Pro upgrade demo | Confirm CTA order             | ⏳ Pending         |
| **Pricing**             | Explain Free vs Pro                       | Free vs Pro explained            | Embed video, check wording    | ⏳ Pending         |
| **Provider guides** (8) | Provider-specific how-tos                 | One guide video per provider     | Upgrade all eight             | ⏳ Pending         |
| **Blog** (9 posts)      | Explainers, ownership, workflow           | One video per post where planned | Publish in order (Section 12) | 🔄 4 of 9 written |
| **Ownership Path**      | Help people use their files               | Using Your Saved Chats videos    | Link Blogs 5–9, embed videos  | ⏳ Pending         |
| **Founder Story**       | Build personal trust                      | Why I Built TotalRecalls         | Embed when ready              | ⏳ Pending         |
| **Legal and Privacy**   | Explain data handling                     | None                             | Name email service provider   | 🔍 Confirm        |

#### Linking the Blog into the Site

| Blog                            | Link From                                                            |
| ------------------------------- | -------------------------------------------------------------------- |
| Blog 3: Markdown vs JSON        | Every provider guide's "What you get" section, starting with ChatGPT |
| Blog 4: Not sent to our servers | Homepage trust section, See It Work, Pricing, footer privacy line    |
| Blog 5: Backup                  | Ownership Path, Library Folder explainer                             |
| Blog 9: VS Code                 | Ownership Path, Blog 3                                               |
| Blogs 6–8                       | Ownership Path, once published                                       |

#### Footer Email Signup

The signup appears once per page, in the global footer, above the legal links. It never sits beside Download free or Buy Pro.

| Element             | Final Copy or Rule                                                                         |
| ------------------- | ------------------------------------------------------------------------------------------ |
| **Eyebrow**         | PRODUCT UPDATES                                                                            |
| **Headline**        | Follow what we build next                                                                  |
| **Description**     | Occasional emails about new features, new AI providers, and what's coming to TotalRecalls. |
| **Label**           | Email address (visible, not placeholder-only)                                              |
| **Button**          | Get updates, in the Secondary style. Never Archive Amber.                                  |
| **Error message**   | Please enter a valid email address.                                                        |
| **Success message** | From the Footer Signup Success Messages document, after final corrections                  |
| **Privacy line**    | Your email is never shared with any third party. Unsubscribe anytime.                      |

**Before launch, confirm:**

1. The Privacy Policy names your email service as a service provider.
2. Single or double opt-in. If single, remove any "check your inbox" line from the success message.
3. GDPR and CASL consent rules are met for EU, UK, and Canadian sign-ups.

#### Visual Review Checklist

A full visual review is still pending. Run it after the final corrections go live.

- Download free is the first and most visible action on every page
- Archive Amber appears only on Download free and Buy Pro
- Only one signup form shows per page
- Video embeds use click-to-play or lazy loading
- Blog posts render code blocks, tables, and file trees cleanly
- Mobile layouts stack cleanly with readable text
- Keyboard focus is visible on every link, field, and button

---

### 7. Provider Guides

Guides are the core of the content library. With Option A approved, they also carry the spotlight role.

#### Standard Guide Structure

1. **What you get:** the two files TotalRecalls saves, with a link to Blog 3
2. **Why this provider matters:** two or three neutral sentences
3. **Embedded video:** the matching Provider Guide video
4. **Step-by-step instructions** with screenshots
5. **Where your files go:** the Library folder
6. **Common problems and fixes**
7. **CTA:** Download free (Free Tier) or Compare Free and Pro (Pro)

#### Provider Rollout

| Provider       | Tier | Guide Update | Video      | Note                              | Status    |
| -------------- | ---- | ------------ | ---------- | --------------------------------- | --------- |
| **ChatGPT**    | Free | Weeks 3–4    | Launch set | Lead guide. Link to Blog 3.       | ⏳ Pending |
| **Claude**     | Free | Weeks 3–4    | Launch set | Add file examples.                | ⏳ Pending |
| **Perplexity** | Free | Weeks 3–4    | Launch set | Use "threads."                    | ⏳ Pending |
| **Gemini**     | Pro  | Week 5       | Week 5     | **Explain Google Takeout first.** | ⏳ Pending |
| **Grok**       | Pro  | Weeks 5–6    | Week 6     | Add Pro note.                     | ⏳ Pending |
| **DeepSeek**   | Pro  | Weeks 5–6    | Week 6     | Add Pro note.                     | ⏳ Pending |
| **Mistral**    | Pro  | Weeks 5–6    | Week 7     | Add Pro note.                     | ⏳ Pending |
| **Qwen**       | Pro  | Weeks 5–6    | Week 8     | Add Pro note.                     | ⏳ Pending |

#### Guide Rules

- Keep "Why this provider matters" short and neutral.
- Write provider names as plain text. Never use logos.
- Never criticize a provider or imply a partnership.
- Note the TotalRecalls version and the month each guide was last checked.

---

### 8. YouTube Channel

Full detail lives in the YouTube Strategy and Description Templates. This section covers planning.

#### Channel Setup

| Element           | Final Spec                                                                                | Status    |
| ----------------- | ----------------------------------------------------------------------------------------- | --------- |
| **Name**          | TotalRecalls (no tagline)                                                                 | ⏳ Pending |
| **Handle**        | @TotalRecalls, or @TotalRecallsApp. Claim it now.                                         | ⏳ Pending |
| **Profile image** | Mark in Paper on Obsidian, tested at 40 pixels                                            | ⏳ Pending |
| **Banner**        | Wordmark, "Save your AI conversations as local files.", `MARKDOWN · JSON · WINDOWS 10/11` | ⏳ Pending |
| **Header links**  | Download free, See It Work, Guides, Pricing, with UTM tags                                | ⏳ Pending |
| **Trailer**       | 45–60 second See It Work cut, captioned                                                   | ⏳ Pending |

#### Launch Set

1. TotalRecalls in 60 Seconds: One Real ChatGPT Download (also the trailer)
2. How to Save ChatGPT Conversations to Your PC
3. How to Save Claude Conversations to Your PC
4. How to Save Perplexity Threads to Your PC
5. Where TotalRecalls Saves Your Files
6. Free vs Pro: What's Included in Each

#### Blog-Paired Videos

Finished blog posts make these videos faster to script. Each post's sections and Short Answer can become the video outline.

| Video                                     | Script Source | Planned Weeks |
| ----------------------------------------- | ------------- | ------------- |
| Markdown vs JSON                          | Blog 3 ✅      | Weeks 9–10    |
| What "not sent to our servers" means      | Blog 4 ✅      | Weeks 9–10    |
| Backing up your AI conversation library   | Blog 5 ✅      | Weeks 11–12   |
| Searching saved chats with Windows search | Blog 6 ⏳      | Weeks 9–10    |
| Organizing saved chats by project         | Blog 7 ⏳      | Weeks 11–12   |
| Note-taking app workflow                  | Blog 8 ⏳      | After day 90  |
| VS Code workflow                          | Blog 9 ✅      | After day 90  |

#### Cadence

| Phase       | Timing         | Output                                   |
| ----------- | -------------- | ---------------------------------------- |
| **Launch**  | Weeks 3–4      | 6 videos together                        |
| **Build**   | Weeks 5–12     | One long video per week, plus 1–2 Shorts |
| **Steady**  | Month 4 onward | Two long videos per month                |
| **Ongoing** | Always         | Re-record when interfaces change         |

#### Playlists

Launch with **Start Here**, **Provider Guides**, and **Quick Demos**. Add **Going Pro**, **Using Your Saved Chats**, **Troubleshooting**, and **Product Updates** once each has at least three videos.

#### Production Rules

- Real screen capture only. Never mock up a screen.
- Calm pacing, clear audio, uploaded captions
- Blur emails, profile images, conversation titles, license keys, and order numbers. Never show a session token.
- Enlarged cursor, 1080p or higher, zoomed app window
- Straight cuts or short crossfades
- Disclose trimmed loading time in every description

#### UTM Standard

```
?utm_source=youtube&utm_medium=[video|comment|channel]&utm_campaign=[series]-[topic]&utm_content=[link]
```

Series codes: `demo`, `guide`, `workflow`, `explainer`, `fix`, `update`. Log every campaign in the tracking sheet.

---

### 9. Social Content

Social posts carry the short, shareable provider angle that spotlights would have played. Finished blogs add a new source of material.

#### Per-Provider Set

| Post                    | Content                                              | Links To       |
| ----------------------- | ---------------------------------------------------- | -------------- |
| **Proof post**          | 15–45 second clip of a real download                 | Matching guide |
| **"What you get" post** | Screenshot of a saved Markdown file, details blurred | Matching guide |
| **Tip post**            | One practical fix from the guide                     | Matching guide |

#### Blog-Based Posts

| Blog      | Post Idea                                                        | Status                                      |
| --------- | ---------------------------------------------------------------- | ------------------------------------------- |
| Blog 3    | "Markdown is for people. JSON is for software."                  | Ready once Blog 3 publishes                 |
| Blog 4    | The connection path diagram: provider → your PC → Library folder | Ready once Blog 4 is reviewed and published |
| Blog 5    | "Back up the whole Library folder" with the four methods         | Ready once Blog 5 publishes                 |
| Blog 9    | One VS Code search shortcut for saved chats                      | Ready once Blog 9 publishes                 |
| Blogs 6–8 | One tip per post                                                 | ⏳ After writing                             |

#### Social Rules

- One idea per post
- Link to the guide or blog post, never a spotlight article
- No fear-based hooks about lost or deleted chats
- No provider logos
- Pair $24 with "launch price" in any pricing post

---

### 10. Email

| Element           | Plan                                                                                                 |
| ----------------- | ---------------------------------------------------------------------------------------------------- |
| **Source**        | Footer signup only                                                                                   |
| **Frequency**     | Only when there's real news                                                                          |
| **Topics**        | New features, new providers, macOS and Linux progress                                                |
| **Blog mentions** | A short "new on the blog" line is fine inside a real update. Don't send emails for blog posts alone. |
| **Platform rule** | macOS and Linux stay "in development." No dates.                                                     |
| **Unsubscribe**   | One-click link in every email                                                                        |

---

### 11. How Everything Connects

#### The Funnel

1. **Discover:** Someone searches on YouTube or Google.
2. **Trust:** A real screen recording, a clear guide, or an honest blog post shows what happens.
3. **Visit:** A description link, guide CTA, or blog CTA brings them to totalrecalls.app.
4. **Try:** They download the Free Tier.
5. **Upgrade:** Pro guides, Going Pro videos, and Pricing help them decide.
6. **Stay:** The footer signup and Product Update videos keep them connected.

#### Where the Blog Fits

Guides answer "how do I save this?" The blog answers "what does this mean?" and "what can I do with my files?" Blogs 3 and 4 build trust before download. Blogs 5 through 9 keep people using the app after download.

#### Assets Per Provider

| Asset                | Count | Upkeep                            |
| -------------------- | ----- | --------------------------------- |
| Written guide        | 1     | Quarterly check                   |
| Provider Guide video | 1     | Re-record when interfaces change  |
| Proof Demo           | 1     | Re-record when interfaces change  |
| Social posts         | 3     | Retire when the video is replaced |

---

### 12. Unified 12-Week Action Plan

This timeline merges the audit, the YouTube plan, and the blog series.

#### Timeline Changes in V3

- **Blogs 3, 4, 5, and 9 are written early.** Their writing slots in Weeks 7–12 are now free.
- **Blogs publish in series order, one per week, from Week 3 to Week 11.** Week 12 is a buffer.
- **Blogs 6, 7, and 8 must be written at least two weeks before their publish week.**
- **Publishing is gated by review.** No post goes live until it passes the accuracy check and the fixes in Section 5.
- **Guide links to Blog 3** go live in Week 5, when Blog 3 publishes.

#### Blog Publishing Schedule

| Week | Publish                         | Gate                               | Status     |
| ---- | ------------------------------- | ---------------------------------- | ---------- |
| 3    | Blog 1                          | Topic and draft confirmed          | 🔍 Confirm |
| 4    | Blog 2                          | Topic and draft confirmed          | 🔍 Confirm |
| 5    | Blog 3: Markdown vs JSON        | Filename format fixed              | ✅ Written  |
| 6    | Blog 4: Not sent to our servers | Second-person privacy review       | ✅ Written  |
| 7    | Blog 5: Backup                  | Path confirmed                     | ✅ Written  |
| 8    | Blog 6                          | Written by Week 6                  | ⏳ Pending  |
| 9    | Blog 7                          | Written by Week 7                  | ⏳ Pending  |
| 10   | Blog 8                          | Written by Week 8                  | ⏳ Pending  |
| 11   | Blog 9: VS Code                 | Path and filename format confirmed | ✅ Written  |
| 12   | Buffer                          | Catch up on any delayed post       | —          |

If Blogs 1 or 2 aren't ready by Week 3, shift the whole schedule by one week rather than publishing out of order.

#### Week 0: Prerequisites

- ⏳ Implement the final website corrections
- ⏳ Run the visual review checklist
- 🔍 Confirm Free Tier limit wording: "per provider" or "per download"
- 🔍 Confirm single or double opt-in
- 🔍 Confirm the Privacy Policy names the email service provider
- 🔍 Confirm Blog 1 and Blog 2 topics and status
- 🔍 Confirm topics for Blogs 6, 7, and 8
- 🔍 Confirm saved filename format and default Library path
- ⏳ Claim @TotalRecalls on YouTube and matching social handles

#### Weeks 1–2: Accuracy and Setup

| Workstream     | Tasks                                                                                                                          |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| **Website**    | Run every page against the guardrails. Archive spotlight drafts. Apply the confirmed Free Tier wording.                        |
| **Blog**       | Apply Section 5 fixes to Blogs 3, 4, 5, and 9. Run second-person review on all four, with Blog 4 first. Start drafting Blog 6. |
| **YouTube**    | Create profile image, banner, and About section. Add header links with UTM tags. Build the thumbnail template.                 |
| **Production** | Record, edit, and caption the six launch videos.                                                                               |
| **Systems**    | Set up one tracking sheet for videos **and** blog posts: title, claims, date, version, UTM campaign, status.                   |

#### Weeks 3–4: Launch

| Workstream  | Tasks                                                                                                    |
| ----------- | -------------------------------------------------------------------------------------------------------- |
| **YouTube** | Publish the launch set. Set the trailer. Build three launch playlists. Pin a comment on every video.     |
| **Guides**  | Upgrade the ChatGPT, Claude, and Perplexity guides. Embed their videos.                                  |
| **Website** | Embed the demo on Homepage and See It Work. Add Free vs Pro to Pricing. Publish the Library Folder page. |
| **Blog**    | Publish Blogs 1 and 2. Finish Blog 6 draft. Start Blog 7.                                                |
| **Social**  | Post Free Tier provider sets. Cut 2–3 Shorts.                                                            |

#### Weeks 5–8: Pro Coverage and Explainers

| Workstream  | Tasks                                                                                                                     |
| ----------- | ------------------------------------------------------------------------------------------------------------------------- |
| **Guides**  | Upgrade all five Pro guides. Rewrite the Gemini opening to explain Google Takeout first. Add Blog 3 links to every guide. |
| **YouTube** | Publish one Pro guide per week, starting with Gemini. Record each Proof Demo in the same session. Launch Going Pro.       |
| **Blog**    | Publish Blogs 3, 4, 5, and 6. Finish Blogs 7 and 8 drafts by Week 8.                                                      |
| **Social**  | Post Pro provider sets and Blog 3–5 posts as they go live.                                                                |
| **Review**  | Log recurring questions. First monthly metrics review in Week 8.                                                          |

#### Weeks 9–12: Trust and Ownership

| Workstream  | Tasks                                                                                                                                                                                                     |
| ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **YouTube** | Publish Markdown vs JSON, "not sent to our servers," Windows search, backup, and organizing videos. Start Using Your Saved Chats and Troubleshooting. Publish the founder video and first Product Update. |
| **Blog**    | Publish Blogs 7, 8, and 9. Embed matching videos in Blogs 3, 4, 5, and 6 as they go live.                                                                                                                 |
| **Website** | Link all published blogs from Ownership Path. Embed the founder video.                                                                                                                                    |
| **Email**   | Send the first update email only if there's real news.                                                                                                                                                    |
| **Review**  | Second metrics review. Plan the next quarter.                                                                                                                                                             |

#### Day 90 Checkpoint

By the end of Week 12, you should have:

- All 9 blog posts published, each linked from the right pages
- All eight provider guides on the standard structure, each with an embedded video
- About 18–22 long videos and around 15–20 Shorts
- Five or six active playlists
- Blog videos embedded for Blogs 3–7, with Blogs 8 and 9 videos planned for next quarter
- Clear data on which pages, posts, and videos send the most downloads

---

### 13. Weekly Operating Rhythm

| Day           | Focus                                                                                         |
| ------------- | --------------------------------------------------------------------------------------------- |
| **Monday**    | Plan the week. Check comments, support emails, and downloads by source.                       |
| **Tuesday**   | Record. Batch two or three videos in one setup.                                               |
| **Wednesday** | Edit, caption, and cut Shorts.                                                                |
| **Thursday**  | Write blog drafts, descriptions, thumbnails, and guide updates. Second-person accuracy check. |
| **Friday**    | Publish the week's blog post and video, embed, post social, update the tracking sheet.        |

#### The Minimum Week

When a week gets busy, protect these and let the rest slide:

1. Reply to support emails and video comments
2. Publish one scheduled item, either the blog post or the video
3. Fix any claim that no longer matches the website

---

### 14. Accuracy Guardrails

These apply to every page, guide, blog post, video, description, pinned comment, social post, and email.

| Topic                | Say This                                                                   | Never Say This                                        |
| -------------------- | -------------------------------------------------------------------------- | ----------------------------------------------------- |
| **Privacy**          | "Your conversations aren't sent to our servers."                           | "Fully offline," "never touches the internet"         |
| **Platforms**        | "Windows 10 and 11. macOS and Linux are in development."                   | Release dates, "coming soon"                          |
| **Gemini**           | "Gemini works through a Google Takeout file."                              | "One-click Gemini download"                           |
| **Price**            | "$24 one-time (launch price)"                                              | Unpublished discounts or end dates                    |
| **Devices**          | "Pro activates on up to 3 PCs."                                            | "Unlimited devices"                                   |
| **Updates**          | "For the life of the product"                                              | "Forever," "lifetime updates"                         |
| **Account**          | "No TotalRecalls account to create"                                        | "No sign-in needed"                                   |
| **Email**            | "Never shared with any third party" (once the Privacy Policy is confirmed) | Any promise the Privacy Policy doesn't support        |
| **Providers**        | Names as plain text                                                        | Logos, or any implied partnership                     |
| **Third-party apps** | Named as plain text, for demonstration                                     | Any implied partnership or endorsement                |
| **Speed**            | Disclose trimmed loading time                                              | Anything suggesting faster speeds than users will see |
| **Features**         | Only what's in the released version                                        | Planned or unreleased features                        |
| **Files and paths**  | The confirmed filename format and Library path                             | Examples that don't match the real app                |

#### Review Process

- A second person checks every new asset against this table before publishing.
- Blog 4 gets the strictest review, since it explains exactly what connects to the internet.
- When website wording changes, update blog posts, video descriptions, and pinned comments the same week.
- Keep prices out of video descriptions and blog body copy. Let the Pricing page carry the number.

---

### 15. Remaining Gaps

These are the open items that block or shape remaining work.

| Gap                                 | Affects                           | Decision or Work Needed                 | Status     |
| ----------------------------------- | --------------------------------- | --------------------------------------- | ---------- |
| **Blogs 1 and 2 status**            | Publishing schedule               | Confirm topics and whether drafts exist | 🔍 Confirm |
| **Blogs 6, 7, 8**                   | Series completion                 | Confirm topics, then write              | ⏳ Pending  |
| **Filename format**                 | Blogs 3 and 9, guides, thumbnails | Confirm the real format                 | 🔍 Confirm |
| **Default Library path**            | Blog 9, guides                    | Confirm the real path                   | 🔍 Confirm |
| **Free Tier limit wording**         | Every channel                     | "Per provider" or "per download"        | 🔍 Confirm |
| **Opt-in type**                     | Success message, email setup      | Single or double                        | 🔍 Confirm |
| **Footer success message**          | Footer signup                     | Apply final corrections                 | ⏳ Pending  |
| **Email service in Privacy Policy** | Footer privacy line, Blog 4       | Confirm it's named                      | 🔍 Confirm |
| \*\*Consent                         |                                   |                                         |            |

---


## 3. YouTube Strategy (cookbook)

## TotalRecalls YouTube Strategy

A YouTube channel can help TotalRecalls grow, but only if it has one clear job. For a privacy-focused Windows app that saves AI conversations as local Markdown and JSON files, that job is:

**Show the app working, honestly, so people trust it enough to try it.**

This document covers how to build and run the channel. It includes the channel's purpose, setup and branding, content, playlists, thumbnails, titles, upload cadence, discoverability, the link to the website funnel, accuracy rules, measurement, and a 90-day plan.

---

### 1. What the Channel Is For

Agree on the channel's role before any setup work. A clear purpose makes every later decision easier, from which videos to make to which links to include.

#### The Channel's Core Job

Most people searching for a way to save their AI chats have the same doubts:

- Does this actually work?
- Where do my conversations go?
- Is this safe to sign in to?
- What will I end up with on my computer?

A real screen recording answers all four in under a minute. Written copy can't do that as well. That's why YouTube matters for TotalRecalls: **it turns claims into visible proof.**

#### What the Channel Should Do

- **Prove the app works.** Show real downloads, start to finish, ending with files open on screen.
- **Answer real search questions.** Cover the phrases people type, such as "how to save ChatGPT conversations" or "download Claude chats."
- **Help existing users.** Show how to organize, search, back up, and reuse saved files.
- **Send viewers to the website.** Point them to totalrecalls.app, where they can download the Free Tier.
- **Show steady progress.** Share honest updates that prove the product is maintained.

#### What the Channel Shouldn't Do

- Act as a stream of ads for the product
- Chase AI news, trends, or reaction content
- Use hype, fast cuts, dramatic music, or fake urgency
- Depend on a personality-driven creator brand
- Use fear about losing chats to drive downloads

#### The Guiding Idea

Think of the channel as a **public evidence library**. Each video is a small, verifiable piece of proof. One video won't change much. Fifty accurate, calm, useful videos will make TotalRecalls look like the most trustworthy option in its category.

---

### 2. Channel Setup and Branding

The channel should look like a natural extension of the website. Same colors, same calm tone, same honest claims. A visitor moving between YouTube and totalrecalls.app should feel no gap.

#### Channel Name

- **Use:** TotalRecalls
- **Avoid:** Taglines or keywords in the name, such as "TotalRecalls | Save Your AI Chats"

Names with taglines look cluttered in search results, get cut off on phones, and age badly when the product grows. The description and video titles handle keywords better.

#### Handle

- **First choice:** @TotalRecalls
- **Backup:** @TotalRecallsApp

Claim the handle now, even before the first upload. Handles can't be reserved, and losing the clean version later would be a hassle. Use the same handle on any other social accounts for consistency.

#### Profile Image

The profile image appears tiny in comments, search results, and subscription lists. It needs to work at about 40 pixels wide.

- Use the TotalRecalls mark or wordmark in Paper on an Obsidian background
- Keep it centered with generous padding, since YouTube crops it into a circle
- Don't add taglines or extra text
- Check it at small sizes on both light and dark YouTube themes before you commit

#### Banner

The banner should explain the product in one glance. YouTube crops banners heavily on phones and TVs, so keep all key content inside the center safe area.

**Recommended content:**

- TotalRecalls wordmark in Paper
- One line in Paper: **Save your AI conversations as local files.**
- A small detail line in Steel Blue mono: `MARKDOWN · JSON · WINDOWS 10/11`
- Obsidian background, with an optional quiet file or folder motif

**Avoid:**

- **AI provider logos.** They can suggest an endorsement, and trademark use gets complicated.
- **Upload schedules.** If you miss one, the channel looks abandoned.
- **Archive Amber.** It stays reserved for primary calls to action on the website.
- **Price mentions.** The $24 launch price will change, and banners often go unupdated.

#### About Section

The About section should be short, factual, and easy to scan. Here's a draft you can use as written:

> TotalRecalls is a Windows app that downloads your AI conversations to your own PC as Markdown and JSON files.
>
> You sign in to each provider inside the app, on your own computer. Your conversations aren't sent to our servers, and there's no TotalRecalls account to create.
>
> The Free Tier covers ChatGPT, Claude, and Perplexity. Pro adds Gemini (through Google Takeout), Grok, DeepSeek, Mistral, and Qwen, with unlimited downloads.
>
> This channel shares real screen recordings of the app, step-by-step provider guides, and simple ways to organize and reuse your saved chats.
>
> TotalRecalls runs on Windows 10 and 11. macOS and Linux versions are in development.
>
> Get product updates by email: totalrecalls.app

Before publishing, check that the provider list, Free Tier limit wording, and platform status match the live website exactly.

#### Channel Links

Add these four links to the channel header, in this order:

1. **Download free** → totalrecalls.app
2. **See It Work** → the See It Work page
3. **Guides** → the Guides section
4. **Pricing** → totalrecalls.app/pricing/

Only the first link shows beside the channel name on most screens, so make it the download. Keep the total to four. More links dilute attention.

Add UTM tags to each link, such as `?utm_source=youtube&utm_medium=channel&utm_campaign=header`, so you can tell channel-header traffic apart from video traffic.

#### Channel Trailer

Use a short version of the See It Work demo as the trailer for visitors who aren't subscribed. It already does exactly the right job.

- **Length:** 45–60 seconds
- **Content:** Open the app, choose ChatGPT, sign in, pick a conversation, download, then open the Markdown and JSON files
- **Ending:** A calm closing card: "Download free at totalrecalls.app"
- **Captions:** On, with an uploaded caption file
- **Description note:** "Real screen recording. Personal details are blurred. Loading time is trimmed."

Don't produce a separate brand film. A polished brand video would feel like advertising. The real demo feels like proof, and proof is what this channel sells.

#### Channel Home Layout

Arrange the home tab so new visitors see proof first and depth second:

1. **Channel trailer:** the 60-second demo
2. **Start Here:** the core videos for new visitors
3. **Provider Guides:** one full guide per provider
4. **Using Your Saved Chats:** workflow and file videos
5. **Latest uploads**

Add the Troubleshooting, Going Pro, and Product Updates sections once each has at least three videos. Empty sections make the channel look unfinished.

---

### 3. Content Strategy

#### Content Pillars

Every video should fit one of four pillars. If an idea doesn't fit, it probably doesn't belong on the channel.

| Pillar        | Purpose                                         | Example                                         |
| ------------- | ----------------------------------------------- | ----------------------------------------------- |
| **Proof**     | Show the app working with no editing tricks     | "TotalRecalls in 60 seconds: one real download" |
| **How-To**    | Answer specific search questions                | "How to save Claude conversations to your PC"   |
| **Ownership** | Help people use, organize, and keep their files | "What to do with your saved AI chats"           |
| **Updates**   | Show steady, honest progress                    | "What's new in TotalRecalls this month"         |

**Early balance:** Proof and How-To should make up about 70% of the first three months. They match search demand and build trust fastest. Ownership and Updates grow in share as the user base grows.

#### Video Types

##### Proof Demos

Short, literal recordings of the app doing exactly what the website says it does.

- **Length:** 45–90 seconds
- **Structure:** One provider, one conversation, one download, ending with both files open
- **Editing:** Minimal. Trim loading time only, and say so in the description.
- **Captions:** Always on

**Order of production:**

1. ChatGPT (also the trailer)
2. Claude
3. Perplexity
4. Then each Pro provider: Gemini, Grok, DeepSeek, Mistral, and Qwen

Proof Demos are the backbone of the channel. They also embed well on the website, where they support the See It Work page and the homepage.

##### Provider Guides

Fuller walkthroughs for each provider, aimed at people searching for a solution.

- **Length:** 3–6 minutes
- **Covers:** Opening the app, choosing the provider, signing in, selecting conversations, downloading, finding files, and fixing common problems
- **Format:** One video per provider, kept current
- **Pairing:** Each video matches a written guide on the website

**The Gemini guide needs special care.** Gemini works through a Google Takeout file, not a one-click download. The guide should explain this in the first 20 seconds, then show each step: requesting the Takeout file, downloading it, and bringing it into TotalRecalls. Nobody should finish the video expecting Gemini to work like ChatGPT.

##### Workflow and File Videos

Videos about what people can do once their conversations are saved as files. These help existing users and attract people who care about keeping their work organized.

**Topic ideas:**

- Opening Markdown files in Notepad, VS Code, or a note-taking app
- Organizing the Library folder by project, client, or date
- Searching across saved chats with Windows search
- What's inside the JSON file, and when it's useful
- Backing up the Library folder to an external drive or cloud folder
- Moving saved chats into a personal knowledge base
- Sharing a single saved conversation with a coworker

When showing third-party apps, name them as text only. Don't imply any partnership or endorsement.

##### Explainers

Calm, short videos that explain the "why" behind the product. They should teach, not lecture.

- **Length:** 2–4 minutes
- **Format:** Screen recording with spoken explanation, plus simple diagrams if needed

**Topic ideas:**

- Why it's worth keeping your own copy of AI conversations
- Markdown vs JSON: which file should you use?
- What "local" means in TotalRecalls, and what still connects to the internet
- Free vs Pro, explained plainly

**The "local" explainer matters most.** Downloads connect directly from the user's PC to each AI provider. The video should say that clearly. Never describe the app as "fully offline" or claim it "never touches the internet." Honest detail here builds more trust than a bold claim.

##### Troubleshooting

Short, specific fixes for real support questions. They take little effort and often earn steady search traffic for years.

- **Length:** 30 seconds to 2 minutes
- **Structure:** Name the problem, explain the cause briefly, show the fix, confirm it worked

**Starting topics:**

- The sign-in window won't load
- "Where did my files go?"
- How to activate a Pro license key
- How to move Pro to a new PC (within the three-PC limit)
- A download stopped partway through

Build this list from real support emails, not guesses. Every repeated support question is a video waiting to be made.

##### Updates

Brief, honest notes on what changed.

- **Length:** 1–3 minutes
- **Structure:** What's new, what's fixed, what's in progress
- **Rule:** No release dates for macOS, Linux, or new providers until they're real and published

Updates show the product is alive and maintained. That matters to anyone deciding whether to pay for software. They're also the natural place to mention the email signup for product news.

##### Shorts

Shorts help reach new people, but they should stay disciplined.

- **Length:** 15–45 seconds, vertical
- **Rule:** One idea per Short, such as "Your ChatGPT chat, saved as a Markdown file"
- **Source:** Cut from longer videos where possible, to save production time
- **Link:** Connect each Short to its related full video using YouTube's related video feature

**Short ideas:**

- One chat, one download, files open (per provider)
- The Library folder in 20 seconds
- What a saved Markdown file looks like
- Finding an old chat with Windows search
- Markdown vs JSON in 30 seconds

Don't build the channel around Shorts. They bring reach, but long videos earn trust and send people to the website.

#### Starter Topic Backlog

These 20 videos cover the first few months, roughly in priority order:

1. TotalRecalls in 60 seconds: one real ChatGPT download
2. How to save ChatGPT conversations to your PC
3. How to save Claude conversations to your PC
4. How to save Perplexity threads to your PC
5. Where TotalRecalls saves your files (the Library folder)
6. Free vs Pro: what's included in each
7. Markdown vs JSON: which saved file should you use?
8. How to upgrade to Pro and activate your license key
9. How to save Gemini conversations using Google Takeout
10. How to save Grok conversations to your PC
11. How to save DeepSeek conversations to your PC
12. How to save Mistral conversations to your PC
13. How to save Qwen conversations to your PC
14. What "not sent to our servers" means in TotalRecalls
15. Searching all your saved AI chats with Windows search
16. Organizing your saved chats by project
17. Backing up your AI conversation library
18. Opening saved chats in a note-taking app
19. Why I built TotalRecalls (founder story)
20. What's new in TotalRecalls: first update

Videos 1–6 form the launch set. Videos 7–13 complete provider coverage. Videos 14–20 deepen trust and help current users.

#### Production Style

Use the same production rules as the See It Work demo. Consistency between the website and the channel is part of the trust signal.

- **Real screen capture only.** Never mock up or recreate a screen.
- **Calm pacing.** Narrate like you're showing a friend what's on your screen.
- **Clear audio.** A decent USB microphone in a quiet room beats any visual polish.
- **Captions on every video.** Upload your own caption file instead of relying on auto-captions, which often garble provider names.
- **Blur everything personal.** Emails, profile images, conversation titles, license keys, and order numbers. Never show a session token.
- **Enlarged cursor** with a soft click highlight, so viewers can follow along on phones.
- **Readable screen size.** Record at 1080p or higher, and zoom the app window so text is legible on mobile.
- **Straight cuts or short crossfades.** No zoom punches, flying logos, or swelling music.
- **Quiet or no background music.** If used, keep it low and neutral.
- **Disclose trimming.** If loading time is cut, say so in the description.
- **Note the version.** Mention the TotalRecalls version and recording month in each guide's description.

Face-on-camera content is optional. A founder intro or update can add warmth, but the product should always be the focus.

#### What Not to Make

- Reaction videos to AI news
- "Top 10 AI tools" lists
- Comparisons that criticize other products by name
- Clickbait about AI companies deleting your chats
- Videos that use fear to drive downloads
- Sponsored segments or affiliate promotions for unrelated tools
- Videos promising features that don't exist yet

Fear and hype might bring clicks. They also undercut the calm, reliable brand the website has built, and they attract viewers who leave quickly.

---

### 4. Playlist Structure

Playlists help people find the right video and keep watching. They also give each video more chances to appear in search and suggested videos.

| Playlist                   | What Goes In It                                                     | Who It's For                            |
| -------------------------- | ------------------------------------------------------------------- | --------------------------------------- |
| **Start Here**             | 60-second demo, Library folder video, Free vs Pro, Markdown vs JSON | New visitors                            |
| **Provider Guides**        | One full guide per provider                                         | People searching for a specific AI tool |
| **Quick Demos**            | 60-second proof videos, one per provider                            | Skeptics and skimmers                   |
| **Using Your Saved Chats** | Organizing, searching, backing up, opening files                    | Current users                           |
| **Going Pro**              | Upgrade walkthrough, license activation, moving PCs                 | Free users considering Pro              |
| **Troubleshooting**        | Short fixes for common problems                                     | Users who are stuck                     |
| **Product Updates**        | Changelogs and progress notes                                       | Returning users and followers           |

#### Playlist Rules

- **Lead with the most useful video**, not the newest one.
- **Write a short description** for every playlist, using plain search terms. For example: "Step-by-step guides for saving your ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral, and Qwen conversations to your PC."
- **Use videos in more than one playlist** when it makes sense. The ChatGPT guide belongs in both Start Here and Provider Guides.
- **Start small.** Launch with Start Here, Provider Guides, and Quick Demos. Add the others once each has at least three videos.
- **Keep order logical.** In Provider Guides, list Free Tier providers first, then Pro providers.
- **Review quarterly.** Remove unlisted or outdated videos and reorder as new ones arrive.

---

### 5. Thumbnail Best Practices

Thumbnails should look like evidence, not advertising. At a glance, a viewer should be able to tell the video shows a real screen.

#### Thumbnail Style

- **Background:** Obsidian
- **Main image:** A real, cropped screenshot, usually the Library folder, an open Markdown file, or the provider selection screen
- **Text:** Two to four words in Paper, Inter Semibold, large enough to read on a phone
- **File names and paths:** Steel Blue mono, such as `chatgpt\pricing-research.md`
- **Provider names:** Written as text, never shown as logos
- **Size:** 1280 × 720 pixels, under 2 MB

#### Thumbnail Rules

- One idea per thumbnail
- Keep the bottom-right corner clear, because the video length badge covers it
- Use the same layout across all videos so the channel looks organized
- Blur personal details in screenshots, the same as in the video
- No shocked faces, arrows, red circles, or fake urgency
- No Archive Amber, to match the website's color rules

#### Series Consistency

Give each series a small, consistent marker so viewers learn the system:

| Series          | Marker                                          |
| --------------- | ----------------------------------------------- |
| Proof Demos     | `60 SEC` in Steel Blue mono, top left           |
| Provider Guides | `GUIDE` in Steel Blue mono, top left            |
| Troubleshooting | `FIX` in Steel Blue mono, top left              |
| Product Updates | `UPDATE · [MONTH]` in Steel Blue mono, top left |

#### Thumbnail Text Examples

| Video            | Thumbnail Text          |
| ---------------- | ----------------------- |
| ChatGPT guide    | **ChatGPT → Files**     |
| Claude guide     | **Claude → Files**      |
| Library folder   | **Where Your Chats Go** |
| Markdown vs JSON | **.md or .json?**       |
| Gemini guide     | **Gemini via Takeout**  |
| Backup video     | **Back Up Your Chats**  |
| Free vs Pro      | **Free or Pro?**        |

Test every thumbnail at phone size before uploading. If the text isn't readable at a glance, cut words.

---

### 6. Title Best Practices

Titles should match what people actually type into search. Clear beats clever every time.

#### Title Formula

**\[Action] + \[Provider or Topic] + \[Outcome]**

- How to Save ChatGPT Conversations to Your PC
- Download Claude Chats as Markdown Files
- Save Perplexity Threads Locally on Windows
- Save Gemini Conversations with Google Takeout

#### Title Rules

- **Lead with the search phrase.** Put the main words in the first 40 characters.
- **Keep it under about 60 characters** so it doesn't get cut off.
- **Use provider names exactly** as people search for them.
- **Add "Windows" or "PC"** when it helps clarity, since the app is Windows-only.
- **Match the thumbnail, don't repeat it.** The title and thumbnail should work together, not say the same words twice.
- **Never promise what the video doesn't show.**

#### Titles by Series

| Series          | Example Title                                           |
| --------------- | ------------------------------------------------------- |
| Proof Demo      | TotalRecalls in 60 Seconds: One Real ChatGPT Download   |
| Provider Guide  | How to Save Claude Conversations to Your PC             |
| Workflow        | Search All Your Saved AI Chats with Windows Search      |
| Explainer       | Markdown vs JSON: Which Saved Chat File Should You Use? |
| Troubleshooting | Fix: TotalRecalls Sign-In Window Won't Load             |
| Update          | What's New in TotalRecalls: \[Month Year]               |

#### Titles to Avoid

- "This App Changed How I Use AI Forever"
- "STOP Losing Your ChatGPT Chats!!"
- "The Secret Tool Nobody Talks About"

These might earn clicks, but they don't match the product's voice. They also attract viewers who leave fast, which hurts how YouTube ranks the video.

---

### 7. Upload Cadence

Consistency matters more than volume. A small team can't sustain daily uploads, and it doesn't need to.

#### Recommended Cadence

| Phase       | Timing              | Cadence                                        |
| ----------- | ------------------- | ---------------------------------------------- |
| **Launch**  | Before going public | Publish 6 core videos together                 |
| **Build**   | Months 1–3          | One long video per week, plus 1–2 Shorts       |
| **Steady**  | Month 4 onward      | Two long videos per month, Shorts as available |
| **Ongoing** | Always              | Re-record guides when interfaces change        |

#### Launch Set

Publish these six together so the channel is useful on day one:

1. TotalRecalls in 60 seconds (also the trailer)
2. How to save ChatGPT conversations to your PC
3. How to save Claude conversations to your PC
4. How to save Perplexity threads to your PC
5. Where TotalRecalls saves your files
6. Free vs Pro explained

A new visitor landing on any one of these should find enough to decide whether to download.

#### Batch Production

Record in batches to save time:

- Record two or three provider guides in one session, since the setup is the same
- Cut Shorts from each long video right after editing it
- Write descriptions and thumbnails for the whole batch at once
- Schedule uploads ahead, so a busy week doesn't break the rhythm

#### Maintenance

AI providers change their interfaces often. An outdated guide damages trust more than a missing one.

- Review every provider guide once a quarter
- Re-record when a provider's sign-in screen or the TotalRecalls interface changes visibly
- Re-record or update any video showing the $24 launch price when the launch price ends
- Unlist old versions instead of deleting them, so embedded links don't break
- Add a pinned comment on outdated videos pointing to the new version until it's unlisted

---

### 8. SEO and Discoverability

YouTube is a search engine. Most of this channel's long-term views will come from people searching for a fix to a specific problem.

#### Keyword Focus

Build videos around phrases people already search for:

- save ChatGPT conversations
- download Claude chats
- export Perplexity threads
- back up AI chat history
- ChatGPT conversations to Markdown
- save Gemini conversations Google Takeout
- export DeepSeek chat history
- save AI chats to PC

**How to check demand:** Type the start of a phrase into YouTube's search bar and note the suggestions. Those come from real search behavior. Look at the top results too. If they're old, poorly made, or off-topic, that's an opening.

#### Description Structure

Use the same structure for every long video:

1. **Opening sentence** that says exactly what the video shows
2. **Download link** in the first two lines, with a UTM tag
3. **Supporting links** to See It Work and the matching written guide
4. **Chapters** with timestamps starting at 0:00
5. **About TotalRecalls** boilerplate, identical across videos
6. **Disclaimer:** "Real screen recording. Personal details are blurred. Loading time is trimmed."
7. **Platform note:** "Windows 10 and 11."

YouTube shows only about the first 150 characters before the "Show more" fold, so the opening sentence and download link must come first.

#### Discoverability Checklist

- **Chapters:** Add timestamps on every video over two minutes. Start at 0:00, use at least three chapters, and keep each at least 10 seconds long.
- **Captions:** Upload an accurate caption file. It improves accessibility and gives YouTube more text to understand the video.
- **Spoken keywords:** Say the main phrase naturally in the first 15 seconds. For example: "In this video, I'll show you how to save your Claude conversations to your PC."
- **File name:** Name the video file with the target phrase before uploading, such as `save-claude-conversations-windows.mp4`.
- **Tags:** Add a few relevant tags, but don't overthink them. Titles, descriptions, and captions matter far more.
- **Playlists:** Add every video to at least one playlist.
- **Cards:** Link to related videos at the moment they become relevant, such as linking the Library folder video when files appear on screen.
- **End screens:** Point to the next logical video and the subscribe button. Keep it to two elements.
- **Language settings:** Set the video and

---

## 4. YouTube Channel Style & Spec

## TotalRecalls YouTube Channel Style

**Version 1.0 · Visual Identity: Private Archive + Calm Utility**

This guide shows how the TotalRecalls look carries over to YouTube: the banner, channel icon, thumbnails, playlist covers, watermark, end screens, and the overall feel of the channel page. Every spec works with free or low-cost tools, so one person can build, update, and keep the system consistent.

The goal is simple. Someone scrolling past a TotalRecalls thumbnail, or landing on the channel page, should sense **order, privacy, and permanence** before they read a word.

---

### 1. Channel Aesthetic at a Glance

#### The Feeling

> **A calm, well-kept archive for important AI work.**

Viewers should feel they've found a quiet, competent corner of YouTube. It shouldn't feel like another loud AI hype channel.

#### Aesthetic Pillars

| Pillar            | What It Looks Like on YouTube                                                    |
| ----------------- | -------------------------------------------------------------------------------- |
| **Dark and warm** | Obsidian and Graphite backgrounds with Paper text. No pure black, no pure white. |
| **Evidence-led**  | File paths, folders, `.md` and `.json` chips, and real app footage               |
| **Restrained**    | One Archive Amber highlight per graphic. Plenty of empty space.                  |
| **Consistent**    | Same layout, same chip position, same type, every time                           |
| **Honest**        | Visuals match the real product: Windows only, accurate tiers, labeled pricing    |

#### Core Palette for YouTube

| Name              | Hex       | YouTube Role                                                     |
| ----------------- | --------- | ---------------------------------------------------------------- |
| **Obsidian**      | `#111315` | Banner base, thumbnail backgrounds, icon background, end screens |
| **Graphite**      | `#1A1D21` | Panels, cards, lower thirds, subtle banner bands                 |
| **Archive Amber** | `#C88A2B` | One highlight word, icon mark, key chip, CTA button graphic      |
| **Paper**         | `#F3EFE7` | Headlines, wordmark, primary text                                |

**Supporting colors (use sparingly):**

- **Slate** `#2A2F36`: borders, chip fills, dividers
- **Mist** `#D9D4CB`: secondary text
- **Steel Blue** `#7A8FA6`: file paths, metadata chips, diagram lines
- **Local Green** `#5E8A68`: "saved" or "complete" states only

#### What the Channel Should Never Look Like

- Neon outlines, glows, scanlines, or glitch effects
- Cyberpunk, gamer, or "hacker" styling
- Red arrows, circled objects, shocked faces, or emoji-heavy thumbnails
- Glowing brains, sparkles, robots, or other AI clichés
- Official provider logos, brand colors, or sharp interface screenshots
- Rainbow or purple "AI" gradients

---

### 2. Channel Banner

#### 2.1 Specs

| Item                    | Spec                                                        |
| ----------------------- | ----------------------------------------------------------- |
| **Upload size**         | 2560 × 1440px                                               |
| **Minimum upload size** | 2048 × 1152px                                               |
| **File size**           | 6MB or smaller                                              |
| **Format**              | PNG preferred for crisp text; JPG at high quality works too |
| **Color profile**       | sRGB                                                        |

#### 2.2 Display Zones

YouTube crops the banner differently on each device. Design for the smallest zone first.

| Zone                        | Size          | What Shows There                                   |
| --------------------------- | ------------- | -------------------------------------------------- |
| **TV (full image)**         | 2560 × 1440px | Everything, including the top and bottom bands     |
| **Desktop (max width)**     | 2560 × 423px  | The full-width horizontal strip through the center |
| **Tablet**                  | 1855 × 423px  | A narrower center strip                            |
| **Text and logo safe area** | 1546 × 423px  | The center strip visible on every device           |

**Rule:** All text, the wordmark, and any meaningful graphic must sit inside the **1546 × 423px safe area**, centered in the canvas. Everything outside it is background texture only.

#### 2.3 Layout

```
┌──────────────────────────────────────────────────────────────┐
│                  Obsidian (TV-only area)                     │
│              Faint folder grid texture, 4–6% opacity         │
│                                                              │
│        ┌────────────── SAFE AREA 1546 × 423 ─────────────┐   │
│  Graph │  [Wordmark]                                     │   │
│  -ite  │  Your AI chats. Your PC.                        │   │
│  band  │  Save ChatGPT, Claude, and 6 more AI tools      │   │
│        │  as local files.                                │   │
│        │  C:\TotalRecalls\Library\     ● SAVED LOCALLY   │   │
│        └─────────────────────────────────────────────────┘   │
│                                                              │
│                  Obsidian (TV-only area)                     │
└──────────────────────────────────────────────────────────────┘
```

**Background:**

- Obsidian `#111315` fills the full canvas.
- A Graphite `#1A1D21` horizontal band, 423px tall, runs through the vertical center. It gives the desktop view quiet depth.
- Optional texture: a very faint grid of folder or file-line icons in Slate, 4–6% opacity, placed **outside** the safe area only. It should read as "archive shelving," not as a pattern you notice.

**Left side of the safe area (text block, left-aligned):**

- **Wordmark:** TotalRecalls in Paper, around 56–64px tall
- **Headline:** Inter Bold, Paper, around 88–100px
- **Subline:** Inter Regular, Mist, around 36–40px
- **Evidence line:** IBM Plex Mono, Steel Blue, around 28–32px

**Right side of the safe area (optional proof visual):**

- A cropped, simplified product visual: a folder with file rows showing `.md` and `.json` chips, or a real TotalRecalls screenshot on a Graphite card with a 1px Slate border.
- Keep it to about 35% of the safe area's width so the text stays dominant.

#### 2.4 Banner Copy Options

Pick one headline and keep it for at least three months. Changing the banner often weakens recognition.

| Option              | Headline                       | Subline                                                   | Evidence Line              |
| ------------------- | ------------------------------ | --------------------------------------------------------- | -------------------------- |
| **A (recommended)** | Your AI chats. Your PC.        | Save ChatGPT, Claude, and 6 more AI tools as local files. | `C:\TotalRecalls\Library\` |
| **B**               | Keep the AI work that matters. | A local, searchable library for your AI conversations.    | `.MD · .JSON · OFFLINE`    |
| **C**               | One folder. Every AI chat.     | 8 AI tools, saved to your own Windows PC.                 | `8 PROVIDERS → 1 LIBRARY`  |

**Amber use:** Highlight a single word at most, such as "**Your PC.**" in Archive Amber. Alternatively, keep all text in Paper and use Amber only for one small chip.

#### 2.5 What to Leave Off the Banner

- **Prices.** The $24 launch price will change. Put pricing in video end screens, descriptions, and pinned comments, where it's easy to update.
- **Upload schedule**, unless you're sure you can keep it.
- **Provider logos.** Name providers in text only.
- **The URL.** YouTube shows your channel links in the header, so a URL on the banner is redundant and gets cropped on mobile.
- **Arrows pointing to the Subscribe button.** They clash with the calm tone.

#### 2.6 Header Links and Details

Set these in YouTube Studio under **Customization → Basic info**:

- **Primary link:** totalrecalls.app, labeled "Try TotalRecalls free"
- **Secondary link (optional):** Download or FAQ page
- **Channel description, first line:** Put the promise up front, since it shows in the header preview. For example: "TotalRecalls saves your AI chats to your own Windows PC as searchable Markdown and JSON files."

---

### 3. Channel Icon (Profile Picture)

#### 3.1 Specs

| Item            | Spec                                                                                                  |
| --------------- | ----------------------------------------------------------------------------------------------------- |
| **Upload size** | 800 × 800px                                                                                           |
| **Display**     | Cropped to a circle, shown as small as about 98 × 98px, and far smaller beside comments and in search |
| **File size**   | 4MB or smaller                                                                                        |
| **Format**      | PNG                                                                                                   |

#### 3.2 Design

The icon has to work at thumbnail-in-a-comment size. That means one shape, high contrast, and no text beyond one or two letters.

**Recommended build:**

- **Background:** Solid Obsidian `#111315`, filling the full square
- **Mark:** The TotalRecalls symbol simplified to a single line-style folder, built on the brand's icon style (rounded joins, even stroke), in Archive Amber `#C88A2B`
- **Size:** The mark fills about 50–55% of the circle's diameter, centered
- **Stroke weight:** Thicken the stroke well beyond the 1.5px UI spec. At 800px, use around 40–48px so the shape survives tiny sizes.

**Alternative:** A "TR" monogram in Inter Bold, Paper, with a small Amber folder tab above the letters. Use this only if the folder mark doesn't read clearly when tested small.

#### 3.3 Icon Rules

- **Keep a clear circle margin.** Nothing important within 80px of the square's edges, because the circular crop removes the corners.
- **No full wordmark.** "TotalRecalls" becomes unreadable in a circle this small.
- **No founder photo as the channel icon.** The channel represents the product. The founder appears in videos and on the Founder Notes playlist.
- **Match the app.** If the app's Windows icon uses a different mark, align them. Viewers should recognize the same symbol on YouTube, the website, and their taskbar.

#### 3.4 Test Before You Upload

1. Export the icon at 800 × 800px.
2. Shrink a copy to 48px and 24px.
3. Place both on a dark background and a light background, since viewers use both YouTube themes.
4. If the folder shape turns into a blob at 24px, thicken the stroke or simplify the shape.

---

### 4. Thumbnail Design System

#### 4.1 Specs

| Item              | Spec                                                                               |
| ----------------- | ---------------------------------------------------------------------------------- |
| **Size**          | 1280 × 720px (16:9)                                                                |
| **File size**     | Under 2MB                                                                          |
| **Format**        | JPG or PNG                                                                         |
| **Safe margin**   | 40px on all sides                                                                  |
| **Reserved area** | Bottom-right corner, about 200 × 90px, where YouTube places the video length stamp |

#### 4.2 The Master Grid

Every thumbnail uses the same underlying grid, so the channel page looks like a tidy, indexed shelf.

```
┌────────────────────────────────────────────────┐
│ [SERIES CHIP]                                  │  ← top-left, 40px in
│                                                │
│  HEADLINE                     [FOCAL ELEMENT]  │
│  3–5 WORDS                    face, folder,    │
│  one amber word               or app screen    │
│                                                │
│ [FILE PATH / EVIDENCE CHIP]        [KEEP CLEAR]│  ← bottom-left / bottom-right
└────────────────────────────────────────────────┘
```

| Element             | Position                       | Spec                                                                                                                  |
| ------------------- | ------------------------------ | --------------------------------------------------------------------------------------------------------------------- |
| **Series chip**     | Top-left, 40px from edges      | IBM Plex Mono Medium, 32–36px, uppercase, Steel Blue text on Slate, 6px radius (scaled up to about 12px at this size) |
| **Headline**        | Left half, vertically centered | Inter Bold, 120–160px, Paper, tight line height (1.0–1.05), 2 lines maximum                                           |
| **Amber word**      | Inside the headline            | One word only, in Archive Amber                                                                                       |
| **Focal element**   | Right 45% of the frame         | One subject only                                                                                                      |
| **Evidence chip**   | Bottom-left, 40px from edges   | IBM Plex Mono, 32–40px, Steel Blue, such as `C:\TotalRecalls\Library\` or `.MD · .JSON`                               |
| **Keep-clear zone** | Bottom-right                   | No text, chips, or faces                                                                                              |

#### 4.3 Typography in Thumbnails

**The rule still applies: sans for meaning, mono for evidence.**

- **Inter Bold** carries the headline. Always uppercase or strong sentence case, chosen once and used on every thumbnail. Uppercase is recommended for readability at small sizes.
- **IBM Plex Mono** carries proof: file paths, file types, series numbers, and counts.
- **Word count:** 3–5 words in the headline. If it needs more, the idea isn't sharp enough yet.
- **Don't repeat the title.** The thumbnail headline should add to the video title, not copy it. If the title is "How to Save Your ChatGPT Chats as Local Files," the thumbnail might read "YOUR CHATS. **LOCAL.**"
- **No outlines, drop shadows, or gradient text.** Contrast comes from Paper on Obsidian, which is already very strong.

#### 4.4 Backgrounds

- **Default:** Solid Obsidian `#111315`
- **With a card:** Obsidian background with a Graphite `#1A1D21` panel behind the focal element, 1px Slate border
- **Texture (optional):** A faint folder grid in Slate at 4–6% opacity. Use the same texture on the banner so the channel feels connected.
- **Problem-focused videos:** You may add a subtle cool Steel Blue tint to the focal element, matching the "problem" grade used in videos. Keep the background Obsidian.
- **Never:** Busy photos, bright colors, blurred screenshots of provider interfaces, or gradients

#### 4.5 Recurring Motifs

These small details make thumbnails recognizably TotalRecalls:

| Motif               | How to Use It                                                                   |
| ------------------- | ------------------------------------------------------------------------------- |
| **File path**       | `C:\TotalRecalls\Library\chatgpt\` in mono, Steel Blue, as the evidence chip    |
| **File-type chips** | `.MD` and `.JSON` side by side                                                  |
| **Saved chip**      | `● SAVED LOCALLY` in Local Green, only when the video shows a completed save    |
| **Folder shape**    | The same line-style folder from the channel icon, used large as a focal element |
| **Series number**   | `EP 06 / 10` or `GUIDE · CLAUDE` in the top-left chip                           |

Use **one or two motifs per thumbnail**, not all of them.

#### 4.6 Thumbnail Templates

Build these four templates once, then duplicate them for every video.

##### Template 1: Founder

**Best for:** Founder story videos, opinion pieces, Shorts series openers

- Founder photo on the right, from mid-chest up, looking at the camera or toward the headline
- Calm, confident expression. A small half-smile or raised eyebrow fits the dry tone. No shocked faces.
- Background removed, with the founder placed on Obsidian and lit neutrally
- Headline on the left, evidence chip bottom-left

**Example:**

- Chip: `FOUNDER NOTES`
- Headline: "WHY I BUILT **THIS**"
- Evidence: `C:\TotalRecalls\`

##### Template 2: Product Proof

**Best for:** Tutorials, provider guides, feature walkthroughs

- A real TotalRecalls screenshot or File Explorer view on a Graphite card, on the right
- Crop tightly to one readable detail, such as a folder filling with `.md` files
- Slight 8–12px corner radius and 1px Slate border on the screenshot
- Blur any account names or personal details

**Example:**

- Chip: `GUIDE · CHATGPT`
- Headline: "SAVE EVERY **CHAT**"
- Evidence: `.MD · .JSON`

##### Template 3: Concept

**Best for:** Local-first explainers, privacy, ownership, "why it matters" videos

- One large line-style icon on the right: folder, lock, desktop monitor, or provider nodes merging into one point
- Icon in Paper or Mist, with one part in Archive Amber (for example, the folder tab)
- No photo, no screenshot

**Example:**

- Chip: `WHY LOCAL-FIRST`
- Headline: "WHO OWNS YOUR **CHATS**?"
- Evidence: `NO CLOUD · NO ACCOUNT`

##### Template 4: Before and After

**Best for:** Comparison videos and export-problem explainers

- Split the right side into two stacked or side-by-side panels
- Left or top panel: abstract "messy" graphic, such as a wall of bracketed raw text in Steel Blue, slightly desaturated
- Right or bottom panel: a clean Markdown file or organized folder
- Thin 1px Slate divider between them. No red X, no green check overlay.

**Example:**

- Chip: `EXPORTS, EXPLAINED`
- Headline: "RAW ZIP VS **READABLE**"
- Evidence: `.JSON → .MD`

#### 4.7 Series Consistency

For the 10-video series, add a consistent episode marker:

- Chip text: `EP 01 / 10` through `EP 10 / 10`
- Same position, size, and color on every episode
- The chip is the only thing that changes position-wise. Headline and focal element change by topic.

When all 10 appear in a row on the channel page, they should look like labeled files in the same drawer.

#### 4.8 Shorts Cover Frames

Shorts use a vertical cover frame, not a standard 1280 × 720 thumbnail, and YouTube's options for custom Short covers vary by upload method. Plan for it in the edit:

- **Pick a designed cover frame.** Choose a clean frame from the video in the YouTube app when uploading, or place a still title card in the first half-second of the edit so it's available to select.
- **Canvas:** 1080 × 1920px
- **Text zone:** Keep the headline in the vertical center of the frame. Shorts shelves often crop to a near-square or 4:5 view, so text near the top or bottom may disappear.
- **Style:** Same rules as thumbnails. Obsidian background or founder shot, Inter Bold headline, one Amber word, one mono chip.
- **Loop-friendly scripts:** If a Short opens on a founder pose, pick a cover frame from a different moment so the cover doesn't spoil the hook.

#### 4.9 Thumbnail Checklist

Before uploading, confirm every item:

- [ ] 1280 × 720px, under 2MB
- [ ] 3–5 headline words, Inter Bold
- [ ] One Amber word maximum
- [ ] One focal element
- [ ] One or two mono evidence details
- [ ] Bottom-right corner clear for the length stamp
- [ ] No provider logos or sharp provider interfaces
- [ ] No personal details visible in screenshots
- [ ] Readable at mobile size (see Section 9.3)
- [ ] Matches the template used for this video type

---

### 5. Playlist and Section Cover Art

#### 5.1 How YouTube Handles This

YouTube's channel page is organized into **sections**, and most sections display a **playlist**. Sections themselves don't take uploaded artwork. The playlist shows the thumbnail of a video inside it, and where YouTube Studio allows it, you can choose which video's thumbnail represents the playlist.

The practical approach: **make each playlist's first or featured video carry a strong series-branded thumbnail**, so the playlist cover looks designed on the channel page.

#### 5.2 Suggested Playlists and Their Visual Codes

Each playlist gets a fixed chip label and one recurring focal motif. Colors stay within the brand palette. Distinction comes from the label and motif, not from new colors.

| Playlist                 | Chip Label           | Recurring Motif                               | Purpose                                                 |
| ------------------------ | -------------------- | --------------------------------------------- | ------------------------------------------------------- |
| **Start Here**           | `START HERE`         | App screenshot, Download step                 | New viewers: what TotalRecalls does and how to try it   |
| **Provider Guides**      | `GUIDE · [PROVIDER]` | Folder labeled with the provider name in mono | One video per AI tool                                   |
| **Why Local-First**      | `WHY LOCAL-FIRST`    | Line icon: desktop monitor or lock            | Ownership, privacy, and portability explainers          |
| **Your Library at Work** | `LIBRARY`            | Markdown file open, or search result          | Using saved chats for research, reuse, and organization |
| **Founder Notes**        | `FOUNDER NOTES`      | Founder photo                                 | Build story, updates, honest lessons                    |
| **Shorts**               | `SHORT`              | Founder pose or single bold line              | Quick hooks and demos                                   |

#### 5.3 Playlist Cover Card Design

If you create a dedicated cover for a playlist (for example, a short channel trailer or intro video that sits first in the list), use this layout:

- **Background:** Obsidian with a Graphite panel filling the right 45%
- **Top-left chip:** Playlist label in mono, Steel Blue on Slate
- **Headline:** The playlist name in Inter Bold, Paper, 130–150px
- **Evidence line:** A short mono detail, such as `8 PROVIDERS · 1 LIBRARY` or `EP 01–10`
- **Right panel:** The playlist's recurring motif, large and centered

#### 5.4 Section Order on the Channel Page

Arrange sections under **Customization → Layout** in this order:

1. **Channel trailer** (for non-subscribers): the clearest, shortest product explanation you have
2. **Featured video** (for returning subscribers): the newest main upload
3. **Start Here** playlist
4. **Provider Guides** playlist
5. **Why Local-First** playlist
6. **Shorts**
7. **Your Library at Work** playlist
8. **Founder Notes** playlist

This order moves visitors from "What is this?" to "Does it work with my AI tool?" to "Why should I trust it?"

---

### 6. Watermark and Logo Placement

#### 6.1 YouTube Branding Watermark

YouTube lets you add a watermark that appears on every video. Viewers on desktop can click it to subscribe.

| Item            | Spec                                                        |
| --------------- | ----------------------------------------------------------- |
| **Upload size** | 150 × 150px minimum; square                                 |
| **File size**   | Under 1MB                                                   |
| **Format**      | PNG with transparency                                       |
| **Placement**   | Fixed by YouTube, bottom-right of the player                |
| **Setup**       | YouTube Studio → Customization → Branding → Video watermark |

**Design:**

- Use the channel icon mark: the Amber line-folder on an Obsidian circle
- Keep the Obsidian circle solid, not transparent, so the mark stays readable over bright screen recordings
- Don't use the full wordmark. It's too small to read.

**Display timing:** Choose **"Entire video"** for tutorials and guides, where viewers are most likely to want more. If it distracts during screen recordings, switch to **"Custom start time"** and begin it after the first 30 seconds, once the hook has landed.

#### 6.2 In-Video Logo Use

Because YouTube's watermark already sits in the bottom-right, avoid adding a second burned-in logo.

| Moment               | Logo Treatment                                                                                                              |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| **Opening seconds**  | No logo. Start cold on the first spoken word or the first action.                                                           |
| **During the video** | No burned-in logo. Let the watermark do the work.                                                                           |
| **Lower thirds**     | Founder name in Inter Semibold, role in IBM Plex Mono. No logo needed.                                                      |
| **End screen**       | Wordmark in Paper, small, centered or top-left of the end card                                                              |
| **Shorts**           | No watermark appears on Shorts. Place a small wordmark on the final CTA frame only, clear of the right-side action buttons. |

#### 6.3 End Screen Template

End screens run for the final 5–20 seconds of a long-form video. Build one 1920 × 1080px template and reuse it.

```
┌──────────────────────────────────────────────────────┐
│ TotalRecalls (wordmark, small)                        │
│                                                      │
│   ┌──────────────┐        ┌──────────────┐           │
│   │  NEXT VIDEO  │        │  PLAYLIST    │  (●)      │
│   │  (element)   │        │  (element)   │ Subscribe │
│   └──────────────┘        └──────────────┘           │
│                                                      │
│   [ Try it free ]  Windows app — visit from desktop  │
│   totalrecalls.app                                   │
└──────────────────────────────────────────────────────┘
```

- **Background:** Obsidian, with faint folder-grid texture if you use it elsewhere
- **Video and playlist elements:** Two placeholders, framed with 1px Sl

---

## 5. YouTube Description Templates

## YouTube Description Templates for the TotalRecalls Channel

A good YouTube description does two jobs. It tells viewers exactly what the video shows, and it gives them one clear next step. These templates handle both, so every upload sounds the same, links to the right page, and repeats the same accurate claims as the website.

There's one template for each video series on the channel:

- Proof Demos
- Provider Guides
- Workflow and File Videos
- Explainers
- Troubleshooting
- Product Updates

Each template uses the same structure. Only the opening line, the chapters, and a few series-specific lines change.

---

### How to Use These Templates

Copy the template for your video type. Then replace every bracketed note with real content. Delete the brackets and the guidance text before you publish.

A few things to know before you start:

- **The first two lines matter most.** YouTube shows roughly the first 150 characters above the "Show more" fold, and search results often show even less. The opening sentence and the download link belong there.
- **YouTube descriptions don't support bold or headings.** The templates use plain text and capital-letter labels so they look the same in the video page and in search.
- **Chapters need three things to work.** The first timestamp must be 0:00, there must be at least three chapters, and each chapter must last at least 10 seconds.
- **Every link gets a UTM tag.** This shows which videos send people to the website and which ones lead to downloads.

---

### Shared Building Blocks

These parts appear in every template. Keep them identical across the channel unless the website wording changes.

#### UTM Tag Format

Use this pattern for every link in every description:

```
?utm_source=youtube&utm_medium=video&utm_campaign=[series]-[topic]
```

**Series codes:**

| Series                   | Code        |
| ------------------------ | ----------- |
| Proof Demos              | `proof`     |
| Provider Guides          | `guide`     |
| Workflow and File Videos | `workflow`  |
| Explainers               | `explainer` |
| Troubleshooting          | `fix`       |
| Product Updates          | `update`    |

**Topic codes** use lowercase words joined with hyphens, such as `chatgpt`, `library-folder`, or `markdown-vs-json`.

**Example:**

```
totalrecalls.app/?utm_source=youtube&utm_medium=video&utm_campaign=guide-claude
```

#### About TotalRecalls Boilerplate

```
ABOUT TOTALRECALLS
TotalRecalls is a Windows app that saves your AI conversations to your PC as Markdown and JSON files. You sign in to each provider inside the app, on your own computer. Your conversations aren't sent to our servers, and there's no TotalRecalls account to create.

The Free Tier covers ChatGPT, Claude, and Perplexity. Pro adds Gemini (through Google Takeout), Grok, DeepSeek, Mistral, and Qwen, with unlimited downloads.
```

#### Disclaimer Line

```
Real screen recording. Personal details are blurred. Loading time is trimmed.
```

\[If no loading time was cut, remove "Loading time is trimmed." If other waits were cut, such as email delivery, say so plainly: "Email delivery time is trimmed." Never let the video suggest faster speeds than users will see.]

#### Platform Note

```
Windows 10 and 11.
```

\[Don't add macOS or Linux release dates. If you mention them at all, describe them as "in development."]

---

### Template 1: Proof Demos

Use this for short, literal recordings of one download from start to finish. These videos are 45–90 seconds and end with files open on screen.

```
[Opening sentence: Say exactly what the video shows, in one plain sentence. Name the provider and the result. Example: "One real ChatGPT download with TotalRecalls, from opening the app to opening the saved Markdown and JSON files."]

Download TotalRecalls free: totalrecalls.app/?utm_source=youtube&utm_medium=video&utm_campaign=proof-[provider]
[For Pro-only providers (Gemini, Grok, DeepSeek, Mistral, Qwen), keep the free download link first. Add one line below it: "This provider is included in Pro." Don't push the upgrade harder than that.]

See it work: [See It Work page URL]?utm_source=youtube&utm_medium=video&utm_campaign=proof-[provider]
Full written guide: [Matching Guides page URL for this provider]?utm_source=youtube&utm_medium=video&utm_campaign=proof-[provider]

CHAPTERS
0:00 Open the app
[0:00] Choose [provider]
[0:00] Sign in
[0:00] Pick a conversation
[0:00] Download
[0:00] Open your files
[Match each timestamp to the final cut. Use the same step names as the on-screen captions. For the ChatGPT demo, the timestamps should match the See It Work page exactly.]

ABOUT TOTALRECALLS
TotalRecalls is a Windows app that saves your AI conversations to your PC as Markdown and JSON files. You sign in to each provider inside the app, on your own computer. Your conversations aren't sent to our servers, and there's no TotalRecalls account to create.

The Free Tier covers ChatGPT, Claude, and Perplexity. Pro adds Gemini (through Google Takeout), Grok, DeepSeek, Mistral, and Qwen, with unlimited downloads.

Real screen recording. Personal details are blurred. Loading time is trimmed.

Windows 10 and 11.
```

---

### Template 2: Provider Guides

Use this for full walkthroughs of one provider, usually 3–6 minutes. These videos target people searching for a specific fix, so the opening line should use the words they type.

```
[Opening sentence: Start with the search phrase, then the outcome. Example: "How to save your Claude conversations to your PC as Markdown and JSON files, step by step, using TotalRecalls on Windows."]

[Optional second sentence: Add one detail that sets expectations. Example: "This guide covers signing in, choosing conversations, downloading, and finding your files."]

Download TotalRecalls free: totalrecalls.app/?utm_source=youtube&utm_medium=video&utm_campaign=guide-[provider]
[For Pro providers, add: "This provider is included in Pro. Compare Free and Pro: totalrecalls.app/pricing/?utm_source=youtube&utm_medium=video&utm_campaign=guide-[provider]"]

See it work: [See It Work page URL]?utm_source=youtube&utm_medium=video&utm_campaign=guide-[provider]
Full written guide with screenshots: [Matching Guides page URL]?utm_source=youtube&utm_medium=video&utm_campaign=guide-[provider]

CHAPTERS
0:00 What this guide covers
[0:00] Open TotalRecalls and choose [provider]
[0:00] Sign in to [provider] inside the app
[0:00] Choose the conversations to save
[0:00] Download
[0:00] Where your files are saved
[0:00] Common problems and fixes
[Rename or add chapters to match the video. Keep names short and literal.]

[GEMINI ONLY: Replace the sign-in and choose chapters with Takeout steps, such as "Request your Google Takeout file," "Download the Takeout file," and "Import it into TotalRecalls." Add this line above CHAPTERS: "Gemini conversations come in through a Google Takeout file. This isn't a one-click download, and this guide shows each step." Never imply Gemini works like the other providers.]

ABOUT TOTALRECALLS
TotalRecalls is a Windows app that saves your AI conversations to your PC as Markdown and JSON files. You sign in to each provider inside the app, on your own computer. Your conversations aren't sent to our servers, and there's no TotalRecalls account to create.

The Free Tier covers ChatGPT, Claude, and Perplexity. Pro adds Gemini (through Google Takeout), Grok, DeepSeek, Mistral, and Qwen, with unlimited downloads.

Real screen recording. Personal details are blurred. Loading time is trimmed.

Windows 10 and 11.

[Recorded with TotalRecalls version [X.X] on [Month Year]. Add this line so viewers can tell whether the guide is current. Update it when you re-record.]
```

---

### Template 3: Workflow and File Videos

Use this for videos about what people can do with their saved files, such as organizing, searching, backing up, or opening chats in other apps.

```
[Opening sentence: Describe the task and the result. Example: "How to search across all your saved AI conversations using Windows search, so you can find any chat in seconds."]

[Optional second sentence: Name the tools shown, plainly. Example: "This video uses File Explorer and Notepad. Both come with Windows." If you show a third-party app, such as VS Code or a note-taking app, name it as text only. Don't imply any partnership or endorsement.]

Download TotalRecalls free: totalrecalls.app/?utm_source=youtube&utm_medium=video&utm_campaign=workflow-[topic]

See it work: [See It Work page URL]?utm_source=youtube&utm_medium=video&utm_campaign=workflow-[topic]
Full written guide: [Matching Guides page URL]?utm_source=youtube&utm_medium=video&utm_campaign=workflow-[topic]
[If no written guide exists for this topic yet, link to the main Guides page instead.]

CHAPTERS
0:00 [What you'll do in this video]
[0:00] [First step, such as "Open your Library folder"]
[0:00] [Second step, such as "Search by keyword"]
[0:00] [Third step, such as "Filter by date"]
[0:00] [Result, such as "Open the chat you found"]
[Use action verbs. Each chapter should describe one thing the viewer does.]

ABOUT TOTALRECALLS
TotalRecalls is a Windows app that saves your AI conversations to your PC as Markdown and JSON files. You sign in to each provider inside the app, on your own computer. Your conversations aren't sent to our servers, and there's no TotalRecalls account to create.

The Free Tier covers ChatGPT, Claude, and Perplexity. Pro adds Gemini (through Google Takeout), Grok, DeepSeek, Mistral, and Qwen, with unlimited downloads.

Real screen recording. Personal details are blurred. Loading time is trimmed.

Windows 10 and 11.
```

---

### Template 4: Explainers

Use this for short videos that explain the "why" behind the product, such as Markdown vs JSON, Free vs Pro, or what "local" means. These may mix screen recording with a spoken explanation.

```
[Opening sentence: State the question the video answers, then the short answer. Example: "Markdown or JSON? TotalRecalls saves every conversation in both formats, and this video explains what each one is good for."]

Download TotalRecalls free: totalrecalls.app/?utm_source=youtube&utm_medium=video&utm_campaign=explainer-[topic]
[FREE VS PRO ONLY: Add this line below the download link: "Compare Free and Pro: totalrecalls.app/pricing/?utm_source=youtube&utm_medium=video&utm_campaign=explainer-free-vs-pro". If the price is mentioned, write "Pro is $24 one-time (launch price)." Always keep "launch price" beside $24. Don't add discounts or end dates unless they're published and real.]

See it work: [See It Work page URL]?utm_source=youtube&utm_medium=video&utm_campaign=explainer-[topic]
Read more: [Matching Guides page URL]?utm_source=youtube&utm_medium=video&utm_campaign=explainer-[topic]

CHAPTERS
0:00 [The question]
[0:00] [First point]
[0:00] [Second point]
[0:00] [Example on screen]
[0:00] [Short answer and recap]

[PRIVACY EXPLAINER ONLY: Add this line above CHAPTERS: "Downloads connect directly from your PC to each AI provider. Your conversations aren't sent to our servers." Never describe the app as "fully offline" or say it "never touches the internet."]

ABOUT TOTALRECALLS
TotalRecalls is a Windows app that saves your AI conversations to your PC as Markdown and JSON files. You sign in to each provider inside the app, on your own computer. Your conversations aren't sent to our servers, and there's no TotalRecalls account to create.

The Free Tier covers ChatGPT, Claude, and Perplexity. Pro adds Gemini (through Google Takeout), Grok, DeepSeek, Mistral, and Qwen, with unlimited downloads.

Real screen recording. Personal details are blurred. Loading time is trimmed.
[If the explainer includes non-recorded visuals, such as a simple diagram, adjust the line: "Screen recordings are real. Personal details are blurred. Loading time is trimmed."]

Windows 10 and 11.
```

---

### Template 5: Troubleshooting

Use this for short, specific fixes based on real support questions. People find these videos when something isn't working, so get to the answer fast.

```
[Opening sentence: Name the problem in the words a user would search for, then promise the fix. Example: "If the sign-in window won't load in TotalRecalls, this short video shows how to fix it."]

PROBLEM: [Describe the symptom in one sentence. Example: "The provider's sign-in window stays blank after you choose it."]
FIX: [Summarize the fix in one or two sentences, so people can solve it without watching. Example: "Close TotalRecalls, check your internet connection, and reopen the app from its folder."]

Download TotalRecalls free: totalrecalls.app/?utm_source=youtube&utm_medium=video&utm_campaign=fix-[topic]

See it work: [See It Work page URL]?utm_source=youtube&utm_medium=video&utm_campaign=fix-[topic]
Full written guide: [Matching Guides or help page URL]?utm_source=youtube&utm_medium=video&utm_campaign=fix-[topic]

Still stuck? Contact us: [support email or contact page URL]

CHAPTERS
0:00 The problem
[0:00] Why it happens
[0:00] Step 1: [first fix step]
[0:00] Step 2: [second fix step]
[0:00] Check that it worked
[Short videos under about a minute can skip chapters if they can't meet the three-chapter, 10-second minimum.]

[LICENSE OR DEVICE VIDEOS ONLY: Use exact wording. "Pro activates on up to 3 PCs." Never say "unlimited devices." Blur the license key in the video and never include it in the description.]

ABOUT TOTALRECALLS
TotalRecalls is a Windows app that saves your AI conversations to your PC as Markdown and JSON files. You sign in to each provider inside the app, on your own computer. Your conversations aren't sent to our servers, and there's no TotalRecalls account to create.

The Free Tier covers ChatGPT, Claude, and Perplexity. Pro adds Gemini (through Google Takeout), Grok, DeepSeek, Mistral, and Qwen, with unlimited downloads.

Real screen recording. Personal details are blurred. Loading time is trimmed.

Windows 10 and 11.

[Recorded with TotalRecalls version [X.X] on [Month Year].]
```

---

### Template 6: Product Updates

Use this for brief, honest notes on what changed. These videos show the product is cared for, so keep the summary factual and specific.

```
[Opening sentence: Name the update and its main change. Example: "What's new in TotalRecalls for [Month Year]: faster Claude downloads, a clearer Library folder, and two bug fixes."]

NEW
- [New feature or provider, in one plain line]
- [Another new item, if any]

FIXED
- [Bug fix, described by what users will notice. Example: "Long Perplexity threads now save completely."]

IN PROGRESS
- [Work underway, with no dates. Example: "macOS and Linux versions are in development."]
[Never give release dates for macOS, Linux, or new providers until they're real and published. If updates come up, say "for the life of the product." Never say "forever" or "lifetime updates."]

Download TotalRecalls free: totalrecalls.app/?utm_source=youtube&utm_medium=video&utm_campaign=update-[month-year]

Get product updates by email: totalrecalls.app/?utm_source=youtube&utm_medium=video&utm_campaign=update-[month-year]#[footer signup anchor]
[Product Update videos are the right place for the email signup. Link straight to the footer form if it has an anchor. Keep this line below the download link.]

See it work: [See It Work page URL]?utm_source=youtube&utm_medium=video&utm_campaign=update-[month-year]
Full changelog: [Changelog or Guides page URL]?utm_source=youtube&utm_medium=video&utm_campaign=update-[month-year]

CHAPTERS
0:00 What's in this update
[0:00] [First new item]
[0:00] [Second new item]
[0:00] Fixes
[0:00] What we're working on

ABOUT TOTALRECALLS
TotalRecalls is a Windows app that saves your AI conversations to your PC as Markdown and JSON files. You sign in to each provider inside the app, on your own computer. Your conversations aren't sent to our servers, and there's no TotalRecalls account to create.

The Free Tier covers ChatGPT, Claude, and Perplexity. Pro adds Gemini (through Google Takeout), Grok, DeepSeek, Mistral, and Qwen, with unlimited downloads.

Real screen recording. Personal details are blurred. Loading time is trimmed.
[If the update includes on-camera segments, adjust: "Screen recordings are real. Personal details are blurred. Loading time is trimmed."]

Windows 10 and 11.
```

---

### Common Mistakes to Avoid

Small wording slips can undo the trust these videos build. Watch for these before you publish:

- **Don't** stack calls to action. Keep "Download free" first and skip extra asks to like, subscribe, and buy in the description.
- **Don't** use hype words like "secret," "insane," or "game-changing." Plain descriptions match the product.
- **Don't** paste provider logos or trademark symbols into descriptions. Write provider names as text.
- **Don't** leave bracketed guidance in a published description. Search the text for "\[" before you hit publish.
- **Do** match every chapter name to what's actually on screen.
- **Do** confirm the Free Tier limit wording ("per provider" or "per download") matches the live site before mentioning it anywhere.
- **Do** keep "launch price" beside every mention of $24.

---

### Before You Publish

Run through this short checklist on every upload:

1

---

## 6. Hook Rankings Guide

## TotalRecalls Hook Rankings Guide

This guide ranks the alternative hooks for each video in the TotalRecalls YouTube series and names the strongest pick. Every recommendation is judged against short-form best practices, so the winner is the hook most likely to stop the scroll, name the pain, and set up the rest of the video in the brand's wry, confident voice.

**A note on coverage:** Full rankings appear for **Video 6** and **Video 10**, the two hook sets available for this review. Videos 1–5 and 7–9 each have a ready-to-fill scorecard that uses the same criteria, so every video gets judged the same way.

---

### How the Hooks Are Scored

Each hook gets a score from 1 to 5 on four criteria, for a maximum of 20 points.

| Criterion            | What It Measures                                  | What a 5 Looks Like                                                           |
| -------------------- | ------------------------------------------------- | ----------------------------------------------------------------------------- |
| **Early retention**  | Does it hold viewers through the first 3 seconds? | The first words or first visual create instant curiosity or a direct call-out |
| **Pain recognition** | Does the viewer feel "that's me"?                 | Names a real, specific frustration most AI users have lived through           |
| **Setup clarity**    | Does it lead cleanly into the rest of the video?  | Scene 2 feels like the natural next beat, with no mental jump                 |
| **Brand tone fit**   | Is it wry, confident, and lightly playful?        | Dry understatement, never loud, never preachy, never a hard sell              |

#### Tie-Breakers

When two hooks score the same, pick the one that:

1. **Works for cold viewers.** Most Shorts viewers haven't seen earlier videos.
2. **Holds up to scrutiny.** Skeptical AI power users will challenge any line that stretches the truth.
3. **Needs fewer props and less rehearsal.** For a solo production, simpler shoots mean more reliable results.

---

### Video Rankings

#### 1. Video 1

**Status:** Hook set pending review

| Hook     | Retention | Pain | Clarity | Tone | Total |
| -------- | --------- | ---- | ------- | ---- | ----- |
| Option 1 |           |      |         |      | /20   |
| Option 2 |           |      |         |      | /20   |
| Option 3 |           |      |         |      | /20   |

**Winner:** \_\_\_\_\_\
**Why it wins:** \_\_\_\_\_\
**Runner-up note:** \_\_\_\_\_

---

#### 2. Video 2

**Status:** Hook set pending review

| Hook     | Retention | Pain | Clarity | Tone | Total |
| -------- | --------- | ---- | ------- | ---- | ----- |
| Option 1 |           |      |         |      | /20   |
| Option 2 |           |      |         |      | /20   |
| Option 3 |           |      |         |      | /20   |

**Winner:** \_\_\_\_\_\
**Why it wins:** \_\_\_\_\_\
**Runner-up note:** \_\_\_\_\_

---

#### 3. Video 3

**Status:** Hook set pending review

| Hook     | Retention | Pain | Clarity | Tone | Total |
| -------- | --------- | ---- | ------- | ---- | ----- |
| Option 1 |           |      |         |      | /20   |
| Option 2 |           |      |         |      | /20   |
| Option 3 |           |      |         |      | /20   |

**Winner:** \_\_\_\_\_\
**Why it wins:** \_\_\_\_\_\
**Runner-up note:** \_\_\_\_\_

---

#### 4. Video 4

**Status:** Hook set pending review

| Hook     | Retention | Pain | Clarity | Tone | Total |
| -------- | --------- | ---- | ------- | ---- | ----- |
| Option 1 |           |      |         |      | /20   |
| Option 2 |           |      |         |      | /20   |
| Option 3 |           |      |         |      | /20   |

**Winner:** \_\_\_\_\_\
**Why it wins:** \_\_\_\_\_\
**Runner-up note:** \_\_\_\_\_

---

#### 5. Video 5

**Status:** Hook set pending review

| Hook     | Retention | Pain | Clarity | Tone | Total |
| -------- | --------- | ---- | ------- | ---- | ----- |
| Option 1 |           |      |         |      | /20   |
| Option 2 |           |      |         |      | /20   |
| Option 3 |           |      |         |      | /20   |

**Winner:** \_\_\_\_\_\
**Why it wins:** \_\_\_\_\_\
**Runner-up note:** \_\_\_\_\_

---

#### 6. Video 6: "I'll Wait"

**Video role:** Awareness Short. It contrasts two painful save methods (official export and copy-paste) with the TotalRecalls way.

| Hook                | Retention | Pain | Clarity | Tone | Total  |
| ------------------- | --------- | ---- | ------- | ---- | ------ |
| **Two Bad Options** | 4         | 3    | 5       | 5    | **17** |
| The Stopwatch       | 5         | 4    | 3       | 4    | 16     |
| The Eulogy          | 3         | 5    | 3       | 3    | 14     |

**🏆 Winner: Two Bad Options**

**Why it wins:**

- **It maps perfectly onto the video.** "Two ways... both terrible... stick around for the third" sets up Scene 2 as option one, Scene 3 as option two, and Scene 4 as the payoff. No other hook fits the structure this tightly.
- **It opens a loop viewers want closed.** The half-raised third finger, cut off by a hard cut, is a clean curiosity gap. Viewers stay to see what the third way is.
- **It's the most on-brand.** Dry, matter-of-fact, and a little smug, with buzzers doing the comedy instead of the founder. The humor comes from understatement, which is exactly the series voice.
- **It needs no stretch claims.** Calling official exports and copy-paste "terrible" is an opinion the video then proves on screen.

**Watch out for:** "Stick around" can read as retention bait if delivered too eagerly. Keep it flat and throwaway, almost bored.

**Runner-up note: The Stopwatch**\
The Stopwatch has the strongest first 3 seconds of the set. A direct challenge with a live countdown turns viewers into participants. The catch is clarity. The hook is about *finding* a chat, while Scene 2 immediately pivots to *saving* chats, so the handoff feels like a jump. It's also slightly off-tone, since "calm and slightly smug" can tip into gloating. Use it as a **standalone 6-second teaser** or test it against the winner if early drop-off is your biggest problem.

**Third place: The Eulogy**\
The Eulogy hits the pain hardest, but it has two real risks. First, "lost to a closed tab" invites pushback, because most providers keep chat history after a tab closes, and skeptical viewers will say so in the comments. Second, the mock funeral takes a beat to decode, so the first 3 seconds are slower. If you use it, swap the loss line for something more defensible, such as a thread you can no longer find or a history that changed after an update.

---

#### 7. Video 7

**Status:** Hook set pending review

| Hook     | Retention | Pain | Clarity | Tone | Total |
| -------- | --------- | ---- | ------- | ---- | ----- |
| Option 1 |           |      |         |      | /20   |
| Option 2 |           |      |         |      | /20   |
| Option 3 |           |      |         |      | /20   |

**Winner:** \_\_\_\_\_\
**Why it wins:** \_\_\_\_\_\
**Runner-up note:**

---

## 7. YouTube Implementation Plan (week-by-week build & run)

> Companion to the YouTube Strategy (§3). Covers how the channel gets built and run,
> week by week, with the Week 0-1 execution checklist, the blog series plan, the
> filename convention (kebab-case, dated), and the 8-week KPI ladder.

## TotalRecalls YouTube Implementation Plan

**Status:** Companion to the TotalRecalls YouTube Strategy. The strategy explains *what* the channel does and *why*. This plan covers *how* you build and run it, week by week.\
**Status date:** October 3, 2026\
**Aligned with:** Master Implementation Plan V3, Content Audit Plan V2, and YouTube Description Templates\
**Built for:** A founder-led team that records, edits, and publishes in small batches.

The channel has one job: **show the app working, honestly, so people trust it enough to try it.** This plan turns that job into tasks, checklists, and a schedule you can follow without rereading the strategy each week.

---

### Status Legend

| Marker         | Meaning                                          |
| -------------- | ------------------------------------------------ |
| ✅ **Complete** | Written, built, or decided as a final asset      |
| ⏳ **Pending**  | Not started, or in progress but not finished     |
| 🔍 **Confirm** | A detail needs checking before work can continue |

---

### 1. How This Plan Fits

| Document                                        | Role                                                 | Use It For                                       | Status     |
| ----------------------------------------------- | ---------------------------------------------------- | ------------------------------------------------ | ---------- |
| **TotalRecalls YouTube Strategy**               | Purpose, pillars, playlists, thumbnails, titles, SEO | Deciding what to make and how it should look     | ✅ Complete |
| **YouTube Implementation Plan** (this document) | Tasks, workflows, schedule, checklists               | Running the channel each week                    | ✅ Complete |
| **YouTube Description Templates**               | Description structure, UTM naming, pinned comments   | Every upload                                     | ✅ Complete |
| **Master Implementation Plan V3**               | Cross-channel priorities and timing                  | Aligning YouTube with the site, blog, and social | ✅ Complete |
| **Blogs 3, 4, 5, and 9**                        | Written posts that double as script sources          | Scripting explainer and workflow videos          | ✅ Complete |

**Precedence rule:** If this plan and Master Implementation Plan V3 disagree on timing, V3 wins. If this plan and the YouTube Strategy disagree on style or rules, the strategy wins.

---

### 2. Finalized Decisions That Shape the Channel

These are closed. They set the boundaries for every task below.

| Decision                    | What It Means for YouTube                                                                                                           | Status     |
| --------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| **Option A approved**       | No provider spotlight videos or posts. Each provider gets one Provider Guide video and one Proof Demo.                              | ✅ Complete |
| **9-post blog series**      | Explainer and workflow videos use finished blog posts as their scripts. No video exists for a topic the blog or guides don't cover. | ✅ Complete |
| **Public evidence library** | Real screen recordings only. No brand film, no creator persona, no reaction content.                                                | ✅ Complete |
| **Trailer**                 | A 45–60 second cut of the See It Work demo                                                                                          | ✅ Complete |
| **CTA order**               | Download free first. Pro only in Pro-related videos. Email updates only in Product Update videos.                                   | ✅ Complete |
| **Archive Amber**           | Never used on YouTube. Website buttons only.                                                                                        | ✅ Complete |
| **Platforms**               | "Windows 10 and 11. macOS and Linux are in development." No dates.                                                                  | ✅ Complete |

---

### 3. Status at a Glance

| Area                             | Status     | Next Step                                        |
| -------------------------------- | ---------- | ------------------------------------------------ |
| Strategy and templates           | ✅ Complete | None                                             |
| Handle claimed                   | ⏳ Pending  | Claim @TotalRecalls in Week 0                    |
| Branding assets                  | ⏳ Pending  | Build in Weeks 1–2                               |
| Recording setup                  | ⏳ Pending  | Set up and test in Week 1                        |
| Tracking sheet                   | ⏳ Pending  | Build in Week 1                                  |
| Launch set (6 videos)            | ⏳ Pending  | Record in Weeks 1–2, publish in Week 3           |
| Pro provider videos              | ⏳ Pending  | Weeks 5–8                                        |
| Blog-paired videos               | ⏳ Pending  | Weeks 9–12, plus two after day 90                |
| Filename format and Library path | 🔍 Confirm | Needed before recording the Library folder video |
| Free Tier limit wording          | 🔍 Confirm | Needed before recording Free vs Pro              |

---

### 4. Week 0 and Phase 1 Setup Tasks

Work through these in order. Each task is small, and most take under an hour.

#### Step 1: Claim the Account and Handle (Week 0)

1. Create the channel under a Google account the business controls, not a personal inbox.
2. Turn on two-step verification for that account.
3. Claim **@TotalRecalls**. If it's taken, claim **@TotalRecallsApp**.
4. Set the channel name to **TotalRecalls**, with no tagline.
5. Claim the same handle on any social platforms you plan to use.
6. Store the login in a password manager, with a backup admin who can recover it.

| Task                                               | Owner   | Status    |
| -------------------------------------------------- | ------- | --------- |
| Business Google account with two-step verification | Founder | ⏳ Pending |
| Handle claimed                                     | Founder | ⏳ Pending |
| Matching social handles claimed                    | Founder | ⏳ Pending |

#### Step 2: Verify the Channel (Week 0)

Verify the account by phone in YouTube Studio. Verification unlocks custom thumbnails and longer uploads, and both are needed for the launch set.

| Task                        | Status    |
| --------------------------- | --------- |
| Phone verification complete | ⏳ Pending |
| Custom thumbnails enabled   | ⏳ Pending |

#### Step 3: Build Branding Assets (Weeks 1–2)

| Asset                    | Spec                                                                                                                         | Check Before Uploading                                                  | Status    |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- | --------- |
| **Profile image**        | Mark or wordmark in Paper (`#F3EFE7`) on Obsidian (`#111315`), centered with padding                                         | Readable at 40 pixels, on light and dark themes                         | ⏳ Pending |
| **Banner**               | Wordmark, "Save your AI conversations as local files.", and `MARKDOWN · JSON · WINDOWS 10/11` in Steel Blue (`#7A8FA6`) mono | All text inside the center safe area on phone, desktop, and TV previews | ⏳ Pending |
| **Thumbnail template**   | 1280 × 720, Obsidian background, series marker top left, bottom-right corner clear                                           | Text readable at phone size                                             | ⏳ Pending |
| **End card template**    | Obsidian background, "Download free at totalrecalls.app" in Paper, space for two end screen elements                         | No Amber, no provider logos                                             | ⏳ Pending |
| **Watermark** (optional) | Small Paper mark on transparent background                                                                                   | Doesn't cover on-screen app content                                     | ⏳ Pending |

**Banner exclusions:** no provider logos, no prices, no upload schedule, no Archive Amber.

#### Step 4: Write the About Section and Links (Weeks 1–2)

1. Paste the About section from the YouTube Strategy.
2. Check the provider list, Free Tier wording, and platform note against the live website. 🔍 Confirm the Free Tier limit wording first.
3. Add the four header links in this order, each with its UTM tag:

| Order | Label         | Link                                                                                               | Status    |
| ----- | ------------- | -------------------------------------------------------------------------------------------------- | --------- |
| 1     | Download free | `totalrecalls.app/?utm_source=youtube&utm_medium=channel&utm_campaign=header&utm_content=download` | ⏳ Pending |
| 2     | See It Work   | See It Work URL with `utm_content=seeitwork`                                                       | ⏳ Pending |
| 3     | Guides        | Guides URL with `utm_content=guide`                                                                | ⏳ Pending |
| 4     | Pricing       | `totalrecalls.app/pricing/` with `utm_content=pricing`                                             | ⏳ Pending |

#### Step 5: Set Upload Defaults (Weeks 1–2)

Upload defaults save time and prevent missed settings. Set them once in YouTube Studio under **Settings → Upload defaults**.

| Setting          | Value                                                             | Status    |
| ---------------- | ----------------------------------------------------------------- | --------- |
| Visibility       | Private (switch to scheduled or public after review)              | ⏳ Pending |
| Category         | Science & Technology                                              | ⏳ Pending |
| Video language   | English                                                           | ⏳ Pending |
| Caption language | English                                                           | ⏳ Pending |
| Description      | The About TotalRecalls boilerplate, disclaimer, and platform note | ⏳ Pending |
| Comments         | On, with potentially inappropriate comments held for review       | ⏳ Pending |
| Audience         | Not made for kids                                                 | ⏳ Pending |
| Paid promotion   | Not declared (the channel carries no sponsored segments)          | ⏳ Pending |

Under **Settings → Community**, add blocked words for common spam phrases. Also turn on review for comments containing links, so spam links never appear unreviewed.

#### Step 6: Set Up the Recording Environment (Week 1)

A clean, repeatable setup makes every recording look consistent and cuts blurring work later.

1. **Create a dedicated Windows user profile** for recording. Keep the desktop clean, with no personal files, notifications, or bookmarks.
2. **Use recording-only provider accounts** filled with harmless sample conversations, such as recipe ideas or report drafts. You'll still blur emails and profile images, but there'll be far less to hide.
3. **Turn on Focus mode** or Do Not Disturb so no notifications appear on screen.
4. **Set display scaling** so the app text is readable on a phone, and record at 1080p or higher.
5. **Enlarge the cursor** in Windows settings and turn on a soft click highlight in your recorder.
6. **Test the microphone** in the actual recording room. Record 30 seconds, listen back on headphones, and fix echo or hum before the first session.
7. **Note the TotalRecalls version** you're recording. Every guide description needs it. 🔍 Confirm the version for the launch batch.

| Task                                                | Status    |
| --------------------------------------------------- | --------- |
| Recording profile created                           | ⏳ Pending |
| Sample provider accounts ready (Free Tier)          | ⏳ Pending |
| Sample provider accounts ready (Pro)                | ⏳ Pending |
| Microphone and room tested                          | ⏳ Pending |
| Recorder settings saved (resolution, cursor, audio) | ⏳ Pending |

#### Step 7: Build the Tracking Sheet (Week 1)

See Section 8 for the full column list. Build it before the first recording session, so every video gets logged from the start.

**Takeaway:** Setup is a two-week job, not a two-month one. Claim the handle first, because everything else can wait a day and the handle can't.

---

### 5. The Launch Set

Publish these six videos together in Week 3, so the channel is useful on day one.

| #     | Title                                                 | Series         | Campaign                   | Length    | Thumbnail Text                   | Script Source                                     | Playlists                   | Status    |
| ----- | ----------------------------------------------------- | -------------- | -------------------------- | --------- | -------------------------------- | ------------------------------------------------- | --------------------------- | --------- |
| **1** | TotalRecalls in 60 Seconds: One Real ChatGPT Download | Proof Demo     | `demo-chatgpt`             | 45–60 sec | **One Real Download** (`60 SEC`) | See It Work demo                                  | Start Here, Quick Demos     | ⏳ Pending |
| **2** | How to Save ChatGPT Conversations to Your PC          | Provider Guide | `guide-chatgpt`            | 3–6 min   | **ChatGPT → Files** (`GUIDE`)    | ChatGPT written guide                             | Start Here, Provider Guides | ⏳ Pending |
| **3** | How to Save Claude Conversations to Your PC           | Provider Guide | `guide-claude`             | 3–6 min   | **Claude → Files** (`GUIDE`)     | Claude written guide                              | Provider Guides             | ⏳ Pending |
| **4** | How to Save Perplexity Threads to Your PC             | Provider Guide | `guide-perplexity`         | 3–6 min   | **Perplexity → Files** (`GUIDE`) | Perplexity written guide                          | Provider Guides             | ⏳ Pending |
| **5** | Where TotalRecalls Saves Your Files                   | Explainer      | `explainer-library-folder` | 2–4 min   | **Where Your Chats Go**          | Library Folder explainer (🔍 Confirm Blog 1 or 2) | Start Here                  | ⏳ Pending |
| **6** | Free vs Pro: What's Included in Each                  | Explainer      | `explainer-free-vs-pro`    | 2–4 min   | **Free or Pro?**                 | Pricing page Free vs Pro copy                     | Start Here                  | ⏳ Pending |

#### Launch Gates

No launch video goes public until these are settled:

- 🔍 **Filename format and Library path** confirmed in the released app. Videos 2–5 show both on screen.
- 🔍 **Free Tier limit wording** confirmed. Video 6 and every About block depend on it.
- ⏳ **Second-person accuracy check** done on all six, against the guardrails in Section 17.
- ⏳ **Captions** uploaded and checked for provider names.

#### Two Extra Demos in the Launch Batch

Record the **Claude** and **Perplexity** Proof Demos in the same session as the launch set. They take minutes to capture and publish in Week 4, which brings the Quick Demos playlist to three videos.

| Title                                                    | Campaign          | Publish | Status    |
| -------------------------------------------------------- | ----------------- | ------- | --------- |
| TotalRecalls in 60 Seconds: One Real Claude Download     | `demo-claude`     | Week 4  | ⏳ Pending |
| TotalRecalls in 60 Seconds: One Real Perplexity Download | `demo-perplexity` | Week 4  | ⏳ Pending |

**Takeaway:** Six videos at launch, two short demos right after. A new visitor landing on any of them has enough to decide whether to download.

---

### 6. Provider Rollout Order

Free Tier providers launch first. Pro providers follow, one or two per week, each with a guide and a Proof Demo recorded in the same session.

| Order | Provider       | Tier | Guide Campaign     | Demo Campaign     | Record    | Publish   | Special Note                                                              | Status    |
| ----- | -------------- | ---- | ------------------ | ----------------- | --------- | --------- | ------------------------------------------------------------------------- | --------- |
| 1     | **ChatGPT**    | Free | `guide-chatgpt`    | `demo-chatgpt`    | Weeks 1–2 | Week 3    | Lead video and trailer                                                    | ⏳ Pending |
| 2     | **Claude**     | Free | `guide-claude`     | `demo-claude`     | Weeks 1–2 | Weeks 3–4 | Show file examples                                                        | ⏳ Pending |
| 3     | **Perplexity** | Free | `guide-perplexity` | `demo-perplexity` | Weeks 1–2 | Weeks 3–4 | Say "threads," matching search wording                                    | ⏳ Pending |
| 4     | **Gemini**     | Pro  | `guide-gemini`     | `demo-gemini`     | Week 4    | Week 5    | **Explain Google Takeout in the first 20 seconds.** No one-click promise. | ⏳ Pending |
| 5     | **Grok**       | Pro  | `guide-grok`       | `demo-grok`       | Week 4    | Week 6    | Pro note in the opening                                                   | ⏳ Pending |
| 6     | **DeepSeek**   | Pro  | `guide-deepseek`   | `demo-deepseek`   | Week 5    | Week 6    | Pro note in the opening                                                   | ⏳ Pending |
| 7     | **Mistral**    | Pro  | `guide-mistral`    | `demo-mistral`    | Week 5    | Week 7    | Pro note in the opening                                                   | ⏳ Pending |
| 8     | **Qwen**       | Pro  | `guide-qwen`       | `demo-qwen`       | Week 6    | Week 8    | Pro note in the opening                                                   | ⏳ Pending |

#### The Gemini Demo Is Different

A one-minute Gemini demo can't show a Google Takeout request finishing, because Google takes time to prepare the file. Record the demo starting from a Takeout file you've already downloaded. Then say so on screen and in the description: "This demo starts with a Google Takeout file that's already downloaded. The full guide shows how to request one." 🔍 Confirm the Takeout import steps match the released app before recording.

#### Pro Note Wording

Every Pro guide opens with one calm line, such as:

> "Grok is part of TotalRecalls Pro. If you're on the Free Tier, the link in the description compares Free and Pro."

**Takeaway:** One guide and one Proof Demo per provider, recorded together. No spotlight videos, ever.

---

### 7. Week-by-Week Production Schedule

This schedule follows Master Implementation Plan V3. "Record" means captured and edited. "Publish" means public on the channel.

#### Week 0: Prerequisites

| Task                                                             | Status     |
| ---------------------------------------------------------------- | ---------- |
| Claim @TotalRecalls and matching social handles                  | ⏳ Pending  |
| Verify the channel by phone                                      | ⏳ Pending  |
| Confirm filename format and default Library path                 | 🔍 Confirm |
| Confirm Free Tier limit wording                                  | 🔍 Confirm |
| Confirm the TotalRecalls version for the launch batch            | 🔍 Confirm |
| Confirm whether the Library Folder explainer is Blog 1 or Blog 2 | 🔍 Confirm |

#### Weeks 1–2: Setup and Launch Recording

| Workstream          | Tasks                                                                                   | Status    |
| ------------------- | --------------------------------------------------------------------------------------- | --------- |
| **Channel**         | Profile image, banner, About section, header links, upload defaults, community settings | ⏳ Pending |
| **Systems**         | Tracking sheet, thumbnail template, end card template                                   | ⏳ Pending |
| **Recording**       | Session A: the six launch videos, plus Claude and Perplexity Proof Demos                | ⏳ Pending |
| **Post-production** | Edit, caption, thumbnails, descriptions, and pinned comments for all eight              | ⏳ Pending |
| **Review**          | Second-person accuracy check on all eight                                               | ⏳ Pending |

#### Weeks 3–4: Launch

| Week  | Publish                                                                    | Other Tasks                                                                                                                                               | Status    |
| ----- | -------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- |
| **3** | All six launch videos, together                                            | Set the trailer. Build Start Here, Provider Guides, and Quick Demos playlists. Pin a comment on each video. Send embed codes to the website (Section 15). | ⏳ Pending |
| **4** | Claude and Perplexity Proof Demos, plus 2–3 Shorts cut from the launch set | Session B: record Gemini and Grok guides and demos. Reply to launch comments daily.                                                                       | ⏳ Pending |

#### Weeks 5–8: Pro Coverage

| Week  | Publish                                                                            | Record                                                                 | Other Tasks                                            | Status    |
| ----- | ---------------------------------------------------------------------------------- | ---------------------------------------------------------------------- | ------------------------------------------------------ | --------- |
| **5** | Gemini guide and demo, plus 1–2 Shorts                                             | Session C: DeepSeek and Mistral                                        | Embed the Gemini video in its written guide            | ⏳ Pending |
| **6** | Grok and DeepSeek guides and demos, plus 1–2 Shorts                                | Session D: Qwen, plus the Going Pro videos                             | Write Gemini and Grok social clips                     | ⏳ Pending |
| **7** | Mistral guide and demo, plus "How to Upgrade to Pro and Activate Your License Key" | —                                                                      | Launch the Going Pro playlist once it has three videos | ⏳ Pending |
| **8** | Qwen guide and demo, plus "How to Move TotalRecalls Pro to a New PC"               | Session E: Markdown vs JSON, Windows search, "not sent to our servers" | First monthly metrics review                           | ⏳ Pending |

The Going Pro playlist reaches three videos in Week 7: the upgrade video, plus the Gemini and Grok guides. Pro provider guides belong in both Provider Guides and Going Pro.

🔍 Confirm the license activation steps, and the three-PC limit wording, before recording Session D.

#### Weeks 9–12: Trust and Ownership

Each blog-paired video publishes after its blog post, so the description can link to the written version from day one.

| Week   | Publish                                                  | Script Source               | Record                                                  | Status    |
| ------ | -------------------------------------------------------- | --------------------------- | ------------------------------------------------------- | --------- |
| **9**  | Markdown vs JSON: Which Saved Chat File Should You Use?  | Blog 3 ✅ (publishes Week 5) | Session F: backup, organizing, founder story, two fixes | ⏳ Pending |
| **9**  | Search All Your Saved AI Chats with Windows Search       | Blog 6 ⏳ (publishes Week 8) | —                                                       | ⏳ Pending |
| **10** | What "Not Sent to Our Servers" Means in TotalRecalls     | Blog 4 ✅ (publishes Week 6) | —                                                       | ⏳ Pending |
| **10** | First Troubleshooting video, from real support questions | Support log                 | —                                                       | ⏳ Pending |
| **11** | How to Back Up Your AI Conversation Library              | Blog 5 ✅ (publishes Week 7) | —                                                       | ⏳ Pending |
| **11** | Why I Built TotalRecalls                                 | Founder Story page          | —                                                       | ⏳ Pending |
| **12** | Organizing Your Saved AI Chats by Project                | Blog 7 ⏳ (publishes Week 9) | Product Update, recorded this week                      | ⏳ Pending |
| **12** | What's New in TotalRecalls: \[Month Year]                | Changelog                   | —                                                       | ⏳ Pending |
| **12** | Second Troubleshooting video                             | Support log                 | —                                                       | ⏳ Pending |

Start the Using Your Saved Chats playlist in Week 11, once Windows search, backup, and the Library folder video give it three entries. Start Troubleshooting once three fixes exist. Until then, add each fix to the most relevant existing playlist.

#### After Day 90

| Video                                                    | Script Source        | Status    |
| -------------------------------------------------------- | -------------------- | --------- |
| Opening Saved Chats in a Note-Taking App                 | Blog 8 ⏳             | ⏳ Pending |
| How to Use Your Saved AI Chats in VS Code                | Blog 9 ✅             | ⏳ Pending |
| Why It's Worth Keeping Your Own Copy of AI Conversations | Explainer, unwritten | ⏳ Pending |

#### Day 90 Checkpoint

By the end of Week 12, the channel should have:

- About 18–22 long videos, plus a Proof Demo for every provider
- Around 15–20 Shorts
- Five or six active playlists
- Every launch and provider video embedded on its matching website page
- Two monthly metrics reviews complete, with clear data on which videos send downloads

**Takeaway:** Record about two weeks ahead of publishing. That buffer is what keeps the schedule steady when a week goes sideways.

---

### 8. Blog Posts as Script Sources

Finished blog posts already contain the outline, examples, and careful wording a video needs. Turning a post into a script takes about an hour, not a day.

#### Blog-to-Video Map

| Blog                                     | Video                               | Blog Status | Video Publish | Status    |
| ---------------------------------------- | ----------------------------------- | ----------- | ------------- | --------- |
| Library Folder explainer (Blog 1 or 2)   | Where TotalRecalls Saves Your Files | 🔍 Confirm  | Week 3        | ⏳ Pending |
| Blog 3: Markdown vs JSON                 | Markdown vs JSON explainer          | ✅ Complete  | Week 9        | ⏳ Pending |
| Blog 4: Not sent to our servers          | "Not sent to our servers" explainer | ✅ Complete  | Week 10       | ⏳ Pending |
| Blog 5: Backup                           | Backing up your library             | ✅ Complete  | Week 11       | ⏳ Pending |
| Blog 6: Windows search (proposed)        | Windows search workflow             | ⏳ Pending   | Week 9        | ⏳ Pending |
| Blog 7: Organizing by project (proposed) | Organizing workflow                 | ⏳ Pending   | Week 12       | ⏳ Pending |
| Blog 8: Note-taking app (proposed)       | Note-taking workflow                | ⏳ Pending   | After day 90  | ⏳ Pending |
| Blog 9: VS Code                          | VS Code workflow                    | ✅ Complete  | After day 90  | ⏳ Pending |

#### How to Turn a Post into a Script

1. **Open with the Short Answer.** The post's three points become the first 20–30 seconds. Say the target search phrase naturally in the first 15 seconds.
2. **Map main sections to chapters.** Each H2 becomes one chapter. Most posts produce four or five.
3. **Show instead of describing.** Where the post explains a step, the video shows it on screen. Cut any sentence the picture already makes clear.
4. **Drop the tables.** Read out only the one or two rows that matter, or show the table briefly as a simple on-screen card.
5. **Keep the wording on claims.** Copy privacy, Gemini, device, and platform lines word for word. These were already checked.
6. **Close with the Recommendation.** The post's three steps become the final minute, followed by one spoken call to action.
7. **Write chapters from the final edit,** not the script, once trimming is done.

#### Special Care for Blog 4

The "not sent to our servers" video carries the most risk of overclaiming. Before recording:

- 🔍 Confirm the Pro license check sends only the license key
- 🔍 Confirm the Gemini Takeout conversion runs on the user's PC
- 🔍 Confirm the email signup collects only the email address
- ⏳ Run a second-person review of the script, and again of the final edit

Never say "fully offline" or "never touches the internet," in narration, on screen, or in the description.

**Takeaway:** The blog does the thinking. The video shows it working. Never change a checked claim while adapting a post.

---

### 9. Video Tracking System

One shared sheet tracks every video from idea to retirement. Master Implementation Plan V3 calls for videos and blog posts in the same sheet. Use one tab for each.

#### Columns

| Column                | Example                                     | Why It Matters                                    |
| --------------------- | ------------------------------------------- | ------------------------------------------------- |
| **ID**                | `V-003`                                     | Stable reference, even if the title changes       |
| **Title**             | How to Save Claude Conversations to Your PC | Final published title                             |
| **Series**            | Provider Guide                              | Drives thumbnail marker and template              |
| **Pillar**            | How-To                                      | Keeps the 70/30 content mix visible               |
| **Provider or topic** | Claude                                      | Groups videos for maintenance                     |
| **Script source**     | Claude written guide                        | Shows where checked wording came from             |
| **Paired blog**       | Blog 3                                      | Links the video to its post                       |
| **Campaign name**     | `guide-claude`                              | Must be unique                                    |
| **Stage**             | Edited                                      | See stages below                                  |
| **Recording date**    | 2026-10-14                                  | Needed for "Recorded with" line                   |
| **App version**       | \[version]                                  | Needed for the description                        |
| **Claims made**       | Not sent to our servers, Windows 10 and 11  | Speeds up the accuracy check and later updates    |
| **Shows price?**      | No                                          | Flags videos to update when the launch price ends |
| **Thumbnail done**    | Yes                                         | Upload checklist item                             |
| **Captions done**     | Yes                                         | Upload checklist item                             |
| **Reviewer**          | \[name]                                     | Second-person check                               |
| **Publish date**      | 2026-10-24                                  | Scheduling                                        |
| **URL**               | —                                           | Filled after publishing                           |
| **Playlists**         | Provider Guides                             | Playlist management                               |
| **Embedded on**       | Claude guide page                           | Embed coordination                                |
| **Shorts cut**        | 2                                           | Tracks reuse                                      |
| **Last checked**      | 2026-10                                     | Quarterly maintenance                             |
| **Notes**             | —                                           | Open issues                                       |

#### Production Stages

Each video moves through these stages in order. Update the Stage column the moment a step finishes.

1. **Idea**: listed, with a topic and series
2. **Scripted**: outline or script written from its source
3. **Recorded**: raw footage captured
4. **Edited**: cut, blurred, cursor and audio checked
5. **Captioned**: caption file corrected and ready
6. **Packaged**: title, thumbnail, description, and pinned comment ready
7. **Reviewed**: second-person accuracy check passed
8. **Scheduled**: uploaded and set to publish
9. **Published**: public, pinned comment posted, playlists added
10. **Embedded**: live on its matching website page
11. **Retired**: unlisted and replaced, with the replacement ID noted

#### Sheet Rules

- Never reuse a campaign name, even after a video is retired
- Log the campaign name before writing the description, not after
- Sort by Stage each Monday, so stuck videos are easy to spot
- Keep a "Support questions" tab for recurring comments and emails (Section 14)

**Takeaway:** If it isn't in the sheet, it doesn't exist. Five minutes of logging saves hours of hunting later.

---

### 10. Batch Recording Workflow

Batching is what makes the cadence possible for a small team. One session can produce two guides, two Proof Demos, and enough footage for four Shorts.

#### Session Plan

| Session | Week | Videos                                                                    | Approx. Time  | Status    |
| ------- | ---- | ------------------------------------------------------------------------- | ------------- | --------- |
| **A**   | 1–2  | Launch set (6), Claude and Perplexity demos                               | Two half-days | ⏳ Pending |
| **B**   | 4    | Gemini and Grok guides and demos                                          | Half-day      | ⏳ Pending |
| **C**   | 5    | DeepSeek and Mistral guides and demos                                     | Half-day      | ⏳ Pending |
| **D**   | 6    | Qwen guide and demo, upgrade and license activation, move Pro to a new PC | Half-day      | ⏳ Pending |
| **E**   | 8    | Markdown vs JSON, Windows search, "not sent to our servers"               | Half-day      | ⏳ Pending |
| **F**   | 9    | Backup, organizing, founder story, two Troubleshooting fixes              | Half-day      | ⏳ Pending |
| **G**   | 12   | Product Update                                                            | One hour      | ⏳ Pending |

Record the Product Update last and close to its publish date, so it only describes changes that have actually shipped.

#### The Day Before a Session

- Write or finalize each script, and print or open it on a second screen
- Load the sample conversations you'll download, and check they contain nothing personal
- Update TotalRecalls to the version you'll show, and note the version number
- Clear the Library folder of old test files, so the folder view looks clean
- Check each provider's sign-in screen still matches your script

#### During the Session

1. **Switch to the recording profile** and turn on Focus mode.
2. **Record a 10-second test** and check audio levels and screen sharpness.
3. **Record in segments.** One take per chapter is easier to fix than one long take.
4. **Say the section name before each take,** such as "Claude, sign in, take two." It makes editing faster.
5. **Leave two seconds of stillness** at the start and end of each take.
6. **Record the Proof Demo straight after its guide,** while the provider is still signed in.
7. **Capture spare footage for Shorts:** a close crop of the Library folder, an open Markdown file, and the download moment.
8. **Log each take** in the tracking sheet notes before moving on.

#### After the Session

- Back up raw footage the same day, to a drive separate from your editing computer
- Name files with the campaign name and take number, such as `guide-claude-take-02.mp4`
- Move each video to **Recorded** in the tracking sheet
- Sign out of every provider in the recording profile

**Takeaway:** Prepare the day before, record in segments, and back up the footage before you close the laptop.

---

### 11. Editing and Captions Workflow

#### Editing Checklist

- Trim loading time only, and note it for the disclaimer
- Blur emails, profile images, conversation titles, license keys, and order numbers
- Check every frame for a session token, browser address bar, or notification. Never publish one.
- Keep straight cuts or short crossfades. No zoom punches or flying logos.
- Keep music off, or low and neutral
- Add the end card for the final 5–20 seconds, leaving space for two end screen elements
- Export at 1080p or higher, named with the target phrase, such as `save-claude-conversations-windows.mp4`

#### Caption Workflow

1. Upload the video as Private.
2. Let YouTube generate automatic captions, or start from your script.
3. Correct every provider name, file type, and product term. Common errors include "Claude," "Qwen," "DeepSeek," ".md," and "JSON."
4. Download the corrected file as `.srt` and save it with the raw footage.
5. Keep the uploaded caption track as the default.

#### Chapter Timestamps

Write chapters from the final export. Start at 0:00, use at least three, and keep each one 10 seconds or longer.

**Takeaway:** The edit should be invisible. Viewers should see the app, not the editing.

---

### 12. Thumbnail Production Workflow

#### Steps

1. **Pick the screenshot** while editing. Use a real frame from the video: the Library folder, an open Markdown file, or the prov

---

## 8. Master Implementation Plan V2 (consolidated — superseded by V3, §2)

> Final consolidated operating document from the earlier Jasper pass. Kept for
> reference; V3 (§2) is current. Dated 2026-10-02.

## TotalRecalls Master Implementation Plan V2

**Status:** Final operating document. It consolidates every approved strategy into one plan.\
**Replaces:** The earlier Master Implementation Plan draft. Where any older document disagrees with this one, this plan wins.\
**Built for:** A founder-led team that records, writes, and publishes in small batches.

TotalRecalls makes one promise: **your AI conversations, saved to your own PC as Markdown and JSON files.** This plan shows how the website, provider guides, explainers, YouTube channel, social posts, and email work together to support that promise. It covers what to build, what to skip, who checks what, and the order to do it in.

---

### 1. How to Use This Plan

This document tells you **what happens and when**. The supporting documents hold the detail.

#### Supporting Documents

| Document                                          | What It Covers                                                     | Use It For                      |
| ------------------------------------------------- | ------------------------------------------------------------------ | ------------------------------- |
| **Master Implementation Plan V2** (this document) | Decisions, timeline, rhythm, guardrails, open items                | Weekly planning and priorities  |
| **Content Audit Plan V2**                         | Keep, update, merge, create, and retire decisions                  | Page and guide changes          |
| **YouTube Strategy V5**                           | Channel setup, video types, playlists, thumbnails, titles, cadence | Recording and publishing videos |
| **YouTube Description Templates**                 | Seven-part description structure, UTM naming, pinned comments      | Every upload                    |
| **Footer Email Signup HTML V2**                   | Signup markup, styles, behavior, accessibility                     | Development and QA              |
| **Footer Signup Success Message**                 | Final post-signup copy                                             | The success state               |

#### Precedence Rule

1. This plan sets priorities and timing.
2. Supporting documents set the detail inside those priorities.
3. If a supporting document conflicts with this plan on timing or scope, follow this plan. Section 10 lists the conflicts it resolves.

#### How the Pieces Fit Together

| Stage        | What Happens                                                              | Main Assets                                 |
| ------------ | ------------------------------------------------------------------------- | ------------------------------------------- |
| **Discover** | Someone searches "how to save ChatGPT conversations" on YouTube or Google | Provider Guide videos, written guides       |
| **Trust**    | A real screen recording or clear guide shows exactly what happens         | Proof Demos, See It Work, explainers        |
| **Visit**    | A description link or guide CTA brings them to totalrecalls.app           | Descriptions, pinned comments, guide CTAs   |
| **Try**      | They download the Free Tier                                               | Homepage, Download free button              |
| **Upgrade**  | They need another provider or more downloads                              | Pro guides, Going Pro videos, Pricing page  |
| **Stay**     | They keep hearing about real progress                                     | Footer signup, Product Update videos, email |

**Takeaway:** Read this plan on Monday. Open the supporting documents only when you're doing the task they cover.

---

### 2. Finalized Decisions

These decisions are closed. Reopen one only if the trigger in the last column happens.

| Area                             | Decision                                                                                                                       | Reopen Only If                                                                                     |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------- |
| **Blog spotlights**              | **Option A approved.** No standalone provider spotlight articles. Spotlight value moves into guides, videos, and social posts. | A clearly different search intent appears that no guide covers. Even then, test one article first. |
| **Provider coverage**            | Each provider gets **one written guide, one Provider Guide video, and one Proof Demo.**                                        | A provider is added or removed.                                                                    |
| **Email signup**                 | **Sitewide footer only.** One form per page. No popups, sticky bars, or exit-intent modals.                                    | Footer signups stay near zero after 90 days.                                                       |
| **CTA order**                    | Download free first, Pro second, email updates third.                                                                          | Never.                                                                                             |
| **Channel role**                 | YouTube is a **public evidence library**, not an ad channel or creator brand.                                                  | Never.                                                                                             |
| **Trailer**                      | A 45–60 second cut of the See It Work demo. No brand film.                                                                     | Never.                                                                                             |
| **Archive Amber**                | Reserved for **Download free** and **Buy Pro** on the website. Never on YouTube, thumbnails, banners, or the footer signup.    | Never.                                                                                             |
| **Platforms**                    | Windows 10 and 11. macOS and Linux are "in development," with no dates.                                                        | A version actually ships.                                                                          |
| **Prices in video descriptions** | None. Descriptions link to the Pricing page instead.                                                                           | Never.                                                                                             |

#### Why Option A Won

- **Guides already do the job.** They match search intent and lead straight to a download.
- **Guide plus video beats a spotlight.** Searchers get instructions and proof in one place.
- **Eight extra articles mean eight more pages to keep current.** Provider interfaces change often, and every extra page is a chance for claims to drift.
- **The real gap is elsewhere.** Explainers, ownership content, and founder material add more value per hour.

**Takeaway:** Don't spend time re-debating these. Spend it shipping.

---

### 3. Core Message Rules

Every asset follows these rules, from the homepage headline to a pinned comment.

#### One Job Per Asset

Each page, guide, and video has one clear job. If two assets do the same job, merge them. This rule is why the spotlight series was cancelled.

#### Call-to-Action Hierarchy

| Priority | Action                                  | Where It Appears                                          |
| -------- | --------------------------------------- | --------------------------------------------------------- |
| **1**    | **Download free**                       | Every page, guide, video, description, and pinned comment |
| **2**    | **Buy Pro** or **Compare Free and Pro** | Pricing page, Pro guides, Going Pro videos                |
| **3**    | **Get product updates** (email)         | Site footer, Product Update videos, YouTube About section |

**Rules:**

- Pick one main ask per video or page section.
- Never push Pro inside a Free Tier guide.
- Never place the email signup beside Download free or Buy Pro.
- Never ask viewers to subscribe, like, comment, download, and buy in the same breath.

#### Spoken and Written Tone

- Calm, plain, and specific
- Show rather than claim
- No hype, fear, countdowns, or "smash that button"
- No hooks about AI companies deleting your chats

#### Brand Colors Across Channels

| Token             | Hex       | Use                                                     |
| ----------------- | --------- | ------------------------------------------------------- |
| **Obsidian**      | `#111315` | Backgrounds: site footer, banner, thumbnails, end cards |
| **Graphite**      | `#1A1D21` | Form field fills                                        |
| **Slate**         | `#2A2F36` | Borders, dividers, secondary buttons                    |
| **Paper**         | `#F3EFE7` | Headlines, wordmark, thumbnail text                     |
| **Mist**          | `#D9D4CB` | Body copy, labels, success messages                     |
| **Dust**          | `#B5AEA3` | Privacy lines, placeholders                             |
| **Steel Blue**    | `#7A8FA6` | Eyebrows, file paths, series markers, focus states      |
| **Archive Amber** | Reserved  | Download free and Buy Pro on the website only           |

**Takeaway:** If a piece of content asks for more than one thing, cut it back to Download free.

---

### 4. Website Implementation

The website explains the details and handles the download. Everything else sends people here.

#### Page-by-Page Plan

| Page                    | Job                                          | Required Elements                                                       | Matching Video                                         | Action                                            |
| ----------------------- | -------------------------------------------- | ----------------------------------------------------------------------- | ------------------------------------------------------ | ------------------------------------------------- |
| **Homepage**            | Explain the product and drive Free downloads | Clear promise, Download free, Compare Free and Pro                      | 60-second demo                                         | Embed demo                                        |
| **See It Work**         | Prove the app works                          | Demo, trust bullets, Download free first, then Pro link                 | 60-second demo (primary), Pro upgrade demo (secondary) | Confirm CTA order                                 |
| **Pricing**             | Explain Free vs Pro                          | Plan comparison, "$24 one-time (launch price)," device and update terms | Free vs Pro explained                                  | Embed video, add written explainer, check wording |
| **Provider guides** (8) | Provider-specific how-tos                    | Standard guide structure (Section 5)                                    | One Provider Guide video each                          | Upgrade all eight                                 |
| **Library folder page** | Show where files go                          | Folder path, file examples, Download free                               | Where TotalRecalls Saves Your Files                    | Publish                                           |
| **Explainers**          | Answer the "why" questions                   | Plain answers, Download free                                            | Matching explainer video                               | Create (Section 6)                                |
| **Ownership Path**      | Help people use their files                  | Workflow guidance, Download free, Compare link                          | Using Your Saved Chats videos                          | Embed workflow videos                             |
| **Founder Story**       | Build personal trust                         | Honest founder narrative                                                | Why I Built TotalRecalls                               | Embed when ready                                  |
| **Legal and Privacy**   | Explain data handling                        | Email service named as a service provider                               | None                                                   | Confirm wording                                   |

#### Video Embed Rules

- Use click-to-play thumbnails or lazy loading so embeds don't slow the page.
- Place the video near the top of guides, after "What you get" and "Why this provider matters."
- Never let an embed push Download free below the fold on desktop.

#### Footer Email Signup

The signup appears once per page, in the global footer, above the legal links and copyright line. A 1px Slate rule separates it from the legal links.

| Element             | Final Copy or Rule                                                                         |
| ------------------- | ------------------------------------------------------------------------------------------ |
| **Eyebrow**         | PRODUCT UPDATES                                                                            |
| **Headline**        | Follow what we build next                                                                  |
| **Description**     | Occasional emails about new features, new AI providers, and what's coming to TotalRecalls. |
| **Label**           | Email address (always visible)                                                             |
| **Placeholder**     | <you@example.com>                                                                          |
| **Button**          | Get updates, in the Secondary style. Never Archive Amber.                                  |
| **Error: invalid**  | Please enter a valid email address.                                                        |
| **Error: network**  | Something went wrong. Please try again in a moment.                                        |
| **Success message** | Copy from the Footer Signup Success Message document                                       |
| **Privacy line**    | Your email is never shared with any third party. Unsubscribe anytime.                      |

**Technical checks before launch:**

- The form posts without JavaScript and keeps browser email validation
- The honeypot field is rejected on the server, not only in the browser
- Focus moves to the success message after signup
- The error message is announced by screen readers
- One form renders per page, never repeated on Ownership Path or See It Work

#### Visual Review Checklist

A full visual review of the updated site is still pending. Run it once the final corrections are live, using a staging link or screenshots.

- Download free is the first and most visible action on every page
- Archive Amber appears only on Download free and Buy Pro
- Only one signup form shows per page
- Demo embeds load with click-to-play or lazy loading
- Every claim matches the guardrails in Section 12
- Mobile layouts stack cleanly, with readable text and full-width form fields
- Keyboard focus is visible on every link, field, and button

**Takeaway:** The site does the converting. Every other channel exists to send people to it with trust already earned.

---

### 5. Provider Guides

Guides are the core of the content library. With Option A approved, they also carry the spotlight role.

#### Standard Guide Structure

Every guide follows the same order, so readers know what to expect and updates stay simple:

1. **What you get:** the two files TotalRecalls saves
2. **Why this provider matters:** two or three neutral sentences
3. **Embedded video:** the matching Provider Guide video
4. **Step-by-step instructions** with screenshots
5. **Where your files go:** the Library folder
6. **Common problems and fixes**
7. **CTA:** Download free (Free Tier guides) or Compare Free and Pro (Pro guides)
8. **Last checked:** TotalRecalls version and month

#### "What You Get" Template

> When you download a \[Provider] conversation with TotalRecalls, you get two files on your PC:
>
> - **A Markdown file** you can open in any text editor or note-taking app
> - **A JSON file** with the full structured conversation
>
> Both are saved in your Library folder. Your conversations aren't sent to our servers.

For Gemini, adjust the opening line: "When you bring a Gemini Google Takeout file into TotalRecalls Pro, you get two files per conversation on your PC."

#### Provider Rollout

| Provider       | Tier | Written Guide Upgrade | Guide Video and Proof Demo | Special Note                                                                                      |
| -------------- | ---- | --------------------- | -------------------------- | ------------------------------------------------------------------------------------------------- |
| **ChatGPT**    | Free | Weeks 3–4             | Launch set (Weeks 3–4)     | Lead guide. Link to the Markdown vs JSON explainer once live.                                     |
| **Claude**     | Free | Weeks 3–4             | Launch set (Weeks 3–4)     | Add file examples.                                                                                |
| **Perplexity** | Free | Weeks 3–4             | Launch set (Weeks 3–4)     | Use "threads" to match search wording.                                                            |
| **Gemini**     | Pro  | Week 5                | Week 5                     | **Explain Google Takeout first.** Gemini works only through a Takeout file. No one-click promise. |
| **Grok**       | Pro  | Weeks 5–6             | Week 6                     | Add Pro note.                                                                                     |
| **DeepSeek**   | Pro  | Weeks 5–6             | Week 7                     | Add Pro note.                                                                                     |
| **Mistral**    | Pro  | Weeks 7–8             | Week 8                     | Add Pro note.                                                                                     |
| **Qwen**       | Pro  | Weeks 7–8             | Week 8                     | Add Pro note.                                                                                     |

#### Gemini Guide Requirements

- State in the first section that Gemini works through a Google Takeout file
- Show each step: request the Takeout file, download it, bring it into TotalRecalls
- Set honest expectations about Google's wait time for the Takeout file
- Never describe Gemini as a one-click download, anywhere

#### Guide Rules

- Keep "Why this provider matters" short and neutral. Don't describe the provider's own features.
- Write provider names as plain text. Never use logos.
- Never criticize a provider or imply a partnership.
- Move useful lines from archived spotlight drafts into the guide. Discard the rest.

**Takeaway:** Eight guides, one structure. When something changes, you update the same section in every guide.

---

### 6. Explainers, Ownership, and Founder Content

These pieces fill the real content gap. They use the time the spotlight series would have taken.

| Topic                                        | Type      | Written Version          | Video        | Priority |
| -------------------------------------------- | --------- | ------------------------ | ------------ | -------- |
| Free vs Pro, explained plainly               | Explainer | Weeks 3–4 (Pricing page) | Launch set   | High     |
| Where TotalRecalls saves your files          | Ownership | Weeks 3–4                | Launch set   | High     |
| Markdown vs JSON: which file should you use? | Explainer | Weeks 7–8                | Weeks 9–10   | High     |
| What "not sent to our servers" means         | Explainer | Weeks 7–8                | Weeks 9–10   | High     |
| Searching saved chats with Windows search    | Ownership | Weeks 9–10               | Weeks 9–10   | Medium   |
| Organizing saved chats by project            | Ownership | Weeks 9–10               | Weeks 9–10   | Medium   |
| Backing up your AI conversation library      | Ownership | Weeks 11–12              | Weeks 11–12  | Medium   |
| Why I built TotalRecalls                     | Founder   | Existing page            | Weeks 11–12  | Medium   |
| Why it's worth keeping your own copy         | Explainer | After Day 90             | Optional     | Medium   |
| Opening saved chats in a note-taking app     | Ownership | After Day 90             | After Day 90 | Low      |

#### The Highest-Risk Explainer

**"What 'not sent to our servers' means"** carries the most risk of overclaiming. It must say clearly that:

- Downloads connect directly from the user's PC to each AI provider
- Users sign in to each provider inside the app, on their own computer
- Saved files stay on the user's PC
- There's no TotalRecalls account to create

Never describe the app as "fully offline," and never say it "never touches the internet." Have a second person review this piece before it goes live.

#### Third-Party Apps

When ownership content shows outside tools such as VS Code or a note-taking app, name them as plain text and add a line saying TotalRecalls isn't affiliated with them.

**Takeaway:** Explainers answer the doubts that stop downloads. Ship the high-priority three first.

---

### 7. YouTube Channel

Full detail lives in **YouTube Strategy V5** and the **YouTube Description Templates**. This section covers what you need for planning.

#### Channel Setup

| Element           | Final Spec                                                                                                                                               |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Name**          | TotalRecalls (no tagline)                                                                                                                                |
| **Handle**        | @TotalRecalls, or @TotalRecallsApp as backup. Claim it in Week 0.                                                                                        |
| **Profile image** | Mark or wordmark in Paper on Obsidian, tested at 40 pixels                                                                                               |
| **Banner**        | Wordmark, "Save your AI conversations as local files.", and `MARKDOWN · JSON · WINDOWS 10/11` in Steel Blue mono. No logos, prices, schedules, or Amber. |
| **About section** | Draft from YouTube Strategy V5, checked against the live site                                                                                            |
| **Header links**  | Download free, See It Work, Guides, Pricing. All four carry UTM tags.                                                                                    |
| **Trailer**       | 45–60 second See It Work cut, captioned                                                                                                                  |
| **Home tab**      | Trailer, Start Here, Provider Guides, Using Your Saved Chats, Latest uploads                                                                             |

#### Content Pillars

| Pillar        | Share in First 90 Days | Video Types                      |
| ------------- | ---------------------- | -------------------------------- |
| **Proof**     | About 70% combined     | Proof Demos                      |
| **How-To**    | (with Proof)           | Provider Guides, Troubleshooting |
| **Ownership** | About 30% combined     | Workflow videos, Explainers      |
| **Updates**   | (with Ownership)       | Product Updates                  |

#### Launch Set

Publish these six together, so the channel is useful on day one:

1. TotalRecalls in 60 Seconds: One Real ChatGPT Download (also the trailer)
2. How to Save ChatGPT Conversations to Your PC
3. How to Save Claude Conversations to Your PC
4. How to Save Perplexity Threads to Your PC
5. Where TotalRecalls Saves Your Files
6. Free vs Pro: What's Included in Each

The Claude and Perplexity Proof Demos are recorded in the same sessions and published with the launch set as bonus videos.

#### Cadence

| Phase       | Timing         | Output                                         |
| ----------- | -------------- | ---------------------------------------------- |
| **Launch**  | Weeks 3–4      | 6 core videos together, plus Proof Demos       |
| **Build**   | Weeks 5–12     | About one long video per week, plus 1–2 Shorts |
| **Steady**  | Month 4 onward | Two long videos per month, Shorts as available |
| **Ongoing** | Always         | Re-record when interfaces change               |

Proof Demos recorded alongside a Provider Guide don't count toward the weekly long video.

#### Playlists

| Playlist                   | Launch Timing                        |
| -------------------------- | ------------------------------------ |
| **Start Here**             | Weeks 3–4                            |
| **Provider Guides**        | Weeks 3–4                            |
| **Quick Demos**            | Weeks 3–4                            |
| **Going Pro**              | Week 8                               |
| **Using Your Saved Chats** | Weeks 9–10                           |
| **Troubleshooting**        | Weeks 11–12, once three videos exist |
| **Product Updates**        | Add after the third update video     |

#### Production Rules

- Real screen capture only. Never mock up a screen.
- Calm pacing, clear audio, uploaded captions
- Blur emails, profile images, conversation titles, license keys, and order numbers. Never show a session token.
- Enlarged cursor, 1080p or higher, zoomed app window
- Straight cuts or short crossfades. No zoom punches or sw

---
## 9. Blog Series (10 posts — Jasper, October 2026)

All ten blog posts from the Jasper campaign, verbatim. Canonical copies live in
`Jasper/YouTube/Blog/` (duplicates of the same files sit in `Jasper/YouTube/` root
— the `Blog/` copies are canonical).

Series map: 4 explainer/educational + 6 workflow/how-to (per the YouTube
Implementation Plan's blog series plan). Filename convention going forward:
kebab-case + date (`YYYY-MM-DD-<slug>.md`); the existing files predate the
convention and keep their names.

---

_(source: `Blog/Free vs Pro Explainer Blog.md`)_

## Free vs Pro, Explained Plainly

You've been using TotalRecalls to save your ChatGPT chats. A few conversations are now sitting in your Library folder as Markdown and JSON files. Then, partway through another download, the app lets you know you've reached the Free Tier limit.

That moment raises fair questions. What happens to the files you already saved? What does Pro add? Is it worth paying for?

This post answers those questions in plain terms, with no pressure either way. Many people will find the Free Tier covers everything they need. Others will want more providers or more downloads. Here's how to tell which one fits you.

---

### What Happens When You Reach the Free Tier Limit

Reaching the limit doesn't take anything away from you.

- **Your saved files stay on your PC.** Every Markdown and JSON file you've downloaded is still in your Library folder. You can open, search, copy, and back them up the same way you always could.
- **The app keeps working.** You can still browse your library and open your files.
- **New downloads pause at the limit.** To download beyond it, you'd move to Pro.

That's the whole trade. Free gives you a real, working version of TotalRecalls with a cap on downloads. Pro removes the cap and adds more providers.

---

### What the Free Tier Includes

The Free Tier isn't a trial or a stripped-down demo. It's the same app, doing the same job, for three of the most widely used AI providers.

#### Providers on Free

- **ChatGPT**
- **Claude**
- **Perplexity**

#### How It Works

You sign in to each provider inside the app, on your own computer. You choose the conversations you want, and TotalRecalls saves each one to your PC as two files:

- **A Markdown file** you can open in Notepad, VS Code, or a note-taking app
- **A JSON file** with the full structured conversation

Both land in your Library folder. Your conversations aren't sent to our servers, and there's no TotalRecalls account to create.

#### Who Free Suits Best

Free is a good fit if you:

- Mainly use ChatGPT, Claude, or Perplexity
- Want to save a handful of important conversations, not your whole history
- Want to see exactly how the app works before deciding anything else

If that sounds like you, you may never need Pro. That's fine.

---

### What Pro Adds

Pro builds on everything in the Free Tier. It adds two things: more providers and unlimited downloads.

#### Five More Providers

Pro adds support for:

- **Gemini** (through Google Takeout)
- **Grok**
- **DeepSeek**
- **Mistral**
- **Qwen**

Combined with the three Free Tier providers, that's eight in total. Conversations from every provider save the same way, as Markdown and JSON files in your Library folder.

#### A Note on Gemini

Gemini works a little differently, and it's worth knowing up front.

Gemini conversations don't download in one click like ChatGPT. Instead, you request a Google Takeout file from your Google account, download that file when it's ready, and then bring it into TotalRecalls Pro. The app turns it into the same Markdown and JSON files you get from every other provider.

Google can take some time to prepare a Takeout file, so plan for a short wait. Once you have it, the rest is quick.

#### Unlimited Downloads

Pro removes the download limit. You can save as many conversations as you like, from any supported provider, as often as you need. That makes Pro the better choice if you want to keep a full archive of your AI work rather than a few highlights.

---

### Free and Pro Side by Side

|                                     | **Free** | **Pro**                     |
| ----------------------------------- | -------- | --------------------------- |
| **ChatGPT, Claude, Perplexity**     | Included | Included                    |
| **Gemini (through Google Takeout)** | —        | Included                    |
| **Grok, DeepSeek, Mistral, Qwen**   | —        | Included                    |
| **Downloads**                       | Limited  | Unlimited                   |
| **Markdown and JSON files**         | Yes      | Yes                         |
| **Saved to your own PC**            | Yes      | Yes                         |
| **TotalRecalls account needed**     | No       | No                          |
| **Price**                           | Free     | $24 one-time (launch price) |
| **PCs**                             | Your PC  | Up to 3 PCs                 |
| **Updates**                         | Included | For the life of the product |

---

### How Pro Pricing Works

Pro costs **$24, one time, at the launch price.** There's no subscription and no monthly fee.

Here's what that one payment covers:

- **Activation on up to 3 PCs.** Use Pro on your desktop, your laptop, and one more computer. If you replace a PC, you can move your license to the new one, as long as you stay within three.
- **Updates for the life of the product.** As TotalRecalls improves and providers change their interfaces, you get those updates without paying again.
- **A license key, not an account.** You activate Pro by entering a license key in the app. There's still no TotalRecalls account to create.

TotalRecalls runs on Windows 10 and 11. macOS and Linux versions are in development.

---

### How to Choose

A simple way to decide:

**Stay on Free if:**

- You only use ChatGPT, Claude, or Perplexity
- You save conversations now and then, not in bulk
- You're still getting a feel for the app

**Consider Pro if:**

- You use Gemini, Grok, DeepSeek, Mistral, or Qwen
- You want to save your full conversation history
- You work across more than one PC
- You've reached the Free Tier limit and want to keep going

There's no rush. Free doesn't expire, and your saved files stay yours either way. The easiest way to decide is to start with Free, save a few conversations, and open the files yourself. You'll know quickly whether you need more.

---

**Download free at totalrecalls.app.**

---

_(source: `Blog/Library Folder Explainer Blog.md`)_

## Where TotalRecalls Saves Your Files

You just downloaded your first conversation with TotalRecalls. The app says it's done, and somewhere on your PC there are now two new files. This post shows you where they are, how they're organized, and what you'll see when you open them.

It takes about five minutes to read. By the end, you'll know exactly what you have and how to use it with tools already on your computer.

---

### Your Files Live in the Library Folder

Everything TotalRecalls saves goes into one place: the **Library folder**. It's a regular Windows folder on your own drive. You can open it in File Explorer, copy it, back it up, or search it like any other folder.

By default, you'll find it here:

```
C:\Users\[YourName]\Documents\TotalRecalls\Library
```

Replace `[YourName]` with your Windows user name.

#### Three Quick Ways to Get There

**1. Through File Explorer**

Open File Explorer, click **Documents** in the left panel, then open **TotalRecalls**, then **Library**.

**2. Through the address bar**

Open File Explorer, click the address bar at the top, paste this line, and press Enter:

```
%USERPROFILE%\Documents\TotalRecalls\Library
```

The `%USERPROFILE%` part fills in your user name automatically.

**3. Through the Run box**

Press **Windows key + R**, paste the same line, and press Enter. File Explorer opens straight to the folder.

#### Keep It One Click Away

Once you're in the Library folder, right-click it in the left panel or the address bar and choose **Pin to Quick access**. It will then appear in File Explorer's sidebar every time you open it, on both Windows 10 and Windows 11.

---

### How the Library Folder Is Organized

Inside the Library folder, each AI provider gets its own subfolder. Each conversation you download becomes a pair of files with the same name, one ending in `.md` and one ending in `.json`.

Here's what a Library might look like after a few downloads:

```
Library
├── chatgpt
│   ├── pricing-research.md
│   ├── pricing-research.json
│   ├── trip-planning-lisbon.md
│   └── trip-planning-lisbon.json
├── claude
│   ├── quarterly-report-draft.md
│   └── quarterly-report-draft.json
└── perplexity
    ├── laptop-comparison.md
    └── laptop-comparison.json
```

A few things are worth knowing:

- **One folder per provider.** ChatGPT conversations go in `chatgpt`, Claude in `claude`, and so on. If you use Pro, you'll also see folders for Gemini, Grok, DeepSeek, Mistral, and Qwen as you download from them.
- **File names come from the conversation.** They're based on the conversation's title, so you can usually recognize a chat at a glance.
- **Two files, same content.** The `.md` and `.json` files hold the same conversation in two different formats. You don't need both, but having both gives you options.

A provider's folder only appears after you download something from it. If you've only saved ChatGPT chats, you'll only see a `chatgpt` folder for now.

---

### What a Markdown File Looks Like

The `.md` file is the one most people open first. Markdown is plain text with a few simple marks for headings and emphasis. It's easy to read as is, and many apps display it neatly.

Here's an example of what you might see:

```
## Pricing research

**Provider:** ChatGPT
**Saved:** 2026-10-02

---

### You

What are common pricing models for small desktop software tools?

### ChatGPT

Most small desktop tools use one of three models:

1. **One-time purchase.** Pay once and keep the version you bought.
2. **Subscription.** Pay monthly or yearly for continued access.
3. **Freemium.** A free version with paid upgrades.
```

Your files may differ slightly in layout, but the idea is the same: each message is labeled, in order, as readable text.

#### How to Open a Markdown File

You already have a tool that can open it. Some good options:

- **Notepad.** Built into Windows. Shows the raw text, including the `#` and `**` marks.
- **VS Code.** A free code editor. It can show a formatted preview of Markdown.
- **A note-taking app.** Many note apps can import or open Markdown files directly.

If Windows asks how you want to open a `.md` file, right-click it and choose **Open with**, then pick **Notepad** or another app. Check **Always use this app to open .md files** to skip the question next time.

#### When Markdown Is Most Useful

- Rereading an old conversation
- Copying part of a chat into a document or email
- Keeping notes from AI work alongside your other notes
- Sharing a single conversation with a coworker

---

### What a JSON File Looks Like

The `.json` file holds the same conversation in a structured format. It's less pleasant to read, but it's very easy for software to work with.

A simplified example:

```
{
  "title": "Pricing research",
  "provider": "chatgpt",
  "saved_at": "2026-10-02T14:31:00Z",
  "messages": [
    {
      "role": "user",
      "content": "What are common pricing models for small desktop software tools?"
    },
    {
      "role": "assistant",
      "content": "Most small desktop tools use one of three models..."
    }
  ]
}
```

The exact fields in your files may vary, but the shape is the same: details about the conversation at the top, then each message in order, labeled by who sent it.

#### How to Open a JSON File

- **Notepad** opens it fine, though long files can be hard to scan.
- **VS Code** adds color and lets you fold sections, which makes it much easier to read.
- **Microsoft Edge** can display JSON files in a tidy, readable layout. Drag the file into a browser window to try it.

#### When JSON Is Most Useful

- Importing conversations into another tool or personal database
- Processing many conversations with a script
- Keeping a complete, structured record alongside the readable version

If you're not sure you'll ever need it, that's okay. Leave it in the folder. It takes up very little space.

---

### Finding a Conversation Later

As your Library grows, you'll want to find things quickly. Windows has good tools for this already.

#### Search in File Explorer

Open the Library folder and type in the search box at the top right. File Explorer searches file names in the folder and all its subfolders. To search one provider only, open that provider's folder first.

#### Search Inside Files

Windows can also search the text inside your files, not just their names. Results depend on whether Windows has indexed the folder. Because the Library folder lives under Documents, Windows usually indexes it by default.

If a search doesn't find words you know are in a file, check your indexing settings:

- **Windows 11:** Settings → Privacy & security → Searching Windows
- **Windows 10:** Settings → Search → Searching Windows

Make sure your Documents folder is included.

#### Sort by Date

In File Explorer, switch to **Details** view and click the **Date modified** column. Your most recent downloads move to the top. This is the fastest way to find something you saved earlier today.

---

### Why Local Files Matter

TotalRecalls saves conversations as ordinary files on your PC for a few simple reasons.

**They're yours to keep.** Your saved files don't depend on a TotalRecalls account, because there isn't one. They don't depend on the app either. You can open them with Notepad years from now.

**They work with tools you already use.** Search, backup software, editors, note apps, and scripts all understand plain files. Nothing is locked in a format only one app can read.

**You decide where they go.** Your conversations aren't sent to our servers. When you download, the app connects directly from your PC to the AI provider you signed in to, and the files are written to your drive. After that, opening a saved file doesn't need TotalRecalls or an internet connection.

One thing to check: some Windows setups sync the Documents folder to OneDrive automatically. If yours does, your Library folder will sync too, just like the rest of Documents. That's a Windows setting, not a TotalRecalls one. You can look for the OneDrive icon in File Explorer's sidebar to see whether it applies to you.

---

### A Few Good Habits

- **Back up the Library folder now and then.** Copy it to an external drive or another backup location you trust. It's a single folder, so this is quick.
- **Copy before you reorganize.** If you'd like to sort conversations by project, copy files into a separate folder rather than moving the originals. That keeps the Library just as TotalRecalls expects it.
- **Keep both formats.** Markdown is for reading. JSON is for tools. Together, they cover nearly anything you might want to do later.

---

### Quick Reference

| Question                        | Answer                                               |
| ------------------------------- | ---------------------------------------------------- |
| **Where's the Library folder?** | `C:\Users\[YourName]\Documents\TotalRecalls\Library` |
| **How is it organized?**        | One subfolder per provider                           |
| **What files do I get?**        | A `.md` and a `.json` file for each conversation     |
| **What opens Markdown?**        | Notepad, VS Code, or a note-taking app               |
| **What opens JSON?**            | Notepad, VS Code, or Microsoft Edge                  |
| **How do I find a chat?**       | File Explorer search, or sort by Date modified       |
| **Which Windows versions?**     | Windows 10 and 11                                    |

---

That's all there is to it. Your conversations are now regular files in a regular folder, on your own PC, ready to read, search, and keep.

If you haven't tried TotalRecalls yet, the Free Tier covers ChatGPT, Claude, and Perplexity, and you can save your first conversation in a few minutes.

**Download free at totalrecalls.app.**

---

_(source: `Blog/Backup Library Blog 5.md`)_

**Meta title:** How to Back Up Your AI Conversation Library

**Meta description:** Your saved AI chats are only as safe as the PC they're on. Here's how to back up your TotalRecalls Library folder, step by step.

---

## How to Back Up Your AI Conversation Library

When you save a conversation with TotalRecalls, it lands in your Library folder as a Markdown file and a JSON file. Those files live on your PC, which means you control them. It also means they're only as safe as that one computer.

A hard drive can fail. A laptop can be lost or replaced. A backup means none of that costs you the conversations you chose to keep.

This post shows you how to back up your AI conversation library in plain steps. It takes about six minutes to read. You'll learn:

- What to back up, and what you can skip
- Four simple backup methods, with the tradeoffs of each
- How often to back up, and how to check that it worked

---

### The Short Answer

The whole idea fits in three points:

- **Back up the entire Library folder.** It holds every saved conversation, in both formats, organized by provider.
- **Keep at least one copy off your PC.** An external drive is the simplest choice. A cloud folder works too, if you're comfortable storing your chats with that service.
- **Repeat it regularly.** Back up after a big download session, and on a set schedule, such as once a month.

**Takeaway:** Copy the whole Library folder to a second place, and do it on a schedule you'll actually keep.

---

### What to Back Up

Your Library folder is the only thing you need to protect. Inside it, each provider has its own subfolder:

```
Library
├── chatgpt
├── claude
└── perplexity
```

Every conversation sits inside as a pair of files, one `.md` and one `.json`. Back up both. The Markdown file is what you'll read later. The JSON file is what you'll need if you ever import your chats into another tool.

#### A Few Extras Worth Keeping

**Your Pro license details.** If you use Pro, store your license key and order email somewhere safe, such as a password manager. Pro activates on up to three PCs, so you'll want the key handy when you set up a new computer.

**Gemini Takeout files.** On Pro, Gemini conversations come through a Google Takeout file. TotalRecalls converts it into Markdown and JSON files in your Library folder. Keeping the original Takeout file is optional, but it gives you a second source if you ever want to convert it again.

#### What You Can Skip

You don't need to back up the TotalRecalls app itself. You can download it again from totalrecalls.app at any time. Your conversations are what matter, and they're all in the Library folder.

**Takeaway:** Back up the Library folder. Keep your license key safe. Everything else can be replaced.

---

### Four Ways to Back Up Your Library Folder

There's no single right method. The best one is the one that fits how you already use your PC. Here are four options, from most hands-on to most automatic.

#### 1. Copy It to an External Drive

This is the simplest backup and the easiest to understand.

1. Plug in a USB flash drive or external hard drive.
2. Open File Explorer and find your Library folder.
3. Copy the whole folder onto the drive.
4. When the copy finishes, safely eject the drive.

For example, you might keep a small USB drive in a desk drawer. Once a month, you plug it in, copy the Library folder over the old copy, and put the drive away.

**Tradeoff:** It only happens when you remember to do it.

#### 2. Use Windows File History

Windows 10 and 11 both include File History, a built-in tool that backs up files to an external drive on a schedule.

1. Connect an external drive.
2. Search for "File History" in the Start menu and open it.
3. Turn it on and choose your drive.
4. Check which folders it covers.

File History focuses on standard folders, such as Documents. If your Library folder sits somewhere else, make sure it's included, or it won't be backed up.

**Tradeoff:** It runs automatically, but only while the drive is connected.

#### 3. Keep a Copy in a Cloud Folder

You can copy your Library folder into OneDrive, Dropbox, Google Drive, or a similar service. Your files then live on that service's servers as well as your PC.

This protects your chats if your computer and drive are both lost. Before you do it, though, make a deliberate choice. Your conversations aren't sent to our servers, but a cloud service will store whatever you place in its folder, under its own policies.

**Tradeoff:** Strong protection against losing your PC, but your files no longer stay only on your computer.

#### 4. Make a Dated Zip Archive

A zip file bundles your whole Library folder into one compressed file.

1. Right-click your Library folder in File Explorer.
2. Choose the option to compress it to a zip file.
3. Rename it with the date, such as `library-backup-2026-10.zip`.
4. Move the zip file to an external drive or another safe location.

Dated archives give you snapshots over time. If you delete or edit a file by mistake, you can open an older archive and recover it.

**Tradeoff:** Tidy and easy to store, but each archive is a manual step.

**Takeaway:** Pick one method to start. You can always add a second one later.

---

### Backup Methods Side by Side

|                                                   | **External Drive Copy** | **File History**              | **Cloud Folder**         | **Zip Archive**           |
| ------------------------------------------------- | ----------------------- | ----------------------------- | ------------------------ | ------------------------- |
| **Effort**                                        | Low, but manual         | Set once, then automatic      | Set once, then automatic | Low, but manual           |
| **Runs on its own?**                              | No                      | Yes, with the drive connected | Yes                      | No                        |
| **Files stay off the cloud?**                     | Yes                     | Yes                           | No                       | Yes, if stored locally    |
| **Protects against PC failure**                   | Yes                     | Yes                           | Yes                      | Yes, if stored off the PC |
| **Protects against losing PC and drive together** | No                      | No                            | Yes                      | Only if stored elsewhere  |
| **Keeps older versions**                          | No                      | Yes                           | Depends on the service   | Yes, one per archive      |
| **Built into Windows**                            | Yes                     | Yes                           | No                       | Yes                       |

**Takeaway:** For most people, an external drive covers the basics. Add a cloud folder or a second drive if you want protection beyond your home or office.

---

### How Often to Back Up

The right schedule depends on how often you save new conversations. Here's a simple guide:

| How You Use TotalRecalls                 | Suggested Backup Schedule       |
| ---------------------------------------- | ------------------------------- |
| You save a few chats now and then        | Once a month                    |
| You save conversations every week        | Every week or two               |
| You just finished a large download       | Right away                      |
| You're about to replace or reset your PC | Right away, then check the copy |

A good rule of thumb is this: back up whenever losing your new conversations would bother you. If you just saved six months of project chats, that's a good moment.

**Takeaway:** Match your backup schedule to how much you'd lose if your PC failed today.

---

### How to Check That Your Backup Worked

A backup you've never opened is a guess. Checking takes two minutes.

1. Open your backup location, whether it's a drive, cloud folder, or zip file.
2. Confirm each provider subfolder is there.
3. Open two or three `.md` files and read a few lines.
4. Open one `.json` file to make sure it isn't empty.

Because both formats are standard, you don't need TotalRecalls to open them. Notepad works for both.

**Takeaway:** Open a few files from every new backup. If you can read them, your backup works.

---

### Common Questions

#### Does TotalRecalls back up my files automatically?

TotalRecalls saves your conversations into your Library folder. Backing up that folder is up to you, using any of the methods above.

#### Can I restore my conversations on a new PC?

Yes. Copy your Library folder from the backup onto the new computer. The files open in Notepad, VS Code, or note-taking apps right away. If you use Pro, install TotalRecalls and enter your license key. Pro activates on up to three PCs.

#### Isn't my provider already storing my chats?

Your original conversations stay with your provider, under that provider's own policies. Your Library folder holds your own copy. A backup protects that copy if something happens to your PC.

#### Should I back up both the Markdown and JSON files?

Yes. They're small, and each serves a different purpose. Backing up the whole folder keeps both without any extra effort.

#### Is it safe to keep backups on a USB drive?

It's as safe as the drive itself. If the drive could be lost, consider an encrypted one. Some editions of Windows include BitLocker To Go for encrypting removable drives.

#### Does this work on Mac or Linux?

TotalRecalls runs on Windows 10 and 11. macOS and Linux versions are in development.

---

### The Recommendation for Most People

**Start with an external drive.** Copy your whole Library folder onto it today. It takes a few minutes and covers the most common risk, which is a failing or replaced PC.

**Put it on a schedule.** Set a monthly reminder, or turn on File History so it happens automatically. Back up right away after any big download session.

**Add a second location if your chats matter a lot.** A second drive kept somewhere else, or a cloud folder you've chosen on purpose, protects you if your PC and first drive are lost together.

---

### Your Chats, Kept Twice

Saving your AI conversations as files gives you control. Backing them up makes that control last. One copy on your PC and one somewhere else is all it takes.

Choose a method, copy your Library folder, and open a few files to check it worked. Then repeat it on a schedule you'll keep.

If you haven't tried TotalRecalls yet, the Free Tier covers ChatGPT, Claude, and Perplexity on Windows 10 and 11. You can save your first conversation in a few minutes, then back it up the same day.

**Download free at totalrecalls.app.**

---

_(source: `Blog/Privacy Explainer Blog 4.md`)_

**Meta title:** What "Not Sent to Our Servers" Means in TotalRecalls

**Meta description:** TotalRecalls saves your AI conversations to your own PC. Here's exactly what connects to the internet, what doesn't, and where your chats actually go.

---

## What "Not Sent to Our Servers" Means in TotalRecalls

On our website, in our videos, and inside the app, you'll see one line again and again: **your conversations aren't sent to our servers.** It's the most important promise we make. It deserves more than a single sentence.

This post explains what that line covers and what it doesn't. You'll see which parts of TotalRecalls connect to the internet, where your conversations travel when you download them, and where they end up. It takes about six minutes to read. By the end, you should be able to explain how the app handles your chats in your own words.

---

### The Short Answer

Here's the whole idea in three points:

- **Your conversations travel from the AI provider straight to your PC.** TotalRecalls doesn't route them through our own servers along the way.
- **Your saved files stay on your computer.** They live in your Library folder, as Markdown and JSON files you control.
- **Some parts of the app still use the internet.** Downloading a conversation means connecting to the provider that holds it. A few other tasks connect too, and we list them below.

**Takeaway:** TotalRecalls is a direct line between you and your AI provider. We aren't standing in the middle of it.

---

### Why We Say It This Way

You might wonder why we don't simply call TotalRecalls "offline." The honest answer is that it wouldn't be true.

Your AI conversations are stored by the provider you used, such as ChatGPT or Claude. To make a copy, TotalRecalls has to reach that provider over the internet. No app can download your chat history without connecting to the place where it lives.

So we use a narrower, more precise promise. "Not sent to our servers" describes what actually happens. It tells you who handles your conversations, which is you and your provider, and who doesn't, which is us.

We'd rather make a smaller claim that holds up than a bigger one that doesn't.

**Takeaway:** The wording is careful on purpose. It describes the app as it really works.

---

### Where Your Conversations Actually Go

Here's the path a conversation takes when you download it, step by step.

1. **You open TotalRecalls on your Windows PC** and choose a provider, like Claude.
2. **You sign in to that provider inside the app.** The sign-in happens on your own computer, directly with the provider. You don't create a TotalRecalls account, and we never see your password.
3. **You pick the conversations you want.** The app requests them from the provider.
4. **The provider sends them to your PC.** They come straight from the provider to your computer.
5. **TotalRecalls saves them as files.** Each conversation becomes a Markdown file and a JSON file in your Library folder.

Here's the same path as a simple picture:

```
AI provider  ───────────────►  Your PC  ───────►  Library folder
(e.g. Claude)   direct download   (TotalRecalls)    .md + .json files

TotalRecalls servers:  not part of this path
```

#### Gemini Works a Little Differently

On Pro, Gemini conversations come through a Google Takeout file. You request that file from Google and download it to your PC yourself. Then you bring it into TotalRecalls, which turns it into the same Markdown and JSON files as every other provider. The conversion happens on your computer, so the result is the same: your conversations aren't sent to our servers.

**Takeaway:** Your conversations make one trip, from the provider to your PC. Then they stay put.

---

### What Connects to the Internet

Being clear about this is the point of the whole post. These are the moments when TotalRecalls, or something related to it, uses the internet:

- **Signing in to a provider.** The sign-in window connects directly to that provider, the same way a browser would.
- **Downloading conversations.** The app connects to the provider to fetch the chats you selected.
- **Activating Pro.** When you enter a Pro license key, the app checks it so your license can work across up to three PCs. That check involves your license key, not your conversations.
- **Buying Pro.** Your purchase happens on our website, through a checkout process, before you ever enter a key in the app.
- **Getting the app.** You download TotalRecalls from totalrecalls.app, like any other Windows program.
- **Signing up for product updates.** If you choose to join our email list, we receive the email address you enter. That's the only thing the form collects.

### What Doesn't Need the Internet

Once your conversations are saved, a lot of what you'll do with them happens entirely on your PC:

- **Opening your saved files.** Markdown and JSON are standard formats. Notepad, VS Code, and many note-taking apps can open them without a connection.
- **Searching your saved chats.** Windows search looks through files on your own drive.
- **Organizing, copying, and backing up.** Moving files between folders or onto an external drive is ordinary file handling.

**Takeaway:** The internet is used to fetch your conversations and manage your license. Using your saved files doesn't require it.

---

### Connections at a Glance

| What You're Doing                | Connects To            | What's Shared                                    | Includes Your Conversations?           |
| -------------------------------- | ---------------------- | ------------------------------------------------ | -------------------------------------- |
| Signing in to a provider         | That AI provider       | Your sign-in, entered directly with the provider | No                                     |
| Downloading conversations        | That AI provider       | A request for your chats, sent from your PC      | Yes, from the provider to your PC only |
| Importing a Gemini Takeout file  | Nothing                | The file is converted on your PC                 | No                                     |
| Activating Pro                   | TotalRecalls licensing | Your license key                                 | No                                     |
| Buying Pro                       | Our website checkout   | Your purchase details                            | No                                     |
| Joining the email list           | Our email service      | Your email address                               | No                                     |
| Opening or searching saved files | Nothing                | Nothing                                          | No                                     |
| Backing up your Library folder   | Wherever you choose    | Whatever you choose to copy                      | Only if you copy them                  |

**Takeaway:** The only connection that carries your conversations is the one between you and the provider that already holds them.

---

### Where Your Files Live on Your PC

Every saved conversation goes into your Library folder, organized by provider:

```
Library
├── chatgpt
├── claude
└── perplexity
```

These are normal files on your drive. They sit alongside your documents and photos, and they follow the same rules.

That has one practical consequence worth knowing. If you place your Library folder inside a folder that syncs to the cloud, such as OneDrive, Dropbox, or Google Drive, that service will copy your files to its own servers. That's your choice to make, and it can be a useful backup. It just means "on my PC only" stops being true for those files.

The same goes for backups. If you copy your Library folder to an external drive, it lives there too. If you copy it to a cloud backup, it lives with that service.

**Takeaway:** Your files go wherever you put them. If you want them to stay only on your PC, keep the Library folder outside any synced folder.

---

### What "Not Sent to Our Servers" Doesn't Mean

A clear promise also needs clear limits. Here's what this line doesn't cover.

**It doesn't remove conversations from your provider.** TotalRecalls makes a copy. Your original conversations stay with ChatGPT, Claude, or whichever provider you used, under that provider's own policies.

**It doesn't make your PC more secure.** Your saved files are as safe as the computer they're on. A strong Windows password, current updates, and regular backups protect them better than any app can.

**It doesn't cover other apps you use.** If you open a saved chat in a note-taking app that syncs online, that app's rules apply.

**It doesn't mean the app never connects.** As covered above, downloads and license checks need the internet.

**Takeaway:** We control what TotalRecalls does with your conversations. We don't control your provider, your other apps, or your cloud settings.

---

### Common Questions

#### Do you ever see my AI conversations?

No. Your conversations aren't sent to our servers. They move from your provider to your PC, and TotalRecalls saves them in your Library folder.

#### Do I need a TotalRecalls account?

No. There's no TotalRecalls account to create. You sign in to each AI provider inside the app, directly with that provider.

#### Do you see my provider password?

No. You enter it in the provider's own sign-in window, on your computer. That sign-in goes to the provider, not to us.

#### What does the Pro license check send?

It sends your license key, so the app can confirm it's valid and track activations across your PCs. Pro activates on up to three PCs. Your conversations aren't part of that check.

#### Can I use my saved files without an internet connection?

Yes. Once a conversation is saved, you can open, read, search, and copy it without a connection. You'll only need the internet again to download new conversations.

#### Does deleting a file in TotalRecalls delete it from ChatGPT or Claude?

No. Your Library folder holds copies. Deleting a file there has no effect on the original conversation stored by your provider.

#### Which versions of Windows does this apply to?

TotalRecalls runs on Windows 10 and 11, and it handles your conversations the same way on both. macOS and Linux versions are in development.

---

### The Recommendation for Most People

**Trust the promise, and understand its edges.** Your conversations aren't sent to our servers. They travel from your provider straight to your PC.

**Decide where your Library folder lives.** If you want your files only on your computer, keep the folder outside OneDrive or any other synced location. If you'd like a cloud backup, place it there on purpose.

**Back up the whole folder.** Your saved chats are only as safe as your PC. Copy your Library folder to an external drive now and then, so one hardware problem doesn't cost you everything.

---

### A Smaller Promise You Can Check

"Not sent to our servers" isn't a slogan. It's a plain description of how TotalRecalls works. Your conversations come from your provider, land on your PC, and stay in a folder you control.

You don't have to take our word for it. Save a conversation, open your Library folder, and look at the files yourself. Everything we've described here is right there on your screen.

The Free Tier covers ChatGPT, Claude, and Perplexity, on Windows 10 and 11. You can save your first conversation in a few minutes and see exactly where it goes.

**Download free at totalrecalls.app.**

---

_(source: `Blog/Windows Search Blog 6.md`)_

**Meta title:** How to Search Your Saved AI Chats with Windows Search

**Meta description:** Your saved AI conversations are ordinary files on your PC. Here's how to find any of them in seconds with the search tools already built into Windows.

---

## How to Search Your Saved AI Conversations with Windows Search

Once you've saved a few dozen conversations with TotalRecalls, a new question comes up. Where was that answer about pricing? Which chat had the email draft you liked? Was it in ChatGPT or Claude?

You don't need a special tool to find out. Every conversation in your Library folder is a normal Markdown and JSON file, so Windows can search it like any other document on your PC.

This post shows you how to search your saved AI conversations with Windows Search. It takes about six minutes to read. You'll learn:

- Where to search, and which search box works best
- How to search inside your files, not just their names
- A few simple filters that narrow results fast
- How to make sure Windows can actually see what's inside your files

---

### The Short Answer

The whole idea fits in three points:

- **Search from inside your Library folder.** Open it in File Explorer and use the search box in the top-right corner.
- **Search the contents, not just the names.** Type `content:` before a word or phrase to search the text of every saved conversation.
- **Filter to Markdown files.** Add `ext:.md` so each conversation shows up once, in the format you'll want to read.

**Takeaway:** Open your Library folder, type `content:"your phrase" ext:.md`, and press Enter.

---

### Why Searching Your Files Works So Well

When a conversation lives only inside an AI provider's website, you can search it only with that provider's tools. And you can search only one provider at a time.

Saved files change that. Your ChatGPT, Claude, and Perplexity conversations sit side by side in one folder:

```
Library
├── chatgpt
│   ├── pricing-research.md
│   └── pricing-research.json
├── claude
│   ├── quarterly-report-draft.md
│   └── quarterly-report-draft.json
└── perplexity
    ├── laptop-battery-comparison.md
    └── laptop-battery-comparison.json
```

One search covers all of them. If you're on Pro, the same goes for Gemini, Grok, DeepSeek, Mistral, and Qwen.

It also happens on your own computer. Searching files in File Explorer looks through your own drive, and you don't need an internet connection to do it.

**Takeaway:** One folder, one search box, every provider at once.

---

### Step 1: Open Your Library Folder

Start in the right place. Searching from your Library folder keeps results focused on your saved conversations instead of your whole PC.

1. Open File Explorer.
2. Go to your Library folder.
3. Click the search box in the top-right corner of the window.

The search box says something like "Search Library." That means it will look through the Library folder and every provider subfolder inside it.

#### Make the Folder Easy to Reach

If you search often, pin the Library folder so it's always one click away:

1. Right-click the Library folder.
2. Choose **Pin to Quick Access** (Windows 10) or **Pin to Quick access** from the menu (Windows 11).

It now appears in the left-hand panel of every File Explorer window.

**Takeaway:** Always search from inside the Library folder. It keeps results relevant and fast.

---

### Step 2: Search Inside Your Conversations

Typing a plain word in the search box usually matches file names first. That's useful if you remember what a conversation was called. Most of the time, though, you remember what was *said*, not the title.

To search the text inside your files, add `content:` before your search term.

#### Basic Content Searches

| What You Type                        | What It Finds                                       |
| ------------------------------------ | --------------------------------------------------- |
| `content:pricing`                    | Conversations that mention "pricing" anywhere       |
| `content:"renewal rate"`             | Conversations with that exact phrase                |
| `content:invoice OR content:receipt` | Conversations mentioning either word                |
| `content:budget NOT content:2025`    | Conversations about budgets that don't mention 2025 |

A few small rules make these work:

- **Use quotes for exact phrases.** Without them, Windows may match the words separately.
- **Write AND, OR, and NOT in capitals.** In lowercase, Windows treats them as ordinary words.
- **Don't worry about capitalization in your search terms.** `content:Pricing` and `content:pricing` find the same files.

#### Example: Finding an Old Answer

Say you remember asking an AI for help with a cover letter months ago, but not which provider. In your Library folder, type:

```
content:"cover letter" ext:.md
```

Every matching conversation appears, from every provider, in one list. The folder path under each result shows which provider it came from.

**Takeaway:** `content:` turns the search box from a file-name finder into a full-text search of every saved chat.

---

### Step 3: Narrow Your Results with Filters

Filters help when a search returns too much. You can combine them with `content:` searches in the same box.

#### Show Each Conversation Only Once

Every conversation is saved as two files, so a content search often shows each match twice: once as `.md` and once as `.json`. Add `ext:.md` to see only the readable version:

```
content:"onboarding checklist" ext:.md
```

If you're looking for structured data for a script or another tool, use `ext:.json` instead.

#### Filter by Date

If you remember roughly when a conversation was saved, filter by date:

| What You Type              | What It Finds                                  |
| -------------------------- | ---------------------------------------------- |
| `datemodified:today`       | Files saved or changed today                   |
| `datemodified:this week`   | Files from this week                           |
| `datemodified:last month`  | Files from last month                          |
| `datemodified:>2026-09-01` | Files saved or changed after September 1, 2026 |

Keep in mind that this date reflects when the file was saved to your PC or last edited. It isn't always the day you had the conversation with the AI provider.

#### Filter by Provider

Each provider has its own subfolder. To search only one provider, open that subfolder first, such as `Library\claude`, then search from there.

#### Filter by File Name

If you remember part of a title, use `name:`:

```
name:pricing
```

This matches file names that include "pricing," like `pricing-research.md`.

#### Combining Filters

Filters stack. Here's a search for a phrase in Markdown files from the past month:

```
content:"launch plan" ext:.md datemodified:last month
```

**Takeaway:** Start with `content:` and `ext:.md`. Add a date or a provider subfolder when you need fewer results.

---

### Step 4: Make Sure Windows Can See Inside Your Files

Sometimes a content search comes back empty, even when you know the phrase is there. This usually means Windows isn't set up to read the contents of `.md` or `.json` files. A one-time setup fixes it.

#### Option A: Turn On Content Search in File Explorer

This is the quickest fix.

1. Open File Explorer.
2. Open **Folder Options**. In Windows 10, click **View**, then **Options**. In Windows 11, click the **three-dot menu** in the toolbar, then **Options**.
3. Go to the **Search** tab.
4. Check **Always search file names and contents**.
5. Click **OK**.

Searches may run a little slower with this on, especially in very large folders. For most Library folders, the difference is small.

#### Option B: Add Your Library Folder to the Windows Index

The Windows index is a catalog your PC builds so it can search faster. Adding your Library folder speeds up content searches, especially as your collection grows.

1. Search for **Indexing Options** in the Start menu and open it.
2. Click **Modify**.
3. Find your Library folder and check its box.
4. Click **OK**.

#### Check That Markdown and JSON Contents Are Indexed

Indexing a folder doesn't always mean indexing what's inside every file type. Check these two:

1. In **Indexing Options**, click **Advanced**.
2. Open the **File Types** tab.
3. Find `md` in the list. If it's missing, type `md` in the box at the bottom and click **Add**.
4. Select `md` and choose **Index Properties and File Contents**.
5. Repeat for `json`.
6. Click **OK**.

Windows may take a while to rebuild the index after these changes. Searches will improve once it finishes.

**Takeaway:** If content searches miss files you know are there, turn on content search or check that `.md` and `.json` contents are indexed.

---

### Search Methods Side by Side

|                                            | **Start Menu Search**           | **File Explorer Search**         | **File Explorer + Filters**        |
| ------------------------------------------ | ------------------------------- | -------------------------------- | ---------------------------------- |
| **Where you use it**                       | Taskbar or Start menu           | Search box in the Library folder | Search box in the Library folder   |
| **Searches only your saved chats?**        | No, searches your whole PC      | Yes                              | Yes                                |
| **Searches inside files?**                 | Indexed files only              | Yes, with `content:`             | Yes, with `content:`               |
| **Can filter by date or file type?**       | Limited                         | Yes                              | Yes                                |
| **Shows which provider a chat came from?** | Sometimes                       | Yes, in the folder path          | Yes, in the folder path            |
| **May include web results?**               | Yes, depending on your settings | No                               | No                                 |
| **Best for**                               | Quick lookups by file name      | Most everyday searches           | Large libraries and specific needs |

The Start menu can be handy for opening a file you know by name. Depending on your Windows settings, though, it may also suggest web results for what you type. If you'd like your searches to stay on your computer, use File Explorer from inside your Library folder.

**Takeaway:** For searching saved conversations, File Explorer is the better choice. It's focused, local, and supports filters.

---

### Common Questions

#### Why does each result show up twice?

Every conversation is saved as a Markdown file and a JSON file with the same name. Both contain the same text, so both match. Add `ext:.md` to your search to see each conversation once.

#### Can I search across every provider at once?

Yes. Search from the top of the Library folder, and Windows looks through every provider subfolder inside it. To search just one provider, open its subfolder first.

#### Do I need TotalRecalls open to search my chats?

No. Your saved conversations are standard files, so Windows can search them whether TotalRecalls is open or not.

#### Does searching send my conversations anywhere?

Searching in File Explorer looks through files on your own drive. Your conversations aren't sent to our servers when you save them, and searching them in File Explorer doesn't change that. If your Library folder sits inside a cloud-synced folder, that service already stores a copy under its own policies.

#### My search is slow. What can I do?

Add your Library folder to the Windows index, as described in Step 4. Indexed searches are much faster than searches that read every file each time.

#### Can I search my backups too?

Yes. Open your backup location in File Explorer and search the same way. A zip archive needs to be extracted first, since Windows can't search reliably inside compressed files.

#### Does this work on Mac or Linux?

TotalRecalls runs on Windows 10 and 11. macOS and Linux versions are in development.

---

### The Recommendation for Most People

**Pin your Library folder.** Put it in Quick Access so it's always one click away.

**Learn one search.** For nearly everything, this is all you need:

```
content:"your phrase" ext:.md
```

**Fix it once if results look thin.** If searches miss conversations you know exist, turn on content search in Folder Options or add `.md` and `.json` to the Windows index. After that, search should just work.

---

### Your Chats, Easy to Find

Saving your AI conversations as files means they belong to you. Being able to search them means you can actually use them. With one folder and one search box, every saved conversation from every provider is a few keystrokes away.

Open your Library folder, try a `content:` search for something you remember asking, and see how fast the right conversation turns up.

If you haven't tried TotalRecalls yet, the Free Tier covers ChatGPT, Claude, and Perplexity on Windows 10 and 11. You can save your first few conversations in minutes, then search them the same day.

**Download free at totalrecalls.app.**

---

_(source: `Blog/TotalRecalls Blog Post 7.md`)_

**Meta title:** How to Open Your Saved AI Chats in Obsidian (Windows)

**Meta description:** Your saved AI conversations are Markdown files, so Obsidian can open them directly. Here's how to set it up, link chats to your notes, and keep originals safe.

---

## How to Open Your Saved AI Chats in Obsidian

Searching your saved conversations helps you find one answer. Sometimes you want more than that. You want to read a chat next to your own notes, link it to a project, or come back to it as part of a bigger body of work.

Obsidian is a good fit for this. It's a note-taking app that works with plain Markdown files stored in a folder on your PC. Every conversation TotalRecalls saves is already a Markdown file, so Obsidian can open your saved AI chats with no conversion step.

This post shows you how to open your saved AI chats in Obsidian on Windows. It takes about seven minutes to read. You'll learn:

- Three ways to set it up, and which one suits you
- How to browse, search, and link your saved conversations
- How to keep your original files safe while you work with them
- A few settings that keep everything on your own computer

---

### The Short Answer

The whole idea fits in three points:

- **Obsidian reads folders of Markdown files.** It calls a folder a "vault," and your Library folder can become one.
- **Pick one setup and stick with it.** Open the Library folder as its own vault, or place it inside a vault you already use.
- **Keep the originals as they are.** Write your thoughts in separate notes that link back to each saved chat.

**Takeaway:** Open your Library folder in Obsidian, then add your own notes alongside your chats instead of inside them.

---

### Why Obsidian Works Well with Saved AI Chats

Obsidian doesn't store your notes in its own database or on its own servers. It reads and writes ordinary `.md` files in a folder you choose. That's the same format TotalRecalls saves your conversations in.

So nothing needs to be imported, exported, or converted. Your saved chats stay where they are on your drive, and Obsidian simply shows them to you in a more useful way.

Here's what that gives you:

- **Readable formatting.** Headings, lists, tables, and code blocks display cleanly.
- **Fast switching.** Jump between conversations by typing part of a title.
- **Links between ideas.** Connect a Claude chat to a ChatGPT chat, or to your own project notes.
- **A clear exit.** If you stop using Obsidian, your files are still plain Markdown in the same folder.

**Takeaway:** Obsidian adds a reading and linking layer on top of your files without taking them over.

---

### Before You Start

You need three things:

1. **Some saved conversations.** At least a few chats in your Library folder. The Free Tier covers ChatGPT, Claude, and Perplexity. Pro adds Gemini, Grok, DeepSeek, Mistral, and Qwen.
2. **Obsidian for Windows.** Download it from obsidian.md and run the installer. It works on Windows 10 and 11, and it's free to download and use.
3. **Your Library folder location.** By default, that's:

```
C:\TotalRecalls\Library\
```

Inside it, each provider has its own subfolder:

```
Library
├── chatgpt
│   ├── 2026-09-14-pricing-research.md
│   └── 2026-09-14-pricing-research.json
├── claude
│   ├── 2026-09-18-quarterly-report-draft.md
│   └── 2026-09-18-quarterly-report-draft.json
└── perplexity
    ├── 2026-09-22-laptop-battery-comparison.md
    └── 2026-09-22-laptop-battery-comparison.json
```

**Takeaway:** Install Obsidian and know where your Library folder lives. That's all the preparation you need.

---

### Step 1: Choose How to Set Up Your Vault

There are three sensible ways to bring your saved chats into Obsidian. Each one has trade-offs, so pick the one that matches how you already work.

#### Option A: Open the Library Folder as Its Own Vault

This is the simplest choice if you're new to Obsidian.

1. Open Obsidian.
2. Choose **Open folder as vault**.
3. Select your Library folder and click **Select Folder**.

Obsidian opens with every provider subfolder in the left-hand panel. Obsidian also adds a small hidden `.obsidian` folder inside Library to store its settings. Your conversation files aren't changed.

#### Option B: Move the Library Folder into a Vault You Already Use

If you already keep notes in Obsidian, you may want your chats in the same place.

1. Close TotalRecalls.
2. Move the Library folder into your existing vault folder.
3. If TotalRecalls lets you choose a save location, point it at the new path.
4. Open your vault in Obsidian. The Library folder appears alongside your other notes.

Check the save location carefully. If TotalRecalls keeps saving to the old path, new chats won't show up in your vault.

#### Option C: Copy Selected Chats into Your Vault

If you only want a handful of important conversations in your notes, copy them across.

1. Open your Library folder in File Explorer.
2. Copy the `.md` files you want.
3. Paste them into a folder inside your vault, such as `AI Chats`.

This keeps your vault tidy. The downside is that new chats won't appear on their own, and you'll have two copies of each file you move.

#### Setup Options Side by Side

|                                      | **A: Library as Its Own Vault** | **B: Library Inside Your Vault** | **C: Copy Selected Chats** |
| ------------------------------------ | ------------------------------- | -------------------------------- | -------------------------- |
| **Effort to set up**                 | Lowest                          | Medium                           | Low, but repeated          |
| **New chats appear automatically?**  | Yes                             | Yes, if the save path is updated | No                         |
| **Mixes chats with your own notes?** | No, separate vault              | Yes                              | Yes                        |
| **Duplicate files?**                 | No                              | No                               | Yes                        |
| **Easy to undo?**                    | Yes, close the vault            | Move the folder back             | Delete the copies          |
| **Best for**                         | New Obsidian users              | Existing Obsidian users          | Keeping only key chats     |

**Takeaway:** Start with Option A. Move to Option B once you know you want chats and notes in one place.

---

### Step 2: Browse Your Saved Conversations

Once your vault is open, the left-hand panel shows your folders. Click a provider subfolder, then click any file to read it.

#### Why You Won't See the JSON Files

By default, Obsidian only shows file types it can open as notes. Your `.json` files are still in the folder, but Obsidian hides them. That's helpful, because each conversation appears once in the readable Markdown version.

If you ever want to see them, go to **Settings → Files and links** and turn on **Detect all file extensions**. Most people can leave this off.

#### Switch Between Chats Quickly

Press **Ctrl + O** to open the Quick Switcher. Type part of a file name, such as `pricing`, and press Enter. Because filenames start with a date, typing `2026-09` also shows every chat saved that month.

#### Read in Reading View

Press **Ctrl + E** to switch between editing and reading view. Reading view displays the conversation cleanly and makes accidental edits less likely.

**Takeaway:** Use the Quick Switcher to move between chats, and reading view to read them safely.

---

### Step 3: Search Across Every Provider

Obsidian has its own search, and it covers every file in your vault at once.

1. Press **Ctrl + Shift + F** to open search.
2. Type a word or phrase.
3. Click a result to jump straight to that part of the conversation.

A few search tips work well with saved chats:

| What You Type        | What It Finds                             |
| -------------------- | ----------------------------------------- |
| `"renewal rate"`     | That exact phrase                         |
| `path:claude budget` | "Budget" in Claude conversations only     |
| `file:pricing`       | Files with "pricing" in the name          |
| `invoice OR receipt` | Either word                               |
| `budget -2025`       | "Budget" in chats that don't mention 2025 |

This works alongside Windows Search, not instead of it. Windows Search is useful from File Explorer and needs no extra app. Obsidian search is faster to use while you're already reading and writing notes.

**Takeaway:** Use `path:` to search one provider, and plain words or quoted phrases to search all of them.

---

### Step 4: Link Chats to Your Own Notes

This is where Obsidian earns its place. You can connect conversations to each other and to your own thinking.

#### Keep the Original Conversation Unchanged

Treat each saved chat as a record of what was said. If you edit it, you lose that record. Instead, write your notes in a separate file and link to the chat.

This also avoids surprises if you save the same conversation again later. Your notes live in your own file, so they stay safe whatever happens to the original.

#### Create a Note That Links to a Chat

1. Create a new note with **Ctrl + N**.
2. Give it a clear title, such as `Pricing decision`.
3. Type `[[` and start typing the chat's filename.
4. Pick the conversation from the list.

Your note now contains a link like this:

```
### Pricing decision

Went with the one-time model. Reasoning is in the original research chat:
[[2026-09-14-pricing-research]]

Follow-up questions I asked Claude:
[[2026-09-18-quarterly-report-draft]]
```

Click either link and Obsidian opens that conversation.

#### See Where a Chat Is Referenced

Open any saved conversation and look at the **Backlinks** panel. It lists every note that links to it. Over time, this shows you which conversations you actually rely on.

#### Use a Simple Folder for Your Notes

Keep your own notes out of the provider subfolders. A structure like this keeps things clear:

```
Vault
├── Library
│   ├── chatgpt
│   ├── claude
│   └── perplexity
└── Notes
    ├── Pricing decision.md
    └── Q4 planning.md
```

**Takeaway:** Saved chats are your source material. Your notes are where you add meaning, and links tie the two together.

---

### Step 5: Keep Everything on Your Computer

Your saved chats aren't sent to our servers. Obsidian, by default, also works with files on your own drive. A few choices decide whether things stay that way.

- **Community plugins.** Obsidian starts with community plugins turned off, in what it calls Restricted mode. Some plugins connect to the internet. If you turn plugins on, read what each one does before you install it.
- **Sync services.** Obsidian offers an optional paid sync service. If you use it, or put your vault in a cloud-synced folder such as OneDrive, a copy of your files is stored by that service under its own policies.
- **Backups.** A vault is just a folder. Back it up the same way you back up your Library folder, such as copying it to an external drive.

If you want everything local, leave plugins off, skip sync, and keep the vault outside any cloud-synced folder.

**Takeaway:** Obsidian's defaults keep files local. Plugins and sync are choices you make on purpose.

---

### Common Mistakes to Avoid

- **Editing original chats.** Write notes in separate files and link to the chat instead.
- **Moving the Library folder without updating the save path.** New chats keep going to the old location.
- **Opening the same folder as two different vaults.** It works, but settings get confusing. Pick one.
- **Installing plugins without checking them.** Some send data online. Read before you enable.
- **Copying chats and then forgetting which copy is current.** If you use Option C, treat the Library folder as the original.

---

### Common Questions

#### Do I need TotalRecalls open to read chats in Obsidian?

No. Your saved conversations are standard Markdown files. Obsidian reads them whether TotalRecalls is open or not.

#### Will Obsidian change my saved conversation files?

Not unless you edit them. Opening, reading, and searching don't change your files. Obsidian does add a hidden `.obsidian` settings folder to the vault.

#### Can I open chats from every provider in one vault?

Yes. Each provider has its own subfolder, and Obsidian shows them all together. On the Free Tier, that's ChatGPT, Claude, and Perplexity. Pro adds Gemini, Grok, DeepSeek, Mistral, and Qwen.

#### What about the JSON files?

They stay in your Library folder for scripts, tools, or anything that needs structured data. Obsidian hides them by default, so you only see the readable Markdown version.

#### Do I have to use Obsidian?

No. Your files open in Notepad, VS Code, Typora, or any text editor. Obsidian is one good option for reading and linking chats, not a requirement.

#### Does this work on Mac or Linux?

TotalRecalls runs on Windows 10 and 11. macOS and Linux versions are in development.

---

### The Recommendation for Most People

**Start simple.** Open your Library folder as its own vault. You can always reorganize later.

**Read, don't rewrite.** Use reading view for saved chats, and keep the originals unchanged.

**Add your own layer.** Create a `Notes` folder, write short notes about what you decided or learned, and link each one to the conversation behind it.

---

### Your Chats, Connected to Your Thinking

Saving your AI conversations as files means they belong to you. Searching them means you can find them. Opening them in Obsidian means you can build on them, linking one answer to the next and turning scattered chats into notes you'll actually return to.

Open your Library folder in Obsidian, pick one conversation that mattered, and write a short note that links back to it. That's the whole habit.

If you haven't tried TotalRecalls yet, the Free Tier covers ChatGPT, Claude, and Perplexity on Windows 10 and 11. You can save your first conversations in minutes and open them in Obsidian the same day.

**Download free at totalrecalls.app.**

---

_(source: `Blog/TotalRecalls Blog Post 8.md`)_

**Meta title:** How to Back Up Your Saved AI Chats on Windows 10 and 11

**Meta description:** Your saved AI conversations are files on your PC, so you can back them up like any other files. Here are four simple ways to keep them safe on Windows.

---

## How to Back Up Your Saved AI Conversations on Windows

Over the last few posts, your Library folder has become more useful. You can search it, open it in Obsidian, and link chats to your own notes. That also makes it worth protecting.

Saving conversations to your PC means they belong to you. It also means your drive is now the only place they live. If that drive fails, or a folder gets deleted by mistake, those chats go with it. A good backup fixes that.

The good news is that your saved chats are ordinary Markdown and JSON files. You don't need special software to protect them. Windows already has everything you need.

This post shows you how to back up your saved AI conversations on Windows 10 and 11. It takes about seven minutes to read. You'll learn:

- What to back up, and where it lives
- Four backup methods, from a one-time copy to a fully automatic schedule
- How to restore a chat when you need it
- How to choose the right method for how you work

---

### The Short Answer

The whole idea fits in three points:

- **Back up the whole Library folder.** It holds every saved conversation, from every provider, in one place.
- **Keep at least one copy off your PC.** An external drive is the simplest choice. A cloud folder works too.
- **Make it automatic.** File History or a scheduled copy means you never have to remember.

**Takeaway:** Turn on File History with an external drive, include your Library folder, and let Windows handle the rest.

---

### What to Back Up

Everything you need is in one folder. By default, that's:

```
C:\TotalRecalls\Library\
```

Inside, each provider has its own subfolder, and each conversation is saved as a Markdown file and a JSON file:

```
Library
├── chatgpt
│   ├── 2026-09-14-pricing-research.md
│   └── 2026-09-14-pricing-research.json
├── claude
│   ├── 2026-09-18-quarterly-report-draft.md
│   └── 2026-09-18-quarterly-report-draft.json
└── perplexity
    ├── 2026-09-22-laptop-battery-comparison.md
    └── 2026-09-22-laptop-battery-comparison.json
```

On the Free Tier, you'll see folders for ChatGPT, Claude, and Perplexity. Pro adds Gemini, Grok, DeepSeek, Mistral, and Qwen. However many providers you use, backing up the Library folder covers all of them.

#### Keep Both File Types

It's tempting to back up only the Markdown files, since those are the ones you read. Keep the JSON files too. They hold the same conversation in a structured format that's useful for scripts and other tools. They're small, so including them costs almost nothing.

#### Don't Forget Your Own Notes

If you followed Blog 7 and keep notes in an Obsidian vault, back up the vault folder as well. If your Library folder sits inside that vault, one backup covers both.

**Takeaway:** Back up the full Library folder, both file types, and any notes folder that links to it.

---

### Method 1: Copy the Folder to an External Drive

This is the quickest way to make your first backup. It takes a few minutes and needs nothing but a USB drive.

1. Plug in an external drive or USB stick.
2. Open File Explorer and go to `C:\TotalRecalls\`.
3. Right-click the **Library** folder and choose **Copy**.
4. Open your external drive.
5. Create a folder with a clear name, such as `TotalRecalls Backup 2026-10-02`.
6. Open that folder, right-click, and choose **Paste**.

Putting the date in the folder name makes it easy to tell backups apart later.

#### Make a Zip Archive Instead

If you'd rather keep a single file, compress the folder first:

- **Windows 11:** Right-click the Library folder and choose **Compress to ZIP file**.
- **Windows 10:** Right-click the Library folder and choose **Send to → Compressed (zipped) folder**.

Then copy the zip file to your external drive. Remember that Windows can't reliably search inside zip files, so you'll need to extract one before searching it.

**Takeaway:** A manual copy is perfect for a first backup. The downside is that it only protects what you've saved so far.

---

### Method 2: Turn On File History

File History is built into Windows 10 and 11. It copies your files to an external drive on a schedule and keeps older versions, so you can go back to an earlier copy of a file. For most people, this is the best long-term option.

#### On Windows 10

1. Plug in your external drive.
2. Open **Settings → Update & Security → Backup**.
3. Under **Back up using File History**, click **Add a drive** and choose your external drive.
4. Click **More options**.
5. Under **Back up these folders**, click **Add a folder**.
6. Select `C:\TotalRecalls\Library` and click **Choose this folder**.
7. Set **Back up my files** to a schedule that suits you, such as every hour or daily.

#### On Windows 11

File History in Windows 11 lives in Control Panel, and it backs up your Windows libraries rather than any folder you pick. You add your Library folder to a Windows library first, then turn File History on.

**Add your Library folder to a Windows library:**

1. Open File Explorer.
2. In the left-hand panel, right-click an empty area and choose **Show libraries**.
3. Find `C:\TotalRecalls\Library`, right-click it, and choose **Include in library → Documents**.

**Turn on File History:**

1. Plug in your external drive.
2. Search for **File History** in the Start menu and open it.
3. Choose your external drive if it isn't already selected.
4. Click **Turn on**.
5. Open **Advanced settings** to choose how often it saves copies and how long it keeps them.

Your files stay where they are. Including the folder in a library only tells Windows to back it up.

#### A Note on "Windows Backup" in Windows 11

Windows 11 also has an app called **Windows Backup**. It mainly backs up folders like Desktop, Documents, and Pictures to OneDrive. It doesn't cover `C:\TotalRecalls\Library` on its own, so don't rely on it for your saved chats unless you move them into one of those folders.

**Takeaway:** File History runs in the background and keeps older versions. Set it up once and it keeps working.

---

### Method 3: Use a Cloud-Synced Folder

If you already use OneDrive, Dropbox, or Google Drive on your PC, you can keep a copy of your Library folder inside it. The sync app then uploads it for you.

1. Open your cloud folder in File Explorer, such as `C:\Users\YourName\OneDrive`.
2. Create a folder called `TotalRecalls Backup`.
3. Copy your Library folder into it.

You could also move the Library folder into your cloud folder completely. If you do, check whether TotalRecalls lets you choose a save location, and point it at the new path. Otherwise, new chats keep going to the old folder.

#### Think About Privacy First

Your conversations aren't sent to our servers when you save them. A cloud folder is different. Once your chats are inside one, that service stores a copy under its own policies. If some conversations are sensitive, an external drive may be the better choice.

#### Sync Isn't Quite a Backup

Sync copies changes in both directions. If you delete a file on your PC, the sync service usually deletes it in the cloud too. Most services keep deleted files for a limited time, but a separate copy on an external drive gives you a safer fallback.

**Takeaway:** Cloud folders are convenient and protect you if your PC is lost. Weigh the privacy trade-off, and don't treat sync as your only backup.

---

### Method 4: Schedule a Copy with Robocopy

Robocopy is a copy tool built into Windows. It only copies new or changed files, so repeat backups are fast. Pair it with Task Scheduler and it runs automatically. This method suits people who are comfortable with a short command.

#### Create the Backup File

1. Open **Notepad**.
2. Paste this line, changing `E:` to your external drive's letter:

```
robocopy "C:\TotalRecalls\Library" "E:\TotalRecalls Backup\Library" /E /XO /R:1 /W:1
```

3. Choose **File → Save As**.
4. Set **Save as type** to **All files**.
5. Name the file `backup-library.bat` and save it somewhere easy to find, such as `C:\TotalRecalls\`.

Here's what each part does:

| Part                               | What It Does                                                               |
| ---------------------------------- | -------------------------------------------------------------------------- |
| `"C:\TotalRecalls\Library"`        | The folder to copy from                                                    |
| `"E:\TotalRecalls Backup\Library"` | The folder to copy to                                                      |
| `/E`                               | Includes every subfolder, so all providers are covered                     |
| `/XO`                              | Skips files that are already up to date in the backup                      |
| `/R:1 /W:1`                        | Retries a busy file once, after one second, instead of waiting a long time |

Double-click the file to test it. A window opens, lists the copied files, and closes when it's done.

#### Avoid /MIR Unless You Mean It

You may see guides that use `/MIR`. It makes the backup an exact mirror, which means files you delete on your PC are also deleted from the backup. For saved conversations, the safer choice is `/E`, which only adds and updates.

#### Run It on a Schedule

1. Search for **Task Scheduler** in the Start menu and open it.
2. Click **Create Basic Task**.
3. Name it `Back up TotalRecalls Library` and click **Next**.
4. Choose how often to run it, such as **Weekly**, and pick a day and time.
5. Choose **Start a program**.
6. Click **Browse**, select `backup-library.bat`, and click **Finish**.

Make sure the external drive is plugged in at the scheduled time, and that Windows gives it the same drive letter each time.

**Takeaway:** Robocopy plus Task Scheduler gives you a fast, automatic copy with full control over where it goes.

---

### Backup Methods Side by Side

|                                           | **Manual Copy**                        | **File History**                       | **Cloud Folder**                   | **Robocopy + Task Scheduler**          |
| ----------------------------------------- | -------------------------------------- | -------------------------------------- | ---------------------------------- | -------------------------------------- |
| **Setup effort**                          | Lowest                                 | Low                                    | Low                                | Medium                                 |
| **Runs automatically?**                   | No                                     | Yes                                    | Yes                                | Yes                                    |
| **Keeps older versions?**                 | Only if you make dated copies          | Yes                                    | Limited, depends on the service    | No                                     |
| **Protects against a lost or stolen PC?** | Yes, if the drive is stored separately | Yes, if the drive is stored separately | Yes                                | Yes, if the drive is stored separately |
| **Copy stays off the internet?**          | Yes                                    | Yes, with an external drive            | No                                 | Yes, with an external drive            |
| **Needs a drive plugged in?**             | Only while copying                     | Yes, for each backup                   | No                                 | Yes, at the scheduled time             |
| **Best for**                              | A quick first backup                   | Most people                            | People already using cloud storage | People who like control                |

You don't have to pick just one. A strong setup for many people is File History to an external drive, plus an occasional dated zip stored somewhere else.

**Takeaway:** File History is the best default. Add a second copy in a different place if your chats really matter to you.

---

### How to Restore a Saved Chat

A backup is only useful if you can get files back. Try a restore once, so you know it works before you need it.

#### From a Manual Copy or Robocopy Backup

1. Open the backup folder on your external drive.
2. Find the provider subfolder, such as `claude`.
3. Copy the `.md` and `.json` files you need.
4. Paste them back into the same subfolder in `C:\TotalRecalls\Library\`.

#### From File History

1. Plug in the drive File History uses.
2. Open File Explorer and go to `C:\TotalRecalls\Library\`.
3. Right-click the provider subfolder and choose **Properties**.
4. Open the **Previous Versions** tab.
5. Pick a date, then click **Restore** or **Open** to choose specific files.

You can also search for **Restore your files with File History** in the Start menu. It opens a window where you can browse back through dates using the arrow buttons.

#### From a Cloud Folder

Copy the files from your cloud folder back into your Library folder. If a file was deleted, check your cloud service's recycle bin or deleted files page.

**Takeaway:** Restoring is just copying files back to the right provider subfolder. Test it once so you're confident.

---

### Common Mistakes to Avoid

- **Backing up to the same drive.** A copy on `C:` doesn't help if `C:` fails. Use an external drive or the cloud.
- **Leaving the backup drive plugged in all the time.** Unplug it between backups, or at least store it away from your PC, so one problem can't affect both.
- **Using /MIR without thinking.** It deletes backup files when you delete originals.
- **Moving the Library folder without updating the save path.** New chats keep going to the old location and miss the backup.
- **Never testing a restore.** Check once that you can open a backed-up chat.

---

### Common Questions

#### How often should I back up my saved chats?

It depends on how often you save new conversations. If you save chats most days, a daily or hourly File History schedule makes sense. If you save a few a month, a weekly backup is plenty.

#### How much space do I need?

Not much. Markdown and JSON are plain text, so even hundreds of conversations usually take up very little room. A small USB stick is often enough.

#### Do I need TotalRecalls open to back up my chats?

No. Your saved conversations are standard files. Windows can copy and back them up whether TotalRecalls is open or not.

#### Can I open my backups on another PC?

Yes. The files open in Notepad, VS Code, Obsidian, or any text editor. You don't need TotalRecalls installed to read them.

#### Should I encrypt my backup drive?

If your chats contain sensitive information, it's a good idea. BitLocker To Go is built into Windows 10 and 11 Pro, Enterprise, and Education editions. Right-click the drive in File Explorer and look for **Turn on BitLocker**. Windows Home doesn't include it, so you'd need a drive with its own encryption or a third-party tool.

#### Does backing up send my conversations anywhere?

Backing up to an external drive keeps everything on hardware you own. Your conversations aren't sent to our servers when you save them. If you back up to a cloud folder, that service stores a copy under its own policies.

#### Does this work on Mac or Linux?

TotalRecalls runs on Windows 10 and 11. macOS and Linux versions are in development.

---

### The Recommendation for Most People

**Make one copy today.** Copy your Library folder to a USB drive, with the date in the folder name. It takes five minutes.

**Set up File History this week.** Point it at an external drive and include your Library folder. After that, backups happen without you thinking about them.

**Keep a second copy somewhere else.** Every few months, make a dated zip and store it on a different drive or in the cloud.

---

### Your Chats, Kept Safe

Saving your AI conversations as files gives you ownership. Searching and linking them makes them useful. Backing them up makes sure all that work is still there next year, whatever happens to your PC.

Start small. Plug in a drive, copy your Library folder, and open one backed-up chat to check it's readable. Then turn on File History and let Windows do the rest.

If you haven't tried TotalRecalls yet, the Free Tier covers ChatGPT, Claude, and Perplexity on Windows 10 and 11. Pro adds Gemini, Grok, DeepSeek, Mistral, and Qwen. You can save your first conversations in minutes and back them up the same day.

**Download free at totalrecalls.app.**

---

_(source: `Blog/VS Code Blog Post 9.md`)_

**Meta title:** How to Use Your Saved AI Chats in VS Code (Windows)

**Meta description:** Your saved AI conversations are Markdown and JSON files, so VS Code can open, search, and compare them. Here's how to set it up and reuse code from your chats safely.

---

## How to Use Your Saved AI Chats in VS Code

Many AI conversations end with something worth keeping: a script, a SQL query, a config file, or a clear explanation of why a build failed. Inside a chat window, those answers are easy to lose. Saved as files, they become a reference you can search and reuse.

VS Code is a good fit for this job. It's a free code editor from Microsoft, and it handles Markdown and JSON well. Every conversation TotalRecalls saves is a Markdown file with a matching JSON file, so VS Code can open your Library folder exactly as it is, with no conversion or import step.

This post shows you how to use your saved AI chats in VS Code on Windows. It takes about seven minutes to read. You'll learn:

- How to open your Library folder and read chats with a clean preview
- How to search every conversation at once, including by provider or month
- How to compare two answers side by side
- How to explore the JSON version of a chat
- How to move code from a chat into a real project
- A few settings that protect your original files and keep your chats on your PC

---

### The Short Answer

The whole idea fits in three points:

- **Open the Library folder in VS Code.** Every provider subfolder appears in one sidebar.
- **Read with the preview, search with Ctrl + Shift + F.** The preview makes chats easy to read, and search covers every file at once.
- **Treat saved chats as a record, not a draft.** Copy code out into your projects instead of editing the originals.

**Takeaway:** VS Code turns your Library folder into a searchable reference shelf for every answer you've saved.

---

### Why VS Code Works Well with Saved AI Chats

Different tools suit different chats. Obsidian is strong when you want to link conversations to your notes and ideas. VS Code is stronger when your chats are full of code, or when you want to work with the JSON files as well.

Here's what VS Code gives you:

- **Syntax highlighting.** Code blocks inside your chats appear in color, matched to their language.
- **Markdown preview.** Headings, lists, tables, and code blocks render cleanly.
- **Flexible search.** Search all chats, one provider, or one month, with optional pattern matching.
- **Readable JSON.** Format and fold the structured version of each conversation.
- **Built-in compare.** See exactly where two answers differ.
- **Workspaces.** Keep your saved chats and your project open in the same window.

#### How It Compares to Other Options

|                             | **Notepad**    | **Obsidian**          | **VS Code**                    |
| --------------------------- | -------------- | --------------------- | ------------------------------ |
| **Cost**                    | Free, built in | Free for personal use | Free                           |
| **Markdown preview**        | No             | Yes                   | Yes                            |
| **Code highlighting**       | No             | Yes                   | Yes, for many languages        |
| **JSON formatting**         | No             | Not shown by default  | Yes                            |
| **Search across all chats** | No             | Yes                   | Yes, with filters and patterns |
| **Compare two files**       | No             | No                    | Yes, built in                  |
| **Link chats to notes**     | No             | Yes, very well        | Basic                          |
| **Best for**                | Quick reading  | Notes and ideas       | Code and technical chats       |

**Takeaway:** Reach for VS Code when your saved chats are technical. Reach for Obsidian when they're about ideas and decisions. Both read the same files, so you don't have to pick just one.

---

### Before You Start

You need three things:

1. **Some saved conversations.** The Free Tier covers ChatGPT, Claude, and Perplexity. Pro adds Gemini (through Google Takeout), Grok, DeepSeek, Mistral, and Qwen.
2. **VS Code for Windows.** Download it from code.visualstudio.com and run the installer. It works on Windows 10 and 11.
3. **Your Library folder location.** By default, that's:

```
C:\TotalRecalls\Library\
```

If your Library lives somewhere else, use your own path wherever you see `C:\TotalRecalls\Library` in this post.

**Takeaway:** Install VS Code and know where your Library folder is. That's all the setup you need.

---

### Step 1: Open Your Library Folder

1. Open VS Code.
2. Choose **File → Open Folder**, or press **Ctrl + K**, then **Ctrl + O**.
3. Select `C:\TotalRecalls\Library` and click **Select Folder**.

The first time you open a folder, VS Code asks whether you trust the authors of its files. Your Library holds plain text conversations, so either choice works for reading. Choosing **No, I don't trust the authors** opens the folder in Restricted Mode. That's a sensible default here, because it turns off features that could run code automatically, while reading, previewing, and searching still work.

Your provider subfolders now appear in the Explorer panel on the left. Click one to see its conversations.

#### Jump to Any Chat by Name

Press **Ctrl + P** and type part of a filename, such as `pricing`. VS Code lists matching files as you type. Because saved filenames start with a date, typing `2026-09` lists every chat saved in September 2026.

**Takeaway:** Open the Library folder once, and every saved chat is a few keystrokes away.

---

### Step 2: Read Chats with Markdown Preview

Raw Markdown is readable, but the preview is easier on the eyes, especially for long answers with lists and code.

| What You Want                        | Shortcut                 |
| ------------------------------------ | ------------------------ |
| Open the preview in its own tab      | **Ctrl + Shift + V**     |
| Open the preview beside the raw file | **Ctrl + K**, then **V** |

The preview shows headings, lists, tables, and code blocks much as they appeared in the original chat. It's also a safe way to read, because you can't type into the preview. Nothing changes by accident.

#### Use the Outline for Long Chats

Long conversations can be tiring to scroll. Open the **Outline** section at the bottom of the Explorer panel. It lists every heading in the current file, including each message label, so you can jump straight to the part you need.

**Takeaway:** Read in preview, and use the Outline to move around long conversations.

---

### Step 3: Search Every Conversation at Once

Press **Ctrl + Shift + F** to open search. Type a word or phrase, and VS Code lists every match across every provider, grouped by file. Click any result to jump to that line.

To narrow your search, click the three dots under the search box. That reveals two fields: **files to include** and **files to exclude**.

| What You Want                    | What to Enter                      |
| -------------------------------- | ---------------------------------- |
| Search Claude chats only         | Files to include: `claude/**`      |
| Search Markdown files only       | Files to include: `*.md`           |
| Search chats from September 2026 | Files to include: `*2026-09*`      |
| Skip the JSON files              | Files to exclude: `*.json`         |
| Match exact capital letters      | Click **Aa**, or press **Alt + C** |
| Match whole words only           | Click **ab**, or press **Alt + W** |

Excluding `*.json` is worth doing most of the time. Each conversation exists in both formats, so without it, you'll see every match twice.

#### Find Answers by Their Shape

Sometimes you remember what an answer looked like, but not its exact words. Turn on pattern matching by clicking **.\***, or pressing **Alt + R**. A few useful patterns:

| Pattern          | What It Finds                        |
| ---------------- | ------------------------------------ |
| `^```python`     | The start of every Python code block |
| `def \w+\(`      | Python function definitions          |
| `SELECT .* FROM` | SQL queries                          |
| `https?://\S+`   | Links mentioned in your chats        |

You don't need to learn patterns to use VS Code well. Plain words work for most searches. Patterns simply help when the shape of an answer is easier to recall than its wording.

**Takeaway:** Plain search finds words. "Files to include" narrows it to one provider or month. Patterns find code by its shape.

---

### Step 4: Compare Two Answers Side by Side

If you asked ChatGPT and Claude the same question, VS Code can show you exactly how their answers differ.

1. In the Explorer panel, right-click the first file and choose **Select for Compare**.
2. Right-click the second file and choose **Compare with Selected**.

VS Code opens both files side by side, with changed lines highlighted. Use the arrows at the top of the compare view to step from one difference to the next.

This also works for two versions of the same conversation. If you saved a chat again after it grew, comparing the two files shows exactly what was added.

**Takeaway:** Built-in compare makes it easy to see how two providers, or two versions of one chat, answered differently.

---

### Step 5: Look Inside the JSON Files

The Markdown file is for reading. The JSON file holds the same conversation in a structured format, with labeled fields for details like the title, provider, and each message. That's useful if you ever want to write scripts or build tools on top of your chats.

To make a JSON file easier to read:

1. Open the `.json` file.
2. Press **Shift + Alt + F** to format it neatly, if it isn't already.
3. Use the small arrows beside the line numbers to fold and unfold sections, such as the full list of messages.

VS Code also adds color to field names and values, which makes the structure easier to follow.

Take a few minutes to see how the data is laid out before writing anything that depends on it. Field details can vary between providers, so check one file from each provider you use. If you only plan to read your chats, you can ignore the JSON files completely.

**Takeaway:** You don't need the JSON files to read your chats, but VS Code makes them easy to explore when you want structured data.

---

### Step 6: Move Code from a Chat into a Project

This is where saved chats pay off. Instead of scrolling through an old chat window, you can find the code you need in seconds and bring it into your work.

#### Use a Workspace with Two Folders

A workspace lets you open your Library folder and a project folder in the same window.

1. Open your project folder in VS Code.
2. Choose **File → Add Folder to Workspace** and select `C:\TotalRecalls\Library`.
3. Choose **File → Save Workspace As** and save the workspace file outside the Library folder, such as in your Documents folder or your project folder.

Both folders now appear in the sidebar. Search covers both at once, and you can drag a saved chat into a split view beside the file you're working on.

#### Copy, Then Make It Your Own

1. Find the code block in the saved chat.
2. Select it and copy it with **Ctrl + C**.
3. Paste it into a new or existing file in your project.
4. Read it carefully, test it, and adjust it to fit your project.

AI-written code can contain mistakes, outdated methods, or assumptions that don't match your setup. Treat it as a starting point you review, not a finished answer.

#### Leave a Pointer Back to the Source

Add a short comment above the pasted code so you know where it came from:

```
## Based on Claude chat: claude/2026-09-18-quarterly-report-draft.md
```

Months later, you can open the original conversation and read the full reasoning behind the code, including any warnings or alternatives the AI mentioned.

**Takeaway:** Keep chats and projects in one workspace. Copy code out, test it, and note which chat it came from.

---

### Step 7: Protect Your Originals and Keep Things Local

#### Make the Library Read-Only in VS Code

Your saved chats are a record of what was said. You can tell VS Code to block edits to them.

1. Press **Ctrl + Shift + P** to open the Command Palette.
2. Type **Preferences: Open Workspace Settings (JSON)** and press Enter.
3. Add this setting:

```
"files.readonlyInclude": {
  "C:/TotalRecalls/Library/**": true
}
```

Use forward slashes in the path, even on Windows. If you saved a workspace file in Step 6, this setting lives in that file, so nothing new gets added inside your Library folder.

For a quick one-off, you can also run **File: Set Active Editor Read-only in Session** from the Command Palette. It locks just the file you have open, until you close VS Code.

#### Decide What Leaves Your PC

Your saved conversations aren't sent to our servers. VS Code itself works with files on your own drive, but some of its features can connect to the internet. It's worth knowing which ones:

- **AI assistants.** Built-in chat features and extensions such as GitHub Copilot can send file contents to their service when you use them. Keep them away from conversations you consider private.
- **Extensions.** Some extensions connect online. Read what each one does before installing it.
- **Telemetry.** VS Code sends usage data to Microsoft by default. To turn it off, open **Settings** with **Ctrl + ,**, search for `telemetry`, and set **Telemetry Level** to **off**.
- **Settings Sync.** If you turn it on, your editor settings sync to your account. Your chat files don't sync, but your settings, including any paths you've added, may.

**Takeaway:** Lock your saved chats as read-only, and choose on purpose which online features you use with them.

---

### Common Mistakes to Avoid

- **Editing original chats.** Copy code out instead, so your saved record stays accurate.
- **Saving the workspace file inside the Library folder.** Keep it in Documents or your project folder, so your Library holds only saved chats.
- **Pasting AI code without testing it.** Read it, run it, and check it fits your project before you rely on it.
- **Using AI assistants on private chats.** These tools may send file contents online when you use them.
- **Searching JSON and Markdown together.** You'll see every match twice. Exclude `*.json` when you only want readable results.
- **Installing extensions without checking them.** Fewer, well-understood extensions keep your setup simple and predictable.

---

### Common Questions

#### Do I need TotalRecalls open to use my chats in VS Code?

No. Your saved conversations are standard Markdown and JSON files. VS Code reads them whether TotalRecalls is open or not.

#### Will VS Code change my saved files?

Not unless you edit a file and save it. Reading, previewing, searching, and comparing don't change anything. The read-only setting adds an extra layer of protection.

#### Can I use VS Code and Obsidian on the same folder?

Yes. They read the same files. Many people use Obsidian for notes and idea-heavy chats, and VS Code for code-heavy ones.

#### Does Restricted Mode limit what I can do?

For reading and searching, no. Restricted Mode mainly turns off features and extensions that could run code from the folder. Markdown preview, search, and compare all still work.

#### Is VS Code hard to learn?

Not for this. Opening a folder, reading, searching, and comparing use the handful of shortcuts covered above. You can safely ignore everything else.

#### Does this work on Mac or Linux?

TotalRecalls runs on Windows 10 and 11. macOS and Linux versions are in development.

---

### The Recommendation for Most People

**Open the folder and search.** Start with **Ctrl + Shift + F**, and exclude `*.json`. It's the fastest way to find an answer you've already saved.

**Read in preview.** **Ctrl + Shift + V** keeps chats readable and safe from accidental edits.

**Build one workspace.** Pair your Library folder with the project you work on most. Copy code out as you need it, test it, and leave a pointer back to the source chat.

---

### Your Saved Answers, Ready to Reuse

Saving your AI conversations as files means they belong to you. Searching, organizing, and backing them up keeps them useful and safe. Opening them in VS Code puts the code and fixes you've already asked for right beside the work you're doing now.

Open your Library folder in VS Code, search for one problem you solved with AI last month, and see how quickly the answer comes back.

If you haven't tried TotalRecalls yet, the Free Tier covers ChatGPT, Claude, and Perplexity on Windows 10 and 11. You can save your first conversations in a few minutes and open them in VS Code the same day.

**Download free at totalrecalls.app.**

---

_(source: `Blog/TotalRecalls Blog Post 10.md`)_

**Meta title:** How to Manage Your Saved AI Chats with PowerShell (Windows)

**Meta description:** Your saved AI conversations are plain files, so PowerShell can count, search, check, and index them. Here are safe, copy-and-paste commands for Windows 10 and 11.

---

## How to Manage Your Saved AI Chats with PowerShell

Over the last few posts, your Library folder has grown into something useful. You can search it, read it in Obsidian, work with it in VS Code, and back it up. As it grows, a new set of questions appears. How many chats have you saved? Which ones came from Claude last month? Is every Markdown file paired with its JSON file?

You could answer those by clicking through folders. PowerShell answers them in seconds.

PowerShell is a command tool that comes with Windows 10 and 11. You don't need to install anything, and you don't need to be a programmer. You type a command, press Enter, and read the result. Your saved chats are ordinary files, so PowerShell can work with them directly.

This post shows you how to manage your saved AI conversations with PowerShell on Windows. It takes about eight minutes to read. You'll learn:

- How to open PowerShell in your Library folder
- How to count, list, and find chats by provider or date
- How to search inside every conversation at once
- How to check your Library for missing or duplicate files
- How to build a simple index you can open in Excel, and refresh it on a schedule

---

### The Short Answer

The whole idea fits in three points:

- **PowerShell is already on your PC.** Open it, point it at your Library folder, and start with simple commands.
- **Most useful commands only read.** Counting, listing, searching, and checking don't change your files.
- **Save what you use often as a script.** A short script can build an index of every chat, and Task Scheduler can run it for you.

**Takeaway:** Start by typing one command at a time. Turn the ones you like into a script later.

---

### Which Tool for Which Job

PowerShell doesn't replace the tools from earlier posts. It fills a different gap.

| Task                           | **File Explorer** | **Obsidian** | **VS Code** | **PowerShell**           |
| ------------------------------ | ----------------- | ------------ | ----------- | ------------------------ |
| **Read one chat**              | Good              | Best         | Good        | Not ideal                |
| **Search for a phrase**        | Good              | Good         | Very good   | Very good                |
| **Link chats to notes**        | No                | Best         | Basic       | No                       |
| **Count chats by provider**    | Manual            | No           | No          | Best                     |
| **Check for missing files**    | Manual            | No           | No          | Best                     |
| **Build a list of every chat** | No                | No           | No          | Best                     |
| **Run on a schedule**          | No                | No           | No          | Yes, with Task Scheduler |

**Takeaway:** Use PowerShell for questions about your whole Library, not for reading individual chats.

---

### Before You Start

You need three things:

1. **Some saved conversations.** The Free Tier covers ChatGPT, Claude, and Perplexity. Pro adds Gemini, Grok, DeepSeek, Mistral, and Qwen.
2. **Windows PowerShell.** It's built into Windows 10 and 11. Every command in this post also works in PowerShell 7 if you've installed it.
3. **Your Library folder location.** By default, that's:

```
C:\TotalRecalls\Library\
```

If your Library lives somewhere else, swap in your own path wherever you see `C:\TotalRecalls\Library`.

#### A Safe Habit Before You Begin

Make a backup first. If you followed Blog 8, you already have one. Almost every command here only reads files, but a fresh backup means you can experiment without worry.

**Takeaway:** Nothing to install. Just know your folder path and have a backup in place.

---

### Step 1: Open PowerShell in Your Library Folder

There are a few ways to open PowerShell. Pick whichever feels easiest.

| Method                     | How                                                                                             |
| -------------------------- | ----------------------------------------------------------------------------------------------- |
| **Start menu**             | Search for **PowerShell** and open **Windows PowerShell**                                       |
| **Windows 11 Terminal**    | Right-click the Start button and choose **Terminal**                                            |
| **From the folder itself** | Open the Library folder in File Explorer, type `powershell` in the address bar, and press Enter |
| **Windows 11 right-click** | Right-click inside the Library folder and choose **Open in Terminal**                           |

If you opened PowerShell from the Start menu, move into your Library folder with this command:

```
Set-Location "C:\TotalRecalls\Library"
```

The line before your cursor should now end with `C:\TotalRecalls\Library>`. That tells you where PowerShell is working.

You don't need to run PowerShell as an administrator for anything in this post. A normal window is safer.

**Takeaway:** Open PowerShell, move into your Library folder, and you're ready.

---

### Step 2: Count and List Your Saved Chats

Start with simple questions. Each command below only reads your files.

#### How Many Chats Have You Saved?

Each conversation has one Markdown file, so counting `.md` files counts your chats:

```
(Get-ChildItem -Recurse -Filter *.md).Count
```

`-Recurse` tells PowerShell to look inside every provider subfolder.

#### How Many from Each Provider?

```
Get-ChildItem -Directory | ForEach-Object {
  [PSCustomObject]@{
    Provider = $_.Name
    Chats    = (Get-ChildItem $_.FullName -Filter *.md).Count
  }
}
```

You'll see a small table, something like this:

```
Provider   Chats
--------   -----
chatgpt       42
claude        27
perplexity    11
```

#### Your Most Recent Chats

Filenames start with a date, so sorting by name puts them in date order:

```
Get-ChildItem -Recurse -Filter *.md |
  Sort-Object Name -Descending |
  Select-Object -First 10 Name, @{Name='Provider'; Expression={$_.Directory.Name}}
```

#### Chats from a Specific Month

```
Get-ChildItem -Recurse -Filter "2026-09-*.md"
```

Change `2026-09` to any year and month you want.

#### How Much Space Your Library Uses

```
"{0:N1} MB" -f ((Get-ChildItem -Recurse -File | Measure-Object Length -Sum).Sum / 1MB)
```

For most people, the answer is surprisingly small, because Markdown and JSON are plain text.

#### Quick Reference

| Question                       | Command                                                                  |
| ------------------------------ | ------------------------------------------------------------------------ |
| Total chats                    | `(Get-ChildItem -Recurse -Filter *.md).Count`                            |
| Claude chats only              | `(Get-ChildItem .\claude -Filter *.md).Count`                            |
| Chats from one month           | `Get-ChildItem -Recurse -Filter "2026-09-*.md"`                          |
| Chats with a word in the title | `Get-ChildItem -Recurse -Filter "*pricing*.md"`                          |
| Library size                   | `(Get-ChildItem -Recurse -File \| Measure-Object Length -Sum).Sum / 1MB` |

**Takeaway:** A handful of short commands tells you more about your Library than an hour of clicking.

---

### Step 3: Search Inside Every Conversation

`Select-String` searches the text inside files. Think of it as Find for your whole Library.

#### Search for a Word or Phrase

```
Get-ChildItem -Recurse -Filter *.md |
  Select-String -Pattern "renewal rate" -SimpleMatch
```

Each result shows the file, the line number, and the line itself. `-SimpleMatch` means PowerShell searches for exactly what you typed, so symbols like `.` or `?` don't cause surprises.

#### List Each Matching Chat Once

A long chat might mention a word dozens of times. To see each file only once:

```
Get-ChildItem -Recurse -Filter *.md |
  Select-String -Pattern "budget" -SimpleMatch -List |
  Select-Object Filename, LineNumber
```

#### Search One Provider

```
Select-String -Path ".\claude\*.md" -Pattern "budget" -SimpleMatch -List
```

#### Open the Matches in Notepad

Once you've found what you need, open the matching chats directly:

```
Get-ChildItem -Recurse -Filter *.md |
  Select-String -Pattern "invoice template" -SimpleMatch -List |
  ForEach-Object { notepad $_.Path }
```

Use a specific phrase here. A common word could open dozens of Notepad windows at once.

#### Search Options at a Glance

| What You Want                          | Add This                                           |
| -------------------------------------- | -------------------------------------------------- |
| Exact text, no pattern matching        | `-SimpleMatch`                                     |
| One result per file                    | `-List`                                            |
| Match exact capital letters            | `-CaseSensitive`                                   |
| Show lines around each match           | `-Context 1,2` (1 line before, 2 after)            |
| Find files that don't contain the word | `-NotMatch` (works line by line, so use with care) |

PowerShell ignores capital letters by default, so `Budget` and `budget` both match.

If accented letters or symbols look garbled in your results, add `-Encoding UTF8` to the `Select-String` command.

**Takeaway:** `Select-String` with `-SimpleMatch -List` is the fastest way to find which chats mention something.

---

### Step 4: Check Your Library for Problems

As your Library grows, small problems can creep in. A file gets moved, or a chat gets saved twice. These checks find them. None of them change anything.

#### Find Markdown Files Without a JSON Partner

```
Get-ChildItem -Recurse -Filter *.md | Where-Object {
  -not (Test-Path ($_.FullName -replace '\.md$', '.json'))
} | Select-Object FullName
```

If nothing appears, every chat has both files. You can reverse the check by swapping `.md` and `.json`.

#### Find Exact Duplicates

This compares file contents, not names, so it catches copies with different filenames:

```
Get-ChildItem -Recurse -Filter *.md |
  Get-FileHash |
  Group-Object Hash |
  Where-Object Count -gt 1 |
  ForEach-Object { $_.Group.Path; "" }
```

Each group of paths is a set of identical files, with a blank line between groups.

#### Find Empty or Very Small Files

```
Get-ChildItem -Recurse -File | Where-Object Length -lt 200 |
  Select-Object FullName, Length
```

A very small file may point to a download that didn't finish. Open it in Notepad to check, then save that conversation again in TotalRecalls if needed.

#### Find Stray Files

```
Get-ChildItem -Recurse -File |
  Where-Object { $_.Extension -notin '.md', '.json' } |
  Select-Object FullName
```

This lists anything that isn't a saved chat, such as a note you dropped in by mistake. Obsidian's hidden `.obsidian` folder won't appear unless you add `-Force`.

#### If You Decide to Remove Something

Delete files in File Explorer, so they go to the Recycle Bin. If you ever use `Remove-Item` in PowerShell, add `-WhatIf` first. It shows what would happen without doing it:

```
Remove-Item ".\chatgpt\2026-09-14-pricing-research-copy.md" -WhatIf
```

Files deleted with `Remove-Item` skip the Recycle Bin.

**Takeaway:** Run these checks every few months. They take seconds and keep your Library tidy.

---

### Step 5: Peek Inside a JSON File

The JSON file holds the same conversation as the Markdown file, in a structured format. PowerShell can read it as data.

```
$chat = Get-Content ".\chatgpt\2026-09-14-pricing-research.json" -Raw -Encoding UTF8 |
  ConvertFrom-Json
```

Nothing appears yet, because the result is stored in `$chat`. To see the top-level fields:

```
$chat | Get-Member -MemberType NoteProperty
```

To see the structure in a readable layout:

```
$chat | ConvertTo-Json -Depth 4 | more
```

Press the spacebar to page through, or **Q** to stop.

Take a few minutes to look at how the data is laid out before you write anything that depends on it. Field names may differ between providers, so check one file from each provider you use. If you only want lists, counts, and searches, the Markdown files are all you need.

**Takeaway:** `ConvertFrom-Json` turns a saved chat into data you can explore. Look before you build.

---

### Step 6: Build an Index of Every Chat

This is where PowerShell earns its place. A short script can create a spreadsheet listing every saved conversation, with its date, provider, and title.

#### Create the Script

1. Create a folder for your scripts, such as `C:\Users\YourName\Documents\Scripts`.
2. Open **Notepad** and paste this:

```
$library = "C:\TotalRecalls\Library"
$output  = "$env:USERPROFILE\Documents\TotalRecalls-index.csv"

Get-ChildItem -Path $library -Recurse -Filter *.md |
  ForEach-Object {
    $date  = ""
    $title = $_.BaseName
    if ($_.BaseName -match '^(\d{4}-\d{2}-\d{2})-(.+)$') {
      $date  = $Matches[1]
      $title = $Matches[2] -replace '-', ' '
    }
    [PSCustomObject]@{
      Date     = $date
      Provider = $_.Directory.Name
      Title    = $title
      SizeKB   = [math]::Round($_.Length / 1KB, 1)
      Path     = $_.FullName
    }
  } |
  Sort-Object Date -Descending |
  Export-Csv -Path $output -NoTypeInformation -Encoding UTF8
```

3. Choose **File → Save As**.
4. Set **Save as type** to **All files**.
5. Name it `build-index.ps1` and save it in your Scripts folder.

The script saves the index in your Documents folder, not inside the Library. That keeps your Library holding only saved chats.

#### What Each Part Does

| Part                                  | What It Does                                          |
| ------------------------------------- | ----------------------------------------------------- |
| `$library` and `$output`              | Where to read chats from, and where to save the index |
| `Get-ChildItem ... -Filter *.md`      | Finds every saved chat across all providers           |
| `-match '^(\d{4}-\d{2}-\d{2})-(.+)$'` | Splits a filename into its date and title             |
| `-replace '-', ' '`                   | Turns `pricing-research` into `pricing research`      |
| `[PSCustomObject]@{ ... }`            | Builds one row per chat                               |
| `Sort-Object Date -Descending`        | Puts the newest chats first                           |
| `Export-Csv ... -Encoding UTF8`       | Saves a file Excel can open, with characters intact   |

#### Run the Script

Windows blocks scripts by default on most PCs. The simplest way to run this one without changing any settings:

```
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\Documents\Scripts\build-index.ps1"
```

This allows the script for this one run only.

If you plan to run your own scripts often, you can allow them for your user account instead:

```
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

After that, you can run the script by typing its path. `RemoteSigned` still blocks unsigned scripts downloaded from the internet, which is a sensible middle ground.

#### Open the Index

Double-click `TotalRecalls-index.csv` in your Documents folder. It opens in Excel, or in any spreadsheet app. You can sort by provider, filter by month, or search titles. Copy a path from the **Path** column into File Explorer's address bar to open that chat.

**Takeaway:** One short script gives you a sortable list of every conversation you've saved.

---

### Step 7: Refresh the Index on a Schedule

Your index only knows about chats that existed when it ran. Task Scheduler can rerun it for you.

1. Search for **Task Scheduler** in the Start menu and open it.
2. Click **Create Basic Task**.
3. Name it `Refresh TotalRecalls index` and click **Next**.
4. Choose how often to run it, such as **Weekly**, and pick a day and time.
5. Choose **Start a program** and click **Next**.
6. In **Program/script**, type:

```
powershell.exe
```

7. In **Add arguments**, type this, with your own username:

```
-NoProfile -ExecutionPolicy Bypass -File "C:\Users\YourName\Documents\Scripts\build-index.ps1"
```

8. Click **Next**, then **Finish**.

To test it, find the task in the Task Scheduler Library, right-click it, and choose **Run**. Check that the date on `TotalRecalls-index.csv` has updated.

If the CSV is open in Excel when the task runs, the update will fail. Close it first, or schedule the task for a time you're usually away.

**Takeaway:** Schedule the index once, and it stays current without you thinking about it.

---

### Common Mistakes to Avoid

- **Running PowerShell as administrator when you don't need to.** A normal window is enough for everything here, and it's safer.
- **Using `Remove-Item` without `-WhatIf`.** Deleted files skip the Recycle Bin. Delete in File Explorer instead.
- **Saving scripts or the index inside the Library folder.** Keep them in Documents, so your Library holds only saved chats.
- **Forgetting to save as "All files" in Notepad.** Otherwise your script becomes `build-index.ps1.txt` and won't run.
- **Assuming every JSON file looks the same.** Check one from each provider before building anything on top of them.
- **Copying scripts from the internet without reading them.** Only run commands you understand, especially ones that move or delete files.

---

### Common Questions

#### Do I need to install anything?

No. Windows PowerShell comes with Windows 10 and 11. Every command here also works in PowerShell 7 if you prefer it.

#### Will these commands change my saved chats?

The counting, listing, searching, checking, and JSON commands only read files. The index script creates one new file in your Documents folder and leaves your Library unchanged.

#### Do I need TotalRecalls open?

No. Your saved conversations are standard files. PowerShell works with them whether TotalRecalls is open or not.

#### What is the execution policy?

It's a Windows setting that controls whether scripts can run. It's there to prevent scripts from running by accident. Typing commands one at a time isn't affected. Only saved `.ps1` files are.

#### Does PowerShell send my chats anywhere?

The commands in this post work entirely on your PC. Your saved conversations aren't sent to our servers, and nothing here uploads them anywhere.

#### Is this hard if I've never used a command line?

Not for these tasks. Copy a command, paste it with a right-click or **Ctrl + V**, press Enter, and read the result. If something goes wrong, PowerShell shows a red error message and your files stay as they were.

#### Does this work on Mac or Linux?

TotalRecalls runs on Windows 10 and 11. macOS and Linux versions are in development.

---

### The Recommendation for Most People

**Try three commands today.** Count your chats, count them by provider, and search for one phrase with `Select-String`. That's enough to see what PowerShell can do.

**Run the checks every few months.** Missing pairs, duplicates, and tiny files take seconds to find.

**Build the index once, then schedule it.** A weekly refresh gives you a current list of every conversation, ready to sort and filter in Excel.

---

### Your Library, Seen All at Once

Saving your AI conversations as files means they belong to you. Searching, linking, reusing, and backing them up keeps them useful and safe. PowerShell adds one more thing: a clear view of everything you've saved, in a few lines of text.

Open PowerShell in your Library folder, type `(Get-ChildItem -Recurse -Filter *.md).Count`, and press Enter. The number you see is your personal archive of AI answers, kept on your own drive.

If you haven't tried TotalRecalls yet, the Free Tier covers ChatGPT, Claude, and Perplexity on Windows 10 and 11. Pro adds Gemini, Grok, DeepSeek, Mistral, and Qwen. You can save your first conversations in minutes and start organizing them with PowerShell the same day.

**Download free at totalrecalls.app.**

---

_(source: `Blog/Markdown vs JSON Explainer Blog.md`)_

**Meta title:** Markdown vs JSON: Which Saved Chat File to Use

**Meta description:** TotalRecalls saves every AI conversation as a .md and a .json file. Here's what each one is for, and which one most people should open first.

---

## Markdown vs JSON: Which Saved File Should You Use?

Every conversation you download with TotalRecalls arrives as two files with the same name. One ends in `.md`, and the other ends in `.json`. If you've opened your Library folder and wondered why there are two, or which one to use, this post explains it.

This Markdown vs JSON guide takes about five minutes to read. It covers what each format is, what it's good for, and where it falls short. It ends with a simple recommendation for most people.

---

### The Short Answer

If you only remember one thing, make it this:

- **Markdown (`.md`) is for people.** Open it when you want to read, copy, or share a conversation.
- **JSON (`.json`) is for software.** Use it when a tool, script, or app needs to work with your conversations.

Both files hold the same conversation. They store it in two different shapes, for two different jobs.

**Takeaway:** If you're reading, open the `.md` file. If a program is reading, give it the `.json` file.

---

### Why TotalRecalls Saves Two Files

People save AI conversations for different reasons. Some want to reread a useful answer next month. Others want to load hundreds of chats into a personal database. One format can't serve both jobs well.

Markdown is easy to read but loose in structure. JSON is precise in structure but tiring to read. Saving both means you don't have to choose up front. You can decide later, once you know how you'll use your files.

Both files sit side by side in your Library folder, inside each provider's subfolder:

```
claude
├── quarterly-report-draft.md
└── quarterly-report-draft.json
```

**Takeaway:** Two files means you keep your options open, at very little cost in disk space.

---

### What Markdown Is

Markdown is plain text with a few simple marks for structure. A `#` at the start of a line makes a heading. Two asterisks around a word make it **bold**. Everything else is ordinary writing.

It was designed to be readable even before any app formats it. You can open a Markdown file in Notepad and follow it without any trouble.

#### What a Saved Markdown File Looks Like

Here's a simplified example of a saved conversation:

```
## Quarterly report draft

**Provider:** Claude
**Saved:** 2026-10-02

---

### You

Can you help me tighten the opening paragraph of my quarterly report?

### Claude

Here's a shorter version that leads with the main result:

Revenue grew 12% this quarter, driven by stronger renewals.
```

Your files may differ slightly in layout. The idea stays the same: each message is labeled, in order, as readable text.

#### When to Use Markdown

**Rereading a conversation.** Open the file and scroll. Headings separate each message, so finding your place is easy.

**Copying part of a chat.** Select the text you want and paste it into an email, a document, or a message. There's no extra formatting to clean up.

**Keeping notes in a note-taking app.** Many note apps open or import Markdown files directly. Your AI conversations can sit right next to your other notes, in a format those apps already understand.

**Sharing with someone else.** Send a single `.md` file to a coworker. They can open it with Notepad or any text editor, without installing anything new.

#### Where Markdown Falls Short

Markdown is loose by design. A program can't always tell where one message ends and the next begins, or which details describe the conversation itself. That's fine for reading, but it makes Markdown a weaker choice for automated work.

**Takeaway:** Markdown is the format to open when a person is doing the reading.

---

### What JSON Is

JSON stands for JavaScript Object Notation. Despite the name, it isn't tied to one programming language. It's a widely used format for storing structured data, and nearly every modern programming language and many apps can read it.

JSON organizes information into labeled fields. Each piece of information has a name and a value. Lists of items, like the messages in a conversation, sit inside square brackets.

#### What a Saved JSON File Looks Like

Here's a simplified version of the same conversation:

```
{
  "title": "Quarterly report draft",
  "provider": "claude",
  "saved_at": "2026-10-02T09:14:00Z",
  "messages": [
    {
      "role": "user",
      "content": "Can you help me tighten the opening paragraph of my quarterly report?"
    },
    {
      "role": "assistant",
      "content": "Here's a shorter version that leads with the main result..."
    }
  ]
}
```

The exact fields in your files may vary. The shape is consistent, though: details about the conversation at the top, then each message in order, labeled by who sent it.

#### When to Use JSON

**Feeding conversations into other tools.** Some apps and personal databases accept JSON imports. Because every field is labeled, the tool can tell titles, dates, and messages apart.

**Working with scripts.** If you write code, even a short script, JSON is far easier to process than Markdown. A few lines can loop through a folder of conversations and pull out every message you sent, for example.

**Keeping a structured record.** JSON keeps each conversation's details in predictable places. That helps if you ever want to sort, filter, or count conversations by provider or date.

**Converting to other formats later.** Structured data is easier to reshape. If a new tool appears that needs a different format, starting from JSON usually makes the conversion simpler.

#### Where JSON Falls Short

JSON is hard on the eyes. Quotes, brackets, and commas surround every value, and long messages can run across a single very long line. It's also strict. A missing comma or bracket can stop a program from reading the file at all.

If you want to look inside a JSON file, an editor like VS Code adds color and lets you fold sections. Microsoft Edge can also display JSON in a tidier layout.

**Takeaway:** JSON is the format to use when a program is doing the reading.

---

### Markdown vs JSON Side by Side

|                        | **Markdown (`.md`)**               | **JSON (`.json`)**                            |
| ---------------------- | ---------------------------------- | --------------------------------------------- |
| **Best for**           | People reading                     | Software processing                           |
| **Readability**        | Easy to read as is                 | Hard to read without a good editor            |
| **Structure**          | Loose, based on headings           | Strict, with labeled fields                   |
| **Copying text**       | Clean and quick                    | Awkward, with quotes and brackets around text |
| **Note-taking apps**   | Often opened or imported directly  | Rarely used directly                          |
| **Scripts and tools**  | Harder to process reliably         | Easy to process                               |
| **Editing by hand**    | Safe and simple                    | Easy to break by accident                     |
| **Opens with**         | Notepad, VS Code, note-taking apps | Notepad, VS Code, Microsoft Edge              |
| **Same conversation?** | Yes                                | Yes                                           |

---

### Which File to Use for Common Tasks

| What You Want to Do                      | Use This File |
| ---------------------------------------- | ------------- |
| Reread an old conversation               | `.md`         |
| Copy an answer into an email or document | `.md`         |
| Add a chat to your notes                 | `.md`         |
| Send one conversation to a coworker      | `.md`         |
| Import conversations into another tool   | `.json`       |
| Run a script across many conversations   | `.json`       |
| Sort or filter chats by date or provider | `.json`       |
| Back up your conversation history        | Both          |

**Takeaway:** Most everyday tasks point to Markdown. Most technical tasks point to JSON. Backups should include both.

---

### Common Questions

#### Can I delete one of the two files?

You can, but there's little reason to. Both files are small, and keeping the pair means you won't need to download the conversation again if your needs change. If you want a tidier folder for reading, copy the `.md` files into a separate folder instead of deleting the originals.

#### Is it safe to edit the files?

Editing a Markdown file is low risk, since it's just text. Editing JSON by hand is riskier, because one misplaced character can make the file unreadable to software. Either way, work on a copy and leave the originals in your Library folder as they are.

#### Do I need TotalRecalls to open these files?

No. Both are standard formats. Once a conversation is saved, you can open either file with tools already on your PC, without TotalRecalls and without an internet connection.

#### Does every provider save both formats?

Yes. Every supported provider saves the same pair of files, whether you're on the Free Tier or Pro. That includes Gemini on Pro, which works through a Google Takeout file and ends up as the same Markdown and JSON files as every other provider.

---

### The Recommendation for Most People

**Start with Markdown.** Open the `.md` file whenever you want to read, copy, or share a conversation. For most people, that covers nearly everything they'll do with their saved chats.

**Keep the JSON file anyway.** You may never open it, and that's fine. It takes up very little space, and it's there if you later want to import your conversations into a new tool or work with them in bulk.

**Back up both.** When you copy your Library folder to an external drive or another backup location, take the whole folder. That way you keep a readable version and a structured version of everything you've saved.

---

### Two Files, Two Jobs

Markdown and JSON aren't competing formats. They're two copies of the same conversation, each shaped for a different reader. Markdown suits you, and JSON suits your software.

For the next conversation you save, open the `.md` file first. If you ever need the structured version, the `.json` file will be right beside it.

If you haven't tried TotalRecalls yet, the Free Tier covers ChatGPT, Claude, and Perplexity. You can save your first conversation and open both files yourself in a few minutes.

**Download free at totalrecalls.app.**

---
