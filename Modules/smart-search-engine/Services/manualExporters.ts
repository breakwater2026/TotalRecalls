// Manual export utility providing downloadable Markdown (.md) and Microsoft Word (.docx/.doc) formats.
// Formats are generated client-side with zero external telemetry or server dependencies.

export const POWER_USER_MANUAL_MARKDOWN = `# TOTALRECALLS POWER USER MANUAL
## Smart Search Engine (SSE): Vector Search, Relational RAG SQL, Consensus Auditing & Air-Gap Privacy Architecture
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
|   +---------------------------------------+   +-------------------------------------+   |
|   | UNIT 1: THE CORE CHAT DOWNLOADER      |   | UNIT 2: THE SMART SEARCH ENGINE     |   |
|   | (Baseline Foundation - $29 Lifetime)  |   | (6-Week Staged Drops / $49-$59 Pass)|   |
|   +---------------------------------------+   +-------------------------------------+   |
|   | * Web LLM scrapers (ChatGPT, Claude,  |   | * Sub-millisecond HNSW Vector Search|   |
|   |   Gemini, Perplexity, Mistral, Grok)  |   | * Reciprocal Rank Fusion (BM25+Vec) |   |
|   | * Formats: JSON, Markdown, HTML, PDF  |   | * Natural Language to SQLite Engine |   |
|   | * Local disk encrypted vault (AES-256)|   | * Cross-AI Consensus Auditor        |   |
|   | * Keyword full-text indexing          |   | * Air-Gap PII & Secret Scrubber     |   |
|   | * Incremental background sync         |   | * 1-Click Fine-Tuning JSONL Export  |   |
|   +---------------------------------------+   +-------------------------------------+   |
|                      |                                           |                      |
|                      +---------------------+---------------------+                      |
|                                            |                                            |
|                                            v                                            |
|                  +----------------------------------------------------+                 |
|                  | 100% PRIVATE, AIR-GAPPED LOCAL DISK RUNTIME        |                 |
|                  | (Zero Cloud Egress • AES-256 SQLite • Local Models)|                 |
|                  +----------------------------------------------------+                 |
+-----------------------------------------------------------------------------------------+
\`\`\`

---

## 2. Commercial Packaging & The 6-Week Staged Drop Model

To ensure sustained innovation and accessible modular adoption, the Smart Search Engine utilizes a staged 6-week drop schedule:

| Drop | Week | Module Title | Standalone Price | Status | Description |
|---|---|---|---|---|---|
| Launch | Week 1 | Tri-Mode Search Chat (Vector + NL→SQL + RRF) | $39 | **LIVE** | Sub-millisecond conversational retrieval across all models |
| Drop 1 | Week 2 | Air-Gap PII & Secret Redaction Scrubber | $19 | Next Up | Automated credential and API key sanitization |
| Drop 2 | Week 3 | 1-Click Fine-Tuning Pipeline (JSONL/Alpaca) | $19 | Planned | OpenAI JSONL, ShareGPT, and Alpaca dataset generation |
| Drop 3 | Week 4 | Cross-AI Consensus & Hallucination Auditor | $25 | Planned | Peer-review board comparing model disagreements |
| Drop 4 | Week 5 | Vault Knowledge Graph & Latent Topic Cards | $19 | Planned | Autonomous entity clustering and taxonomy cards |
| Drop 5 | Week 6 | Embedding Engine Benchmark & 2D PCA Cluster Map | $19 | Planned | Hardware latency, RAM profiler, and 2D vector map |

- **Sum of Parts Standalone Value:** **$140**
- **Founder's Season Pass (Launch Week Special):** **$49** *(Standard Bundle: $59 | Post-Rollout: $79)*
- **Core Downloader:** **$29** *(One-time lifetime baseline)*
- **Enterprise Local Fleet:** **$149/seat perpetual** *(All modules unlocked immediately)*

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

## 5. Air-Gap & Zero-Egress Verification

Verify zero outbound telemetry with Wireshark:

\`\`\`bash
# Capture loopback and physical interface traffic
tshark -i any -f "not port 53 and not arp" -Y "http or tls"
\`\`\`

During vector search, SQL querying, and dataset fine-tuning export, **0 packets are transmitted**.

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

1. **The Downloader ($29 Lifetime):** Quietly saves a private copy of all your conversations from ChatGPT, Claude, Gemini, Perplexity, and Mistral directly onto your computer's hard drive.
2. **The Smart Search Engine:** Lets you ask questions across *all* your saved chats at once. It answers in seconds and tells you exactly which AI gave the answer!

---

## The 6-Week Feature Drops & Founder's Season Pass

To keep things affordable and give you fresh innovations every week, we are releasing the Smart Search Engine in **6 weekly feature drops**:

- **Week 1 (Available Today):** The Smart Search Assistant — ask any question in plain English.
- **Week 2:** The Secret Scrubber — hides passwords and emails before you share.
- **Week 3:** Model Creator — turn your best chats into training sets.
- **Week 4:** The AI Peer Reviewer — see where ChatGPT and Claude agree or disagree.
- **Week 5:** Topic Discovery Cards — colorful cards organizing your topics.
- **Week 6:** Speed & Memory Tester — tests which AI model runs fastest on your laptop.

### How to Buy:
- Buy individual features a-la-carte as you need them ($9 to $25 each, totaling $140).
- **Or save 65% with the Founder's Season Pass ($49 Launch Week / $59 standard)**, which unlocks every single weekly drop for life!

---

## How to Search in Plain English

1. Click on the **Search Chat** tab.
2. Type your question naturally, like: *"What recipe did Claude give me for gluten-free pasta?"*
3. Read the instant answer. Click on the cited chat card to open the full conversation.

---

## Our 100% Privacy Guarantee

Unlike other tools that upload your chats to cloud servers, TotalRecalls is **100% private and offline**:
- Your chats never leave your computer.
- It works on an airplane with Wi-Fi turned off.
- Nobody—not even the TotalRecalls team—can ever see your conversations.

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
    <p style="color: #64748b; font-size: 10pt;">Offline AI Chat Downloader, Vector Search & RAG SQL • totalrecalls.app</p>
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

