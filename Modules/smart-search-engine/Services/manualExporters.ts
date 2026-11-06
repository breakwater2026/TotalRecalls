// Manual export utility providing downloadable Markdown (.md) and Microsoft Word (.docx/.doc) formats.
// Formats are generated client-side with zero external telemetry or server dependencies.

export const POWER_USER_MANUAL_MARKDOWN = `# TOTALRECALLS POWER USER MANUAL
## Smart Search Engine (SSE): Vector Search, Relational RAG SQL, Consensus Auditing & Local-Only Privacy Architecture
**Product Edition:** v2.5.0-MarketLeader  
**Vendor:** TotalRecalls (totalrecalls.app)  
**Distribution Target:** Senior Software Engineers, Data Architects, Security Auditors & Enterprise Teams  

---

## 1. Executive Summary & Dual-Unit Architecture

The TotalRecalls suite is architected around two decoupled, complimentary units:

\`\`\`
+-----------------------------------------------------------------------------------------+
| TOTALRECALLS PRODUCT ECOSYSTEM (totalrecalls.app)                                       |
+-----------------------------------------------------------------------------------------+
|                                                                                         |
|   +--------------------------------------+   +--------------------------------------+   |
|   | UNIT 1: TOTALRECALLS PRO             |   | UNIT 2: SMART SEARCH ENGINE ADD-ON   |   |
|   | $24 launch / $48 regular (one-time)  |   | $29 launch / $58 regular (one-time)  |   |
|   +--------------------------------------+   +--------------------------------------+   |
|   | * Scrapers: ChatGPT, Claude,         |   | * HNSW vector search                 |   |
|   |   Perplexity, Gemini, Grok,          |   | * Reciprocal Rank Fusion (BM25+Vec)  |   |
|   |   DeepSeek, Mistral, Qwen            |   | * Natural Language to SQLite         |   |
|   | * Formats: JSON, Markdown, PDF       |   | * Cross-AI Consensus Auditor         |   |
|   | * Local encrypted vault (AES-256)    |   | * PII & Secret Scrubber              |   |
|   | * Keyword full-text indexing         |   | * Fine-Tuning JSONL Export           |   |
|   | * Incremental background sync        |   | * Free updates (bug fixes) to SSE    |   |
|   +--------------------------------------+   +--------------------------------------+   |
|                       |                                          |                      |
|                       +------------------------------------------+                      |
|                                            |                                            |
|                                            v                                            |
|                      +-------------------------------------------+                      |
|                      | PRIVATE LOCAL DISK RUNTIME                |                      |
|                      | (Nothing you write or save is uploaded    |                      |
|                      |  • AES-256 SQLite • Local Models)         |                      |
|                      +-------------------------------------------+                      |
+-----------------------------------------------------------------------------------------+
\`\`\`

---

## 2. Commercial Packaging & Pricing

TotalRecalls is a one-time purchase with no subscription. There are three prices:

| Product | Launch price | Regular price | Notes |
|---|---|---|---|
| TotalRecalls Pro (downloader) | $24 | $48 | One-time. All 8 providers, unlimited downloads. |
| Smart Search Engine (SSE) add-on | $29 | $58 | One-time. Requires Pro. |
| Pro + SSE bundle | $49.89 | $99.89 | One-time. Best value, one checkout. |

- **Updates vs upgrades:** updates (bug fixes, provider-compatibility fixes) are free. Upgrades (new features, new add-ons) are paid. SSE buyers get free updates to SSE; new modules and upgrades are separate purchases.
- **Refunds:** the Smart Search Engine add-on has a 7-day refund, no questions asked. TotalRecalls Pro has no standard refund — the Free Tier is the try-before-you-buy mechanism.

---

## 3. Relational Schema Architecture (SQLite)

\`\`\`sql
CREATE TABLE conversations (
    id VARCHAR(64) PRIMARY KEY,
    provider VARCHAR(32) NOT NULL,
    model VARCHAR(64) NOT NULL,
    title TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    total_tokens INTEGER DEFAULT 0,
    message_count INTEGER DEFAULT 0,
    tags TEXT
);

CREATE TABLE messages (
    id VARCHAR(64) PRIMARY KEY,
    conversation_id VARCHAR(64) NOT NULL,
    role VARCHAR(16) NOT NULL,
    content TEXT NOT NULL,
    token_count INTEGER DEFAULT 0,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
);

CREATE VIRTUAL TABLE chat_chunks USING vec0(
    chunk_id TEXT PRIMARY KEY,
    conversation_id TEXT,
    embedding float[768] distance_metric=cosine
);
\`\`\`

---

## 4. Hybrid Reciprocal Rank Fusion (RRF) Retrieval

Combines BM25 token scores with dense vector cosine similarity:

$$RRF\\_Score(d) = \\sum_{m \\in M} \\frac{1}{k + \\text{rank}_m(d)}$$

Where $k = 60$. Dense retrieval pulls conceptual neighbors while BM25 guarantees precision on exact code variables and UUIDs.

---

## 5. Privacy & Local-Only Operation

TotalRecalls runs on your PC. Nothing you write or save is uploaded. The only internet use is a one-time search-model download at setup; after that search works without a connection.

You can verify local-only operation yourself — e.g. with Wireshark:

\`\`\`bash
# Capture loopback and physical interface traffic
tshark -i any -f "not port 53 and not arp" -Y "http or tls"
\`\`\`

No chat content is transmitted off your machine during search, SQL querying, or dataset export.

---
*TotalRecalls Engineering Manual • totalrecalls.app*
`;

export const LAYMAN_USER_MANUAL_MARKDOWN = `# TOTALRECALLS EVERYDAY USER MANUAL
## Simple, Step-by-Step Guide for Non-Technical Users
**Software Edition:** v2.5.0  
**Vendor:** TotalRecalls (totalrecalls.app)  

---

## Welcome to TotalRecalls!

Think of TotalRecalls as your **personal digital safe and super-smart librarian** for all your AI conversations.

If you use ChatGPT, Claude, or Gemini for work, cooking recipes, travel plans, or studying, you know how frustrating it is to lose an amazing answer in your chat history. TotalRecalls solves this forever.

---

## The Two Parts of TotalRecalls

1. **TotalRecalls Pro ($24 at launch, regular $48):** Quietly saves a private copy of all your conversations from ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral, and Qwen directly onto your computer's hard drive.
2. **Smart Search Engine add-on ($29 at launch, regular $58):** Lets you ask questions across *all* your saved chats at once. It answers in seconds and tells you exactly which AI gave the answer!

---

## The Smart Search Engine — What Ships When

Smart Search Engine launches today with plain-English search across your whole archive. The PII Scrubber, Fine-Tuning Pipeline, Consensus Auditor, Knowledge Graph cards, and Embedding Benchmark follow as paid upgrades for Smart Search Engine buyers (separate purchases).

**Pricing (one-time, launch prices):**
- TotalRecalls Pro: **$24** (regular $48) — all 8 providers, unlimited downloads.
- Smart Search Engine: **$29** (regular $58) — requires Pro.
- Pro + SSE bundle: **$49.89** (regular $99.89).

**Updates vs upgrades:** updates (bug fixes, provider-compatibility fixes) are free. Upgrades (new features, new add-ons) are paid. SSE buyers get free updates to SSE; new modules and upgrades are separate purchases.

**Refunds:** the Smart Search Engine add-on has a 7-day refund, no questions asked. TotalRecalls Pro has no standard refund — the Free Tier is the try-before-you-buy mechanism.

---

## How to Search in Plain English

1. Click on the **Search Chat** tab.
2. Type your question naturally, like: *"What recipe did Claude give me for gluten-free pasta?"*
3. Read the instant answer. Click on the cited chat card to open the full conversation.

---

## Our Privacy Promise

TotalRecalls runs on your PC. Nothing you write or save is uploaded. The only internet use is a one-time search-model download at setup. After that, search works without a connection.

---
*TotalRecalls Everyday User Guide • totalrecalls.app*
`;

export const downloadManualMarkdown = (isLayman: boolean = false): void => {
  const content = isLayman ? LAYMAN_USER_MANUAL_MARKDOWN : POWER_USER_MANUAL_MARKDOWN;
  const filename = isLayman ? 'TOTALRECALLS_USER_MANUAL_LAYMAN.md' : 'TOTALRECALLS_POWER_USER_MANUAL.md';
  
  const blob = new Blob([content], { type: 'text/markdown;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
};

export const downloadManualWordDocx = (isLayman: boolean = false): void => {
  const markdown = isLayman ? LAYMAN_USER_MANUAL_MARKDOWN : POWER_USER_MANUAL_MARKDOWN;
  const title = isLayman 
    ? 'TotalRecalls User Manual - Everyday Edition' 
    : 'TotalRecalls Power User Technical Manual - Smart Search Engine';
  const filename = isLayman ? 'TOTALRECALLS_USER_MANUAL_LAYMAN.doc' : 'TOTALRECALLS_POWER_USER_MANUAL.doc';

  // Format as clean HTML document with Word XML envelope
  const htmlContent = `
<html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:w='urn:schemas-microsoft-com:office:word' xmlns='http://www.w3.org/TR/REC-html40'>
<head>
  <meta charset="utf-8">
  <title>${title}</title>
  <style>
    body {
      font-family: 'Segoe UI', Calibri, Arial, sans-serif;
      font-size: 11pt;
      line-height: 1.5;
      color: #1e293b;
      margin: 40px;
    }
    h1 {
      color: #0891b2;
      font-size: 20pt;
      border-bottom: 2px solid #0891b2;
      padding-bottom: 6px;
      margin-top: 24px;
    }
    h2 {
      color: #0f766e;
      font-size: 15pt;
      margin-top: 20px;
    }
    h3 {
      color: #155e75;
      font-size: 12pt;
      margin-top: 14px;
    }
    p {
      margin-bottom: 10pt;
    }
    table {
      border-collapse: collapse;
      width: 100%;
      margin: 16px 0;
      font-size: 10pt;
    }
    th, td {
      border: 1px solid #cbd5e1;
      padding: 8px 12px;
      text-align: left;
    }
    th {
      background-color: #f1f5f9;
      color: #0f172a;
      font-weight: bold;
    }
    pre {
      background-color: #f8fafc;
      border: 1px solid #e2e8f0;
      padding: 12px;
      font-family: Consolas, 'Courier New', monospace;
      font-size: 9.5pt;
      border-radius: 6px;
      overflow-x: auto;
    }
    code {
      font-family: Consolas, 'Courier New', monospace;
      background-color: #f1f5f9;
      padding: 2px 4px;
      border-radius: 4px;
      font-size: 9.5pt;
    }
    .badge {
      display: inline-block;
      padding: 3px 8px;
      background-color: #06b6d4;
      color: #ffffff;
      font-weight: bold;
      border-radius: 4px;
      font-size: 9pt;
    }
  </style>
</head>
<body>
  <div style="text-align: center; margin-bottom: 30px;">
    <h1 style="border: none; margin-bottom: 4px;">TotalRecalls Documentation Suite</h1>
    <p style="color: #64748b; font-size: 10pt;">Local AI Chat Downloader, Vector Search & RAG SQL • totalrecalls.app</p>
  </div>
  ${markdownToHtml(markdown)}
</body>
</html>
  `;

  const blob = new Blob([htmlContent], { type: 'application/msword;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
};

function markdownToHtml(md: string): string {
  let html = md
    .replace(/^### (.*$)/gim, '<h3>$1</h3>')
    .replace(/^## (.*$)/gim, '<h2>$1</h2>')
    .replace(/^# (.*$)/gim, '<h1>$1</h1>')
    .replace(/\*\*(.*?)\*\*/gim, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/gim, '<em>$1</em>')
    .replace(/`([^`]+)`/gim, '<code>$1</code>')
    .replace(/```([\s\S]*?)```/gim, '<pre><code>$1</code></pre>')
    .replace(/\n\n/gim, '<p></p>')
    .replace(/\n/gim, '<br />');

  return html;
}

// Named alias for convenience across packaging studio and other components
export const downloadManualDocx = downloadManualWordDocx;

