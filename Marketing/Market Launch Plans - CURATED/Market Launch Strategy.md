# TotalRecalls — Market Launch Strategy (Unified Gen A–D Edition)

**Status:** Canonical Unified Operating Strategy (Synthesizing Generations A, B, C, and D from `Market Launch Plans - CURATED`)  
**Date:** November 15, 2026  
**Core Motto:** *"There is no pride of authorship. We're all working toward a common goal of excellence in our combined output."*  
**Companion Document:** `Market Launch Strategy Implementation Content.md`

---

## 1. Executive Summary & Generation Reconciliation

Over the past month, four successive planning generations (`Gen A` through `Gen D`) were developed across `Marketing/Market Launch Plans - CURATED`. While `Gen A–C` produced exceptional strategic depth—including the binding **Claims Register (§0.2)**, primary-source **Competitive Analysis**, **Cloudflare Traffic Baseline (with `TotalRecallsAudit` excluded)**, the **9-Post Blog Architecture**, the **Visual Style System**, and **Validation Gates**—the product itself leaped forward into **Generation D**:
1. **Official Microsoft Store Certification (`9PP1KKD5X2D6`):** Eliminates the #1 trial-conversion leak identified in `Gen C` (Windows SmartScreen / Smart App Control friction).
2. **Smart Search Engine (SSE) Add-On Shipped:** Turns what `Gen C` treated as a future roadmap item into an immediate `$29` add-on and `$49` **Pro + SSE Bundle** (doubling average order value while solving the *"thousands of files in folders is still a pile"* problem).
3. **8 Studio-Grade Narrated Provider Walkthroughs (`3440×1440 · CRF 10`):** Replaces the silent/placeholder `2026-10-01` cuts with full end-to-end recordings covering both **Downloader Pro** and the **SSE Add-On** across all 8 providers, plus live **Gemini direct in-app sign-in** (86 conversations exported in real time).

### The Single Strategic Idea
**Market the demonstrated workflow, not feature lists.**  
In a category crowded with browser extensions and SaaS subscriptions, recorded proof beats promises. Every video, blog post, community thread, and social asset demonstrates the exact same verifiable loop:
> **Install from the Microsoft Store (or portable ZIP) → Sign in to your AI providers locally inside the app → Download your conversations into `C:\TotalRecalls\Library\` as plain `.md` + `.json` files → Search across all 8 providers in plain English with the local Smart Search Engine (SSE).**

---

## 2. Verified Product Snapshot & Binding Claims Register (Updated to Gen D)

All public copy, scripts, blog posts, and community replies are strictly bound by this updated Claims Register (superseding the pre-Store/pre-SSE assumptions of `Gen A–C` while preserving `Gen C`'s strict truth-in-advertising guardrails).

### 2.1 Allowed & Verified Product Claims (Gen D Reality)

| Topic | Binding Wording / Verified Fact | Live Website Source |
| :--- | :--- | :--- |
| **What It Is** | A local Windows 10 & 11 (64-bit) desktop application that downloads your AI conversation history into plain Markdown (`.md`) and JSON (`.json`) files in a folder on your own PC. | `/`, `/faq/` |
| **Distribution & Packaging** | 1. **TotalRecalls Downloader (Free Tier & Pro):** Certified and distributed via the **Official Microsoft Store** (`https://apps.microsoft.com/detail/9PP1KKD5X2D6`, Package Family `34690AndreG.TotalRecalls`) — one-click install, zero security prompts, clean sandbox isolation, and automatic silent updates.<br>2. **Smart Search Engine (SSE) Add-On:** Standalone archive `TotalRecalls-Smart-Search-Engine-1.0.0.zip` (`0.78 MB`, SHA-256 `5811ed24f4d61ce58505e0a575f4a286a160445b789d09f100139fa8d44e9c22`) on `/download/`. Extract to any folder, run `run-smart-search.bat`, and activate with your `SSE-XXXXXXXX-XXXX-XXXX` key. Includes PDF & Markdown Quick-Start and Power User Guides. | `/download/`, `/release-notes/` |
| **8 Supported Providers** | ChatGPT (`OAI-001`), Claude (`ANT-002`), Perplexity (`PPL-003`), Gemini (`GEM-004`), Grok (`GRK-005`), DeepSeek (`DSK-006`, includes R1 thinking traces), Mistral (`MST-007`, Le Chat with UTF-8 fidelity), and Qwen Chat (`QWN-008`, `chat.qwen.ai` consumer app). | `/providers/`, `/see-it-work/` |
| **How Downloads Work** | You sign in to each provider locally inside the app's embedded Microsoft Edge WebView2 sign-in window on your own PC (and for Gemini, TotalRecalls also supports converting a Google Takeout folder). All 8 providers have verified live in-app walkthroughs on `/see-it-work/`. | `/see-it-work/`, `/providers/`, `/privacy/` |
| **Output Format & Scale** | One human-readable `.md` file and one machine-readable `.json` file per conversation, with dated filenames and UTF-8 throughout, organized in provider subfolders inside `C:\TotalRecalls\Library\` (or a folder you choose). Practically unlimited scale — downloads stream to disk (`50,000-message` archives work the same as `500-message` ones). | `/library/`, `/faq/` |
| **Attachments Rule** | Chat text, code blocks, and Perplexity/web citation references (e.g. `sources.json`) are preserved in Markdown/JSON; the binary attachment files themselves stay in your provider account. | `/faq/`, `/help/` |
| **Free Tier (`{FREE_LINE}`)** | **Resolved:** **"Free Tier covers ChatGPT, Claude, and Perplexity — 5 conversations per provider, no card, no account."** This is the official try-before-you-buy mechanism. | `/`, `/pricing/`, `/faq/`, `/download/` |
| **Downloader Pro Pricing** | **$24 USD one-time launch price** (regular $48 USD). No subscription. Sold via **Paddle** (merchant of record). Unlocks all 8 providers, unlimited downloads, up to 3 personal Windows PC activations (seat resets available via `support@totalrecalls.app`), and free maintenance updates (bug fixes & provider adapter updates) for the life of the product. | `/#pricing`, `/buy/`, `/release-notes/`, `/support/` |
| **Smart Search Engine (SSE)** | **$29 USD one-time launch price** (regular $58 USD). Requires Downloader Pro. Indexes your local Library on your PC (embedded local SQLite + LanceDB vector index) so you can search across all 8 providers by **meaning (vector)**, **keyword + meaning (hybrid)**, or **plain-English-to-SQL**, plus chat with your archive and connect to Obsidian/Notion. Runs on Windows 10/11 CPU (~8 GB RAM, ~2 GB disk, **no graphics card needed**). One-time internet connection downloads the search model at setup; works 100% offline thereafter. Automatically re-indexes after downloads and on a nightly schedule. | `/smart-search/`, `/faq/`, `/privacy/` |
| **Pro + SSE Bundle** | **$49 USD one-time launch price** (regular $98 USD). Best value: unlocks both Downloader Pro and Smart Search Engine (SSE) in one checkout. | `/#pricing`, `/smart-search/`, `/buy/` |
| **Refund Policy (Exact Split)** | • **Downloader Pro:** **No refund** — the Free Tier is our try-before-you-buy mechanism so you can test a real download on your own chats before paying. Statutory consumer rights (including Quebec online cancellation rights) are never excluded.<br>• **Smart Search Engine (SSE) Add-On:** **7 days, no questions asked** — email `support@totalrecalls.app` within 7 days of purchase for a full refund. | `/legals/#refund`, `/faq/` |
| **Privacy & Local State** | *"TotalRecalls never sees your chats."* Session files and license entitlements are stored locally on your PC, encrypted with **Windows DPAPI** (tied to your Windows user account). Zero app telemetry, zero background services, zero website cookies (uses cookieless Cloudflare Web Analytics). The **only** outbound call to `totalrecalls.app` is a best-effort license verification check sending only the license key (`TR-…` or `SSE-…`) + a pseudonymous salted machine hash to enforce the 3-PC seat limit (never revokes offline). Compliant by design with Quebec Law 25, PIPEDA, and GDPR. | `/privacy/`, `/legals/` |
| **Video Card Usage Rule** | • **V5 Logo Card (`v5_card.png` / `card420.mp4`):** Pure brand logo lockup (`TotalRecalls — AI CHAT RETRIEVER` on `#0B0E14` dark canvas). Used as the 3-second intro/outro stamp on general product and provider walkthrough videos.<br>• **V3 Schematic Card (`intro_card_v3.png` / `cta_card_v2.png` + `TotalRecalls-Search_Frame1..4.png`):** System architecture schematic (`8 Providers* > Unlimited Conversations > Unlimited Messages = 1 Unlimited Chat Searchable Local Folder` and the Pro Pyramid → Library Cylinder → SSE Container diagram). Used wherever the full Pro + SSE system workflow or Search Add-On architecture is explained. | Verified local video assets |

### 2.2 Strict "Never Say" Guardrails (Binding Across All Channels)
1. **Never use absolute security guarantees** like *"100% hack-proof"* or *"virus-free guarantee"*. State what the architecture actually does (*no TotalRecalls account, direct provider-to-PC download, Microsoft Store certified, verifiable via Wireshark/Resource Monitor*).
2. **Never claim exclusivity** (*"the only tool"*, *"the first tool"*). Competitors exist; win on **8-provider breadth + direct in-app sign-in + plain `.md`/`.json` files + offline CPU semantic search + one-time pricing**.
3. **Never claim binary images/attachments are downloaded.** State honestly that text, code, and citation references are saved while binary attachments stay in the provider account.
4. **Never quote spoken dollar prices inside video narration tracks.** Prices belong on pricing pages, video descriptions, and pinned comments so rendered videos remain evergreen when launch pricing changes.
5. **Never promise dates for macOS, Linux, or roadmap previews.**

---

## 3. Market Context, Competitive Landscape & Honest Qualification

### 3.1 Primary-Source Competitive Matrix

| Product | Type | Providers Covered | How It Gets Chats | Search & Retrieval | Pricing |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TotalRecalls (Pro + SSE)** | **Windows 10/11 Desktop App** (Microsoft Store + Portable ZIP) | **8** (ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral, Qwen) | **Direct in-app local sign-in** (plus Takeout import option for Gemini) | **Plain `.md` + `.json` files** (works with Explorer/Obsidian/VS Code) + **Optional SSE Add-On** (local vector, hybrid & NL-to-SQL search across all 8 providers) | **Free Tier** (3 providers, 5 chats each)<br>**$24** Pro one-time<br>**$29** SSE one-time<br>**$49** Pro + SSE Bundle |
| **AI Chat Importer** | Windows/Linux Desktop App + Web App | **4** (ChatGPT, Claude, DeepSeek, Grok) | User must manually request provider's official export ZIP, wait, then import ZIP | Local archive | **£29** (~$37 USD) one-time |
| **RecallBase** | Browser Extension | 8+ | Saves via active browser extension while chatting | Browser/extension export formats | Free tier (limits apply); Pro price unpublished |
| **Official Built-in Exports** | Vendor Web Settings | 1 per vendor (none for Grok, DeepSeek, Qwen) | Manual request → wait hours/days for email link → download raw ZIP | Machine-only JSON dumps; zero cross-provider search | Free (your data remains siloed) |

### 3.2 Defensible Differentiators
1. **8 Providers with Direct In-App Sign-In:** Covers the full modern multi-LLM stack (including Perplexity, Gemini, DeepSeek, Mistral, and Qwen) without forcing the user to request and wait for 8 separate ZIP dumps.
2. **Sovereign Plain Files (`.md` + `.json`):** Zero proprietary database lock-in for your conversations. If you uninstall TotalRecalls ten years from now, every `.md` file still opens in Notepad, Word, Obsidian, or VS Code.
3. **100% Local Semantic Search (SSE) Without a GPU:** Searches across all 8 provider folders simultaneously by meaning, keyword, or SQL on a standard Windows CPU.
4. **One-Time Price Ladder with a Real Free Tier:** Test on your own ChatGPT, Claude, and Perplexity chats before paying a cent.

### 3.3 Honest Qualification: "Who Should NOT Buy This"
Maintaining the candor established in `Master Launch Plan §4`:
> *If you only use one AI assistant and occasionally want a copy of a single conversation, your provider's built-in export or copy-paste is probably enough. TotalRecalls is built for people who rely on multiple AI tools for real work—code, research, writing, financial or personal analysis—and want their entire history saved as plain, searchable files on their own Windows PC.*

---

## 4. Target Audience, Unit Economics & Validation Funnel

### 4.1 Target Audience Segments
- **Primary Launch Focus:** Windows 10/11 power users who regularly use **two or more** AI assistants and treat their chats as reusable intellectual capital:
  1. **Developers & Software Architects:** Debug in ChatGPT, architect in Claude, reason in DeepSeek-R1; use VS Code, PowerShell, and Git.
  2. **Researchers, Consultants & Analysts (Finance/Legal/Medical):** Conduct cited reconnaissance in Perplexity, synthesize in Claude/Gemini; worry about client confidentiality, compliance trails, and losing months of research.
  3. **PKM & Local-First Enthusiasts (Obsidian / Notion / Data Hoarders):** Already organize their digital life in local Markdown vaults and refuse cloud SaaS lock-in.

### 4.2 Unit Economics & Revenue Ladder (Updated for Pro + SSE)

| Tier / Checkout Option | Launch Price | List Price | Est. Payment Fee (~3.5% + $0.30) | Est. Refund Allowance (3%) | Illustrative Net Receipts | Provisional Paid CAC Ceiling (~40%) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Downloader Pro** | **$24.00** | $48.00 | −$1.14 | −$0.72 | **~$22.14** | **≤ $9.00** |
| **SSE Add-On (Standalone)** | **$29.00** | $58.00 | −$1.32 | −$0.87 | **~$26.81** | **≤ $10.50** |
| **Pro + SSE Bundle (Featured)** | **$49.00** | $98.00 | −$2.02 | −$1.47 | **~$45.51** | **≤ $18.00** |

*Strategic Impact of Gen D:* The **$49 Pro + SSE Bundle** more than doubles net receipts per new customer (`$45.51` vs. `$22.14`), substantially increasing our margin of safety while giving the buyer an immediate, complete download-plus-search solution.

### 4.3 Privacy-Compatible Measurement & Cloudflare Baseline
- **Verified Pre-Launch Baseline (from `Master Launch Plan §11`, with `TotalRecallsAudit` excluded):**
  - ~1,489 visits and 1,612 pageviews per 7 days (~1,226 visits excluding Cloudflare-verified bots); ~6.6k visits / 7.0k pageviews over 30 days.
  - Top countries: **Canada (~37%)** and **United States (~33%)**—making optional **French (Québec)** social/ad tests (`Appendix A`) a zero-cost, high-relevance local lever for a Montreal-built product.
  - Top non-home paths: `/download/` (~63/wk), `/see-it-work/` (~50/wk), and the provider export guides (`/guides/*`).
- **Telemetry Rule:** Because TotalRecalls publicly promises **"no telemetry"**, never add in-app tracking beacons. Measure the funnel strictly through:
  1. **UTM-Tagged Site Visits & Guide Views** (excluding `TotalRecallsAudit` user-agents).
  2. **Microsoft Store Install Analytics + `/download/` ZIP Clicks.**
  3. **Voluntary First-Export Feedback & Support Logs.**
  4. **Checkout Conversions (`$24` Pro vs. `$49` Bundle vs. `$29` SSE Upgrade).**
- **Clean-Link Rule for Skeptical Communities:** On **Reddit** and **Hacker News (`Show HN`)**, readers distrust long `?utm_source=...` query strings. Use clean URLs (`https://totalrecalls.app` or the specific `/guides/[provider]/` URL) and attribute lifts by post timestamp; use full UTM parameters on YouTube, X, LinkedIn, Facebook, and Instagram bio links.

---

## 5. Multi-Channel Architecture & Closed Decisions

### 5.1 Finalized Cross-Channel Governance (from `Master Implementation Plan V3` + `Gen D`)
1. **Call-to-Action (CTA) Hierarchy:**
   - **Priority 1:** **Download Free** (`/download/` or Official Microsoft Store `9PP1KKD5X2D6`) — appears first on every video, guide, and post.
   - **Priority 2:** **Get the Pro + SSE Bundle ($49) / Downloader Pro ($24)** (`/#pricing` or `/smart-search/`).
   - **Priority 3:** **Get Product Updates (Email)** — sitewide footer only (`"real news only"`, zero popups or exit-intent modals).
2. **YouTube's Role — "The Public Evidence Library":**
   - Real screen recordings and calm, verifiable proof. No creator hype, no AI news chasing, no shocked-face thumbnails.
   - **Channel Visual Identity (`YouTube Channel Style v1`):**
     - **Obsidian** `#111315` backgrounds · **Graphite** `#1A1D21` panels · **Paper** `#F3EFE7` headlines · **Mist** `#D9D4CB` body · **Steel Blue** `#7A8FA6` mono evidence chips (`C:\TotalRecalls\Library\`, `.MD · .JSON`) · **Local Green** `#5E8A68` (`● SAVED LOCALLY`) · **Archive Amber** `#C88A2B` (maximum one highlight word on thumbnails; reserved on the website for primary CTAs).
3. **The 9-Post Blog Series (`/blog/` or `/guides/` Ownership Hub):**
   - **Option A Ruling Retained:** No repetitive provider spotlight blog posts (the 8 `/guides/[provider]/` and `/compare/[provider]/` pages already do that job).
   - The 9 blog posts cover **Explainers, Ownership, and Workflows** (`B1` Launch Announcement, `B2` Library Folder, `B3` Markdown vs. JSON, `B4` What "Not Sent to Our Servers" Means, `B5` Windows Backup / Robocopy, `B6` Windows Search + SSE Bridge, `B7` PowerShell Management, `B8` Obsidian Workflow, `B9` VS Code Workflow).
   - **Each Blog Post Doubles as a Video Script Source:** Every blog post pairs 1:1 with a YouTube Explainer/Workflow video so research is written once and deployed twice.
4. **The Founder Story Asset (`Andre Denis — 45+ Years in Investment Banking & VC`):**
   - One of the strongest differentiating assets in `06_Founder_Story/` and `Scripts/V2`. A seasoned investment banker and venture capitalist in Montreal who lost weeks of AI research, realized he had violated his own lifelong rule of *protecting your assets*, and built a local-first, zero-cloud, no-subscription tool. This narrative anchors the **About page**, **LinkedIn**, **Show HN**, **Product Hunt**, and **Video V2**.
5. **Community Guardrails:**
   - Always disclose founder status in the first line.
   - Focus Reddit activity on high-fit communities where users ask how to save or search hosted AI chats (`r/ChatGPT`, `r/ClaudeAI`, `r/perplexity_ai`, `r/DeepSeek`, `r/ObsidianMD`, `r/PKMS`, `r/DataHoarder`, `r/windows`). Per `Master Launch Plan §9`, avoid pitching hosted-chat archiving in `r/LocalLLaMA` unless specifically discussing the offline CPU embedding/SQL architecture of SSE.

---

## 6. The Integrated 90-Day Operating Spine (Focus on Weeks 1–4 + Gates at D14, D28, D56, D90)

### Phase P — Pre-Launch Readiness Verification (Day 0)
- [x] **Website & 8 Provider Demos Live:** `totalrecalls.app` live on Cloud Run + Cloudflare; 8 narrated `3440×1440` `CRF 10` walkthroughs (`Pro + SSE`) live on R2 (`demo-video.totalrecalls.app`).
- [x] **Free-Tier Wording Resolved:** Standardized everywhere to *"ChatGPT, Claude, and Perplexity, 5 conversations each"*.
- [x] **Microsoft Store Certified (`9PP1KKD5X2D6`):** Live and linked across the site, eliminating SmartScreen blockers for Store users (while retaining the honest SHA-256 / SmartScreen guide for portable ZIP users).
- [x] **`VideoObject` JSON-LD Schema:** Patched and verified across all 10 video pages (`/`, `/demo/`, `/see-it-work/`, and all 7 `/see-it-work/[provider]/` pages).
- [ ] **YouTube Channel Final Prep:** Verify phone in YouTube Studio (lifts upload cap & custom thumbnail API lock), delete the 9 superseded `2026-10-01` silent private cuts (keeping convergence animation `2Bl4wMzLUxk` as optional loop/trailer), re-crop the 10 thumbnails from `2292w` to the `3440w` masters, and publish the 8 narrated walkthroughs.

### Weeks 1–4 — The 4-Week Intensive Launch Window (Detailed in Companion Implementation Doc)

| Week | Core Focus | YouTube Long-Form | YouTube Shorts (3/wk) | Blog / Written Hub | Social & Community (X, LinkedIn, Reddit, FB/IG, FR-QC) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Week 1 (Days 1–7)** | **Launch & Core Proof (ChatGPT, Claude & The Founder Story)** | • **Publish:** ChatGPT (`6:03`) & Claude (`4:47`) Walkthroughs (or full 8-pack in *Start Here*)<br>• **Publish:** *Why I Built TotalRecalls* (Founder V2 / 8,135 Chats Flagship) | • **S1:** 8,135 chats on C:\<br>• **S2:** *I'll Wait* (`V6` 3-Click Dare)<br>• **S3:** *Rental Agreement* Hook (`V2`) | • **B1:** Launch Announcement<br>• **B2:** *Where TotalRecalls Saves Your Files* (Library Folder) | • Launch Runbook (LI → X → FB → IG)<br>• Reddit `r/ChatGPT` & `r/ClaudeAI` + `r/DataHoarder`<br>• Bilingual **Québec French** test (`L1-FR`, `FB1-FR`) |
| **Week 2 (Days 8–14)** | **Research, Reasoning & Local Privacy Proof (Perplexity, DeepSeek, Gemini)** | • **Publish:** Perplexity (`4:38`), DeepSeek (`4:46`), Gemini (`4:31`) Walkthroughs<br>• **Publish:** *Is TotalRecalls Safe? Resource Monitor & Wi-Fi Off Proof* (`V8` + `yt_wk2`) | • **S4:** *I Turned Off Wi-Fi. My Chats Are Still Here* (`V8`)<br>• **S5:** Perplexity threads + sources<br>• **S6:** 86 Gemini chats in real time | • **B3:** *Markdown vs. JSON: Which Saved File Should You Use?*<br>• **B4:** *What "Not Sent to Our Servers" Means* | • X/LI Research & Privacy Proof posts<br>• Reddit `r/perplexity_ai` & `r/DeepSeek`<br>• **D14 Gate Review** |
| **Week 3 (Days 15–21)** | **Smart Search Engine (SSE) & Launch Event (Grok + PH / Show HN)** | • **Publish:** Grok (`5:19`) Walkthrough<br>• **Publish:** *Thousands of Chats Is Still a Pile: Smart Search Engine (SSE) Deep Dive* (`yt_wk3` + `B6`) | • **S7:** Search 8 AIs by meaning, not keywords<br>• **S8:** Plain English to SQL counts<br>• **S9:** *The Endless Scroll ("Pack a Lunch")* | • **B5:** *How to Back Up Your Saved AI Chats on Windows*<br>• **B6:** *Searching Saved Chats (Windows Search + SSE)* | • **Product Hunt Launch (`PH1`)** or **Show HN (`HN1`)**<br>• X/LI SSE 3-Mode Breakdown & `$49` Bundle push<br>• Reddit `r/PKMS` |
| **Week 4 (Days 22–28)** | **Complete 8-Provider Ecosystem & PKM Workflows (Mistral, Qwen, Obsidian, VS Code)** | • **Publish:** Mistral (`4:23`) & Qwen Chat (`5:18`) Walkthroughs<br>• **Publish:** *Connect 8 AI Providers to Obsidian, VS Code & PowerShell* (`yt_wk4` + `B7/B8/B9`) | • **S10:** Point Obsidian at `C:\TotalRecalls\Library\`<br>• **S11:** *Sticky Note Backup System* (`V2` Hook 3)<br>• **S12:** Mistral & Qwen local export | • **B7:** *PowerShell Management*<br>• **B8:** *Opening Chats in Obsidian*<br>• **B9:** *Using Saved Chats in VS Code* | • X/LI Obsidian + Developer Workflow threads<br>• Reddit `r/ObsidianMD` & `r/SideProject`<br>• **D28 Gate Review** |

### Weeks 5–12 — Post-Launch Expansion, Urgency & Paid Testing Gates
- **Day 14 Gate (Funnel Validation):** Confirm clean install-to-first-export flow, zero licensing bottlenecks, and initial Free → Pro/Bundle conversions. If drop-off appears, fix the page/guide before scaling.
- **Day 28 Gate (Scale Readiness):** Review cumulative Microsoft Store + ZIP downloads, YouTube CTR, Free → Paid conversion rate, and refund rate (`< 5%`).
- **Day 42 Launch-Price Urgency Window (if discount expiry `D6` is set for Day 60):** Publish *"Launch Pricing Ends Soon"* update and send Email Sequence 3 to non-upgraded Free Tier subscribers.
- **Day 56 Gate (Week-8 Metrics & Paid Go/No-Go Rule):** Per `Master Launch Plan §7.1 (U4)`, paid amplification (`$5–$10/day` YouTube in-feed promotion of the hero walkthrough) proceeds **only if** observed `Free → Pro/Bundle conversion ≥ 8%` AND `YouTube CTR ≥ 3%`, with an immediate hard stop if `CAC` exceeds the provisional ceiling (`$9` Pro / `$18` Bundle).
- **Day 90 Quarterly Review:** Evaluate total unit economics, support load (`tickets per 100 downloads`), and demand signals (`contact@totalrecalls.app`) for **Portable RAG Containers** and **macOS/Linux**.
