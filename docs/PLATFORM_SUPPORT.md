# Platform support

The desktop application keeps exports and credentials local.  OS integration
is dependency-free and selected at runtime:

| Host | Local state directory | Folder opener |
| --- | --- | --- |
| Windows | `%APPDATA%\PerplexityExporter` (unchanged) | `os.startfile` / Explorer |
| macOS | `~/Library/Application Support/TotalRecalls` | `open` |
| Linux/BSD | `$XDG_STATE_HOME/TotalRecalls`, or `~/.local/state/TotalRecalls` | `xdg-open` |

Set `TOTALRECALLS_STATE_DIR` for a portable build or a test profile.  The
directory is created on first use.

Windows session files use DPAPI.  On systems without DPAPI, state is stored in
a `private-file` envelope and written with owner-only permissions where the OS
supports them.  This fallback avoids plaintext JSON and extra dependencies, but
it is not equivalent to a hardware-backed keychain; users should protect their
account and home-directory access.

Folder and process commands are passed as argument lists, never through a
shell.  Windows keeps its existing `tasklist`/`taskkill` behavior; Unix-like
systems use `pgrep`/`kill` when process takeover is requested.

## Building the desktop app

PyInstaller builds are native to the host OS; build each release on its target
platform.  From the repository root:

```text
Windows: .venv\Scripts\python.exe tools\build_exe.py --edition free
macOS:   .venv/bin/python tools/build_exe.py --edition free
Linux:   .venv/bin/python tools/build_exe.py --edition free
```

The script restores the source edition to `free` after the build.  Windows
produces `dist\TotalRecalls.exe`; macOS and Linux produce `dist/TotalRecalls`
(or a native bundle when configured).  Code signing and
installer/notarization steps remain platform-specific.
