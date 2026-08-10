"""Grok (xAI / grok.x.ai) web transport.

Credential: Bearer access token (eyJ…) or Cookie header from grok.x.ai / x.com.
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request

from totalrecalls.core.paths import log

BASE = "https://grok.x.ai"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
)
DEFAULT_DELAY = 1.25
MAX_RETRIES = 6

try:
    from curl_cffi import requests as _cffi_requests
    _HAS_CFFI = True
except Exception:
    _cffi_requests = None  # type: ignore
    _HAS_CFFI = False


class GrokApiError(Exception):
    pass


def looks_like_bearer(value: str) -> bool:
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
    raw = (credential or "").strip()
    if not raw:
        raise GrokApiError("auth-failed")
    if "Cookie:" in raw:
        return raw.split(":", 1)[-1].strip()
    if "=" in raw and not looks_like_bearer(raw):
        return raw
    raise GrokApiError("auth-failed")


def request(
    path: str,
    *,
    access_token: str | None = None,
    cookie: str | None = None,
    method: str = "GET",
    body: dict | None = None,
    delay: float = DEFAULT_DELAY,
    base: str = BASE,
) -> tuple[int, dict | list | None]:
    url = base + path if path.startswith("/") else path
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
        "Origin": base,
        "Referer": base + "/",
    }
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"
    if cookie:
        headers["Cookie"] = cookie
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
                log(f"grok cffi fail: {e}")
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
            if e.code in (429, 500, 502, 503, 504) and attempt < MAX_RETRIES:
                time.sleep(min(2 ** attempt * 2, 40))
                continue
            if e.code in (401, 403):
                raise GrokApiError("auth-failed")
            raise GrokApiError(f"http-{e.code}")
        except GrokApiError:
            raise
        except Exception as e:
            if attempt < MAX_RETRIES:
                time.sleep(min(2 ** attempt * 2, 40))
                continue
            raise GrokApiError("network") from e
    raise GrokApiError("network")
