# Home workspace notes

## ACTIVE HANDOFF (read this first in any new session)
TotalRecalls LAUNCH (Search Console + YouTube channel) — status note:
`C:\Users\break\Projects\TotalRecalls\docs\STATUS-2026-10-01-youtube-launch.md`
(2026-10-01 evening EDT. Supersedes the 09-15 shoot-resume note — the
Claude hero was delivered and the app delivery bug is RESOLVED.)

State: Sitemap URL for GSC = `https://totalrecalls.app/sitemap.xml`
(200, 54 URLs, verified). YouTube channel **TotalRecalls @totalrecalls**
exists (ID `UChO3ZyrGqRtBFHRuQx2qX1w`); API key test PASSES; OAuth upload
flow BLOCKED on Google's `403 org_internal` (fix = consent with the plain
Gmail that owns the project + add as test user; exact steps + scripts in
the note, `Marketing/Jasper/YouTube/yt-api/`). Video to upload = the
embedded website hero `TR_website_claude_hero.mp4` (2292×1440, 30fps,
silent, 4:19 — already MP4).
Repo: `C:\Users\break\Projects\TotalRecalls`, branch `main`, tip `0206265`.

## Skills
Before replying, scan the skills below. If a skill matches or is even partially relevant to your task, you MUST load it with skill_view(name) and follow its instructions. Err on the side of loading — it is always better to have context you don't need than to miss critical steps, pitfalls, or established workflows. Skills contain specialized knowledge — API endpoints, tool-specific commands, and proven workflows that outperform general-purpose approaches. Skills also encode the user's preferred approach, conventions, and quality standards for tasks like code review, planning, and testing — load them even if you think you could handle the task with basic tools like web_search or terminal.
If a skill has issues, fix it with skill_manage(action='patch').
After difficult/iterative tasks, offer to save as a skill. If a skill you loaded was missing steps, had wrong commands, or needed pitfalls you discovered, update it before finishing.
