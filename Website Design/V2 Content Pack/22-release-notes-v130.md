# 22 — "What's New in v1.3.0" Release Notes

**Source:** Thread "Release Notes v1.3.0" (L2915–3015). Curated final copy. Route: `/release-notes/`.

## What's New in v1.3.0

TotalRecalls v1.3.0 is now live. This update improves reliability, expands provider support, and makes exports more predictable across ChatGPT, Claude, Perplexity, Gemini, and Grok.

### New in this release

**✔ Perplexity Exporter (full rewrite)**
- More reliable thread extraction
- Better handling of long research chains
- Cleaner Markdown formatting
- Improved JSON metadata

**✔ Gemini Takeout improvements**
- Faster folder scanning
- Better detection of valid Takeout paths
- More readable Markdown conversion
- Reduced duplicate conversation entries

**✔ Claude Projects enhancements**
- Better long-thread stitching
- Cleaner Markdown output
- More consistent folder naming

**✔ ChatGPT export stability**
- Improved pagination handling
- More predictable JSON structure
- Better fallback behavior when history is large

**✔ Grok export support**
- Initial Grok conversation export
- Markdown + JSON output
- Basic folder structure

### UI & UX improvements
- Cleaner provider selection screen
- More consistent progress messages
- Better error reporting
- Clearer folder-selection prompts
- Reduced "silent failures" during export

### Performance improvements
- Faster exports across all providers
- Reduced memory usage
- More stable long-running exports
- Better handling of large Takeout folders

### Bug fixes
- Fixed rare crash during Perplexity export
- Fixed Gemini JSON parsing edge cases
- Fixed Claude Project naming inconsistencies
- Fixed ChatGPT export stalling on large histories
- Fixed Grok export missing metadata fields

### Known issues
- Windows SmartScreen may warn about unsigned builds
- Surface Smart App Control may block unsigned apps
- Some Gemini Takeout ZIPs contain inconsistent JSON formats
- Perplexity occasionally rate-limits long exports

### Roadmap
Code-signed builds · Semantic search · Obsidian + Notion sync · Multi-assistant timeline · Multi-device memory · RAG containers · Optional cloud sync (opt-in)
