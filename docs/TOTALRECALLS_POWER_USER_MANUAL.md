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
|   | * Exporters: ChatGPT, Claude,        |   | * Local vector search                |   |
|   |   Perplexity, Gemini, Grok,          |   | * Weighted BM25 + vector retrieval   |   |
|   |   DeepSeek, Mistral, Qwen            |   | * Natural Language to SQLite         |   |
|   | * Formats: Markdown (.md), JSON      |   | * Cross-AI Consensus Auditor (planned) | |
|   | * Direct local filesystem storage    |   | * PII & Secret Scrubber (planned)    |   |
|   | * Microsoft Store certified          |   | * Fine-Tuning JSONL Export (planned) |   |
|   | * Zero warnings, one-click install   |   | * Free maintenance updates           |   |
|   +--------------------------------------+   +--------------------------------------+   |
|                       |                                          |                      |
|                       +------------------------------------------+                      |
|                                            |                                            |
|                                            v                                            |
|                      +-------------------------------------------+                      |
|                      | PRIVATE LOCAL DISK RUNTIME                |                      |
|                      | C:\TotalRecalls\Library\                   |                      |
|                      | (Zero telemetry • Zero cloud egress)      |                      |
|                      +-------------------------------------------+                      |
+-----------------------------------------------------------------------------------------+
```

---

## 2. Commercial Packaging & Pricing

TotalRecalls is a one-time purchase with no recurring subscription:

| Product | Launch Price | Regular Price | Notes |
|---|---|---|---|
| **TotalRecalls Free Tier** | **$0** | $0 | ChatGPT, Claude and Perplexity; five conversations per provider. Same app, no account, no time limit. |
| **TotalRecalls Downloader Pro** | **$24** | $48 | One-time. All 8 providers, unlimited downloads. Available on Microsoft Store (free trial) with in-app Pro key activation. |
| **Smart Search Engine (SSE) Add-On** | **$29** | $58 | One-time. Requires Pro. Indexes all saved Markdown & JSON files. |
| **Pro + SSE Bundle** | **$49** | $98 | One-time. Downloader Pro + SSE Add-On in a single discounted checkout. |

- **License Scope:** Each license key covers up to **3 personal PC activations**.
- **Updates vs. Upgrades:** Maintenance updates and provider-compatibility bug fixes within v1 are free for the life of the product.
- **Refunds:** Downloader Pro is non-refundable — the Free Tier is the try-before-you-buy mechanism. The Smart Search Engine (SSE) add-on carries a 7-day, no-questions-asked refund. An approved refund deactivates the key and frees the slot. See `/legals/#refund`.
- **One build, one installer:** the Microsoft Store app is the same binary for everyone. It starts in the Free Tier; a `TR-…` key entered in **Settings → Licence** unlocks all eight providers and unlimited downloads. There is no separate "Pro download".
- **Where the Free Tier stops:** three providers (ChatGPT, Claude, Perplexity) and five conversations per provider, enforced when conversations are selected and again at export. The ledger lives in the app's own data folder, so editing the UI cannot lift the cap.

---

## 3. Relational Schema Architecture (SQLite)

SSE models your library as three logical tables and answers read-only SQL over them. The shipped v1.0.0 build holds them in memory and persists the parsed index in IndexedDB, rather than in an on-disk SQLite file; the schema below documents the shape the query engine exposes.

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

> The shipped build does not create a `vec0` virtual table or an HNSW index. The vector column describes the logical shape; scoring is a linear cosine scan over an in-memory array (see §4).

---

## 4. Hybrid Retrieval (BM25 + Vector)

Combines BM25 token frequencies with cosine similarity over a deterministic 384-dimension hash embedder (`generateLocalPseudoEmbedding`). The shipped build uses a weighted blend, not rank fusion:

```text
score = 0.6 × cosine(query, chunk) + 0.4 × BM25(query, chunk)
```

There are no model weights to download or load. Because the vector is a normalised frequency hash rather than a trained transformer embedding, it captures lexical overlap and word co-occurrence; keyword precision is strong, while purely conceptual recall is weaker than a `bge`-class model would give. The results are sorted by that blended score and the top *k* are returned.

---

## 5. Local Filesystem Integration

TotalRecalls Downloader exports one folder per conversation into your local Library. The default root is `C:\TotalRecalls\Library`; if Windows does not allow writing to the drive root, the app falls back to `%USERPROFILE%\TotalRecalls\Library` (and keeps an existing `TotalRecalls-download` folder in use so no archive is orphaned):

```text
C:\TotalRecalls\Library\
  └── chatgpt\
      └── Home\
          └── 2023-07-30 20-52 -- PineScript Help Offered -- a05b4514\
              ├── conversation.json    <- canonical record (schema_version 1)
              └── conversation.md      <- human-readable render of the same conversation
```

Conversations filed in a provider Space are written under `Spaces\<Space name>\` instead of `Home\`.

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

## 8. Diagnostics & Support Playbook

**Reproducing the shipped artifact.** `python tools/package_sse.py` rebuilds `dist/bundle.js` with esbuild, regenerates the PDFs through headless Edge, and re-zips `site/public/downloads/`, printing the bundle size and SHA-256 it just produced. A rebuild from a clean HEAD must be byte-identical to the shipped bundle: compare the printed values with the artifact you deploy. Do not hardcode those values here — the in-app manual is itself compiled into `bundle.js` (`--loader:.md=text`), so any edit to this file changes the bundle hash. The packager calls the PDF builder with `sys.executable` — calling it with bare `python` resolves to whichever interpreter is first on `PATH` and fails on a missing module.

**Inspecting the live index.** DevTools → *Application* → *IndexedDB* → `tr-sse-library` → store `index` → key `current`. `value.meta` records `conversationCount`, `messageCount`, `providerCount`, `filesSeen`, `skipped` and `indexedAt`. Only conversations and metadata are stored; vectors are rebuilt at launch by the deterministic hash embedder, so there are no model weights on disk and nothing to corrupt.

**Expected counts.** `filesSeen` will be roughly twice `conversationCount` because each conversation is written as `conversation.json` + `conversation.md`; the `.md` is skipped when its sibling JSON parses. A non-zero `skipped` with an empty `skippedReasons` list is normal for non-`.json`/`.md` files. Some Qwen exports carry an empty `id`; those fall back to the folder slug, and genuine duplicates are suffixed so chunk keys stay unique.

**Licence state.** `localStorage['tr-sse-license']` holds `{sse, key, instance_id, activated_at, last_validated_at}`. Revalidation runs at most every 3600 s and revokes **only** on an explicit `valid:false`; a network failure leaves the cached licence intact. Server-side, the `product` field selects the SKU: an `SSE-` key sent with `product:"pro"` returns `wrong_product`, which is the fastest way to tell a key/SKU mismatch from a bad key.

**When a paying customer reports being blocked.** Check in this order: (1) `valid:false` with no `error` means the key is unknown or inactive; (2) `wrong_product` means the client sent the wrong SKU or the key belongs to the other product; (3) `activation_limit_reached` means three devices are already registered — have them run **Deactivate (free slot)** on an old machine; (4) entitlement revoked while offline cannot happen by design, so an offline block is a client bug, not policy.

**Origin matrix.** `run-smart-search.bat` opens `file://`. On an opaque `file://` origin `showDirectoryPicker()` is absent in some Chromium builds (no secure context), while `<input webkitdirectory>` is always available — hence the layered design: the folder input is the guaranteed path, the picker only appears where the API exists. Serve the app over `http://localhost` and both work.

---
*TotalRecalls Engineering Manual • totalrecalls.app*