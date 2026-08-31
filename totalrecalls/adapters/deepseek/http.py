"""DeepSeek (chat.deepseek.com) web backend transport.

Verified against the reverse-engineered web-client spec (Aver005/deep-reverse,
live-captured 2026-06-27). Auth is a Bearer token in the `Authorization` header
(issued by POST /api/v0/users/login, re-read via GET /api/v0/users/current).
A `ds_session_id` cookie is accepted as a legacy fallback.

Every JSON response uses a two-level envelope:

    {"code": 0, "msg": "", "data": {"biz_code": 0, "biz_msg": "", "biz_data": …}}
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request

from totalrecalls.core.paths import log

BASE = "https://chat.deepseek.com"
DEFAULT_DELAY = 1.5
MAX_RETRIES = 6
RETRY_BASE = 2.0
RETRY_MAX = 45.0
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
)
# The web client sends x-app-version / x-client-version; the API may reject
# requests without a plausible client version.
APP_VERSION = "2.0.0"

try:
    from curl_cffi import requests as _cffi_requests
    _HAS_CFFI = True
except Exception:
    _cffi_requests = None  # type: ignore
    _HAS_CFFI = False


class DeepSeekApiError(Exception):
    pass


def looks_like_bearer(value: str) -> bool:
    """True for 'Bearer …' or a JWT (eyJ…) token string."""
    v = (value or "").strip()
    if v.lower().startswith("bearer "):
        return True
    return v.startswith("eyJ") and v.count(".") >= 2


def normalize_bearer(value: str) -> str:
    v = (value or "").strip()
    if v.lower().startswith("bearer "):
        return v[7:].strip()
    return v


def cookie_header_from_credential(credential: str) -> str:
    """Accept a raw cookie string or a 'Cookie: ...' line; return the bare cookie string."""
    raw = (credential or "").strip()
    if not raw:
        raise DeepSeekApiError("auth-failed")
    if raw.lower().startswith("cookie:"):
        return raw.split(":", 1)[1].strip()
    return raw


def _headers(cookie: str | None, access_token: str | None) -> dict[str, str]:
    h = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": BASE,
        "Referer": BASE + "/",
        "x-client-platform": "web",
        "x-client-bundle-id": "com.deepseek.chat",
        "x-app-version": APP_VERSION,
        "x-client-version": APP_VERSION,
    }
    if access_token:
        h["Authorization"] = f"Bearer {access_token}"
    if cookie:
        h["Cookie"] = cookie
    return h


def request(path: str, *, cookie: str | None = None,
            access_token: str | None = None,
            delay: float | None = None) -> tuple[int, object]:
    """Make one HTTP GET. Returns (status, parsed_json_or_text)."""
    url = path if path.startswith("http") else BASE + path
    if delay is None:
        delay = DEFAULT_DELAY
    last_err: Exception | None = None
    for attempt in range(MAX_RETRIES):
        if attempt > 0:
            wait = min(RETRY_MAX, RETRY_BASE * (2 ** (attempt - 1)))
            time.sleep(wait)
        time.sleep(delay)
        try:
            if _HAS_CFFI:
                r = _cffi_requests.get(url, headers=_headers(cookie, access_token), timeout=30)
                status = r.status_code
                try:
                    data = r.json()
                except Exception:
                    data = r.text
                return status, data
            req = urllib.request.Request(url, headers=_headers(cookie, access_token))
            with urllib.request.urlopen(req, timeout=30) as resp:
                status = resp.status
                body = resp.read().decode("utf-8", errors="replace")
            try:
                data = json.loads(body)
            except Exception:
                data = body
            return status, data
        except urllib.error.HTTPError as e:
            last_err = e
            if e.code in (401, 403):
                raise DeepSeekApiError(f"http-{e.code}") from e
            if e.code == 429:
                continue
        except Exception as e:
            last_err = e
            continue
    raise DeepSeekApiError(f"network: {last_err}")
