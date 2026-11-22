# TotalRecalls — Week 1 Launch Execution Pack (Ready to Publish)

This execution pack is prepared for immediate deployment across **X (Twitter)**, **LinkedIn**, and **Reddit** (`r/DataHoarder`, `r/ChatGPT`, `r/ClaudeAI`). All links point to the live website, the Microsoft Store, and the newly deployed public YouTube walkthroughs.

---

## 1. X (Twitter) — Pinned Launch Thread (5 Tweets)

**Posting Schedule:** Post during morning peak hours (09:00–10:00 EST).  
**Media:** Attach the 60-second clip from `TR_website_chatgpt_pro_sse.mp4` (or `tr_thumb_chatgpt.jpg` as a fallback image) to Tweet 1.

### Tweet 1 (Main Post / Hook)
Over the last 2 years, I accumulated 8,135 conversations across ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral & Qwen.

None of those browser tabs are actually yours. One billing glitch, UI redesign, or account lock and years of thinking vanish.

So I built TotalRecalls for Windows. 🧵👇

*(Attach video or image: `tr_thumb_chatgpt.jpg`)*

---

### Tweet 2 (The Dual-Format Local Library)
TotalRecalls downloads your history from all 8 major AI providers into one clean local folder on your PC (`C:\TotalRecalls\Library\`).

Every conversation is saved twice:
• `.md` — clean Markdown that opens in Obsidian, Notion, Word, or Notepad in 20 years
• `.json` — full structured data for scripts & local tooling

---

### Tweet 3 (Local Smart Search Engine — SSE)
What happens when you have thousands of local files and can't remember if you solved a bug in Claude, ChatGPT, or DeepSeek?

We built the Smart Search Engine (SSE) add-on:
• Query all 8 providers at once in plain English
• Search by meaning (vector), exact keyword (hybrid), or SQL
• Runs 100% offline on CPU (no GPU required)

---

### Tweet 4 (Zero-Cloud Privacy & Anti-Subscription)
Four rules we refuse to break:
1. Zero servers & zero telemetry. Sessions stay encrypted locally with Windows DPAPI.
2. Direct provider-to-PC download (verify it in Wireshark!).
3. Official Microsoft Store certified (zero security warnings).
4. One-time purchase ($24 Pro / $49 Pro + SSE Bundle). No recurring monthly rent.

---

### Tweet 5 (Call to Action & Links)
There is a permanent Free Tier available right now (ChatGPT, Claude, and Perplexity — 5 conversations per provider) so you can test it on your real chats before paying a cent.

• Try the Free Tier: https://totalrecalls.app/download/?utm_source=x&utm_medium=social&utm_campaign=launch&utm_content=x1
• Get from Microsoft Store: https://apps.microsoft.com/detail/9PP1KKD5X2D6
• Full 6-min walkthrough: https://www.youtube.com/watch?v=fQBNazsL-VE

---

## 2. LinkedIn — Founder Launch Post

**Target Profile:** Personal profile (`Andre Denis`)  
**Recommended Timing:** Tuesday, 08:45–09:30 EST  
**Media:** Attach `C:\Users\break\demo-shoot\vectorsql-video\build\intro_card_v3.png` or `site/public/og-image.png`.

### Post Copy:
Over the last two years, I had 8,135 conversations across ChatGPT, Claude, Perplexity, Gemini, and four other AI assistants.

I spent more than 45 years in financial services, most of it as an investment banker and venture capitalist. The primary lesson from that career was simple: protect your assets.

Yet recently, I caught myself violating my own rule. 

A multi-week research project I had built inside an AI assistant vanished overnight. Whether it was an expired session or an interface update, weeks of refined thinking were gone. There was no backup, no undo button, and no support line.

AI is no longer a novelty chatbot. It has quietly become our external working memory—holding software architecture decisions, financial models, market research, and strategic drafts. 

Yet almost all of that intellectual capital sits inside rented browser tabs—scattered across eight disconnected corporate silos with zero unified backup.

So in retirement, I built **TotalRecalls** for Windows 10 & 11 (now certified and available directly on the Official Microsoft Store).

TotalRecalls connects locally on your PC to the top 8 AI providers—ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral, and Qwen Chat—and saves each conversation as both a readable Markdown (`.md`) file and a structured JSON (`.json`) file in a local folder you control.

Three principles guide the software:

1. **Local-First & Zero Telemetry:** There is no TotalRecalls account, no cloud middleman, and no telemetry. Session tokens are encrypted on your PC via Windows DPAPI. Your conversations go straight from the provider to your drive. You can verify this in Wireshark or Resource Monitor.
2. **Smart Search Engine (SSE):** Because thousands of files in folders is still a pile, our optional local search engine lets you query all 8 providers simultaneously in plain English—by semantic meaning, keyword, or natural-language-to-SQL—running 100% locally on CPU without needing a dedicated graphics card.
3. **No Subscription:** You shouldn't pay monthly rent to keep access to your own thoughts. TotalRecalls is a one-time purchase ($24 USD for Pro, or $49 for the Pro + SSE Bundle). 

A Free Tier is available right now covering ChatGPT, Claude, and Perplexity (5 conversations per provider) so you can verify the output on your own chats before spending anything.

• Try it free on Windows: https://totalrecalls.app/?utm_source=linkedin&utm_medium=social&utm_campaign=launch&utm_content=l1
• Microsoft Store listing: https://apps.microsoft.com/detail/9PP1KKD5X2D6
• Full walkthrough video: https://www.youtube.com/watch?v=fQBNazsL-VE

If you rely on AI for your daily work: where does your conversation history live today?

#AI #Productivity #KnowledgeManagement #DataOwnership #Windows11 #CyberSecurity #IndieHacker

---

## 3. Reddit Post 1: `r/DataHoarder`

**Subreddit:** `r/DataHoarder`  
**Posting Rule:** Clean URL only (no UTM parameters). Disclose maker status immediately. Lead with data format, local storage specs, and offline search architecture.  
**Title:** I archived 8,135 AI conversations across 8 providers (ChatGPT, Claude, Perplexity, Gemini, DeepSeek, Grok, Mistral, Qwen) into a local Markdown + JSON folder on Windows

### Body Copy:
Hi r/DataHoarder,

Founder here. Over the past two years, my AI chat history became my primary external technical notebook—containing database schemas, architecture notes, financial models, and research threads. 

Having that data trapped across eight different browser tabs bothered me:
1. Official export tools either don't exist (DeepSeek, Grok, Qwen), or require waiting days for an email link containing an unreadable monolithic JSON dump.
2. Sidebar histories quietly get pruned or broken whenever a provider pushes a frontend update.
3. You cannot run a single grep or local semantic search across all eight providers at once.

I built a Windows 10/11 desktop utility called **TotalRecalls** (certified on the Microsoft Store) to pull conversations from all 8 providers into one local directory (`C:\TotalRecalls\Library\<provider>\`).

**Technical & Archival Specs:**
- **Dual Format Output:** Every conversation is written as a clean, human-readable `.md` file (preserving formatting, code blocks, timestamps, and citation links) paired with a structured `.json` file for scripting.
- **Local Authentication & Zero Telemetry:** There is no TotalRecalls account and no middleman proxy server. The app opens an embedded Microsoft Edge WebView2 window on your machine where you authenticate directly with the provider. Session files and license records are encrypted at rest using Windows DPAPI (tied to your Windows user account). Traffic flows solely between your PC and the provider.
- **Offline Vector + Hybrid + SQL Search (SSE Add-On):** Because 8,000 Markdown files is still a pile, we built an offline Smart Search Engine (SSE) add-on that indexes the local library into embedded SQLite + LanceDB. It runs completely offline on standard CPUs (~8GB RAM, no GPU required) and supports vector similarity, exact keyword hybrid search, and natural-language-to-SQL.
- **Pricing:** Permanent Free Tier covering ChatGPT, Claude, and Perplexity (5 conversations each) so you can test the export on your own chats. Pro is a one-time $24 purchase (no subscription).

Format specs & walkthrough videos: https://totalrecalls.app/library/  
Official Microsoft Store: https://apps.microsoft.com/detail/9PP1KKD5X2D6

Happy to answer any questions about the WebView2 session extraction, DPAPI encryption, or local vector indexing.

---

## 4. Reddit Post 2: `r/ChatGPT` & `r/ClaudeAI`

**Subreddit:** `r/ChatGPT` or `r/ClaudeAI`  
**Title:** How I export my AI conversations to local Markdown files on Windows (instead of wrestling with official bulk JSON exports)

### Body Copy:
Quick disclosure: I'm the developer behind TotalRecalls.

If you use ChatGPT or Claude heavily for coding, writing, or research, relying on the browser sidebar has two big friction points:
1. If an account gets suspended or the provider changes their sidebar UI, older threads become nearly impossible to reach.
2. The official account export makes you wait for an email link and gives you an enormous, monolithic JSON file that no text editor or note-taking app can display cleanly.

I built a Microsoft Store-certified Windows app called **TotalRecalls** that connects locally on your PC and downloads your conversations directly into a local folder (`C:\TotalRecalls\Library\`) as individual Markdown (`.md`) and JSON (`.json`) files.

**Key details:**
- **100% Local:** Runs on your PC with zero servers in between and zero telemetry (verify it via Wireshark or Resource Monitor).
- **Obsidian / Notepad / Word Ready:** The `.md` files open immediately in any text editor without needing conversion scripts.
- **Cross-Provider Search:** If you also use Perplexity, Claude, DeepSeek, or Gemini, our local search add-on lets you search across all your saved conversations in plain English.
- **Free Tier:** You can test it on your own history for free (covers ChatGPT, Claude, and Perplexity — 5 conversations per provider).

Walkthrough video & guide: https://totalrecalls.app/see-it-work/  
Microsoft Store link: https://apps.microsoft.com/detail/9PP1KKD5X2D6

---

## 5. Media Assets Attached & Ready to Use

All referenced media files exist locally and are ready for upload alongside the copy:
- **`tr_thumb_chatgpt.jpg`** (`1280×720` sharp preview): `C:\Users\break\Projects\TotalRecalls-Source Code\Marketing\Market Launch Plans - CURATED\07_Assets\thumbnails_3440\tr_thumb_chatgpt.jpg`
- **`intro_card_v3.png`** (`3440×1440` system schematic): `C:\Users\break\demo-shoot\vectorsql-video\build\intro_card_v3.png`
- **`og-image.png`** (`1200×630` social card): `C:\Users\break\Projects\TotalRecalls-Source Code\site\public\og-image.png`
- **`v5_card.png`** (`TotalRecalls Logo Card`): `C:\Users\break\demo-shoot\qc\head\v5_card.png`
