# TotalRecalls — Market Launch Implementation Plan

**Date:** 2026-10-13 · **Status:** Full implementation plan — consolidated from existing marketing material (no new creative) + template-complete sections (market context, funnel/leaks, Phase 0, months 2–3 engine, budget, risks, source list) added 2026-10-13 evening
**Scope:** YouTube · Blog · Social media · Email — everything assembled from the `marketing/` source documents in §3, plus dated market context in §2.
**Precedence rule (inherited from Master Implementation Plan V3):** where any document below disagrees with V3, V3 wins. Where V3 marks an item 🔍 Confirm, it is carried into §16 as a decision item.

## 1. Product snapshot (verified 2026-10-13 against the live site)

| Fact | Value | Source |
|---|---|---|
| Product / one-liner | TotalRecalls — "Recall every AI conversation, keep on your own PC." Windows app that downloads AI chats from 8 providers as local Markdown + JSON | totalrecalls.app (homepage, fetched 2026-10-13) |
| Providers (8) | ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral, Qwen | homepage; `messaging/TotalRecalls Launch Campaign.md` |
| Free Tier | ChatGPT, Claude, Perplexity — 5 conversations each. **Live-site wording conflict: homepage says "5 conversations each" (per provider); download page says "5 conversations per download"** | homepage vs /download/ (fetched 2026-10-13) → decision item D5 |
| Pro price | $24 one-time (launch price), normal $48, "for the life of the product" updates | live `/js/config.js` (`$24USD` / `$48 USD`, Paddle); /pricing/ |
| Checkout / merchant of record | Paddle Billing (client-side Paddle.js checkout; price `pri_01m37q…`, launch discount `dsc_01m398…`) | live `/js/config.js` |
| Version | v1.0.0 (released 2026-09-12), portable ZIP ~17.8 MB, no installer | /download/ (fetched 2026-10-13) |
| Code signing | Not yet — "Code-signing is on the roadmap"; SmartScreen prompt expected on first launch; Windows 11 Smart App Control may block with no override | /download/ technical notes |
| Platforms | Windows 10/11 only; macOS and Linux "in development", no dates | V3 §2 Finalized Decisions; /download/ |
| Blog surface on site | **None.** `/blog` → 404; only `/guides` (200) and `/press` (200) exist | curl check 2026-10-13; `meta/GAPS-2026-10-02-blogs-social.md` B1 |
| YouTube channel | TotalRecalls `@totalrecalls` (ID `UChO3ZyrGqRtBFHRuQx2qX1w`); 8 videos uploaded private in "Start Here" playlist `PLHGgAPo4_vi8` (Claude hero + 7 provider videos — Qwen not yet; convergence is a channel artifact); banner applied; thumbnails built | `Jasper/YouTube/NIGHT_WORKLIST.md`; `docs/STATUS-2026-10-01-youtube-launch.md` |
| Site health | apex + www both 200; robots.txt 200; sitemap 200 (54 URLs, GSC-verified 2026-10-01) | curl 2026-10-13; status note |

## 2. Market context (dated sources, fetched 2026-10-13)

**Incumbent scale (why the audience is huge and multi-provider):**
- ChatGPT: 900M weekly active users — OpenAI official, Feb 2026 (TechCrunch, 2026-02-27); 50M paying subscribers (same release). At DevDay 2026 (keynote 2026-09-29) OpenAI stated 1.2B weekly users (OpenAI recap; company statement, no outside audit).
- Claude: "100M+ weekly users" — Anthropic announcement, April 2026 (company figures, via contemporaneous coverage). Third-party MAU estimates diverge widely (56M mobile-app MAU Q2 2026, Sensor Tower via TechTimes 2026-06-05, vs 220M "consumer surface" Q1 2026, presenc.ai) — treat the company's weekly figure as the anchor and note the estimates as unverified.
- Implication: the realistic user is already on 2–4 of these providers. Every one of them accumulates months of conversation history that the provider hosts — and **none of the eight provides a local, user-owned export of your full history by default**. That is the demand TotalRecalls answers.

**Overlap / adjacent tools (the gap none of them cover):**

| Tool | What it is | Providers | Output | Cost | Gap vs TotalRecalls |
|---|---|---|---|---|---|
| ChatGPT Exporter (Chrome extension) | browser extension | ChatGPT only | PDF/MD | free | 1 provider, per-chat, browser-dependent |
| chatgpt-chat-exporter (userscript, GitHub `rashidazarang`) | console script | ChatGPT + Gemini | MD/HTML/PDF | free | manual, per-chat, 2 providers |
| ChatKeeper (martiansoftware.com) | converter | ChatGPT official export → local Markdown | free | requires the official export first, ChatGPT only |
| Pactify | extension + sync | ChatGPT → Notion/Word/PDF | paid | pushes to cloud/Notion — not local files you own |
| Rewind / Mem / Supermemory / MIND / SecondBrain | AI-memory / screen-capture apps | N/A (capture ongoing activity, forward-looking) | SaaS, mostly subscription | ongoing capture, cloud or heavy local compute, recurring cost — different job: they log what happens *next*; TotalRecalls is a **one-time download of history you already have**, plain files, $24 once, no account |

**The pitch (locked by §4):** 8 providers → one local folder, Markdown + JSON, no cloud, no account, no subscription, $24 once. No free tool covers multi-provider; no subscription covers local ownership.

## 3. Dedupe record + source library

### 3.1 Dedupe performed (2026-10-13)

SHA256 + normalized-content scan of all 160 content files in `marketing/`:

| Removed | Why | Kept |
|---|---|---|
| `Jasper/YouTube/Privacy Explainer Blog 4.md` | exact byte-dup (same 2026-10-02 mtime) of the `Jasper/YouTube/Blog/` copy | `Jasper/YouTube/Blog/Privacy Explainer Blog 4.md` |
| `Jasper/YouTube/TotalRecalls Blog Post 10.md` | dup of the `Blog/` copy (05:30 vs 05:35, same 20,222 B) | `Jasper/YouTube/Blog/TotalRecalls Blog Post 10.md` (newer) |
| `email/Email Sequence (fragment).docx` | 600-char strict subset of `email/sequences/Email 1 Welcome — early draft.md` | the `.md` |

No near-duplicates (pairwise ratio > 0.70) found elsewhere. All three
removals completed 2026-10-13 (the `.docx` was initially file-locked but
freed and was deleted the same day). Full trail:
`marketing/Jasper/tools/reports/deleted-manifest.txt`.

**Image dups found but NOT deleted (2026-10-13):** a full 712-file byte-hash
pass also surfaced 5 byte-identical image groups, all in production asset
folders (not marketing content), so they were flagged, not removed — deleting
them would break the thumbnail/video build:
- `Jasper/YouTube/frames/`: `thumb_claude.jpg` ≡ `thumb_master.jpg`;
  `_claude_frame.jpg` ≡ `_minis_frame.jpg`; `scan_100.jpg` ≡ `thumb_minis.jpg`
  (build_thumbnails.py consumes `thumb_claude`/`thumb_master` as inputs).
- `Jasper/YouTube/frames_conv_test_fix.png` ≡ `frames_convergence/f0036.png`
  (convergence-animation frame; `build_convergence_video.py` reads
  `frames_convergence/`).
- `Jasper/Website Rewrite/_shots/08_mobile_02…11.png` — 10 identical captures
  (a capture-loop artifact; the loop wrote the same frame 10×).
These are video/screenshot build artifacts. If you want them collapsed, name
which side to keep and I'll delete the rest — but do it after the current
thumbnail/video render, not before.

**Superseded-but-kept documents** (versioned plans — kept for history, NOT used
as source for this plan): `strategy/TotalRecalls Master Implementation Plan.md`
(09-28, replaced by V2 → V3), `Jasper/YouTube/TotalRecalls Master Plan V2.md`
(10-02, replaced by V3). `strategy/TotalRecalls Launch Marketing Plan (Revised)
— 2 variants.md` and `messaging/TotalRecalls Launch Campaign.md` are pre-V3
strategy inputs: their channel mix, key messages, and KPI objectives are folded
into §4–§8 and §13 below; their timelines are superseded by V3's 12-week plan.

### 3.2 Source library (what this plan is built from)

All paths relative to `marketing/`. "Role" = what each contributes.

**A. Operating plans (source of truth for sequencing)**
| Doc | Date | Role |
|---|---|---|
| `Jasper/YouTube/Master Implementation Plan V3.md` | 10-03 | **Primary.** Decisions, blog series status, 12-week timeline, accuracy guardrails, CTA hierarchy, weekly rhythm |
| `Jasper/YouTube/YouTube Implementation Plan.md` | 10-03 | YouTube week-by-week execution, aligned to V3 |
| `Jasper/YouTube/TotalRecalls YouTube Strategy.md` | 10-02 | Channel purpose, pillars, playlists, thumbnails, 90-day plan |
| `Jasper/YouTube/YouTube Description Templates.md` | 10-02 | Per-series description structure, UTM naming, pinned comments |
| `Jasper/YouTube/TotalRecalls Content Audit Plan V2.docx` | 10-02 | Keep/update/merge/retire decisions |
| `Jasper/YouTube/TotalRecalls Hook Rankings Guide.md` | 09-30 | Hook scoring (V6, V10 ranked; scorecards for the rest) |
| `Jasper/YouTube/NIGHT_WORKLIST.md` | 10-02 | Verified channel state: 9 uploads, playlist, banner, thumbnails |
| `strategy/TotalRecalls Launch Marketing Plan (Revised) — 2 variants.md` | 09-29 | Channel mix + 5 video scripts + short-form pillars (superseded timeline) |
| `strategy/TotalRecalls Launch Readiness Plan.md` / `Launch Gap Checklist.md` / `Launch Marketing Organization.md` | 09-28/29 | Readiness gates, org/ownership, gaps |
| `strategy/TotalRecalls Missing Items Checklist.md` | 09-29 | Open-item rollup (P1/P2/P3) |
| `meta/GAP_ANALYSIS_2026-09-29.md` + `meta/GAPS-2026-10-02-blogs-social.md` | 09-29 / 10-02 | Gap findings (B1–B4, S1–S5, C1–C8) feeding §16 |

**B. Blog (9-post series per V3; 10 drafts on disk — see D1 and §6)**
`Jasper/YouTube/Blog/`: Markdown vs JSON (B3), Privacy Explainer (B4), Backup
Library (B5), Windows Search (B6), Obsidian (B8), Backup Windows (extra —
overlaps B5), VS Code (B9), PowerShell (extra — candidate B7), Library Folder
Explainer (candidate B2), Free vs Pro Explainer (extra).
`messaging/founder/Founder Story — Why I Built TotalRecalls (2 variants + profile).md`
= Day-5 founder-story post. `messaging/Press & Announcement Copy.md` = launch-
announcement copy + "Launch Pricing Ends Soon" urgency post + headlines.

**C. YouTube**
`TotalRecalls-Youtube/scripts/` — 10 scripts (V6 = Final); `TotalRecalls-Youtube/`
— Content Plan (first 10), Short-Form Strategy, Upload Checklist & Template,
Thumbnail Concepts, Channel Description, Playlist Structure, Main Explainer
Outline & Shot List. `Jasper/YouTube/TotalRecalls YouTube Channel Style.md` =
visual identity spec.

**D. Social**
`social/{facebook,instagram,linkedin,x}/… all variants.md` — 18 launch-day
variants. `Jasper/Social media/Content Calendar.md` — Day 0–29 calendar
across 7 surfaces (IG/LinkedIn/TikTok/X/Threads/FB + Blog rows — see §7).
`Jasper/Social media/{Social Media Campaign, TotalRecalls Social Media
Campaign, Untitled Document (1)}.md` — Day 0/3/10 post bodies.
`ops/Launch-Day Social Posting Checklist.md` — launch-day runbook.

**E. Email**
`email/sequences/` (Welcome + Seq 1–3), `email/slot-2|3|4/` — 4-email program,
19 variants. `Jasper/Website Rewrite/Footer Signup Success Messages.md` etc. —
signup copy.

**F. Messaging & website**
`messaging/` — Launch Campaign (KPI objectives), Landing Page Copy (3
variants), FAQ (safe?/Windows warning). `Jasper/Website Rewrite/` — 16 page
specs incl. Homepage Flow, Pricing Section, Brand Style Guide. `ads/` — 5
networks' paid copy (deferred; see §11).

**G. Master compendium**
`TotalRecalls Master Launch Document.md` (324 KB, 10-03) — embeds A+B+C items
verbatim; use for cross-reference, not as a separate source.

## 4. Core messages & rules (from V3 §3 + Launch Campaign)

**Positioning (locked):** AI chat history drifts. Files stay put. — 8
providers → one local folder, Markdown + JSON. No cloud. No account. No
subscription. $24 once. (The §2 gap table is why this positioning is defensible:
free tools stop at 1–2 providers; subscription memory apps do a different job.)

**One job per asset:** every asset has exactly one purpose — acquisition
(drive to site), conversion (Free Tier download), or retention (upgrade /
re-engagement). No asset does two jobs.

**CTA hierarchy (every asset follows this order):**
1. Primary → `https://totalrecalls.app/download/` (Free Tier)
2. Secondary → `https://totalrecalls.app/buy/` (Pro, $24 launch price)
3. Tertiary → blog / guide / video deep links

**Proof points (use these, nothing invented):** 8 providers supported; files
are plain Markdown + JSON on the user's disk; one-time $24 (normal $48); no
account, no cloud, no subscription; Windows 10/11 portable ZIP.

**Accuracy guardrails (V3 §14):** every provider-specific claim (export
mechanism, file types, limits) must match the app's actual behavior and the
live site. If a script or post can't be verified against the product or a
guide, it is a 🔍 Confirm item — it does not ship until verified. This applies
to community posts (Reddit, HN) exactly as to paid content.

## 5. Channel 1 — YouTube

**Current state (verified 10-02 worklist):** channel live, banner applied,
8 videos uploaded private in "Start Here" playlist
(`PLHGgAPo4_vi8`): Claude hero (`TR_website_claude_hero.mp4`) + 7 provider
videos (ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral —
Qwen not yet). The convergence animation (1.5) is a channel artifact, not
a video upload. Confirm actual private count in Studio — D7. Thumbnails
built (Template 2, product proof). API key works; OAuth upload flow was
blocked on Google `403 org_internal` — fix documented in
`docs/STATUS-2026-10-01-youtube-launch.md` (consent with the plain Gmail
that owns the project + test user).

**What to execute (from YouTube Implementation Plan, weeks 1–2):**
1. Complete the OAuth/consent fix; verify one API upload lands.
2. Write 9 per-video descriptions from `YouTube Description Templates.md`
   (series header → what the video covers → provider note → CTA block →
   UTM-tagged links → related videos). Pinned comment per video = one
   provider-specific question (drives engagement + surfaces the guide link).
3. Publicize the 9 "Start Here" videos on launch day (not staggered — the
   launch set goes public together, per V3 Week 3–4 "Launch").
4. Upload remaining scripts: V6 (Final, "Trying to Get Your Old AI
   Conversations Back?") + V7–V10 per the 10-video plan; hook choice from
   the Hook Rankings Guide (V6/V10 ranked; others use their merged
   "Alternative Hooks" section).
5. Cadence (V3 §8): 2 videos/week through Week 8 (provider + explainer
   alternation), 1/week Weeks 9–12 (trust/ownership). Blog-paired video
   rule: every explainer post (B4–B9) has a companion video or reuse of an
   existing provider video.

**KPIs (V3):** launch week — full launch set public, channel sub target from
Launch Campaign (to be set — D8); Weeks 1–8 — 2 uploads/week on schedule,
CTR ≥ 3% (to be measured from baseline, no prior data); Week 90 checkpoint —
playlist views, average view duration, subs.

## 6. Channel 2 — Blog

**Blocker (B1, confirmed 2026-10-13):** the site has **no blog** — `/blog`
returns 404. Only `/guides` and `/press` exist. Before any post publishes,
the blog surface must exist (decision D2: build `/blog` on the existing
Cloudflare Pages Astro site — `site/` in the repo — vs. publishing posts
into the existing `/guides` section).

**The series (V3 §4 — 9 posts, "there is no Blog 10"):**
| # | V3 topic | V3 status (10-03) | On-disk draft (10-02/03 batch) |
|---|---|---|---|
| B1 | 🔍 Confirm (topic TBD) | 🔍 Confirm | Launch-announcement copy exists: `messaging/Press & Announcement Copy.md` ("Introducing TotalRecalls: Never Lose an AI Conversation Again") → D1 |
| B2 | 🔍 Confirm (likely the Library Folder explainer) | 🔍 Confirm | `Jasper/YouTube/Blog/Library Folder Explainer Blog.md` (100% written) → D1 |
| B3 | Markdown vs JSON: Which Saved File Should You Use? | ✅ Written | `Blog/Markdown vs JSON Explainer Blog.md` (100%) |
| B4 | What "Not Sent to Our Servers" Means in TotalRecalls | ✅ Written (second-person privacy review required) | `Blog/Privacy Explainer Blog 4.md` (100%) |
| B5 | How to Back Up Your AI Conversation Library | ✅ Written | `Blog/Backup Library Blog 5.md` (100%) |
| B6 | Searching saved chats with Windows Search | ⏳ Pending in V3 (write by Week 6) | **Written since V3:** `Blog/Windows Search Blog 6.md` (100%, 10-03) |
| B7 | Organizing saved chats by project | ⏳ Pending in V3 (write by Week 7) | `Blog/TotalRecalls Blog Post 10.md` — "PowerShell" (100%, 10-03) is a candidate for this slot → D1; V3's own "by project" framing is not yet drafted |
| B8 | Using saved chats in a note-taking app (Obsidian) | ⏳ Pending in V3 (write by Week 8) | **Written since V3:** `Blog/TotalRecalls Blog Post 7.md` (Obsidian, 100%, 10-03) |
| B9 | How to Use Your Saved AI Chats in VS Code | ✅ Written | `Blog/VS Code Blog Post 9.md` (100%) |

**Note:** V3's tracker (dated 10-03) predates the 10-03 Jasper blog batch, so
B6 and B8 show "Pending" in V3 but have complete drafts on disk. On disk
status wins; the V3 statuses above are the source for the *topics*, the on-disk
files are the source for the *drafts*.

**Extra drafts on disk (outside the 9-post series):**
- `Blog/TotalRecalls Blog Post 8.md` — "How to Back Up Your Saved AI
  Conversations on Windows 10/11" (100%). Overlaps B5's backup topic → D1
  (merge into B5 or hold as a guide).
- `Blog/Free vs Pro Explainer Blog.md` — "Free vs Pro, Explained Plainly"
  (100%; pairs with the pricing page and the Day-42 urgency post — must use
  the D5-resolved free-tier wording).

**Publishing schedule (V3 §12 + 60-Day calendar):**
- Week 3 (launch): launch post (B1, once D1 confirms the topic) live on
  launch day; founder story (`messaging/founder/Founder Story — Why I Built
  TotalRecalls`, 2 variants + "ANDRE DENIS" profile) on Day 5.
- Week 5–8 (Pro Coverage & Explainers): B3–B6, one per week, each with its
  companion video/social set (see §7 calendar).
- Week 9–12 (Trust & Ownership): B7–B9 (+ any D1-merged extras).
- Urgency post: "Launch Pricing Ends Soon" (`Press & Announcement Copy.md`
  + Day-42 row of `strategy/TotalRecalls 60-Day Launch Content Calendar.md`)
  — publish ~2 weeks before the launch discount expires (date to be set —
  D6; the live config carries a discount id with no visible expiry).

**Blog rules (V3 §4):** standard structure (meta title + short answer +
steps + "keep it on your machine" close); one job per post; no provider
spotlights/logos/implied partnerships; third-party apps named as plain text;
CTA per the hierarchy; provider claims verified against the app before
publish (accuracy guardrail). Internal linking: homepage → post →
download/buy; each post links the matching YouTube video.

## 7. Channel 3 — Social media

**Accounts (per the strategy docs — product-focused channels, no personal
accounts):** Facebook, Instagram, LinkedIn (company profile), X (Twitter).
All 4 already have launch-day post variants written.

**What's written (on disk):**
- `social/facebook/Facebook Posts — all variants.md` — 5 variants
- `social/instagram/Instagram Captions — all variants.md` — 4 variants
- `social/linkedin/LinkedIn Posts — all variants.md` — 4 variants
- `social/x/X (Twitter) Posts — all variants.md` — 5 variants
- `Jasper/Social media/Content Calendar.md` — **Day 0–29 calendar (30 days)
  across 7 surfaces**: Instagram (21 posts), LinkedIn (16), TikTok (14),
  X (22), Threads (16), Facebook (18), plus 6 Blog rows tying the calendar
  to the blog series. No Reddit/Discord rows in this calendar. This is the
  primary social sequencing doc.
- `Jasper/Social media/{Social Media Campaign, TotalRecalls Social Media
  Campaign, Untitled Document (1)}.md` — 3 Day 0/3/10 post bodies (complement
  the calendar, not dups).
- `ops/Launch-Day Social Posting Checklist.md` — launch-day runbook
  (timing, stagger order, asset list, UTM tags, comment monitoring).

**Launch-day execution (from the Launch-Day Checklist):**
- Pre-launch (before 8:00 AM): confirm blog live, email scheduled, pull asset
  list (Claude demo video 15–30s teaser cut, 8-sources→1-folder graphic,
  Library file-explorer screenshot, logo crops), confirm buy + free-tier
  links, stage UTM-tagged links, pre-stage all 4 posts as drafts.
- Posting order (stagger): 9:00 AM LinkedIn → 9:15 AM X → 10:00 AM Facebook
  → 12:00 PM Instagram (update IG bio link to Free Tier before 12:00).
- Cross-channel: email + blog + LinkedIn all live by 9:00 AM, same narrative
  (losing AI conversations → local ownership). Reference the blog URL in
  Facebook + LinkedIn (not X/IG). Reuse the Claude demo video on FB + LinkedIn.
  No verbatim copy across platforms.
- Monitor comments/DMs across all 4 platforms for the first 4 hours.

**Post-launch cadence (Day 3–29, from the Day 0–29 calendar):** one post per
platform per day per the calendar, rotating the content pillars:
1. **Ownership** (your files, your machine)
2. **Privacy** (no cloud, no account, local-only)
3. **Provider coverage** (8 providers, one app)
4. **Price/urgency** ($24 once, launch window)
5. **Proof** (demo clips, file-explorer screenshots, before/after)

Reddit and Discord: not in the Day 0–29 calendar. The 60-Day calendar and the
launch strategy's channel mix include them as value-first community channels —
every post must answer a real question or link a guide, never a bare CTA.
(If included, cadence is lighter than the paid-style platforms; the calendar
does not schedule them. Concretely for Phase 0, see §10.)

**Scope note (D4):** the calendar also schedules TikTok (14 posts) and Threads
(16 posts), but neither appears in the launch-day checklist or the strategy
channel mix — decide whether to operate them or keep those rows as reference.

**Social rules (V3 §9 + content audit):** product-focused voice, no
personal-branding, no provider logos implying partnership, one CTA per post
(from the hierarchy), UTM tags on every link
(`?utm_source=<platform>&utm_medium=social&utm_campaign=launch`), no
identical copy across platforms.

## 8. Supporting channel — Email (written, low-cadence)

**Model (V3 §10 — deliberately minimal):**
- Source: footer signup on the site only (no gated content, no lead magnets).
- Frequency: only when there's real news (new feature, new provider, macOS/
  Linux progress). Blog mentions allowed as a short line inside a real
  update — never an email for a blog post alone.
- Platform rule: macOS and Linux stay "in development," no dates.
- One-click unsubscribe in every email.

**What's written (on disk):** a 4-email program with 19 variants —
`email/sequences/` (Welcome + Seq 1 Core Welcome/Onboarding, Seq 2
Free-Tier→Pro Upgrade, Seq 3 Launch Urgency) and `email/slot-2|3|4/` (Email
2: 6 variants incl. "Why $24 once beats $10 a month" + "48 hours left at
$24"; Email 3: 7 variants incl. "No cloud. No account. Just your files.";
Email 4: 3 variants, the final unlock-all-8 offer). Plus
`Jasper/Website Rewrite/Footer Signup Success Messages.md` for the signup
thank-you.

**Execution:** pick one variant per slot (the "alt"/"(variant N)" rows are A/B
material for the test roadmap — see the Missing Items Checklist 2.9), wire the
Prospect → Free-Tier → Buyer bucket automations (Missing Items 2.6), and send
Day 1 Welcome on launch day (per the Launch-Day Checklist). The rest of the
sequence fires on the V3 minimal cadence, not on a fixed timer.

**Note:** the pre-V3 Launch Marketing Plan's heavier 60-day email program is
superseded by V3's "real news only" rule — use it only if the user decides to
go aggressive (D3).

## 9. Funnel & leak points

From V3 §11 "How Everything Connects" + the Launch-Day Checklist:

- **Discovery** (YouTube launch set, social Day 0–29, guides/SEO, Reddit)
  → **Evaluation** (site homepage → See It Work / demo → pricing) →
  **Trial** (Free Tier download: ChatGPT/Claude/Perplexity, 5 conversations
  — wording per D5) → **Purchase** (Pro $24, Paddle) → **Retention**
  (footer email on real news; provider-guide + explainer content).
- Every asset carries the CTA hierarchy; every link is UTM-tagged so
  video → blog → social → email are measurable as one funnel.
- Cross-references are already written into the content: each provider guide
  embeds its video; each blog post links its video; each video's description
  links the guide; the Day 0–29 calendar's 6 Blog rows tie social to the blog.
- The single tracking sheet (V3 Weeks 1–2 "Systems") records, per video and
  per blog post: title, claims, date, version, UTM campaign, status. This is
  the KPI baseline generator (there is no pre-launch traffic data — baselines
  are "to be measured" until Week 8's first monthly metrics review).

**Leak points (measured/verified 2026-10-13 where marked):**

| Stage | Instrumentation needed | Leak risk |
|---|---|---|
| Discovery | GSC (verified 2026-10-01) + GA + launch UTMs from Week 0 | no traffic baseline exists — "to be measured" until Week 8 |
| Evaluation | per-page GA | blog surface is 404 (verified) — the 9-post series has nowhere to publish until D2 lands |
| Trial (download) | download counters | **SmartScreen: no code signing** (roadmap-only per /download/) — first-launch warning is the #1 trial-conversion leak; Windows 11 Smart App Control may block with no override |
| Purchase | Paddle analytics | launch discount `dsc_01m398…` has **no visible expiry** (D6) — urgency copy has nothing to point at; free-tier wording conflict (D5) can make the trial feel broken |
| Retention | ESP dashboard | ESP not chosen (D9); footer signup unwired until Week 0 tasks done; no other update channel (V3 "real news only") |

## 10. Phase 0 (launch week) — zero-cost only

The launch-day runbook itself (`ops/Launch-Day Social Posting Checklist.md`)
is the operating doc for the day; these are the prerequisites + zero-cost
acquisition plays that must land first:

- [ ] **D5 — Free Tier wording:** verify the limit in the app (run the EXE, try a 6th conversation on ChatGPT), then fix whichever page is wrong. Everything inherits this wording.
- [ ] **D6 — discount expiry:** set the date in Paddle (`dsc_01m39879ga7pv9zg0gsvzqsmjw`) and publish it on /pricing/. Anchors the Day-42 urgency post.
- [ ] **D7 — YouTube:** open Studio, count the private "Start Here" videos, upload the missing Qwen video; complete the OAuth consent fix (recipe in `docs/STATUS-2026-10-01-youtube-launch.md`) and verify one API upload.
- [ ] **D2 — blog surface:** build `/blog` on the Cloudflare Pages Astro site (`site/`) or decide `/guides`. Currently 404 (curl-verified 2026-10-13). Gates the B1 launch-day post.
- [ ] **Launch-day social:** pre-stage the 4 posts as drafts (LinkedIn 9:00 → X 9:15 → FB 10:00 → IG 12:00), UTM-tagged, stagger per the checklist; IG bio link → Free Tier before 12:00; monitor 4 hours.
- [ ] **YouTube launch set:** all 9 "Start Here" videos public on launch day; 3 launch playlists; pinned comment on every video; descriptions from the templates.
- [ ] **Community posts (value-first, one per venue, no bare CTAs, accuracy guardrail applies):**
  - r/ChatGPT + r/ClaudeAI — "I built a tool that downloads your entire conversation history as local Markdown files" angle (the "TIL you can export…" thread pattern already exists in these subs); lead with what the user keeps (files, search, backup), not a promo.
  - r/ObsidianMD — the B8 angle (saved chats as Obsidian notes) — publish when B8 lands (Week 8), not launch day.
  - r/windows — the B6 angle (Windows Search over saved chats) — when B6 lands (Week 6).
  - Show HN / HN — founder story + product ("I built TotalRecalls after losing X months of AI conversations") — launch day or Day 5 with the founder post.
  - **Do NOT claim:** provider partnerships, support from any of the 8 companies, or stats not in §1/§2.
- [ ] **Directories:** submit to AI-tool directories (AlternativeTo, Product Hunt-adjacent AI roundups, etc.) — product page + one-liner from §4.
- [ ] **Instrumentation:** GA + launch UTMs live (GSC already verified), single tracking sheet created (video + blog rows).

## 11. Months 2–3 engine

**SEO matrix (pages × target queries × intent):**

| Page | Target queries (long-tail, how-to) | Intent |
|---|---|---|
| 8 provider guides (upgrade per V3 Wk 5–8) | "how to export chatgpt conversations" / "…claude…" / "…perplexity…" / "…gemini…" / "…grok…" / "…deepseek…" / "…mistral…" / "…qwen…" | high-intent how-to — the acquisition backbone |
| B3 Markdown vs JSON | "markdown vs json chat export", "which export format for ai chats" | informational |
| B4 Privacy explainer | "is it safe to export ai conversations", "ai chat data privacy" | trust |
| B5 Backup library | "back up ai conversations", "chatgpt backup local" | how-to |
| B6 Windows Search | "search saved ai conversations windows", "windows search markdown files" | how-to |
| B7 Organizing by project | "organize ai notes by project" | how-to |
| B8 Obsidian | "import chatgpt obsidian", "ai conversations obsidian notes" | how-to (community overlap → r/ObsidianMD post) |
| B9 VS Code | "view ai chat history in vs code" | how-to (VS Code community = future partnership surface) |
| Free vs Pro (extra draft) | "totalrecalls free vs pro" | commercial |
| Library Folder page (V3 Wk 3–4) | "totalrecalls library folder" | product |

Internal linking per §6 blog rules; sitemap + GSC already live — new URLs
must land in the sitemap (Astro: check sitemap plugin config when /blog is
built).

**Email (months 2–3):** the 4-email program stays on V3's "real news only"
cadence; the Prospect → Free-Tier → Buyer bucket automations (Missing Items
2.6) make the Free→Pro email (Seq 2) fire on behavior, not on a timer. The
Day-42 urgency email (Seq 3) is tied to the D6 expiry date.

**Partnerships / communities (zero-cost first):** Obsidian community (B8 is a
natural fit — community posts, not paid placement), VS Code community (B9; a
future VS Code companion would be the partnership surface — product decision,
not a launch commitment), YouTube: reuse the Claude hero cut in Shorts
(2–3/launch week per V3), no collab commitments in the 12-week window.

**Paid (deferred — only after the Week-8 KPI review):** `ads/` already has
written copy for 5 networks. Sequence: run the zero-cost engine for 8 weeks →
first metrics review → paid only if (a) Free→Pro conversion ≥ 8% by day 60
AND (b) the CTR ≥ 3% baseline holds — i.e., the funnel converts before it is
amplified. Kill criteria: either condition missed at Week 8, or blended CAC
> $24 (list price) in the first paid flight. Budget ceiling: to be set by the
user at the Week-8 review (none committed in this plan).

**Product commitments to keep (messaging lock):** macOS and Linux "in
development," no dates; "for the life of the product" updates; code signing
once shipped (see Budget) — do not announce before the cert is live.

## 12. 12-week timeline (V3 §12 — the operating schedule)

| Week | YouTube | Blog | Social | Website / Guides / Email |
|---|---|---|---|---|
| **0 — Prerequisites** | Claim @TotalRecalls handles | Confirm B1/B2 topics (D1), B6–B8 topics | — | Final site corrections; visual review checklist; confirm free-tier wording (D5), opt-in (D3), privacy-policy email vendor, filename format + default Library path |
| **1–2 — Accuracy & Setup** | Profile, banner, About, UTM header links, thumbnail template; record/edit/caption launch videos | Apply V3 §5 fixes to B3/B4/B5/B9; second-person review (B4 first); start B6 | — | Pages vs guardrails; archive spotlight drafts; one tracking sheet (video + blog) |
| **3–4 — Launch** | Publish launch set; set trailer; 3 launch playlists; pin comment on every video | Publish B1 (launch day) + B2 (Day 5); finish B6; start B7 | Launch-day runbook (LinkedIn 9:00 → X 9:15 → FB 10:00 → IG 12:00); Free Tier provider sets; 2–3 Shorts | Upgrade ChatGPT/Claude/Perplexity guides + embed videos; embed demo on Homepage & See It Work; Free vs Pro on Pricing; publish Library Folder page; Day 1 Welcome email |
| **5–8 — Pro Coverage & Explainers** | 1 Pro guide video/week from Gemini; Proof Demos same session; launch Going Pro | Publish B3, B4, B5, B6 (one/week); B7+B8 drafts done by Wk 8 | Pro provider sets; B3–B5 posts as they go live | Upgrade all five Pro guides (Gemini opening = Takeout-first); Blog 3 links in every guide; Day 42 urgency post ≈ 2 wks before discount expiry (D6) |
| **9–12 — Trust & Ownership** | Publish Markdown-vs-JSON, "not sent to our servers," Windows search, backup, organizing videos; start Using-Your-Saved-Chats + Troubleshooting; founder video; first Product Update | Publish B7, B8, B9; embed matching videos in B3–B6 | Day 0–29 calendar continues (final-call week = Day 29) | Link all blogs from Ownership Path; embed founder video; first update email only if real news |
| **Day 90 — Checkpoint** | — | — | — | Second metrics review; plan next quarter |

**Weekly operating rhythm (V3 §13, "the minimum week"):** 1 blog post OR 1
video on schedule, 3–5 social posts, comment/DM monitoring, tracking sheet
updated — this is the floor, not the ceiling.

## 13. KPIs (targets from the Launch Campaign objectives; baselines to be measured)

| KPI | Baseline | Target | How measured |
|---|---|---|---|
| Landing-page unique visits | to be measured (GSC + site analytics from Week 0) | 5,000 / 60 days | GSC + GA, launch campaign UTMs |
| Free-tier → Pro conversion | to be measured (Paddle + download counts from Week 3) | ≥ 8% by day 60 | Paddle checkout vs Free Tier downloads |
| Pro purchases | 0 | 1,000 by campaign end | Paddle |
| Combined social following (X + LinkedIn + FB) | to be measured (current follower counts, Week 0) | +2,000 / 60 days | Platform dashboards |
| Email sign-ups | 0 | 500 | Footer signup / email platform |
| YouTube | 0 subs | sub target TBD (D8); CTR ≥ 3% from first public week (no prior data) | YouTube Studio |

## 14. Budget

| Item | Cost | Why (or why deferred) |
|---|---|---|
| OV code-signing cert (e.g. Sectigo / GoGetSSL / DigiCert — get a quote) | ~$100–400/yr depending on CA (quote at purchase; not a committed figure) | **The long pole — start in Week 0.** SmartScreen warnings kill trial conversion (the #1 leak, §9); issuance + identity verification takes days |
| Domain + hosting | $0 | Cloudflare Pages free tier; domain already owned; GSC verified |
| Email ESP | $0 at launch | 500-signup target fits the free tiers of common ESPs (Brevo/MailerLite/ConvertKit — pick in D9) |
| Social / YouTube / Reddit | $0 | existing accounts; zero-cost channels only in the 12-week window |
| Paid ads | $0 until Week-8 kill criteria pass | solo operator, no activation data yet; §11 defines the gate (≥8% Free→Pro, CTR ≥3%, CAC < $24) |
| **Phase-0 total** | **≈ cert only** | everything else is zero-cost by design (one-operator reality) |

## 15. Risks

| Risk | Likelihood | Mitigation | Owner |
|---|---|---|---|
| SmartScreen / Smart App Control blocks trials (no code signing) | High | cert ordered in Week 0 (long pole); /download/ already discloses the warning; "More info → Run" path documented in FAQ | Andre |
| Launch discount expires silently (no visible expiry in live config) | Medium | D6 sets the date before Week 3; Day-42 urgency post points at it | Andre |
| Free-tier wording conflict confuses trial users (D5) | Medium | verify in-app first, fix the wrong page before launch — everything inherits the wording | Andre |
| YouTube OAuth `403 org_internal` blocks API uploads at launch | Medium | consent fix recipe in STATUS-2026-10-01; fallback = manual upload (9 videos, one session) | Andre |
| Blog 404 gates the Week-3 launch post | High (404 verified 2026-10-13) | D2 in Week 0–1; if the Astro build slips, fallback (b) = publish under /guides | Andre |
| Provider-specific claim ships unverified (per-provider limits differ) | Medium | accuracy guardrail (V3 §14): nothing ships unverified; 🔍 Confirm list in §16 | Andre |
| macOS/Linux demand with no ETA | Medium | messaging locked "in development," no dates — never announce before shipped | Andre |
| Solo-operator bandwidth (2 videos/wk + weekly blog + daily social for 12 weeks) | High | "the minimum week" floor (V3 §13); TikTok/Threads off by default (D4); community posts batched, not daily | Andre |
| Multi-estimate market numbers get quoted wrong in copy | Low | §2 numbers are dated + sourced; copy uses only §1 proof points, never §2 stats (stats are context, not claims) | Andre |

## 16. Decision items (user picks before public/paid action)

| # | Decision | Options | Default if unchosen |
|---|---|---|---|
| D1 | Blog B1/B2 topics + the 3 extra drafts (PowerShell, Backup-Windows, Library Folder) | (a) B1 = launch announcement, B2 = Library Folder explainer, PowerShell → B7 "organizing" slot, Backup-Windows merged into B5, Library Folder also gets its own page (V3 Week 3–4 "publish the Library Folder page"); (b) keep V3's "confirm topics" open and wait for Jasper | (a) — matches the on-disk drafts and the Week 3–4 website task |
| D2 | Blog surface | (a) build `/blog` on the Cloudflare Pages Astro site (`site/`); (b) publish the series under the existing `/guides` section | (a) — V3's internal linking and the Day 0–29 calendar's Blog rows assume a distinct blog URL |
| D3 | Opt-in model for footer signup | (a) single opt-in (simpler, V3-era default); (b) double opt-in (cleaner list) | (a), flagged in V3 Week 0 as 🔍 Confirm |
| D4 | TikTok + Threads (in the Day 0–29 calendar, absent from the launch-day runbook) | (a) operate them; (b) keep the rows as reference, post only on FB/IG/LinkedIn/X | (b) — 4 channels is the solo-operator floor |
| D5 | Free Tier wording: "5 conversations **each**" (homepage) vs "**per download**" (/download/) | (a) per provider (3 providers × 5 = 15 total); (b) per download session — fix whichever page is wrong | (a), matching the pricing page and the app's actual limits — verify in-app first, then fix the /download/ page |
| D6 | Launch-discount expiry date (live config has discount id `dsc_01m398…` but no visible expiry) | set the date in Paddle + publish it on /pricing/ | no date = the Day-42 urgency post has nothing to point at — set a date before Week 3 |
| D7 | Actual private-video count in "Start Here" (status note says 8 uploads; worklist lists 7 providers + hero) | count in Studio, upload Qwen to reach the full 8 | count + upload Qwen |
| D8 | Channel-sub target for launch week (Launch Campaign gives no YouTube number) | set a number | 250 subs by Week 8 (to be set) |
| D9 | Email service provider for footer signup (must be named in the Privacy Policy — V3 Week 0 🔍) | pick + name in policy | — |
| D10 | ~~Delete the file-locked `email/Email Sequence (fragment).docx`~~ **DONE 2026-10-13** — file unlocked and deleted | — | — |

## 17. Source list

**Live site (fetched/curl-verified 2026-10-13):**
- https://totalrecalls.app/ (apex 200, www 200) — homepage, provider list, free-tier wording
- https://totalrecalls.app/pricing/ — $24 launch / $48 normal
- https://totalrecalls.app/download/ — v1.0.0, ZIP ~17.8 MB, code-signing status, free-tier wording conflict
- https://totalrecalls.app/js/config.js — Paddle (16× `paddle`/`Paddle` refs), `pri_01m37qpx77bst2w1gnf3zkf4zd`, `dsc_01m39879ga7pv9zg0gsvzqsmjw`
- https://totalrecalls.app/guides/ (200), /press/ (200), /blog (404), /robots.txt (200), /sitemap.xml (200)

**Marketing corpus (all under `marketing/`, indexed by `marketing/README.md` 2026-09-29):**
- `Jasper/YouTube/Master Implementation Plan V3.md` (10-03) — operating document of record
- `meta/GAP_ANALYSIS_2026-09-29.md`, `meta/GAPS-2026-10-02-blogs-social.md` — gap findings
- `Jasper/tools/reports/deleted-manifest.txt` (2026-10-13) — full dedupe trail
- `docs/STATUS-2026-10-01-youtube-launch.md` — channel state + OAuth fix recipe
- `TotalRecalls Master Launch Document.md` (324 KB, 10-03) — master compendium

**Market context (fetched 2026-10-13, all dated):**
- ChatGPT 900M WAU + 50M paid subs — OpenAI, Feb 2026 (techcrunch.com, 2026-02-27)
- ChatGPT 1.2B weekly — OpenAI DevDay 2026 keynote, 2026-09-29 (openai.com/index/devday-2026-recap)
- Claude 100M+ weekly users — Anthropic announcement, April 2026 (diaryofatoken.com retrospective of the 2026-04-10 announcement)
- Claude 56M mobile-app MAU Q2 2026; ChatGPT 1B app users May 2026 — Sensor Tower via techtimes.com, 2026-06-05
- Claude 220M MAU Q1 2026 — presenc.ai (divergent third-party estimate; flagged, not used in copy)
- Single-provider export tools: chromewebstore.google.com (ChatGPT Exporter extension), github.com/rashidazarang/chatgpt-chat-exporter (userscript), martiansoftware.com/chatkeeper (ChatKeeper), pactify.io (comparison, 2026)
- AI-memory/second-brain category: adityaarsharma.com comparison (7 systems), secondbrain.fyi, m-i-n-d.ai, evermind.ai — category context only

## 18. Next actions (ordered, this week)

1. **Code-signing cert (the long pole — start today):** order an OV cert for totalrecalls.app + the EXE (Sectigo/GoGetSSL/DigiCert — compare quotes). SmartScreen is the #1 trial leak (§9); issuance + verification takes days.
2. **D5 first** — verify the Free Tier limit in the app (run the EXE, try a 6th conversation on ChatGPT), then fix the wrong page. Everything (blog, email, social, pricing) inherits this wording.
3. **D6** — set the launch-discount expiry in Paddle; it anchors the Day-42 urgency post and the pricing-page copy.
4. **D7** — open YouTube Studio, confirm the private count, upload the Qwen video; complete the OAuth consent fix and verify one API upload.
5. **D2** — stand up `/blog` on the Astro site (or decide `/guides`); this gates the B1 launch-day publish. Check the Astro sitemap config so the new URLs land in sitemap.xml.
6. **D1** — confirm the B1/B2 mapping; apply the V3 §5 consistency fixes to B3/B4/B5/B9 and run the second-person review (B4 first).
7. Write the 9 video descriptions from the templates + pinned comments; pre-stage the 4 launch-day social posts as drafts with UTM links.
8. Pick one email variant per slot + D3/D9 (opt-in + ESP), wire the footer signup, test the Welcome send end-to-end.
9. Set up the single tracking sheet (video + blog) and the Week-0 instrumentation (GSC already verified; add GA/UTMs) so the Week-8 metrics review has baselines.
