"""Perplexity HTTP transport (curl_cffi preferred, urllib fallback)."""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request

from totalrecalls.core.paths import log

BASE = "https://www.perplexity.ai"
API_VERSION = "2.18"
USER_AGENT = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36")
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
    _HAS_CFFI = False


class ApiError(Exception):
    pass


def make_cookie_header(token: str) -> str:
    return f"{COOKIE_NAME}={token}"


def request(path: str, token: str, method: str = "GET", body: dict | None = None,
            delay: float = DEFAULT_DELAY) -> tuple[int, dict | list]:
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

    for attempt in range(MAX_RETRIES + 1):
        # Politeness delay applies BETWEEN requests, not before the first one.
        # Sleeping on attempt 0 added a flat 3s to every single call (connect
        # validate, list_conversations, every conversation fetch) with no
        # anti-ban benefit — pacing only matters once requests have flowed.
        if delay > 0 and attempt > 0:
            time.sleep(delay)
        try:
            return _one_attempt()
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504):
                backoff = min(RETRY_BASE * (2 ** attempt), RETRY_MAX)
                if e.code == 429:
                    backoff = max(backoff, 20.0)
                log(f"HTTP {e.code} on {path.split('?')[0]} — retry in {backoff:.0f}s")
                time.sleep(backoff)
                continue
            if e.code in (401, 403):
                raise ApiError("auth-failed")
            raise ApiError(f"http-{e.code}")
        except Exception as e:
            if isinstance(e, ApiError):
                raise
            if attempt < MAX_RETRIES:
                backoff = min(RETRY_BASE * (2 ** attempt), RETRY_MAX)
                log(f"network error ({type(e).__name__}) — retry in {backoff:.0f}s")
                time.sleep(backoff)
                continue
            raise ApiError("network")
    raise ApiError("network")

