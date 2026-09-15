# Home workspace notes

## ACTIVE HANDOFF (read this first in any new session)
TotalRecalls website + apps — latest status note:
`C:\Users\break\Projects\TotalRecalls\docs\STATUS-2026-09-14-shoot-setup.md`
(branch `fix/robust-auth-20260913`, pushed to origin, tip `0623c8c`;
supersedes `docs/STATUS-2026-09-13-robust-auth-fix.md`).

State as of 2026-09-14 ~19:50 EDT (2h autonomous session, user away):
- **Demo RE-SHOOT setup** (the 09-13 video didn't reach a favorable
  conclusion — name everywhere in logins + Explorer). New plan: 2/3 of the
  3440 monitor = canvas, right 1/3 = login zone. Tooling in
  `C:\Users\break\demo-shoot\`: `shoot_config.json` (3 canvas presets incl.
  the requested smaller one), `shoot.sh` (layout-gated armer),
  `blur_mask.py` v3 (OPAQUE — the earlier invisibility was a layered-alpha
  bug), `PRE-SHOOT-CHECKLIST-2026-09-14.md`.
- **Name hiding SHIPPED in the EXEs:** `C:\Users\Profile` → `C:\Users\break`
  alias symlink (user-created) + `bridge.py` auto-routes the default save
  folder through it (islink-gated, inert without the alias) → "Open folder"
  shows `Profile`, not "Andre Denis". Account email now masked `••••••` on
  page 2 with an eye toggle (user's idea). Both EXEs rebuilt + PYZ-verified
  13/13 (free sha `140c9a9d…`, pro sha `3fd8fd10…`); 219 tests pass; new Pro
  EXE running (clean "Not connected" slate).
- **Still open:** (1) user reviews eye toggle + alias in the running app;
  (2) pre-shoot physical steps (checklist); (3) shoot + post (cuts/assembly/
  H.264; old v3 video SUPERSEDED — not the deliverable); (4) free-ZIP
  repackage = separate delivery decision; (5) LS live-key test + X230 cron
  unchanged.
Repo: `C:\Users\break\Projects\TotalRecalls`.

## Skills
Before replying, scan the skills below. If a skill matches or is even partially relevant to your task, you MUST load it with skill_view(name) and follow its instructions. Err on the side of loading — it is always better to have context you don't need than to miss critical steps, pitfalls, or established workflows. Skills contain specialized knowledge — API endpoints, tool-specific commands, and proven workflows that outperform general-purpose approaches. Skills also encode the user's preferred approach, conventions, and quality standards for tasks like code review, planning, and testing — load them even if you think you could handle the task with basic tools like web_search or terminal.
If a skill has issues, fix it with skill_manage(action='patch').
After difficult/iterative tasks, offer to save as a skill. If a skill you loaded was missing steps, had wrong commands, or needed pitfalls you discovered, update it before finishing.
