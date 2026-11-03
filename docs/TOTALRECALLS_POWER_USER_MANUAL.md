# TOTALRECALLS POWER USER MANUAL

## Smart Search Engine (SSE): Vector Search, Relational RAG SQL, Consensus Auditing & Air-Gap Privacy Architecture

**Product Edition:** v2.5.0-MarketLeader  
**Vendor:** TotalRecalls (totalrecalls.app)  
**Distribution Target:** Senior Software Engineers, Data Architects, Security Auditors & Enterprise Teams  
**Distribution Format:** Markdown (.md), Microsoft Word (.docx), Print-Ready PDF  
**License:** Founder's Season Pass Perpetual (ECDSA-signed offline token)

---

## Table of Contents

1. [Executive Summary & Product Architecture](#chapter-1-executive-summary--product-architecture)
2. [Unified Search Chat GUI & Tri-Mode Retrieval](#chapter-2-unified-search-chat-gui--tri-mode-retrieval)
3. [RAG SQL Analytical Engine & Saved Views](#chapter-3-rag-sql-analytical-engine--saved-views)
4. [Consensus Auditor & Cross-AI Peer Review](#chapter-4-consensus-auditor--cross-ai-peer-review)
5. [Air-Gap PII Scrubber & Fine-Tuning Pipeline](#chapter-5-air-gap-pii-scrubber--fine-tuning-pipeline)
6. [Embedding Benchmark & 2D PCA Cluster Map](#chapter-6-embedding-benchmark--2d-pca-cluster-map)
7. [Knowledge Graph & Latent Topic Inference](#chapter-7-knowledge-graph--latent-topic-inference)
8. [Downside Protection: Backup Scheduler & Cold Vault](#chapter-8-downside-protection-backup-scheduler--cold-vault)
9. [Code Integrity & Regression Test Suite](#chapter-9-code-integrity--regression-test-suite)
10. [Commercial Packaging & 6-Week Staged Drop Model](#chapter-10-commercial-packaging--6-week-staged-drop-model)
11. [Relational Schema Architecture (SQLite)](#chapter-11-relational-schema-architecture-sqlite)
12. [Hybrid Reciprocal Rank Fusion (RRF) Retrieval](#chapter-12-hybrid-reciprocal-rank-fusion-rrf-retrieval)
13. [Air-Gap & Zero-Egress Verification](#chapter-13-air-gap--zero-egress-verification)
14. [ZIP Distribution & Installer Architecture](#chapter-14-zip-distribution--installer-architecture)
15. [In-App Access & PDF Generation](#chapter-15-in-app-access--pdf-generation)
16. [Licensing Information](#chapter-16-licensing-information)

---

# Chapter 1. Executive Summary & Product Architecture

The TotalRecalls suite is architected around two decoupled, complimentary units:

```
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
```

### 1.1 The Air-Gap Principle

Zero cloud data leakage. Client-side embedded SQLite. In-memory SIMD-accelerated vectors. Every operation—vector search, SQL querying, dataset fine-tuning export—executes entirely on-device. No packets are transmitted to any third-party server during search, indexing, or export.

### 1.2 Core Downloader (Unit 1)

The Core Downloader provides continuous local batch chat downloads across five AI providers:

| Provider | Scraper Type | Export Formats | Sync Mode |
|----------|-------------|----------------|-----------|
| ChatGPT | Web LLM scraper | JSON, Markdown, HTML, PDF | Incremental background |
| Claude | Web LLM scraper | JSON, Markdown, HTML, PDF | Incremental background |
| Gemini | Web LLM scraper | JSON, Markdown, HTML, PDF | Incremental background |
| Perplexity | Web LLM scraper | JSON, Markdown, HTML, PDF | Incremental background |
| Mistral | Web LLM scraper | JSON, Markdown, HTML, PDF | Incremental background |

All conversations are saved to an AES-256 encrypted local SQLite vault with keyword full-text indexing.

### 1.3 Smart Search Engine Add-On (Unit 2)

The Smart Search Engine transforms static local downloads into a searchable, queryable, grounded knowledge vault:

- **Semantic Vector Search Engine:** Cross-provider semantic search using cosine distance and in-memory high-dimensional embeddings. Match-quality scoring with interactive similarity sliders, top-K filters, and AI provider toggles.
- **RAG SQL Analytical Studio:** Natural Language to SQL queries translated into relational SQLite queries. Interactive SQL execution against conversations and messages tables with execution latency metrics.
- **Consensus Auditor:** Multi-model stance classification comparing ChatGPT, Claude, Gemini, and Mistral on the same topics. Detects consensus, divergence, and complementary positions.
- **PII & Secret Scrubber:** Regex and NER-based redaction engine masking live API keys (`sk_live_...`, `ghp_...`), customer emails, and private IP addresses prior to export.
- **Fine-Tuning Pipeline:** One-click export to OpenAI/Mistral JSONL, Alpaca/ShareGPT, and DPO/RLHF preference pairs for local LLM training.
- **Embedding Benchmark:** 384-dim vs 768-dim model comparison with live RAM overhead profiler and 2D PCA/UMAP semantic cluster visualization.
- **Knowledge Graph:** Automatic background entity discovery, cluster coherence scoring, and cross-thread linkage across AI providers.

---

# Chapter 2. Unified Search Chat GUI & Tri-Mode Retrieval

### 2.1 Interface Overview

The Unified Search Chat GUI is the primary interactive view of the TotalRecalls application. It features:

- **Conversational message bubbles** with turn-by-turn user/assistant rendering
- **Token counters** and metadata tags per conversation
- **Source citation drawers** under each assistant response with similarity match percentages and AI provider badges
- **SQL Execution Context Accordion** showing the exact SQLite statement generated and live table preview rows
- **Provider Filters:** All Providers, ChatGPT Only, Claude Only, Gemini Only, Perplexity Only, Mistral Only
- **Quick Suggestion Chips:** One-click sample questions (e.g., *"How do we handle 30-day refunds and Stripe webhooks?"*)

### 2.2 Tri-Mode Retrieval Switcher

| Mode | Description | Best For | Latency |
|------|-------------|----------|---------|
| **Hybrid RAG** (Default) | Combines top-K vector semantic chunks with relational SQL schema telemetry | Factually grounded, verified answers with citations | ~38ms |
| **Vector Only** | Direct cosine similarity semantic search across embeddings | Conceptual matching when you don't recall exact terms | ~12ms |
| **NL → SQL** | Translates natural language questions into local SQLite queries | Analytics, counts, comparisons, structured metrics | ~25ms |

### 2.3 Persona Customization

Switch synthesis views on the fly:

| Persona | Output Style | Use Case |
|---------|-------------|----------|
| **Standard Technical Assistant** | Balanced conversational responses | General-purpose Q&A |
| **Executive Briefing Mode** | High-density bullet points, zero fluff | Leadership summaries |
| **Code & CLI Extractor** | Code blocks and CLI commands only | Extracting snippets from chats |
| **Fact-Check & Air-Gap Auditor** | Highlights ungrounded claims | Verifying AI-generated claims |

### 2.4 Step-by-Step Operational Workflow

1. Click on the **Search Chat** tab in the navigation bar
2. Type your question in plain English (e.g., *"Which database schema did Claude and ChatGPT recommend for high concurrency?"*)
3. Select retrieval mode: Hybrid RAG, Vector Only, or NL → SQL
4. Optionally filter by AI provider
5. Read the synthesized answer with verifiable source citations
6. Click on a cited chat card to open the full conversation in the Downloader Vault
7. Optionally switch persona mode for different output styles

---

# Chapter 3. RAG SQL Analytical Engine & Saved Views

### 3.1 Relational SQLite Schema

The Smart Search Engine uses a local embedded SQLite database with the following schema:

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
    embedding float[768] distance_metric=cosine
);
```

### 3.2 Natural Language to SQL (NL → SQL)

Users can ask plain English questions which are translated into relational SQLite queries:

| Example Question | Generated SQL Pattern | Result Type |
|-----------------|----------------------|-------------|
| "Which AI provider has the highest total tokens?" | `SELECT provider, SUM(total_tokens) FROM conversations GROUP BY provider ORDER BY SUM(total_tokens) DESC LIMIT 1` | Single row, provider name |
| "Show top 5 largest conversations" | `SELECT title, total_tokens FROM conversations ORDER BY total_tokens DESC LIMIT 5` | Table with titles and token counts |
| "How many chats did I have with Claude last month?" | `SELECT COUNT(*) FROM conversations WHERE provider='Claude' AND created_at >= ?` | Integer count |
| "Show conversations containing Docker" | `SELECT * FROM messages WHERE content LIKE '%Docker%'` | Matching message rows |

**Read-Only Sandbox Guardrails:** The SQL compiler strictly rejects destructive clauses (`DROP TABLE`, `DELETE`, `UPDATE`, `INSERT`). All queries execute in a read-only sandbox.

### 3.3 Saved Analytical Views

Users can save persistent custom SQL analytical views:

- "Top 10 Most Expensive Chats" (by token count)
- "Chats containing code snippets > 50 lines"
- "Unanswered queries" (conversations with no assistant response)
- "Provider comparison by response length"

Saved views persist across sessions and can be re-executed with updated data.

### 3.4 Hybrid Grounded RAG

Combines semantic vector chunks and structured SQL telemetry to generate verified, cited answers without cloud leaks:

1. **Vector retrieval** pulls conceptual neighbors using cosine similarity
2. **BM25 lexical search** guarantees precision on exact code variables and UUIDs
3. **SQL telemetry** adds structured metadata (provider, model, timestamps, token counts)
4. **Synthesis** combines all sources into a single grounded answer with citations
5. **Verification** cross-checks the answer against source conversation text

---

# Chapter 4. Consensus Auditor & Cross-AI Peer Review

### 4.1 Multi-Model Stance Classification

The Consensus Auditor clusters discussions on matching subjects across AI providers and classifies each model's stance:

| Classification | Description | Example |
|---------------|-------------|---------|
| **High Consensus** | All models agree on the recommendation | All three recommend WAL mode for SQLite |
| **Divergent Stance** | Models disagree on the approach | Claude recommends optimistic concurrency; ChatGPT recommends Redis Redlock |
| **Complementary** | Models address different aspects of the problem | One covers security, another covers performance |

### 4.2 Automated Peer-Review Matrix

The auditor produces a side-by-side comparison showing:

- Key code snippets from each model's response
- Confidence scores per model
- Divergence analysis explaining why models disagree
- Concrete, recommended resolution

### 4.3 Divergence Analyzer & Strategic Verdict

When models disagree, the auditor analyzes root causes:

- Cloud concurrency vs. zero-dependency client portability
- Managed service vs. self-hosted infrastructure
- Short-term velocity vs. long-term maintainability

The system produces a strategic verdict with actionable recommendations.

### 4.4 Cross-Model Comparison Example

| Topic | ChatGPT Stance | Claude Stance | Gemini Stance | Consensus Score |
|-------|---------------|---------------|---------------|-----------------|
| SQLite WAL mode | Recommended | Recommended | Recommended | 94% |
| Redis Redlock for distributed locking | Recommended | Not recommended | Conditional | 67% |
| Local embedding dimension | 384-dim sufficient | 768-dim preferred | 512-dim balanced | 72% |

---

# Chapter 5. Air-Gap PII Scrubber & Fine-Tuning Pipeline

### 5.1 Secret Redaction Signatures

The PII Scrubber automatically detects and replaces sensitive data before export:

| Pattern | Example | Redaction Token |
|---------|---------|-----------------|
| Live API keys | `sk_live_51...` | `[REDACTED_API_KEY]` |
| GitHub tokens | `ghp_...` | `[REDACTED_GITHUB_TOKEN]` |
| Customer emails | `john.doe@company.com` | `[REDACTED_EMAIL]` |
| Private IP addresses | `10.0.0.5`, `192.168.1.1` | `[REDACTED_IP]` |
| JWT secrets | `eyJhbGciOiJIUzI1NiIs...` | `[REDACTED_JWT]` |
| Credit card numbers | `4111-1111-1111-1111` | `[REDACTED_CC]` |

### 5.2 Export Pipeline Formatting

The Fine-Tuning Pipeline converts curated chats into training-ready formats:

#### OpenAI / Mistral JSONL Format
```jsonl
{"messages": [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}
{"messages": [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}
```

#### Alpaca / ShareGPT Instruction Format
```json
{"instruction": "...", "input": "...", "output": "..."}
```

#### DPO / RLHF Preference Pairs
```json
{"chosen": {"role": "assistant", "content": "..."}, "rejected": {"role": "assistant", "content": "..."}}
```

Export targets: Ollama Modelfiles, Llama-Factory, Hugging Face training pipelines.

### 5.3 Air-Gap Verification

All scrubbing and export happens locally. No sensitive data is transmitted to any external service during the redaction or fine-tuning preparation process.

---

# Chapter 6. Embedding Benchmark & 2D PCA Cluster Map

### 6.1 Embedding Model Comparison

| Model | Dimension | Quantization | Latency per 1k Tokens | RAM per 100k Chunks | Provider |
|-------|-----------|--------------|----------------------|---------------------|----------|
| All-MiniLM-L6-v2 | 384 | Q4 | 18ms | 32 MB | WASM / Browser |
| BGE-Small | 384 | INT8 | 22ms | 38 MB | Local / Ollama |
| Nomic-Embed-Text | 768 | INT8 | 42ms | 78 MB | Local / Ollama |
| Gemini text-embedding-004 | 768 | FP32 | 55ms | 154 MB | Local API |

### 6.2 Trade-Off Analysis

**384-dimensional models** (BGE-Small, MiniLM):
- ~154 MB RAM per 100k turns
- Lower latency, faster indexing
- Sufficient for general semantic search
- Runs entirely in WebAssembly / browser

**768-dimensional models** (Nomic-Embed, Gemini):
- ~307 MB RAM per 100k turns
- Higher latency, slower indexing
- Better accuracy for technical code and nuanced topics
- Requires local model execution (Ollama or llama.cpp)

### 6.3 2D PCA / UMAP Semantic Cluster Projection

The Embedding Benchmark includes an interactive 2D PCA/UMAP semantic cluster scatter plot:

- Clusters conversations by topics (DevOps, Legal, Stripe, Architecture)
- Live RAM overhead profiler (MB per 100k chunks)
- Model switching on the fly with real-time re-ranking
- Hover over nodes to inspect conversation content
- Export cluster maps as SVG or PNG

---

# Chapter 7. Knowledge Graph & Latent Topic Inference

### 7.1 Automatic Entity Discovery

The Knowledge Graph performs background categorization of conversations into thematic concept cards:

| Knowledge Card | Topic Cluster | Conversation Count | Coherence Score |
|---------------|--------------|-------------------|-----------------|
| Local Vector Stores | DevOps, Infrastructure | 32 | 0.91 |
| Docker GPU Configuration | DevOps, Hardware | 14 | 0.87 |
| Stripe Webhook Idempotency | Commerce, Security | 28 | 0.89 |
| PostgreSQL pgvector | Database, Vector | 19 | 0.84 |
| Kubernetes Pod Security | Infrastructure, Security | 22 | 0.86 |

### 7.2 Cross-Thread Linkage

The graph links multi-turn threads across AI providers, enabling users to trace a topic from initial question in ChatGPT through follow-up in Claude to final resolution in Gemini.

### 7.3 Interactive Timeline

A timeline view shows token consumption trends and topic evolution over weeks or months, helping users understand how their knowledge base has grown.

---

# Chapter 8. Downside Protection: Backup Scheduler & Cold Vault

### 8.1 Autonomous Background Scheduler

Configurable schedule frequencies:

| Frequency | Options |
|-----------|---------|
| Hourly | Every hour on the hour |
| Daily | Custom local time (e.g., 03:00) |
| Weekly | Specific day of week |
| On Every Sync Event | Triggered when new conversations are downloaded |

### 8.2 Snapshot Strategies

| Strategy | Description | Storage Impact |
|----------|-------------|----------------|
| Full Snapshot | Entire conversation corpus, SQLite metadata, and pre-vectorized chunks | High |
| Differential Delta | Only conversations and vectors modified since previous snapshot | Low |

Snapshot formats: `.trsnap` (immutable snapshot container) or `.zip`

### 8.3 Cold Storage Targets

- Local app vault (`~/.totalrecalls/backups`)
- External air-gapped USB/NAS drives
- Cold `.ZIP` archive files for offline transport

### 8.4 Retention Rules

Adjustable slider from 3 to 60 snapshots. Old archives are pruned while preserving point-in-time recovery points.

### 8.5 Cryptographic Bit-Rot Protection

Each snapshot automatically computes a 256-bit SHA-256 digest via the native Web Crypto API (`crypto.subtle`). Verification:

```
Live Verify Checksum: Re-hashes stored payload and verifies against recorded manifest
One-Click Restore: Restores to active memory with safety confirmation
Export: Snapshot manifests as downloadable .JSON / .trsnap archives
```

---

# Chapter 9. Code Integrity & Regression Test Suite

### 9.1 Individual Component Tests

| Component | Test Category | Key Invariants |
|-----------|--------------|----------------|
| Vector Engine & Indexing | Zero NaN/null, dimension matching | All embeddings match active dimension (384/768) |
| Cosine Similarity | Range validation | Scores strictly bounded in [-1.0, 1.0]; identical docs score 1.000 |
| Monotonic Top-K | Order validation | Descending order across retrieved candidate pools |
| BM25 Search | Term frequency/IDF | Correctly penalizes document length; prioritizes rare technical terms |
| RRF Fusion | Formula validation | `1 / (k + rank)` with k=60; no rank inversion |
| NL → SQL Compiler | AST generation | Valid SELECT statements; row counts and execution metrics |
| SQL Sandbox Guardrails | Destructive clause rejection | Strict rejection of DROP TABLE, DELETE, UPDATE, INSERT |
| Consensus Auditor | Multi-provider extraction | Cross-model sentiment and divergence categorization |
| PII Scrubber | Zero leakage | No live secret keys, IP addresses, emails, or credit cards exported |
| Embedding Benchmark | Hardware profiles | FP32 vs INT8/Q4 quantization ratios; RAM footprints |
| Knowledge Graph | Topological clustering | Automatic entity discovery and keyword cross-linking |
| Backup Scheduler | SHA-256 hashing | Hashing speed; payload serialization; round-trip verification |

### 9.2 Whole-Module Integration Test

**Air-Gapped Zero-Egress Invariant Guarantee:** Asserts 100% on-device browser/local execution with zero third-party telemetry and zero cloud socket connections.

### 9.3 Interactive Test UI

- Real-time test status display (Passing, Failed, Running, Duration in ms)
- Filter by test category
- Inspect individual test invariants
- Export signed audit report: `TotalRecalls_SSE_Integrity_Audit.json`

Expected result: **14/14 passing** against real data.

---

# Chapter 10. Commercial Packaging & 6-Week Staged Drop Model

### 10.1 Pricing Tiers

| Tier | Price | Features |
|------|-------|----------|
| Core Downloader | $29 Lifetime | Local multi-provider chat backup, search, and export |
| Smart Search Suite (Founder's Pass) | $49 Launch / $59 Standard / $79 Post-Rollout | Vector RAG, SQL generation, PII Scrubber, Consensus Auditor, Fine-Tuning pipeline |
| Enterprise Local Fleet | $149/seat perpetual | All modules unlocked immediately; multi-seat deployment |

### 10.2 Sum-of-Parts Standalone Value: $140

| Drop | Week | Module Title | Standalone Price | Status |
|------|------|-------------|-----------------|--------|
| Launch | Week 1 | Tri-Mode Search Chat (Vector + NL→SQL + RRF) | $39 | LIVE |
| Drop 1 | Week 2 | Air-Gap PII & Secret Redaction Scrubber | $19 | Next Up |
| Drop 2 | Week 3 | 1-Click Fine-Tuning Pipeline (JSONL/Alpaca) | $19 | Planned |
| Drop 3 | Week 4 | Cross-AI Consensus & Hallucination Auditor | $25 | Planned |
| Drop 4 | Week 5 | Vault Knowledge Graph & Latent Topic Cards | $19 | Planned |
| Drop 5 | Week 6 | Embedding Engine Benchmark & 2D PCA Cluster Map | $19 | Planned |

### 10.3 Founder's Season Pass

- **Launch Week Special:** $49 (65% off sum-of-parts)
- **Standard Bundle:** $59
- **Post-Rollout:** $79

Grants instant access to Week 1 plus automatic lifetime unlock of all upcoming weekly drops.

---

# Chapter 11. Hybrid Reciprocal Rank Fusion (RRF) Retrieval

### 11.1 Mathematical Formulation

The Smart Search Engine combines BM25 token scores with dense vector cosine similarity using Reciprocal Rank Fusion:

```
RRF_Score(d) = Σ (m ∈ M) 1 / (k + rank_m(d))
```

Where **k = 60**.

Dense retrieval pulls conceptual neighbors while BM25 guarantees precision on exact code variables and UUIDs.

### 11.2 Hybrid Blend Ratio

- **60%** cosine semantic distance (conceptual matching)
- **40%** BM25 exact keyword match (precision on variables, error codes, UUIDs)

This blend guards against vector semantic drift on exact terms like `ECONNREFUSED`, `stripe.webhooks`, or function names.

---

# Chapter 12. Air-Gap & Zero-Egress Verification

### 12.1 Verification Methodology

Verify zero outbound telemetry with Wireshark:

```bash
# Capture loopback and physical interface traffic
tshark -i any -f "not port 53 and not arp" -Y "http or tls"
```

### 12.2 Zero-Egress Guarantee

During vector search, SQL querying, and dataset fine-tuning export, **0 packets are transmitted**.

### 12.3 Air-Gap Validation Checklist

- [ ] Wi-Fi toggle set to DISCONNECTED; app continues to search vectors
- [ ] SQLite database stored locally; no cloud sync
- [ ] Embedding models run locally (Ollama, llama.cpp, or WASM)
- [ ] No third-party telemetry endpoints contacted
- [ ] PII scrubbing executes entirely on-device
- [ ] Fine-tuning export generates files locally

---

# Chapter 13. ZIP Distribution & Installer Architecture

### 13.1 Distribution Archive Structure

`TotalRecalls-SSE-Suite-v2.5.0.zip` (~18.4 MB):

```
TotalRecalls-SSE-Suite-v2.5.0.zip
│
├── install.bat              # Windows 10/11 1-Click Installer
├── install.sh               # macOS / Linux Terminal Installer
├── checksums.sha256         # NIST-compliant SHA-256 integrity manifest
├── README_FIRST_START_HERE.html  # Offline landing page
│
├── bin/                     # Zero-dependency runtimes
│   └── totalrecalls-sse.wasm.bin  # Pre-compiled WebAssembly SQLite-Vec engine
│
├── docs/                    # Complete Documentation Bundle
│   ├── TOTALRECALLS_POWER_USER_MANUAL.pdf    # 30+ page technical reference
│   ├── TOTALRECALLS_USER_MANUAL_LAYMAN.pdf   # 15+ page everyday handbook
│   ├── QUICKSTART_GUIDE_3_MINUTES.pdf        # 3-minute visual setup
│   ├── TOTALRECALLS_MANUAL.docx              # Editable Word version
│   ├── TOTALRECALLS_POWER_USER_MANUAL.md     # Raw Markdown
│   └── DEMO_VIDEO_SCRIPT_TELEPROMPTER.md     # 2.5-min video script
│
├── src/                     # 100% Unminified TypeScript Source Code
│   ├── components/          # All React 19 UI modules
│   ├── services/            # Local Vector, BM25, PII Regex engines
│   └── types.ts & constants.ts  # Type definitions and mock schemas
│
└── licenses/
    └── FOUNDERS_PASS_PERPETUAL.key  # Cryptographically signed offline ECDSA token
```

### 13.2 Installer Workflows

**Mode A: In-App Drop (Zero Terminal Commands)**
Drag and drop the ZIP onto the Core Downloader desktop window. The application detects the signature, extracts the add-on to `~/.totalrecalls/modules/smart-search/`, and unlocks the Smart Search tab automatically.

**Mode B: Double-Click Native Scripts**
- **Windows (`install.bat`):** Verifies file permissions, symlinks the WASM vector database engine, verifies the offline token, creates Start Menu/Desktop shortcut, opens the PDF manual.
- **macOS/Linux (`install.sh`):** Strips Apple Quarantine bits, configures local SQLite vector extensions, creates `/usr/local/bin/totalrecalls-sse` CLI alias.

---

# Chapter 14. In-App Access & PDF Generation

### 14.1 Navigation

- **Navigation Bar:** Direct access via the Manual tab in the top navigation bar
- **Footer:** Direct link to the Power User Manual (PDF)
- **Export / Print:** "Print / Save as PDF" button invokes browser print formatting

### 14.2 Print-to-PDF Features

- Clean page breaks
- High-contrast tables
- Formatted mathematical formulas
- High-resolution code blocks

### 14.3 In-App View Modes

| Mode | Description |
|------|-------------|
| **Interactive Book Reader** | Chapter-by-chapter reading with search filtering and active status indicators |
| **Raw Markdown Source (.MD)** | Live preview of the complete Markdown document with "Copy All MD" button and line count indicator |
| **PDF Print** | Clean print-to-PDF formatting |

---

# Chapter 15. Licensing Information

**FOUNDERS_PASS_PERPETUAL.key**  
Cryptographically signed offline ECDSA token. Verified locally during installation. No cloud license server required.

### License Terms

- **Core Downloader:** Perpetual use on one machine
- **Founder's Season Pass:** Lifetime access to all 6 weekly drops, no recurring subscription
- **Enterprise Fleet:** Per-seat perpetual license, all modules unlocked immediately
- **Air-Gap Compliance:** Suitable for air-gapped and offline enterprise environments
- **Source Code:** 100% unminified TypeScript included in distribution; inspectable by security auditors

---

*TotalRecalls Power User Manual • totalrecalls.app • v2.5.0-MarketLeader*
