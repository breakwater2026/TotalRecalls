"""App data paths, logging, session persistence, single-instance guard."""

from __future__ import annotations

import os
import time
from datetime import datetime, timezone

from totalrecalls.core.platform import (
    app_state_dir,
    parse_process_ids,
    process_list_command,
    process_terminate_command,
)
from totalrecalls.core.secure_storage import (
    SecureStorageError,
    delete as delete_secure_state,
    load_json,
    save_json,
)


def appdata_dir() -> str:
    d = app_state_dir()
    os.makedirs(d, exist_ok=True)
    return d


def _my_pid() -> int:
    try:
        return os.getpid()
    except Exception:
        return 0


def kill_other_exporter_processes(force: bool = True) -> list[int]:
    """Terminate other PerplexityExporter.exe processes (not this PID).

    Used at startup (take over from stale instances) and before deep export
    discovery so a leftover GUI cannot keep the old build on screen.
    """
    killed: list[int] = []
    me = _my_pid()
    try:
        import subprocess
        process_name = "TotalRecalls.exe" if os.name == "nt" else "TotalRecalls"
        r = subprocess.run(
            process_list_command(process_name),
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
        for pid in parse_process_ids(r.stdout or ""):
            if pid == me or pid <= 0:
                continue
            kr = subprocess.run(
                process_terminate_command(pid, force=force),
                capture_output=True,
                text=True,
                timeout=15,
                check=False,
            )
            if kr.returncode == 0:
                killed.append(pid)
                log(f"killed other exporter pid={pid}")
            else:
                log(f"could not kill exporter pid={pid}: {(kr.stderr or kr.stdout or '').strip()}")
    except Exception as e:
        log(f"kill_other_exporter_processes failed: {e}")
    if killed:
        # Let the OS release the mutex / WebView2 locks
        time.sleep(1.2)
    return killed


def acquire_single_instance(takeover: bool = True) -> tuple[object | None, bool]:
    """Acquire the app mutex. If another instance owns it and takeover=True,
    kill sibling PerplexityExporter.exe processes and retry once.
    """
    if os.name != "nt":
        return None, True
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        mutex_name = "Global\\\\TotalRecalls_Instance"

        def _try():
            # Clear last error so ERROR_ALREADY_EXISTS is trustworthy
            kernel32.SetLastError(0)
            handle = kernel32.CreateMutexW(None, False, mutex_name)
            if handle is None or handle == 0:
                return None, True
            error = kernel32.GetLastError()
            if error == 183:  # ERROR_ALREADY_EXISTS
                try:
                    kernel32.CloseHandle(handle)
                except Exception:
                    pass
                return None, False
            return handle, True

        handle, primary = _try()
        if primary:
            return handle, True

        if not takeover:
            log("another PerplexityExporter instance is already running; exiting (no takeover)")
            return None, False

        log("another instance detected — taking over (killing siblings)")
        killed = kill_other_exporter_processes(force=True)
        log(f"takeover: killed {len(killed)} process(es): {killed}")
        # Mutex may linger briefly after process death
        for attempt in range(8):
            time.sleep(0.4)
            handle, primary = _try()
            if primary:
                log(f"takeover: acquired mutex on attempt {attempt + 1}")
                return handle, True
        log("takeover: failed to acquire mutex after killing siblings")
        return None, False
    except Exception as e:
        log(f"single-instance guard unavailable: {e}")
        return None, True


SESSION_FILE = os.path.join(appdata_dir(), "session.json")
LOG_FILE = os.path.join(appdata_dir(), "app.log")
SIGNIN_CALLBACK_FILE = os.path.join(appdata_dir(), "signin_callback.json")


def _candidate_log_paths() -> list[str]:
    candidates = [LOG_FILE]
    appdata = os.environ.get("APPDATA")
    if appdata:
        candidates.append(os.path.join(appdata, "PerplexityExporter", "app.log"))
    local_appdata = os.environ.get("LOCALAPPDATA")
    if local_appdata:
        candidates.append(os.path.join(local_appdata, "PerplexityExporter", "app.log"))
    cwd = os.getcwd()
    if cwd:
        candidates.append(os.path.join(cwd, "app.log"))
    return list(dict.fromkeys(candidates))


def log(msg: str):
    for candidate in _candidate_log_paths():
        try:
            directory = os.path.dirname(candidate)
            if directory:
                os.makedirs(directory, exist_ok=True)
            with open(candidate, "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now().isoformat(timespec='seconds')}] {msg}\n")
            return
        except Exception:
            continue


def save_session(token: str, email: str):
    save_json(
        SESSION_FILE,
        {
            "token": token,
            "email": email,
            "saved_at": datetime.now(timezone.utc).isoformat(),
        },
    )


def load_session() -> dict | None:
    try:
        return load_json(SESSION_FILE)
    except SecureStorageError as exc:
        log(f"could not load protected session: {exc}")
        return None


def clear_session():
    try:
        delete_secure_state(SESSION_FILE)
    except SecureStorageError as exc:
        log(f"could not clear protected session: {exc}")


def write_signin_callback(token: str):
    try:
        save_json(
            SIGNIN_CALLBACK_FILE,
            {
                "token": token,
                "saved_at": datetime.now(timezone.utc).isoformat(),
            },
        )
    except SecureStorageError as exc:
        log(f"could not save protected sign-in callback: {exc}")


def consume_signin_callback() -> str | None:
    try:
        payload = load_json(SIGNIN_CALLBACK_FILE)
        if payload is None:
            return None
        token = (payload or {}).get("token")
        if token:
            delete_secure_state(SIGNIN_CALLBACK_FILE)
            return str(token)
    except SecureStorageError as exc:
        log(f"could not consume protected sign-in callback: {exc}")
    return None
