"""Gemini adapter transport helpers.

Supports:
  1) Offline Google Takeout / exported JSON (preferred, stable)
  2) Live cookie credential (browser session via gemini.google.com)
"""

from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.request
from pathlib import Path

from totalrecalls.core.paths import log

BASE = "https://gemini.google.com"
APP_BASE = "https://gemini.google.com"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
)

DEFAULT_DELAY = 1.0
MAX_RETRIES = 6
RETRY_BASE = 2.0
RETRY_MAX = 30.0

try:
    from curl_cffi import requests as _cffi_requests
    _HAS_CFFI = True
except Exception:
    _cffi_requests = None  # type: ignore
    _HAS_CFFI = False


class GeminiApiError(Exception):
    pass


# ---------------------------------------------------------------------------
# Credential helpers
# ---------------------------------------------------------------------------

def looks_like_path(credential: str) -> bool:
    """Detect a Takeout file/dir path vs a live cookie/bearer credential."""
    c = (credential or "").strip().strip('"')
    if not c:
        return False
    p = Path(c)
    return (
        p.exists()
        or c.lower().endswith((".json", ".zip"))
        or "takeout" in c.lower()
    )


def looks_like_cookie(credential: str) -> bool:
    """Detect a raw cookie header / cookie value usable for live Gemini."""
    c = (credential or "").strip().strip('"')
    if not c:
        return False
    if "__Secure-1PSID=" in c:
        return True
    if c.startswith("eyJ") and c.count(".") >= 2:
        return True
    if c.startswith("__Secure-1PSID="):
        return True
    if "=" not in c and len(c) > 50 and not c.startswith("Bearer"):
        return True
    return False


def cookie_header_from_credential(credential: str) -> str:
    """Normalize a credential into a usable Cookie header string."""
    raw = (credential or "").strip().strip('"')
    if not raw:
        raise GeminiApiError("auth-failed")
    if "Cookie:" in raw or "__Secure-1PSID=" in raw or "__Host-" in raw or "NID=" in raw:
        return raw
    if "=" not in raw:
        return f"__Secure-1PSID={raw}"
    raise GeminiApiError("auth-failed")


# ---------------------------------------------------------------------------
# HTTP transport (curl_cffi with Chrome impersonation — bypasses Google
# anti-bot). Falls back to urllib but live Gemini almost always 401s with
# stdlib UA.
# ---------------------------------------------------------------------------

def request(
    path: str,
    cookie: str | None = None,
    *,
    delay: float = DEFAULT_DELAY,
    base: str = APP_BASE,
    max_retries: int = MAX_RETRIES,
) -> tuple[int, dict | list | None]:
    """GET *path* (relative to *base*) with live Gemini cookies.

    Returns (status_code, parsed_json_or_none).  Raises GeminiApiError
    only after retries are exhausted.
    """
    url = base + path if path.startswith("/") else path
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/x-component, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": APP_BASE + "/app",
        "Origin": APP_BASE,
    }
    if cookie:
        headers["Cookie"] = cookie

    def _one():
        if _HAS_CFFI and _cffi_requests is not None:
            try:
                resp = _cffi_requests.get(
                    url,
                    headers=headers,
                    timeout=60,
                    impersonate="chrome131",
                    allow_redirects=True,
                )
                code = resp.status_code
                raw = resp.content
                if not raw:
                    return code, None
                try:
                    parsed = json.loads(raw.decode("utf-8", "replace"))
                except Exception:
                    parsed = None
                return code, parsed
            except Exception as e:
                log(f"gemini cffi fail: {e}")
        req = urllib.request.Request(url, headers=headers, method="GET")
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read()
            parsed = json.loads(raw.decode("utf-8", "replace")) if raw else None
            return resp.status, parsed

    last_err: Exception | None = None
    for attempt in range(max_retries + 1):
        if delay > 0:
            time.sleep(delay)
        try:
            code, parsed = _one()
            if code in (429, 500, 502, 503, 504):
                backoff = min(RETRY_BASE * (2 ** attempt), RETRY_MAX)
                if code == 429:
                    backoff = max(backoff, 20.0)
                log(f"gemini HTTP {code} on {path} — retry in {backoff:.0f}s")
                time.sleep(backoff)
                continue
            if code in (401, 403):
                raise GeminiApiError("auth-failed")
            return code, parsed
        except urllib.error.HTTPError as e:
            if e.code in (401, 403):
                raise GeminiApiError("auth-failed")
            if e.code in (429, 500, 502, 503, 504) and attempt < max_retries:
                backoff = min(RETRY_BASE * (2 ** attempt), RETRY_MAX)
                time.sleep(backoff)
                continue
            last_err = e
            if attempt < max_retries:
                continue
            raise GeminiApiError(f"http-{e.code}") from e
        except GeminiApiError:
            raise
        except Exception as e:
            last_err = e
            if attempt < max_retries:
                backoff = min(RETRY_BASE * (2 ** attempt), RETRY_MAX)
                log(f"gemini network error ({type(e).__name__}) — retry in {backoff:.0f}s")
                time.sleep(backoff)
                continue
            raise GeminiApiError("network") from e
    raise GeminiApiError("network") from last_err


# ---------------------------------------------------------------------------
# Live connection helpers — extract endpoints dynamically from page config
# ---------------------------------------------------------------------------

# Google API keys always start with AIza
GOOGLE_API_KEY_PATTERN = r'AIza[A-Za-z0-9_\-]{30,}'


def extract_api_key(html: str) -> str | None:
    """Extract the embedded Gemini API key from the page HTML."""
    if not html:
        return None
    m = re.search(GOOGLE_API_KEY_PATTERN, html)
    if m:
        return m.group(0)
    return None


def extract_page_config(html: str) -> tuple[str | None, str | None, str | None]:
    """Extract the RPC base URL, RPC path, and API key from the Gemini page.

    The Gemini page embeds a JSON config blob (WIZ_global_data) with:
      - HUGLxb: API base URL (e.g. https://geminiweb-pa.clients6.google.com)
      - qKIAYe: feed path for conversation list (e.g. feeds/mcudyrk2a4khkz)
      - KnDnFf: feed path for conversation detail (e.g. feeds/nrij2vo2gajxiu)
      - API key: AIza... token

    Returns (base_url, list_rpc_path, api_key).
    """
    if not html:
        return None, None, None

    api_key = extract_api_key(html)

    # Extract HUGLxb (API base URL) — the real API server, not a static CDN
    base_url = None
    for pattern in [
        r'"HUGLxb":"(https?://[^"]+)"',
        r'\\"HUGLxb\\":\\"([^\\"]+)',
    ]:
        m = re.search(pattern, html)
        if m:
            base_url = m.group(1).replace('\\', '')
            break

    # Fallback to p9hQne (static CDN URL) if HUGLxb not found
    # Note: p9hQne is used for static JS/CSS, not API calls
    if not base_url:
        for pattern in [
            r'"p9hQne":"(https?://[^"]+)"',
            r'\\"p9hQne\\":\\"([^\\"]+)',
        ]:
            m = re.search(pattern, html)
            if m:
                base_url = m.group(1).replace('\\', '')
                break

    # Extract qKIAYe (feed RPC path) — may be deeply escaped
    rpc_path = None
    for pattern in [
        r'"qKIAYe":"([^"]+)"',
        r'\\"qKIAYe\\":\\"([^\\"]+)',
    ]:
        m = re.search(pattern, html)
        if m:
            rpc_path = m.group(1).replace('\\', '')
            break

    return base_url, rpc_path, api_key


def extract_detail_rpc_path(html: str) -> str | None:
    """Extract the detail RPC path (KnDnFf) for fetching a single conversation."""
    if not html:
        return None
    for pattern in [
        r'"KnDnFf":"([^"]+)"',
        r'\\"KnDnFf\\":\\"([^\\"]+)',
    ]:
        m = re.search(pattern, html)
        if m:
            return m.group(1).replace('\\', '')
    return None


def fetch_page_html(cookie: str, *, delay: float = 0) -> str | None:
    """Fetch the Gemini app page HTML (needed to extract API key + endpoints)."""
    url = APP_BASE + "/app"
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": (
            "text/html,application/xhtml+xml,application/xml;q=0.9,"
            "image/avif,image/webp,*/*;q=0.8"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": APP_BASE + "/app",
        "Origin": APP_BASE,
        "Cookie": cookie,
    }
    if delay > 0:
        time.sleep(delay)

    def _one():
        if _HAS_CFFI and _cffi_requests is not None:
            try:
                resp = _cffi_requests.get(
                    url, headers=headers, timeout=60,
                    impersonate="chrome131", allow_redirects=True,
                )
                if resp.status_code in (401, 403):
                    raise urllib.error.HTTPError(url, resp.status_code, "auth", {}, None)
                if resp.status_code >= 400:
                    raise urllib.error.HTTPError(url, resp.status_code, "http", {}, None)
                return resp.text or ""
            except (UnicodeEncodeError, UnicodeDecodeError, ValueError) as e:
                log(f"gemini page cffi fail: {e}")
        req = urllib.request.Request(url, headers=headers, method="GET")
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.read().decode("utf-8", "replace")

    last_err: Exception | None = None
    for attempt in range(MAX_RETRIES + 1):
        try:
            return _one()
        except urllib.error.HTTPError as e:
            if e.code in (401, 403):
                raise GeminiApiError("auth-failed")
            if e.code in (429, 500, 502, 503, 504) and attempt < MAX_RETRIES:
                backoff = min(RETRY_BASE * (2 ** attempt), RETRY_MAX)
                time.sleep(backoff)
                continue
            last_err = e
            if attempt < MAX_RETRIES:
                continue
            raise GeminiApiError(f"http-{e.code}") from e
        except GeminiApiError:
            raise
        except Exception as e:
            last_err = e
            if attempt < MAX_RETRIES:
                backoff = min(RETRY_BASE * (2 ** attempt), RETRY_MAX)
                time.sleep(backoff)
                continue
            raise GeminiApiError("network") from e
    raise GeminiApiError("network") from last_err


def _make_rpc_request(rpc_url: str, rpc_body: bytes, cookie: str) -> bytes:
    """POST an RPC body to the Gemini API endpoint."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Type": "application/json",
        "Referer": APP_BASE + "/app",
        "Origin": APP_BASE,
        "Cookie": cookie,
        "X-Goog-AuthUser": "[]",
        "X-Goog-AuthServer": "1",
        "X-Goog-AuthMethod": "credentials",
    }

    if _HAS_CFFI and _cffi_requests is not None:
        try:
            resp = _cffi_requests.post(
                rpc_url, data=rpc_body, headers=headers, timeout=60,
                impersonate="chrome131", allow_redirects=True,
            )
            if resp.status_code in (401, 403):
                raise GeminiApiError("auth-failed")
            if resp.status_code >= 400:
                log(f"gemini rpc HTTP {resp.status_code} on {rpc_url}")
                return b""
            return resp.content
        except Exception as e:
            log(f"gemini rpc cffi fail: {e}")
            # fall through to urllib
    req = urllib.request.Request(rpc_url, data=rpc_body, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def list_conversations_live(html: str, cookie: str) -> list[dict]:
    """Fetch the list of Gemini conversations using endpoints + key from the page.

    This mirrors what the browser does: GET /app to extract the API key and
    RPC endpoint config, then POST to the boq RPC endpoint with that key +
    cookie.
    """
    # Use cached page HTML if provided (from validate()), otherwise fetch fresh
    if not html:
        html = fetch_page_html(cookie, delay=0)
    if not html:
        raise GeminiApiError("auth-failed")
    api_key = extract_api_key(html)
    if not api_key:
        log("gemini live: could not extract API key from page HTML")
        raise GeminiApiError("auth-failed")

    base_url, rpc_path, _ = extract_page_config(html)
    if not base_url or not rpc_path:
        base_url = "https://geminiweb-pa.clients6.google.com"
        rpc_path = "feeds/mcudyrk2a4khkz"

    rpc_url = f"{base_url}{rpc_path}?key={api_key}"
    log(f"gemini live: calling {rpc_url[:80]}...")

    rpc_body = json.dumps([
        {"method": "gem.conversation.list", "params": {"page_size": 100}}
    ]).encode("utf-8")

    try:
        raw = _make_rpc_request(rpc_url, rpc_body, cookie)
    except GeminiApiError:
        raise
    except Exception as e:
        log(f"gemini live list failed: {e}")
        raise GeminiApiError("network")

    if not raw:
        # Google returns 404 for expired/unauthorized sessions on these
        # internal endpoints — treat it as auth failure, not network error
        raise GeminiApiError("auth-failed")

    try:
        result = json.loads(raw.decode("utf-8", "replace"))
    except Exception:
        return []

    conversations = []
    if isinstance(result, list) and len(result) > 0:
        outer = result[0]
        if isinstance(outer, dict):
            if isinstance(outer.get("result"), list):
                conversations = outer["result"]
            elif isinstance(outer.get("result"), dict):
                r = outer["result"]
                if isinstance(r.get("conversations"), list):
                    conversations = r["conversations"]
                elif "conversations" in outer:
                    conversations = outer["conversations"]

    out = []
    for item in conversations:
        if not isinstance(item, dict):
            continue
        cid = str(item.get("id") or item.get("conversationId") or item.get("uuid") or "")
        if not cid:
            continue
        title = str(item.get("title") or item.get("name") or "Gemini conversation")
        out.append({
            "id": cid,
            "title": title.strip() or "Gemini conversation",
            "updated_at": str(item.get("updated_at") or item.get("modifiedTime") or item.get("updatedTime") or ""),
            "created_at": str(item.get("created_at") or item.get("createTime") or item.get("createdTime") or ""),
            "raw": item,
        })
    return out


def fetch_conversation_live(html: str, cookie: str, conv_id: str) -> dict | None:
    """Fetch a single Gemini conversation by ID using the live API."""
    # Use cached page HTML if provided (from validate()), otherwise fetch fresh
    if not html:
        html = fetch_page_html(cookie, delay=0)
    if not html:
        raise GeminiApiError("auth-failed")
    api_key = extract_api_key(html)
    if not api_key:
        raise GeminiApiError("auth-failed")

    base_url, _, _ = extract_page_config(html)
    detail_rpc_path = extract_detail_rpc_path(html)
    if not base_url:
        base_url = "https://geminiweb-pa.clients6.google.com"
    if not detail_rpc_path:
        detail_rpc_path = "feeds/nrij2vo2gajxiu"

    rpc_url = f"{base_url}{detail_rpc_path}?key={api_key}"
    rpc_body = json.dumps([
        {"method": "gem.conversation.get", "params": {"conversation_id": conv_id, "page_size": 100}}
    ]).encode("utf-8")

    try:
        raw = _make_rpc_request(rpc_url, rpc_body, cookie)
    except GeminiApiError:
        raise
    except Exception as e:
        log(f"gemini fetch cffi fail: {e}")
        # fall through to return None
        return None

    if not raw:
        raise GeminiApiError("auth-failed")

    try:
        result = json.loads(raw.decode("utf-8", "replace"))
    except Exception:
        return None

    detail = None
    if isinstance(result, list) and len(result) > 0:
        outer = result[0]
        if isinstance(outer, dict):
            if isinstance(outer.get("result"), dict):
                detail = outer["result"]
            elif "conversation" in outer:
                detail = outer["conversation"]
    if not detail and isinstance(result, dict):
        if isinstance(result.get("result"), dict):
            detail = result["result"]
        elif "conversation" in result:
            detail = result["conversation"]
    if not detail:
        detail = {"id": conv_id, "messages": []}
    return detail


# ---------------------------------------------------------------------------
# Offline (Takeout) export loader — unchanged
# ---------------------------------------------------------------------------

def load_offline_export(path_str: str) -> list[dict]:
    """Load conversations from a Takeout-like JSON file or directory."""
    path = Path(path_str.strip().strip('"')).expanduser()
    if not path.exists():
        raise GeminiApiError("auth-failed")
    candidates: list[Path] = []
    if path.is_file():
        candidates = [path]
    else:
        for pattern in (
            "**/Gemini/**/*.json",
            "**/My Activity/**/Gemini*.json",
            "**/*gemini*.json",
            "**/*Gemini*.json",
            "**/conversations.json",
            "**/*.json",
        ):
            candidates.extend(list(path.glob(pattern)[:50]))
        seen = set()
        uniq = []
        for c in candidates:
            s = str(c.resolve())
            if s not in seen:
                seen.add(s)
                uniq.append(c)
        candidates = uniq[:80]

    conversations: list[dict] = []
    for fp in candidates:
        try:
            if fp.suffix.lower() != ".json" or fp.stat().st_size > 80_000_000:
                continue
            data = json.loads(fp.read_text(encoding="utf-8", errors="replace"))
        except Exception:
            continue
        conversations.extend(_normalize_offline_payload(data, source=str(fp)))
    if not conversations:
        raise GeminiApiError("auth-failed")
    log(f"gemini offline: loaded {len(conversations)} conversation(s) from {path}")
    return conversations


def _normalize_offline_payload(data, *, source: str) -> list[dict]:
    out: list[dict] = []
    if isinstance(data, list):
        for i, item in enumerate(data):
            if isinstance(item, dict):
                out.append(_coerce_offline_item(item, fallback_id=f"{Path(source).stem}-{i}"))
        return [x for x in out if x]
    if isinstance(data, dict):
        if any(k in data for k in ("messages", "turns", "chat", "conversation")):
            item = _coerce_offline_item(data, fallback_id=Path(source).stem)
            return [item] if item else []
        for key in ("conversations", "chats", "items", "activities"):
            val = data.get(key)
            if isinstance(val, list):
                for i, item in enumerate(val):
                    if isinstance(item, dict):
                        c = _coerce_offline_item(item, fallback_id=f"{key}-{i}")
                        if c:
                            out.append(c)
        return out
    return []


def _coerce_offline_item(item: dict, *, fallback_id: str) -> dict | None:
    cid = str(item.get("id") or item.get("conversation_id") or item.get("uuid") or fallback_id)
    title = str(item.get("title") or item.get("name") or item.get("prompt") or "Gemini conversation")
    messages = item.get("messages") or item.get("turns") or item.get("chat") or []
    if not messages and (item.get("title") or item.get("html")):
        messages = []
        if item.get("title"):
            messages.append({"role": "user", "content": str(item.get("title"))})
        body = item.get("html") or item.get("content") or item.get("text")
        if body:
            messages.append({"role": "assistant", "content": str(body)})
    if not messages and not title:
        return None
    return {
        "id": cid,
        "title": title[:200],
        "messages": messages if isinstance(messages, list) else [],
        "updated_at": str(item.get("updated_at") or item.get("time") or item.get("timestamp") or ""),
        "created_at": str(item.get("created_at") or ""),
        "_source": "offline",
        "raw": item,
    }
