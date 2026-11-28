# Archive Manifest — smart-search-engine document curation

Source: `Modules/smart-search-engine/` · Curated 2026-11-15 · **source folder unmodified**

Archived: **1** · Kept: **4** · Excluded classes: **6**

---

## Archived

| File | Original path | Why |
| --- | --- | --- |
| `TotalRecalls-Power-User-Guide (retired Python-CLI edition 2026-10-27).pdf` | `TotalRecalls-Power-User-Guide.pdf` | Documents a **retired architecture**: a Python CLI/container package (`scripts\build_sql_container.py`, `venv\Scripts\python.exe`, LanceDB, `sentence-transformers`, LM Studio on port 8000). The current product is a React SPA. Keeping it beside the current docs is how someone ships the wrong guide. <br>Also exists byte-identically at `docs/`, `Marketing/Plans/` and `Marketing/User Guides/` (SHA-256 `636cb748369c8913…`) — those copies are **not** carried here. |

---

## Excluded entirely

| What | Why |
| --- | --- |
| `node_modules/` (134 MB) | Dependency tree; already in `.gitignore`; regenerable. Not content. |
| `dist/` (`bundle.js` 3.1 MB, `tailwind.css`, `tailwind.min.js`) | Build output, regenerable. Note: `tailwind.min.js` is **0 bytes** — a build defect to fix at source, not a document. |
| `package-lock.json` (51 KB) | Regenerable lockfile, not a document. |
| `Components/`, `Services/`, `scripts/` (TS/TSX) | Product source — the *subject* of the guide, not part of the document corpus. |
| `App.tsx`, `index.tsx`, `index.html`, `input.css`, `constants.ts`, `types.ts`, `run-smart-search.bat` | Application shell and source. |
| The retired PDF's 3 other copies (`docs/`, `Marketing/Plans/`, `Marketing/User Guides/`) | Byte-identical duplicates (same SHA-256). Needs a canonical-location decision before any of them is updated. |

---

## Verification method

- **Twin detection** — `README.pdf` vs `README-SSE.md`: containment 1.00, Jaccard 0.99, tails
  identical. Treated as source + render, both kept and labelled.
- **Retired-edition detection** — extracted the PDF text (`pdftotext -layout`, 10,011 words) and
  compared its architecture terms against the source tree: `venv`/`build_sql_container`/`LanceDB`
  appear only in the PDF; `ragEngine.ts`/`licensing.ts`/`App.tsx` appear only in the code.
- **Simulator detection** — read `Services/ragEngine.ts` directly: function names and comments
  (`generateLocalPseudoEmbedding`, *"BM25 … simulator"*, `executeLocalSQL` over in-memory arrays).
- **Cloud-egress detection** — `new GoogleGenAI(...)` + `gemini-2.5-flash` at `ragEngine.ts:256`
  and `:317`.
- **Identity** — SHA-256 of all four PDF copies compared.
- **Secrets** — whole-tree sweep including `.log` and extensionless files: no hits.
- **Source integrity** — every copied file re-hashed against its origin after the build.

Per-file origin and SHA-256: `_build_records.json`.
