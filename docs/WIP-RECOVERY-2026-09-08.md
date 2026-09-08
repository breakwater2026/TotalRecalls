# USER WIP — RECOVERED HUNK (durable copy)

Context: the user's uncommitted WIP was backed up on 2026-09-07 to
`%LOCALAPPDATA%\Temp\tr_wip_backup_20260907\` (7 items) with the user's
authorization to remove it from the working tree ("You can delete my WIP...
My WIP will resurface at that point" — the side-by-side website+GUI session).
The Temp backup was PURGED overnight (Storage Sense / temp cleanup) before the
09-08 session. This file preserves the only non-reproducible item.

## Item 1 of 7 — app_ui.html provider-sync hunk (RECOVERED, see below)

Verbatim content, captured from `git diff TotalRecalls.exe_extracted/app_ui.html`
in session 20260906_190653_d4b609 on 2026-09-07 (the WIP hunk that had to be
reverted from the preserved extracted artifact before committing 974aa72).
Location in `app_ui.html`: the "Idle disconnected" branch, at the marker
`setPill('Not connected', false);` (~line 747 in the then-current file; find by
the surrounding comment, not by line number).

```diff
@@ -379,6 +379,11 @@
       q('cookie-box').classList.add('hidden');
     } else {
       // Idle disconnected: only restore connect screen if export is showing, or waiting stuck.
+      if (s.provider) {
+        const sel = q('provider-select');
+        if (sel) sel.value = s.provider;
+        updateProviderUI(s.provider);
+      }
       setPill('Not connected', false);
       if (!q('scr-export').classList.contains('hidden') && !s.connected) {
         q('scr-export').classList.add('hidden');
```

Re-apply: insert the five `+` lines immediately BEFORE `setPill('Not connected', false);`
in the idle-disconnected else-branch. Purpose (from the user's WIP): on an idle
disconnect, re-sync the provider dropdown + provider UI to the last state's
provider instead of leaving them stale.

Fidelity note: this is a transcript-captured diff, not a byte-level file backup
(the original backup file's sha was 8fffcb80… for the full WIP app_ui.html, but
only this one hunk differed from HEAD in that file — verified at the time:
"CONFIRMED 7 hunks in diff: 6 mine + 1 user WIP", and after my fixes shipped,
this hunk is the only remaining user-WIP change to app_ui.html).

## Items 2–7 of 7 — TRIVIAL / RECREATABLE (not lost in any meaningful sense)

2. `build_exe.py` — user's WIP was an EDITION regex tweak. Current committed
   `tools/build_exe.py` works; the user can redo their tweak in the GUI session.
3. `.gitignore` — WIP added a `release/` line. One line, re-add if desired
   (note: `release/TotalRecalls-1.0.0-pro.zip` IS currently committed, so
   adding the ignore line now would need `git rm --cached` discussion first).
4. `.vscode/settings.json` — WIP added an env-file line. One line, editor-local.
5. `docs-audit-prompt.md` — user's own prompt notes; superseded by
   `docs/ACTION_PLAN-prelaunch-2026-09-06.md` (committed) and
   `docs/HANDOFF-website-apps-2026-09-07.md` (committed).
6. `docs-website-comments.md` — user's website comments; content was already
   consumed by the audit (see ACTION_PLAN "Comment-file items already applied").
   Ask the user if they still have their original copy (it came from them).
7. `docs-Lemon-Squeezy/` — LS evaluation notes; superseded by the committed
   licensing implementation (0bd8ebe) + HANDOFF note.

## Also purged from Temp (assess impact — both acceptable)

- `pro_exe_backup_1788819224.exe` (old Sept-3 Pro EXE): superseded — the NEW
  `dist/TotalRecalls-Pro.exe` (committed, edition=pro, carries ALL fixes) is
  strictly better. No loss.
- `app_ui_full_with_wip.html` (full WIP file copy): the only delta vs HEAD was
  hunk #1 above, which is recovered here. No loss.

## LESSON (recorded in memory + skill)

NEVER store user backups in `%LOCALAPPDATA%\Temp` — Windows purges it
(Storage Sense / cleanup / reboots). Durable locations: the repo itself
(committed), `C:\Users\break\vast-tools\`, or `%LOCALAPPDATA%\hermes\`.
