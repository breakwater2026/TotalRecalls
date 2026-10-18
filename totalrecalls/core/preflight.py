"""Startup capability self-check.

Why: a build whose runtime cannot dispatch WebView2/WinForms events looks
perfectly healthy — the window opens, pages load — until a login flow silently
never ticks. That failure produced hours of misdiagnosis on 2026-10-17 because
nothing anywhere said "pythonnet is not usable here".

`run()` never raises. It returns a list of human-readable problems; an empty
list means every capability we depend on is present.
"""

from __future__ import annotations

import sys


def _webview2_version() -> str:
    """Installed Evergreen WebView2 runtime version, or '' if absent."""
    try:
        import winreg
    except Exception:
        return ""
    key = r"Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}"
    for hive in (winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER):
        for prefix in (r"SOFTWARE\WOW6432Node" + "\\", r"SOFTWARE" + "\\"):
            try:
                with winreg.OpenKey(hive, prefix + key) as k:
                    value = winreg.QueryValueEx(k, "pv")[0]
                if value:
                    return str(value)
            except OSError:
                continue
    return ""


def _pythonnet_version() -> str:
    try:
        import importlib.metadata as md
        return md.version("pythonnet")
    except Exception:
        return ""


def run() -> list[str]:
    """Return a list of missing capabilities (empty list = healthy)."""
    problems: list[str] = []

    if sys.version_info[:2] < (3, 10):
        problems.append(f"Python {sys.version.split()[0]} is too old (need 3.10+)")

    # The one that bit us: without a working `clr`, pythonnet cannot attach any
    # .NET event handler, so login flows hang with no error at all.
    try:
        import clr  # noqa: F401
    except Exception as e:
        problems.append(
            f"pythonnet is not usable in this interpreter ({type(e).__name__}: {e}). "
            f"Interpreter: {sys.executable}"
        )
    else:
        ver = _pythonnet_version()
        if not ver:
            problems.append("pythonnet imported but its version could not be read")

    if not _webview2_version():
        problems.append("Microsoft Edge WebView2 runtime not found")

    return problems
