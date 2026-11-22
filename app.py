#!/usr/bin/env python3
"""
TotalRecalls / Perplexity Exporter — compatibility entrypoint.

Implementation lives under the `totalrecalls` package (Phase 2 split).
This module re-exports the public surface so existing tests, PyInstaller
(`app.py`), and imports like `from app import Bridge` keep working.
"""

from __future__ import annotations

import sys

from totalrecalls import APP_NAME, APP_VERSION, APP_BUILD_TAG

from totalrecalls.core.paths import (
    appdata_dir, _my_pid, kill_other_exporter_processes, acquire_single_instance,
    SESSION_FILE, LOG_FILE, SIGNIN_CALLBACK_FILE,
    _candidate_log_paths, log, save_session, load_session, clear_session,
    write_signin_callback, consume_signin_callback,
)
from totalrecalls.core.errors import friendly_error
from totalrecalls.core.export_fs import (
    HOME_SPACE_NAME, SPACES_DIRNAME, LEGACY_THREADS_DIRNAME,
    space_label_from_collection, safe_name, short_id, thread_folder_name,
    space_dir_name, thread_rel_path, thread_abs_folder,
    load_uuid_index, save_uuid_index, find_existing_thread_folder,
    entry_stats, write_conversation_markdown, build_space_readme,
    build_root_readme, write_export_indexes,
)
from totalrecalls.adapters.perplexity.http import (
    BASE, API_VERSION, USER_AGENT, DEFAULT_DELAY, MAX_RETRIES,
    RETRY_BASE, RETRY_MAX, PAGE_SIZE, COOKIE_NAME,
    ApiError, make_cookie_header, request, _HAS_CFFI,
)
# optional curl_cffi handle for tests that patch app._cffi_requests
try:
    from totalrecalls.adapters.perplexity import http as _pplx_http
    _cffi_requests = getattr(_pplx_http, "_cffi_requests", None)
except Exception:  # pragma: no cover
    _cffi_requests = None

from totalrecalls.adapters.perplexity.auth import (
    extract_session_token_from_cookie_header,
    extract_session_token_from_cookie_records,
    extract_session_token_from_cdp_json,
    validate_session,
    detect_session_token_from_browser_store,
)
from totalrecalls.adapters.perplexity.discover import (
    _normalize_thread_items, _thread_key, _merge_thread,
    list_spaces, list_threads,
    _discover_list_ask_threads, _discover_thread_list,
    _discover_thread_search, _discover_space_threads,
)
from totalrecalls.adapters.perplexity.thread import (
    get_thread, extract_entry, render_markdown,
)
from totalrecalls.desktop.ui_dispatch import dispatch_to_ui_thread
from totalrecalls.desktop.js_api import JsApi
from totalrecalls.desktop.bridge import Bridge
from totalrecalls.desktop.main import main

# Keep test patches on app.* working for Bridge internals that still bind
# names at import time inside totalrecalls.desktop.bridge — tests that
# patch app.validate_session / app.list_threads are updated to patch the
# bridge module symbols as well via aliases below used by legacy tests.
import totalrecalls.desktop.bridge as _bridge_mod
import totalrecalls.adapters.perplexity.http as _http_mod
import totalrecalls.core.paths as _paths_mod

def __getattr__(name: str):
    # Lazy alias so patch("app._HAS_CFFI") can still work if rebound
    if name == "_cffi_requests":
        return getattr(_http_mod, "_cffi_requests", None)
    raise AttributeError(name)

def _selftest(strict: bool = False) -> int:
    """Headless capability check for CI and packaging.

    The GUI entrypoint calls main(), which shows a modal "cannot start on this
    machine" dialog when the runtime is incomplete. On a headless runner that
    dialog never gets dismissed, so the job looks like a hang — which is how a
    CI run sat for six hours before being cancelled. This path reports to
    stdout and returns an exit status instead.

    Core checks must pass anywhere. GUI-runtime checks (pythonnet, WebView2)
    are only fatal in strict mode, because CI never installs the desktop stack
    but a shipped build must have it.
    """
    from totalrecalls.core import preflight

    problems = preflight.run()
    gui_markers = ("pythonnet", "WebView2")
    gui = [p for p in problems if any(m in p for m in gui_markers)]
    core = [p for p in problems if p not in gui]

    print(f"{APP_NAME} {APP_VERSION} selftest ({APP_BUILD_TAG or 'dev'})")
    print(f"  interpreter : {sys.executable}")
    print(f"  python      : {sys.version.split()[0]}")
    print(f"  package     : totalrecalls import ok")

    for p in core:
        print(f"  FAIL  {p}")
    for p in gui:
        print(f"  {'FAIL' if strict else 'WARN'}  {p}")

    if not core and not gui:
        print("  runtime     : desktop stack present")
    elif not strict and gui:
        print("  note        : GUI runtime is needed to *run* the app; CI checks core only.")

    if core or (strict and gui):
        print("selftest: FAILED")
        return 1
    print("selftest: ok")
    return 0


if __name__ == "__main__":
    _argv = sys.argv[1:]
    if "--selftest" in _argv:
        raise SystemExit(_selftest(strict="--strict" in _argv))
    main()
