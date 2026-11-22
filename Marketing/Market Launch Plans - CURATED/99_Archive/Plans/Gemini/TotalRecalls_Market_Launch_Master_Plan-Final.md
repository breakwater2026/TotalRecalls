# TotalRecalls — Market Launch Master Plan & Content Repository

**Document Status:** Consolidated Master Launch Plan & Content Repository (Deduplicated)
**Consolidation Date:** October 23, 2026
**Core Objective:** Single unified operating blueprint for TotalRecalls market launch across YouTube, Blog, Social, Email, and Community Channels.

---

## 1. Executive Summary & Strategic Foundations

#### 1. Executive Summary
TotalRecalls is a $24 one-time Windows desktop app in a category crowded with browser extensions. The closest comparable desktop product found, AI Chat Importer, charges £29 one-time and covers 4 providers versus the 8 listed on the TotalRecalls site ([ai-chat-importer.com](https://ai-chat-importer.com/), [totalrecalls.app](https://www.totalrecalls.app)). The defensible advantages, based strictly on what the website states: provider breadth (8 services listed, including Perplexity, Gemini, Mistral and Qwen), a desktop workflow where users sign in to providers inside the app (rather than importing official export ZIPs), and plain Markdown + JSON output in a folder the user controls.
This plan treats the launch as a  **validation-first launch** : a launch-readiness gate, then a 90-day phased program built around one primary channel (YouTube demonstration content) and one supporting channel (relevant communities, disclosed and rule-compliant), with Product Hunt as an optional launch event and X/LinkedIn as repurposing channels. Scaling decisions are tied to observed activation and purchase data, not dates.
Cloudflare analytics for totalrecalls.app, pulled directly on 2026-10-23 with all TotalRecallsAudit traffic (unknown operator) excluded, show about 1,489 visits and 1,612 pageviews in the last 7 days. That is down about 16% from the prior week, not the +39% the earlier dashboard figures suggested. Over the last 30 days there were about 6.6k visits and 7.0k pageviews. Canada (≈ 37%) and the United States (≈ 33%) lead 30-day visits, and Windows is the leading identified OS. The totals still include other automated traffic, and referrer data isn't available on the current plan. See Section 11 for the full baseline and its limits.
The single most important strategic idea:  **market the demonstrated workflow, not feature lists.**  Every asset shows the same loop: sign in to your AI provider inside the app → download your conversations → open the resulting .md files in Notepad or a notes app → find them again with search. In a market where users are skeptical of yet another AI utility, recorded proof beats promises — and nothing may be claimed that has not been recorded for real.

--------------------------------------------------------------------------------


## 2. Verified Product Snapshot & Claims Register

#### 2. Product Information Sheet (Website-Stated, Not Independently Tested)
Everything in this plan is built on the following website-stated information, collected 2026-10-23, or explicitly labeled as an assumption. No claim below has been tested by installing and operating the application.

##### Website-stated information

| Item | Detail | Source |
| ------ | ------ | ------ |
| What it is | Local Windows desktop app (portable TotalRecalls.exe, no installer, plus README.txt) that downloads AI conversations | [totalrecalls.app/faq<br>](https://www.totalrecalls.app/faq) |
| Providers | ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral, Qwen (8) | [totalrecalls.app<br>](https://www.totalrecalls.app) |
| Output | Markdown + JSON files in a local Library folder (example path C:\TotalRecalls\Library\) | [totalrecalls.app<br>](https://www.totalrecalls.app) |
| Free tier | ChatGPT, Claude, Perplexity; FAQ wording:  **"5 conversations per download"** | [totalrecalls.app/faq<br>](https://www.totalrecalls.app/faq) |
| Paid tier | **$24 USD one-time launch price** ; covers the core download tool with free updates to it for the life of the product; add-ons (semantic search, Obsidian/Notion sync, RAG containers, multi-device memory) listed as separate purchases | [totalrecalls.app/faq<br>](https://www.totalrecalls.app/faq) |
| Privacy claims (site's wording) | "Session tokens stay on your machine"; "never hosts your chats, downloads, or credentials"; "no telemetry"; suggests verifying with Wireshark | [totalrecalls.app/faq<br>](https://www.totalrecalls.app/faq) |
| Accounts | No TotalRecalls account; users sign in to each AI provider locally inside the app | [totalrecalls.app<br>](https://www.totalrecalls.app) |
| Platforms | Windows 10/11 now; Linux and macOS "in the works" | [totalrecalls.app<br>](https://www.totalrecalls.app) |
| Known friction | First launch may show Windows SmartScreen prompt; site links to a SmartScreen guide | [totalrecalls.app<br>](https://www.totalrecalls.app) |
| Refunds | Handled case by case; Quebec consumer cancellation rights explicitly preserved | [totalrecalls.app<br>](https://www.totalrecalls.app) |

##### Word-of-caution: free-tier wording discrepancy (fix before launch)
The retrieved homepage summary describes the free tier as "5 conversations per provider," while the FAQ says "5 conversations per download" ([homepage](https://www.totalrecalls.app), [FAQ](https://www.totalrecalls.app/faq)). This is a discrepancy between a retrieved summary and the FAQ that needs confirmation against the live pages — the implemented limit is not established either way. Until confirmed, campaign copy provisionally follows the FAQ wording ("5 conversations per download") and avoids any arithmetic combination such as "3 providers × 5 conversations," which implies a quantity that is not established. Confirming the actual behavior and aligning all pages is Gate item 1 — mixed wording is a refund-dispute generator.

##### What is NOT established (never use in marketing until tested)

*  Whether downloads capture  **attachments, images, or conversation branches**  — untested.
*  Whether downloads are complete for long histories or subject to provider rate limits in practice.
*  Whether the app operates identically with no browser running (it is a desktop app; sign-in flows may still use system browser components).
*  Code signing status — the SmartScreen warning suggests the executable's reputation is not yet established; do not claim or imply it is "trusted by Windows."
*  Baseline traffic was pulled from the Cloudflare API for the totalrecalls.app zone on 2026-10-23, with all TotalRecallsAudit traffic excluded (Section 11). Other automated traffic remains in the totals, so they are not a human acquisition baseline. Traffic sources (referrers), download actions and sales data are not available (Gate item 8).

##### Planning assumptions (to be replaced with real data)

| Assumption | Working value | Replace with |
| ------ | ------ | ------ |
| Conversion (site visit → Pro purchase) | Unknown; set no target until 2 weeks of data exist | Cloudflare Analytics + payment records |
| Net receipts per Pro sale | Illustrative ~$22 after assumed payment fees (~3.5% + $0.30) and a small refund allowance; excludes support and maintenance costs, so it is  **not**  net contribution | First 30 days of sales data |
| Refund rate | Unknown | Payment records |
| Founder time available | ~10–15 hrs/week on marketing | Your actual availability |


--------------------------------------------------------------------------------

##### 0.2 Claims register — what content may and may not say
**Allowed (website-stated as of 2026-10-23).**  Keep wording close to the site's.

| Topic | Allowed wording | Where the site says it |
| ------ | ------ | ------ |
| What it is | Windows 10/11 desktop app; portable TotalRecalls.exe + README.txt in a ZIP (~17.8 MB); no installer | [Download](https://www.totalrecalls.app/download/), [FAQ<br>](https://www.totalrecalls.app/faq) |
| Providers | ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral, Qwen | [Homepage<br>](https://www.totalrecalls.app) |
| How it gets chats | You sign in to each provider locally, inside the app.  **Gemini is the exception: you point the app at your Google Takeout folder** | [Download](https://www.totalrecalls.app/download/), [FAQ<br>](https://www.totalrecalls.app/faq) |
| Output | One Markdown file and one JSON file per conversation, in a subfolder per provider, inside a Library folder (example C:\TotalRecalls\Library\) or a folder you choose | [See It Work](https://www.totalrecalls.app/see-it-work/), [Download<br>](https://www.totalrecalls.app/download/) |
| What's in the files | Chat text and code blocks as Markdown; attachment references preserved alongside; the binary files themselves stay in your provider account | [FAQ<br>](https://www.totalrecalls.app/faq) |
| Account | No TotalRecalls account, no sign-up | [FAQ<br>](https://www.totalrecalls.app/faq) |
| Price | Pro: $24 USD one-time, discounted launch price, no subscription; all 8 providers; unlimited downloads; up to 3 device activations; free core-app updates; license key by email | [Homepage<br>](https://www.totalrecalls.app) |
| Free Tier | ChatGPT, Claude, Perplexity; 5-conversation limit ( **see 0.3 — wording not yet settled** ); no card, no account | [Download<br>](https://www.totalrecalls.app/download/) |
| Provider accounts | Works with free-tier ChatGPT, Claude, Perplexity, Grok, DeepSeek, Mistral and Qwen Chat accounts; Gemini needs a Google account with Takeout | [FAQ<br>](https://www.totalrecalls.app/faq) |
| Privacy (verbatim only) | "Your AI session tokens stay on your machine." "We never host your chats, your downloads, or your credentials." "No telemetry." You can check the network traffic yourself with Wireshark | [FAQ](https://www.totalrecalls.app/faq), [Download<br>](https://www.totalrecalls.app/download/) |
| Integrity | SHA-256 checksum published on the Download page; verify with Get-FileHash in PowerShell | [Download<br>](https://www.totalrecalls.app/download/) |
| Platforms | Windows 10/11 today; Linux and macOS "in the works"; no mobile | [FAQ<br>](https://www.totalrecalls.app/faq) |
| SmartScreen | First launch may show "Windows protected your PC" → More info → Run anyway; download only from totalrecalls.app | [Microsoft Warning<br>](https://www.totalrecalls.app/microsoft-warning/) |
| Smart App Control | Windows 11 Smart App Control may block unsigned apps with no override; code signing is on the roadmap | [Download<br>](https://www.totalrecalls.app/download/) |
| Release | Version 1.0.0, released October 17, 2026 | [Download<br>](https://www.totalrecalls.app/download/) |
| Trademarks | "Not affiliated with OpenAI, Anthropic, Perplexity, Google, xAI, DeepSeek, Mistral, or Qwen." | Site footer |

**Record before you claim.**  These are on the site but have not been tested for this plan. Use them only after you've filmed them working:

*  Speed ("setup takes a few minutes", "a pick and a click")
*  Very large histories ("a 50,000-message archive works the same as a 500-message one")
*  "Catches conversations the official download tools miss (shared links, archived conversations, partial histories)"
*  Exactly what each provider's files contain (Gate item 5 in the plan)
**Never say:**

*  "Safe", "secure", "100% private", "trusted by Microsoft/Windows" or "virus-free" as a guarantee. Say what the app does and how to check it yourself (SHA-256, Wireshark).
*  "The only…", "the first…", "unlike every other tool…". Other archive tools also save locally and to Markdown.
*  That attachments, images or files are downloaded. Only references are saved.
*  That add-ons (semantic search, Obsidian/Notion sync, RAG containers, multi-device memory) exist or are coming on a date.
*  "Just click Run anyway, it's fine." The SmartScreen framing is always: here's what it is, here's how to check the file, here's how to continue.
*  Anything that implies endorsement by, or partnership with, an AI provider.


## 3. Market Context & Competitive Analysis

#### 3. Market Context
AI chat usage is mainstream and multi-provider usage is common enough that archiving is a real need, but total chatbot usage figures are not the addressable market for a Windows archive utility and are therefore deliberately excluded from this plan. The addressable market is the subset of heavy, multi-provider users whose chats contain reusable work — a smaller group this plan targets deliberately through demonstration content rather than mass messaging.

--------------------------------------------------------------------------------

#### 4. Competitive Landscape (Primary-Source Comparison)

|  | TotalRecalls | AI Chat Importer (desktop) | RecallBase | ChatGPT built-in export |
| ------ | ------ | ------ | ------ | ------ |
| **Type** | Windows desktop app | Windows/Linux desktop app + free web app | Browser extension | Built into ChatGPT |
| **Providers (as stated)** | 8 (incl. Perplexity, Gemini, Mistral, Qwen) | 4 (ChatGPT, Claude, DeepSeek, Grok) | 8+ (incl. Perplexity) | ChatGPT only |
| **How it gets chats (as stated)** | Sign in to each provider inside the app; downloads directly | User requests the provider's official export ZIP, then imports it | Saves via the browser while you chat | Manual export request; ZIP delivery |
| **Price (as stated)** | $24 one-time; free tier: 3 providers, 5 conversations per download | £29 one-time; web app free | Free tier; Pro price not published | Free |
| **Output (as stated)** | Markdown + JSON in a local folder | Searchable local archive | Markdown, PDF, Word, Notion, Obsidian, JSON (free tier limits some) | Provider-specific export |
| **Source** | [totalrecalls.app<br>](https://www.totalrecalls.app) | [ai-chat-importer.com<br>](https://ai-chat-importer.com/) | [recallbase.net<br>](https://recallbase.net/) | [OpenAI Help<br>](https://help.openai.com/en/articles/7260999-exporting-your-chatgpt-history-and-data) |

(Claude's official export options were not verified for this plan; do not make claims about them without checking Anthropic's documentation.)
**What this comparison honestly supports as differentiators:**

1.  **Breadth with direct download.**  AI Chat Importer has a comparable one-time-price desktop model but covers 4 providers and uses the export-ZIP-then-import workflow. TotalRecalls lists 8 providers with in-app sign-in and direct download. This is the core paid-app justification: convenience across the services the customer actually uses.
2.  **Plain files, no proprietary archive.**  Markdown + JSON in a normal folder means no lock-in: Notepad, Obsidian, VS Code, grep, or any backup tool works. (RecallBase also offers Markdown/Obsidian — claim the desktop workflow, not uniqueness.)
3.  **Perplexity, Gemini, Mistral, Qwen coverage.**  RecallBase and AISaver also list Perplexity ([recallbase.net](https://recallbase.net/), [aisaver.app](https://aisaver.app/)) — so frame provider coverage as "covers the services you use," never as exclusive.
**What this comparison does NOT support claiming:**  that competitors are free (RecallBase has an unpublished Pro tier; AI Chat Importer charges £29 — [ai-chat-importer.com](https://ai-chat-importer.com/)), that local storage or Markdown is unique, or that any workflow claim is better until timed personally.

##### Honest "Who should NOT pay for this" section (publish on the site)
Include a short section or FAQ entry: If you use one AI service and only occasionally want a copy of a single chat, your provider's built-in export may be enough. TotalRecalls is for people who use several AI services regularly and want their conversations as plain files on their PC. This candor builds trust, pre-filters refunds, and the launch content should reflect the same honesty.

--------------------------------------------------------------------------------


## 4. Positioning, Messaging & Target Audience

#### 5. Positioning & Messaging
##### Positioning statement
**Keep a copy of your AI conversations on your Windows PC.**  TotalRecalls signs in to the AI tools you already use, downloads your conversations, and saves them as Markdown and JSON files in a folder you control.
Supporting brand line (emotional layer, used in social content): "Your AI conversations belong to you." It needs the concrete workflow underneath it — never use it alone.

##### Message hierarchy

1.  **Why care?**  Your AI work — research, code, drafts, decisions — is scattered across services' sidebars and disappears under newer chats.
2.  **What is it?**  A Windows desktop app that downloads your conversations from the AI tools you already use and saves them as plain files on your PC.
3.  **Why this?**  One app for the providers you use; sign in and download directly (no export-ZIP dance); plain Markdown + JSON in a folder you control; no account with us, no subscription — $24 once.
4.  **Do this.**  Download the free tier and pull your first conversations in the next ten minutes.

##### Tagline options (test in thumbnails and titles)

*  "Recall every AI conversation."
*  "Your AI chats, saved as files on your PC."
*  "Eight AI tools. One folder on your PC."

--------------------------------------------------------------------------------

#### 6. Target Audience
**Primary segment (single focus for launch):**
Windows users who regularly use  **two or more**  of the supported AI services, have valuable research, drafts, or code scattered across conversations, and want reusable local files.
Likely subsegments (pick ONE to lead with after validation, not four simultaneous campaigns):

| Subsegment | Why they may care | Where they gather | Validation signal to look for |
| ------ | ------ | ------ | ------ |
| Developers | Code-heavy chats, multiple providers, notes-app users | Reddit, X, YouTube dev content | Comments mentioning "I lost a snippet" |
| Researchers/consultants | Long research threads they re-open weeks later | LinkedIn, Reddit, YouTube | Comments mentioning "can't find that chat" |
| Writers/creators | Drafts and brainstorms worth keeping | YouTube, X, writing communities | Saves/bookmarks on demo videos |

**Recommended validation step (Week 1, before scaling anything):**  ask 5–10 heavy AI users (your own network, a community thread, or people who download the free tier) to do their first export while you watch. Record where they hesitate. One afternoon of observation will improve the funnel more than any ad spend.

--------------------------------------------------------------------------------

##### 0.5 Tracked links (UTM scheme)
Referrer data isn't available on the current Cloudflare plan (Launch Plan, Section 11), so every link carries UTM tags. Use the homepage or the specific guide page — not a direct ZIP link — so the SmartScreen and Smart App Control notes are seen before the download.
```
https://www.totalrecalls.app/?utm_source={source}&utm_medium={medium}&utm_campaign=launch&utm_content={asset_id}

```

| Channel | utm_source | utm_medium |
| ------ | ------ | ------ |
| YouTube long-form | youtube | video |
| YouTube Shorts | youtube | short |
| TikTok | tiktok | short |
| Instagram | instagram | social |
| Facebook | facebook | social |
| Reddit | reddit | community |
| LinkedIn | linkedin | social |
| X | x | social |
| Product Hunt | producthunt | launch |
| Hacker News | hackernews | community |

Example: https://www.totalrecalls.app/?utm_source=youtube&utm_medium=video&utm_campaign=launch&utm_content=v1
Notes:

*  Reddit and Hacker News readers distrust tracked links. In those posts, use the clean URL https://www.totalrecalls.app and judge results from the date of the post instead.
*  TikTok and Instagram don't allow clickable links in captions. Put the link in your profile (bio link) and say "link in profile".
*  A UTM tag is part of the URL and is visible in your own server/Cloudflare data. It doesn't add tracking to the site, so it's compatible with the site's "no analytics, no tracking pixels" statement. Keep it that way: don't add pixels or tag managers to the site for this launch.
*  Before launch, check that UTM query strings show up in the Cloudflare data you pull (query parameters may need the request-query field). If they don't, you can still use short, distinct paths per channel (e.g. /yt, /r) that redirect to the homepage.


## 5. Offer, Pricing & Unit Economics

#### 7. Offer, Pricing & Unit Economics
##### Keep the $24 price — do not change pricing before launch data exists
The free-extension competition is not a reason to cut price: the closest desktop analog charges £29 for fewer listed providers ([ai-chat-importer.com](https://ai-chat-importer.com/)). Price changes are experiments to run after baseline data exists.
**What the $24 must be shown to buy**  (this is the job of every video and post):

1. All 8 listed providers in one app
2. Sign in and download directly (no export ZIP + import)
3. Plain Markdown + JSON files in a folder you choose
4. Free updates to the core tool for the life of the product; 3 device activations

##### Unit economics (illustrative until real data arrives)

| Item | Value |
| ------ | ------ |
| List price | $24.00 |
| Payment processing (assumption ~3.5% + $0.30) | −$1.14 |
| Refund allowance (assumption 3%) | −$0.72 |
| **Illustrative receipts per sale** | **≈ $22.14**  — excludes support time and ongoing compatibility maintenance, so treat as receipts, not contribution |

The allowable acquisition cost threshold below is  **provisional**  — a working hypothesis to replace with observed unit economics, not a demonstrated affordable CAC.

| Item | Value |
| ------ | ------ |
| Provisional CAC ceiling | ≤ $8–11 per sale (roughly 40–50% of illustrative receipts for a bootstrapped product) — revisit after 30 days of data |

The free tier is the trial. Track the funnel from  **download → successful first export → Pro purchase**  — a download alone is not activation. (Measurement approach in Section 11.)

##### Add-on roadmap note
Semantic search, Obsidian/Notion sync, RAG containers, and multi-device memory are listed on the FAQ as separate purchases; availability is not established. Do not market them as available; mention only that the core tool gets free updates. When an Obsidian workflow genuinely exists and is demonstrated, that is a natural second launch moment for the Obsidian community.

--------------------------------------------------------------------------------


## 6. Launch-Readiness Gate List

#### 8. Launch-Readiness Gate (Complete Before Any Promotion)
Nothing in the Content Pack is published until these are green.

| # | Item | Why | Status |
| ------ | ------ | ------ | ------ |
| 1 | Confirm the actual free-tier behavior, then align the homepage, FAQ, checkout, and campaign copy with that behavior (the retrieved homepage summary says "per provider," the FAQ says "per download") | Mixed wording creates refund disputes | ☐ |
| 2 | Confirm pricing consistent everywhere (homepage, FAQ, checkout) at $24 one-time | Checkout surprises kill trust | ☐ |
| 3 | Download works from a clean Windows 10 and Windows 11 machine; ZIP contains exe + README as described | Verify the actual flow end-to-end | ☐ |
| 4 | First-run experience documented: SmartScreen steps shown with screenshots, framed as a reputation check on new apps — never as "just click through, it's fine" | SmartScreen is a potential source of onboarding friction for new apps | ☐ |
| 5 | Test one export per provider (all 8): confirm what is captured (text? images? attachments?) and what the files contain | Marketing can only claim what is tested | ☐ |
| 6 | Support contact visible on the site; refund policy terms readable | Support spikes at launch | ☐ |
| 7 | Payment → license key → activation flow tested end-to-end on 2–3 machines | Broken licensing at launch is fatal to word of mouth | ☐ |
| 8 | Visitor/pageview baseline now pulled from the Cloudflare API, with TotalRecallsAudit excluded (Section 11). Still open: add UTM tagging or another way to see traffic sources, and separately select and test a supported method for measuring download clicks | Without measurement the launch is invisible | ◐ partly done |
| 9 | Code signing status decided (sign the exe if feasible; if not, the SmartScreen guide stays prominent) | Directly affects conversion | ☐ |
| 10 | A 60–90 second "first export" walkthrough recorded from the real app, with sensitive information concealed | This becomes the hero asset for all channels | ☐ |
| 11 | A short "what we do NOT collect" privacy note in the FAQ, in plain language | The Wireshark-verification suggestion is a differentiator; make it easy to find | ☐ |


--------------------------------------------------------------------------------

#### 9. Channel Strategy
One primary channel, one supporting channel, two repurposing channels, one launch event. Do not run five full programs.

##### Primary: YouTube
**Why:**  the product is a "show me" product — a 6-minute screen recording does the entire selling job. Tutorial searches ("export ChatGPT history," "save Claude conversations," "back up AI chats") are intent-rich. Treat search demand as a hypothesis to measure in YouTube Analytics, not an established fact.
**Format plan:**

*  1 hero explainer (6–8 min), full script in the Content Pack
*  3–6 Shorts from the same recording session
*  Ongoing: one provider-specific tutorial per supported service (8 evergreen videos, each targeting "export [provider] history") — released across the 90 days
*  Each video's CTA: free tier download

##### Supporting: Relevant communities (Reddit and forums)
**Why:**  heavy multi-provider AI users congregate and actively discuss losing chats. Rules:

*   **Disclose the founder relationship in every post.**  Undisclosed self-promo gets removed and poisons the well.
*  Read each community's self-promotion rules first; use designated threads or moderator approval where required.
*  Communities to evaluate by fit: r/ChatGPT, r/ClaudeAI, r/PerplexityAI, and Windows/AI-productivity communities. Do NOT use r/LocalLLaMA — local model inference is a different interest than archiving hosted-service chats. Obsidian communities come later, only when an Obsidian workflow is genuinely demonstrated.
*  Lead with the problem ("How do you keep track of your best AI chats across tools?") and participate in unrelated threads before ever mentioning the app.

##### Launch event: Product Hunt (optional, Week 3–4)
Only after the readiness gate passes and the funnel works (first exports happen without support tickets). Prepare: tagline, gallery of 5 images/GIFs from the real app, founder first comment, and be present all day to answer comments. Product Hunt is a spike, not a strategy — capture the traffic with a launch-week offer (e.g., extended trial limits, not a discount, to protect the $24 anchor).

##### Repurposing: X and LinkedIn
Not separate programs. Each YouTube video and community post gets reformatted: X thread (the demo steps as images), LinkedIn post (the product-purpose angle). X/LinkedIn pay off only with consistency — 3 posts/week minimum, all recycled from YouTube material.

##### What NOT to do in the first 90 days

*  No paid promotion until the D28 gate passes (see calendar).
*  No mass cold outreach, no email blasts to purchased lists.
*  No claims about attachments/branches/quality until Gate item 5 is done.

--------------------------------------------------------------------------------

#### 10. 90-Day Launch Calendar
Every item has an owner, status, asset ID (matching the Content Pack), CTA, and measure. Targets are initial hypotheses to replace with observed data. "D" = day relative to launch. Owner is the founder throughout (solo launch).

##### Phase 0 — Readiness (Weeks −2 to 0)

| Day | Action | Asset | CTA | Measure | Status |
| ------ | ------ | ------ | ------ | ------ | ------ |
| D−14 | Complete Launch-Readiness Gate items 1–11 | — | — | All gates green | ☐ |
| D−10 | Record hero video raw footage (real exports, real files, sensitive info concealed) | V1 | — | Recording done | ☐ |
| D−7 | Publish SmartScreen guide screenshots + privacy note to FAQ | W1 | — | Page live | ☐ |
| D−5 | Verify analytics events (download clicks, UTM-tagged campaign links); re-pull the visit baseline with the TotalRecallsAudit exclusion | — | — | Download-click measurement live | ☐ |
| D−3 | Dry-run the funnel with 3 friendly testers (watch them do a first export) | — | — | 3/3 complete an export unaided | ☐ |
| D−1 | Schedule Week-1 posts; YouTube premiere set | — | — | Queue loaded | ☐ |

##### Phase 1 — Validation (Weeks 1–2): prove the funnel with a small audience. Recalibrate the gate thresholds below once a download-click baseline exists (Gate item 8). For context, /download/ received 63 pageviews last week, excluding TotalRecallsAudit (Section 11). That is a count of page loads, not downloads, and the current thresholds are first hypotheses.

| Day | Action | Asset | CTA | Measure (hypothesis) | Status |
| ------ | ------ | ------ | ------ | ------ | ------ |
| D0 | Publish hero video V1 on YouTube | V1 | Free tier | Views → site clicks; establish true baseline | ☐ |
| D0 | Founder post: "I built TotalRecalls — ask me anything" in 1 subreddit (rules-checked, disclosed) | R1 | Free tier | 50 upvotes, 10 comments | ☐ |
| D2 | X thread: the 5-step workflow with screenshots | X1 | Free tier | 1,000 impressions | ☐ |
| D3 | LinkedIn product-purpose post | L1 | Free tier | 500 impressions | ☐ |
| D4 | YouTube Short S1 | S1 | V1 | 1,000 views | ☐ |
| D5 | Publish provider tutorial #1: "Export your ChatGPT history" | V2 | Free tier | Rank in YouTube search for the phrase | ☐ |
| D7 | **Checkpoint:**  review funnel — downloads, first-export signals (feedback, support), purchases, tickets | — | — | Fix top drop-off before more effort | ☐ |
| D8 | X single post (privacy-verification angle) | X2 | Free tier | Clicks | ☐ |
| D9 | Reddit r/ClaudeAI value post (disclosed) | R2 | Free tier | Engagement | ☐ |
| D11 | Short S2 | S2 | V1 | Views | ☐ |
| D12 | Tutorial V3 (Claude) | V3 | Free tier | Search rank | ☐ |
| D14 | **Gate:**  ≥ 30 downloads, ≥ 10 confirmed first exports (via voluntary feedback or support contacts), ≥ 1 purchase | — | — | If missed, fix funnel before Phase 2 | ☐ |

##### Phase 2 — Launch Event (Weeks 3–4): Product Hunt + full content cadence

| Day | Action | Asset | CTA | Measure (hypothesis) | Status |
| ------ | ------ | ------ | ------ | ------ | ------ |
| D15 | Product Hunt launch (Tuesday or Thursday), founder active all day | PH1 | Free tier | Top-10 of day, 300+ site visits | ☐ |
| D15 | X and LinkedIn launch-day posts pointing to PH | X3, L2 | PH page | Amplified spike | ☐ |
| D16 | Publish tutorial V4 (Perplexity — the differentiator hook) | V4 | Free tier | Evergreen search asset | ☐ |
| D18 | Reddit r/PerplexityAI value post (disclosed) | R3 | Free tier | 30 upvotes | ☐ |
| D20 | Short S4 | S4 | V1 | 5,000 views | ☐ |
| D22 | Short S3 | S3 | Free tier | Views | ☐ |
| D25 | Tutorial V5 (Gemini) + X post X4 (objection handler) | V5, X4 | Free tier | Baseline | ☐ |
| D28 | **Gate:**  ≥ 150 cumulative downloads, stable download→Pro conversion (set target from first 4 weeks of data), refund rate < 5% | — | — | Decide Phase 3 scale | ☐ |

##### Phase 3 — Scale or Fix (Weeks 5–12)
Only if D28 gates pass. If they don't, spend weeks 5–6 fixing the funnel and re-run the gates.

| Day | Action | Asset | Measure | Status |
| ------ | ------ | ------ | ------ | ------ |
| D29–60 | Remaining provider tutorials (V6–V8: Grok, DeepSeek, Mistral/Qwen), 1/week | V6–V8 | Search rankings | ☐ |
| D29–60 | Community rhythm: 2 value-first posts/week (90% no-link) | R4+ | Karma, DMs, referrals | ☐ |
| D35 | First small paid promotion test — only if conversion data is solid: $10/day promoting the hero video on one platform, with a hard stop if CAC exceeds the provisional ceiling | A1 | CAC vs provisional ceiling | ☐ |
| D45 | If real user quotes exist by then (with permission), publish a "Who uses TotalRecalls" page | W2 | Conversion lift | ☐ |
| D60 | Obsidian/notes-app angle test: only if the .md files have been tested in Obsidian and genuinely work | V9 | New audience | ☐ |
| D75 | Mid-quarter review: kill weakest channel, double best | — | Unit economics | ☐ |
| D90 | Quarterly review: CAC, conversion, refunds, support load; decide macOS/Linux waitlist messaging | — | Full picture | ☐ |


--------------------------------------------------------------------------------

#### 11. Funnel & Measurement (Privacy-Compatible)
The funnel, honestly defined — each stage is measurable without spying on users:
```
Site visit → Download click → First export (activation) → First reopened file → Pro purchase → Repeat use

```

##### Baseline (Cloudflare zone analytics for totalrecalls.app, pulled 2026-10-23)
This baseline replaces the earlier dashboard-supplied 7-day figures. It was pulled directly from the Cloudflare GraphQL Analytics API (api.cloudflare.com/client/v4/graphql) for the totalrecalls.app zone (Free plan) with a read-only API token.  **Every figure, breakdown, ratio and comparison below excludes the TotalRecallsAudit traffic**  (see exclusion rule).
**Method and scope**

| Item | Detail |
| ------ | ------ |
| Exclusion rule | Every request whose user agent contains TotalRecallsAudit is removed before any metric is computed. This covers both variants found: TotalRecallsAudit/1.0 and Mozilla/5.0 (TotalRecallsAudit). A search for any user agent containing "udit" found no other variants. Operator unknown |
| Datasets | httpRequestsAdaptiveGroups (visits, pageviews, requests, dimensions, filtered by user agent). The 30-day pageview total is the exact httpRequests1dGroups roll-up minus the excluded traffic's pageviews |
| Windows (UTC) | Last 7 days: 2026-10-16 00:00 → 2026-10-23 00:00 · Prior 7 days: 2026-10-09 → 2026-10-16 · Last 30 days: 2026-09-23 → 2026-10-23. Zone data begins 2026-09-22 (partial day, not used) |
| Host scope | All hosts in the zone. Visits are recorded almost entirely on totalrecalls.app (apex); www.totalrecalls.app recorded ≈ 810 visits earlier in the 30-day window and none in the last 7 days. video. and demo-video. subdomains carry requests but no visits |
| Visits | Cloudflare edge-defined visits (a page request whose referrer is not the site itself). Not unique people and not browser-beacon sessions |
| Pageviews | Successful (HTTP 200) HTML responses |
| Sampling | 7-day windows: near-exact (sample interval ≈ 1.1–1.4). 30-day window:  **sampled**  (interval ≈ 13.6), so its breakdowns are rounded estimates |
| Not available on this plan/token | Referrer/source (Free plan), ASN, bot score; Cloudflare Web Analytics (browser beacon) data was not authorized for this token. Threat counts are left out because they can't be filtered by user agent |

**Excluded traffic (documented for traceability only; not part of any analysis)**

| Variant | When (UTC) | Requests | Visits | Origin |
| ------ | ------ | ------ | ------ | ------ |
| TotalRecallsAudit/1.0 | 2026-10-18, 10:00–12:00 (06:00–08:00 Toronto) | 982 | 935 | Canada, Montréal (YUL) data center |
| Mozilla/5.0 (TotalRecallsAudit) | 2026-10-15, 01:00 (Oct 14, 21:00 Toronto) | 58 | 56 | Canada, Toronto (YYZ) data center |

Both variants requested one page per visit across the site (guides, previews, see-it-work pages, help, about), and neither is a Cloudflare-verified bot. The user-agent name does not establish who operates it. The earlier dashboard baseline included this traffic, which inflated Canada's share and produced the reported "+39% visits / +34.5% pageviews" trend. Those figures are superseded.
**Headline figures (TotalRecallsAudit excluded)**

| Metric | Last 7 days | Prior 7 days | Week-over-week | Last 30 days |
| ------ | ------ | ------ | ------ | ------ |
| Visits | **1,489** | 1,768 | **−15.8%** | **≈ 6.6k**  (sampled) |
| Pageviews | **1,612** | 1,911 | **−15.6%** | **≈ 7.0k**  (7,038) |
| Pageviews per visit | 1.08 | 1.08 | — | ≈ 1.06 |
| Visits, also excluding Cloudflare-verified bots | 1,226 | 1,450 | −15.4% | ≈ 5.6k |
| Requests (all hosts) | 14,408 | 13,732 | +4.9% | ≈ 57.7k (sampled) |

Daily visits over 30 days are spiky, with no sustained trend. Single-day peaks were ≈ 440 (10-02), ≈ 540 (10-10), ≈ 900 (10-14), ≈ 470 (10-18) and ≈ 440 (10-22) against a typical 50–250. The causes of the peaks are not identified. Last week was down about 16% from the week before.
**Breakdowns (TotalRecallsAudit excluded)**

| Dimension | Last 7 days | Prior 7 days | Last 30 days (sampled) |
| ------ | ------ | ------ | ------ |
| Countries (visits) | Canada 539 · United States 334 · China 255 · Germany 178 · United Kingdom 37 · Netherlands 33 | Canada 926 · United States 485 · China 121 · United Kingdom 66 · Belgium 34 · Germany 30 | Canada ≈ 2,440 · United States ≈ 2,160 · China ≈ 560 · Germany ≈ 340 · United Kingdom ≈ 270 · Poland ≈ 120 |
| Top paths (pageviews) | / 579 · /download/ 63 · /see-it-work/ 50 · /legals/ 43 · /about/ 36 · /terms/ 31 · /feature-requests/ 28 · /guides/gemini-takeout-archive/ 28 · /guides/grok/ 26 · /buy/ 25 | / 573 · /download/ 82 · /faq/ 47 · /legals/ 40 · /guides/export-perplexity-conversations/ 38 · /guides/ 35 · /guides/qwen/ 34 · /guides/own-your-ai-chat-data/ 34 · /providers/ 32 · /compare/claude/ 32 | / ≈ 3,120 · /download/ ≈ 340 · /see-it-work/ ≈ 200 · /legals/ ≈ 170 · /guides/own-your-ai-chat-data/ ≈ 150 · /guides/export-chatgpt-conversations/ ≈ 150 · /guides/grok/ ≈ 140 · /privacy/ ≈ 130 · /buy/ ≈ 130 |
| Operating system (visits) | Unknown 852 · Windows 250 · Android 218 · iOS 91 · macOS 50 · Linux 28 | Unknown 923 · Windows 522 · Android 144 · iOS 90 · Linux 52 · macOS 37 | Unknown ≈ 3,060 · Windows ≈ 1,800 · Android ≈ 690 · macOS ≈ 470 · iOS ≈ 370 · Linux ≈ 250 |
| Device type (visits) | Desktop 1,141 · Mobile 343 · Tablet 5 | Desktop 1,508 · Mobile 256 · Tablet 4 | Desktop ≈ 5,320 · Mobile ≈ 1,300 · Tablet ≈ 20 |
| Browser (visits) | Unknown 596 · GoogleBot 261 · Chrome 198 · Curl 122 · HeadlessChrome 107 · Mobile Safari 91 · Chrome Mobile 88 | Unknown 826 · Chrome 597 · GoogleBot 115 · Curl 93 · Mobile Safari 87 · Chrome Mobile 33 | Unknown ≈ 2,560 · Chrome ≈ 2,250 · GoogleBot ≈ 460 · Chrome Mobile ≈ 420 · Mobile Safari ≈ 370 · Curl ≈ 300 |
| Cloudflare-verified bots (visits) | Search crawlers 151 · AI crawlers 69 · Security 42 · Page preview 1 | Search crawlers 120 · AI search 113 · Security 41 · AI crawlers 24 · Monitoring 17 | AI crawlers ≈ 320 · Search crawlers ≈ 310 · AI search ≈ 230 · Security ≈ 130 · Monitoring ≈ 20 |
| Data centers (visits) | Montréal 318 · Amsterdam 276 · Newark 154 · Dallas 135 · Frankfurt 97 · Toronto 71 | Montréal 799 · Atlanta 162 · Chicago 151 · Toronto 116 · Amsterdam 78 · London 77 | Montréal ≈ 1,310 · Toronto ≈ 800 · Chicago ≈ 720 · Amsterdam ≈ 540 · Newark ≈ 460 · London ≈ 350 |

**How to read this baseline**

*   **Excluding TotalRecallsAudit does not make the remainder human.**  Unverified automation is still in the totals. Last 7 days: bare Mozilla/5.0 157 visits, curl 121, HeadlessChrome 101, serpstatbot 60, and a short Windows Chrome/120 user agent with no engine string 212. Real human visits are below 1,226/week by an amount these analytics can't measure.
*   **Canada leads, but by much less than the earlier report suggested.**  Canada is ≈ 36% of last-week visits, ≈ 52% the week before, and ≈ 37% over 30 days. The United States is close behind at ≈ 33% over 30 days. Founder and testing traffic is not separately identified, so this is not yet evidence of Canadian demand. Bilingual English/French content remains an optional experiment.
*   **Windows is the leading identified OS over 30 days.**  Among visits with an identified OS, Windows is ≈ 50% over 30 days but ≈ 39% last week (vs ≈ 66% the week before), and Android + iOS are ≈ 30% over 30 days. Unknown OS is 46–57% of visits, so no share of human visitors who can or cannot run the app is established. The mobile fallback CTA ("email yourself the download link") stays an optional experiment.
*   **Path traffic is not outcomes.**  /download/ had 63 pageviews last week, 82 the week before, and ≈ 340 over 30 days. These are page loads, not download clicks or installs; /buy/ had 25 last week and ≈ 130 over 30 days. Recalibrate the D14/D28 gates only against measured download actions.
*   **Guide pages get traffic.**  Provider guides (ChatGPT, Grok, Gemini, Perplexity, Qwen, "own your AI chat data") are a meaningful share of non-home pageviews. This is consistent with the plan's bet on provider-specific tutorial content but doesn't prove it. Their content was not reviewed for this plan.
*   **No source attribution.**  Referrer data is not available on the Free plan, so YouTube, Reddit and Product Hunt can't be compared from these analytics.
*   **App-like requests seen.**  A separate user agent, TotalRecalls/1.0 (+https://totalrecalls.app), made ≈ 40 requests over 30 days (0 visits, so it doesn't affect any figure above). Whether this is the desktop app (e.g., an update check) or a site tool is not established. Since the FAQ says "no telemetry", confirm what sends it and make sure the privacy wording describes it accurately.
*   **Earlier "requests layer" figures retired.**  The previously supplied account-home figures (100.39k requests, Worker invocations, cache rate) had unconfirmed scope. The zone-level request counts above replace them.
**Next measurement steps**

1. Apply the same exclusion (user agent contains TotalRecallsAudit) to every future report, alongside the "also excluding verified bots" line.
2. Try to identify the TotalRecallsAudit operator (check whether any tool, monitor, or contractor you use sends it). If it recurs and is not yours, consider a Cloudflare WAF rule to log or challenge it. That's a configuration decision for you, not part of this plan.
3. Add source attribution: UTM parameters on every campaign link (?utm_source=youtube&utm_campaign=v1, etc.). Also consider enabling Cloudflare Web Analytics, a cookieless browser beacon that provides referrers; adding Account Analytics: Read to the token lets that data be pulled the same way.
4. Measure download clicks and purchases separately (Gate item 8). /download/ pageviews are not a substitute.

| Stage | How it's measured | Notes |
| ------ | ------ | ------ |
| Site visit | Cloudflare zone analytics via API (baseline in Section 11), always excluding user agents containing TotalRecallsAudit and also reporting a view without verified bots | Source attribution needs UTM tags or Web Analytics (Free plan lacks referrers) |
| Download click | Analytics event on the download link | Not an install |
| First export | Not directly measurable without telemetry. Baseline approach: voluntary feedback ("Did your first export work?" prompt or email link) and support-contact monitoring | See note below before adding any in-app telemetry |
| Pro purchase | Payment records | Track conversion from download click |
| Refunds | Payment records | > 5% = product/expectation mismatch |
| Support burden | Ticket count / 100 downloads | Rising = funnel friction |

**Important telemetry caution:**  the site publicly promises "no telemetry" ([FAQ](https://www.totalrecalls.app/faq)). Adding even opt-in usage statistics would change that public promise and is a product/privacy decision to make deliberately — not a marketing decision. Until then, voluntary feedback and support signals are the activation baseline.
**KPI dashboard (weekly):**  downloads, first-export signals, conversion %, CAC (when paid tests start), refund %, YouTube view→site-click rate, top drop-off point.
**Privacy note for all public messaging:**  keep the site's privacy claims verbatim ("we never host your chats or credentials; no telemetry") and never extend them beyond what's written until the app's actual network behavior has been audited.

--------------------------------------------------------------------------------

#### 12. Budget Scenarios (USD)
Paid spending in every scenario starts only after the D28 gate passes.

##### Scenario A — Bootstrap ($0)

*  All organic: YouTube + communities + Product Hunt. Founder time is the budget (est. 10–15 hrs/week).
*  Illustrative planning goal — not a forecast — if the funnel works: a few hundred downloads, early Pro sales, and — most valuably — data.

##### Scenario B — Modest ($500 total)

*  $150: YouTube in-feed promotion of the hero video, ~$5/day for 30 days, starting after D28
*  $150: recording upgrade (decent USB mic) — improves every future asset
*  $200: held in reserve for the channel the data says is working at D60
*   **Total: $500**

##### Scenario C — Serious ($2,000 total, standalone allocation)

*  $600: paid promotion of the hero video, capped at $10/day, from D35 through D90 (~56 days)
*  $400: one sponsorship in a small AI-focused newsletter (founder-story angle)
*  $300: thumbnail design help (highest-leverage spend in YouTube marketing)
*  $700: reserve for the best-performing channel at D60, or a second newsletter sponsorship
*   **Total: $2,000**
*  Hard rule: any channel whose measured CAC exceeds the provisional ceiling is paused, not topped up.

--------------------------------------------------------------------------------

#### 13. Risks & Mitigations

| Risk | Likelihood | Mitigation |
| ------ | ------ | ------ |
| SmartScreen warning kills conversion | High | Sign the executable if affordable; keep the honest guide; show the real prompt inside the hero video so it's expected |
| Free extensions "good enough" objection | High | Never argue price — demonstrate the multi-provider, direct-download, plain-files workflow; publish the honest "when free is enough" section |
| Provider API/interface changes break downloads | Medium | Free core updates are already promised — communicate fixes fast; re-test exports after every provider update |
| Refund disputes from misread free-tier limits | Medium | One exact phrase everywhere: "3 providers, 5 conversations per download" (reconcile homepage vs FAQ first) |
| Reddit self-promo backlash | Medium | Disclose always; give value 90% of the time; follow each community's rules |
| Claims outrun reality (attachments, export quality) | Medium | Gate item 5: test every provider's export before any claim appears in content |
| Unidentified automated traffic (e.g., TotalRecallsAudit) distorts launch metrics | High | Exclude by user agent in every report, keep a "verified bots excluded" view, and judge channels on download clicks and purchases, not visits |
| "Windows-only" cuts the audience | Certain | Frame as intentional focus; a macOS/Linux waitlist page is a cheap demand test and roadmap signal |


--------------------------------------------------------------------------------

#### 14. What I Can Execute From Here (With Your Authorization)
This plan and the accompanying Content Pack are drafts, scripts, and text. With your go-ahead I can also: draft the site copy changes (SmartScreen guide, privacy note, "when free is enough" section), produce the thumbnail images, write the full provider-tutorial scripts (V2–V8), or research any specific competitor further. I will not publish, post, or spend on anything without your explicit approval.

--------------------------------------------------------------------------------

Sources: Cloudflare GraphQL Analytics API (api.cloudflare.com/client/v4/graphql, totalrecalls.app zone, pulled 2026-10-23) · [totalrecalls.app](https://www.totalrecalls.app) · [TotalRecalls FAQ](https://www.totalrecalls.app/faq) · [AI Chat Importer](https://ai-chat-importer.com/) · [RecallBase](https://recallbase.net/) · [AISaver](https://aisaver.app/) · [OpenAI export help](https://help.openai.com/en/articles/7260999-exporting-your-chatgpt-history-and-data). All product claims are website-stated and not independently tested.

#### 5. Launch-day gate list (Day 1 starts only when all are green)
P1 GA4 live · P2 wording fixed · P3 discount date set + published · P4 /blog live · P5 channel verified · P6 token fresh · P7 old uploads deleted · P8 8 masters prepped · P9 8 descriptions verified · P12 ESP wired + test send green.

--------------------------------------------------------------------------------


## 7. Operational Task Graph & Master Schedule

### 7.1 Key Rulings & Verified Execution State

#### 1. User decisions (given 2026-10-20, this conversation)

| # | Decision | Ruling |
| ------ | ------ | ------ |
| U1 | **T0** | **Launch immediately.**  Schedule is a day-number schedule (Day 0 = today, 2026-10-20; Day 1 = launch day). No fixed calendar date is asserted; Day 1 = the first day on which every launch gate in §5 is green. Target: within 48 h. |
| U2 | **Superseded YouTube uploads** | **Delete the old private 10-01 cuts, upload the 8 new CRF-10 masters.**  Interpretation applied (flagged for confirmation): the convergence animation 2Bl4wMzLUxk is  **not**  a superseded take (it is the 12 s 8-sources→1-folder animation built from the site's components) — it is kept as channel trailer; the other  **9**  are deleted. If you want it deleted too, say so and it is re-uploaded (costs one upload slot). |
| U3 | **Blog surface (D2)** | **Build /blog in the Astro site**  (Cloudflare Pages, site/ in the repo). |
| U4 | **KPIs** | **No revenue/sales forecasts in this plan.**  §13's purchase/visit/follower targets are dropped. What remains: (a) process metrics — did the schedule happen (binary, tracked in the sheet); (b) measurement from Day 1 with  **no targets**  — first review Day 56; (c) the approved plan's Week-8 paid gate stays as a go/no-go  **rule**  (Free→Pro ≥ 8% AND CTR ≥ 3% before any paid amplification), not a forecast. |


--------------------------------------------------------------------------------

#### 2. Day-number ↔ V3-week mapping
The source plan's V3 12-week spine is compressed at the front because launch is immediate: V3 Weeks 0–2 (prerequisites + accuracy) collapse into  **Day 0**  (today, partially) and  **Day 1 pre-dawn** . Everything else transposes 1:1.

| V3 week | Days | Content |
| ------ | ------ | ------ |
| Wk 0–2 | Day 0 | Prerequisites (this plan's Phase P) |
| Wk 3–4 (Launch) | Day 1–14 | Launch set public; B1 Day 1, B2 + founder Day 5; guide upgrades; 2 videos/wk begins |
| Wk 5–8 | Day 15–56 | B3 Day 15 · B4 Day 22 · B5 Day 29 · B6 Day 36 · V6–V9 on cadence ·  **Week-8 metrics review Day 56** |
| Wk 9–12 | Day 57–84 | B7 Day 43… — correction: B7 Day 43, B8 Day 50, B9 Day 57 (Wk 9–12 = Day 57–84 holds B8/B9 + founder video + first product update; B7 lands Day 43 inside the B7/B8/B9 block start) |
| Day 90 | Day 90 | Checkpoint review + next quarter |
| Urgency | **Day 42** | "Launch pricing ends soon" post + Seq-3 urgency email — points at the D6 expiry (recommended  **Day 60** ) |

**Weekly floor (V3 §13, binding):**  1 blog post OR 1 video on schedule + 3–5 social posts + comment/DM monitoring + tracking sheet updated. No week may carry more than one parallel user-hand task for Andre.

--------------------------------------------------------------------------------

#### 3. Verified input state (live, 2026-10-20 — not copied from the plan)

| # | Item | State | Evidence |
| ------ | ------ | ------ | ------ |
| 1 | Vast rig (orchestrator model) | UP. Instance 56907684, RTX 3090, 38.145.234.214:60914, qwen3.8-27b-ud-q4-k-xl, 131K ctx; /health 200; end-to-end hermes -z → PONG | curl + vastai show instances --raw + hermes probe |
| 2 | Hermes config | vast3090.base_url was stale (dead instance 154.64.230.50:53469) —  **fixed**  to http://38.145.234.214:60914/v1; models map corrected to real id @131072; dead rows rtx3090/vast5090 disabled | hermes config get |
| 3 | Site | / 200 · /pricing/ 200 · /download/ 200 · /guides/ 200 ·  **/blog/ 404** | curl |
| 4 | Checkout | $24USD / $48 USD; Paddle pri_01m37qpx77bst2w1gnf3zkf4zd + dsc_01m39879ga7pv9zg0gsvzqsmjw —  **no expiry field**  (D6 open) | live /js/config.js |
| 5 | Free-tier wording (D5) | **Conflict live:**  homepage "5 conversations  **each** " vs site/src/pages/download/index.astro:31 " **5 conversations per download** " | curl + repo grep |
| 6 | YouTube channel | @totalrecalls (UChO3ZyrGqRtBFHRuQx2qX1w),  **0 public** ,  **10 private**  = 8 batch (10-01) + hero 99xoJ6w3yXI + convergence 2Bl4wMzLUxk | channel RSS + yt-api/*result*.json |
| 7 | YouTube OAuth | Token  **expired 2026-10-02**  → re-auth required; channel  **unverified**  → ~9–10 upload cap + thumbnail API 403 | token.json; STATUS note |
| 8 | Re-shot masters | 8/8 present: demo-shoot/renders/{chatgpt_v12, claude2_final, perplexity_p2, gemini_v3, grok_v1, deepseek_p2, mistral_v2, qwen_v1}, 3440×1440, yuv420p, 30 fps,  **no audio** , CRF 10 | ffprobe |
| 9 | Thumbnails | 10 JPGs built from  **old 2292-wide**  frames → re-crop needed for 3440-wide masters | Jasper/YouTube/thumbnails/ |
| 10 | Blog drafts | 9-post series on disk (B3–B9 + 2 extras); B1/B2 mapping = D1 | Jasper/YouTube/Blog/ |
| 11 | GSC | Verified 2026-10-01; sitemap 200 (54 URLs) | STATUS note + curl |

**Corrections to the source plan**  (full table in TDP §3): D7 "upload Qwen" is stale (Qwen already uploaded — now superseded); the OAuth blocker is really  *expired token + upload cap* ; the channel holds superseded cuts; /blog is a build, not a config flip; the KPI table is replaced per U4.

--------------------------------------------------------------------------------

#### 4. Task graph
Owner key:  **A**  = agent (orchestrator, Qwen on the Vast rig) ·  **W**  = worker (DeepSeek-Flash direct API for drafting; free model for cheap passes) ·  **Andre**  = user (accounts, phones, purchases, his social handles). [GATE] = requires explicit user approval before execution (mandate).

##### Phase P — Pre-launch (Day 0; launch day is gated on these)

| ID | WS | Task | Owner | Deps | Size | Acceptance test (binary) | Gate |
| ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| P1 | W6 | GA4 property + tag in Astro + UTM convention doc + tracking sheet (Marketing/ops/tracking-sheet.csv, columns per V3 Wk 1–2) | A | — | M | Test event visible in GA4 Realtime ≤ 1 h after deploy; /blog-less sitemap still 200; sheet file exists with all columns | **[GATE]**  (deploy) |
| P2 | W5 | D5: find the free-tier limit in app code (file:line), run-verify if a live login is feasible, fix the wrong page(s) so homepage ≡ /download/ ≡ app behavior | A | — | S | One code citation (path:line); both pages' HTML contain the identical resolved wording; pages 200 | **[GATE]**  (deploy) |
| P3 | W5 | D6: set discount expiry in Paddle (recommend  **Day 60**  from launch) + publish the date on /pricing/ | Andre (Paddle) + A (page) | — | S | Paddle UI shows end date; /pricing/ HTML contains it | **[GATE]**  (Paddle + deploy) |
| P4 | W1 | **Build /blog**  in Astro: content collection, post template (meta title + short answer + steps + "keep it on your machine" close), index page, internal linking per blog rules,  **sitemap plugin check**  so new URLs land | A | — | L | Local astro build passes; post-deploy: /blog/ 200, sample post 200, sitemap.xml contains both URLs | **[GATE]**  (deploy) |
| P5 | W2 | **Phone-verify the channel in YouTube Studio**  — lifts upload cap + thumbnail-API 403 | Andre | — | S | Studio shows verified; an API thumbnail upload or 2nd batch insert no longer returns uploadLimitExceeded | no |
| P6 | W2 | Re-auth YouTube OAuth (yt-api/oauth_final.py, browser paste) | Andre + A | — | S | token.json expiry > now; videos.list?part=status returns 200 | no |
| P7 | W2 | Delete the  **9 superseded**  private uploads: Bphshxf4luQ TGkLPq4y7mU ngEG1qGz7ds 8Y8tyuQ9LDI UeC-bBej8ho w2bStEH-xwk Mah9B9QIcks reIGo_aryAU 99xoJ6w3yXI.  **Keep**  2Bl4wMzLUxk (U2 flag) | A (API) | P6 | S | videos.list (mine) contains none of the 9; convergence present | **[GATE]**  (pre-approved 2026-10-20 in this conversation; executed via API) |
| P8 | W2 | Prepare the 8 new masters for YT: add silent AAC, verify spec, size check → demo-shoot/renders/yt_final/ | A | — | S | 8 files: ffprobe = 3440×1440, yuv420p, 30 fps, aac audio, each < 2 GB | no |
| P9 | W2 | 8 video descriptions + 8 pinned comments from YouTube Description Templates.md (series header → covers → provider note → CTA block → UTM links → related).  **Accuracy guardrail:**  no provider claim not verified against app/site; unverified → held | W (draft) + A (verify) | P8 | M | 8 files in yt-api/descriptions/; each has CTA block + ≥ 1 UTM link; guardrail checklist signed per video | no |
| P10 | W2 | Rebuild 8 thumbnails from the new 3440-wide masters (Template 2, 1280×720) + QC strips | A | P8 | M | 8 JPGs at 1280×720; 48 px desktop-strip QC images saved | no |
| P11 | W3 | Stage the 4 launch-day social posts as drafts (LinkedIn/X/FB/IG, no verbatim repeats, all UTM-tagged) + pull asset list:  **15–30 s teaser cut from the new masters** , 8-sources graphic, Library screenshot, logo crops | A | P8, P1 | M | Staging file with 4 distinct copy blocks + UTM on every link; every asset path exists | no |
| P12 | W4 | ESP decision ( **D9** : Brevo / MailerLite / ConvertKit free tier), footer signup wiring, Prospect→Free-Tier→Buyer buckets, test Welcome send end-to-end | Andre (pick) + A | P1 | M | Test email delivered with working one-click unsubscribe; footer form submits to ESP | **[GATE]**  (ESP account creation) |
| P13 | W8 | **Code-signing cert — the long pole:**  get OV quotes (Sectigo / GoGetSSL / DigiCert) and order | Andre | — | S | Order confirmation with delivery ETA on file | **[GATE]**  (purchase ~$100–400/yr) |
| P14 | W1 | D1 mapping + V3 §5 consistency fixes to B3/B4/B5/B9 + second-person review of B4 + merge Backup-Windows into B5. D1 default (a): B1 = launch announcement, B2 = Library Folder, PowerShell → B7 slot, Backup-Windows → B5, Library Folder also gets its own page | W (apply) + A (verify) | — | M | D1 row closed in §7; review-notes file per touched draft | no |
| P15 | W2 | Cut  **2–3 Shorts**  (15–30 s) from the new Claude master for launch week (V3 §11) | A | P8 | S | 2–3 MP4s ≤ 60 s, 9:16, in yt_final/shorts/ | no |

**Launch gates**  — Day 1 may start only when green:  **P1, P2, P3, P4, P5, P6, P7, P8, P9, P12**  (P10/P11/P13/P14/P15 may finish Day 1 morning; P3's date and P4 are the two hard ones; P13 runs in the background — cert is not a launch gate, it's a conversion fix).

##### Phase L — Launch day (Day 1)

| ID | WS | Task | Owner | Deps | Acceptance test | Gate |
| ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| L1 | W1 | Publish  **B1**  (launch announcement) | A + Andre (approve) | P4, P14 | /blog/<slug>/ 200; in sitemap; CTA per hierarchy | **[GATE]** |
| L2 | W2 | Publish the  **8-video launch set**  public; playlist "Start Here" = the 8; set thumbnails; pinned comment on every video; convergence 2Bl4wMzLUxk set as channel trailer | A (API) | P5–P10 | 8 public watch?v= URLs; playlist item count = 8; every video has thumbnail + comment | **[GATE]** |
| L3 | W3 | Launch social runbook:  **9:00 LinkedIn → 9:15 X → 10:00 Facebook → 12:00 Instagram**  (IG bio → Free Tier before 12:00); same narrative; blog URL referenced on FB+LinkedIn; monitor comments/DMs 4 h | Andre | P11, L1 | 4 posts live with timestamps; monitoring log entry | **[GATE]**  (each post) |
| L4 | W4 | Send  **Day-1 Welcome**  email (Seq 1) | A (ESP) | P12 | ESP send log; unsubscribe works | **[GATE]** |
| L5 | W7 | Community, value-first, one per venue, guardrail applies:  **r/ChatGPT + r/ClaudeAI**  ("I built a tool that downloads your entire conversation history as local Markdown files" — lead with what the user keeps);  **Show HN**  = founder story + product | Andre | L1 | Post URLs logged; zero claims outside §1 proof points (no partnerships, no invented stats) | **[GATE]**  (each) |
| L6 | W5 | Launch-week website batch: embed videos in ChatGPT/Claude/Perplexity guides; Homepage + See It Work embed check;  **Free vs Pro**  on /pricing/ (uses D5-resolved wording);  **Library Folder page**  live | A + Andre (deploy) | P2, P3, P4, L2 | Pages 200; player src/link points at the new video IDs; sitemap contains new URLs | **[GATE]**  (deploy) |
| L7 | W6 | Post-launch instrumentation verification: GA4 events flowing, UTMs present on every published link (social, video, blog) | A | L1–L3 | Verification-log entry with the actual URLs checked | no |
| L8 | W7 | Directories: submit product page + one-liner to AlternativeTo + AI-tool roundups | Andre (accounts) + A (copy) | L1 | Submission confirmations logged | **[GATE]**  (each submission) |

##### Phase D — Post-launch (day-number schedule)

| ID | Day | WS | Task | Owner | Deps | Acceptance test | Gate |
| ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| D1 | 2–7 | W3 | Social cadence begins:  **floor 3–5 posts/week**  from the Day 0–29 calendar pool (TikTok/Threads rows off per D4 default) | A (stage) + Andre (post) | L3 | Tracking sheet rows ≥ floor each week | **[GATE]**  (posting is Andre's accounts; batch-approved per week) |
| D2 | 3–7 | W2 | Publish  **2–3 Shorts**  (P15) | Andre | P15, L2 | Shorts public, URLs logged | **[GATE]** |
| D3 | 5 | W1 | Publish  **B2**  (Library Folder) +  **founder story**  post (variant pick from the 2) | A + Andre | P4, P14 | Both URLs 200, in sitemap | **[GATE]** |
| D4 | 5 | W7 | **Show HN**  (if not taken Day 1) — with the founder post | Andre | D3 | URL logged | **[GATE]** |
| D5 | 8 | W2 | **V6**  (Final script, "Trying to Get Your Old AI Conversations Back?") produced + published, with description + pinned comment | Andre (shoot) + A (edit/publish) | L2 | Public URL by Day 8; guardrail-signed description | **[GATE]** |
| D6 | 15 | W1 | **B3**  (Markdown vs JSON) + upgrade ChatGPT/Claude/Perplexity guides with video embeds (if not done in L6) | A + Andre | P4, P14, D5 | URL 200; guides embed the matching video | **[GATE]**  (deploy) |
| D7 | 15 | W2 | V7 published (2/wk cadence from Day 8: V6 d8 · V7 d15 · V8 d22 · V9 d29 · V10 d36) | Andre + A | D5 | Public URL | **[GATE]** |
| D8 | 22 | W1 | **B4**  (privacy — "not sent to our servers") | A + Andre | D6 | URL 200; second-person review signed | **[GATE]** |
| D9 | 29 | W1 | **B5**  (backup library, with Backup-Windows merged) | A + Andre | D8 | URL 200 | **[GATE]** |
| D10 | 36 | W1+W7 | **B6**  (Windows Search) +  **r/windows**  post when B6 lands | A + Andre | D9 | URL 200; Reddit post logged | **[GATE]** |
| D11 | 42 | W1+W4 | **Urgency post**  "Launch Pricing Ends Soon" +  **Seq-3 urgency email**  — points at the P3 expiry date | A + Andre | P3, D10 | URL 200 with the date; email send log | **[GATE]** |
| D12 | 43 | W1 | **B7**  (organizing by project, PowerShell slot per D1) | A + Andre | D10 | URL 200 | **[GATE]** |
| D13 | 50 | W1+W7 | **B8**  (Obsidian) +  **r/ObsidianMD**  post | A + Andre | D12 | URL 200; Reddit post logged | **[GATE]** |
| D14 | 56 | W6 | **Week-8 metrics review**  (first baselines: CTR, view duration, Free→Pro, signups — measurement only, no targets).  **Paid go/no-go rule**  (source plan §11): paid only if Free→Pro ≥ 8% AND CTR ≥ 3%; kill if CAC > $24 in first flight | A | D13 | Review doc in Marketing/ops/; paid decision recorded | no (review);  **[GATE]**  if paid proceeds |
| D15 | 57 | W1 | **B9**  (VS Code) | A + Andre | D13 | URL 200 | **[GATE]** |
| D16 | 57–84 | W2 | Founder video + first Product Update video (Wk 9–12 block) | Andre + A | D15 | Public URLs | **[GATE]** |
| D17 | cert ETA | W8 | **Cert arrives → sign EXE → rebuild → new ZIP on /download/ + status note updated**  (do not announce before the cert is live) | A + Andre | P13 | authenticode verification on the new EXE; /download/ wording updated; deploy | **[GATE]**  (deploy + purchase already gated) |
| D18 | 90 | W6 | Day-90 checkpoint: second review, next quarter | A + Andre | D14 | Doc in Marketing/ops/ | no |

**Ongoing (no day):**  email cadence =  **"real news only"**  (V3 §10) — Seq 2 (Free→Pro) fires on ESP behavior automation from P12, not a timer; macOS/Linux stay "in development, no dates"; every asset UTM-tagged ?utm_source=<platform>&utm_medium=social&utm_campaign=launch; tracking sheet updated weekly (floor).

--------------------------------------------------------------------------------

### 7.2 Corrections & Implementation Mandate

#### 3. Corrections to the source plan (stale items found while verifying)
These change the task graph; they are not strategy changes.

| # | Plan said | Reality | Effect on plan |
| ------ | ------ | ------ | ------ |
| C1 | §5/D7: "Qwen not yet uploaded — upload the Qwen video" | Qwen  **is**  uploaded (Mah9B9QIcks), part of the 8-video batch on 2026-10-01 | D7 collapses; replace with the real decision: what to do with the 10  **superseded 10-01 cuts** |
| C2 | §5/§9: "OAuth blocked on Google 403 org_internal" | OAuth worked; 10 uploads landed. The blocker now is the  **expired token**  + the  **unverified-channel upload cap**  (~9–10 videos.insert, then uploadLimitExceeded) | YouTube critical path starts at phone verification, not at the consent fix |
| C3 | §5: channel holds "Claude hero + 7 provider videos" (old takes) | Site now serves the  **re-shot CRF 10 demos**  (2026-10-16/17); YouTube still holds the  **10-01 cuts** | New workstream item: re-cut + re-upload the 8 new masters (otherwise the channel advertises a stale product) |
| C4 | §13 KPI targets: 1,000 Pro purchases, 5,000 visits, +2,000 followers, 500 email signups by campaign end | Inherited from Jasper's aspirational brief; no audience baseline exists. Converting 1,000 × $24 = $24k with a cold channel is not a plan, it is a wish | Needs a floor/stretch split (decision §8.4) or the launch is defined as a failure on day 45 |
| C5 | Two schedules in force: V3 12-week spine (§12) and the Day 0–45 / 60-day content calendars | They disagree on sequence and cadence | One spine must be declared; the calendars transpose onto it |


--------------------------------------------------------------------------------

#### Operating Governance & Approval Gates

You are the Marketing Implementation Orchestrator (bot) in charge of implementing a product (TotalRecalls) market launch.
Your master source document is the Implementation Plan that you prepared on October 13, 2026. That plan located locally at C:\Users\break\Projects\TotalRecalls-Source Code\Marketing\Plans was essentially an amalgamation of various documents prepared by the marketing model Jasper.ai. It covers the YouTube (YT) channel style and content as well as the social media strategies and content. You will convert it into an executable project: task graph, deliverables, owners, dependencies, acceptance criteria, content, landing-page requirements, tracking events, and launch checklist. Do not invent strategy beyond the approved plan; ask for clarification when requirements conflict.
Your ai model engine is Qwen 3.8-27B ud Q4-K-XL from Unsloth and running on a RTX 32GB rented card at Vast.ai.  Look for and activate any additional skills you might need.
You will use designated workers when the sub-task is justified.  Your main designated worker is DeepSeek-Flash direct API. Because of the costs involved in running that model you are encouraged to use the long list of free available models on this Hermes desktop installation (see model selection picker). Do not delegate changes to the project source code. It is located located at this path: C:\Users\break\Projects\TotalRecalls-Source Code. The project is also loacated on GitHub (breakwater2026/TotalRecalls) and deployed by Cloudflare.
The website (www.totalrecalls.app) is complete and deployed. The website pulls its embedded Chat GPT video from Cloudeflare R2. That R2 storage container also contains the 7 other providers' videos. All of those 8 videos will need to be uploaded (or connected to) the YT channel. .The YouTube channel's name is TotalRecalls. It is not deployed yet as a lot of additional work is required for this channel to be deployable
Your first task is is to generate a work plan. Before beginning your task, produce a task deployment plan containing: objective, inputs, required output format, constraints, acceptance criteria, and files or systems affected.
After a worker returns, verify the result against the approved marketing plan before marking it complete.
Never publish, send, purchase, or modify production systems without explicit user approval.

### 7.3 12-Week Operating Spine & Calendar

#### 12. 12-week timeline (V3 §12 — the operating schedule)

| Week | YouTube | Blog | Social | Website / Guides / Email |
| ------ | ------ | ------ | ------ | ------ |
| **0 — Prerequisites** | Claim @TotalRecalls handles | Confirm B1/B2 topics (D1), B6–B8 topics | — | Final site corrections; visual review checklist; confirm free-tier wording (D5), opt-in (D3), privacy-policy email vendor, filename format + default Library path |
| **1–2 — Accuracy & Setup** | Profile, banner, About, UTM header links, thumbnail template; record/edit/caption launch videos | Apply V3 §5 fixes to B3/B4/B5/B9; second-person review (B4 first); start B6 | — | Pages vs guardrails; archive spotlight drafts; one tracking sheet (video + blog) |
| **3–4 — Launch** | Publish launch set; set trailer; 3 launch playlists; pin comment on every video | Publish B1 (launch day) + B2 (Day 5); finish B6; start B7 | Launch-day runbook (LinkedIn 9:00 → X 9:15 → FB 10:00 → IG 12:00); Free Tier provider sets; 2–3 Shorts | Upgrade ChatGPT/Claude/Perplexity guides + embed videos; embed demo on Homepage & See It Work; Free vs Pro on Pricing; publish Library Folder page; Day 1 Welcome email |
| **5–8 — Pro Coverage & Explainers** | 1 Pro guide video/week from Gemini; Proof Demos same session; launch Going Pro | Publish B3, B4, B5, B6 (one/week); B7+B8 drafts done by Wk 8 | Pro provider sets; B3–B5 posts as they go live | Upgrade all five Pro guides (Gemini opening = Takeout-first); Blog 3 links in every guide; Day 42 urgency post ≈ 2 wks before discount expiry (D6) |
| **9–12 — Trust & Ownership** | Publish Markdown-vs-JSON, "not sent to our servers," Windows search, backup, organizing videos; start Using-Your-Saved-Chats + Troubleshooting; founder video; first Product Update | Publish B7, B8, B9; embed matching videos in B3–B6 | Day 0–29 calendar continues (final-call week = Day 29) | Link all blogs from Ownership Path; embed founder video; first update email only if real news |
| **Day 90 — Checkpoint** | — | — | — | Second metrics review; plan next quarter |

**Weekly operating rhythm (V3 §13, "the minimum week"):**  1 blog post OR 1 video on schedule, 3–5 social posts, comment/DM monitoring, tracking sheet updated — this is the floor, not the ceiling.


## 8. Multi-Channel Content Repository

#### Part 0 — Ground Rules for Every Asset
##### 0.1 The one-line pitch (use everywhere)
**TotalRecalls is a Windows app that saves your AI conversations as Markdown and JSON files in a folder on your own PC.**
Supporting line:  *Eight AI tools. One folder on your PC.*  — ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral, Qwen.
Brand line (emotional, never used alone):  *Your AI conversations belong to you.*

##### 0.2 Claims register — what content may and may not say
**Allowed (website-stated as of 2026-10-23).**  Keep wording close to the site's.

| Topic | Allowed wording | Where the site says it |
| ------ | ------ | ------ |
| What it is | Windows 10/11 desktop app; portable TotalRecalls.exe + README.txt in a ZIP (~17.8 MB); no installer | [Download](https://www.totalrecalls.app/download/), [FAQ<br>](https://www.totalrecalls.app/faq) |
| Providers | ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral, Qwen | [Homepage<br>](https://www.totalrecalls.app) |
| How it gets chats | You sign in to each provider locally, inside the app.  **Gemini is the exception: you point the app at your Google Takeout folder** | [Download](https://www.totalrecalls.app/download/), [FAQ<br>](https://www.totalrecalls.app/faq) |
| Output | One Markdown file and one JSON file per conversation, in a subfolder per provider, inside a Library folder (example C:\TotalRecalls\Library\) or a folder you choose | [See It Work](https://www.totalrecalls.app/see-it-work/), [Download<br>](https://www.totalrecalls.app/download/) |
| What's in the files | Chat text and code blocks as Markdown; attachment references preserved alongside; the binary files themselves stay in your provider account | [FAQ<br>](https://www.totalrecalls.app/faq) |
| Account | No TotalRecalls account, no sign-up | [FAQ<br>](https://www.totalrecalls.app/faq) |
| Price | Pro: $24 USD one-time, discounted launch price, no subscription; all 8 providers; unlimited downloads; up to 3 device activations; free core-app updates; license key by email | [Homepage<br>](https://www.totalrecalls.app) |
| Free Tier | ChatGPT, Claude, Perplexity; 5-conversation limit ( **see 0.3 — wording not yet settled** ); no card, no account | [Download<br>](https://www.totalrecalls.app/download/) |
| Provider accounts | Works with free-tier ChatGPT, Claude, Perplexity, Grok, DeepSeek, Mistral and Qwen Chat accounts; Gemini needs a Google account with Takeout | [FAQ<br>](https://www.totalrecalls.app/faq) |
| Privacy (verbatim only) | "Your AI session tokens stay on your machine." "We never host your chats, your downloads, or your credentials." "No telemetry." You can check the network traffic yourself with Wireshark | [FAQ](https://www.totalrecalls.app/faq), [Download<br>](https://www.totalrecalls.app/download/) |
| Integrity | SHA-256 checksum published on the Download page; verify with Get-FileHash in PowerShell | [Download<br>](https://www.totalrecalls.app/download/) |
| Platforms | Windows 10/11 today; Linux and macOS "in the works"; no mobile | [FAQ<br>](https://www.totalrecalls.app/faq) |
| SmartScreen | First launch may show "Windows protected your PC" → More info → Run anyway; download only from totalrecalls.app | [Microsoft Warning<br>](https://www.totalrecalls.app/microsoft-warning/) |
| Smart App Control | Windows 11 Smart App Control may block unsigned apps with no override; code signing is on the roadmap | [Download<br>](https://www.totalrecalls.app/download/) |
| Release | Version 1.0.0, released October 17, 2026 | [Download<br>](https://www.totalrecalls.app/download/) |
| Trademarks | "Not affiliated with OpenAI, Anthropic, Perplexity, Google, xAI, DeepSeek, Mistral, or Qwen." | Site footer |

**Record before you claim.**  These are on the site but have not been tested for this plan. Use them only after you've filmed them working:

*  Speed ("setup takes a few minutes", "a pick and a click")
*  Very large histories ("a 50,000-message archive works the same as a 500-message one")
*  "Catches conversations the official download tools miss (shared links, archived conversations, partial histories)"
*  Exactly what each provider's files contain (Gate item 5 in the plan)
**Never say:**

*  "Safe", "secure", "100% private", "trusted by Microsoft/Windows" or "virus-free" as a guarantee. Say what the app does and how to check it yourself (SHA-256, Wireshark).
*  "The only…", "the first…", "unlike every other tool…". Other archive tools also save locally and to Markdown.
*  That attachments, images or files are downloaded. Only references are saved.
*  That add-ons (semantic search, Obsidian/Notion sync, RAG containers, multi-device memory) exist or are coming on a date.
*  "Just click Run anyway, it's fine." The SmartScreen framing is always: here's what it is, here's how to check the file, here's how to continue.
*  Anything that implies endorsement by, or partnership with, an AI provider.

##### 0.3 The free-tier line (one placeholder, swap everywhere)
The live site still uses two wordings: "5 conversations each / per provider" on the [homepage](https://www.totalrecalls.app) and [See It Work](https://www.totalrecalls.app/see-it-work/), and "5 conversations per download" in the [FAQ](https://www.totalrecalls.app/faq) and on the [Download page](https://www.totalrecalls.app/download/). Until you confirm which is true and fix the site (plan Gate item 1), every asset uses one token:
{FREE_LINE} =  **"Free Tier: ChatGPT, Claude and Perplexity — 5 conversations per download, no card, no account."**
This is provisional and follows the FAQ/Download wording. If the actual behaviour is per provider, find-and-replace {FREE_LINE} in this file once. Never write "15 free conversations" or any other multiplied figure.

##### 0.4 Disclosure
Every post you publish personally about TotalRecalls says plainly that you made it: "I built this", "I'm the developer", "founder here". On Reddit, Facebook Groups and Hacker News this isn't optional — undisclosed self-promotion gets removed and burns the account. If you ever pay a creator or newsletter, they must label it as sponsored using the platform's paid-partnership tools.

##### 0.5 Tracked links (UTM scheme)
Referrer data isn't available on the current Cloudflare plan (Launch Plan, Section 11), so every link carries UTM tags. Use the homepage or the specific guide page — not a direct ZIP link — so the SmartScreen and Smart App Control notes are seen before the download.
```
https://www.totalrecalls.app/?utm_source={source}&utm_medium={medium}&utm_campaign=launch&utm_content={asset_id}

```

| Channel | utm_source | utm_medium |
| ------ | ------ | ------ |
| YouTube long-form | youtube | video |
| YouTube Shorts | youtube | short |
| TikTok | tiktok | short |
| Instagram | instagram | social |
| Facebook | facebook | social |
| Reddit | reddit | community |
| LinkedIn | linkedin | social |
| X | x | social |
| Product Hunt | producthunt | launch |
| Hacker News | hackernews | community |

Example: https://www.totalrecalls.app/?utm_source=youtube&utm_medium=video&utm_campaign=launch&utm_content=v1
Notes:

*  Reddit and Hacker News readers distrust tracked links. In those posts, use the clean URL https://www.totalrecalls.app and judge results from the date of the post instead.
*  TikTok and Instagram don't allow clickable links in captions. Put the link in your profile (bio link) and say "link in profile".
*  A UTM tag is part of the URL and is visible in your own server/Cloudflare data. It doesn't add tracking to the site, so it's compatible with the site's "no analytics, no tracking pixels" statement. Keep it that way: don't add pixels or tag managers to the site for this launch.
*  Before launch, check that UTM query strings show up in the Cloudflare data you pull (query parameters may need the request-query field). If they don't, you can still use short, distinct paths per channel (e.g. /yt, /r) that redirect to the homepage.

##### 0.6 Recording rules (all video)

1.  **Use a demo account with demo conversations.**  Create 15–30 throwaway chats in each provider (sample research, a code snippet, a recipe, a trip plan) so nothing private ever appears on screen. Use a fresh Windows user profile with a neutral desktop.
2.  **Blur or avoid:**  email addresses, account names, conversation titles from real accounts, license keys, the system clock if it reveals your location, browser tabs.
3.  **Show the real thing.**  SmartScreen prompt included. If a step is slow, speed it up and say so on screen ("4× speed" — the See It Work page already does this).
4.  **Resolution:**  record at 1920×1080 (or 2560×1440) at 100–125% Windows scaling so text stays readable when cropped to vertical.
5.  **Vertical crops:**  for Shorts/Reels/TikTok, plan for a 9:16 crop of the app window. Keep the app window narrow (about 1000 px wide) and centred so it survives the crop.
6.  **Audio:**  use a USB mic in a quiet room. No copyrighted music — use the YouTube Audio Library or each platform's licensed library.
7.  **Captions:**  burn captions into all short-form video (most people watch muted). Upload an SRT file for long-form.
8.  **Provider names and logos:**  say provider names freely (descriptive use). For thumbnails, prefer text names over provider logos unless you've checked that provider's brand guidelines. Add the "not affiliated" line to every description.

##### 0.7 Visual identity cues (from the site)

*  Recurring visual: the Library folder path C:\TotalRecalls\Library\claude\2026-07-28-refactor-plan.md with the "● Saved locally" badge. Make it the signature end-card of every video.
*  File chips .md + .json as a recurring graphic.
*  Tone: plain, calm, specific. Short sentences. The site's voice ("Tabs close. Interfaces change. Nobody keeps a backup. Until they need one.") is the model — reuse it.

--------------------------------------------------------------------------------

#### Part 1 — YouTube (Primary Channel)
##### 1.1 Channel setup (do once, before D0)

| Element | Copy / spec |
| ------ | ------ |
| Channel name | TotalRecalls |
| Handle | @totalrecalls (check availability; fallback @totalrecallsapp) |
| Banner text (2048×1152, keep text in the central 1235×338 safe area) | **Your AI chats, saved as files on your PC.**  · ChatGPT · Claude · Perplexity · Gemini · Grok · DeepSeek · Mistral · Qwen · Windows 10/11 |
| Profile image | The TotalRecalls mark on a plain background; must read at 98×98 px |
| Banner links | Website (UTM: utm_source=youtube&utm_medium=channel), Download page, Guides |
| Channel trailer | V1 cut to 60–90 s (S1 works as a placeholder) |

**About section (paste):**
TotalRecalls is a Windows app that saves your AI conversations as Markdown and JSON files in a folder on your own PC.
This channel shows exactly how it works — real recordings, real files — plus step-by-step guides for saving your chat history from ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral and Qwen.
No TotalRecalls account. No subscription. You sign in to your AI tools locally, inside the app, and your files land in a folder you control.
Windows 10/11 · Free Tier available · Pro $24 one-time (launch price)
Made by [Founder name]. Questions: support@totalrecalls.app
TotalRecalls is not affiliated with OpenAI, Anthropic, Perplexity, Google, xAI, DeepSeek, Mistral, or Qwen.
**Playlists:**

1. Start Here — V1 plus the S1 Short
2. Save Your AI Chats — Provider Guides — V2–V8, in release order
3. Shorts — all Shorts
4. Release Notes and Updates — short changelog videos (optional, from D30)
**Default upload settings**  (Settings → Upload defaults): category Science & Technology; language English; captions certification "This content has never aired on TV"; license Standard YouTube; tags field pre-filled with the core tag set below.
**Core tag set:**  save ai conversations, ai chat history, backup chatgpt conversations, export chatgpt history, save claude chats, ai chat archive, markdown, windows app, local files, chatgpt history download
**Standard description footer**  (paste at the end of every description):
```
—
TotalRecalls · Windows 10/11 · Markdown + JSON files saved on your PC
{FREE_LINE}
Pro: $24 one-time (launch price) — all 8 providers, unlimited downloads, up to 3 device activations, free core updates.

Download (verify the SHA-256 on the page): https://www.totalrecalls.app/download/
SmartScreen prompt explained: https://www.totalrecalls.app/microsoft-warning/
FAQ: https://www.totalrecalls.app/faq
Support: support@totalrecalls.app

Windows 11 note: Smart App Control may block unsigned apps with no override. Code signing is on the roadmap — details on the Download page.

TotalRecalls is not affiliated with OpenAI, Anthropic, Perplexity, Google, xAI, DeepSeek, Mistral, or Qwen. I'm the developer of TotalRecalls.

```

--------------------------------------------------------------------------------

##### 1.2 V1 — Hero explainer (6–8 min) · Calendar D0
**Goal:**  the asset every other post points to. Shows one complete loop — get the app → sign in → download → open the files → find something again — and handles the three main objections (safety, SmartScreen, why pay).
**Title options**  (test with YouTube's thumbnail/title A/B tool if available on your channel):

1. I Saved Every AI Conversation I've Ever Had as Files on My PC
2. Stop Losing Your ChatGPT and Claude Chats — Save Them as Files (Windows)
3. Your AI Chats, Saved as Markdown on Your PC — 8 AI Tools, One Folder
**Thumbnail concepts**  (1280×720; text ≤ 5 words; readable at phone size):

*   **A:**  Left: a messy sidebar of chat titles fading out. Right: a clean Windows folder tree Library › chatgpt › claude › perplexity. Text:  **"SAVED. FOREVER."**
*   **B:**  Your face (if you're comfortable on camera) pointing at a folder icon labelled .md. Text:  **"MY AI CHATS → FILES"**
*   **C:**  Eight provider names as text chips flowing into one folder. Text:  **"8 AI TOOLS. 1 FOLDER."**
**Chapters**  (put in the description; adjust timestamps after editing):
```
0:00 Your AI chats are scattered
0:40 What TotalRecalls does (in one sentence)
1:05 Getting the app (and checking the file)
1:50 The Windows SmartScreen prompt, explained
2:30 Sign in and see your history
3:15 Download your conversations
4:05 What you actually get: the .md and .json files
5:05 Finding an old chat again in seconds
5:45 Is it safe? What it does and doesn't do
6:30 Free Tier vs Pro
7:05 Who should NOT buy this
7:30 Wrap-up

```
**Full script**  (spoken words in plain text; [SCREEN] = what's shown; [TEXT] = on-screen caption/graphic). Roughly 1,050 words, about 7 minutes at a calm pace.

--------------------------------------------------------------------------------

**0:00 — Cold open: the problem**
[SCREEN] Fast scroll through a long ChatGPT sidebar (demo account), then Claude, then Perplexity. Stop on nothing.
A few weeks ago I needed a piece of code I'd worked out with an AI. I knew I'd done it. I couldn't find it. It was somewhere in one of four different AI tools, under hundreds of newer chats.
If you use more than one AI tool, you've probably had that moment. Your research, your drafts, your code, your decisions — they live in sidebars that you don't control.
[TEXT]  *Tabs close. Interfaces change. Nobody keeps a backup.*
So I built a small Windows app to fix it for myself. This video shows you exactly how it works — real recording, no mock-ups.
**0:40 — The one-sentence explanation**
[SCREEN] The Library folder in File Explorer: C:\TotalRecalls\Library\ with subfolders chatgpt, claude, perplexity, gemini…
TotalRecalls is a Windows app that saves your AI conversations as Markdown and JSON files in a folder on your own PC. It covers ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral and Qwen.
You don't create an account with me. You sign in to your AI tools inside the app, on your own computer, and the files land in a folder you choose.
[TEXT] .md + .json · one folder · your PC
**1:05 — Getting the app (and checking it)**
[SCREEN] totalrecalls.app → Download page. Show the "~17.8 MB" ZIP and the SHA-256 line.
You get it from totalrecalls.app — and only from there. It's a ZIP file of about 18 megabytes with two things inside: the app, which is portable — no installer — and a README.
Before you run anything you downloaded, it's worth checking the file. The Download page publishes a SHA-256 checksum. Open PowerShell where you saved the ZIP and type this.
[SCREEN] PowerShell: Get-FileHash TotalRecalls-1.0.0-free-tier.zip -Algorithm SHA256. Highlight that the output matches the page.  **RECORD**  with the actual current file name.
If the two strings match, you have exactly the file I published. Then unzip it anywhere — I'll use a folder on the desktop.
**1:50 — SmartScreen, explained honestly**
[SCREEN] Double-click TotalRecalls.exe → the real "Windows protected your PC" dialog.
The first time you run it, Windows will probably show this: "Windows protected your PC." Here's what it actually means. Microsoft Defender SmartScreen warns about apps that don't have a download history yet. TotalRecalls is new, and it isn't code-signed yet, so it gets this warning. It isn't Windows saying it found something harmful.
But don't train yourself to click past these for everything. Do it when you know where the file came from and you've checked it — like we just did with the checksum. Then it's "More info", then "Run anyway".
[SCREEN] Click More info → Run anyway.
[TEXT]  *Only from totalrecalls.app · check the SHA-256 first*
One more note for Windows 11: if Smart App Control is turned on, it may block unsigned apps completely, with no "Run anyway" button. Code signing is on my roadmap. The details are on the Download page.
**2:30 — Sign in and see your history**
[SCREEN] App Step 1: provider list. Pick ChatGPT. Step 2: sign-in window.  **Blur the email.**
Step one: pick a provider. I'll start with ChatGPT. Step two: sign in. This sign-in happens inside the app, on my PC. My session stays on this machine — as the site puts it, "your AI session tokens stay on your machine."
Once I'm connected, the app lists my conversations and shows how many there are before it downloads anything.
[SCREEN] The conversation count appears.  **RECORD**  the real number from your demo account.
**3:15 — Download**
[SCREEN] Choose output folder → Download → progress. Speed up long stretches and label them on screen "4× speed".
I pick where the files should go and hit Download. It walks through the history and writes each conversation to disk. I've sped this part up — how long it takes depends on how many chats you have and on the provider.
[SCREEN] Completion screen → "open the folder".
When it's done, it tells you exactly where the files went.
**4:05 — What you actually get**
[SCREEN] File Explorer: Library\chatgpt\ with pairs of .md and .json files. Open one .md in Notepad, then the same in VS Code or a Markdown viewer. Then open the .json.
Here's the result. Each conversation becomes two files. The Markdown file is the conversation as readable text — headings and code blocks intact. It opens in Notepad, Word, VS Code, Obsidian — anything. The JSON file is the same chat as structured data, if you want to search it with other tools or build something on top of it.
One honest limit: images and attachments aren't downloaded as files. Their references are kept, but the files themselves stay in your provider account.
[SCREEN] Repeat quickly with Claude and Perplexity so three subfolders appear.  **RECORD** .
I'll do the same for Claude and Perplexity. Same steps, separate subfolders, one library. Gemini works slightly differently: you request your data through Google Takeout and point the app at that folder — there's a guide for it on the site.
**5:05 — Finding it again**
[SCREEN] Windows search in the Library folder for a word from a demo chat ("pricing"), or VS Code "Find in files", or Select-String in PowerShell.
And here's the payoff. Remember that piece of code I couldn't find? Now it's a file. I search the folder for a word I remember, and there it is — across every AI tool at once.
[SCREEN] Copy the Library folder to a USB drive or backup folder.
And because they're just files, I can back them up, copy them to a new PC, or put them in my notes app. No login needed to read them.
**5:45 — Is it safe? What it does and doesn't do**
[SCREEN] FAQ privacy lines as on-screen text.
You're giving an app access to your AI accounts, so you should ask hard questions. Here's what TotalRecalls says it does — and how you can check it yourself.
It runs locally on your PC. There's no TotalRecalls account. It doesn't host your chats, your downloads or your credentials, and it ships with no telemetry. You don't have to take my word for that — run a network monitor like Wireshark while it works and see what it connects to.
[TEXT]  *Don't trust. Verify.*  · SHA-256 · Wireshark
**6:30 — Free Tier vs Pro**
[SCREEN] Pricing section of the homepage.
You can try it for free on ChatGPT, Claude and Perplexity, with a 5-conversation limit per download — no card, no account. That's enough to see the files on your own chats before you decide anything.
Pro is a one-time $24 launch price: all eight providers, unlimited downloads, up to three devices, and free updates to the core app. No subscription.
[TEXT] {FREE_LINE} · Pro $24 one-time
**7:05 — Who should NOT buy this**
Quick honesty check. If you only use one AI tool and you just want a copy of a chat now and then, your provider's built-in export may be all you need. TotalRecalls is for people who use several AI tools regularly and want all of it as plain files on their PC. And right now it's Windows only — Mac and Linux are in the works.
**7:30 — Wrap-up**
[SCREEN] Signature end card: C:\TotalRecalls\Library\…\your-best-idea.md ● Saved locally
That's it: sign in, download, and your AI conversations are files you own. The link to try it free is in the description, along with the SmartScreen guide and the checksum. If you've got questions — especially skeptical ones — leave them in the comments. I read all of them.
[End screen, 20 s] Element 1: Subscribe. Element 2: "Save Your AI Chats — Provider Guides" playlist. Element 3: V2 (once it's published).

--------------------------------------------------------------------------------

**V1 description (above the footer):**
```
I use several AI tools every day and kept losing track of conversations that mattered. So I built TotalRecalls — a Windows app that saves your AI conversations as Markdown + JSON files in a folder on your own PC.

This video is a real, unedited-in-substance recording: getting the app, checking the file, the Windows SmartScreen prompt, signing in, downloading, and opening the files.

Try it free: https://www.totalrecalls.app/?utm_source=youtube&utm_medium=video&utm_campaign=launch&utm_content=v1

[chapters]

[standard footer]

```
**Pinned comment (V1):**
Developer here — I'll answer anything in the comments, especially the skeptical questions. Three I expect:

1. "Is it safe?" — it runs locally, has no TotalRecalls account and no telemetry. Check it yourself with Wireshark, and verify the download with the SHA-256 on the Download page.
2. "Why the SmartScreen warning?" — the app is new and not code-signed yet. The full explanation is linked in the description.
3. "Mac?" — not yet. Windows 10/11 today; Mac and Linux are in the works.
**Verify before posting V1**

*  [ ] {FREE_LINE} matches what the app actually does (Gate 1)
*  [ ] All on-screen data is demo data; emails and keys blurred
*  [ ] The checksum shown matches the file on the live Download page
*  [ ] The Smart App Control statement still matches the Download page
*  [ ] Captions file uploaded and checked
*  [ ] No provider logos in the thumbnail unless brand guidelines were checked

--------------------------------------------------------------------------------

##### 1.3 Provider tutorials V2–V8 (4–6 min each) · Calendar D5, D12, D16, D25, D29–60
**Why:**  the site's own traffic shows provider guide pages getting steady views (Launch Plan, Section 11). Each video targets one "how do I save my [provider] chats" search and links to the matching site guide.
**Shared structure**  (every tutorial follows it, so viewers know what to expect):

| Beat | Time | Content |
| ------ | ------ | ------ |
| Hook | 0:00–0:20 | The specific pain for this provider (see table below) + "in 4 minutes you'll have every [provider] chat as a file on your PC" ( **only if your recording shows it takes about that long** ) |
| Two ways to do it | 0:20–1:10 | The provider's own export option, shown or described neutrally ("here's what the built-in option gives you") — then TotalRecalls. Never disparage the built-in option. If you haven't checked the provider's current export, skip the comparison rather than guess |
| Get the app | 1:10–1:40 | Short version of V1 1:05–2:30 (checksum + SmartScreen in 20 s; link V1 for the full explanation) |
| The provider-specific steps | 1:40–3:30 | **RECORD**  sign-in (or Takeout import), count, download |
| The files | 3:30–4:30 | Open .md + .json; show what this provider's chats look like as files (code blocks, sources, etc. —  **only what you recorded** ) |
| Tier note + CTA | 4:30–5:00 | Free Tier or Pro for this provider; link to the site guide |

**Provider details:**

| ID | Provider | Day | Title | Hook line | Provider-specific notes | Tier | Site guide |
| ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| V2 | ChatGPT | D5 | How to Save All Your ChatGPT Conversations as Files (Windows) | "Hundreds of ChatGPT chats, one search box that only goes so far." | Show the conversation count before download. Mention it works with free ChatGPT accounts (FAQ) | Free Tier | [ChatGPT guide<br>](https://www.totalrecalls.app/guides/export-chatgpt-conversations/) |
| V3 | Claude | D12 | How to Save Your Claude Chat History as Markdown Files | "Your best Claude conversations — the long reasoning ones — deserve better than a sidebar." | If your demo uses Claude Projects, show it (the site has a Claude Projects guide). Code blocks look good in Markdown, so show one | Free Tier | [Claude guide<br>](https://www.totalrecalls.app/guides/export-claude-chat-history/) |
| V4 | Perplexity | D16 | How to Save Your Perplexity Threads (With Sources) as Files | "Perplexity answers come with sources. Keep both." | Show the sources reference file  **only if**  your recording shows one (FAQ mentions sources.json as an example of preserved references) | Free Tier | [Perplexity guide<br>](https://www.totalrecalls.app/guides/export-perplexity-conversations/) |
| V5 | Gemini | D25 | How to Turn Your Gemini Takeout Into Readable Markdown Files | "Google Takeout gives you your Gemini data. Here's how to make it readable." | **Different flow:**  request Gemini data via Google Takeout, download it, then point TotalRecalls at the Takeout folder. Follow the site's guide step by step; don't describe Takeout menus you haven't recorded | Pro | [Gemini Takeout guide<br>](https://www.totalrecalls.app/guides/gemini-takeout-archive/) |
| V6 | Grok | D29–36 | How to Save Your Grok Conversations to Your PC | "Grok chats, saved as plain files you can search." | Standard sign-in flow | Pro | [Grok guide<br>](https://www.totalrecalls.app/guides/grok/) |
| V7 | DeepSeek | D37–44 | How to Back Up Your DeepSeek Chats as Markdown | "Keep a local copy of your DeepSeek work." | Standard sign-in flow | Pro | DeepSeek guide (linked from the Download page — paste its URL) |
| V8 | Mistral + Qwen | D45–60 | Save Your Mistral and Qwen Chats as Files (Windows) | "Two more AI tools, same folder." | Can be two short videos or one combined video | Pro | Mistral guide (paste URL) · [Qwen guide<br>](https://www.totalrecalls.app/guides/qwen/) |

**Tutorial description template:**
```
How to save your [Provider] conversations as Markdown + JSON files on your Windows PC with TotalRecalls.

Step-by-step written guide: [site guide URL]?utm_source=youtube&utm_medium=video&utm_campaign=launch&utm_content=[v#]
Full walkthrough of how the app works: [V1 link]

0:00 [Provider-specific pain]
0:20 Two ways to save your [Provider] chats
1:10 Getting the app
1:40 Signing in to [Provider] (or: Importing your Google Takeout)
3:30 What the files look like
4:30 Free Tier vs Pro for [Provider]

[standard footer]

```
**Tutorial thumbnail system**  (consistency = recognisability): the same layout every time — the provider name in large text on the left, an arrow, a folder with .md on the right, and a small "Windows" tag. Use a different accent colour per provider. Avoid logos unless brand guidelines were checked.
**Tags per tutorial:**  core tag set + save [provider] chats, [provider] chat history, export [provider] conversations, backup [provider], [provider] to markdown

--------------------------------------------------------------------------------

##### 1.4 V9 — Obsidian / notes-app workflow · Calendar D60 (conditional)
**Only produce this if**  you have opened the Library's .md files in Obsidian (or another notes app) and they work well. Don't promise sync: Obsidian/Notion sync is a future add-on per the FAQ.

*   **Title:**  I Put Every AI Conversation Into My Obsidian Vault (Plain Markdown, No Plugins)
*   **Outline:**  point Obsidian at the Library folder (or copy it into a vault) → search across providers → link a chat into a note → limits (no sync; re-run downloads to refresh)
*   **CTA:**  Free Tier
*   **Opens the door to:**  r/ObsidianMD and Obsidian forum posts (Part 4), only after this video exists

--------------------------------------------------------------------------------

##### 1.5 YouTube Shorts S1–S6 (vertical, ≤ 60 s) · Calendar D4, D11, D20, D22 + 2 extra
All Shorts: 1080×1920, ≤ 60 seconds so the same file works on YouTube Shorts, TikTok, Instagram Reels and Facebook Reels without changes. Burn captions into the video, with the hook text on screen in the first second. Link the related long video in the Short (YouTube's related-video feature).
**S1 — "My AI chats are now files" (the 30-second demo)**  · D4

| Time | Visual | Voice-over / on-screen text |
| ------ | ------ | ------ |
| 0–2 s | Long sidebar scroll, blurred | TEXT:  **"Where did that AI chat go?"** |
| 2–6 s | Cut to the Library folder with 3 subfolders | VO: "I got tired of losing AI chats, so I made them files." |
| 6–14 s | Sped-up: pick ChatGPT → sign in (blurred) → count → Download | TEXT: "Sign in on your PC → download" |
| 14–22 s | File Explorer → open .md in Notepad | VO: "Every conversation becomes a Markdown file and a JSON file. In a folder I control." |
| 22–27 s | Windows search finds a word inside the chats | TEXT: "Search all of it at once" |
| 27–30 s | End card: path + "● Saved locally" | VO: "TotalRecalls. Windows. Link on my channel." |

**S2 — "The SmartScreen thing, explained in 40 seconds"**  · D11

*   **Hook (0–2 s):**  "Windows protected your PC" dialog. TEXT:  **"Should you click 'Run anyway'?"**
*   **Beats:**  (1) What SmartScreen does: warns about apps with no download history. (2) Why new apps get it: no reputation yet; mine isn't code-signed yet. (3) The habit to build: only when you know the source and you've checked the file — show Get-FileHash matching the site. (4) Windows 11 Smart App Control may block unsigned apps entirely.
*   **Closing line:**  "Check first, then decide. That goes for my app too."
*   **Why it works:**  an educational Short that's useful beyond TotalRecalls, and it builds trust.
**S3 — "8 AI tools, 1 folder"**  · D22

*  Fast montage of the 8 provider names (text) dropping into the Library folder tree. Each subfolder appears with a soft click.
*  VO: "ChatGPT. Claude. Perplexity. Gemini. Grok. DeepSeek. Mistral. Qwen. One folder on my PC."
*  TEXT at end:  **"Your AI chats belong to you."**  + "Windows · link on channel"
*   **RECORD:**  subfolders must come from real downloads (Pro), not renamed empty folders.
**S4 — "The file test" (what's actually inside)**  · D20

*   **Hook:**  TEXT  **"What do you actually get?"**
*  Open one .md: scroll to a heading and a code block. Open the .json: highlight the structure.
*  VO: "Markdown you can read anywhere. JSON you can build on. Images and attachments stay in your account — only references are kept."
*   **Why include the limit:**  it pre-empts the most common "but does it…?" comment and lowers refund risk.
**S5 — "Is it safe? Check it yourself"**  · extra, D30+

*  Wireshark (or Windows Resource Monitor's network tab) running alongside the app during a download.  **RECORD**  and show only what you actually observe.
*  VO: "Don't trust a developer's word on privacy. Watch the network yourself. Here's what TotalRecalls connects to while it downloads." (Describe the observed connections accurately — e.g. the AI provider's own servers.)
*   **Do not publish**  until you have done this test and the result matches the site's claims.
**S6 — "When you DON'T need this"**  · extra, D40+

*  Face-to-camera or text-only. "If you use one AI tool and rarely need old chats, your provider's own export is probably enough. If you use three or four every day and you've ever lost something — that's who I built this for."
*  Honesty content performs well and filters out refund-prone buyers.
**Shorts title/description pattern:**

*   **Title (≤ 60 characters):**  "My AI chats are now files on my PC #shorts" · "Should you click Run anyway? #shorts" · "8 AI tools, 1 folder #shorts"
*   **Description:**  one line of what it shows + the full-video link + "Windows 10/11 · I'm the developer · not affiliated with [providers shown]"

--------------------------------------------------------------------------------

##### 1.6 Comment-reply bank (YouTube, reusable on every channel)
Reply within 24 hours for the first two weeks. Answer the actual question, use no superlatives, and link the FAQ when useful.

| Comment type | Reply |
| ------ | ------ |
| "Is this safe? You want my login?" | "Fair question. You sign in to the provider inside the app on your own PC; there's no TotalRecalls account, and per the FAQ your session tokens stay on your machine and nothing is sent to TotalRecalls servers. Please don't take my word for it — verify the download's SHA-256 and watch the network traffic with Wireshark while it runs." |
| "Why does Windows block it?" | "SmartScreen warns about apps without a download history yet. TotalRecalls is new and not code-signed yet. Only run it if you got it from totalrecalls.app and the checksum matches. On Windows 11, Smart App Control may block it entirely — code signing is on the roadmap." |
| "ChatGPT already has an export." | "It does, and if it covers what you need, use it. TotalRecalls is for people who use several AI tools and want all of them in one folder, as Markdown + JSON, without waiting for an emailed ZIP."  *[(Check the current ChatGPT export flow before saying "emailed ZIP"; OpenAI documents it here.)*<br>*](https://help.openai.com/en/articles/7260999-exporting-your-chatgpt-history-and-data)* |
| "Why pay $24 when [free extension] exists?" | "If a free extension does what you need, go for it. TotalRecalls is a desktop app for 8 providers with plain files in your own folder, one payment, no subscription — and you can try the Free Tier before deciding." |
| "Mac version?" | "Not yet — Windows 10/11 today. Mac and Linux are in the works. Sign up for product updates on the site and you'll hear when it's ready." |
| "Does it save images/attachments?" | "Not the files themselves. Text and code blocks come through as Markdown, and attachment references are kept, but images and attachments stay in your provider account." |
| "Does it work with free accounts?" | "Yes for ChatGPT, Claude, Perplexity, Grok, DeepSeek, Mistral and Qwen Chat. Gemini works through Google Takeout, so you need a Google account with Takeout enabled." |
| "Is this against [provider]'s terms?" | "You're signing in with your own account to get your own conversations, but every provider has its own terms, and I'm not affiliated with any of them — so please read your provider's terms yourself."  *(Have this reviewed before using it; see Part 9.)* |
| "Does it work on 50k messages?" | Only answer with what you've tested: "I've tested it on [N] conversations. Downloads stream to disk, so size is mostly limited by disk space — if you try a huge history, tell me how it goes." |
| Bug report | "Thanks — sorry about that. Could you email support@totalrecalls.app with your Windows version, the provider, and what you saw? I'll look at it personally." |
| Hostile / spam | Don't argue. Hide clear spam; answer the factual part of criticism once, politely, and stop. |


--------------------------------------------------------------------------------

#### Part 2 — TikTok and Instagram (Short-Form Repurposing)
**Role in the plan:**  repurposing channels, not separate programs. Every Short (S1–S6) is cross-posted, plus a few native formats below. Note from the traffic baseline: a big share of identified visits come from phones (Launch Plan, Section 11), and the app is Windows-only. Every mobile CTA therefore says  **"save this for when you're at your PC"**  and points to the profile link. The homepage already tells phone visitors: "Windows app. Visit from your desktop to download" ([homepage](https://www.totalrecalls.app)).

##### 2.1 Profile setup

| Field | TikTok | Instagram |
| ------ | ------ | ------ |
| Handle | @totalrecalls (fallback @totalrecalls.app) | @totalrecalls (fallback @totalrecalls.app) |
| Name | TotalRecalls · AI chat archive | TotalRecalls · AI chats → files |
| Bio (≤ 80 / 150 chars) | Save your AI chats as files on your PC. Windows. Made by [Founder name]. | Your AI conversations, saved as Markdown + JSON files on your own PC. 8 AI tools · Windows 10/11 · made by [Founder name] |
| Link | Homepage with utm_source=tiktok&utm_medium=bio | Homepage with utm_source=instagram&utm_medium=bio (or a simple links page: Free Tier / See It Work / SmartScreen guide) |
| Account type | Business account. Check that commercial use of sounds is allowed — use only the Commercial Music Library | Professional (Creator or Business) |

##### 2.2 Cross-posting rules for S1–S6

*  Upload the  **clean**  file, without the YouTube watermark or end screen. Each platform downgrades content carrying another platform's watermark.
*  Re-add on-screen text using each app's native text tool for the hook (first 1–2 seconds). Keep burned-in captions low enough to clear each app's interface.
*  Keep text inside the central safe zone: avoid the top ~220 px and bottom ~420 px of a 1080×1920 frame, and the right edge where the buttons sit.
*  Post time: test 12:00–13:00 and 19:00–21:00 Eastern for the first two weeks, then keep what works for your own account.
*  Hashtags: 3–5 relevant ones beat 30 generic ones.

##### 2.3 Captions per Short (TikTok + Instagram Reels + Facebook Reels)
**S1 — "My AI chats are now files"**
I kept losing AI chats in sidebars, so I built a Windows app that saves them as files on my PC. ChatGPT, Claude, Perplexity and 5 more → Markdown + JSON in one folder. No account with me, no subscription. (I'm the developer.) Save this for when you're at your PC — link in profile.

#ChatGPT #ClaudeAI #productivity #windows #aitools
**S2 — "Should you click Run anyway?"**
That "Windows protected your PC" box — what it actually means, and the 10-second check to do before you click anything. Applies to every new app, including mine. (I'm the developer of TotalRecalls.)

#windows11 #techtips #cybersecurity #pctips
**S3 — "8 AI tools, 1 folder"**
ChatGPT · Claude · Perplexity · Gemini · Grok · DeepSeek · Mistral · Qwen → one folder on my PC. Your AI conversations belong to you. Windows app, link in profile. (I made it.)

#AI #ChatGPT #Gemini #productivitytips #markdown
**S4 — "What do you actually get?"**
Every AI conversation → one .md file + one .json file. Text and code blocks intact. Honest limit: images and attachments stay in your account — only references are saved. Windows app, link in profile. (I'm the developer.)

#markdown #notetaking #ChatGPT #coding
**S5 — "Check it yourself"**  — post only after the test is real
Don't trust any developer's privacy claims — including mine. Here's the network traffic while my app downloads AI chats. [Describe exactly what's shown.] #privacy #wireshark #techtok
**S6 — "When you don't need this"**
If you use one AI tool and rarely look back, your provider's own export is probably enough. This is for people juggling 3–4 AI tools every day. (I'm the developer — honesty saves us both a refund.) #AItools #productivity

##### 2.4 Native TikTok formats (beyond the Shorts)
**T1 — "Reply to comment" videos**  · ongoing. Use the reply-with-video feature to answer the top questions ("Mac?", "Is it safe?", "Why pay?") with 15–30 s screen recordings. These are highly reusable and build trust.
**T2 — "Things I found in my AI chat history"**  · D30+. Founder-voice, light: scroll the Library folder (demo or your own, carefully curated — nothing private), searching for funny or useful old chats. Script:
"I downloaded every AI chat I've had this year into one folder. Here's what I found. One: I asked three different AIs the same pasta question. [show search results across 3 subfolders]. Two: the code I lost in August — found in one search. Three: …" — CTA: "If you want your own folder — Windows app, link in profile. I built it."
**T3 — "Build in public" diary**  · weekly, optional. 20–40 s: "Week 2 of launching my first app: [one real number you're comfortable sharing], [one thing that broke], [one thing users asked for]." Real numbers only.

##### 2.5 Instagram-native formats
**Carousel C1 — "Your AI chats are disappearing (kind of)"**  · 1080×1350, 7 slides

| Slide | Text | Visual |
| ------ | ------ | ------ |
| 1 | **Your AI chats don't disappear. They just get impossible to find.** | Endless sidebar, blurred |
| 2 | Tabs close. Conversations sink under hundreds of newer ones. | Sidebar scroll arrow |
| 3 | Interfaces change. Old chats get harder to reach. | Before/after interface mock (generic, no provider UI) |
| 4 | Nobody keeps a backup. Until they need one. | Empty folder icon |
| 5 | **What if every AI chat were a file on your PC?** | Library folder tree |
| 6 | .md to read anywhere · .json to build on · one folder you control | File chips |
| 7 | TotalRecalls · Windows 10/11 · 8 AI tools · Free Tier · link in bio ·  *made by [Founder name]* | Logo + path badge |

**Carousel C2 — "How to check a new Windows app before you run it"**  · 6 slides, educational, evergreen

1.  **Before you click "Run anyway"…**
2. Download only from the developer's official site.
3. Compare the checksum: Get-FileHash file.zip -Algorithm SHA256 in PowerShell, against the hash on the download page.
4. SmartScreen warns about apps without a download history — it isn't a malware verdict either way.
5. Windows 11 Smart App Control may block unsigned apps entirely.
6. "I follow these steps for my own app too → TotalRecalls publishes its SHA-256 on the Download page."
**Carousel C3 — "8 AI tools, 1 folder"**  · 10 slides: one slide per provider (name + what you get, e.g. "Gemini → via Google Takeout → readable Markdown") plus a cover and a CTA slide. Only use claims from Part 0.2.
**Stories (Instagram + Facebook)**  · ongoing

*   **Launch day:**  a countdown sticker set for D0 (V1 premiere); a poll "How many AI tools do you use? 1 / 2–3 / 4+"; a question box "What would you never want to lose from your AI chats?" — the answers feed future content.
*   **Every new video:**  a 3-frame story: hook frame → 5 s clip → link sticker (Instagram allows link stickers in Stories).
*   **Highlights:**  "Start here" (S1 + link), "Safety" (S2, C2), "Guides" (provider list), "FAQ".
**Instagram/Threads text post (optional):**  reuse the X single posts in Part 6.

--------------------------------------------------------------------------------

#### Part 3 — Facebook (Page, Groups, Reels)
**Fit:**  Facebook isn't a primary channel in the plan, but two uses are worth it: (1) cross-posting Reels and video for very little extra effort, and (2) carefully chosen  **Groups**  where people discuss AI tools or Windows productivity. Groups have strict rules and active admins: read the rules, ask an admin when in doubt, and lead with value.

##### 3.1 Page setup

| Field | Copy |
| ------ | ------ |
| Page name | TotalRecalls |
| Category | Software · App Page |
| Intro (≤ 101 chars) | Save your AI conversations as Markdown + JSON files on your own Windows PC. |
| About | TotalRecalls is a Windows 10/11 app that saves your conversations from ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral and Qwen as plain files in a folder you control. No TotalRecalls account, no subscription. Free Tier available; Pro is $24 one-time (launch price). Not affiliated with OpenAI, Anthropic, Perplexity, Google, xAI, DeepSeek, Mistral, or Qwen. |
| Button | "Learn more" → homepage with utm_source=facebook&utm_medium=page |
| Cover (851×315 desktop; keep text centred for mobile crop) | "Your AI chats, saved as files on your PC." + folder tree |

##### 3.2 Page posts
**FB1 — Launch announcement**  · D0 (with the V1 link; native video upload is often better than a YouTube link — test both)
I built a small Windows app for a problem I kept having: losing track of AI conversations that mattered.
TotalRecalls saves your chats from ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral and Qwen as Markdown and JSON files in a folder on your own PC. You sign in to your AI tools inside the app, on your computer. There's no TotalRecalls account and no subscription.
The video shows the whole thing for real — including the Windows SmartScreen prompt you'll see the first time, and how to check the download before you run it.
{FREE_LINE} Pro is $24 one-time (launch price).
Windows 10/11 only for now. Mac and Linux are in the works.
[link with utm_content=fb1]
**FB2 — "Question for the AI-heavy crowd"**  · D3 (engagement, no link in the post)
Honest question for people who use AI tools every day: how do you find an old conversation from a month ago? Search in the app? Copy-paste into notes? Give up?
(Asking because I just built something for this — but I want to hear how you handle it today.)
**FB3 — Educational (repurposes C2)**  · D11. "5 things to check before you run a new Windows app" — the carousel as a multi-image post.
**FB4 — Provider-guide drops**  · one per tutorial (V2–V8). "New guide: how to save your [Provider] chats as files on your PC. Step-by-step video + written guide: [link]."
**FB5 — Milestone / build-in-public**  · D30. "One month since launch: what people asked for most, what I fixed, what's next." Real numbers only, and only ones you're comfortable sharing.

##### 3.3 Facebook Groups
**Finding groups:**  search Facebook for "ChatGPT users", "AI tools", "Claude AI", "AI productivity", "Windows 11", and — for the Québec experiment — "IA Québec", "entrepreneurs Montréal", "outils IA". Keep only groups that are active (posts in the last 24 h), moderated, and allow tool sharing — at least on a weekly promo thread. Log each group in a sheet: name, size, rules summary, promo allowed? (Y / thread / N), date joined.
**Rules of engagement:**  join and comment helpfully for at least a week before posting anything about TotalRecalls. Post about it at most once per group, disclosed, and reply to every comment.
**FG1 — Group post (value-first, disclosed)**
**How I stopped losing useful AI conversations (3 approaches, from free to paid)**
I use ChatGPT, Claude and Perplexity most days, and old chats were getting impossible to find. What I've tried:

1.  **Built-in export**  (ChatGPT has one in Settings → Data controls). Good for a one-off copy. You get a ZIP by email; it covers one provider.
2.  **Copy-paste the good bits into a notes app.**  Free and works, but only if you remember to do it.
3.  **A tool that saves everything as files.**  Full disclosure: I built one — TotalRecalls, a Windows app that saves chats from 8 AI tools as Markdown + JSON in a folder on your PC. There's a free tier if you want to try it.
Curious what others do — anyone have a system that actually sticks?
*(Mods: happy to remove the mention of my app if it breaks the rules.)*
Note: check the ChatGPT export path and delivery method against [OpenAI's help article](https://help.openai.com/en/articles/7260999-exporting-your-chatgpt-history-and-data) on posting day. Menu names change.
**FG2 — Promo-thread version (for weekly "share your project" threads)**
I made TotalRecalls — a Windows app that saves your AI conversations (ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral, Qwen) as Markdown + JSON files on your own PC. No account, no subscription, free tier to try. Happy to answer questions. [link with utm_content=fg2]

--------------------------------------------------------------------------------

#### Part 4 — Reddit (Supporting Channel)
**Role:**  the plan's supporting channel. Reddit rewards candour and punishes marketing voice. Each post below is written to be useful even if the reader never clicks.

##### 4.1 Before any post (every subreddit, every time)

*  [ ] Read the sidebar rules  **and**  the pinned posts. Note: self-promotion allowed? Only in a weekly thread? Account age/karma minimums? Link restrictions? Required flair?
*  [ ] If the rules are unclear, message the moderators first: "Hi — I'm the developer of a small Windows app for saving AI chats as files. Would a disclosed post about it be OK here, or is there a thread you'd prefer?" Save the reply.
*  [ ] Your account has a genuine history of helpful, non-promotional comments in that subreddit (the old Reddit guideline was roughly 9 non-promotional contributions for every 1 self-promotional one).
*  [ ] Disclosure is in the  **first two lines**  of the post.
*  [ ] Clean link (no UTM) or no link in the body — put it in a comment if the subreddit prefers that.
*  [ ] You can be online for 2–3 hours after posting to reply.
*  [ ] Don't cross-post the same text to several subreddits on the same day. Rewrite for each community.
**Candidate communities**  (check each one exists, is active, and allows this before use):

| Community | Fit | Asset | Notes |
| ------ | ------ | ------ | ------ |
| r/SideProject | Founder launch stories are the point of the sub | R1 (D0) | Most tolerant of "I built this" |
| r/ChatGPT | Biggest audience; frequent "how do I find old chats" threads | R4 (value posts, comments) | Very strict about promotion; often megathreads only |
| r/ClaudeAI | Long reasoning chats, Projects users | R2 (D9) | Check the flair/rules for tools |
| r/PerplexityAI | Threads with sources; research use | R3 (D18) | Smaller; be especially helpful |
| r/GeminiAI, r/grok, r/DeepSeek, r/MistralAI, Qwen communities | Provider-specific | R4 variants alongside V5–V8 | Check names and activity first |
| r/DataHoarder | Archiving culture; local files and checksums appreciated | R5 (D45+) | Very skeptical audience. Lead with format details, checksums and limits |
| r/windows, r/Windows11 | SmartScreen/Smart App Control discussions | Comments only | Help people; don't post the app |
| r/ObsidianMD | Markdown vaults | Only after V9 exists | Plan rule: not before a real Obsidian workflow is shown |
| ~~r/LocalLLaMA~~ | Not a fit (local model inference ≠ archiving hosted chats) | — | Excluded by the plan |

##### 4.2 R1 — Founder launch post · D0 · r/SideProject (or the best-fit sub from 4.1)
**Title options:**

1. I built a Windows app that saves your AI chats (ChatGPT, Claude + 6 others) as Markdown files on your PC
2. After losing one too many AI conversations, I built a tool to keep them as plain files — feedback welcome
**Body:**
Hi r/SideProject — I'm the solo developer of  **TotalRecalls** , and this is its first public launch, so I'd love honest feedback.
**The problem:**  I use several AI tools every day. Useful stuff — code, research, drafts — ends up buried in four different sidebars. I'd go looking for a conversation from last month and just… not find it.
**What I built:**  a small Windows 10/11 app. You sign in to your AI tools inside the app (on your own PC), and it downloads your conversations as one Markdown file + one JSON file per chat, into a folder you choose. It supports ChatGPT, Claude, Perplexity, Gemini (via Google Takeout), Grok, DeepSeek, Mistral and Qwen.
**Design decisions I'd like feedback on:**

*   **No account, no server.**  There's no TotalRecalls account and no telemetry — your session stays on your machine. You can check that with Wireshark.
*   **Plain files over a fancy UI.**  The output opens in Notepad, VS Code, Obsidian, grep — anything. There's no proprietary archive.
*   **One-time price.**  Free Tier for ChatGPT/Claude/Perplexity ({FREE_LINE}); Pro is $24 one-time for all 8. No subscription.
**Known rough edges (honest list):**

*  Windows only for now (Mac/Linux in the works).
*  Not code-signed yet, so you'll see a SmartScreen warning on first launch — and Windows 11's Smart App Control may block it entirely. The checksum is on the download page.
*  Images and attachments aren't downloaded as files, only their references.
A 4-minute screen recording of the full flow is on the site's "See It Work" page if you want to see it before downloading anything.
What would make you trust (or not trust) a tool like this? That's the question I'm most curious about.
**First comment (post it yourself, right away):**  "Link for anyone who wants it: https://www.totalrecalls.app — happy to answer anything here."
**Success measure (from the plan):**  50 upvotes, 10 comments. The real goal is the content of the comments: collect every objection into the reply bank (1.6).

##### 4.3 R2 — r/ClaudeAI value post · D9
**Title:**  How I keep my long Claude conversations searchable months later (Markdown files + a 10-second search)
Disclosure up front: I'm the developer of the tool I use for this (TotalRecalls). The workflow below works with any approach, though.
Claude conversations tend to be the long, valuable ones — reasoning through a design, a refactor plan, a long research thread. I wanted them out of the sidebar and into something I could search and keep. Here's the setup:

1.  **Get each conversation into a plain Markdown file.**  You can do this manually (copy into a .md file) or with a tool. I use mine; it saves each chat as .md + .json into Library\claude\.
2.  **One folder per provider, dated file names.**  E.g. 2026-07-28-refactor-plan.md. Dates in file names make sorting trivial.
3.  **Search the folder, not the app.**  Windows search works; VS Code "Find in Files" is better; in PowerShell: Select-String -Path .\Library\claude\*.md -Pattern "migration".
4.  **Back up the folder**  like any other documents.
Code blocks survive intact in Markdown, which was my main requirement. Images and attachments don't — only references.
How do you all handle this? Projects? Manual notes? Curious whether anyone has a better system.
**Link:**  only in a reply if someone asks, or if the subreddit's rules allow it in the body.

##### 4.4 R3 — r/PerplexityAI value post · D18
**Title:**  Keeping Perplexity research threads (and their sources) outside the app — what's worked for me
Developer disclosure: I built TotalRecalls, a Windows app that saves AI chats as files. Mentioning it because it's part of my workflow, but the question is genuinely open.
I use Perplexity mostly for research, and the value is half in the answer and half in the sources. When a thread turns into something I'll come back to, I want both in a file I own.
What I do now: download the threads as Markdown + JSON into a local folder (my tool keeps source references alongside the conversation — [ **only include this if your V4 recording shows it** ]), then search the folder when I need something.
Questions for the sub:

*  Do you re-open old threads, or treat Perplexity as disposable?
*  Anyone built a "research library" from their threads? What format?

##### 4.5 R4 — Ongoing value posts and comments · D29–60 (2 per week, 90% with no link)
**Post ideas**  (no link unless asked):

1. "PSA: three ways to keep a copy of your AI chats (and what each one misses)" — built-in exports, copy to notes, tools. Fair to all three.
2. "I searched one year of AI conversations at once. Here's what I learned about how I use AI." — personal insights from your own (curated) library, with counts by provider and topic. Mention the tool once, at the end, disclosed.
3. "Markdown vs JSON for archiving AI chats — why I keep both" — format discussion that's useful to developers.
4. "What actually happens when Windows says 'Windows protected your PC'" — the S2/C2 content as a text post in r/Windows11 (if allowed), with no app link.
**Comment templates**  (when someone asks "how do I find/save old chats?" — adjust every time, never paste the same text twice):
If you only need one provider, the built-in export is the simplest ([ChatGPT's is in Settings → Data controls](https://help.openai.com/en/articles/7260999-exporting-your-chatgpt-history-and-data)). If you use several AI tools and want them all as files, I built a Windows app for that — TotalRecalls (disclosure: it's mine). It saves each chat as Markdown + JSON in a local folder. There's a free tier if you want to test it.

##### 4.6 R5 — r/DataHoarder post · D45+ (only after Gate item 5 — per-provider export tests — is done)
**Title:**  Archiving AI chat history from 8 providers as Markdown + JSON — format notes and limits (dev here)
Developer disclosure: I built the tool below, and I'm posting because this sub cares about formats and integrity, and I'd value critique.
**What it produces:**  one .md + one .json per conversation, in per-provider folders, with dated file names: Library\<provider>\YYYY-MM-DD-title.md.
**What's captured / not captured**  (tested on [date], v[1.x]):

| Provider | Text | Code blocks | Sources/attachment refs | Binary attachments |
| ------ | ------ | ------ | ------ | ------ |
| [fill from your Gate 5 tests] |  |  |  | ✗ (stays in provider account) |

**Integrity:**  the release ZIP has a published SHA-256. The app is portable (no installer, no background services).
**Known limits:**  Windows only; unsigned for now (SmartScreen/Smart App Control); depends on provider web interfaces, which change — updates are free.
I'd especially like feedback on the JSON structure and file naming for long-term archives.

##### 4.7 Reddit reply bank (additions to 1.6)

| Comment | Reply |
| ------ | ------ |
| "This is just an ad." | "Fair to flag it — I'm the developer and I said so up top. I tried to make the post useful without the app; if it isn't, tell me what would be." |
| "Closed source + my login = no." | "Totally reasonable position. Two things you can check without trusting me: the SHA-256 of the download, and the network traffic while it runs (Wireshark). If that's still not enough, the manual copy-to-Markdown approach works — it's just slower." |
| "Why not open source?" | Answer honestly with your actual reasoning. Don't promise open-sourcing unless you've decided to. |
| Downvoted to 0 in the first hour | Don't delete and repost. Leave it, answer the comments, and learn from them. |


--------------------------------------------------------------------------------

#### Part 5 — LinkedIn (Repurposing Channel)
**Angle:**  the professional value of AI work — research, client deliverables, decisions — and keeping that work in files you control. Post from your  **personal profile**  (it gets far more reach than a company page); the company page is a credibility anchor.

##### 5.1 Setup

*   **Personal headline addition:**  "… · Building TotalRecalls — your AI conversations, saved as files on your PC"
*   **Featured section:**  V1 video link · See It Work page · Download page
*   **Company page:**  name TotalRecalls; tagline "Your AI conversations, saved as Markdown + JSON files on your own PC."; industry Software Development; website with utm_source=linkedin&utm_medium=page
*   **Format rules:**  the first 2 lines decide whether people click "…see more", so make them count. Short paragraphs. Many LinkedIn users believe outbound links in the post body reduce reach — test link-in-post vs link-in-first-comment for your own account. 3 hashtags maximum.

##### 5.2 L1 — Product-purpose post · D3
Your best work this year might be sitting in an AI chat sidebar.
Research for a client. A pricing analysis. The reasoning behind a decision. Code you'll need again. For a lot of us, that work now happens in conversations with ChatGPT, Claude, Perplexity and others — and those conversations sink under hundreds of newer ones.
Interfaces change. Tabs close. Nobody keeps a backup until they need one.
I built TotalRecalls to fix that for myself. It's a Windows app that saves your AI conversations as Markdown and JSON files in a folder on your own PC — from 8 AI tools, into one library you can search, back up and keep.
A few deliberate choices: → No TotalRecalls account. You sign in to your AI tools locally, inside the app. → No cloud. Your chats aren't sent to my servers. → Plain files. They open in Word, Notepad, Obsidian, anything. → One payment, no subscription.
If you use AI for real work, I'd love to know: do you keep any record of those conversations today?
[Link in first comment] · #AI #Productivity #KnowledgeManagement
**First comment:**  "Here's a 4-minute recording of the whole flow, and a free tier to try it on your own chats (Windows 10/11): [link with utm_content=l1]"

##### 5.3 L2 — Product Hunt launch day · D15
Today TotalRecalls is on Product Hunt.
It's a small Windows app that does one thing: saves your conversations from ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral and Qwen as plain Markdown and JSON files on your own PC.
What I learned in the first two weeks since launch: • [Real lesson #1 — e.g., the most common question people asked] • [Real lesson #2 — e.g., what confused first-time users and what I changed] • [Real lesson #3]
If you have a minute, I'd value your honest feedback on the Product Hunt page — questions and criticism included. [link in first comment]

#ProductHunt #BuildInPublic #AI
*(Product Hunt's community guidelines discourage asking for upvotes — ask for feedback, not votes.)*

##### 5.4 L3 — Founder story · D22
I lost a conversation that was worth about a day of work.
[Your real story, 3–5 short paragraphs: what you were working on, which AI tools you were using, the moment you couldn't find it, what you tried, why you decided to build something.]
The fix turned out to be simple: treat AI conversations like documents. Save them as files. Put them in a folder. Search the folder.
That became TotalRecalls. [One line about where it is now — real figures only.]
What's the one AI conversation you'd hate to lose?

##### 5.5 L4 — Professional data-ownership angle (consultants, researchers) · D35
A question worth asking your team: where does your AI-assisted work actually live?
If the answer is "in each person's chat history", that's work product sitting in a dozen sidebars, across several providers, with no consistent copy.
Three low-effort habits that help:

1. Save AI conversations that lead to a deliverable as a file, alongside the deliverable.
2. Use one format (Markdown is readable everywhere and future-proof).
3. Keep it in the same place you keep the rest of the project.
Disclosure: I built a Windows app that automates #1 and #2 — TotalRecalls. But the habit matters more than the tool.

#KnowledgeManagement #AI #Consulting
*Be careful with this angle:*  don't suggest it solves compliance, records-retention or confidentiality obligations. It doesn't claim to, and organisations have their own policies on AI tools and data.

##### 5.6 LinkedIn carousel (document post) — L5 · optional
Upload C1 (Part 2.5) as a PDF document post, at 1080×1350 per page. Caption: "Your AI chats don't disappear — they just get impossible to find. 7 slides on keeping them."

--------------------------------------------------------------------------------

#### Part 6 — X (Repurposing Channel)
**Setup:**  handle @totalrecalls (or the founder's personal account — usually better for reach; then link @totalrecalls in the bio). Bio: "Building TotalRecalls — your AI chats, saved as Markdown + JSON files on your PC. Windows. 8 AI tools." Pin X1.
**Format rules:**  each post ≤ 280 characters (unless you have a Premium account and choose longer posts). Images and short clips outperform plain text. One link per thread, in the last post.

##### 6.1 X1 — The workflow thread · D2
**1/**  I kept losing useful AI conversations across ChatGPT, Claude and Perplexity. So I built a Windows app that saves them all as files on my PC. Here's the whole flow in 5 steps: [image: Library folder tree]
**2/**  Step 1: download a ~18 MB ZIP. Portable app, no installer. The SHA-256 is published on the download page — check it with Get-FileHash before running anything. [image: PowerShell hash match]
**3/**  Step 2: first launch shows "Windows protected your PC". The app is new and not code-signed yet. More info → Run anyway, once you've checked the file. (Windows 11 Smart App Control may block it entirely — code signing is on the roadmap.) [image: SmartScreen dialog]
**4/**  Step 3: pick a provider and sign in — inside the app, on your PC. No account with me. The app lists your conversations and their count before downloading anything. [image: provider list]
**5/**  Step 4: download. Every conversation becomes one .md and one .json file, in a subfolder per provider. [image: Explorer with file pairs]
**6/**  Step 5: search the folder. One search across ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral and Qwen at once. [GIF: search finding a term across subfolders]
**7/**  Honest limits: Windows 10/11 only (Mac/Linux in the works). Images and attachments stay in your account — only references are kept. Free tier: ChatGPT, Claude, Perplexity. Pro: $24 one-time. I'm the developer → [link with utm_content=x1]
*Check each post's length after filling placeholders. Posts 3 and 7 are close to 280 characters.*

##### 6.2 X2 — Privacy-verification single post · D8
Don't trust any app's privacy page. Including mine.
TotalRecalls says: no telemetry, no TotalRecalls account, your chats aren't sent to its servers.
Check it yourself: run Wireshark while it downloads your AI chats and see what it connects to. [clip from S5 — only once recorded]
*(If S5 isn't recorded by D8, post the text with a screenshot of the FAQ privacy lines and swap the clip in later.)*

##### 6.3 X3 — Product Hunt launch day · D15 (3 posts across the day)

*   **Morning:**  "TotalRecalls is live on Product Hunt today. A Windows app that saves your AI conversations from 8 tools as Markdown + JSON files on your PC. I'd love your honest feedback → [PH link]" + S1 clip
*   **Midday:**  "Most asked question on Product Hunt so far: '[real question]'. Answer: [real answer]." (real only)
*   **Evening:**  "Thank you to everyone who commented today. Biggest lesson: [real lesson]."

##### 6.4 X4 — Objection handler · D25
"Why would I pay $24 when ChatGPT has a free export?"
If you only use ChatGPT, maybe you shouldn't.
TotalRecalls is for people who use several AI tools and want all of it in one folder, as plain files, with one payment and no subscription. Try the free tier first and decide.

##### 6.5 X5 — Single-post bank (3/week, recycled from YouTube and community content)

| # | Post | Visual |
| ------ | ------ | ------ |
| 1 | Tabs close. Interfaces change. Nobody keeps a backup. Until they need one. Your AI chats, saved as files on your PC → [link] | Library folder |
| 2 | A Markdown file opens the same way in Notepad next year, whatever the chat interface looks like. That's the whole idea. | .md in Notepad |
| 3 | 8 AI tools. 1 folder. ChatGPT · Claude · Perplexity · Gemini · Grok · DeepSeek · Mistral · Qwen | S3 clip |
| 4 | Gemini users: Google Takeout gives you your data. TotalRecalls turns that Takeout folder into readable Markdown. Guide: [Gemini guide link] | Takeout → .md |
| 5 | The Windows SmartScreen warning in 40 seconds — what it means, and the 10-second check before you click "Run anyway". | S2 clip |
| 6 | Build in public, week [N]: [one real number] · [one bug fixed] · [one request heard]. | Screenshot |
| 7 | Every conversation → one .md + one .json. Text and code blocks intact. Images stay in your provider account. Honest limits > surprises. | S4 clip |
| 8 | Your AI conversations belong to you. (Windows app, I'm the developer → [link]) | End-card graphic |

**Reply strategy:**  search X daily for phrases like "lost my chatgpt conversation", "can't find old claude chat", "export perplexity threads". Reply helpfully, and mention TotalRecalls only when it directly answers the question, with disclosure ("I built a tool for this: …"). Keep it to 5–10 replies per day at most; avoid anything that looks automated.
**Threads / Bluesky (optional):**  cross-post X5 single posts as-is. These communities skew toward tech and developers, which is a reasonable fit.

--------------------------------------------------------------------------------

#### Part 7 — Launch Events: Product Hunt and Hacker News
##### 7.1 PH1 — Product Hunt · D15 (only after the D14 gate passes)
**Prep (D8–D14):**  create or warm up the maker account (comment on other launches for a week); prepare the gallery; schedule the launch for 00:01 Pacific (Product Hunt's day starts at midnight PT, which is 03:01 in Montréal); block the whole day to reply.

| Field | Copy |
| ------ | ------ |
| Name | TotalRecalls |
| Tagline (keep ≤ 60 characters; check the current limit) | **Save your AI chats as Markdown files on your PC**  (47) — alt: "8 AI tools, one folder of your chats, on Windows" (48) |
| Topics | Productivity · Artificial Intelligence · Windows · Developer Tools |
| Pricing | Free options (Free Tier) + paid (one-time) |
| Links | Homepage with utm_source=producthunt&utm_medium=launch&utm_content=ph1 |
| Thumbnail | The TotalRecalls mark (240×240, a GIF is allowed — e.g., files dropping into a folder) |

**Description (≤ 500 characters; check the limit):**
TotalRecalls is a Windows 10/11 app that saves your conversations from ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral and Qwen as Markdown + JSON files in a folder on your own PC. You sign in to each AI tool locally, inside the app — there's no TotalRecalls account, no cloud and no telemetry. Search, back up and keep your AI work as plain files. Free Tier for ChatGPT, Claude and Perplexity; Pro is $24 one-time.
**Gallery (1270×760, 5–6 images; every image a real capture):**

1. Hero: the Library folder tree with 8 subfolders + the headline "Your AI chats, saved as files on your PC"
2. Provider list in the app, with the caption "8 AI tools. Sign in locally, inside the app."
3. Download progress with conversation count — "See your history before you download"
4. .md open next to .json — "Markdown to read anywhere. JSON to build on."
5. Search across subfolders — "Find any chat again in seconds" (only if your recording shows that speed)
6. Trust card: "No account · No cloud · No telemetry · SHA-256 published · $24 one-time"
*  Video: V1, or a 60–90 s cut of it (YouTube link)
**Maker's first comment:**
Hi Product Hunt — I'm [Founder name], the solo developer of TotalRecalls.
**Why I built it:**  I use several AI tools every day, and the useful conversations — code, research, decisions — kept getting lost in sidebars. I wanted them as plain files I own.
**What it does:**  sign in to your AI tools inside the app (on your PC), pick a folder, click Download. Each conversation becomes a .md and a .json file. 8 providers; Gemini works via your Google Takeout folder.
**What it deliberately doesn't do:**  no TotalRecalls account, no cloud, no telemetry, no subscription.
**Honest limits:**  Windows only for now (Mac/Linux in the works). Not code-signed yet, so you'll see a SmartScreen prompt — and Windows 11 Smart App Control may block it. Attachments aren't downloaded, only their references.
**For today:**  [launch-week offer, if any — the plan suggests something like extended free limits rather than a discount, to protect the $24 price. Only include it if it's implemented.]
I'll be here all day. The questions I'd most like to hear: what would make you trust a tool like this, and which feature would make it a must-have for you?
**Day-of schedule (Eastern time):**

| Time | Action |
| ------ | ------ |
| 03:01 | Launch goes live; post the first comment immediately |
| 07:00 | X3 morning post; LinkedIn L2; email your personal list (people who already know you) — ask for feedback, not upvotes |
| 08:00–23:00 | Reply to every comment within 30 minutes; log questions for the FAQ |
| 12:00 | X3 midday post; Instagram/Facebook Story with the PH link |
| 20:00 | X3 evening thank-you |
| Next day | Write up the results (visits by UTM, download clicks, sales, top questions) |

**Rules:**  don't ask for upvotes, don't use upvote groups, don't create fake accounts. Product Hunt penalises all of these, and they distort your data.

##### 7.2 HN1 — Show HN · optional, D20–30
**Fit:**  a local-first, file-based, no-account tool is the kind of thing Hacker News readers like to examine — and criticise. Their expectations: something people can actually try (the Free Tier qualifies), a plain-voiced post, and the maker present in the comments.
**Title (HN style — plain, no marketing words):**
Show HN: TotalRecalls – Save your AI chats from 8 providers as Markdown on Windows
**URL field:**  https://www.totalrecalls.app (clean link)
**Text (first comment, posted by you):**
Hi HN — I built this because my AI conversations (ChatGPT, Claude, Perplexity, etc.) had become a big chunk of my working notes, and they were scattered across sidebars I don't control.
TotalRecalls is a portable Windows app (~18 MB ZIP, no installer). You sign in to each provider inside the app; it enumerates your conversations and writes each one as a Markdown file plus a JSON file into a local folder, organised by provider. Gemini goes through a Google Takeout export instead.
Some details people here may care about:

*  No account, no server component, no telemetry. Session tokens stay on the machine. Happy for anyone to put it behind Wireshark and report what they see.
*  SHA-256 of the release is published on the download page.
*  Unsigned for now, so SmartScreen will warn; Windows 11 Smart App Control may block it outright. Signing is on the roadmap.
*  It depends on provider web interfaces, which change. That's the main maintenance burden, and updates are free.
*  Attachments: references only, not the binaries.
Pricing: free tier (ChatGPT/Claude/Perplexity, limited conversations), $24 one-time for all 8 providers.
I'm especially interested in feedback on the output format (file naming, JSON structure) and on what would make a closed-source tool like this trustworthy enough to use.
**Prepare for:**  "Why not open source?", "This violates ToS", "Why not just use the official exports?", "How do you handle auth?" — have short, factual answers ready (1.6, 4.7, and Part 9's terms review). Never argue. Thank critics.
**Posting time:**  US weekday mornings (about 08:00–10:00 Eastern) are commonly recommended. You only get one real shot, so don't repost the same Show HN if it doesn't take off.

--------------------------------------------------------------------------------

#### Part 8 — Master Calendar and Measurement
##### 8.1 Asset calendar (aligned with the Launch Plan's 90-day calendar; the new channels are folded in)

| Day | YouTube | TikTok / IG / FB Reels | Instagram native | Facebook | Reddit | LinkedIn | X | Event |
| ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| D−10 | Record V1 + S1–S4 (one session, Appendix B) |  |  |  |  |  |  |  |
| D−7 | Channel setup (1.1) | Profile setup | Profile setup | Page setup | Read rules, start commenting | Profile updates | Bio, pin placeholder |  |
| D0 | **V1**  premiere |  | Story countdown → V1 | FB1 | **R1** |  |  | Launch |
| D2 |  |  |  |  |  |  | **X1** |  |
| D3 |  |  |  | FB2 |  | **L1** |  |  |
| D4 | **S1** | S1 |  |  |  |  |  |  |
| D5 | **V2**  ChatGPT |  |  | FB4 |  |  | X5-1 |  |
| D7 |  |  | **C1** |  |  |  |  | Checkpoint |
| D8 |  |  |  |  |  |  | **X2** |  |
| D9 |  |  |  |  | **R2**  r/ClaudeAI |  |  |  |
| D11 | **S2** | S2 |  | FB3 |  |  | X5-5 |  |
| D12 | **V3**  Claude |  |  | FB4 |  |  |  |  |
| D14 |  |  | **C2** |  |  |  |  | **Gate** |
| D15 |  |  | Story → PH |  |  | **L2** | **X3**  ×3 | **PH1** |
| D16 | **V4**  Perplexity |  |  | FB4 |  |  |  |  |
| D18 |  |  |  |  | **R3**  r/PerplexityAI |  |  |  |
| D20 | **S4** | S4 |  |  |  |  | X5-7 | (HN1 window opens) |
| D22 | **S3** | S3 |  |  |  | **L3** | X5-3 |  |
| D25 | **V5**  Gemini |  | **C3** | FB4 |  |  | **X4** , X5-4 |  |
| D28 |  |  |  |  |  |  |  | **Gate** |
| D29–60 | V6–V8 (1/week) | T1 replies, T2 | Stories per video | FB4, FG1/FG2 in vetted groups | R4 2×/week; R5 at D45+ | L4 (D35), L5 | X5 3×/week | Paid test A1 (D35, only if the gate passes) |
| D30+ | S5 (once tested), S6 | S5, S6, T3 weekly |  | FB5 (D30) |  |  | X5-6 weekly |  |
| D60 | V9 (conditional) |  |  |  | r/ObsidianMD (only after V9) |  |  |  |

##### 8.2 What to measure per asset (weekly sheet)

| Column | Source |
| ------ | ------ |
| Asset ID, channel, publish date/time | You |
| Views / impressions | Platform analytics |
| Engagement (comments, saves/shares, upvotes) | Platform analytics |
| Site visits with matching utm_content | Cloudflare, with TotalRecallsAudit excluded (Launch Plan, Section 11) |
| /download/ pageviews that day vs baseline (≈ 9/day, from 63/week) | Cloudflare |
| Download clicks | Once Gate item 8's measurement exists |
| Pro purchases | Paddle |
| Top questions/objections | Comments → add to the reply bank and the FAQ |

**What "working" looks like**  (initial hypotheses — replace them after D28): a video or post that produces site visits  *and*  a visible rise in /download/ pageviews above the baseline, and comments that ask "how" rather than "what". Kill or rework any format that gets views without visits after three tries.

--------------------------------------------------------------------------------

#### Part 9 — Pre-Publish Review Checklist (every asset)
**Claims**

*  [ ] Every product statement is in the claims register (0.2), or has been recorded working
*  [ ] {FREE_LINE} replaced with the confirmed wording (Gate 1)
*  [ ] No "safe/secure/trusted/only/first" guarantees
*  [ ] No add-on promises; no dates for Mac/Linux
*  [ ] Limits stated where relevant (Windows-only, unsigned/SmartScreen, Smart App Control, attachments)
**Disclosure and rules**

*  [ ] "I'm the developer" (or equivalent) is visible without clicking
*  [ ] Community rules re-read on the day of posting (Reddit, Facebook Groups, HN, PH)
*  [ ] No vote/upvote requests anywhere
**Privacy in media**

*  [ ] Demo accounts only; emails, names, keys and real chat titles blurred
*  [ ] No real customer data or quotes without written permission
**Provider relationships — get these reviewed before launch**

*  [ ] The "not affiliated with…" line in every description and profile
*  [ ] Provider logos only if their brand guidelines allow it; otherwise text names
*  [ ] The reply about provider terms of service (1.6) has been reviewed by you, and ideally a lawyer. Some AI providers' terms restrict automated access to their services, and users will ask. The content should never say or imply that using TotalRecalls is approved by a provider or definitely compliant with its terms
**Links**

*  [ ] UTM tags correct (utm_content = the asset ID); clean links on Reddit and HN
*  [ ] Links point to the homepage or a guide page (so the SmartScreen and Smart App Control notes are seen), not straight to the ZIP

--------------------------------------------------------------------------------

#### Appendix A — French (Québec) Versions · optional experiment
The traffic baseline shows Canada as the largest identified country (Launch Plan, Section 11). That's not yet proof of Québec demand, but the cost of testing is low. Before posting, check that the site's French coverage matches what these posts promise. If the site is English-only, say so ("site en anglais").
**FB1-FR — Annonce (Page Facebook)**
J'ai créé une petite application Windows pour un problème que j'avais sans cesse : perdre la trace de conversations d'IA importantes.
TotalRecalls enregistre vos conversations de ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral et Qwen sous forme de fichiers Markdown et JSON, dans un dossier sur votre propre PC. Vous vous connectez à vos outils d'IA directement dans l'application, sur votre ordinateur. Aucun compte TotalRecalls, aucun abonnement.
La vidéo montre tout, pour vrai — y compris l'avertissement SmartScreen de Windows au premier lancement, et comment vérifier le fichier avant de l'exécuter.
Version gratuite : ChatGPT, Claude et Perplexity — 5 conversations par téléchargement, sans carte ni compte. Pro : 24 $ US, paiement unique (prix de lancement).
Windows 10/11 seulement pour l'instant. Mac et Linux sont en préparation.
(Je suis le développeur de TotalRecalls.) [lien]
*(Replace the free-tier sentence if the confirmed {FREE_LINE} changes: "5 conversations par fournisseur".)*
**L1-FR — LinkedIn**
Votre meilleur travail de l'année dort peut-être dans la barre latérale d'un clavardage d'IA.
Une recherche pour un client. Une analyse de prix. Le raisonnement derrière une décision. Du code dont vous aurez encore besoin. Ce travail se fait de plus en plus dans des conversations avec ChatGPT, Claude, Perplexity et d'autres — et ces conversations s'enfouissent sous des centaines de nouvelles.
J'ai créé TotalRecalls pour régler ça. C'est une application Windows qui enregistre vos conversations d'IA en fichiers Markdown et JSON, dans un dossier sur votre PC — 8 outils d'IA, une seule bibliothèque que vous pouvez fouiller, sauvegarder et conserver.
→ Aucun compte TotalRecalls : vous vous connectez localement, dans l'application. → Pas de nuage : vos conversations ne sont pas envoyées à mes serveurs. → Des fichiers ordinaires : ils s'ouvrent dans Word, le Bloc-notes, Obsidian… → Un seul paiement, pas d'abonnement.
Si vous utilisez l'IA pour du vrai travail : gardez-vous une trace de ces conversations aujourd'hui?

#IA #Productivité #GestionDesConnaissances
**S1-FR — Légende courte (TikTok / Reels)**
Je perdais mes conversations d'IA dans les barres latérales, alors j'ai créé une appli Windows qui les enregistre en fichiers sur mon PC. ChatGPT, Claude, Perplexity et 5 autres → Markdown + JSON dans un seul dossier. Aucun compte, aucun abonnement. (C'est moi le développeur.) Lien dans le profil — à ouvrir sur ton PC.

#IA #ChatGPT #productivité #Windows #Québec
**S3-FR — Légende**
ChatGPT · Claude · Perplexity · Gemini · Grok · DeepSeek · Mistral · Qwen → un seul dossier sur mon PC. Tes conversations d'IA t'appartiennent. Appli Windows, lien dans le profil. (Je l'ai créée.)
**Burned-in French captions for S1:**  « Où est passée cette conversation? » → « Connexion sur ton PC → téléchargement » → « Chaque conversation devient un fichier » → « Cherche dans tout, d'un coup » → « TotalRecalls · Windows »

--------------------------------------------------------------------------------

#### Appendix B — One-Day Recording Session (produces V1, V2, S1–S4 and all stills)
**Prep (the day before)**

*  [ ] Fresh Windows user profile, 100–125% scaling, neutral wallpaper, notifications off (Focus Assist), clock hidden or neutral
*  [ ] Demo accounts on ChatGPT, Claude and Perplexity (and Pro providers, for S3 and later tutorials), each with 15–30 harmless demo conversations, including at least one with a code block and one with sources
*  [ ] The latest ZIP downloaded fresh from the live Download page; checksum noted
*  [ ] OBS (or similar): 1920×1080 at 30 fps; a second scene with the app window centred at ~1000 px wide for vertical crops
*  [ ] USB mic levels checked; room quiet
*  [ ] Script (1.2) printed or on a second screen
**Shot list (in this order — it follows the real first-run sequence, which only happens once per profile)**

| # | Shot | Used in |
| ------ | ------ | ------ |
| 1 | Sidebar scrolls (demo accounts) in each provider | V1 cold open, S1, C1 |
| 2 | Website → Download page → ZIP download | V1, X1-2 |
| 3 | PowerShell Get-FileHash with matching output | V1, S2, C2, X1-2 |
| 4 | Unzip; first launch;  **real SmartScreen dialog** ; More info → Run anyway | V1, S2, X1-3 |
| 5 | (Separately, if available) Smart App Control on a Windows 11 test machine — what users see | S2, FAQ support |
| 6 | Provider list → ChatGPT → sign-in (blur) → conversation count → folder choice → Download → completion | V1, V2, S1, X1-4/5 |
| 7 | Repeat for Claude and Perplexity | V1, V3, V4, S3 |
| 8 | File Explorer tour; .md in Notepad, VS Code/Markdown preview, Word; .json in VS Code | V1, S4, C1, PH gallery 4 |
| 9 | Search across the Library (Windows search + VS Code + Select-String) | V1, S1, X1-6, PH gallery 5 |
| 10 | Copy the Library to a USB/backup folder | V1 |
| 11 | Clean stills: folder tree, file pair, provider list, pricing section | Thumbnails, carousels, PH gallery, X images |
| 12 | (Optional) talking-head intro and outro, 3 takes each | V1, S6, T1 |
| 13 | (Later session) Wireshark capture during a download | S5, X2 |

**After the session:**  export a vertical (9:16) cut of shots 1, 4, 6, 8 and 9 for the Shorts. Write down the real numbers you saw (conversation counts, durations) so captions and claims match the footage.

--------------------------------------------------------------------------------

#### Appendix C — Keyword and Hashtag Bank
**Search phrases**  (YouTube titles, guide pages, descriptions — check real volume in YouTube search suggestions and your own analytics): save chatgpt conversations · export chatgpt history · backup chatgpt chats · download claude conversations · save claude chat history · export perplexity threads · gemini takeout chat history · save ai chats to pc · ai chat history markdown · archive ai conversations
**Hashtags (pick 3–5 per post):**

*  General: #AI #AItools #productivity #productivitytips
*  Providers (only when that provider is shown): #ChatGPT #ClaudeAI #Perplexity #Gemini #Grok #DeepSeek
*  Format/workflow: #markdown #notetaking #knowledgemanagement #obsidian (Obsidian only after V9)
*  Windows/safety: #windows11 #pctips #cybersecurity #techtips
*  Founder: #buildinpublic #indiehacker #solofounder
*  French: #IA #productivité #Québec #outilsIA

--------------------------------------------------------------------------------

*[This content pack contains drafts only. Nothing has been published, scheduled, purchased, or recorded. Product facts come from the TotalRecalls website as of 2026-10-23 (homepage, FAQ, Download, See It Work, Microsoft Warning) and have not been independently tested. The ChatGPT export reference points to OpenAI's help article. Platform specs and limits (character counts, image sizes) change — check them on the day of posting.](https://www.totalrecalls.app)*


## 9. Funnel Audit, Leak Points & Analytics

#### 9. Funnel & leak points
From V3 §11 "How Everything Connects" + the Launch-Day Checklist:

*   **Discovery**  (YouTube launch set, social Day 0–29, guides/SEO, Reddit) →  **Evaluation**  (site homepage → See It Work / demo → pricing) →  **Trial**  (Free Tier download: ChatGPT/Claude/Perplexity, 5 conversations — wording per D5) →  **Purchase**  (Pro $24, Paddle) →  **Retention**  (footer email on real news; provider-guide + explainer content).
*  Every asset carries the CTA hierarchy; every link is UTM-tagged so video → blog → social → email are measurable as one funnel.
*  Cross-references are already written into the content: each provider guide embeds its video; each blog post links its video; each video's description links the guide; the Day 0–29 calendar's 6 Blog rows tie social to the blog.
*  The single tracking sheet (V3 Weeks 1–2 "Systems") records, per video and per blog post: title, claims, date, version, UTM campaign, status. This is the KPI baseline generator (there is no pre-launch traffic data — baselines are "to be measured" until Week 8's first monthly metrics review).
**Leak points (measured/verified 2026-10-13 where marked):**

| Stage | Instrumentation needed | Leak risk |
| ------ | ------ | ------ |
| Discovery | GSC (verified 2026-10-01) + GA + launch UTMs from Week 0 | no traffic baseline exists — "to be measured" until Week 8 |
| Evaluation | per-page GA | blog surface is 404 (verified) — the 9-post series has nowhere to publish until D2 lands |
| Trial (download) | download counters | **SmartScreen: no code signing**  (roadmap-only per /download/) — first-launch warning is the #1 trial-conversion leak; Windows 11 Smart App Control may block with no override |
| Purchase | Paddle analytics | launch discount dsc_01m398… has  **no visible expiry**  (D6) — urgency copy has nothing to point at; free-tier wording conflict (D5) can make the trial feel broken |
| Retention | ESP dashboard | ESP not chosen (D9); footer signup unwired until Week 0 tasks done; no other update channel (V3 "real news only") |


## 10. Budget Scenarios, Risk Matrix & Governance

#### 14. Budget

| Item | Cost | Why (or why deferred) |
| ------ | ------ | ------ |
| OV code-signing cert (e.g. Sectigo / GoGetSSL / DigiCert — get a quote) | ~$100–400/yr depending on CA (quote at purchase; not a committed figure) | **The long pole — start in Week 0.**  SmartScreen warnings kill trial conversion (the #1 leak, §9); issuance + identity verification takes days |
| Domain + hosting | $0 | Cloudflare Pages free tier; domain already owned; GSC verified |
| Email ESP | $0 at launch | 500-signup target fits the free tiers of common ESPs (Brevo/MailerLite/ConvertKit — pick in D9) |
| Social / YouTube / Reddit | $0 | existing accounts; zero-cost channels only in the 12-week window |
| Paid ads | $0 until Week-8 kill criteria pass | solo operator, no activation data yet; §11 defines the gate (≥8% Free→Pro, CTR ≥3%, CAC < $24) |
| **Phase-0 total** | **≈ cert only** | everything else is zero-cost by design (one-operator reality) |

#### 15. Risks

| Risk | Likelihood | Mitigation | Owner |
| ------ | ------ | ------ | ------ |
| SmartScreen / Smart App Control blocks trials (no code signing) | High | cert ordered in Week 0 (long pole); /download/ already discloses the warning; "More info → Run" path documented in FAQ | Andre |
| Launch discount expires silently (no visible expiry in live config) | Medium | D6 sets the date before Week 3; Day-42 urgency post points at it | Andre |
| Free-tier wording conflict confuses trial users (D5) | Medium | verify in-app first, fix the wrong page before launch — everything inherits the wording | Andre |
| YouTube OAuth 403 org_internal blocks API uploads at launch | Medium | consent fix recipe in STATUS-2026-10-01; fallback = manual upload (9 videos, one session) | Andre |
| Blog 404 gates the Week-3 launch post | High (404 verified 2026-10-13) | D2 in Week 0–1; if the Astro build slips, fallback (b) = publish under /guides | Andre |
| Provider-specific claim ships unverified (per-provider limits differ) | Medium | accuracy guardrail (V3 §14): nothing ships unverified; 🔍 Confirm list in §16 | Andre |
| macOS/Linux demand with no ETA | Medium | messaging locked "in development," no dates — never announce before shipped | Andre |
| Solo-operator bandwidth (2 videos/wk + weekly blog + daily social for 12 weeks) | High | "the minimum week" floor (V3 §13); TikTok/Threads off by default (D4); community posts batched, not daily | Andre |
| Multi-estimate market numbers get quoted wrong in copy | Low | §2 numbers are dated + sourced; copy uses only §1 proof points, never §2 stats (stats are context, not claims) | Andre |

#### 16. Decision items (user picks before public/paid action)

| # | Decision | Options | Default if unchosen |
| ------ | ------ | ------ | ------ |
| D1 | Blog B1/B2 topics + the 3 extra drafts (PowerShell, Backup-Windows, Library Folder) | (a) B1 = launch announcement, B2 = Library Folder explainer, PowerShell → B7 "organizing" slot, Backup-Windows merged into B5, Library Folder also gets its own page (V3 Week 3–4 "publish the Library Folder page"); (b) keep V3's "confirm topics" open and wait for Jasper | (a) — matches the on-disk drafts and the Week 3–4 website task |
| D2 | Blog surface | (a) build /blog on the Cloudflare Pages Astro site (site/); (b) publish the series under the existing /guides section | (a) — V3's internal linking and the Day 0–29 calendar's Blog rows assume a distinct blog URL |
| D3 | Opt-in model for footer signup | (a) single opt-in (simpler, V3-era default); (b) double opt-in (cleaner list) | (a), flagged in V3 Week 0 as 🔍 Confirm |
| D4 | TikTok + Threads (in the Day 0–29 calendar, absent from the launch-day runbook) | (a) operate them; (b) keep the rows as reference, post only on FB/IG/LinkedIn/X | (b) — 4 channels is the solo-operator floor |
| D5 | Free Tier wording: "5 conversations  **each** " (homepage) vs " **per download** " (/download/) | (a) per provider (3 providers × 5 = 15 total); (b) per download session — fix whichever page is wrong | (a), matching the pricing page and the app's actual limits — verify in-app first, then fix the /download/ page |
| D6 | Launch-discount expiry date (live config has discount id dsc_01m398… but no visible expiry) | set the date in Paddle + publish it on /pricing/ | no date = the Day-42 urgency post has nothing to point at — set a date before Week 3 |
| D7 | Actual private-video count in "Start Here" (status note says 8 uploads; worklist lists 7 providers + hero) | count in Studio, upload Qwen to reach the full 8 | count + upload Qwen |
| D8 | Channel-sub target for launch week (Launch Campaign gives no YouTube number) | set a number | 250 subs by Week 8 (to be set) |
| D9 | Email service provider for footer signup (must be named in the Privacy Policy — V3 Week 0 🔍) | pick + name in policy | — |
| D10 | ~~Delete the file-locked email/Email Sequence (fragment).docx~~   **DONE 2026-10-13**  — file unlocked and deleted | — | — |


## 11. Marketing Asset Index & Deduplication Log

### TotalRecalls Marketing — Asset Index
Reorganized 2026-09-29 from Jasper's flat canvas/jasper/YouTube exports into a topical structure, deduped (SHA256 + normalized-content passes), then  **merged the same-topic docs under ~2 pages into single review files**  (21 merged files, 79 small docs consumed). Full audit trail: Jasper/tools/reports/ (audit_report.txt, near_dup_report.txt, deleted-manifest.txt) and the merge spec in Jasper/tools/scripts/merge_docs.py.
**Conventions**

*  .md = working source (mine); .docx = human-facing copy (yours), regenerable from the .md via Jasper/tools/scripts/batch_convert.py.
*  Merged files: ## section = one original document, unedited. Empty/duplicate sections dropped during cleanup (cleanup_merged.py).
*  (variant N) = a genuinely different version of the same asset (A/B material).
*  No hash suffixes.
```
marketing/
├── ads/                    paid campaigns (merged per network)
│   ├── google/             Google Ads Copy — Search, Display & Video (6 sections)
│   ├── meta/               Meta Ad Copy (2 sections)
│   ├── linkedin/           LinkedIn Ad Copy (2 sections)
│   ├── x/                  X Ad Copy (2 sections)
│   └── generic/            Paid Ad Copy — Ad Variations & Search (4 sections)
├── email/                  launch email program (merged per slot/sequence)
│   ├── sequences/          Email 1 Welcome (early draft) +
│   │                       Email Sequences 1-3 — Welcome, Upgrade, Urgency (4 sections)
│   ├── slot-2/             Email 2 — all variants (6 sections)
│   ├── slot-3/             Email 3 — all variants (7 sections)
│   └── slot-4/             Email 4 — all variants (3 sections)
├── messaging/              core brand copy (merged)
│   ├── TotalRecalls Launch Campaign (brief + abstract + full plan, 3 sections)
│   ├── Landing Page Copy — 3 variants
│   ├── Press & Announcement Copy (press release, launch pricing, blog, headlines)
│   ├── FAQ — Is TotalRecalls safe, Windows warning
│   └── founder/            Founder Story — Why I Built TotalRecalls (2 variants + profile)
├── strategy/               plans & checklists
│   ├── Master Implementation Plan
│   ├── Launch Marketing Plan (Revised) — 2 variants (merged)
│   ├── 60-Day Launch Content Calendar
│   ├── Launch Readiness Plan · Launch Marketing Organization · Launch Gap Checklist
│   └── Missing Items Checklist   (Jasper's own latest status tracker)
├── youtube/                channel & production
│   ├── scripts/            YT Video 1–10 scripts — ALL 10 complete (Video 6 = Final, 2026-09-29)
│   ├── hooks/              alternative hook docs (Jasper, 2026-09-29) — source
│   │                       .md; each merged into its script's "Alternative Hooks"
│   │                       section via merge_hooks.py (ALL 10 done, 2026-09-29)
│   ├── YouTube Content Plan — First 10 Videos · Channel Description
│   ├── YouTube Playlist Structure — 2 frameworks (merged)
│   ├── Upload Checklist & Template · Thumbnail Concepts
│   └── Main Explainer Video — Outline & Shot List (includes the Video Storyboard
│       Visuals/Audio summary table, restored from the raw dump)
├── social/                 organic launch-day posts (merged per platform)
│   ├── facebook/           Facebook Posts — all variants (5 sections)
│   ├── instagram/          Instagram Captions — all variants (4 sections)
│   ├── linkedin/           LinkedIn Posts — all variants (4 sections)
│   └── x/                  X (Twitter) Posts — all variants (5 sections)
├── website/                landing page & optimization
│   ├── Landing Page Copy — Hero & Trust (merged)
│   ├── Part 1 Page-by-Page Website Optimization Brief
│   └── Part 2 Homepage Rewrite
├── ops/                    Launch-Day Social Posting Checklist
├── meta/                   tracking docs
│   ├── TOPICS_AND_GAPS (2026-09-29 gap analysis).md   ← STATUS OF RECORD
│   └── REORGANIZATION (2026-09-28 canvas capture).md
├── raw_dumps/              unstructured exports kept for reference
│   ├── Conversation Jasper ai — Day2.md
│   └── Jasper Plan 1 (full canvas export).md
└── Jasper/                 tooling (not content)
    ├── tools/scripts/      convert.py, batch_convert.py, consolidate.py,
    │                       merge_docs.py, cleanup_merged.py, sha_audit.py, near_dup.py
    └── tools/reports/      audit reports, deleted-manifest.txt,
                            canvas_index_stale_pre_consolidation.
```
```
json,
                            coverage_check2.py, cluster_diff.py

```
**Counts (post-merge, 2026-09-29):**  53 .md / 49 .docx (21 of the .md are merged review files; the 4 extra .md without a .docx are meta/tracking docs and the README itself).
**Dedupe pass 2026-10-13**  (SHA256 + normalized-content scan of all 160 files): deleted 2 exact dups (Jasper/YouTube/Privacy Explainer Blog 4.md, Jasper/YouTube/TotalRecalls Blog Post 10.md — both duplicated Jasper/YouTube/Blog/ copies; newest kept) and 1 subset (email/Email Sequence (fragment).docx — strict subset of email/sequences/Email 1 Welcome — early draft.md). All three deleted 2026-10-13. No near-dups found. Trail: Jasper/tools/reports/deleted-manifest.txt.
**Post-09-29 growth (still topical, not merged):**  Jasper/YouTube/ now holds the operating plans (Master Plan V2 + V3, YouTube Implementation Plan, Content Audit Plan V2, Strategy, Description Templates, Hook Rankings Guide, Channel Style, Night Worklist, Blog/ 9+1 drafts, yt-api/) and Jasper/Social media/ holds the Day 0–29 social content calendar + 3 post-body fragments. The master compendium (root) embeds V3, V2, Strategy, and the Implementation Plan verbatim; the compendium is NOT updated for the Day 0–29 calendar. Canonical launch implementation plan: docs/LAUNCH-IMPLEMENTATION-PLAN-2026-10-13.md.

#### YT 10-Video Plan status (as of 2026-09-29)

| # | Script | Status |
| ------ | ------ | ------ |
| 1–5 | Videos 1, 2, 3 (V2), 4, 5 (V2) | ✅ complete |
| 6 | Trying to Get Your Old AI Conversations Back? | ✅  **Final**  (2026-09-29) + 3 alternative hooks merged in |
| 7–10 | Videos 7 (V3), 8 (V2), 9, 10 | ✅ complete |