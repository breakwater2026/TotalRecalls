"""Claude.ai web backend transport (not the public Anthropic Messages API).

Credential is typically the `sessionKey` cookie value from claude.ai, or a
full Cookie header containing it.
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request

from totalrecalls.core.paths import log

BASE = "https://claude.ai"
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


class ClaudeApiError(Exception):
    pass


def cookie_header_from_credential(credential: str) -> str:
    raw = (credential or "").strip()
    if not raw:
        raise ClaudeApiError("auth-failed")
    if "sessionKey=" in raw or "Cookie:" in raw:
        return raw.split(":", 1)[-1].strip() if raw.lower().startswith("cookie:") else raw
    # bare sessionKey value
    if raw.startswith("sk-ant-"):
        return f"sessionKey={raw}"
    return f"sessionKey={raw}"


def _headers(cookie: str) -> dict[str, str]:
    return {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": BASE,
        "Referer": BASE + "/",
        "Cookie": cookie,
    }


def request(
    path: str,
    cookie: str,
    *,
    method: str = "GET",
    body: dict | None = None,
    delay: float = DEFAULT_DELAY,
) -> tuple[int, dict | list | None]:
    url = BASE + path if path.startswith("/") else path
    headers = _headers(cookie)
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"

    def _one():
        if _HAS_CFFI and _cffi_requests is not None:
            try:
                resp = _cffi_requests.request(
                    method, url, data=data, headers=headers,
                    timeout=60, impersonate="chrome131", allow_redirects=True,
                )
                if resp.status_code in (429, 500, 502, 503, 504):
                    raise urllib.error.HTTPError(url, resp.status_code, "retryable", {}, None)
                if resp.status_code in (401, 403):
                    raise urllib.error.HTTPError(url, resp.status_code, "auth", {}, None)
                raw = resp.content
                parsed = json.loads(raw.decode("utf-8", "replace")) if raw else None
                return resp.status_code, parsed
            except (UnicodeEncodeError, UnicodeDecodeError, ValueError) as e:
                log(f"claude request: cffi failed ({type(e).__name__}) — urllib fallback: {e}")

        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read()
            parsed = json.loads(raw.decode("utf-8", "replace")) if raw else None
            return resp.status, parsed

    for attempt in range(MAX_RETRIES + 1):
        if delay > 0:
            time.sleep(delay)
        try:
            return _one()
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504):
                backoff = min(RETRY_BASE * (2 ** attempt), RETRY_MAX)
                if e.code == 429:
                    backoff = max(backoff, 15.0)
                log(f"claude HTTP {e.code} on {path.split('?')[0]} — retry {backoff:.0f}s")
                time.sleep(backoff)
                continue
            if e.code in (401, 403):
                raise ClaudeApiError("auth-failed")
            raise ClaudeApiError(f"http-{e.code}")
        except ClaudeApiError:
            raise
        except Exception as e:
            if attempt < MAX_RETRIES:
                backoff = min(RETRY_BASE * (2 ** attempt), RETRY_MAX)
                log(f"claude network ({type(e).__name__}) — retry {backoff:.0f}s")
                time.sleep(backoff)
                continue
            raise ClaudeApiError("network") from e
    raise ClaudeApiError("network")
