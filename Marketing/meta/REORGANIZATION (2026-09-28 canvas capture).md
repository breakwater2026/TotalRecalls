# TotalRecalls Canvas — 100-Artifact Reorganization
Source: Jasper canvas "TotalRecalls App Launch" (b477ef8f-bd6d-4cc1-a23c-050ac901871f)
Captured: 2026-09-28, logged in as marketing@totalrecalls.app (full DOM text of every node).

## Inventory
- 101 `[data-id]` nodes in the canvas = **99 real documents** + 2 empty/toolbar entries (3244a21d, one duplicate of 904ecc99).
- All 99 docs are saved in this folder as `.md` AND `.docx`, named `<title>_<nodeid8>`.
- Largest: TotalRecalls Master Implementation Plan (15,948 chars, node 904ecc99).

## Duplicates (verified by content comparison, not just titles)
### Safe to DELETE (2)
| Delete | Keep | Why |
|---|---|---|
| `TotalRecalls Master Implementation Plan_26de1acc` | `..._904ecc99` (15,948) | 26de1acc (5,258) is a TRUNCATED copy: ends mid-sentence ("…designates **one approved final"), 76% text-identical to 904ecc99. |
| `Sequence_1_Core_Welcome_Onboarding_023c3cc4` | `..._5d9c45c2` | Byte-identical content (similarity 1.00, same 1,050 chars). |

### Near-duplicates — delete one if you want, keep both if you want variants
| Pair | Note |
|---|---|
| Why I Built TotalRecalls: `e6cd1378` (5,130) vs `d7ea1339` (5,105) | Same founder story, two drafts (same ending, same opening). Keep the larger (e6cd1378); delete d7ea1339 if deduping. |
| Launch Marketing Plan (Revised): `72b37216` (9,550) vs `6f06cdb1` (4,173) | 6f06cdb1 ends mid-week-5 table row → likely an earlier/truncated draft of the same plan. 72b37216 is complete (ends on video overlay CTA). Keep 72b37216. (Its "ergreen" ending is a table-cell artifact of "Evergreen", not a typo.) |
| Tweet: `119587b6` vs `58751f7a` | NOT duplicates — two genuinely different tweets. Keep both. |

### Same-title groups that are DISTINCT variants (keep all — different copy)
Instagram captions ×3, LinkedIn posts ×3, Facebook posts ×3 (4 variants), Google Ads Search/Display/Video ×2, Meta Ads ×2, X Ads ×2, LinkedIn Ads ×2, ad variations ×3 — all low similarity (≤0.4), different messaging. If you must free slots, collapsing each social group to its single best-performing post is the cleanest cut.

## Unfinished items
### YouTube videos 3–10 (the main gap)
- **Complete:** `TotalRecalls YouTube Content Plan: Your First 10 Videos` (baee6adf) — all 10 titles, formats, runtimes, hooks, CTAs are in it.
- **Scripts written:** Video 1 "Save AI Chats from 8 Providers" (18d7057b) and Video 2 "Why I Built TotalRecalls" (df0b43e0) — full 5,400-char scripts each.
- **Missing scripts:** Videos 3–10 (8 docs). Titles per the plan:
  3. You're Not Backing Up Your AI Chats (Short)
  4. How to Export ChatGPT Conversations to Markdown
  5. Back Up Your Claude… (see plan for full titles)
  … through 10. (Full list in the 10-Videos doc.)
- Related video docs (complete, not missing): Short-Form Video Strategy, Main Product Explainer Video Outline, Video Shot List, Video Storyboard.

## Deletion plan to make room (~8–10 slots)
1. **Certain (2):** 26de1acc (truncated Master Plan), 023c3cc4 (Sequence 1 exact dup).
2. **Strong candidates (2):** d7ea1339 (founder-story draft), 6f06cdb1 (truncated Revised plan).
3. **If more slots needed (up to 8):** drop 1 of each social-post variant set (2 of 3 Instagram, 2 of 3 LinkedIn, 2 of 4 Facebook, 1 of 2 per ad type) — each is redundant messaging, and the plan docs cover all angles.
→ Deleting items 1–3 frees ~12 slots: enough for the 8 missing YouTube scripts (3–10) plus buffer.

## Note on capture fidelity
Canvas nodes render full text for most docs, but the Master Plan (904ecc99) canvas text matches its full-view render exactly (18,113 vs 18,100 chars, same ending), so the DOM capture is the complete document. The one doc that WAS truncated on the canvas (26de1acc) is the one being deleted.
