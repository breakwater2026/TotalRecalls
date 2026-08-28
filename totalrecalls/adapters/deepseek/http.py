"""DeepSeek (chat.deepseek.com) web backend transport.

Credential is a session cookie captured from the WebView2 login flow.
Endpoints are the same JSON surface the web app uses (NOT the
developer DeepSeek API at api-docs.deepseek.com).
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

try:
    from curl_cffi import requests as _cffi_requests
    _HAS_CFFI = True
except Exception:
    _cffi_requests = None  # type: ignore
    _HAS_CFFI = False


class DeepSeekApiError(Exception):
    pass


def cookie_header_from_credential(credential: str) -> str:
    """Accept a raw cookie string or a 'Cookie: ...' line; return the bare cookie string."""
    raw = (credential or "").strip()
    if not raw:
        raise DeepSeekApiError("auth-failed")
    if raw.lower().startswith("cookie:"):
        return raw.split(":", 1)[1].strip()
    return raw


def _headers(cookie: str) -> dict[str, str]:
    return {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": BASE,
        "Referer": BASE + "/",
        "Cookie": cookie,
    }


def request(path: str, *, cookie: str, delay: float | None = None) -> tuple[int, object]:
    """Make one HTTP request. Returns (status, parsed_json_or_text)."""
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
                r = _cffi_requests.get(url, headers=_headers(cookie), timeout=30)
                status = r.status_code
                try:
                    data = r.json()
                except Exception:
                    data = r.text
                return status, data
            req = urllib.request.Request(url, headers=_headers(cookie))
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
