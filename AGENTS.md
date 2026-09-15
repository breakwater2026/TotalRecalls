# Home workspace notes

## ACTIVE HANDOFF (read this first in any new session)
TotalRecalls demo RE-SHOOT — resume note for the morning session:
`C:\Users\break\Projects\TotalRecalls\docs\HANDOFF-2026-09-15-shoot-resume.md`
(supersedes `docs/STATUS-2026-09-14-shoot-setup.md`; branch
`fix/robust-auth-20260913` pushed to origin, tip `a2158b9`).

State as of 2026-09-14 ~22:45 EDT (shoot night, user ending early — tired):
- **Decisions locked (do not revisit):** (1) NO 25 MB cap exists — it was an
  email-attachment assumption; LS letter asks only for a demo video →
  top-quality render (native 2292×1440, 2-pass ~10 Mbps) delivered as an
  OneDrive "anyone with link" URL; (2) per-provider recording — Claude full
  hero take + 7 individual minis, 1.5× in post, no conversation displays,
  concat stream-copy stitch; (3) name hiding FINAL = export folder + library
  at `C:\TotalRecalls` via `TR_DEMO_FOLDER` + desktop shortcut "TotalRecalls
  (Shoot)" (the `C:\Users\Profile` symlink was a dead end — Explorer shows
  the account display name for anything under the profile); (4) eye toggle
  shipped + user-confirmed.
- **Shoot state:** tooling proven (shoot.sh native-path fixed; STOP = kill
  session + Stop-Process ffmpeg, two steps). `masters/seg1_claude.mkv` =
  take 5, 4:31, NOT locked (ends "Not connected" + Word shows a
  confidential trading thread). Claude hero redo is the morning's first
  task, then the 7 minis, then post (`render_final_top.sh`) + OneDrive + LS
  reply (4 questions: pricing / video link / social URLs KYB-KYC / product
  description).
- **Recurring defect:** hero takes end "Not connected" (user disconnects at
  the end) — stop the take BEFORE disconnecting.
Repo: `C:\Users\break\Projects\TotalRecalls`.

## Skills
Before replying, scan the skills below. If a skill matches or is even partially relevant to your task, you MUST load it with skill_view(name) and follow its instructions. Err on the side of loading — it is always better to have context you don't need than to miss critical steps, pitfalls, or established workflows. Skills contain specialized knowledge — API endpoints, tool-specific commands, and proven workflows that outperform general-purpose approaches. Skills also encode the user's preferred approach, conventions, and quality standards for tasks like code review, planning, and testing — load them even if you think you could handle the task with basic tools like web_search or terminal.
If a skill has issues, fix it with skill_manage(action='patch').
After difficult/iterative tasks, offer to save as a skill. If a skill you loaded was missing steps, had wrong commands, or needed pitfalls you discovered, update it before finishing.
