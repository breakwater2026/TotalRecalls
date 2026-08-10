"""Perplexity provider adapter (engine ported from v1 app.py)."""

from totalrecalls.adapters.perplexity.http import (
    BASE, API_VERSION, USER_AGENT, DEFAULT_DELAY, MAX_RETRIES,
    RETRY_BASE, RETRY_MAX, PAGE_SIZE, COOKIE_NAME,
    ApiError, make_cookie_header, request, _HAS_CFFI,
)
from totalrecalls.adapters.perplexity.auth import (
    extract_session_token_from_cookie_header,
    extract_session_token_from_cookie_records,
    extract_session_token_from_cdp_json,
    validate_session,
    detect_session_token_from_browser_store,
)
from totalrecalls.adapters.perplexity.discover import (
    list_spaces, list_threads,
    _normalize_thread_items, _thread_key, _merge_thread,
    _discover_list_ask_threads, _discover_thread_list,
    _discover_thread_search, _discover_space_threads,
)
from totalrecalls.adapters.perplexity.thread import (
    get_thread, extract_entry, render_markdown,
)

__all__ = [
    "BASE", "API_VERSION", "COOKIE_NAME", "DEFAULT_DELAY",
    "ApiError", "request", "validate_session",
    "list_threads", "list_spaces", "get_thread",
    "extract_entry", "render_markdown",
    "extract_session_token_from_cookie_header",
    "extract_session_token_from_cookie_records",
    "extract_session_token_from_cdp_json",
]
