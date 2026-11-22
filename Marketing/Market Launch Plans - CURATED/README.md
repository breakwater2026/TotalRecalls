# TotalRecalls — Market Launch Plans (CURATED)

A cleaned, de-duplicated, generation-ordered rebuild of `Marketing/Market Launch Plans/`.
**The source folder was copied, never modified.** Every file here is a byte-identical copy of a
source file (SHA-256 recorded in `_build_records.json`), renamed and regrouped for clarity.

Curated 2026-11-15.

---

## Why this folder exists

The source folder held **555 files / 122 MB** spanning four months of planning by three different
AI tools (Jasper → Claude/Gemini → later sessions). It contained:

- **Four stacked plan generations** that contradict each other on pricing, free-tier wording,
  channel lineup, and even whether the product is on the Microsoft Store.
- **19 exact `.docx` ↔ `.md` duplicate pairs**, plus 5 more that are token-identical apart from
  table extraction — 24 content-equivalent pairs in all (Word conversions of the same text).
- **10 "alternative hooks" files** that are strict subsets of the scripts they belong to.
- **6 documents truncated mid-sentence** (see the Currency Register).
- **Live Google API credentials** sitting in a marketing folder.
- 88 MB of superseded placeholder video and 47 MB of intermediate render frames.

Nothing was deleted from the source. Everything dropped from *this* folder is listed in
`99_Archive/MANIFEST.md` with the reason, and the source remains intact.

---

## Start here — what to actually use

| If you want to… | Open this | Status |
| --- | --- | --- |
| Know the strategy, claims you may make, 90-day calendar, budget, risks | `01_Strategy_and_Plans/Master Launch Plan (2026-10-23).md` | **Current authority** |
| Decide what to publish on YouTube and in what order | `01_Strategy_and_Plans/YouTube Launch Plan (2026-11-14).md` | **Current** |
| Publish the 8 provider walkthroughs | `03_YouTube/Upload Pack - 8 Provider Walkthroughs (2026-11-15).md` | **Current, copy-paste ready** |
| Post social this week | `05_Social/4-Week Social Pack (2026-11-15).md` | **Current, copy-paste ready** |
| Check a claim before it goes in public copy | Master Launch Plan §0.2 claims register | **Binding** |
| Write a video description | `01_Strategy_and_Plans/YouTube Description Templates (2026-10-02).md` | Current |
| Record a scripted video | `03_YouTube/Scripts/V1…V10` | See register — some stale |
| Publish a blog post | `04_Blog/B2…B9` | See Blog Series Map |
| Design a thumbnail or banner | `01_Strategy_and_Plans/YouTube Channel Style v1 (2026-09-30).md` | Current (truncated) |
| Run the channel week to week | `03_YouTube/Production Runbook (2026-10-03).md` | Current (truncated) |

**Do not work from `99_Archive/`.** It is history, kept so nothing is lost.

---

## Folder guide

```
01_Strategy_and_Plans/   Strategy, channel plan, brand/style, audit, description standard,
                        plus two index docs (Blog Series Map, Document Currency Register)
02_Content_Pack/        The 17-page launch content pack (website copy, SmartScreen guide,
                        provider guide copy, V2-V8 scripts) - one PDF
03_YouTube/             Upload pack, production runbook, and the 10 canonical video scripts
04_Blog/                The 9-post blog series (B2-B9) plus the pricing explainer
05_Social/              Current 4-week pack + the 30-day calendar
06_Founder_Story/       Founder narrative, 2 variants + profile block
07_Assets/              Channel art, 10 thumbnails, QC strips, logo data
08_Tooling/             Build scripts and the YouTube Data API automation (no credentials)
99_Archive/             Superseded, duplicated and incomplete documents + MANIFEST.md
```

---

## The four generations (why so many contradicting plans existed)

| Gen | Dates | Documents | Product reality assumed |
| --- | --- | --- | --- |
| **A** | 2026-09-28 → 09-30 | YouTube Content Plan, Playlist Structure, Thumbnail Concepts, Short-Form Strategy, Main Explainer, Channel Description, Upload Checklist, 10 scripts, hooks, blog drafts, social posts | Pre-launch. $24 Pro, no Microsoft Store, no SSE add-on |
| **B** | 2026-10-01 → 10-03 | Strategy V5, Channel Style, Description Templates, Content Audit V2, Master Plan V2, Master Implementation Plan V3, YouTube Implementation Plan | + 9-post blog series, Option A (no provider spotlights), footer email signup |
| **C** | 2026-10-20 → 10-26 | Master Launch Plan Final, Launch Content Pack (PDF), Implementation Content Pack (docx) | + GA4, Cloudflare traffic baseline, day-number schedule, P1-P15 task graph |
| **D** | 2026-11-14 → 11-15 | YouTube Launch Plan, Upload Pack, 4-Week Social Pack | **Microsoft Store live, SSE add-on, $24 Pro / $49 Pro+SSE, 3-device licence, "5 conversations each"** |

**Gen D is the product as it is today.** Gen A/B/C describe a product that no longer exists in that
form. Where they conflict, Gen D wins — but the Gen C master plan is still the best source for
positioning, the claims register, budget logic and the 90-day calendar, because Gen D does not
restate them.

### The specific contradictions to be aware of

| Topic | Older docs (A/B/C) | Current (D) |
| --- | --- | --- |
| Free tier | "5 conversations per download" (also "per provider" on the old homepage) | ✅ **Resolved 2026-11-15** — 3 providers (ChatGPT, Claude, Perplexity) × 5 conversations each = **15 maximum**, matching the live site. Gen D assets already carry the correct "5 conversations each" wording. |
| Pricing | Pro $24 one-time, launch price | Pro $24; Pro + SSE bundle $49 (regular $98) |
| Distribution | totalrecalls.app download only | Microsoft Store **and** site |
| Add-ons | "not available, do not market" | SSE is live and marketed |
| Channel lineup | 6-video launch set | 2 how-tos → flagship → ownership/Obsidian/SSE/Gemini/backup/pricing |

---

## Removed, and why

Full detail in `99_Archive/MANIFEST.md`. Summary:

- **24 `.docx` files with an `.md` twin** — content-equivalent Word conversions: 19 byte-identical
  after whitespace normalisation, 5 with identical token sets (Jaccard 1.000) apart from table
  extraction. The source convention (recorded in the Master Plan) is ".md = working source, .docx =
  regenerable human copy", so only the `.md` was carried. Two documents that exist *only* as
  `.docx` were kept as `.docx`.
- **10 hooks files** — verified strict subsets of the matching script's "Alternative Hooks"
  section: containment 1.00, zero unique lines. The text already lives in `03_YouTube/Scripts/`.
- **Superseded strategy docs (8)** — Gen-A plans replaced by Strategy V5 / Channel Style /
  Description Templates / the Upload Pack. Kept in `99_Archive/`.
- **`TotalRecalls Master Plan V2`** — superseded by V3 and truncated.
- **`Implementation Content Pack .docx`** — strict subset of the PDF; the PDF adds a whole section.
- **`Backup Library Blog 5`** — same topic as B5; the kept B5 is more complete.
- **`YouTube/videos/` (10 MP4s, 88 MB)** — the 2026-10-01 placeholder cuts, already uploaded
  private and slated for deletion. Current masters live in `demo-shoot/renders/`.
- **`frames/` + `frames_convergence/` (393 images, 29 MB)** — intermediate render frames.
- **`__pycache__/`**, convergence test frames.

### ⚠ Security — live credentials removed

`YouTube/yt-api/` in the source contains a **live Google API key, an OAuth client secret, a refresh
token and a one-time authorisation code** (`api_key.txt`, `credentials.json`, `token.json`,
`capture_in.txt`, `capture_out.txt`, `oauth_run.log`). These were **not** carried into this folder.

The Python automation scripts were carried — they read credentials from files rather than
embedding them, with **one exception**: `exchange_once.py` had a live Google OAuth authorisation
code hardcoded in a string literal. It was quarantined too (see the manifest). The remaining
scripts will not run until credential files are re-created. See `08_Tooling/yt-api/README.md`.

Recommend: rotate the API key and re-issue the OAuth client rather than copying the old ones back.

---

## Known defects carried over (not fixed — flagged)

Six source documents are **truncated mid-sentence**. Their `.docx` twins are *not* more complete
(identical word counts), and no complete copy exists anywhere in the repo — a repo-wide content
search for text that would only appear in the missing tails returns only the source and its
subset copy. Details, including exactly where each one cuts off, are in
`01_Strategy_and_Plans/Document Currency Register.md`.

**Decision (2026-11-15): leave them as they are — do not reconstruct.** They stay flagged in the
register so nobody quotes a truncated section as if it were complete.

---

## Provenance

- Source: `C:\Users\break\Projects\TotalRecalls-Source Code\Marketing\Market Launch Plans\`
- **The source folder is deliberately retained for about a month** (until mid-December 2026) while
  the plan is implemented, then retired. Until then it is the fallback, not the working copy — work
  from this curated folder.
- `Marketing\Jasper\YouTube\` is a strict **subset** of the source: 487 of the source's 555 files,
  byte-for-byte identical wherever they overlap (verified by SHA-256). The source adds the
  `Social media/` and `Founder's Story/` trees and 20 YouTube-level files. So anything dropped here
  still exists in the source, and most of it also exists in `Jasper\YouTube\`.
- Related canonical plans outside this folder:
  `docs/LAUNCH-IMPLEMENTATION-PLAN-2026-10-13.md` (cited by the Master Plan as the canonical
  launch implementation plan), `Marketing/Plans/` (Claude/Gemini plan variants).
- Per-file SHA-256 and origin path: `_build_records.json` in this folder.
