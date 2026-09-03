#!/usr/bin/env python3
"""Build TotalRecalls.exe in either the locked Free Tier or unlocked buyer
(Pro) edition.

Usage:
    python tools/build_exe.py --edition pro
    python tools/build_exe.py --edition free

The Free Tier EXE is the default artifact and also ships in the free ZIP.
The Pro EXE is what buyers receive: all 8 providers, unlimited downloads,
no license key needed (see totalrecalls/edition.py).

The script rewrites totalrecalls/edition.py to the requested edition, runs
PyInstaller, then restores the source file to the "free" default so the tree
never accidentally commits a Pro build flag.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO not in sys.path:
    sys.path.insert(0, REPO)

from totalrecalls.core.platform import (
    parse_process_ids,
    process_list_command,
    process_terminate_command,
)

EDITION_FILE = os.path.join(REPO, "totalrecalls", "edition.py")
EXE_FILENAME = "TotalRecalls.exe" if os.name == "nt" else "TotalRecalls"
EXE_OUT = os.path.join(REPO, "dist", EXE_FILENAME)


def set_edition(edition: str) -> None:
    src = open(EDITION_FILE, encoding="utf-8").read()
    new = re.sub(r'^EDITION = "(free|pro)"', f'EDITION = "{edition}"', src, count=1, flags=re.M)
    if new == src:
        raise SystemExit(f"ERROR: could not set EDITION in {EDITION_FILE}")
    open(EDITION_FILE, "w", encoding="utf-8").write(new)
    print(f"[build_exe] edition.py -> EDITION = \"{edition}\"")


def restore_edition() -> None:
    try:
        set_edition("free")
    except SystemExit as e:
        print(f"WARNING: {e} — restore EDITION manually before committing!")


def kill_running() -> None:
    process_name = "TotalRecalls.exe" if os.name == "nt" else "TotalRecalls"
    try:
        result = subprocess.run(
            process_list_command(process_name),
            capture_output=True,
            text=True,
            check=False,
        )
        for pid in parse_process_ids(result.stdout or ""):
            subprocess.run(
                process_terminate_command(pid),
                capture_output=True,
                text=True,
                check=False,
            )
    except (OSError, subprocess.SubprocessError):
        # A running desktop process is not a prerequisite for building.
        pass


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--edition", choices=["free", "pro"], required=True)
    ap.add_argument("--name", default=None,
                    help=f"Optional output name (default: {EXE_FILENAME})")
    args = ap.parse_args()

    venv_py = os.path.join(REPO, ".venv", "Scripts", "python.exe")
    if not os.path.exists(venv_py):
        venv_py = os.path.join(REPO, ".venv", "bin", "python")
    if not os.path.exists(venv_py):
        raise SystemExit("ERROR: .venv python not found")

    kill_running()
    set_edition(args.edition)
    try:
        # The edition flag is baked into totalrecalls.edition. Force PyInstaller
        # to refresh its analysis so consecutive Free/Pro builds cannot reuse
        # the previous edition's cached module bytecode.
        cmd = [
            venv_py,
            "-m",
            "PyInstaller",
            "TotalRecalls.spec",
            "--noconfirm",
            "--clean",
        ]
        print("[build_exe] running:", " ".join(cmd))
        rc = subprocess.call(cmd, cwd=REPO)
    finally:
        restore_edition()

    if rc != 0:
        return rc

    if args.name:
        dest = os.path.join(REPO, "dist", args.name)
        shutil.copy2(EXE_OUT, dest)
        print(f"[build_exe] copied to {dest}")
    print(f"[build_exe] DONE ({args.edition} edition): {EXE_OUT} "
          f"({os.path.getsize(EXE_OUT):,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
