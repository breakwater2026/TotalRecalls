#!/usr/bin/env python3
"""
TotalRecalls / Perplexity Exporter — compatibility entrypoint.

Implementation lives under the `totalrecalls` package (Phase 2 split).
This module re-exports the public surface so existing tests, PyInstaller
(`app.py`), and imports like `from app import Bridge` keep working.
"""

from __future__ import annotations

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

if __name__ == "__main__":
    main()
