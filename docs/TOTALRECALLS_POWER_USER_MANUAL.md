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

TotalRecalls Downloader exports one folder per conversation into your Windows user profile:

```text
C:\Users\<YourUsername>\TotalRecalls-download\Library\
  └── chatgpt\
      └── Home\
          └── 2023-07-30 20-52 -- PineScript Help Offered -- a05b4514\
              ├── conversation.json    <- canonical record (schema_version 1)
              └── conversation.md      <- human-readable render of the same conversation
```

`conversation.json` carries `provider`, `account`, and `conversation{id,title,created_at,updated_at,folder,messages[]}`; every message has `role`, `content_md`, `created_at`, `model`, `citations`. The same shape is used for all eight providers.

**SSE does not watch or auto-index this folder.** You point it at the Library once, and it builds an index:

| Stage | Behaviour |
| --- | --- |
| Connect | Folder picker (`<input webkitdirectory>`), or `showDirectoryPicker()` where the API exists |
| Parse | One conversation per `conversation.json`; the sibling `conversation.md` is skipped, so nothing is counted twice |
| Index | One vector chunk per message, built in-page |
| Persist | Conversations + metadata in IndexedDB (`tr-sse-library`), so the folder is picked once per install |
| Refresh | **Re-scan folder…** after new downloads; **Forget library** clears the stored index |

Edge cases handled by the loader: conversations whose `id` is empty (some Qwen exports) fall back to the folder slug; duplicate ids are suffixed so chunk keys never collide; a folder with only a `.md` is still read as a single-turn record.

Measured on a real archive — 930 files, 464 conversations, 9,317 messages, 8 providers — parse takes ~0.5 s, the vector pass a few seconds, and a hybrid query answers in ~200 ms.

**Origin note.** `run-smart-search.bat` opens the app from `file://`. On an opaque `file://` origin `showDirectoryPicker()` is not always exposed, so the folder input is the primary path and the **Remember folder** button appears only where the API exists.

Results reference the *conversation*, not a file path on disk: open it in **Chat Explorer**, or open its folder from Windows Explorer.

---

## 6. Privacy & Zero-Egress Contract

Smart Search Engine runs 100% locally on your PC:
* **Zero Telemetry:** No analytics, no tracking pixels, no telemetry pings.
* **Zero Cloud Egress:** Your prompts, search queries, SQL queries, and chat archives never leave your local machine.
* **Offline Independence:** only activation touches the network, once. There are no model weights to download — embeddings are computed in-page from a deterministic hash — so start-up itself needs no connection.

You can audit network traffic using packet inspection tools like Wireshark or `tshark`:
```bash
tshark -i any -f "not port 53 and not arp" -Y "http or tls"
```
No chat content or queries are transmitted over network adapters during search, SQL compilation, or data export.

---

## 7. Licence & Entitlement Model

SSE is a separate SKU from Downloader Pro and is gated on its own key.

| Capability | Unlicensed | Licensed |
| --- | --- | --- |
| Import your Library | Blocked | Enabled |
| Search over your own archive | Blocked | Enabled |
| Five bundled sample chats | Available (**Demo mode**) | Available until you connect a Library |

* **Key format:** `SSE-XXXXXXXX-XXXX-XXXX`. A `PRO-…` key is rejected with a specific message rather than a generic failure, so support can triage in one step.
* **Verification:** `POST https://totalrecalls.app/api/licenses/verify` with `{license_key, instance_name, product:"sse"}`. The `product` field is what separates the two SKUs server-side; an SSE key sent as `pro` comes back `wrong_product`.
* **Cached entitlement:** held in `localStorage` under `tr-sse-license`. Revalidation is attempted at most once an hour and revokes **only** on an explicit `valid:false`; an unreachable server leaves the cached licence intact, so an activated copy keeps working offline indefinitely.
* **Gate placement:** both the UI (no Connect control — an "Activate SSE key" button instead) and the handlers are gated. `ingestLibrary` and the folder picker refuse and open the activation panel, so a scripted `change` event cannot bypass the button state.
* **Index and licence are independent:** revoking or deactivating drops the app to Demo mode and the stored index is left untouched. Re-activating restores it immediately, with no re-scan and no re-download.
* **Devices:** three activations per key. **Deactivate (free slot)** releases this machine; if the server cannot be reached the local licence is still removed and the slot can be freed later.
* **No local reset:** earlier builds shipped a "Reset local state" helper. It has been removed — `Deactivate` is the only way to remove a licence, and it also frees the slot.

---
*TotalRecalls Engineering Manual • totalrecalls.app*