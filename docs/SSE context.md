I'll need to understand the current structure before planning. Let me explore the downloader code and the module layout in parallel.

Let me examine the key integration files — the downloader UI, the module's types/constants, and how conversations flow between them.

Let me look at the downloader's save logic and the module's App.tsx to understand the data flow and current entry point.

Let me check the existing DeliveryPackagingStudio component (already handles .ZIP packaging) and the app.py downloader backend to leverage existing work.

I have enough context to present a concrete implementation plan. Here's the design:

Implementation Plan: Wire Smart Search Engine + TotalRecalls Downloader into a Live-Test ZIP
Current state (verified)
Module at TotalRecalls-Source Code/Modules/smart-search-engine/ — standalone React 19 + TS SPA. App.tsx seeds conversations from INITIAL_CONVERSATIONS (hardcoded seed data in constants.ts), builds a vector index via buildVectorIndex(conversations, 384). Integrity suite: 14/14 passing.
Downloader at repo root (app_ui.html + app.py + totalrecalls/ package) — downloads AI chat conversations from providers and saves them to C:/Users/<user>/TotalRecalls-downloads/Library/<provider>/home/ as Markdown + JSON via totalrecalls.core.export_fs.write_conversation_markdown.
Shared contract: ChatConversation type in types.ts (id, title, provider, model, messages[], etc.). The downloader's output schema needs to be confirmed as compatible.
Packaging exists only as UI simulation: DeliveryPackagingStudio.tsx describes .ZIP contents but doesn't create one. No real zip build script exists yet.
Plan (ordered by dependency)
Phase 1 — Discover & align data formats (no code changes yet)

Inspect a sample of downloader output: read one JSON file under TotalRecalls-downloads/Library/<provider>/home/ to learn its schema.
Map downloader fields → ChatConversation fields (title, provider, model, messages[], timestamps, tokenCount). Identify any mismatches (e.g. downloader stores created_at vs. createdAt).
If mismatched, write a small adapter/normalizer; if compatible, proceed.
Phase 2 — Add a downloaded-conversation loader to the module

New file Modules/smart-search-engine/Services/downloadedConversations.ts exporting loadDownloadedConversations(downloadRoot?: string): Promise<ChatConversation[]>.
It reads TotalRecalls-downloads/Library/*/home/ recursively, parses each conversation JSON, normalizes via the Phase 1 adapter, returns ChatConversation[].
Graceful fallback: if folder missing/empty, return [] (don't crash the live test).
Phase 3 — Wire App.tsx to prefer real downloaded data

Edit App.tsx: replace useState<ChatConversation[]>(INITIAL_CONVERSATIONS) with an async initializer that calls loadDownloadedConversations() and falls back to INITIAL_CONVERSATIONS when nothing downloaded yet.
Rebuild chunks via buildVectorIndex(loadedConversations, 384) once loaded.
Keep handleAddNewMockChat unchanged.
Phase 4 — Create a unified ZIP launcher

New top-level Modules/smart-search-engine/live-test.html (or a small launcher HTML) that iframes or links both: (a) the downloader (app_ui.html) and (b) the search engine (index.html), so a tester can download conversations then immediately search them in one browser session.
Alternatively: keep them as two entry points in the zip with a README.live-test.md explaining the order (download first, then open search).
Phase 5 — Build the ZIP

New build script scripts/zip-live-test.mjs (Node, no external deps beyond built-in zlib/fs or a tiny zip package) that packages:
Modules/smart-search-engine/ (full module, minus node_modules — regenerate via npm install after unzip, OR include node_modules to make it truly air-gap/zero-friction)
app_ui.html + app.py + totalrecalls/ package (downloader)
live-test.html launcher + README.live-test.md
Output: TotalRecalls-LiveTest-<date>.zip at repo root.
Include a SHA-256 checksum file (checksums.sha256) — consistent with the module's downside-protection theme and the existing manifest pattern.
Phase 6 — Live test on a clean machine

Unzip to a fresh folder.
Run the downloader (app_ui.html or python app.py) against a provider to populate real conversations.
Open the search module (index.html), confirm real downloaded conversations appear (not just seed data), run search/RAG/SQL.
Re-run npm run integrity:test from the module folder inside the zip — expect 14/14 passing against real data.
Ordering rationale
Data-format discovery (Phase 1) must come first because the loader and App wiring depend on the downloader's actual output schema. The loader (Phase 2) must precede App wiring (Phase 3). The ZIP (Phase 5) bundles the wired module + downloader, and the live test (Phase 6) validates end-to-end. Copy-first/delete-later (per the js-project-restructuring skill) applies if we relocate anything — avoid mv on Windows due to file-lock "Device or resource busy" errors.

What I need from you before starting
Confirm the downloader output folder path on this machine (C:/Users/break/TotalRecalls-downloads/Library/...) and whether there's already sample downloaded data to inspect.
Confirm whether to include node_modules in the zip (bigger, zero-friction) or exclude it and require npm install after unzip.
Confirm you want me to proceed with Phase 1 (inspect downloader output schema) — I'll stop there and report findings before writing code.
