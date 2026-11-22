# Blog Series Map

Consolidated 2026-11-15 from the ten drafts in `04_Blog/` and the plan's B1–B9 series definition.
The source filenames do **not** match the plan's slot numbers — this map resolves that.

---

## Slot map

| Plan slot | Topic | File in `04_Blog/` | Source file | Words | State |
| --- | --- | --- | --- | --- | --- |
| **B1** | Launch announcement | — | — | — | ⚪ **No draft exists** — verified by repo-wide search 2026-11-15; nothing to delete |
| **B2** | Where TotalRecalls saves your files | `B2 - Where TotalRecalls Saves Your Files.md` | `Library Folder Explainer Blog.md` | 1,587 | ✅ complete (no meta title/description) |
| **B3** | Markdown vs JSON | `B3 - Markdown vs JSON.md` | `Markdown vs JSON Explainer Blog.md` | 1,711 | ✅ complete |
| **B4** | What "not sent to our servers" means | `B4 - What Not Sent to Our Servers Means.md` | `Privacy Explainer Blog 4.md` | 1,848 | ✅ complete — strictest review |
| **B5** | Backing up your AI conversation library | `B5 - How to Back Up Your Saved AI Chats on Windows.md` | `TotalRecalls Blog Post 8.md` | 2,671 | ✅ complete — **canonical B5** |
| **B6** | Searching saved chats with Windows Search | `B6 - How to Search Saved Chats with Windows Search.md` | `Windows Search Blog 6.md` | 2,059 | ✅ complete |
| **B7** | Organising saved chats by project | `B7 - How to Manage Saved Chats with PowerShell.md` | `TotalRecalls Blog Post 10.md` | 2,997 | ✅ complete — see slot ruling below |
| **B8** | Using saved chats in a note-taking app | `B8 - How to Open Saved Chats in Obsidian.md` | `TotalRecalls Blog Post 7.md` | 2,293 | ✅ complete |
| **B9** | Using saved chats in VS Code | `B9 - How to Use Saved Chats in VS Code.md` | `VS Code Blog Post 9.md` | 2,826 | ✅ complete |
| — | Free vs Pro explainer (not in the series) | `Extra - Free vs Pro, Explained Plainly.md` | `Free vs Pro Explainer Blog.md` | 985 | ⚠ missing meta title/description; stale pricing |

---

## Two filename/slot traps

1. **`TotalRecalls Blog Post 7` is plan slot B8, not B7.** It is the Obsidian/note-taking post.
2. **`TotalRecalls Blog Post 8` is plan slot B5, not B8.** It is a backup post — and a second,
   thinner backup post (`Backup Library Blog 5.md`, 1,777 words) also exists. The two overlap
   heavily; `Blog Post 8` is more complete (adds Robocopy, Task Scheduler, restore steps and a
   common-mistakes section) and is the one kept. The thinner one is archived.

Also: the plan states plainly that **there is no Blog 10** — the series is 9 posts. The file named
`TotalRecalls Blog Post 10` is the PowerShell post, which the D1 decision places in the **B7**
("organising") slot.

---

## Resolved gaps

| Gap | Resolution |
| --- | --- |
| **B1 has no draft** | ✅ **Checked 2026-11-15.** Repo-wide search for any B1 / launch-announcement file returns only `Marketing/messaging/Press & Announcement Copy.md` (a press release, not a blog post) and an archived social fragment. There is no B1 file to delete. If B1 is wanted, it must be written; if it is dropped, say so and the slot closes. |
| **B7 had no draft** | **Resolved** — the PowerShell post fills it per the D1 ruling. Note it is "managing with PowerShell" rather than the originally proposed "organising by project"; the topic is adjacent, not identical. |
| **Duplicate B5** | **Resolved** — `Blog Post 8` kept, `Backup Library Blog 5` archived. |

---

## Publishing schedule (from Master Implementation Plan V3 §12)

One post per week, series order, Week 3 → Week 11. Week 12 is a buffer.

| Week | Post | Gate |
| --- | --- | --- |
| 3 | B1 | 🔴 blocked — topic and draft unconfirmed |
| 4 | B2 | Topic and draft confirmed |
| 5 | B3 | Filename format fixed |
| 6 | B4 | Second-person privacy review |
| 7 | B5 | Library path confirmed |
| 8 | B6 | Written by Week 6 |
| 9 | B7 | Written by Week 7 |
| 10 | B8 | Written by Week 8 |
| 11 | B9 | Path and filename format confirmed |
| 12 | — | Buffer |

If B1 or B2 slip, shift the whole schedule a week rather than publishing out of order.

---

## Blog → video pairings

Each finished post is the script source for its video. Copy checked wording (privacy, Gemini,
device, platform lines) verbatim — do not re-derive claims while adapting.

| Blog | Video | Planned |
| --- | --- | --- |
| B2 | Where TotalRecalls Saves Your Files | launch set |
| B3 | Markdown vs JSON | Weeks 9–10 |
| B4 | What "Not Sent to Our Servers" Means | Weeks 9–10 |
| B5 | Backing up your AI conversation library | Weeks 11–12 |
| B6 | Searching saved chats with Windows Search | Weeks 9–10 |
| B7 | Organising saved chats by project | Weeks 11–12 |
| B8 | Note-taking app workflow | after day 90 |
| B9 | VS Code workflow | after day 90 |

**Note:** the Gen-D `YouTube Launch Plan` supersedes this lineup with its own first-10 (two export
how-tos, the 8,135-conversation flagship, then ownership / Obsidian / SSE / Gemini / backup /
pricing). Reconcile the two before scheduling — see `Document Currency Register.md`.

---

## Open consistency items (carried from V3 §5)

These block publication until answered against the released app:

| Item | Where it appears | Action |
| --- | --- | --- |
| Saved filename format | B3 shows `quarterly-report-draft.md`; B9 says filenames start with a date | Confirm the real format in the app, then update every post, guide and thumbnail |
| Default Library path | B9 uses `C:\TotalRecalls\Library\` | Confirm the real default path |
| Pro license check | B4 says only the licence key is sent | Confirm against real activation |
| Gemini Takeout conversion | B4 says conversion happens on the user's PC | Confirm against the released app |
