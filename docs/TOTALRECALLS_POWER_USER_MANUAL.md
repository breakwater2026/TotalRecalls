# TOTALRECALLS POWER USER MANUAL
## Smart Search Engine (SSE): Vector Search, Relational RAG SQL, Consensus Auditing & Local-Only Privacy Architecture
**Product Edition:** v1.0.0-MarketLeader  
**Vendor:** TotalRecalls (totalrecalls.app)  
**Distribution Target:** Senior Software Engineers, Data Architects, Security Auditors & Power Users  

---

## 1. Executive Summary & Dual-Unit Architecture

The TotalRecalls suite is architected around two decoupled, complimentary units:

```
+-----------------------------------------------------------------------------------------+
| TOTALRECALLS PRODUCT ECOSYSTEM (totalrecalls.app)                                       |
+-----------------------------------------------------------------------------------------+
|                                                                                         |
|   +--------------------------------------+   +--------------------------------------+   |
|   | UNIT 1: TOTALRECALLS PRO             |   | UNIT 2: SMART SEARCH ENGINE ADD-ON   |   |
|   | $24 launch / $48 regular (one-time)  |   | $29 launch / $58 regular (one-time)  |   |
|   +--------------------------------------+   +--------------------------------------+   |
|   | * Exporters: ChatGPT, Claude,        |   | * HNSW vector search                 |   |
|   |   Perplexity, Gemini, Grok,          |   | * Reciprocal Rank Fusion (BM25+Vec)  |   |
|   |   DeepSeek, Mistral, Qwen            |   | * Natural Language to SQLite         |   |
|   | * Formats: Markdown (.md), JSON      |   | * Cross-AI Consensus Auditor         |   |
|   | * Direct local filesystem storage    |   | * PII & Secret Scrubber              |   |
|   | * Microsoft Store certified          |   | * Fine-Tuning JSONL Export           |   |
|   | * Zero warnings, one-click install   |   | * Free maintenance updates           |   |
|   +--------------------------------------+   +--------------------------------------+   |
|                       |                                          |                      |
|                       +------------------------------------------+                      |
|                                            |                                            |
|                                            v                                            |
|                      +-------------------------------------------+                      |
|                      | PRIVATE LOCAL DISK RUNTIME                |                      |
|                      | C:\Users\<You>\TotalRecalls-download\     |                      |
|                      | (Zero telemetry • Zero cloud egress)      |                      |
|                      +-------------------------------------------+                      |
+-----------------------------------------------------------------------------------------+
```

---

## 2. Commercial Packaging & Pricing

TotalRecalls is a one-time purchase with no recurring subscription:

| Product | Launch Price | Regular Price | Notes |
|---|---|---|---|
| **TotalRecalls Downloader Pro** | **$24** | $48 | One-time. All 8 providers, unlimited downloads. Available on Microsoft Store (free trial) with in-app Pro key activation. |
| **Smart Search Engine (SSE) Add-On** | **$29** | $58 | One-time. Requires Pro. Indexes all saved Markdown & JSON files. |
| **Pro + SSE Bundle** | **$49** | $98 | One-time. Downloader Pro + SSE Add-On in a single discounted checkout. |

- **License Scope:** Each license key covers up to **3 personal PC activations**.
- **Updates vs. Upgrades:** Maintenance updates and provider-compatibility bug fixes within v1 are free for the life of the product.
- **Refund Guarantee:** 30-day money-back guarantee on all web purchases processed via Paddle.

---

## 3. Relational Schema Architecture (SQLite)

SSE structures your local conversations into a high-performance relational and vector SQLite schema:

```sql
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
    embedding float[384] distance_metric=cosine
);
```

---

## 4. Hybrid Reciprocal Rank Fusion (RRF) Retrieval

Combines BM25 token frequencies with dense vector cosine similarity (default embedding profile: `bge-small-en-v1.5`, 384 dimensions):

$$RRF\_Score(d) = \sum_{m \in M} \frac{1}{k + \text{rank}_m(d)}$$

Where $k = 60$. Dense retrieval surfaces conceptual and thematic neighbors, while BM25 guarantees exact precision on variable names, UUIDs, function signatures, and error codes.

---

## 5. Local Filesystem Integration

TotalRecalls Downloader exports all chats directly to your Windows user profile:
```text
C:\Users\<YourUsername>\TotalRecalls-download\Library\
  ├── chatgpt\
  │   └── home\
  │       ├── 2026-10-14_Neural-Network-Optimization.md
  │       └── 2026-10-14_Neural-Network-Optimization.json
  ├── claude\
  │   └── home\
  ├── perplexity\
  └── ... (all 8 providers)
```

SSE automatically indexes this directory structure. Every search result contains a direct file link to open the source Markdown file in your favorite editor (VS Code, Obsidian, Notepad, Word).

> **Operational Warning:** Also, note that the first download and indexing run may take 5–15 minutes depending on the number of conversations being indexed by the Smart Search Engine (SSE).

---

## 6. Privacy & Zero-Egress Contract

Smart Search Engine runs 100% locally on your PC:
* **Zero Telemetry:** No analytics, no tracking pixels, no telemetry pings.
* **Zero Cloud Egress:** Your prompts, search queries, SQL queries, and chat archives never leave your local machine.
* **Offline Independence:** After the initial one-time model weight initialization, SSE operates completely disconnected from the internet.

You can audit network traffic using packet inspection tools like Wireshark or `tshark`:
```bash
tshark -i any -f "not port 53 and not arp" -Y "http or tls"
```
No chat content or queries are transmitted over network adapters during search, SQL compilation, or data export.

---
*TotalRecalls Engineering Manual • totalrecalls.app*