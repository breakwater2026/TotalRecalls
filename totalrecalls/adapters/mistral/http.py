"""Mistral (chat.mistral.ai) web backend transport.

Credential is a session cookie captured from the WebView2 login flow.

chat.mistral.ai (Le Chat) exposes its web app API as tRPC under
``/api/trpc``.  Auth is the Ory Kratos session cookie (``ory_session_<id>``)
plus ancillary cookies; there is no Authorization header.  The client uses a
superjson transformer, so queries are sent as ``?input={"json": <input>}`` and
responses arrive wrapped as ``{"result": {"data": {"json": <payload>, "meta":
...}}``.
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request

from totalrecalls.core.paths import log

BASE = "https://chat.mistral.ai"
TRPC = BASE + "/api/trpc"
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


class MistralApiError(Exception):
    pass


def cookie_header_from_credential(credential: str) -> str:
    """Accept a raw cookie string or a 'Cookie: ...' line; return the bare cookie string."""
    raw = (credential or "").strip()
    if not raw:
        raise MistralApiError("auth-failed")
    if raw.lower().startswith("cookie:"):
        return raw.split(":", 1)[1].strip()
    return raw


def _headers(cookie: str) -> dict[str, str]:
    return {
        "User-Agent": USER_AGENT,
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": BASE,
        "Referer": BASE + "/",
        "Cookie": cookie,
    }


def request(path: str, *, cookie: str,
            delay: float | None = None) -> tuple[int, object]:
    """Make one HTTP GET. Returns (status, parsed_json_or_text).

    On 4xx returns (status, body) instead of raising, so the adapter can
    decide whether to retry, fail soft, or surface auth-failed.
    """
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
                r = _cffi_requests.get(url, headers=_headers(cookie), timeout=30,
                                       impersonate="chrome")
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
            if e.code == 429:
                continue  # rate limit — retry
            if 400 <= e.code < 500:
                body = ""
                try:
                    body = e.read().decode("utf-8", errors="replace")
                except Exception:
                    pass
                return e.code, body
            # 5xx — transient server error; fall through to retry
        except Exception as e:
            last_err = e
            continue
    raise MistralApiError(f"network: {last_err}")


def trpc_query(procedure: str, input_: dict, *, cookie: str,
               delay: float | None = None) -> tuple[int, object]:
    """Call a tRPC query procedure and return (status, unwrapped_payload).

    Uses the non-batch httpLink GET form (``?input={"json": <input>}``) which
    returns a single JSON document.  On success the payload is the superjson
    ``result.data.json`` value (the ``meta`` side-channel is dropped).  On a
    tRPC error the returned value is the ``error`` object.
    """
    payload = json.dumps({"json": input_})
    qs = urllib.parse.quote(payload)
    url = f"{TRPC}/{procedure}?input={qs}"
    status, data = request(url, cookie=cookie, delay=delay)
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except Exception:
            pass
    if isinstance(data, dict):
        if "error" in data:
            return status, data.get("error")
        result = data.get("result")
        if isinstance(result, dict):
            inner = result.get("data")
            if isinstance(inner, dict) and "json" in inner:
                return status, inner["json"]
            return status, inner
        return status, result
    return status, data
