"""ChatGPT / OpenAI web backend transport.

Uses the same browser-session surfaces the ChatGPT web app uses
(not the public Platform inference API). Credential is either:
  - a short-lived access token (Bearer), or
  - a session cookie value that we exchange via /api/auth/session.
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request

from totalrecalls.core.paths import log

BASE = "https://chatgpt.com"
DEFAULT_DELAY = 3.0   # ChatGPT rate-limits aggressively after ~3 rapid fetches (429 storm
                      # observed live 2026-08-24); 3s pacing avoids tripping it
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


class ChatGptApiError(Exception):
    pass


def _headers(access_token: str | None = None, cookie: str | None = None) -> dict[str, str]:
    h = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": BASE,
        "Referer": BASE + "/",
    }
    if access_token:
        h["Authorization"] = f"Bearer {access_token}"
    if cookie:
        h["Cookie"] = cookie
    return h


def request(
    path: str,
    *,
    access_token: str | None = None,
    cookie: str | None = None,
    method: str = "GET",
    body: dict | None = None,
    delay: float = DEFAULT_DELAY,
    base: str = BASE,
    max_retries: int | None = None,
) -> tuple[int, dict | list | None]:
    retries = MAX_RETRIES if max_retries is None else max(0, int(max_retries))
    url = base + path if path.startswith("/") else path
    headers = _headers(access_token=access_token, cookie=cookie)
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
                log(f"chatgpt request: cffi failed ({type(e).__name__}) — urllib fallback: {e}")

        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read()
            parsed = json.loads(raw.decode("utf-8", "replace")) if raw else None
            return resp.status, parsed

    for attempt in range(retries + 1):
        if delay > 0:
            time.sleep(delay)
        try:
            return _one()
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504):
                backoff = min(RETRY_BASE * (2 ** attempt), RETRY_MAX)
                if e.code == 429:
                    # ChatGPT's limiter needs real cooldowns — 15s retries kept
                    # re-tripping 429 for minutes (observed live 2026-08-24).
                    backoff = max(backoff, 30.0) + attempt * 10
                log(f"chatgpt HTTP {e.code} on {path.split('?')[0]} — retry in {backoff:.0f}s")
                time.sleep(backoff)
                continue
            if e.code in (401, 403):
                raise ChatGptApiError("auth-failed")
            raise ChatGptApiError(f"http-{e.code}")
        except ChatGptApiError:
            raise
        except Exception as e:
            if attempt < retries:
                backoff = min(RETRY_BASE * (2 ** attempt), RETRY_MAX)
                log(f"chatgpt network error ({type(e).__name__}) — retry in {backoff:.0f}s")
                time.sleep(backoff)
                continue
            raise ChatGptApiError("network") from e
    raise ChatGptApiError("network")
