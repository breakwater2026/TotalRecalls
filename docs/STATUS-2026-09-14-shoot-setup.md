# STATUS — 2026-09-14 demo re-shoot setup (autonomous 2h session)

User away 2h, full latitude. Decision: **redo the demo video** — the 09-13 v3
masks didn't reach a favorable conclusion (5 of 8 providers need full logins;
name everywhere; Explorer OneDrive tree + address-bar name visible). New plan:
**2/3 of the 3440 monitor = recording canvas; right 1/3 = login zone** (user
moves login popups there, off-camera). Smaller-canvas preset prepared in
`demo-shoot/shoot_config.json` if the login zone is too tight.

## DONE + verified this session (branch `fix/robust-auth-20260913`, LOCAL commit — NOT pushed)

### 1. Alias path (name out of the Explorer breadcrumb)
- User ran (admin): `mklink /d C:\Users\Profile C:\Users\break` — VERIFIED
  resolving (Python `os.path.isdir` + `realpath` through the link).
- Account display name is **"Andre Denis"** — that's what Explorer showed for
  the real path; the symlink only helps if the app navigates THROUGH it.
- `totalrecalls/desktop/bridge.py` `__init__`: default save folder now resolves
  to `C:\Users\Profile\TotalRecalls-download` when `C:\Users\Profile` exists as
  a SYMLINK (`os.path.islink` gate — a coincidental real folder can never
  hijack; inert for users without the alias). `TR_DEMO_FOLDER` env var
  overrides. Functional check: resolved path = alias path, `realpath` = the
  real dir. "Open folder" + address bar will now show `This PC > Users >
  Profile` — no name.
- **REVERT (if ever needed):** delete the symlink (`rmdir C:\Users\Profile`
  from an admin cmd — it's a dir link) or set `TR_DEMO_FOLDER` to the real
  path. The app code change is production-inert without the symlink.

### 2. Account-name eye toggle (app page 2, under "Connected")
- `app_ui.html`: `#acct-email` now renders `••••••` by default; `#btn-eye`
  (eye / eye-off SVG, swaps on state) reveals/hides the real email —
  password-field pattern, user's own idea. `resetLoginUi()` clears the reveal
  state so no prior email lingers. Verified: Node harness against the
  extracted functions (7/7 assertions: default masked, reveal exact, re-mask,
  icon differs; JS syntax `node --check` OK).

### 3. Both EXEs rebuilt (clean venv, PyInstaller 6.22.2) + PYZ-verified 13/13 each
- free  `dist/TotalRecalls.exe`     sha256 `140c9a9d9ce836f2cc0ceb172a25126068e6136d6d4dfb992344729127f47cbe` (18,885,846 B)
- pro   `dist/TotalRecalls-Pro.exe` sha256 `3fd8fd109b870c77c08f88fa2cb6771ec8b8d8b29d4e71c1a116265bd7bfab03` (18,888,965 B)
- Verifier: `demo-shoot/verify_20260914_exe.py` (edition consts top-level;
  `TR_DEMO_FOLDER`/`Profile`/`islink` in bridge incl. nested code; 09-13 auth
  fixes still present: `userToken`, `_local_storage_probe_ok`, `api-40003`,
  `is_auth_rejected`; bundled app_ui.html has `btn-eye` + `toggleAccountEmail`
  + `acct-email`). Two first-run verifier FAILS were verifier bugs (tuple
  consts not unwrapped; nested code object names) — fixed in the verifier,
  re-ran clean.
- Tests: **219 passed, 2 deselected (live/battery), 6 subtests** — 09-13
  baseline 221, no regression.
- New Pro EXE relaunched and health-checked (app.log: clean startup,
  connected=False — clean slate for the shoot; old session.json intact).
- `edition.py` back to `EDITION = "free"` in the tree.

### 4. Shoot tooling (all in `C:\Users\break\demo-shoot\`)
- `shoot_config.json` — presets: `two_thirds` (canvas 2292×1440 @0,0 —
  DEFAULT; login zone x2292–3440, 1148px), `sixteen_nine` (2560×1440, zone
  880px — tight), `small` (2048×1440, zone 1392px — generous, prepared on
  user request).
- `shoot.sh <preset> <segname>` — reads config, RE-PROBES layout (ABORTS if
  primary isn't the 3440 at (0,0)), arms `ffmpeg gdigrab` FFV1 master →
  `masters/<segname>.mkv`, open-ended (stop = kill; read last `frame=` line).
- `blur_mask.py` **v3 OPAQUE** — the 09-14 "not working" blur was a
  per-pixel-alpha bug (StretchBlt writes RGB only → alpha 0 → invisible
  window; same class as the arrow-overlay bug). Opaque WS_POPUP +
  WS_EX_TRANSPARENT + WS_EX_TOPMOST renders fine (~18 fps, measured).
  `pythonw blur_mask.py X Y W H`; kill by PID. ctypes notes: this Python
  build rejects bare `int` in argtypes (use `wintypes.LONG`); `LPPOINT`/
  `LPSIZE` need `wintypes.POINT`/`SIZE` instances (not `byref`);
  `WNDCLASSEXW.lpfnWndProc` must be the `WINFUNCTYPE` and `DefWindowProcW`
  restype `c_ssize_t`.
- `PRE-SHOOT-CHECKLIST-2026-09-14.md` — the physical pre-shoot steps (3440
  primary + 2560 OFF, 100% scaling, panel placement in canvas, login zone
  empty, shoot order: Claude hero → 6-provider minis (ChatGPT inside) →
  DeepSeek manual-paste).

## GIT
- Local commit on `fix/robust-auth-20260913`: bridge.py + app_ui.html + this
  doc. Working tree otherwise clean. **NOT pushed** (user's no-push-without-
  review rule; user returns in ~2h). `dist/`+`build/` modified in tree per
  project convention.

## REMAINS (for when the user is back)
1. User reviews the eye toggle + alias behavior in the running Pro app
   (launch it, connect any provider, check page-2 mask + "Open folder"
   breadcrumb).
2. Pre-shoot physical steps (checklist) — only the user can do these.
3. Shoot (user drives; assistant arms/stops per the locked protocol).
4. Post-shoot: cuts + assembly + 1.5x + H.264 (recipe in
   `references/demo-video-capture.md`), then LS email (zip + web cut under
   25 MB) — the old v3 video is now superseded, NOT the deliverable.
5. Free-ZIP repackage is a SEPARATE delivery decision (site frozen at the 404
   gate; decide with the user when the eye toggle ships to buyers).
6. LS live-key test + X230 cron — unchanged, still open.

## LESSONS (this session)
- MSYS path bug, again: ffmpeg/native tools given `/c/...` or `C:/...`-in-bash
  wrote to a literal `C:\c\Users\...` tree — deleted. For native tools in
  bash: `cd` in MSYS paths + relative/MSYS paths for ffmpeg, `C:/...` forward
  slashes for node/python argv, or run via `cmd //c`/`powershell -File`.
- Layered-window masks: if a GDI pass writes RGB only, alpha stays 0 →
  invisible. For solid masks, don't use per-pixel alpha at all.
- PYZ verifiers: unwrap tuple/frozenset consts and walk NESTED code objects
  for `co_names` — both missed real content on first run.
