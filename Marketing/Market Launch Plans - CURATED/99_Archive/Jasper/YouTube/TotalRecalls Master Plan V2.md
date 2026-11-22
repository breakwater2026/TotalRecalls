# TotalRecalls Master Implementation Plan V2

**Status:** Final operating document. It consolidates every approved strategy into one plan.\
**Replaces:** The earlier Master Implementation Plan draft. Where any older document disagrees with this one, this plan wins.\
**Built for:** A founder-led team that records, writes, and publishes in small batches.

TotalRecalls makes one promise: **your AI conversations, saved to your own PC as Markdown and JSON files.** This plan shows how the website, provider guides, explainers, YouTube channel, social posts, and email work together to support that promise. It covers what to build, what to skip, who checks what, and the order to do it in.

---

## 1. How to Use This Plan

This document tells you **what happens and when**. The supporting documents hold the detail.

### Supporting Documents

| Document                                          | What It Covers                                                     | Use It For                      |
| ------------------------------------------------- | ------------------------------------------------------------------ | ------------------------------- |
| **Master Implementation Plan V2** (this document) | Decisions, timeline, rhythm, guardrails, open items                | Weekly planning and priorities  |
| **Content Audit Plan V2**                         | Keep, update, merge, create, and retire decisions                  | Page and guide changes          |
| **YouTube Strategy V5**                           | Channel setup, video types, playlists, thumbnails, titles, cadence | Recording and publishing videos |
| **YouTube Description Templates**                 | Seven-part description structure, UTM naming, pinned comments      | Every upload                    |
| **Footer Email Signup HTML V2**                   | Signup markup, styles, behavior, accessibility                     | Development and QA              |
| **Footer Signup Success Message**                 | Final post-signup copy                                             | The success state               |

### Precedence Rule

1. This plan sets priorities and timing.
2. Supporting documents set the detail inside those priorities.
3. If a supporting document conflicts with this plan on timing or scope, follow this plan. Section 10 lists the conflicts it resolves.

### How the Pieces Fit Together

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

## 2. Finalized Decisions

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

### Why Option A Won

- **Guides already do the job.** They match search intent and lead straight to a download.
- **Guide plus video beats a spotlight.** Searchers get instructions and proof in one place.
- **Eight extra articles mean eight more pages to keep current.** Provider interfaces change often, and every extra page is a chance for claims to drift.
- **The real gap is elsewhere.** Explainers, ownership content, and founder material add more value per hour.

**Takeaway:** Don't spend time re-debating these. Spend it shipping.

---

## 3. Core Message Rules

Every asset follows these rules, from the homepage headline to a pinned comment.

### One Job Per Asset

Each page, guide, and video has one clear job. If two assets do the same job, merge them. This rule is why the spotlight series was cancelled.

### Call-to-Action Hierarchy

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

### Spoken and Written Tone

- Calm, plain, and specific
- Show rather than claim
- No hype, fear, countdowns, or "smash that button"
- No hooks about AI companies deleting your chats

### Brand Colors Across Channels

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

## 4. Website Implementation

The website explains the details and handles the download. Everything else sends people here.

### Page-by-Page Plan

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

### Video Embed Rules

- Use click-to-play thumbnails or lazy loading so embeds don't slow the page.
- Place the video near the top of guides, after "What you get" and "Why this provider matters."
- Never let an embed push Download free below the fold on desktop.

### Footer Email Signup

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

### Visual Review Checklist

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

## 5. Provider Guides

Guides are the core of the content library. With Option A approved, they also carry the spotlight role.

### Standard Guide Structure

Every guide follows the same order, so readers know what to expect and updates stay simple:

1. **What you get:** the two files TotalRecalls saves
2. **Why this provider matters:** two or three neutral sentences
3. **Embedded video:** the matching Provider Guide video
4. **Step-by-step instructions** with screenshots
5. **Where your files go:** the Library folder
6. **Common problems and fixes**
7. **CTA:** Download free (Free Tier guides) or Compare Free and Pro (Pro guides)
8. **Last checked:** TotalRecalls version and month

### "What You Get" Template

> When you download a \[Provider] conversation with TotalRecalls, you get two files on your PC:
>
> - **A Markdown file** you can open in any text editor or note-taking app
> - **A JSON file** with the full structured conversation
>
> Both are saved in your Library folder. Your conversations aren't sent to our servers.

For Gemini, adjust the opening line: "When you bring a Gemini Google Takeout file into TotalRecalls Pro, you get two files per conversation on your PC."

### Provider Rollout

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

### Gemini Guide Requirements

- State in the first section that Gemini works through a Google Takeout file
- Show each step: request the Takeout file, download it, bring it into TotalRecalls
- Set honest expectations about Google's wait time for the Takeout file
- Never describe Gemini as a one-click download, anywhere

### Guide Rules

- Keep "Why this provider matters" short and neutral. Don't describe the provider's own features.
- Write provider names as plain text. Never use logos.
- Never criticize a provider or imply a partnership.
- Move useful lines from archived spotlight drafts into the guide. Discard the rest.

**Takeaway:** Eight guides, one structure. When something changes, you update the same section in every guide.

---

## 6. Explainers, Ownership, and Founder Content

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

### The Highest-Risk Explainer

**"What 'not sent to our servers' means"** carries the most risk of overclaiming. It must say clearly that:

- Downloads connect directly from the user's PC to each AI provider
- Users sign in to each provider inside the app, on their own computer
- Saved files stay on the user's PC
- There's no TotalRecalls account to create

Never describe the app as "fully offline," and never say it "never touches the internet." Have a second person review this piece before it goes live.

### Third-Party Apps

When ownership content shows outside tools such as VS Code or a note-taking app, name them as plain text and add a line saying TotalRecalls isn't affiliated with them.

**Takeaway:** Explainers answer the doubts that stop downloads. Ship the high-priority three first.

---

## 7. YouTube Channel

Full detail lives in **YouTube Strategy V5** and the **YouTube Description Templates**. This section covers what you need for planning.

### Channel Setup

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

### Content Pillars

| Pillar        | Share in First 90 Days | Video Types                      |
| ------------- | ---------------------- | -------------------------------- |
| **Proof**     | About 70% combined     | Proof Demos                      |
| **How-To**    | (with Proof)           | Provider Guides, Troubleshooting |
| **Ownership** | About 30% combined     | Workflow videos, Explainers      |
| **Updates**   | (with Ownership)       | Product Updates                  |

### Launch Set

Publish these six together, so the channel is useful on day one:

1. TotalRecalls in 60 Seconds: One Real ChatGPT Download (also the trailer)
2. How to Save ChatGPT Conversations to Your PC
3. How to Save Claude Conversations to Your PC
4. How to Save Perplexity Threads to Your PC
5. Where TotalRecalls Saves Your Files
6. Free vs Pro: What's Included in Each

The Claude and Perplexity Proof Demos are recorded in the same sessions and published with the launch set as bonus videos.

### Cadence

| Phase       | Timing         | Output                                         |
| ----------- | -------------- | ---------------------------------------------- |
| **Launch**  | Weeks 3–4      | 6 core videos together, plus Proof Demos       |
| **Build**   | Weeks 5–12     | About one long video per week, plus 1–2 Shorts |
| **Steady**  | Month 4 onward | Two long videos per month, Shorts as available |
| **Ongoing** | Always         | Re-record when interfaces change               |

Proof Demos recorded alongside a Provider Guide don't count toward the weekly long video.

### Playlists

| Playlist                   | Launch Timing                        |
| -------------------------- | ------------------------------------ |
| **Start Here**             | Weeks 3–4                            |
| **Provider Guides**        | Weeks 3–4                            |
| **Quick Demos**            | Weeks 3–4                            |
| **Going Pro**              | Week 8                               |
| **Using Your Saved Chats** | Weeks 9–10                           |
| **Troubleshooting**        | Weeks 11–12, once three videos exist |
| **Product Updates**        | Add after the third update video     |

### Production Rules

- Real screen capture only. Never mock up a screen.
- Calm pacing, clear audio, uploaded captions
- Blur emails, profile images, conversation titles, license keys, and order numbers. Never show a session token.
- Enlarged cursor, 1080p or higher, zoomed app window
- Straight cuts or short crossfades. No zoom punches or sw
