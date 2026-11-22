# TotalRecalls Canonical Knowledge Base Manifest

This container defines the authoritative ground-truth sources used by the TotalRecalls Social Media Reply Bot to synthesize accurate technical, architectural, and user-facing answers.

---

## 1. Primary Knowledge Base Sources

### A. Technical & Power User Specifications
- **SSE Power User Manual:** `C:\Users\break\Projects\TotalRecalls-Source Code\docs\TOTALRECALLS_POWER_USER_MANUAL.md`
  - Covers: SQLite FTS5 configuration, LanceDB vector indexing (all-MiniLM-L6-v2), Natural Language to SQL generation, schema structure, performance tuning, and offline CPU constraints.
- **SSE Quick Start Guide:** `C:\Users\break\Projects\TotalRecalls-Source Code\docs\TOTALRECALLS_SSE_QUICK_START_GUIDE.md`
  - Covers: First-run indexing, folder mapping, query syntax, search filters (provider, date, keyword, semantic similarity).
- **SSE Layman Guide:** `C:\Users\break\Projects\TotalRecalls-Source Code\docs\TOTALRECALLS_SSE_LAYMAN_GUIDE.md`
  - Covers: Plain English explanations for non-technical users, benefits of local search vs cloud search.

### B. Live Website Copy & FAQ (Single Source of Truth)
- **Features & Architecture:** `C:\Users\break\Projects\TotalRecalls-Source Code\site\src\pages\features\index.astro`
- **Pricing & Tier Structure:** `C:\Users\break\Projects\TotalRecalls-Source Code\site\src\pages\pricing\index.astro`
- **FAQ & Objection Handling:** `C:\Users\break\Projects\TotalRecalls-Source Code\site\src\pages\faq\index.astro`
- **Local Storage / Library Schema:** `C:\Users\break\Projects\TotalRecalls-Source Code\site\src\pages\library\index.astro`
- **SSE Product Overview:** `C:\Users\break\Projects\TotalRecalls-Source Code\site\src\pages\sse\index.astro`

### C. Live Application Source Code (Verification & Engine Details)
- **Core Downloader Adapters (8 Providers):** `C:\Users\break\Projects\TotalRecalls-Source Code\adapters\`
  - Implements: WebView2 session extraction, direct provider API sync, local `.md` and `.json` file generation.
- **Smart Search Engine Core:** `C:\Users\break\Projects\TotalRecalls-Source Code\Modules\smart-search-engine\`
  - Implements: Local embedding generation, LanceDB vector table, SQLite full-text search, and NL-to-SQL translation engine.
- **Security & Storage Engine:** Windows DPAPI encryption routines (tied to current Windows user SID, never stored in plaintext, zero external transmission).

---

## 2. Inviolable Response Rules (The Claims Register)

When answering questions on behalf of TotalRecalls, the bot MUST strictly observe:
1. **Never claim image or attachment downloads:** The app currently extracts text, markdown, code blocks, citations, and conversation metadata. It does NOT download binary images, files, or attachments.
2. **Never claim 100% hack-proof or absolute guarantees:** Use precise terms: *"Session tokens and license keys are encrypted at rest on your local disk using Windows Data Protection API (DPAPI) and never leave your PC."*
3. **No Cloud Middleman / Zero Telemetry:** The app has no proxy server, no telemetry SDKs, and no tracking pixels. Traffic goes directly from your machine to the provider. Wireshark or Resource Monitor verification is welcomed.
4. **Accurate Pricing:**
   - **Free Tier:** Permanent, no card required, covers ChatGPT, Claude, and Perplexity (5 conversations each).
   - **Downloader Pro:** $24 one-time launch price (all 8 providers, unlimited exports, lifetime license for current major version). No refund policy (try before you buy via Free Tier; statutory consumer rights preserved).
   - **Smart Search Engine (SSE):** $29 one-time launch price (7-day no-questions-asked refund policy via `support@totalrecalls.app`).
   - **Pro + SSE Bundle:** $49 one-time.
5. **Platform Requirements:** Windows 10 (version 19041+) and Windows 11 on x64 / ARM64 (via emulation). No dedicated GPU required; runs on standard CPUs with 8GB RAM.
6. **Disclosure:** On Reddit and community forums, always open with: *"Founder here / Developer of TotalRecalls here."*
