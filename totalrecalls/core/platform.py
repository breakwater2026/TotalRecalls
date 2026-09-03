"""Small, dependency-free platform integrations used by the desktop app.

The UI can remain platform agnostic while this module owns OS-specific paths,
folder launching, and process command construction.  Commands are returned as
argument lists and are never passed through a shell.
"""

from __future__ import annotations

import csv
import io
import os
import subprocess
import sys
from pathlib import Path
from typing import Mapping

APP_STATE_DIR_ENV = "TOTALRECALLS_STATE_DIR"
_WINDOWS_APP_DIR = "PerplexityExporter"  # Keep the existing Windows location.
_POSIX_APP_DIR = "TotalRecalls"


def _host_platform_name() -> str:
    return "darwin" if sys.platform == "darwin" else os.name


def app_state_dir(
    *,
    platform_name: str | None = None,
    environ: Mapping[str, str] | None = None,
    home: str | os.PathLike[str] | None = None,
) -> str:
    """Return the per-user directory for local state, without creating it.

    ``TOTALRECALLS_STATE_DIR`` is an explicit portable-build override.  Native
    defaults follow Windows roaming AppData, macOS Application Support, and
    the Linux/BSD XDG state directory.
    """

    platform_name = platform_name or _host_platform_name()
    env = os.environ if environ is None else environ
    override = env.get(APP_STATE_DIR_ENV)
    if override:
        return os.path.abspath(os.path.expanduser(override))

    user_home = os.fspath(home) if home is not None else os.path.expanduser("~")
    if platform_name == "nt":
        base = env.get("APPDATA") or user_home
        return os.path.join(base, _WINDOWS_APP_DIR)
    if platform_name == "darwin":
        return os.path.join(user_home, "Library", "Application Support", _POSIX_APP_DIR)
    base = env.get("XDG_STATE_HOME") or os.path.join(user_home, ".local", "state")
    return os.path.join(base, _POSIX_APP_DIR)


def ensure_app_state_dir(**kwargs: object) -> str:
    """Return :func:`app_state_dir` and create it if needed."""

    directory = app_state_dir(**kwargs)
    os.makedirs(directory, exist_ok=True)
    return directory


def folder_open_command(
    path: str | os.PathLike[str],
    *,
    platform_name: str | None = None,
) -> list[str]:
    """Build the native command used to open a directory."""

    platform_name = platform_name or _host_platform_name()
    value = os.fspath(path)
    if platform_name == "nt":
        return ["explorer.exe", value]
    if platform_name == "darwin":
        return ["open", value]
    if platform_name == "posix":
        return ["xdg-open", value]
    raise OSError(f"Opening folders is unsupported on platform {platform_name!r}.")


def open_folder(
    path: str | os.PathLike[str],
    *,
    platform_name: str | None = None,
) -> None:
    """Open an existing directory with the host's file manager.

    Windows uses ``os.startfile`` when available, preserving the shell
    integration users already have.  Unix-like systems use an argument-list
    subprocess so paths containing spaces or shell characters are safe.
    """

    platform_name = platform_name or _host_platform_name()
    folder = Path(path).expanduser()
    if not folder.is_dir():
        raise NotADirectoryError(f"Folder does not exist: {folder}")
    if platform_name == "nt":
        startfile = getattr(os, "startfile", None)
        if startfile is not None:
            startfile(str(folder))
            return
    command = folder_open_command(folder, platform_name=platform_name)
    subprocess.Popen(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        close_fds=platform_name != "nt",
        start_new_session=platform_name != "nt",
    )


def process_list_command(
    process_name: str | None = None,
    *,
    platform_name: str | None = None,
) -> list[str]:
    """Build a command that lists PIDs for the desktop process."""

    platform_name = platform_name or _host_platform_name()
    name = process_name or ("TotalRecalls.exe" if platform_name == "nt" else "TotalRecalls")
    if platform_name == "nt":
        return ["tasklist", "/FI", f"IMAGENAME eq {name}", "/FO", "CSV", "/NH"]
    if platform_name == "posix":
        return ["pgrep", "-x", name]
    raise OSError(f"Listing processes is unsupported on platform {platform_name!r}.")


def process_terminate_command(
    pid: int,
    *,
    force: bool = True,
    platform_name: str | None = None,
) -> list[str]:
    """Build a command that terminates one PID without invoking a shell."""

    if pid <= 0:
        raise ValueError("PID must be positive.")
    platform_name = platform_name or _host_platform_name()
    if platform_name == "nt":
        command = ["taskkill", "/PID", str(pid)]
        if force:
            command.append("/F")
        return command
    if platform_name == "posix":
        return ["kill", "-KILL" if force else "-TERM", str(pid)]
    raise OSError(f"Terminating processes is unsupported on platform {platform_name!r}.")


def parse_process_ids(output: str, *, platform_name: str | None = None) -> list[int]:
    """Parse the stdout from :func:`process_list_command`."""

    platform_name = platform_name or os.name
    if platform_name == "nt":
        values: list[int] = []
        for row in csv.reader(io.StringIO(output)):
            if len(row) < 2:
                continue
            try:
                values.append(int(row[1].strip()))
            except ValueError:
                continue
        return values
    values = []
    for line in output.splitlines():
        try:
            pid = int(line.strip())
        except ValueError:
            continue
        if pid > 0:
            values.append(pid)
    return values
