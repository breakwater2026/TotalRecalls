"""Perplexity HTTP transport (curl_cffi preferred, urllib fallback)."""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from contextvars import ContextVar
from typing import Callable, Optional

from totalrecalls.core.paths import log

BASE = "https://www.perplexity.ai"
API_VERSION = "2.18"
USER_AGENT = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36")
DEFAULT_DELAY = 3.0          # seconds between requests — do NOT lower (session-kill risk)
MAX_RETRIES = 8
RETRY_BASE = 2.0
RETRY_MAX = 60.0
PAGE_SIZE = 20
COOKIE_NAME = "__Secure-next-auth.session-token"


try:
    from curl_cffi import requests as _cffi_requests
    _HAS_CFFI = True
except Exception:
    _cffi_requests = None  # type: ignore
    _HAS_CFFI = False


class ApiError(Exception):
    pass


# Contextvar sink for retry notifications (same pattern as
# adapters/chatgpt/http.py). The desktop bridge sets this at the start of an
# export so every retry in the (deep) listing can surface "provider servers
# busy — retrying" to the UI without threading a callback through ~10 function
# signatures. An explicit ``on_retry=`` argument on request() always wins.
_RETRY_SINK: ContextVar[Optional[Callable[[int, int, float], None]]] = ContextVar(
    "perplexity_retry_sink", default=None
)


def set_retry_sink(callback: Optional[Callable[[int, int, float], None]]):
    """Install (or clear, with None) the process-wide retry notification sink.
    Returns a token usable with :func:`reset_retry_sink`. The sink is a
    contextvar, so it is inherited by threads spawned from the setter and
    stays isolated per export worker."""
    return _RETRY_SINK.set(callback)


def reset_retry_sink(token) -> None:
    try:
        _RETRY_SINK.reset(token)
    except Exception:
        pass


def make_cookie_header(token: str) -> str:
    parts = [f"{COOKIE_NAME}={token}"]
    # Attach Cloudflare cookies captured at login — without cf_clearance,
    # Cloudflare challenges bare session cookies after ~10 rapid fetches.
    try:
        from totalrecalls.adapters.perplexity.auth import load_cf_cookies
        cf = load_cf_cookies()
        if cf:
            parts.append(cf)
    except Exception:
        pass
    return "; ".join(parts)


def request(path: str, token: str, method: str = "GET", body: dict | None = None,
            delay: float = DEFAULT_DELAY, stop_event=None,
            on_retry: Optional[Callable[[int, int, float], None]] = None) -> tuple[int, dict | list]:
    """Perform a request with retry/backoff.

    ``stop_event``: optional threading.Event for caller-side cancellation
    (the desktop bridge sets it on disconnect). Checked before every attempt
    AND before every sleep (politeness + backoff), so a disconnected UI stops
    the worker's in-flight retry chain within one check — no more orphaned
    retries (the 2026-09-15 re-shoot showed downloads continuing minutes
    after the user disconnected).

    ``on_retry``: optional callback ``(attempt, status_code, backoff_seconds)``
    invoked before each backoff sleep, so the caller can surface "the
    provider's servers are busy — retrying" to the UI. Falls back to the
    process-wide :func:`set_retry_sink` sink when not given.
    """
    if on_retry is None:
        on_retry = _RETRY_SINK.get()
    url = BASE + path
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
        "Cookie": make_cookie_header(token),
        "Referer": "https://www.perplexity.ai/",
        "Origin": "https://www.perplexity.ai",
    }
    data = None
    if body is not None:
        data = json.dumps(body).encode()
        headers["Content-Type"] = "application/json"

    def _one_attempt():
        if _HAS_CFFI:
            try:
                resp = _cffi_requests.request(method, url, data=data, headers=headers,
                                              timeout=60, impersonate="chrome131",
                                              allow_redirects=True)
                # curl_cffi does NOT raise on HTTP errors — convert status codes
                # to exceptions so the retry/auth logic below fires correctly
                if resp.status_code in (429, 500, 502, 503, 504):
                    raise urllib.error.HTTPError(url, resp.status_code, "retryable", {}, None)
                if resp.status_code in (401, 403):
                    raise urllib.error.HTTPError(url, resp.status_code, "auth", {}, None)
                raw = resp.content
                parsed = json.loads(raw.decode("utf-8", "replace")) if raw else None
                return resp.status_code, parsed
            except (UnicodeEncodeError, UnicodeDecodeError, ValueError) as e:
                log(f"request: curl_cffi failed ({type(e).__name__}) — falling back to stdlib urllib: {e}")

        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read()
            parsed = json.loads(raw.decode("utf-8", "replace")) if raw else None
            return resp.status, parsed

    def _cancelled():
        return stop_event is not None and stop_event.is_set()

    def _sleep(seconds: float):
        # Interruptible sleep: a set stop_event aborts early (ChatGPT's
        # http.request() uses plain time.sleep + pre-sleep checks; this is
        # strictly snappier — a disconnect stops within ~1s even mid-sleep).
        if stop_event is not None:
            stop_event.wait(seconds)
        else:
            time.sleep(seconds)

    for attempt in range(MAX_RETRIES + 1):
        if _cancelled():
            raise ApiError("cancelled")
        # Politeness delay applies BETWEEN requests, not before the first one.
        # Sleeping on attempt 0 added a flat 3s to every single call (connect
        # validate, list_conversations, every conversation fetch) with no
        # anti-ban benefit — pacing only matters once requests have flowed.
        if delay > 0 and attempt > 0:
            _sleep(delay)
            if _cancelled():
                raise ApiError("cancelled")
        try:
            return _one_attempt()
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504):
                backoff = min(RETRY_BASE * (2 ** attempt), RETRY_MAX)
                if e.code == 429:
                    backoff = max(backoff, 20.0)
                log(f"HTTP {e.code} on {path.split('?')[0]} — retry in {backoff:.0f}s")
                if on_retry:
                    try:
                        on_retry(attempt + 1, e.code, backoff)
                    except Exception:
                        pass
                _sleep(backoff)
                if _cancelled():
                    raise ApiError("cancelled")
                continue
            if e.code in (401, 403):
                # A genuinely dead session 401s on EVERY request — but listing
                # succeeded moments earlier. Transient 401/403 here is usually a
                # Cloudflare challenge; retry with backoff before giving up.
                if attempt < MAX_RETRIES:
                    backoff = min(RETRY_BASE * (2 ** attempt), RETRY_MAX)
                    log(f"HTTP {e.code} on {path.split('?')[0]} — challenge? retry in {backoff:.0f}s")
                    if on_retry:
                        try:
                            on_retry(attempt + 1, e.code, backoff)
                        except Exception:
                            pass
                    _sleep(backoff)
                    if _cancelled():
                        raise ApiError("cancelled")
                    continue
                raise ApiError("auth-failed")
            raise ApiError(f"http-{e.code}")
        except Exception as e:
            if isinstance(e, ApiError):
                raise
            if attempt < MAX_RETRIES:
                backoff = min(RETRY_BASE * (2 ** attempt), RETRY_MAX)
                log(f"network error ({type(e).__name__}) — retry in {backoff:.0f}s")
                if on_retry:
                    try:
                        on_retry(attempt + 1, 0, backoff)
                    except Exception:
                        pass
                _sleep(backoff)
                if _cancelled():
                    raise ApiError("cancelled")
                continue
            raise ApiError("network") from e
    raise ApiError("network")

