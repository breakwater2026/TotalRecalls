# smart-search-engine — Document Curation

Applied `document-corpus-curation` to the document layer of
`Modules/smart-search-engine` on 2026-11-15. **The source folder was not modified.**

Scope note: "main folder" was read as `Modules/smart-search-engine`. Say the word if you meant the
repo root or `Modules/` instead and I will redo it at that scope.

---

## ⚠ Task 1 is blocked — and the reason matters

The task was *"update the SSE PDF guide for the latest version."* **The attached PDF cannot be
updated, because it documents a product that no longer exists.** It is not a few turns behind; it is
a different architecture.

| | The PDF (2026-10-27) | The app in this repo (2026-11-12) |
| --- | --- | --- |
| Form | 44-page CLI/container guide | React 19 SPA (`App.tsx`, 16 components) |
| Stack | Python, `venv`, `scripts\build_sql_container.py` | TypeScript, `ragEngine.ts`, `licensing.ts` |
| Vector | real `sentence-transformers/all-MiniLM-L6-v2`, LanceDB | `generateLocalPseudoEmbedding()` — a **word-hash pseudo-embedding** |
| Keywords | real BM25 | `calculateBM25Score()` — commented *"BM25 … simulator"* |
| SQL | real SQLite | `executeLocalSQL()` — `if (sql.includes('group by provider'))` pattern branches |
| Data | the user's real Library | `INITIAL_CONVERSATIONS` — **5 hardcoded mock chats** |
| Cloud | none | `naturalLanguageToSQL()` / `executeHybridRAG()` call **Gemini in the cloud** |

**Two consequences:**

1. **Re-rendering the current manual would shrink the guide from 44 pages to about 4** — the current
   source (`POWER_USER_MANUAL_MARKDOWN` in `Services/manualExporters.ts`) is ~120 lines.
2. **Writing a new guide from this code would mean documenting a simulator as a real engine.** The
   app's own comments say *pseudo*-embedding and *simulator*, and it calls `gemini-2.5-flash` over the
   network — which contradicts the site's *"Zero Cloud Egress"* and the manual's *"100% Local PC
   Runtime"*. Marketing copy that says otherwise would breach the claims register we just curated.

**So I have not written the guide.** Which one is the shipping product?

- If the **real** SSE is a build artefact produced elsewhere (a packaged installer, or a different
  branch/repo), point me at it and I will write the guide from that.
- If this repo **is** the product, then the honest guide describes what it does today, and the gap
  between the code and the live site's claims is a separate problem to fix first.

---

## Findings (all measured)

| # | Finding | Evidence |
| --- | --- | --- |
| 1 | The PDF is the **retired Python-CLI edition** | 44 pp; documents `build_sql_container.py`, `venv\Scripts\python.exe`, LanceDB, LM Studio `:8000` |
| 2 | The same PDF exists in **4 places**, byte-identical | `docs/`, `Marketing/Plans/`, `Marketing/User Guides/`, `Modules/smart-search-engine/` — SHA-256 `636cb748…` |
| 3 | The engine layer is a **simulator** | `ragEngine.ts:6` `generateLocalPseudoEmbedding`; `:55` `calculateBM25Score` ("simulator"); `:140` `executeLocalSQL` (pattern branches) |
| 4 | **Cloud egress exists** in the NL→SQL path | `ragEngine.ts:256` and `:317` construct `GoogleGenAI` and call `gemini-2.5-flash` |
| 5 | Data is **mock**, not the user's Library | `constants.ts:3` `INITIAL_CONVERSATIONS`; `App.tsx:86` `handleAddNewMockChat` |
| 6 | **Version drift** | Navbar badge `SSE v1.0` · app manual `v2.5.0-MarketLeader` · `docs/TOTALRECALLS_POWER_USER_MANUAL.md` `v1.0.0-MarketLeader` |
| 7 | **Price drift** | Live site: bundle **$49** (regular $98) · app manual: **$49.89** (regular $99.89) |
| 8 | `metadata.json` claims **PDF manuals**; the code exports only `.md` + `.docx` | `Services/manualExporters.ts` — `downloadManualMarkdown`, `downloadManualWordDocx`; no PDF path |
| 9 | `README.pdf` is a **render** of `README-SSE.md` | containment 1.00, Jaccard 0.99 |
| 10 | `dist/tailwind.min.js` is **0 bytes** | build output, 2026-11-12 14:15 — a build defect at source |
| 11 | `OverviewHub` / `PowerUserManual` say **"Across 5 AI providers"** | the product has 8 — stale copy in the UI |

---

## Wiring defects (verified 2026-11-15)

These are code facts, checked directly, not inferences:

| # | Defect | Evidence |
| --- | --- | --- |
| W1 | **5 of the 16 panes are unreachable.** Knowledge Graph's nav button sets `knowledgeGraph` but `App.tsx` tests `'knowledge'`; and nothing sets `'scrubber'`, `'benchmarks'`, `'demoScript'` or `'specs'`. | `App.tsx:303` vs `Navbar.tsx:23,52`; no setter for the other four |
| W2 | **The "User Guide" tab shows no manual.** `PowerUserManual.tsx` never imports `manualExporters` — it renders a near-duplicate of OverviewHub. The actual manual text (`POWER_USER_MANUAL_MARKDOWN` / `LAYMAN_USER_MANUAL_MARKDOWN`) is not shown anywhere in the UI. | `grep` for `manualExporters` in `PowerUserManual.tsx` → no match |
| W3 | **The cloud path is real and shipped**, but cannot authenticate. `ragEngine.ts:256,317` call `new GoogleGenAI({ apiKey: process.env.API_KEY })`; the built bundle still contains `process.env.API_KEY` twice plus 82 GenAI SDK references. In a browser `process.env.API_KEY` is undefined, so the call throws and falls through to the local template fallback. **If a key were injected at build time, NL→SQL answers and hybrid answers would leave the machine.** |
| W4 | The integrity suite claims **12** tests; `TEST_DEFINITIONS` holds **14**. | `constants.ts` / `Services/testRunner.ts` |
| W5 | `JWT_SECRET` and `CREDIT_CARD` regexes are defined but never applied in `scrubText`. | `Services/datasetExporters.ts` |
| W6 | "Obsidian and Notion connections" is claimed in `WebsitePresentation`, `SpecsAndPricing` and `constants.ts`; no code in this module reads or writes either. | repo-wide grep |
| W7 | Cross-tab "open this conversation" links do nothing: `App.tsx` passes `initialSelectedId`, but `ChatExplorer` declares `selectedConvId`. | `App.tsx:314`, `ChatExplorer.tsx` props |
| W8 | `SpecsAndPricing` lists the PII Scrubber, Consensus Auditor, Knowledge Graph and Embedding Benchmark as **paid upgrades not included**, yet all four are implemented in this build. | `constants.ts` `SSE_PAID_UPGRADES` |

---

## What is in this folder

```
01_Current/   README-SSE.md (canonical) · README.pdf (its render) · metadata.json · package.json
99_Archive/   the retired Python-CLI edition of the Power User Guide + MANIFEST.md
```

Not carried, and why — see `99_Archive/MANIFEST.md`:
`node_modules/` (134 MB, gitignored, regenerable) · `dist/` (build output, regenerable) ·
`package-lock.json` (regenerable) · the TS/TSX source tree (the *subject* of the guide, not documents).

---

## To finish Task 1, I need one of these

1. **The real product.** A path to the shipping SSE build/installer, or confirmation of which repo and
   branch is authoritative — I will write and render the guide from it.
2. **Permission to document the prototype honestly.** Then the guide says what the app does today
   (a local SPA with a simulated index and an optional cloud NL→SQL step), and the site's claims get
   flagged as unmatched.
3. **Permission to write the guide from the live site + current manual only.** Faithful to today's
   public claims, but it would describe behaviour the code in this repo does not implement.

---

## Verification

- Coverage: 6 source documents → 4 kept, 1 archived, 1 accounted as a render twin; 0 unaccounted.
- Secret sweep (whole tree, incl. `.log` and extensionless): **0 hits**.
- Source integrity: **0 files altered** (per-file SHA-256 in `_build_records.json`).
- Report: `99_Archive/MANIFEST.md`.
