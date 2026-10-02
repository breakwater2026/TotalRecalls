# TotalRecalls Marketing — Asset Index

Reorganized 2026-09-29 from Jasper's flat canvas/jasper/YouTube exports into a
topical structure, deduped (SHA256 + normalized-content passes), then
**merged the same-topic docs under ~2 pages into single review files**
(21 merged files, 79 small docs consumed). Full audit trail:
`Jasper/tools/reports/` (audit_report.txt, near_dup_report.txt, deleted-manifest.txt)
and the merge spec in `Jasper/tools/scripts/merge_docs.py`.

**Conventions**
- `.md` = working source (mine); `.docx` = human-facing copy (yours), regenerable
  from the `.md` via `Jasper/tools/scripts/batch_convert.py`.
- Merged files: `## section` = one original document, unedited. Empty/duplicate
  sections dropped during cleanup (`cleanup_merged.py`).
- `(variant N)` = a genuinely different version of the same asset (A/B material).
- No hash suffixes.

```
marketing/
├── ads/                    paid campaigns (merged per network)
│   ├── google/             Google Ads Copy — Search, Display & Video (6 sections)
│   ├── meta/               Meta Ad Copy (2 sections)
│   ├── linkedin/           LinkedIn Ad Copy (2 sections)
│   ├── x/                  X Ad Copy (2 sections)
│   └── generic/            Paid Ad Copy — Ad Variations & Search (4 sections)
├── email/                  launch email program (merged per slot/sequence)
│   ├── sequences/          Email 1 Welcome (early draft) +
│   │                       Email Sequences 1-3 — Welcome, Upgrade, Urgency (4 sections)
│   ├── slot-2/             Email 2 — all variants (6 sections)
│   ├── slot-3/             Email 3 — all variants (7 sections)
│   └── slot-4/             Email 4 — all variants (3 sections)
├── messaging/              core brand copy (merged)
│   ├── TotalRecalls Launch Campaign (brief + abstract + full plan, 3 sections)
│   ├── Landing Page Copy — 3 variants
│   ├── Press & Announcement Copy (press release, launch pricing, blog, headlines)
│   ├── FAQ — Is TotalRecalls safe, Windows warning
│   └── founder/            Founder Story — Why I Built TotalRecalls (2 variants + profile)
├── strategy/               plans & checklists
│   ├── Master Implementation Plan
│   ├── Launch Marketing Plan (Revised) — 2 variants (merged)
│   ├── 60-Day Launch Content Calendar
│   ├── Launch Readiness Plan · Launch Marketing Organization · Launch Gap Checklist
│   └── Missing Items Checklist   (Jasper's own latest status tracker)
├── youtube/                channel & production
│   ├── scripts/            YT Video 1–10 scripts — ALL 10 complete (Video 6 = Final, 2026-09-29)
│   ├── hooks/              alternative hook docs (Jasper, 2026-09-29) — source
│   │                       .md; each merged into its script's "Alternative Hooks"
│   │                       section via merge_hooks.py (ALL 10 done, 2026-09-29)
│   ├── YouTube Content Plan — First 10 Videos · Channel Description
│   ├── YouTube Playlist Structure — 2 frameworks (merged)
│   ├── Upload Checklist & Template · Thumbnail Concepts
│   └── Main Explainer Video — Outline & Shot List (includes the Video Storyboard
│       Visuals/Audio summary table, restored from the raw dump)
├── social/                 organic launch-day posts (merged per platform)
│   ├── facebook/           Facebook Posts — all variants (5 sections)
│   ├── instagram/          Instagram Captions — all variants (4 sections)
│   ├── linkedin/           LinkedIn Posts — all variants (4 sections)
│   └── x/                  X (Twitter) Posts — all variants (5 sections)
├── website/                landing page & optimization
│   ├── Landing Page Copy — Hero & Trust (merged)
│   ├── Part 1 Page-by-Page Website Optimization Brief
│   └── Part 2 Homepage Rewrite
├── ops/                    Launch-Day Social Posting Checklist
├── meta/                   tracking docs
│   ├── TOPICS_AND_GAPS (2026-09-29 gap analysis).md   ← STATUS OF RECORD
│   └── REORGANIZATION (2026-09-28 canvas capture).md
├── raw_dumps/              unstructured exports kept for reference
│   ├── Conversation Jasper ai — Day2.md
│   └── Jasper Plan 1 (full canvas export).md
└── Jasper/                 tooling (not content)
    ├── tools/scripts/      convert.py, batch_convert.py, consolidate.py,
    │                       merge_docs.py, cleanup_merged.py, sha_audit.py, near_dup.py
    └── tools/reports/      audit reports, deleted-manifest.txt,
                            canvas_index_stale_pre_consolidation.json,
                            coverage_check2.py, cluster_diff.py
```

**Counts (post-merge, 2026-09-29):** 53 `.md` / 49 `.docx` (21 of the `.md` are
merged review files; the 4 extra `.md` without a `.docx` are meta/tracking docs
and the README itself).

## YT 10-Video Plan status (as of 2026-09-29)
| # | Script | Status |
|---|---|---|
| 1–5 | Videos 1, 2, 3 (V2), 4, 5 (V2) | ✅ complete |
| 6 | Trying to Get Your Old AI Conversations Back? | ✅ **Final** (2026-09-29) + 3 alternative hooks merged in |
| 7–10 | Videos 7 (V3), 8 (V2), 9, 10 | ✅ complete |
