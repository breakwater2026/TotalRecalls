# Archive Manifest

Everything in this folder is **superseded, duplicated, incomplete or historical**.
It is kept so nothing is lost and so the curation decisions are auditable.
**Do not work from here.** The source folder was not modified — the originals still live at
`Marketing/Market Launch Plans/`. Most also exist in `Marketing/Jasper/YouTube/`, which is a
strict subset of the source (487 of 555 files, byte-identical where they overlap).

Archived documents: **20** · Kept documents: **77**

---

## Archived documents

| File in this archive | Original path | Why archived |
| --- | --- | --- |
| `Backup Library Blog 5 (duplicate of B5, less complete).md` | `YouTube/Blog/Backup Library Blog 5.md` | Same topic as B5; the kept B5 is more complete. |
| `Facebook Posts - all variants (superseded, no UTM).md` | `Social media/facebook/Facebook Posts — all variants.md` | Superseded by the 4-week pack; no UTM tags; free-tier wording risk. |
| `Fragment - Day 0 Launch Announcement.md` | `Social media/Social Media Campaign.md` | Single-day fragment, pre-dates the 4-week pack. |
| `Fragment - Day 10 How It Works.md` | `Social media/Untitled Document (1).md` | Untitled single-day fragment, pre-dates the 4-week pack. |
| `Fragment - Day 3 Problem With AI Chat History.md` | `Social media/TotalRecalls Social Media Campaign.md` | Single-day fragment, pre-dates the 4-week pack. |
| `Implementation Content Pack (subset of the PDF).docx` | `TotalRecalls_Implementation_Content_Pack.docx` | Strict subset of Launch Content Pack (2026-10-24).pdf; no unique content. |
| `Instagram Captions - all variants (superseded, no UTM).md` | `Social media/instagram/Instagram Captions — all variants.md` | Superseded by the 4-week pack; no UTM tags; no disclosure. |
| `LinkedIn Posts - all variants (superseded, no UTM).md` | `Social media/linkedin/LinkedIn Posts — all variants.md` | Superseded by the 4-week pack; no UTM tags. |
| `Main Explainer Video - Outline & Shot List (superseded).md` | `YouTube/Main Explainer Video — Outline & Shot List.md` | Superseded by the Launch Plan flagship script and Strategy production rules. |
| `Night Worklist 2026-10-01 (historical).md` | `YouTube/NIGHT_WORKLIST.md` | One-night completion log; all items done. Historical record only. |
| `Short-Form Video Strategy (superseded).md` | `YouTube/Short-Form Video Strategy.md` | Superseded by Strategy section 3 (Shorts) and the Launch Plan; script content overlaps Main Explainer. |
| `Thumbnail Concepts (superseded by Channel Style sec.4).md` | `YouTube/Thumbnail Concepts.md` | Superseded by the Channel Style thumbnail design system. |
| `TotalRecalls Hook Rankings Guide (incomplete).md` | `YouTube/TotalRecalls Hook Rankings Guide.md` | Only 2 of 10 scorecards filled; hook text already merged into the scripts. |
| `TotalRecalls Master Plan V2 (superseded by V3, truncated).md` | `YouTube/TotalRecalls Master Plan V2.md` | Superseded by Master Implementation Plan V3; also truncated mid-word. |
| `X (Twitter) Posts - all variants (superseded, no UTM).md` | `Social media/x/X (Twitter) Posts — all variants.md` | Superseded by the 4-week pack; no UTM tags; no disclosure. |
| `YT Video 3 Script (truncated stub, superseded by V2).md` | `YouTube/scripts/YT Video 3 Script.md` | 228-word stub ending mid-sentence; superseded by V2 (2,982 words). |
| `YouTube Channel Description (superseded by Upload Pack).md` | `YouTube/YouTube Channel Description.md` | Gen-A channel bio; the Nov Upload Pack carries the current bio. |
| `YouTube Content Plan - First 10 Videos (Jasper gen, superseded).md` | `YouTube/YouTube Content Plan — First 10 Videos.md` | Gen-A lineup; superseded by Strategy V5 and the Nov Launch Plan. |
| `YouTube Playlist Structure - 2 frameworks (superseded by Strategy sec.4).md` | `YouTube/YouTube Playlist Structure — 2 frameworks.md` | Superseded by Strategy section 4 playlist structure. |
| `YouTube Upload Checklist & Template (superseded).md` | `YouTube/YouTube Upload Checklist & Template.md` | Superseded by Strategy + Description Templates + Upload Pack. |

---

## Excluded entirely (not carried into the curated folder at all)

| What | Why |
| --- | --- |
| YouTube/hooks/*.md (10 files) | Strict subsets of the matching script's 'Alternative Hooks' section - containment 1.00, zero unique lines. Content already lives in 03_YouTube/Scripts/. |
| 24 .docx files that have an .md twin | Content-equivalent Word conversions: 19 are byte-identical after whitespace normalisation, 5 have identical token sets (Jaccard 1.000) with minor table/formatting extraction differences. Convention recorded in the Master Plan: .md = working source, .docx = regenerable human copy. |
| YouTube/frames/ (33 JPGs, 12 MB) and YouTube/frames_convergence/ (360 PNGs, 17 MB) | Intermediate render frames, not deliverables. |
| YouTube/videos/ (10 MP4s, 88 MB + encode logs) | Superseded 2026-10-01 placeholder cuts, already uploaded private to YouTube and slated for deletion. Current masters live in demo-shoot/renders/ per the shoot handoff. |
| YouTube/__pycache__/ | Bytecode cache. |
| YouTube/frames_conv_test_*.png (3) | Intermediate convergence test frames. |
| YouTube/yt-api/api_key.txt, credentials.json, token.json, capture_in.txt, capture_out.txt, oauth_run.log | LIVE SECRETS - Google API key, OAuth client secret, refresh token and a one-time auth code. Deliberately not carried over. Rotate/re-issue before any reuse. |
| YouTube/yt-api/*.json, *.log (channel/playlist/upload state) | Stale October channel state (video IDs of uploads slated for deletion). Scripts are kept; state files are not. |
| YouTube/TotalRecalls YouTube Launch Plan.pdf | Content-identical PDF twin of the .md/.docx Launch Plan (unique-token Jaccard 1.000). Only the .md was carried. |
| YouTube/yt-api/capture_err.txt | Empty file (0 bytes). |
| YouTube/yt-api/exchange_once.py | Hardcodes a live Google OAuth authorization code in a string literal (AUTH_RESPONSE). Quarantined with the other credentials; the auth code is one-time and already consumed, but the script must not be carried into a curated set. |

---

## Verification method

- **Exact duplicates** — SHA-256 of normalised text (whitespace-collapsed, lower-cased).
- **Near-duplicates** — token Jaccard + containment (intersection over the smaller set).
- **Subset claims (hooks)** — containment 1.00 with zero unique lines, confirmed by reading.
- **Truncation** — file tails inspected directly; a file counts as truncated only if it ends
  mid-word or mid-table-row, not merely without terminal punctuation.
- **Secrets** — regex sweep for `GOCSPX-`, `ya29.`, `AIzaSy`, `refresh_token`, `client_secret`,
  `Bearer`, and assigned key literals.

Per-file origin path and SHA-256 prefix: `_build_records.json` in the folder root.
