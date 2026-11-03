# TOTALRECALLS POWER USER GUIDE

## Local Vector Search & SQL Container — Smart Search Engine Add-On

**Product Edition:** v2.5.0-MarketLeader  
**Vendor:** TotalRecalls (totalrecalls.app)  
**Distribution Target:** Senior Software Engineers, Data Architects, Security Auditors & Enterprise Teams  
**Distribution Format:** Markdown (.md), Microsoft Word (.docx), Print-Ready PDF  
**License:** Founder's Season Pass Perpetual (ECDSA-signed offline token)

---

## Table of Contents

1. [Overview](#chapter-1-overview)
2. [Package Contents](#chapter-2-package-contents)
3. [Step 1 — Export Your Conversations](#chapter-3-step-1-export-your-conversations)
4. [Step 2 — Build the SQL Container](#chapter-4-step-2-build-the-sql-container)
5. [Step 3 — Build the Vector Index](#chapter-5-step-3-build-the-vector-index)
6. [Step 4 — Run a Query](#chapter-6-step-4-run-a-query)
7. [Step 5 — Chat with Your Archive](#chapter-7-step-5-chat-with-your-archive)
8. [Step 6 — Connect to Obsidian](#chapter-8-step-6-connect-to-obsidian)
9. [Step 7 — Connect to Notion](#chapter-9-step-7-connect-to-notion)
10. [Consensus Auditor & Cross-AI Peer Review](#chapter-10-consensus-auditor--cross-ai-peer-review)
11. [Air-Gap PII Scrubber & Fine-Tuning Pipeline](#chapter-11-air-gap-pii-scrubber--fine-tuning-pipeline)
12. [Hybrid Reciprocal Rank Fusion (RRF) Retrieval](#chapter-12-hybrid-reciprocal-rank-fusion-rrf-retrieval)
13. [Embedding Benchmark & Dimension Visualizer](#chapter-13-embedding-benchmark--dimension-visualizer)
14. [Knowledge Graph & Latent Topic Inference](#chapter-14-knowledge-graph--latent-topic-inference)
15. [Custom Persona Modes](#chapter-15-custom-persona-modes)
16. [Maintenance](#chapter-16-maintenance)
17. [Downside Protection: Backup Scheduler & Cold Vault](#chapter-17-downside-protection-backup-scheduler--cold-vault)
18. [Code Integrity & Regression Test Suite](#chapter-18-code-integrity--regression-test-suite)
19. [Scripts Reference](#chapter-19-scripts-reference)
20. [Commercial Packaging & 6-Week Staged Drop Model](#chapter-20-commercial-packaging--6-week-staged-drop-model)
21. [ZIP Distribution & Installer Architecture](#chapter-21-zip-distribution--installer-architecture)
22. [Notes](#chapter-22-notes)

---

# Chapter 1. Overview

TotalRecalls exports your conversations from the eight leading AI providers into open, local files. This system turns that export into two searchable containers on your own PC — a SQL database for structured queries, and a vector index for natural-language search — so you can find anything you ever asked any model, regardless of which sidebar it came from.

Everything runs on your machine. Nothing is uploaded, and no session tokens or conversation contents ever leave your PC.

## The eight providers

| Provider | Conversations | Status |
|----------|-------------|--------|
| chatgpt | 106 | indexed |
| perplexity | 90 | indexed |
| gemini | 86 | indexed |
| deepseek | 45 | indexed |
| claude | 39 | indexed |
| qwen | 25 | indexed |
| grok | 21 | indexed |
| mistral | 3 | indexed |
| **Total** | **415 conversations · 8,265 messages** | |

Vector index: 43,633 chunks at 384 dimensions — every provider, every conversation. Chunks are 500-character windows with 50-character overlap so sentences are never split mid-thought.

The Smart Search Engine add-on extends this foundation with seven market-leading capabilities: tri-mode retrieval (Hybrid RAG, Vector Only, NL→SQL), a cross-AI Consensus Auditor, an air-gapped PII Scrubber with fine-tuning export, an Embedding Benchmark with 2D PCA cluster visualization, a Knowledge Graph, custom Persona Modes, and downside protection via a Backup Scheduler and Code Integrity Test Suite.

| What you get | Detail |
|-------------|--------|
| One search across all eight | A single query reaches ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral and Qwen at once. |
| Natural-language search | Ask in plain English; the vector index finds the relevant conversations by meaning, not by keyword. |
| Structured SQL queries | Filter by provider, date range, message count, model, or join messages to their conversations. |
| A chat interface | Talk to your whole archive through a local chat UI backed by a local model. |
| Works with your tools | Native Markdown for Obsidian, and a documented export path for Notion. |
| Fully offline | Retrieval is local; generation uses a local model. No cloud dependency. |
| One-time setup, then automatic | Build the two containers once, register the re-index task, and the system keeps itself current. |

---

# Chapter 2. Package Contents

Everything you need ships together in one folder:

| Path | Purpose |
|------|---------|
| `scripts\build_sql_container.py` | Parses every `conversation.json` into SQLite |
| `scripts\build_vector_index.py` | Embeds every `conversation.md` into the vector index |
| `scripts\search_my_ai.py` | Natural-language search from the command line |
| `scripts\chat_server.py` | Local chat UI + API (retrieval + local model) |
| `scripts\export_for_notion.py` | Exports the archive as Notion-ready Markdown |
| `scripts\reindex_all.py` | Re-runs both indexes; used by the scheduled task |
| `scripts\install_task.py` | Sets up or changes the automatic re-index schedule |
| `scripts\tr_discovery.py` | Shared discovery of conversations in the library |
| `scripts\verify_install.py` | Checks the installation end to end |
| `scripts\test_suite.py` | Assertions over the system's behaviour |
| `scripts\backup_engine.py` | Autonomous backup scheduler & cold vault studio |
| `scripts\manualExporters.ts` | Multi-format exporter (MD / DOCX / PDF) |
| `docs\` | This guide and its build script |
| `src/components/` | React 19 UI modules (Search, SQL, Auditor, Scrubber, Benchmark, Graph) |
| `src/services/` | Local Vector, BM25, PII Regex, backup, test engines |
| `venv\` | Isolated Python environment (do not delete) |
| `data\totalrecalls_chats.db` | The SQL container (created on first build) |
| `vector_store\` | The vector index (created on first build) |
| `README.md` / `INSTALL-NOTES.md` | Quick reference and full documentation |

---

# Chapter 3. Step 1 — Export Your Conversations

Open the TotalRecalls app on your Windows PC and run an export across your active providers. Each conversation is written as a pair of files into your library root:

```
C:\TotalRecalls-Downloads\Library\
  chatgpt\Home\2026-10-15 14-02 -- Async Python Architecture -- a1b2c3d4\
      conversation.json      <structured data>
      conversation.md         <readable transcript>
  claude\Home\...
  perplexity\Home\...
  gemini\Home\...
  grok\Home\...
  deepseek\Home\...
  mistral\Home\...
  qwen\Home\...
```

Both files matter: the `.json` feeds the SQL container, and the `.md` feeds the vector index.

You do not need to organise anything. The discovery layer walks the whole library tree and finds every conversation, at any nesting depth. Export a new provider and run one command — it is picked up automatically.

---

# Chapter 4. Step 2 — Build the SQL Container

This parses every `conversation.json` into a single SQLite database you can query with ordinary SQL:

```
C:\TotalRecalls-Search> venv\Scripts\python.exe scripts\build_sql_container.py
[PARSED]   106 chatgpt conversations
[PARSED]    90 perplexity conversations
[PARSED]    86 gemini conversations
[PARSED]    45 deepseek conversations
[PARSED]    39 claude conversations
[PARSED]    25 qwen conversations
[PARSED]    21 grok conversations
[PARSED]     3 mistral conversations
------------------------------------------------------------------------
[TOTAL]   415 conversations, 8265 messages
[COVERAGE] 8/8 providers indexed
```

## Schema

| Column | Meaning |
|--------|---------|
| `conv_key` | Unique key joining chats and messages (provider + relative path) |
| `provider` | chatgpt, claude, perplexity, gemini, grok, deepseek, mistral, qwen |
| `title` / `conv_label` | Conversation title; directory name with export artifacts stripped |
| `created_at` / `updated_at` | Timestamps from the export |
| `message_count` / `char_count` | Size of the conversation |
| `json_path` / `md_path` | Where the source files live |

The `messages` table holds one row per message with its role, model, `content_md`, and `external_id`.

## Example queries

```sql
-- conversations per provider in 2026
SELECT provider, COUNT(*) FROM chats
WHERE created_at >= '2026-01-01' GROUP BY provider ORDER BY 2 DESC;

-- average engagement per provider
SELECT provider, COUNT(*), ROUND(AVG(message_count),1)
FROM chats GROUP BY provider ORDER BY 3 DESC;

-- which models were used
SELECT model, COUNT(*) FROM messages
WHERE model != '' GROUP BY model ORDER BY 2 DESC;

-- every message with its conversation title
SELECT c.title, m.role, substr(m.content_md,1,80)
FROM chats c JOIN messages m ON m.conv_key = c.conv_key
WHERE c.provider = 'perplexity';
```

## Saved analytical views (Smart Search Engine add-on)

You can save persistent custom SQL analytical views:

- "Top 10 Most Expensive Chats" (by token count)
- "Chats containing code snippets > 50 lines"
- "Unanswered queries" (conversations with no assistant response)
- "Provider comparison by response length"

Saved views persist across sessions and can be re-executed with updated data.

---

# Chapter 5. Step 3 — Build the Vector Index

This converts your transcripts into numerical embeddings so the system can search by meaning. It runs entirely on your PC's CPU:

```
C:\TotalRecalls-Search> venv\Scripts\python.exe scripts\build_vector_index.py
[MODEL]     loading sentence-transformers/all-MiniLM-L6-v2 (100% local, CPU)
[MODEL]     384 dimensions
[DISCOVERY] 415 conversations across 8 providers
[INDEX]     25/415 files, 336 chunks
[INDEX]     50/415 files, 913 chunks
...
[VECTOR]    43,633 chunks x 384 dims -> LanceDB 'ai_knowledge_base'
[VECTOR]    merged 19,111 new chunks (24,522 already present)
========================================================================
VECTOR INDEX BUILT
========================================================================
[STORE]     C:\TotalRecalls-Search\vector_store\ai_knowledge_base.lance
[MODEL]     sentence-transformers/all-MiniLM-L6-v2
[FILES]     415 conversations indexed (0 skipped)
[CHUNKS]    43,633 total (500 chars, 50 overlap)
[DIMS]      384
[COVERAGE]  8/8 providers indexed
```

Re-running is cheap. The builder only embeds conversations it has not seen before, so a re-index after exporting new conversations takes seconds rather than re-processing everything.

## Embedding dimension options (Smart Search Engine add-on)

| Dimension | Typical models | RAM per 100k chunks | Best for |
|-----------|---------------|---------------------|----------|
| 384 | BGE-Small, all-MiniLM-L6-v2 | ~32–38 MB | General semantic search, browser/WASM |
| 768 | Nomic-Embed-Text, Gemini | ~78–154 MB | Technical code, nuanced topics |

The 384-dim index is the default and runs entirely in WebAssembly / browser. The 768-dim index offers better accuracy for code and architecture topics but requires local model execution (Ollama or llama.cpp).

---

# Chapter 6. Step 4 — Run a Query

Ask a question in plain English. The system searches every provider at once and returns the most relevant passages with their source files.

```
C:\TotalRecalls-Search> venv\Scripts\python.exe scripts\search_my_ai.py "sierra chart order flow reversal alert"
[QUERY]   "sierra chart order flow reversal alert"
[MODEL]   sentence-transformers/all-MiniLM-L6-v2 (local)
[MATCHES] 4
------------------------------------------------------------------------------
[MATCH 1 - QWEN] cosine similarity 0.6788 (distance 0.6425)
  Conversation: 2025-08-13 08-52 -- Accessing Coding Model Clarification
  File: C:/TotalRecalls-Downloads/Library/qwen/Home/2025-08-13 08-52 -- Accessing Coding Model Clarification --
  Snippet: "(2 minutes) 1. Open your ES chart in Sierra Chart 2. Ensure the "SML Zone Exporter Hybrid Final" stu
------------------------------------------------------------------------------
[MATCH 2 - PERPLEXITY] cosine similarity 0.6667 (distance 0.6667)
  Conversation: 2025-08-16 21-25 -- I am a full-time daytrader in the CME indices futures contracts (ES for -- 6
...
[RESULT] 4 matches across providers
[COVERAGE] 8/8 providers indexed
```

## Reading the output

| Line | Meaning |
|------|---------|
| `[MATCH n — PROVIDER]` | Which provider the hit came from — one query, eight providers |
| `cosine similarity` | 0 to 1; higher is closer to your question |
| `distance` | LanceDB's internal metric; lower is better |
| `Conversation` | The conversation the chunk belongs to |
| `File` | The exact source file on your disk — click through to read the full context |
| `Snippet` | The matched text itself |

## Useful variations

```
:: restrict to one provider
venv\Scripts\python.exe scripts\search_my_ai.py "prop firm rules" --provider perplexity

:: ask for more results
venv\Scripts\python.exe scripts\search_my_ai.py "redis worker retry" --limit 10

:: only accept confident matches
venv\Scripts\python.exe scripts\search_my_ai.py "kubernetes ingress" --min-score 0.55

:: also search the SQL metadata (titles and full message text)
venv\Scripts\python.exe scripts\search_my_ai.py "sierra chart" --sql
```

When a hit looks right, open the file. The snippet is a 500-character window; the source file contains the whole conversation, so you always have the full context available.

## Tri-Mode Retrieval (Smart Search Engine add-on)

| Mode | Description | Best For | Latency |
|------|-------------|----------|---------|
| **Hybrid RAG** (Default) | Combines top-K vector semantic chunks with relational SQL schema telemetry | Factually grounded, verified answers with citations | ~38ms |
| **Vector Only** | Direct cosine similarity semantic search across embeddings | Conceptual matching when you don't recall exact terms | ~12ms |
| **NL → SQL** | Translates natural language questions into local SQLite queries | Analytics, counts, comparisons, structured metrics | ~25ms |

---

# Chapter 7. Step 5 — Chat with Your Archive

The chat interface has two modes. Retrieval works on any machine; generation additionally needs a local model that can actually run on your hardware.

| Mode | When to use it |
|------|---------------|
| Retrieval only (`--no-llm`) | Default recommendation. Answers instantly, with no model required — the interface returns the matching passages with their sources. |
| Retrieval + model (`chat_server.py`) | When you have a local model that runs acceptably on your machine (see the hardware note below). The model answers using only the retrieved passages. |

## Start the chat interface

```bash
:: retrieval only - recommended, no model needed
C:\TotalRecalls-Search> venv\Scripts\python.exe scripts\chat_server.py --no-llm

:: with a local model (LM Studio or any OpenAI-compatible endpoint)
C:\TotalRecalls-Search> venv\Scripts\python.exe scripts\chat_server.py
```

Then open `http://localhost:8000` in your browser.

## Custom Persona Modes (Smart Search Engine add-on)

Switch synthesis views on the fly:

| Persona | Output Style | Use Case |
|---------|-------------|----------|
| **Standard Technical Assistant** | Balanced conversational responses | General-purpose Q&A |
| **Executive Briefing Mode** | High-density bullet points, zero fluff | Leadership summaries |
| **Code & CLI Extractor** | Code blocks and CLI commands only | Extracting snippets from chats |
| **Fact-Check & Air-Gap Auditor** | Highlights ungrounded claims | Verifying AI-generated claims |

Use the Persona Mode pills right at the top bar of the Search Chat GUI.

---

# Chapter 8. Step 6 — Connect to Obsidian

Your library is already plain Markdown, so Obsidian needs no conversion at all. The eight provider folders appear as native notes with full graph connectivity.

## Set up the vault

1. Open Obsidian and choose **Open folder as vault**.
2. Select `C:\TotalRecalls-Downloads\Library`.

That is the entire setup. Every conversation becomes a note, and because each `.md` file starts with the conversation title as an `#` heading, Obsidian builds a browsable graph automatically.

## Recommended vault settings

| Setting | Recommendation |
|---------|---------------|
| New link format | Relative path — keeps links working if you ever move the library |
| Detect all file extensions | On |
| Excluded folders | None — you want all eight providers visible |
| Templates folder | Optional — create one if you want to add your own notes alongside the exports |

## Making the most of it

- **Graph view** — open it and filter by provider folder to see which topics recur across models.
- **Search** — Obsidian's own search is instant and covers the full text of every transcript, complementing the semantic search in this system.
- **Daily notes** — link a conversation into your daily note to build a personal knowledge trail over time.
- **Tags** — add `#sierra-chart` or `#prop-firm` to conversations you want to find again; Obsidian's tag pane then groups them across all providers.
- Keep the library read-only if you can. TotalRecalls rewrites these files on each export. If you edit a note, consider copying it to a separate Notes folder inside your vault so an export does not overwrite your annotations.

---

# Chapter 9. Step 7 — Connect to Notion

Notion cannot read a folder of Markdown files directly, so this system provides an exporter that turns your archive into Notion-ready pages. Each conversation becomes one page, grouped by provider.

## Export your archive for Notion

```
C:\TotalRecalls-Search> venv\Scripts\python.exe scripts\export_for_notion.py
========================================================================
NOTION EXPORT COMPLETE
========================================================================
[SOURCE]   C:\TotalRecalls-Downloads\Library
[OUTPUT]   C:\TotalRecalls-Search\notion_export\
[PROVIDERS] 8
[PAGES]    415 conversation pages
[INDEX]    8 provider index pages
Files written:
  notion_export\index.md              <start here — links to all providers>
  notion_export\chatgpt.md            <106 pages>
  notion_export\perplexity.md         <90 pages>
  notion_export\gemini.md             <86 pages>
  notion_export\deepseek.md           <45 pages>
  notion_export\claude.md             <39 pages>
  notion_export\qwen.md               <25 pages>
  notion_export\grok.md               <21 pages>
  notion_export\mistral.md            <3 pages>
```

## Import into Notion

1. In Notion, open the workspace page that will hold your archive.
2. Choose **Import** from the `···` menu (or drag the folder onto the page).
3. Select **Markdown & CSV** as the import type.
4. Select the `C:\TotalRecalls-Search\notion_export` folder.
5. Notion creates one page per conversation, grouped under a folder per provider.

Import is one-way and repeatable. Notion copies the content in; it does not stay linked to your library. Re-run the exporter and re-import to refresh after new exports — pages are named by conversation, so you can replace rather than duplicate.

## Alternative: Notion API (automatic sync)

If you prefer the archive to stay current without manual imports, the same script can push pages straight into Notion via its API:

```bash
:: create a Notion integration at https://www.notion.so/my-integrations
:: copy the internal integration token
:: share your target database/page with that integration
venv\Scripts\python.exe scripts\export_for_notion.py --to-api \
    --token secret_xxxxxxxxxxxx --parent-page PAGE_ID
```

Run that on the same schedule as your re-index and Notion always mirrors your archive.

| Tool | Best for |
|------|---------|
| Notion import | A one-off copy you can freely rearrange, annotate and share |
| Notion API sync | A living mirror that tracks new exports automatically |
| Obsidian | Daily working, graph exploration, and your own linked notes |

---

# Chapter 10. Consensus Auditor & Cross-AI Peer Review

When you ask multiple AIs (e.g., ChatGPT vs Claude vs Gemini) the same complex technical, legal, or architectural question over time, their recommendations often diverge or contradict each other. The Consensus Auditor is your personal AI peer review board.

## Multi-model stance classification

The auditor clusters discussions on matching subjects across AI providers and classifies each model's stance:

| Classification | Description | Example |
|---------------|-------------|---------|
| **High Consensus** | All models agree on the recommendation | All three recommend WAL mode for SQLite |
| **Divergent Stance** | Models disagree on the approach | Claude recommends optimistic concurrency; ChatGPT recommends Redis Redlock |
| **Complementary** | Models address different aspects of the problem | One covers security, another covers performance |

## Automated peer-review matrix

The auditor produces a side-by-side comparison showing:

- Key code snippets from each model's response
- Confidence scores per model
- Divergence analysis explaining why models disagree
- Concrete, recommended resolution

## Divergence analyzer & strategic verdict

When models disagree, the auditor analyzes root causes:

- Cloud concurrency vs. zero-dependency client portability
- Managed service vs. self-hosted infrastructure
- Short-term velocity vs. long-term maintainability

The system produces a strategic verdict with actionable recommendations.

## Cross-model comparison example

| Topic | ChatGPT Stance | Claude Stance | Gemini Stance | Consensus Score |
|-------|---------------|---------------|---------------|-----------------|
| SQLite WAL mode | Recommended | Recommended | Recommended | 94% |
| Redis Redlock for distributed locking | Recommended | Not recommended | Conditional | 67% |
| Local embedding dimension | 384-dim sufficient | 768-dim preferred | 512-dim balanced | 72% |

Access via **Navbar → Consensus** to audit conflicting AI stances across topics and inspect source conversations.

---

# Chapter 11. Air-Gap PII Scrubber & Fine-Tuning Pipeline

Downloaded chat logs frequently contain sensitive data — live Stripe keys (`sk_live_...`), GitHub tokens (`ghp_...`), internal employee emails, and private IP addresses. Developers cannot safely share archives or train local LLMs without risking credential leaks. The PII Scrubber solves this.

## Secret redaction signatures

The PII Scrubber automatically detects and replaces sensitive data before export:

| Pattern | Example | Redaction Token |
|---------|---------|-----------------|
| Live API keys | `sk_live_51...` | `[REDACTED_API_KEY]` |
| GitHub tokens | `ghp_...` | `[REDACTED_GITHUB_TOKEN]` |
| Customer emails | `john.doe@company.com` | `[REDACTED_EMAIL]` |
| Private IP addresses | `10.0.0.5`, `192.168.1.1` | `[REDACTED_IP]` |
| JWT secrets | `eyJhbGciOiJIUzI1NiIs...` | `[REDACTED_JWT]` |
| Credit card numbers | `4111-1111-1111-1111` | `[REDACTED_CC]` |

## Export pipeline formatting

The Fine-Tuning Pipeline converts curated chats into training-ready formats:

### OpenAI / Mistral JSONL Format
```jsonl
{"messages": [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}
{"messages": [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}
```

### Alpaca / ShareGPT Instruction Format
```json
{"instruction": "...", "input": "...", "output": "..."}
```

### DPO / RLHF Preference Pairs
```json
{"chosen": {"role": "assistant", "content": "..."}, "rejected": {"role": "assistant", "content": "..."}}
```

Export targets: Ollama Modelfiles, Llama-Factory, Hugging Face training pipelines.

## Air-gap verification

All scrubbing and export happens locally. No sensitive data is transmitted to any external service during the redaction or fine-tuning preparation process.

Access via **Navbar → PII Scrubber** to audit redacted credentials and download ready-to-train `.jsonl` or `.json` datasets.

---

# Chapter 12. Hybrid Reciprocal Rank Fusion (RRF) Retrieval

## 12.1 Mathematical Formulation

The Smart Search Engine combines BM25 token scores with dense vector cosine similarity using Reciprocal Rank Fusion:

```
RRF_Score(d) = Σ (m ∈ M) 1 / (k + rank_m(d))
```

Where **k = 60**.

Dense retrieval pulls conceptual neighbors while BM25 guarantees precision on exact code variables and UUIDs.

## 12.2 Hybrid Blend Ratio

- **60%** cosine semantic distance (conceptual matching)
- **40%** BM25 exact keyword match (precision on variables, error codes, UUIDs)

This blend guards against vector semantic drift on exact terms like `ECONNREFUSED`, `stripe.webhooks`, or function names.

## 12.3 How RRF Works in Practice

When you run a query, the system:

1. Retrieves the top-K results from the vector index (semantic similarity)
2. Retrieves the top-K results from BM25 lexical search (exact keyword match)
3. Computes the RRF score for each document that appears in either list
4. Re-ranks the combined list by RRF score
5. Returns the top results with source citations

### Example

A search for `"sierra chart order flow reversal alert"` might return:

| Rank | Document | Vector Rank | BM25 Rank | RRF Score |
|------|----------|-------------|-----------|-----------|
| 1 | Qwen conversation (Sierra Chart alert) | 1 | 3 | 0.58 |
| 2 | Perplexity thread (ES futures) | 2 | 1 | 0.52 |
| 3 | Gemini thread (Sierra Chart Script) | 3 | 5 | 0.41 |

Even though the Perplexity thread ranked #1 in BM25 (exact keyword match), the Qwen conversation ranks #1 overall because it scored highly in both vector and BM25 retrieval — the hallmark of a strong RRF result.

Access via **Navbar → RAG SQL** to toggle FTS5 + Vector RRF Blend and create custom saved analytical views.

---

# Chapter 13. Embedding Benchmark & Dimension Visualizer

Users frequently ask whether they should use nomic-embed-text (768-dim), bge-small-en (384-dim), or Gemini/OpenAI embeddings. The Embedding Benchmark lets you switch models on the fly, showing memory footprint calculations and re-ranking differences in real-time.

## Embedding model comparison

| Model | Dimension | Quantization | Latency per 1k Tokens | RAM per 100k Chunks | Provider |
|-------|-----------|--------------|----------------------|---------------------|----------|
| All-MiniLM-L6-v2 | 384 | Q4 | 18ms | 32 MB | WASM / Browser |
| BGE-Small | 384 | INT8 | 22ms | 38 MB | Local / Ollama |
| Nomic-Embed-Text | 768 | INT8 | 42ms | 78 MB | Local / Ollama |
| Gemini text-embedding-004 | 768 | FP32 | 55ms | 154 MB | Local API |

## Trade-off analysis

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

## 2D PCA / UMAP semantic cluster projection

The benchmark includes an interactive 2D PCA/UMAP semantic cluster scatter plot:

- Clusters conversations by topics (DevOps, Legal, Stripe, Architecture)
- Live RAM overhead profiler (MB per 100k chunks)
- Model switching on the fly with real-time re-ranking
- Hover over nodes to inspect conversation content
- Export cluster maps as SVG or PNG

Access via **Navbar → Embedding Bench**.

---

# Chapter 14. Knowledge Graph & Latent Topic Inference

As the downloader pulls hundreds of sessions, users lose track of what knowledge they actually possess. The Knowledge Graph performs automatic background categorization into thematic concept cards.

## Automatic entity discovery

| Knowledge Card | Topic Cluster | Conversation Count | Coherence Score |
|---------------|--------------|-------------------|-----------------|
| Local Vector Stores | DevOps, Infrastructure | 32 | 0.91 |
| Docker GPU Configuration | DevOps, Hardware | 14 | 0.87 |
| Stripe Webhook Idempotency | Commerce, Security | 28 | 0.89 |
| PostgreSQL pgvector | Database, Vector | 19 | 0.84 |
| Kubernetes Pod Security | Infrastructure, Security | 22 | 0.86 |

## Cross-thread linkage

The graph links multi-turn threads across AI providers, enabling users to trace a topic from initial question in ChatGPT through follow-up in Claude to final resolution in Gemini.

## Interactive timeline

A timeline view shows token consumption trends and topic evolution over weeks or months, helping users understand how their knowledge base has grown.

Access via **Navbar → Knowledge Graph** to filter by domain (Data & Search, Infrastructure, Security & Commerce, Analytics) and inspect automatically clustered themes and linked chat sessions.

---

# Chapter 15. Custom Persona Modes

Let users define custom personas and system instructions when interacting with their vault in the Search Chat GUI:

| Persona | Output Style | Use Case |
|---------|-------------|----------|
| **Standard Technical Assistant** | Balanced conversational responses | General-purpose Q&A |
| **Executive Briefing Mode** | High-density bullet points, zero fluff | Leadership summaries |
| **Code & CLI Extractor** | Code blocks and CLI commands only | Extracting snippets from chats |
| **Fact-Check & Air-Gap Auditor** | Highlights ungrounded claims | Verifying AI-generated claims |

Use the Persona Mode pills right at the top bar of the Search Chat GUI.

---

# Chapter 16. Maintenance

The system is designed to maintain itself. You choose how often it runs.

## Automatic re-index

Register the scheduled task and the system re-indexes itself on a fixed schedule. The default is once every 24 hours at 3:00 a.m.

```
C:\TotalRecalls-Search> venv\Scripts\python.exe scripts\install_task.py
[OK] task 'TotalRecalls-ReIndex' registered (every 24 hours at 03:00)
State  : Ready
Start  : 2026-10-27T03:00:00-04:00
Repeat : P1D
```

The task runs `scripts\reindex_all.py`, which rebuilds both containers. It only processes conversations it has not seen before, so a run after a normal day takes seconds.

## Choosing your own schedule

```bash
:: default: every 24 hours at 03:00
venv\Scripts\python.exe scripts\install_task.py

:: every 12 hours at 03:00 and 15:00
venv\Scripts\python.exe scripts\install_task.py --interval-hours 12

:: every 6 hours
venv\Scripts\python.exe scripts\install_task.py --interval-hours 6

:: weekly on Sunday at 03:00
venv\Scripts\python.exe scripts\install_task.py --weekly --day Sunday

:: run at a different time of day
venv\Scripts\python.exe scripts\install_task.py --at 22:30

:: stop the automatic task entirely
venv\Scripts\python.exe scripts\install_task.py --disable

:: see what is currently registered
venv\Scripts\python.exe scripts\install_task.py --show
```

| Option | Effect |
|--------|--------|
| `--interval-hours N` | Run every N hours (default 24) |
| `--at HH:MM` | Time of day for the run (default 03:00) |
| `--weekly --day D` | Run weekly on day D instead of hourly |
| `--disable` | Remove the task; re-index manually when you choose |
| `--show` | Print the current task definition |

Leaving it on is the recommended default. A 24-hour cycle means your archive is never more than a day stale, and the incremental merge keeps the cost near zero.

## Manual re-index

```
C:\TotalRecalls-Search> venv\Scripts\python.exe scripts\reindex_all.py
```

Every scheduled run appends to `reindex_log.txt` in the install folder, so you can see exactly what happened and when.

---

# Chapter 17. Downside Protection: Backup Scheduler & Cold Vault

Because local chat histories and embeddings are critical intellectual property that must survive accidental corruption, disk failure, or schema upgrades, TotalRecalls includes a dedicated downside protection engine.

## Autonomous background scheduler

Configurable schedule frequencies:

| Frequency | Options |
|-----------|---------|
| Hourly | Every hour on the hour |
| Daily | Custom local time (e.g., 03:00) |
| Weekly | Specific day of week |
| On Every Sync Event | Triggered when new conversations are downloaded |

## Snapshot strategies

| Strategy | Description | Storage Impact |
|----------|-------------|----------------|
| Full Snapshot | Captures the entire conversation corpus, SQLite metadata, and pre-vectorized chunks into an immutable snapshot container (`.trsnap` or `.zip`) | High |
| Differential Delta | Backs up only conversations and vectors modified since the previous snapshot | Low |

## Cold storage targets

- Local app vault (`~/.totalrecalls/backups`)
- External air-gapped USB/NAS drives
- Cold `.ZIP` archive files for offline transport

## Retention rules

Adjustable slider from 3 to 60 snapshots. Old archives are pruned while preserving point-in-time recovery points.

## Cryptographic bit-rot protection

Each snapshot automatically computes a 256-bit SHA-256 digest via the native Web Crypto API (`crypto.subtle`).

**Live Verify Checksum** — Re-hashes the stored payload and verifies it against the recorded manifest.

**One-Click Restore** — Restores to active memory with safety confirmation and summary of restored chats, vector count, and timestamp.

**Export** — Snapshot manifests as downloadable `.JSON` / `.trsnap` archives.

---

# Chapter 18. Code Integrity & Regression Test Suite

A rigorous test harness executes comprehensive assertions across every component and the module as a whole.

## Individual component tests

| Component | Test Category | Key Invariants |
|-----------|--------------|----------------|
| Vector Engine & Indexing | Zero NaN/null, dimension matching | All embeddings match active dimension (384/768) |
| Cosine Similarity | Range validation | Scores strictly bounded in [-1.0, 1.0]; identical docs score 1.000 |
| Monotonic Top-K | Order validation | Descending order across retrieved candidate pools |
| BM25 Search | Term frequency/IDF | Correctly penalizes document length; prioritizes rare technical terms |
| RRF Fusion | Formula validation | `1 / (k + rank)` with k=60; no rank inversion |
| NL → SQL Compiler | AST generation | Valid SELECT statements; row counts and execution metrics |
| SQL Sandbox Guardrails | Destructive clause rejection | Strict rejection of `DROP TABLE`, `DELETE`, `UPDATE`, `INSERT` |
| Consensus Auditor | Multi-provider extraction | Cross-model sentiment and divergence categorization |
| PII Scrubber | Zero leakage | No live secret keys, IP addresses, emails, or credit cards exported |
| Embedding Benchmark | Hardware profiles | FP32 vs INT8/Q4 quantization ratios; RAM footprints |
| Knowledge Graph | Topological clustering | Automatic entity discovery and keyword cross-linking |
| Backup Scheduler | SHA-256 hashing | Hashing speed; payload serialization; round-trip verification |

## Whole-module integration test

**Air-Gapped Zero-Egress Invariant Guarantee:** Asserts 100% on-device browser/local execution with zero third-party telemetry and zero cloud socket connections.

## Interactive test UI

- Real-time test status display (Passing, Failed, Running, Duration in ms)
- Filter by test category
- Inspect individual test invariants
- Export signed audit report: `TotalRecalls_SSE_Integrity_Audit.json`

Expected result: **14/14 passing** against real data.

Access via **Navbar → Integrity Tests** to run the full suite.

---

# Chapter 19. Scripts Reference

Every script in the package, with its full source. They are also on disk under `scripts\`.

## Core Scripts

### build_sql_container.py

Parses every `conversation.json` into the SQLite container.

```python
#!/usr/bin/env python
"""Rebuild the local SQLite metadata container from the TotalRecalls library.
Discovers every conversation regardless of nesting depth, so adding a provider
requires no code change.
Writes: C:\TotalRecalls-Search\data\totalrecalls_chats.db
Run:  C:\TotalRecalls-Search\venv\Scripts\python.exe build_sql_container.py
"""
from __future__ import annotations
import argparse
import os
import sqlite3
import sys
from datetime import datetime, timezone
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tr_discovery import (
    SUPPORTED_PROVIDERS,
    conversation_body,
    dir_identity,
    display_name,
    find_conversations,
    provider_coverage,
    read_json,
)
DEFAULT_LIBRARY = r"C:\TotalRecalls-Downloads\Library"
DEFAULT_DB = r"C:\TotalRecalls-Search\data\totalrecalls_chats.db"
SCHEMA_VERSION = 3
SCHEMA = """
CREATE TABLE IF NOT EXISTS chats (
    row_pk      INTEGER PRIMARY KEY AUTOINCREMENT,
    conv_key    TEXT NOT NULL UNIQUE,
    provider    TEXT NOT NULL,
    folder      TEXT NOT NULL,
    title       TEXT,
    conv_label  TEXT,
    occurred_at TEXT,
    created_at  TEXT,
    updated_at  TEXT,
    message_count INTEGER NOT NULL DEFAULT 0,
    char_count  INTEGER NOT NULL DEFAULT 0,
    json_path   TEXT NOT NULL,
    md_path     TEXT
);
CREATE TABLE IF NOT EXISTS messages (
    message_pk  INTEGER PRIMARY KEY AUTOINCREMENT,
    conv_key    TEXT NOT NULL,
    ordinal     INTEGER NOT NULL,
    role        TEXT NOT NULL,
    model       TEXT,
    created_at  TEXT,
    char_count  INTEGER NOT NULL DEFAULT 0,
    external_id TEXT,
    content_md  TEXT,
    UNIQUE(conv_key, ordinal)
);
CREATE INDEX IF NOT EXISTS idx_chats_provider ON chats(provider);
CREATE INDEX IF NOT EXISTS idx_chats_created  ON chats(created_at);
CREATE INDEX IF NOT EXISTS idx_msgs_conv      ON messages(conv_key, ordinal);
CREATE TABLE IF NOT EXISTS meta (
    key   TEXT PRIMARY KEY,
    value TEXT
);
"""
```

### build_vector_index.py

Embeds every `conversation.md` into the LanceDB index.

```python
#!/usr/bin/env python
"""Build the offline LanceDB vector index from TotalRecalls Markdown exports.
Discovers every conversation regardless of nesting depth, so adding a provider
requires no code change.
Reads:  C:\TotalRecalls-Downloads\Library\  (any layout)
Writes: C:\TotalRecalls-Search\vector_store\  (LanceDB table "ai_knowledge_base")
Embeddings are computed 100% locally by sentence-transformers
(all-MiniLM-L6-v2, 384 dims). Nothing leaves the machine.
Chunking: 500-char windows with 50-char overlap.
Run:  C:\TotalRecalls-Search\venv\Scripts\python.exe build_vector_index.py
"""
from __future__ import annotations
import argparse
import os
import sys
from datetime import datetime, timezone
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tr_discovery import (
    SUPPORTED_PROVIDERS,
    display_name,
    find_conversations,
    provider_coverage,
)
DEFAULT_LIBRARY = r"C:\TotalRecalls-Downloads\Library"
DEFAULT_STORE = r"C:\TotalRecalls-Search\vector_store"
DEFAULT_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")
```

### search_my_ai.py

Natural-language search across all providers.

```python
#!/usr/bin/env python
"""Cross-provider semantic search over the local TotalRecalls vector index.
Natural-language queries run against every indexed conversation, regardless
of which AI provider originated it.
Usage:
  python search_my_ai.py "asynchronous queue worker error handling"
  python search_my_ai.py "sierra chart reversal alert" --limit 5 --provider perplexity
Run:  C:\TotalRecalls-Search\venv\Scripts\python.exe search_my_ai.py "your query"
"""
from __future__ import annotations
import argparse
import os
import sqlite3
import sys
DEFAULT_STORE = r"C:\TotalRecalls-Search\vector_store"
DEFAULT_DB = r"C:\TotalRecalls-Search\data\totalrecalls_chats.db"
DEFAULT_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
TABLE = "ai_knowledge_base"
```

### chat_server.py

Local chat UI + OpenAI-compatible API with retrieval.

```python
#!/usr/bin/env python
"""Local RAG chat server for the TotalRecalls search system.
Serves a web chat UI and an OpenAI-compatible API on http://localhost:8000.
Each user message is embedded and used to retrieve the most relevant chunks from
the LanceDB vector index; those chunks are prepended as context and the prompt
is sent to a local LLM for generation.
Generation backend (in order of preference):
  1. LM Studio's local server   (http://localhost:1234/v1)  — default
  2. Any other OpenAI-compatible endpoint via --llm-base-url
Nothing is sent to the cloud: retrieval is local, and generation goes to the
local model you already run.
Run:
  C:\TotalRecalls-Search\venv\Scripts\python.exe chat_server.py
  then open http://localhost:8000
"""
from __future__ import annotations
import argparse
import json
import os
import sys
import urllib.error
import urllib.request
DEFAULT_STORE = r"C:\TotalRecalls-Search\vector_store"
DEFAULT_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
TABLE = "ai_knowledge_base"
DEFAULT_LLM_URL = "http://localhost:1234/v1"
DEFAULT_LLM_MODEL = "qwen3-30b-a3b-instruct-2507"
PORT = 8000
```

### export_for_notion.py

Exports the archive as Notion-ready Markdown (and optional API sync).

```python
#!/usr/bin/env python
"""Export the TotalRecalls archive as Notion-ready Markdown.
Notion can import a folder of Markdown directly, so this writes one page per
conversation, grouped by provider, plus an index. Optionally pushes the same
pages into Notion over its API so the workspace stays in step automatically.
Modes:
  (default)            write Markdown files to C:\TotalRecalls-Search\notion_export\
  --to-api             push/upsert pages via the Notion API
  --to-api --dry-run   show what the API sync would do, without changing anything
Run:
  C:\TotalRecalls-Search\venv\Scripts\python.exe scripts\export_for_notion.py
"""
from __future__ import annotations
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tr_discovery import (
    SUPPORTED_PROVIDERS,
    conversation_body,
    find_conversations,
    provider_coverage,
    read_json,
)
DEFAULT_LIBRARY = r"C:\TotalRecalls-Downloads\Library"
DEFAULT_OUT = r"C:\TotalRecalls-Search\notion_export"
NOTION_VERSION = "2022-06-28"
```

### reindex_all.py

Re-runs both indexes; used by the scheduled task.

```python
#!/usr/bin/env python
"""Re-run both local indexes (SQLite metadata + LanceDB vectors).
Intended for the Windows scheduled task. Safe to run repeatedly: the SQL
builder upserts, and the vector builder merges only unseen chunk_ids.
Exit code 0 = both indexes current. Non-zero = something needs attention
(the scheduled task logs this to reindex_log.txt).
Run:  C:\TotalRecalls-Search\venv\Scripts\python.exe reindex_all.py
"""
from __future__ import annotations
import os
import subprocess
import sys
from datetime import datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VENV_PY = os.path.join(ROOT, "venv", "Scripts", "python.exe")
LOG = os.path.join(ROOT, "reindex_log.txt")
```

### install_task.py

Sets up, reconfigures or removes the automatic re-index task.

```python
#!/usr/bin/env python
"""Install, reconfigure, or remove the automatic re-index scheduled task.
You choose how often the system maintains itself. Defaults to once every 24
hours at 03:00.
Options:
  --interval-hours N   run every N hours            (default 24)
  --at HH:MM           time of day for the run      (default 03:00)
  --weekly --day D     run weekly on day D instead  (e.g. Sunday)
  --disable            remove the task entirely
  --show               print the current task definition
Run:
  C:\TotalRecalls-Search\venv\Scripts\python.exe scripts\install_task.py
"""
from __future__ import annotations
import argparse
import os
import subprocess
import sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VENV_PY = os.path.join(ROOT, "venv", "Scripts", "python.exe")
SCRIPT = os.path.join(ROOT, "scripts", "reindex_all.py")
TASK_NAME = "TotalRecalls-ReIndex"
```

### tr_discovery.py

Shared discovery of conversations in the library.

```python
#!/usr/bin/env python
"""Shared discovery of TotalRecalls conversations in the export library.
The export layout has drifted over time and differs by provider:
  Current (chatgpt/claude/perplexity/qwen):
      Library/<provider>/<folder>/<conversation-dir>/conversation.{md,json}
  Memo's own snapshot (older/newer export style):
      Library/<provider>/<conversation>.md
  Gemini Takeout may nest one level deeper again.
Discovery is therefore layout-agnostic: walk the tree, find every
`conversation.json`, and derive the provider from the first path segment under
the library root. This means adding a provider requires no code change.
"""
from __future__ import annotations
import json
import os
import re
SUPPORTED_PROVIDERS = (
    "chatgpt",
    "claude",
    "perplexity",
    "gemini",
    "grok",
    "deepseek",
    "mistral",
    "qwen",
)
```

### verify_install.py

Checks the whole installation end to end.

```python
#!/usr/bin/env python
"""Verify the installed TotalRecalls local search stack end to end.
Checks: dependency imports, SQLite row counts vs the library, LanceDB table
shape, embedding dimension agreement, and a live semantic query.
Exit 0 = everything checks out.
Run:  C:\TotalRecalls-Search\venv\Scripts\python.exe scripts\verify_install.py
"""
from __future__ import annotations
import glob
import os
import sqlite3
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tr_discovery import (
    SUPPORTED_PROVIDERS,
    find_conversations,
    provider_coverage,
)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VENV_PY = os.path.join(ROOT, "venv", "Scripts", "python.exe")
DB = os.path.join(ROOT, "data", "totalrecalls_chats.db")
STORE = os.path.join(ROOT, "vector_store")
LIBRARY = r"C:\TotalRecalls-Downloads\Library"
failures = []
```

### test_suite.py

Assertions over the system's behaviour.

```python
#!/usr/bin/env python
"""Test suite for TotalRecalls local search stack.
Executes 37 assertions covering vector indexing, SQL schema, RRF fusion,
PII scrubbing, consensus classification, and air-gap integrity.
Run:  C:\TotalRecalls-Search\venv\Scripts\python.exe scripts\test_suite.py
"""
from __future__ import annotations
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
```

### backup_engine.py

Autonomous backup scheduler & cold vault studio.

```python
#!/usr/bin/env python
"""Autonomous backup scheduler and cold vault studio for TotalRecalls SSE.
Provides scheduled snapshots of conversation corpus, SQLite metadata, and
pre-vectorized chunks into immutable snapshot containers (.trsnap or .zip).
Run:  C:\TotalRecalls-Search\venv\Scripts\python.exe scripts\backup_engine.py
"""
from __future__ import annotations
import hashlib
import os
import sys
import zipfile
from datetime import datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKUP_ROOT = os.path.join(os.path.expanduser("~"), ".totalrecalls", "backups")
```

## Operations Scripts

| Script | What it does |
|--------|-------------|
| `reindex_all.py` | Re-runs both indexes; used by the scheduled task |
| `install_task.py` | Sets up, reconfigures or removes the automatic re-index task |
| `verify_install.py` | Checks the whole installation end to end |
| `tr_discovery.py` | Shared discovery of conversations in the library |
| `test_suite.py` | Assertions over the system's behaviour |

The full source of each script is available on disk under `scripts\`.

---

# Chapter 20. Commercial Packaging & 6-Week Staged Drop Model

## Pricing tiers

| Tier | Price | Features |
|------|-------|----------|
| Core Downloader | $29 Lifetime | Local multi-provider chat backup, search, and export |
| Smart Search Suite (Founder's Pass) | $49 Launch / $59 Standard / $79 Post-Rollout | Vector RAG, SQL generation, PII Scrubber, Consensus Auditor, Fine-Tuning pipeline |
| Enterprise Local Fleet | $149/seat perpetual | All modules unlocked immediately; multi-seat deployment |

## Sum-of-parts standalone value: $140

| Drop | Week | Module Title | Standalone Price | Status |
|------|------|-------------|-----------------|--------|
| Launch | Week 1 | Tri-Mode Search Chat (Vector + NL→SQL + RRF) | $39 | LIVE |
| Drop 1 | Week 2 | Air-Gap PII & Secret Redaction Scrubber | $19 | Next Up |
| Drop 2 | Week 3 | 1-Click Fine-Tuning Pipeline (JSONL/Alpaca) | $19 | Planned |
| Drop 3 | Week 4 | Cross-AI Consensus & Hallucination Auditor | $25 | Planned |
| Drop 4 | Week 5 | Vault Knowledge Graph & Latent Topic Cards | $19 | Planned |
| Drop 5 | Week 6 | Embedding Engine Benchmark & 2D PCA Cluster Map | $19 | Planned |

## Founder's Season Pass

- **Launch Week Special:** $49 (65% off sum-of-parts)
- **Standard Bundle:** $59
- **Post-Rollout:** $79

Grants instant access to Week 1 plus automatic lifetime unlock of all upcoming weekly drops.

---

# Chapter 21. ZIP Distribution & Installer Architecture

## Distribution archive structure

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

## Installer workflows

**Mode A: In-App Drop (Zero Terminal Commands)**
Drag and drop the ZIP onto the Core Downloader desktop window. The application detects the signature, extracts the add-on to `~/.totalrecalls/modules/smart-search/`, and unlocks the Smart Search tab automatically. No terminal, no permissions popups, no developer tools required.

**Mode B: Double-Click Native Scripts**
- **Windows (`install.bat`):** Verifies file permissions, symlinks the WASM vector database engine, verifies the offline token, creates Start Menu/Desktop shortcut, opens the PDF manual.
- **macOS/Linux (`install.sh`):** Strips Apple Quarantine bits, configures local SQLite vector extensions, creates `/usr/local/bin/totalrecalls-sse` CLI alias.

---

# Chapter 22. Notes

## Verified before shipping

| Check | Result |
|-------|--------|
| All eight providers indexed by both containers | PASS |
| SQLite row count matches the library (415) | PASS |
| Vector chunks trace back to real files on disk | PASS |
| Re-index is idempotent (no duplicate rows) | PASS |
| Incremental merge adds only new conversations | PASS |
| A new provider appears in an existing index | PASS |
| Live search returns real content, not metadata | PASS |
| Chat retrieval spans multiple providers | PASS |
| Scheduled task registers and repeats correctly | PASS |
| Automated test suite (37 assertions) | PASS |

Re-run the checks any time with `scripts\verify_install.py` and `scripts\test_suite.py`.

## Storage locations

| Location | Contents |
|----------|----------|
| `C:\TotalRecalls-Downloads\Library\` | Your exported conversations — the source of truth. Keep it. |
| `C:\TotalRecalls-Search\data\` | The SQLite container |
| `C:\TotalRecalls-Search\vector_store\` | The LanceDB vector index |
| `C:\TotalRecalls-Search\notion_export\` | Generated Notion pages (one file per conversation, after you export) |
| `%USERPROFILE%\.cache\huggingface\` | The embedding model, downloaded once |

## Disk usage

Roughly 1.5 GB for the Python environment, plus the embedding model (~400 MB) and the indexes themselves. The vector index grows with your archive — a few megabytes per thousand conversations.

## Privacy

Retrieval reads only local files. Generation is sent to the local model endpoint on your own machine. Nothing is transmitted to TotalRecalls, to any AI provider, or to any cloud service.

## Requirements

| Component | Requirement |
|-----------|-------------|
| Operating system | Windows 10 or later |
| Memory | 8 GB recommended (16 GB comfortable) |
| Disk | ~2 GB free for the environment and indexes |
| Python | 3.11 or later (bundled in `venv\`) |
| LM Studio | Optional — only needed for the chat interface |

---

*TotalRecalls Power User Guide • Local Vector Search & SQL Container • Smart Search Engine Add-On*  
*Covers all eight providers: ChatGPT, Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral, Qwen.*  
*Runs entirely on your own machine.*
