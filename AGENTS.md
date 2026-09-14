# Home workspace notes

## ACTIVE HANDOFF (read this first in any new session)
TotalRecalls website + apps — latest status note:
`C:\Users\break\Projects\TotalRecalls\docs\STATUS-2026-09-13-robust-auth-fix.md`
(branch `fix/robust-auth-20260913`, pushed to origin; supersedes
`docs/HANDOFF-website-apps-2026-09-07.md`, which is kept for history).

State as of 2026-09-13 ~22:00 EDT (user asleep, returns ~08:00 EDT):
- **Auth robustness fix DONE + LIVE-TESTED by user ("You nailed it"):**
  `core/errors.py` `is_auth_rejected()` uniform gate; DeepSeek fail-closed
  validate + CDP `localStorage[userToken]` capture **validated through the
  provider's own validate() before the login window closes** (the 30-char
  auth-page nonce bug found in the user's 20:05 test, fixed + re-verified);
  ChatGPT chunked `session-token.N` cookie capture. 221 tests pass.
  Both EXEs rebuilt (clean venv) + PYZ-verified 16/16:
  free `dist/TotalRecalls.exe` sha `4fe55ee9…`, pro
  `dist/stage/TotalRecalls-Pro.exe` + `dist/TotalRecalls-Pro.exe`
  sha `f8aef6a2…`. User's running app was the STAGE build — they relaunched
  it themselves after the fix.
- **Demo video DONE:** `demo-shoot/final/final_totalrecalls_demo_1080p.mp4`
  (46 MB master) + `final_totalrecalls_demo_web.mp4` (23.5 MB, 14:08, H.264,
  under the 25 MB e-mail limit). Structure: logo_open → Claude 3:43 @1× →
  Perplexity/Qwen 4:45 @2× → ChatGPT 3:57 @2× → DeepSeek-redo 1:34 @2× →
  logo_end. DeepSeek segment re-shot 21:08 (`masters/seg3_deepseek_redo.mkv`)
  showing the FIXED in-app login. Awaiting: user watch-through, then send
  video + screenshot pack to Lemon Squeezy.
- **LS screenshot pack DONE:** `site/docs-screenshots/` 52/52 full-page PNGs
  (one per site page) + `site/docs-screenshots.zip` (8.6 MB) — for the LS
  app review (site not public yet). Regenerate: `site/scripts/capture-pages.mjs`
  (needs `astro dev` on 127.0.0.1:4321; playwright-core devDep, drives system Edge).
- **Git:** all committed + pushed to `origin/fix/robust-auth-20260913`
  (9a5c89f robust-auth, 80c3549 LS screenshot pack). Working tree clean.
- **Still open:** (1) user watches final video + e-mails LS (zip + 23.5 MB
  video); (2) LS live-key test — blocked until LS approves the app;
  (3) site deployment gate stays FROZEN (production_branch = RedesignV7,
  intentional); (4) X230 15-min provider-health cron — personal resilience
  layer, unbuilt.
Repo: `C:\Users\break\Projects\TotalRecalls`.

## Skills
Before replying, scan the skills below. If a skill matches or is even partially relevant to your task, you MUST load it with skill_view(name) and follow its instructions. Err on the side of loading — it is always better to have context you don't need than to miss critical steps, pitfalls, or established workflows. Skills contain specialized knowledge — API endpoints, tool-specific commands, and proven workflows that outperform general-purpose approaches. Skills also encode the user's preferred approach, conventions, and quality standards for tasks like code review, planning, and testing — load them even if you think you could handle the task with basic tools like web_search or terminal.
If a skill has issues, fix it with skill_manage(action='patch').
After difficult/iterative tasks, offer to save as a skill. If a skill you loaded was missing steps, had wrong commands, or needed pitfalls you discovered, update it before finishing.
