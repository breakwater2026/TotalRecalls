# TOTALRECALLS POWER USER MANUAL
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
