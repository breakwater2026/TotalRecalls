# TotalRecalls Master Implementation Plan V3

**Status:** Current operating document. Replaces the previous "TotalRecalls Master Implementation Plan."\
**Status date:** October 3, 2026\
**Key update:** The 9-post blog series is now partly written. Blogs 3, 4, 5, and 9 are complete as standalone assets. Blogs 6, 7, and 8 are still pending.\
**Built for:** A founder-led team that records, writes, and publishes in small batches.

TotalRecalls makes one promise: **your AI conversations, saved to your own PC as Markdown and JSON files.** This plan shows how the website, guides, blog, YouTube channel, social posts, and email support that promise. It covers what's done, what's left, and the order for the remaining work.

---

## Status Legend

These markers are used throughout the plan:

| Marker           | Meaning                                                              |
| ---------------- | -------------------------------------------------------------------- |
| ✅ **Complete**   | Written or built as a final asset                                    |
| 🔄 **In review** | Written, but waiting on an accuracy check or a fix before publishing |
| ⏳ **Pending**    | Not yet started or not yet written                                   |
| 🔍 **Confirm**   | Status or detail needs to be checked before work continues           |

---

## 1. How to Use This Plan

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

## 2. Finalized Decisions

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

## 3. Core Message Rules

### One Job Per Asset

Each page, guide, blog post, and video has one clear job. If two assets do the same job, merge them. This is why the spotlight series was cancelled, and why each blog post covers one topic that no guide already handles.

### Call-to-Action Hierarchy

| Priority | Action                                  | Where It Appears                                          |
| -------- | --------------------------------------- | --------------------------------------------------------- |
| **1**    | **Download free**                       | Every page, guide, blog post, video, and description      |
| **2**    | **Buy Pro** or **Compare Free and Pro** | Pricing, Pro guides, Going Pro videos                     |
| **3**    | **Get product updates** (email)         | Site footer, Product Update videos, YouTube About section |

Every blog post ends with a single ask: **Download free at totalrecalls.app.** The four finished posts already follow this rule.

### Brand Colors Across Channels

| Token             | Hex       | Use                                                           |
| ----------------- | --------- | ------------------------------------------------------------- |
| **Obsidian**      | `#111315` | Backgrounds on the site footer, banner, thumbnails, end cards |
| **Paper**         | `#F3EFE7` | Headlines, wordmark, thumbnail text                           |
| **Mist**          | `#D9D4CB` | Body copy, success messages                                   |
| **Steel Blue**    | `#7A8FA6` | Eyebrows, file paths, series markers, focus states            |
| **Archive Amber** | Reserved  | Download free and Buy Pro on the website only                 |

---

## 4. Blog Series Status

The blog fills the real content gap identified in the audit: explainers, ownership, and workflow content. It replaces the time the spotlight series would have taken.

### Progress at a Glance

|            | Count                     |
| ---------- | ------------------------- |
| ✅ Written  | 4 of 9 (Blogs 3, 4, 5, 9) |
| ⏳ Pending  | 3 of 9 (Blogs 6, 7, 8)    |
| 🔍 Confirm | 2 of 9 (Blogs 1, 2)       |
| Published  | 0 of 9                    |

### Series Tracker

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

### What Changed from V2

The earlier plan scheduled these pieces later. Writing has moved ahead of schedule:

| Piece                              | Planned Before | Actual Status |
| ---------------------------------- | -------------- | ------------- |
| Markdown vs JSON (Blog 3)          | Weeks 7–8      | ✅ Written     |
| "Not sent to our servers" (Blog 4) | Weeks 7–8      | ✅ Written     |
| Backup (Blog 5)                    | Weeks 11–12    | ✅ Written     |
| VS Code / editor workflow (Blog 9) | After day 90   | ✅ Written     |

That frees writing time in Weeks 7–12. Use it for Blogs 6–8 and for upgrading the eight provider guides.

### Standard Blog Structure

Blogs 6, 7, and 8 should match the structure the finished posts already use, so the series reads as one set:

1. **Meta title and meta description**
2. **Opening:** what the post covers, reading time, and what you'll learn
3. **The Short Answer:** three points
4. **Main sections**, each ending with a bold **Takeaway**
5. **A side-by-side or task table**
6. **Common Questions**
7. **The Recommendation for Most People:** three plain steps
8. **Closing section** with the Free Tier note and **Download free at totalrecalls.app**

### Blog Rules

- One topic per post. No overlap with a provider guide.
- No provider spotlights, logos, or implied partnerships.
- Third-party apps, such as VS Code or Obsidian, are named as plain text only.
- Each post links to its matching guide and, once live, embeds its matching video.
- Every post gets a second-person accuracy check against Section 14 before publishing.

---

## 5. Blog Consistency Fixes

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

## 6. Website Implementation

The website explains the details and handles the download. Everything else sends people here.

### Page-by-Page Plan

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

### Linking the Blog into the Site

| Blog                            | Link From                                                            |
| ------------------------------- | -------------------------------------------------------------------- |
| Blog 3: Markdown vs JSON        | Every provider guide's "What you get" section, starting with ChatGPT |
| Blog 4: Not sent to our servers | Homepage trust section, See It Work, Pricing, footer privacy line    |
| Blog 5: Backup                  | Ownership Path, Library Folder explainer                             |
| Blog 9: VS Code                 | Ownership Path, Blog 3                                               |
| Blogs 6–8                       | Ownership Path, once published                                       |

### Footer Email Signup

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

### Visual Review Checklist

A full visual review is still pending. Run it after the final corrections go live.

- Download free is the first and most visible action on every page
- Archive Amber appears only on Download free and Buy Pro
- Only one signup form shows per page
- Video embeds use click-to-play or lazy loading
- Blog posts render code blocks, tables, and file trees cleanly
- Mobile layouts stack cleanly with readable text
- Keyboard focus is visible on every link, field, and button

---

## 7. Provider Guides

Guides are the core of the content library. With Option A approved, they also carry the spotlight role.

### Standard Guide Structure

1. **What you get:** the two files TotalRecalls saves, with a link to Blog 3
2. **Why this provider matters:** two or three neutral sentences
3. **Embedded video:** the matching Provider Guide video
4. **Step-by-step instructions** with screenshots
5. **Where your files go:** the Library folder
6. **Common problems and fixes**
7. **CTA:** Download free (Free Tier) or Compare Free and Pro (Pro)

### Provider Rollout

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

### Guide Rules

- Keep "Why this provider matters" short and neutral.
- Write provider names as plain text. Never use logos.
- Never criticize a provider or imply a partnership.
- Note the TotalRecalls version and the month each guide was last checked.

---

## 8. YouTube Channel

Full detail lives in the YouTube Strategy and Description Templates. This section covers planning.

### Channel Setup

| Element           | Final Spec                                                                                | Status    |
| ----------------- | ----------------------------------------------------------------------------------------- | --------- |
| **Name**          | TotalRecalls (no tagline)                                                                 | ⏳ Pending |
| **Handle**        | @TotalRecalls, or @TotalRecallsApp. Claim it now.                                         | ⏳ Pending |
| **Profile image** | Mark in Paper on Obsidian, tested at 40 pixels                                            | ⏳ Pending |
| **Banner**        | Wordmark, "Save your AI conversations as local files.", `MARKDOWN · JSON · WINDOWS 10/11` | ⏳ Pending |
| **Header links**  | Download free, See It Work, Guides, Pricing, with UTM tags                                | ⏳ Pending |
| **Trailer**       | 45–60 second See It Work cut, captioned                                                   | ⏳ Pending |

### Launch Set

1. TotalRecalls in 60 Seconds: One Real ChatGPT Download (also the trailer)
2. How to Save ChatGPT Conversations to Your PC
3. How to Save Claude Conversations to Your PC
4. How to Save Perplexity Threads to Your PC
5. Where TotalRecalls Saves Your Files
6. Free vs Pro: What's Included in Each

### Blog-Paired Videos

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

### Cadence

| Phase       | Timing         | Output                                   |
| ----------- | -------------- | ---------------------------------------- |
| **Launch**  | Weeks 3–4      | 6 videos together                        |
| **Build**   | Weeks 5–12     | One long video per week, plus 1–2 Shorts |
| **Steady**  | Month 4 onward | Two long videos per month                |
| **Ongoing** | Always         | Re-record when interfaces change         |

### Playlists

Launch with **Start Here**, **Provider Guides**, and **Quick Demos**. Add **Going Pro**, **Using Your Saved Chats**, **Troubleshooting**, and **Product Updates** once each has at least three videos.

### Production Rules

- Real screen capture only. Never mock up a screen.
- Calm pacing, clear audio, uploaded captions
- Blur emails, profile images, conversation titles, license keys, and order numbers. Never show a session token.
- Enlarged cursor, 1080p or higher, zoomed app window
- Straight cuts or short crossfades
- Disclose trimmed loading time in every description

### UTM Standard

```
?utm_source=youtube&utm_medium=[video|comment|channel]&utm_campaign=[series]-[topic]&utm_content=[link]
```

Series codes: `demo`, `guide`, `workflow`, `explainer`, `fix`, `update`. Log every campaign in the tracking sheet.

---

## 9. Social Content

Social posts carry the short, shareable provider angle that spotlights would have played. Finished blogs add a new source of material.

### Per-Provider Set

| Post                    | Content                                              | Links To       |
| ----------------------- | ---------------------------------------------------- | -------------- |
| **Proof post**          | 15–45 second clip of a real download                 | Matching guide |
| **"What you get" post** | Screenshot of a saved Markdown file, details blurred | Matching guide |
| **Tip post**            | One practical fix from the guide                     | Matching guide |

### Blog-Based Posts

| Blog      | Post Idea                                                        | Status                                      |
| --------- | ---------------------------------------------------------------- | ------------------------------------------- |
| Blog 3    | "Markdown is for people. JSON is for software."                  | Ready once Blog 3 publishes                 |
| Blog 4    | The connection path diagram: provider → your PC → Library folder | Ready once Blog 4 is reviewed and published |
| Blog 5    | "Back up the whole Library folder" with the four methods         | Ready once Blog 5 publishes                 |
| Blog 9    | One VS Code search shortcut for saved chats                      | Ready once Blog 9 publishes                 |
| Blogs 6–8 | One tip per post                                                 | ⏳ After writing                             |

### Social Rules

- One idea per post
- Link to the guide or blog post, never a spotlight article
- No fear-based hooks about lost or deleted chats
- No provider logos
- Pair $24 with "launch price" in any pricing post

---

## 10. Email

| Element           | Plan                                                                                                 |
| ----------------- | ---------------------------------------------------------------------------------------------------- |
| **Source**        | Footer signup only                                                                                   |
| **Frequency**     | Only when there's real news                                                                          |
| **Topics**        | New features, new providers, macOS and Linux progress                                                |
| **Blog mentions** | A short "new on the blog" line is fine inside a real update. Don't send emails for blog posts alone. |
| **Platform rule** | macOS and Linux stay "in development." No dates.                                                     |
| **Unsubscribe**   | One-click link in every email                                                                        |

---

## 11. How Everything Connects

### The Funnel

1. **Discover:** Someone searches on YouTube or Google.
2. **Trust:** A real screen recording, a clear guide, or an honest blog post shows what happens.
3. **Visit:** A description link, guide CTA, or blog CTA brings them to totalrecalls.app.
4. **Try:** They download the Free Tier.
5. **Upgrade:** Pro guides, Going Pro videos, and Pricing help them decide.
6. **Stay:** The footer signup and Product Update videos keep them connected.

### Where the Blog Fits

Guides answer "how do I save this?" The blog answers "what does this mean?" and "what can I do with my files?" Blogs 3 and 4 build trust before download. Blogs 5 through 9 keep people using the app after download.

### Assets Per Provider

| Asset                | Count | Upkeep                            |
| -------------------- | ----- | --------------------------------- |
| Written guide        | 1     | Quarterly check                   |
| Provider Guide video | 1     | Re-record when interfaces change  |
| Proof Demo           | 1     | Re-record when interfaces change  |
| Social posts         | 3     | Retire when the video is replaced |

---

## 12. Unified 12-Week Action Plan

This timeline merges the audit, the YouTube plan, and the blog series.

### Timeline Changes in V3

- **Blogs 3, 4, 5, and 9 are written early.** Their writing slots in Weeks 7–12 are now free.
- **Blogs publish in series order, one per week, from Week 3 to Week 11.** Week 12 is a buffer.
- **Blogs 6, 7, and 8 must be written at least two weeks before their publish week.**
- **Publishing is gated by review.** No post goes live until it passes the accuracy check and the fixes in Section 5.
- **Guide links to Blog 3** go live in Week 5, when Blog 3 publishes.

### Blog Publishing Schedule

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

### Week 0: Prerequisites

- ⏳ Implement the final website corrections
- ⏳ Run the visual review checklist
- 🔍 Confirm Free Tier limit wording: "per provider" or "per download"
- 🔍 Confirm single or double opt-in
- 🔍 Confirm the Privacy Policy names the email service provider
- 🔍 Confirm Blog 1 and Blog 2 topics and status
- 🔍 Confirm topics for Blogs 6, 7, and 8
- 🔍 Confirm saved filename format and default Library path
- ⏳ Claim @TotalRecalls on YouTube and matching social handles

### Weeks 1–2: Accuracy and Setup

| Workstream     | Tasks                                                                                                                          |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| **Website**    | Run every page against the guardrails. Archive spotlight drafts. Apply the confirmed Free Tier wording.                        |
| **Blog**       | Apply Section 5 fixes to Blogs 3, 4, 5, and 9. Run second-person review on all four, with Blog 4 first. Start drafting Blog 6. |
| **YouTube**    | Create profile image, banner, and About section. Add header links with UTM tags. Build the thumbnail template.                 |
| **Production** | Record, edit, and caption the six launch videos.                                                                               |
| **Systems**    | Set up one tracking sheet for videos **and** blog posts: title, claims, date, version, UTM campaign, status.                   |

### Weeks 3–4: Launch

| Workstream  | Tasks                                                                                                    |
| ----------- | -------------------------------------------------------------------------------------------------------- |
| **YouTube** | Publish the launch set. Set the trailer. Build three launch playlists. Pin a comment on every video.     |
| **Guides**  | Upgrade the ChatGPT, Claude, and Perplexity guides. Embed their videos.                                  |
| **Website** | Embed the demo on Homepage and See It Work. Add Free vs Pro to Pricing. Publish the Library Folder page. |
| **Blog**    | Publish Blogs 1 and 2. Finish Blog 6 draft. Start Blog 7.                                                |
| **Social**  | Post Free Tier provider sets. Cut 2–3 Shorts.                                                            |

### Weeks 5–8: Pro Coverage and Explainers

| Workstream  | Tasks                                                                                                                     |
| ----------- | ------------------------------------------------------------------------------------------------------------------------- |
| **Guides**  | Upgrade all five Pro guides. Rewrite the Gemini opening to explain Google Takeout first. Add Blog 3 links to every guide. |
| **YouTube** | Publish one Pro guide per week, starting with Gemini. Record each Proof Demo in the same session. Launch Going Pro.       |
| **Blog**    | Publish Blogs 3, 4, 5, and 6. Finish Blogs 7 and 8 drafts by Week 8.                                                      |
| **Social**  | Post Pro provider sets and Blog 3–5 posts as they go live.                                                                |
| **Review**  | Log recurring questions. First monthly metrics review in Week 8.                                                          |

### Weeks 9–12: Trust and Ownership

| Workstream  | Tasks                                                                                                                                                                                                     |
| ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **YouTube** | Publish Markdown vs JSON, "not sent to our servers," Windows search, backup, and organizing videos. Start Using Your Saved Chats and Troubleshooting. Publish the founder video and first Product Update. |
| **Blog**    | Publish Blogs 7, 8, and 9. Embed matching videos in Blogs 3, 4, 5, and 6 as they go live.                                                                                                                 |
| **Website** | Link all published blogs from Ownership Path. Embed the founder video.                                                                                                                                    |
| **Email**   | Send the first update email only if there's real news.                                                                                                                                                    |
| **Review**  | Second metrics review. Plan the next quarter.                                                                                                                                                             |

### Day 90 Checkpoint

By the end of Week 12, you should have:

- All 9 blog posts published, each linked from the right pages
- All eight provider guides on the standard structure, each with an embedded video
- About 18–22 long videos and around 15–20 Shorts
- Five or six active playlists
- Blog videos embedded for Blogs 3–7, with Blogs 8 and 9 videos planned for next quarter
- Clear data on which pages, posts, and videos send the most downloads

---

## 13. Weekly Operating Rhythm

| Day           | Focus                                                                                         |
| ------------- | --------------------------------------------------------------------------------------------- |
| **Monday**    | Plan the week. Check comments, support emails, and downloads by source.                       |
| **Tuesday**   | Record. Batch two or three videos in one setup.                                               |
| **Wednesday** | Edit, caption, and cut Shorts.                                                                |
| **Thursday**  | Write blog drafts, descriptions, thumbnails, and guide updates. Second-person accuracy check. |
| **Friday**    | Publish the week's blog post and video, embed, post social, update the tracking sheet.        |

### The Minimum Week

When a week gets busy, protect these and let the rest slide:

1. Reply to support emails and video comments
2. Publish one scheduled item, either the blog post or the video
3. Fix any claim that no longer matches the website

---

## 14. Accuracy Guardrails

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

### Review Process

- A second person checks every new asset against this table before publishing.
- Blog 4 gets the strictest review, since it explains exactly what connects to the internet.
- When website wording changes, update blog posts, video descriptions, and pinned comments the same week.
- Keep prices out of video descriptions and blog body copy. Let the Pricing page carry the number.

---

## 15. Remaining Gaps

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
