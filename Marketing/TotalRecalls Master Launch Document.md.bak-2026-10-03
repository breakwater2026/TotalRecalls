# TotalRecalls — Master Launch Document

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

---

## 2. Master Implementation Plan (operational command sheet)

## TotalRecalls Master Implementation Plan

This is your live command sheet. Where strategy tells you what to say and the gap checklist tells you what's open, this document tells you how to run the launch — every asset, on every channel, on every day, with a clear owner, CTA, dependency, and status. Treat it as the single operational source of truth for the 45-day launch window.
Fill the Owner columns with real names (or your own, if solo). Update Status daily. Everything points back to one product truth: TotalRecalls downloads your AI conversations from eight providers into local Markdown and JSON files, for a one-time $24 Pro price, with a Free Tier so people can try before they buy.
Status key: ⬜ Not started · 🟡 In progress · ✅ Done · ⏸ Blocked
Priority key: P1 Critical · P2 High · P3 Medium · P4 Low
1. Master execution table (Days -7 to 45)
Pre-launch (Days -7 to -1)
Day
Channel
Asset
Owner
CTA
KPI
Dependencies
Status
-7
Infrastructure
Blog section live + Day 1 post loaded
____
—
Blog publishes a test post cleanly
Blog template, hosting
⬜
-7
Analytics
UTM scheme + GA/events live
____
—
Test event fires end-to-end
Analytics account
⬜
-6
Website
Homepage rewrite deployed + mobile/desktop QA
____
—
Loads clean on all breakpoints
Homepage final approved
⬜
-5
Email
Platform connected, welcome sequence wired
____
—
Test signup triggers Email 1
Email tool, forms
⬜
-5
Ads
Pixels installed, ad accounts verified
____
—
Pixel fires on 3 key pages
Ad accounts
⬜
-4
Email
Segmentation tags + events created
____
—
Download and purchase events tag correctly
Email platform, tracking
⬜
-3
QA
Buy + download links tested on live site
____
—
100% of links resolve + purchase completes
Paddle/checkout live
⬜
-2
Support
SmartScreen + FAQ replies staged
____
—
Canned replies saved, owner assigned
FAQ content
⬜
-1
All
Full dry run — schedule everything
____
—
All Day 1 assets queued and previewed
All above
⬜
Phase 1 — Launch & category (Days 1–10)
Primary audience: Prospects + cold visitors. Phase CTA: Try the Free Tier.
Day
Channel
Asset
Owner
CTA
KPI
Dependencies
Status
1
Blog
Launch announcement post
____
Try the Free Tier
Page views, time on page
Blog live
⬜
1
Email
Launch broadcast + welcome Email 1
____
Try the Free Tier
Open %, click %
List, sequence wired
⬜
1
Video
Primary launch video embedded
____
Watch the demo
Views, completion %
Video file hosted
⬜
1
Paid social
Launch awareness ad set
____
Try the Free Tier
Cost per free download
Pixels, creative
⬜
1
LinkedIn
Launch organic post (9:00 AM)
____
Try the Free Tier
Reach, engagement
Blog URL live
⬜
1
X
Launch organic post (9:15 AM)
____
Try free
Impressions, reposts
—
⬜
1
Facebook
Launch organic post (10:00 AM)
____
Try the Free Tier
Reach, clicks
Blog URL live
⬜
1
Instagram
Launch post (12:00 PM)
____
Link in bio
Saves, reach
Bio link updated
⬜
5
Blog
Founder story post
____
Try the Free Tier
Views, scroll depth
Blog live
⬜
5
Social
Founder-led post (LinkedIn lead)
____
Read the story
Engagement, comments
Founder post ready
⬜
5
Email
Founder story broadcast
____
Try the Free Tier
Open %, click %
List
⬜
10
Blog
Category piece → "Own Your AI Chat Data"
____
Try the Free Tier
Views, guide clicks
Pillar guide live
⬜
10
Email
Welcome Email 2 (one library, 8 providers)
____
Try the Free Tier
Click %
Sequence wired
⬜
Phase 2 — Provider spotlights (Days 14–38)
Primary audience: Cold search + Prospects, soft nudge to Free-Tier users. Phase CTA: Try the Free Tier (mid-content Pro nudge).
Day
Channel
Asset
Owner
CTA
KPI
Dependencies
Status
14
Blog + short video
ChatGPT spotlight
____
Try the Free Tier
Organic traffic, downloads
Guide live
⬜
18
Blog + short video
Claude spotlight
____
Try the Free Tier
Organic traffic, downloads
Guide live
⬜
20
Email
Guide roundup #1 (ChatGPT + Claude)
____
Try the Free Tier
Click %
Two guides live
⬜
22
Blog + short video
Perplexity spotlight
____
Try the Free Tier
Organic traffic, downloads
Guide live
⬜
26
Blog + short video
Gemini spotlight
____
Try the Free Tier
Organic traffic, downloads
Guide live
⬜
28
Email
Guide roundup #2 (Perplexity + Gemini)
____
Try the Free Tier
Click %
Two guides live
⬜
30
Blog + short video
Grok spotlight
____
Try the Free Tier
Organic traffic, downloads
Guide live
⬜
34
Blog + short video
DeepSeek spotlight
____
Try the Free Tier
Organic traffic, downloads
Guide live
⬜
36
Email
Guide roundup #3 (Grok + DeepSeek) — Free-Tier nudge
____
Upgrade to Pro
Free→Pro clicks
Two guides live
⬜
38
Blog + short video
Mistral spotlight
____
Try the Free Tier
Organic traffic, downloads
Guide live
⬜
Phase 3 — Urgency & conversion (Days 42–45)
Primary audience: Free-Tier users + warm retargeting pools. Phase CTA: Buy Pro — $24 one-time.
Day
Channel
Asset
Owner
CTA
KPI
Dependencies
Status
42
Blog
Urgency post ("Launch Pricing Ends Soon")
____
Buy Pro — $24
Purchases
Blog live
⬜
42
Email
Urgency Email 1 (heads-up)
____
Buy Pro — $24
Conversion %
Buyer exclusion synced
⬜
42
Paid social
Retargeting urgency ad set live
____
Buy Pro — $24
ROAS, CPA
Warm pools built
⬜
43
Email
Urgency Email 2 (48 hours left)
____
Buy Pro — $24
Conversion %
Buyer exclusion synced
⬜
45
Email
Urgency Email 3 (last call)
____
Buy Pro — $24
Conversion %
Buyer exclusion synced
⬜
45
Blog + short video
Qwen spotlight (closes series)
____
Try free / Buy Pro
Traffic, downloads
Guide live
⬜
Section takeaway: If a row has no owner or an unmet dependency, it's not ready to ship. Scan this table each morning and clear blockers before publishing.
2. Asset-to-channel mapping (final vs. backup)
You have many overlapping assets on the canvas. This map designates one approved final per slot and keeps the rest as labeled backups, so nothing ships by accident.
Homepage / landing
Slot
Approved final
Backups / drafts
Channel
Homepage
TotalRecalls Homepage Rewrite
Landing Page (x4), Landing Page Hero
Website
FAQ block
FAQ (Frequently Asked Questions)
—
Website
Email sequences
Stage
Approved final
Backups / drafts
Trigger
Welcome (prospect)
TotalRecalls Welcome Email Sequence
Email Sequence (x2)
New signup
Value nurture
AI Providers Consolidation Email; Data Ownership Email Campaign
Multi-AI Organization, AI Consolidation, Privacy Features, Data Privacy
Post-welcome drip
Free→Pro upgrade
Free-to-Pro Upgrade Email Sequence
Pro Upgrade Email (x2), One-Time Payment Value (x2), Pro Upgrade Persuasion (x2), Free-Tier to Pro
Free-tier tag applied
Urgency (Phase 3)
Launch Pricing Urgency Email Sequence
Launch Urgency Sequence, Pro Launch Price Reminder, Final Reminder, Discount Reminder, Expires Tonight
Day 42
Ads
Channel
Approved final
Backups / drafts
Google/Search
TotalRecalls Search Ads
Google Ads Campaign (x2), App Google Ads, Chats Backup Google Ads, Search Campaign, Google Ads Video
Meta/Facebook
TotalRecalls Meta Ad Variations
Stop Losing AI Chats FB Ad, Social Media Ad, Ad Campaign (x2)
LinkedIn
TotalRecalls LinkedIn Ad Variations
LinkedIn Ad, Product LinkedIn Ad
X
TotalRecalls X Ads
AI Chat Backup X Ad, X Ad
Organic social
Platform
Approved final (launch day)
Backups / drafts
LinkedIn
AI Chat Backup LinkedIn Post
AI Chat Backup Tool LinkedIn Post
Facebook
TotalRecalls Facebook Post
Data Privacy FB Post, Ad Variation FB Post
X
TotalRecalls AI Chat Backup X Post
—
Instagram
TotalRecalls Product Launch IG Post
AI Privacy IG Post
Multi-platform set
Launch-Day Social Posting Checklist (Social Media Posts)
Social Media Posts (earlier versions)
Blog
Post
Approved final
Status
Launch announcement
TotalRecalls Launch Announcement Blog
✅
Founder story
TotalRecalls Founder Story Blog
✅
Category piece
Own Your AI Chat Data (live guide)
✅
Urgency post
TotalRecalls Launch Pricing Urgency Blog
✅
Governance rule: Rename every non-final asset with a [BACKUP] or [DRAFT] prefix. Only the approved final feeds the execution table. Deprecate untitled documents.
Section takeaway: One approved asset per slot. Everything else is clearly labeled and out of the shipping path.
3. Lifecycle automation logic
Three buckets carry the campaign. Every contact sits in exactly one, and actions move them between buckets automatically.
Bucket definitions and triggers
Bucket
Enters when
Primary CTA
Receives
A — Prospect
Submits any signup form; no download
Try the Free Tier
Welcome sequence, value nurture, guide roundups
B — Free-Tier user
Free-tier download event fires
Upgrade to Pro — $24
Upgrade sequence, soft Pro nudges
C — Buyer
Purchase event fires
None commercial
Onboarding, tips, feature/provider updates
Movement and suppression rules
Rule
Logic
Prospect → Free-Tier
Download event applies "free-tier" tag; remove from prospect acquisition drip
Free-Tier → Buyer
Purchase event applies "buyer" tag; exit all upgrade + urgency flows immediately
Prospect → Buyer (direct)
Purchase event applies "buyer" tag; skip free-tier flows
Buyer suppression
Exclude Bucket C from every sell, upgrade, and urgency send — no exceptions
Mid-sequence purchase
Nightly sync removes new buyers from active urgency emails before the next send
Inactive free-tier
No download activity in 14 days → "activation reminder" branch (how-to, not sell)
Unsubscribe
Global suppression across all flows; keep only transactional/license emails
Sequence entry/exit map
Welcome sequence: Entry = new signup. Exit = download (→ upgrade flow) or purchase (→ onboarding).
Value nurture: Entry = welcome sequence complete, still a prospect. Exit = download or purchase.
Upgrade sequence: Entry = free-tier tag. Exit = purchase or end of sequence (→ long-term nurture).
Urgency sequence: Entry = Day 42 for Buckets A + B. Exit = purchase or campaign end. Buyers hard-excluded.
Onboarding: Entry = purchase. No commercial CTA; focus on activation and updates.
Section takeaway: Tag on action, move on action, and suppress buyers everywhere. The nightly buyer sync is the single most important automation to get right.
4. Retargeting mechanics
Phase 1–2 builds the pools; Phase 3 converts them. Set these up early so audiences are large enough by Day 42.
Audience definitions
Audience
Definition
Window
Pricing viewers
Visited pricing or buy page, no purchase
30 days
Download-page visitors
Visited download page, no confirmed free-tier
30 days
Free-tier users
Confirmed free-tier tag, no Pro
45 days
Video viewers
Watched 25%+ of launch or spotlight video
30 days
Guide readers
Read any Phase 2 spotlight/guide page
30 days
Exclusions (critical)
Suppress all buyers (Bucket C) from every retargeting ad set.
Sync the buyer tag to each ad platform daily so purchasers stop seeing sell ads within 24 hours.
Exclude anyone who converts mid-campaign from active urgency ad sets.
Creative rotation rules
Phase
Creative focus
Rotation
Phase 1–2 (pool-building)
Soft: loss aversion, ownership, "try free"
Rotate 2–3 creatives; refresh every 7 days
Phase 3 (conversion)
Hard: deadline + one-time-vs-subscription math
3-creative rotation; swap the fatigued unit at CTR drop >20%
Free-tier specific
"5 locked providers Pro unlocks"
Serve only to Bucket B
Activation thresholds: Don't launch a retargeting set until its audience clears platform minimums (roughly 1,000+ users). If a pool is thin by Day 40, consolidate audiences to reach size.
Section takeaway: Build pools from Day 1, cap frequency, and let the daily buyer sync protect your paying customers from sell ads.
5. Infrastructure readiness checklist
This is your pre-launch gate. If any item is unchecked, hold the launch.
Blog and website
⬜ Blog section live, template tested, headings and CTA slot working
⬜ Meta title/description fields functional
⬜ Day 1 announcement post loaded and scheduled
⬜ Homepage rewrite deployed and reviewed on mobile + desktop
Analytics and UTMs
⬜ Analytics installed and firing on all key pages
⬜ UTM convention documented (utm_source / utm_medium / utm_campaign=launch)
⬜ Free-tier download event tracked
⬜ Purchase event tracked
Email capture and platform
⬜ Signup forms live on homepage, guide pages, pricing/buy pages
⬜ "Notify me" capture for macOS/Linux and new providers
⬜ Email platform connected with tags and automations
⬜ Welcome sequence test-fires on new signup
Ad pixels
⬜ Pixels installed on homepage, pricing, download pages
⬜ Conversion events mapped (download, purchase)
⬜ Ad accounts verified and billing active
Buy/download links QA
⬜ Buy link completes a real test purchase
⬜ Free-tier download link delivers the correct ZIP
⬜ License key delivery email confirmed
⬜ All CTAs across site point to correct destinations
Support workflow
⬜ Support inbox monitored, owner assigned
⬜ SmartScreen canned reply saved
⬜ FAQ/help path reachable from every page
⬜ Escalation path defined for edge-case issues
Section takeaway: No blog, no tracking, no working buy link means no launch. Clear every box before Day 1.
6. Launch-week support and objection-handling workflow
A new downloadable Windows tool triggers predictable questions. Handle them fast and consistently.
Monitoring cadence (Days 1–7)
Window
Action
Owner
First 4 hours
Check all platforms + support inbox every 30 min
____
Hours 4–24
Check every 1–2 hours
____
Days 2–7
Check morning, midday, evening
____
Canned replies
SmartScreen warning ("Windows protected your PC"):
Thanks for flagging this! That message is standard SmartScreen behavior for any newly released, independently developed app — it's not a sign of malware. Click More info, then Run anyway to continue. Only download from totalrecalls.app. As the app builds reputation with Microsoft, the warning fades. Any trouble, email support@totalrecalls.app.
"Is my data safe / uploaded anywhere?":
Great question. TotalRecalls runs 100% locally — your conversations are saved to a folder on your own machine as Markdown and JSON, and nothing is ever uploaded to a server. There's no account and no sign-up. More detail on our Privacy Policy.
"Is this a subscription?":
No subscription, ever. Pro is a one-time $24 (discounted launch price), and you keep free updates to the core app for life. There's also a Free Tier so you can test it first.
"Does it work on Mac / mobile?":
Not yet — Windows 10/11 today. macOS and Linux versions are in development. Drop your email on our site and we'll notify you when they land.
FAQ escalation process
Tier 1 — Canned reply. Covered above? Respond with the saved reply.
Tier 2 — Personalized. New but simple? Answer directly, then log it.
Tier 3 — Escalate. Bug or edge case? Route to the developer, set expectation on timing.
Feed the loop. Any question asked 3+ times → add to the live FAQ and consider a Day 2–3 social FAQ post.
Section takeaway: Speed and consistency build trust for a new app. Pre-written replies and a clear escalation ladder keep launch week calm.
7. Testing roadmap
Test one variable at a time, give each test enough traffic to matter, and roll winners into the approved assets.
Element
What to test
How
Success metric
When
Headlines
Loss-aversion vs. ownership framing
A/B on homepage hero + top ads
Click-through to free download
Phase 1
CTAs
"Try the Free Tier" vs. "Download free"
Button-copy A/B on homepage
Download conversion rate
Phase 1
Landing variants
Homepage rewrite vs. control section order
Split traffic 50/50
Free-tier downloads per visit
Phase 1–2
Email subject lines
Curiosity vs. direct-benefit
A/B on each broadcast
Open rate
Every send
Ad creatives
Static graphic vs. short video
Per-platform creative A/B
Cost per free download
Phase 1–2
Urgency framing
Deadline-led vs. value-led
A/B on Phase 3 ads + emails
Purchase conversion rate
Phase 3
Testing rules
Change one variable per test — never headline and image together.
Let each test run to a meaningful sample before calling it; don't stop early on noise.
Log every result in a shared sheet; promote winners into the approved asset for that slot.
Kill any ad creative when CTR drops more than 20% below its cohort.
Section takeaway: Small, disciplined tests compound. Feed every winner back into your approved assets so quality climbs across the whole launch.
How to run this document
Assign owners to every row

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
