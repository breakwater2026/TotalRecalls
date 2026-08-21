"""Gemini adapter transport helpers.

Supports:
  1) Offline Google Takeout / exported JSON (preferred, stable)
  2) Live cookie credential (browser session via gemini.google.com)
"""

from __future__ import annotations

import hashlib
import base64
import json
import random
import re
import time
import uuid
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from totalrecalls.core.paths import log

BASE = "https://gemini.google.com"
APP_BASE = "https://gemini.google.com"
BATCH_EXECUTE = "https://gemini.google.com/_/BardChatUi/data/batchexecute"
LIST_CONVERSATIONS_RPC = "MaZiqc"
LIST_CONVERSATION_TURNS_RPC = "hNvQHb"
_BATCH_SESSION_ID = str(uuid.uuid4()).upper()
_BATCH_REQUEST_ID = random.randint(10000, 99999)
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
    # Google cookies may have __Secure-, __Host-, _Secure- or no prefix
    for prefix in ["__Secure-1PSID", "__Secure-1PSIDCC", "__Secure-1PAPISID",
                   "_Secure-1PSID", "_Secure-1PAPISID"]:
        if prefix + "=" in c:
            return True
    if "__Host-" in c:
        return True
    if c.startswith("eyJ") and c.count(".") >= 2:
        return True
    if "SID=" in c and "HSID=" in c:
        return True
    if c.startswith("__Secure-1PSID=") or c.startswith("_Secure-1PSID="):
        return True
    if "=" not in c and len(c) > 50 and not c.startswith("Bearer"):
        return True
    return False


def cookie_header_from_credential(credential: str) -> str:
    """Normalize a credential into a usable Cookie header string."""
    raw = (credential or "").strip().strip('"')
    if not raw:
        raise GeminiApiError("auth-failed")
    if "Cookie:" in raw or "__Secure-1PSID=" in raw or "__Host-" in raw or "NID=" in raw or "SID=" in raw:
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
      - HUGNlb/HUGLxb: API base URL (e.g. https://geminiweb-pa.clients6.google.com)
      - qKIAYe: feed path for conversation list (e.g. feeds/mcudyrk2a4khkz)
      - KnDnFf: feed path for conversation detail (e.g. feeds/nrij2vo2gajxiu)
      - API key: AIza... token

    Returns (base_url, list_rpc_path, api_key).
    """
    if not html:
        return None, None, None

    api_key = extract_api_key(html)

    # Extract HUGNlb (API base URL) — the real API server, not a static CDN
    # Key may appear as HUGNlb or HUGLxb depending on Google's build
    base_url = None
    for config_key in ["HUGNlb", "HUGLxb"]:
        for pattern in [
            rf'"{config_key}":"(https?://[^"]+)"',
            rf'\\"{config_key}\\":\\\"([^\\\"]+)',
        ]:
            m = re.search(pattern, html)
            if m:
                base_url = m.group(1).replace("\\", "")
                break
        if base_url:
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

    # Extract at token (Anti-XSRF) — needed for clients6 feed RPC calls
    # The key may be "SNlM0e" (Google's current format) or "thykhd" (older builds)
    at_token = None
    for token_key in ["SNlM0e", "thykhd"]:
        for pattern in [
            rf'"{token_key}":"([^"]+)"',
            rf'\\\\"{token_key}\\":\\"([^\\\\"]+)',
        ]:
            m = re.search(pattern, html)
            if m:
                at_token = m.group(1).replace("\\", "")
                break
        if at_token:
            break

    return base_url, rpc_path, api_key, at_token


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
                    impersonate="chrome151", allow_redirects=True,
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


def _extract_sapisid_hash(cookie: str) -> str:
    "Extract the SAPISID value from cookie string to compute SAPISIDHASH."
    for part in cookie.split(";"):
        part = part.strip()
        if "=" in part:
            name, value = part.split("=", 1)
            if name.strip() in ("SAPISID", "__Secure-1PAPISID", "__Secure-3PAPISID", "APISID"):
                return value
    return ""


def _build_sapisid_hash(sapisid: str, origin: str) -> str:
    "Compute Google's SAPISIDHASH for API authorization."
    timestamp = str(int(time.time()))
    raw = timestamp + origin + sapisid
    sha1_hash = hashlib.sha1(raw.encode("utf-8")).digest()
    b64_hash = base64.b64encode(sha1_hash).decode("ascii").rstrip("=")
    return f"{timestamp}_{b64_hash}"


def _make_rpc_request(rpc_url: str, rpc_body: bytes, cookie: str,
                      content_type: str = "application/x-www-form-urlencoded",
                      rpc_ids: str | None = None,
                      source_path: str = "/app") -> bytes:
    """POST an RPC body to the Gemini API endpoint."""
    # No synthetic CONSENT/SOCS injection — see note above
    # Add SAPISIDHASH for Google API authorization
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Type": content_type,
        "X-Same-Domain": "1",
        "Origin": "https://gemini.google.com",
        "Referer": "https://gemini.google.com/",
        "X-Goog-BatchExecute-Path": "/app",
        "X-Goog-Visitor-Id": "gemini",
        "X-Goog-AuthUser": "[]",
        "X-Goog-AuthServer": "1",
        "X-Goog-AuthMethod": "credentials",
        "Cookie": cookie,
        "x-goog-ext-525001261-jspb": json.dumps(
            [1, None, None, None, None, None, None, None, [4, 5, 6, 8],
             None, None, None, None, None, None, _BATCH_SESSION_ID]
        ),
        "x-goog-ext-73010989-jspb": "[0]",
    }
    
    # Compute and add SAPISIDHASH if we have a SAPISID cookie
    sapisid = _extract_sapisid_hash(cookie)
    if sapisid:
        origin = "https://gemini.google.com"
        sapisid_hash = _build_sapisid_hash(sapisid, origin)
        headers["Authorization"] = f"SAPISIDHASH {sapisid_hash}"
        log(f"gemini rpc: adding SAPISIDHASH auth header ({len(cookie.split(';'))} cookies)")

    cffi_error = None
    request_url = rpc_url
    if rpc_ids:
        global _BATCH_REQUEST_ID
        request_id = _BATCH_REQUEST_ID
        _BATCH_REQUEST_ID += 100000
        query = urllib.parse.urlencode({
            "rpcids": rpc_ids,
            "hl": "en",
            "_reqid": request_id,
            "rt": "c",
            "source-path": source_path,
        })
        request_url = f"{rpc_url}&{query}" if "?" in rpc_url else f"{rpc_url}?{query}"

    if _HAS_CFFI and _cffi_requests is not None:
        # Log full request details for debugging (headers names only, not values)
        header_names = list(headers.keys())
        log(f"gemini rpc request: POST {request_url[:100]}... headers={header_names} body_len={len(rpc_body)} body_type={type(rpc_body).__name__}")
        try:
            resp = _cffi_requests.post(
                request_url, data=rpc_body, headers=headers, timeout=60,
                impersonate="chrome151", allow_redirects=True,
            )
            if resp.status_code in (401, 403):
                raise GeminiApiError("auth-failed")
            if resp.status_code >= 400:
                log(f"gemini rpc HTTP {resp.status_code} on {request_url[:100]}... body={resp.text[:200]}")
                return b""
            return resp.content
        except GeminiApiError:
            raise
        except Exception as e:
            cffi_error = e
            log(f"gemini rpc cffi fail: {e}")
    # Fallback to urllib (less effective — Google may reject stdlib UA)
    try:
        req = urllib.request.Request(request_url, data=rpc_body, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.read()
    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            raise GeminiApiError("auth-failed")
        raise GeminiApiError(f"http-{e.code}") from e
    except Exception as e:
        log(f"gemini rpc urllib fail: {e} (cffi_error={cffi_error})")
        raise GeminiApiError("network") from e


def _batchexecute_body(rpc_id: str, payload: list, at_token: str | None) -> bytes:
    """Build the form body used by Gemini's BardChatUi RPC client."""
    rpc = [rpc_id, json.dumps(payload, separators=(",", ":")), None, "generic"]
    form = {
        "at": at_token or "",
        "f.req": json.dumps([[rpc]], separators=(",", ":")),
    }
    return urllib.parse.urlencode(form).encode("utf-8")


def _parse_batchexecute_response(raw: bytes) -> list:
    """Parse Google's XSSI-prefixed, length-framed batchexecute response."""
    text = raw.decode("utf-8", "replace").lstrip()
    if text.startswith(")]}'"):
        text = text[4:].lstrip("\r\n")

    frames: list = []
    offset = 0
    while offset < len(text):
        newline = text.find("\n", offset)
        if newline < 0:
            break
        length_text = text[offset:newline].strip()
        if not length_text.isdigit():
            break
        length = int(length_text)
        start = newline + 1
        frame = text[start:start + length]
        if len(frame) != length:
            break
        try:
            frames.append(json.loads(frame))
        except json.JSONDecodeError:
            pass
        offset = start + length
        while offset < len(text) and text[offset] in "\r\n":
            offset += 1

    if frames:
        return frames
    try:
        parsed = json.loads(text.strip())
    except json.JSONDecodeError as exc:
        raise GeminiApiError("http-empty") from exc
    return parsed if isinstance(parsed, list) else [parsed]


def _rpc_response_bodies(raw: bytes) -> list[list]:
    """Return decoded RPC body arrays from a batchexecute response."""
    bodies: list[list] = []
    for part in _parse_batchexecute_response(raw):
        if not isinstance(part, list) or len(part) < 3:
            continue
        body = part[2]
        if isinstance(body, str):
            try:
                body = json.loads(body)
            except json.JSONDecodeError:
                continue
        if isinstance(body, list):
            bodies.append(body)
    return bodies


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

    _, _, _, at_token = extract_page_config(html)
    params = urllib.parse.urlencode({"at": at_token or "", "rpcids": LIST_CONVERSATIONS_RPC})
    rpc_url = f"{BATCH_EXECUTE}?{params}"
    conversations: list[dict] = []
    for payload in ([13, None, [1, None, 1]], [13, None, [0, None, 1]]):
        raw = _make_rpc_request(
            rpc_url,
            _batchexecute_body(LIST_CONVERSATIONS_RPC, payload, at_token),
            cookie,
            "application/x-www-form-urlencoded;charset=UTF-8",
            LIST_CONVERSATIONS_RPC,
        )
        for body in _rpc_response_bodies(raw):
            chat_list = body[2] if len(body) > 2 else []
            if not isinstance(chat_list, list):
                continue
            for item in chat_list:
                if not isinstance(item, list) or len(item) < 2:
                    continue
                cid = str(item[0] or "")
                if not cid or any(existing["id"] == cid for existing in conversations):
                    continue
                timestamp = item[5] if len(item) > 5 else None
                updated_at = str(timestamp[0]) if isinstance(timestamp, list) and timestamp else ""
                conversations.append({
                    "id": cid,
                    "title": str(item[1] or "Gemini conversation").strip(),
                    "updated_at": updated_at,
                    "created_at": "",
                    "raw": item,
                })
    return conversations


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

    _, _, _, at_token = extract_page_config(html)
    params = urllib.parse.urlencode({"at": at_token or "", "rpcids": LIST_CONVERSATION_TURNS_RPC})
    rpc_url = f"{BATCH_EXECUTE}?{params}"
    rpc_body = _batchexecute_body(
        LIST_CONVERSATION_TURNS_RPC,
        [conv_id, 100, None, 1, [1], [4], None, 1],
        at_token,
    )

    try:
        raw = _make_rpc_request(
            rpc_url,
            rpc_body,
            cookie,
            "application/x-www-form-urlencoded;charset=UTF-8",
            LIST_CONVERSATION_TURNS_RPC,
        )
    except GeminiApiError:
        raise
    except Exception as e:
        log(f"gemini fetch cffi fail: {e}")
        # fall through to return None
        return None

    if not raw:
        raise GeminiApiError("auth-failed")

    try:
        bodies = _rpc_response_bodies(raw)
    except Exception:
        return None
    messages: list[dict] = []
    for body in bodies:
        turns = body[0] if body else []
        if not isinstance(turns, list):
            continue
        for turn in turns:
            if not isinstance(turn, list):
                continue
            turn_messages: list[dict] = []
            if len(turn) > 2 and isinstance(turn[2], list):
                user_text = turn[2][0][0] if turn[2] and isinstance(turn[2][0], list) and turn[2][0] else ""
                if user_text:
                    turn_messages.append({"role": "user", "content": str(user_text)})
            candidates = turn[3][0] if len(turn) > 3 and isinstance(turn[3], list) and turn[3] and isinstance(turn[3][0], list) else []
            if candidates and isinstance(candidates[0], list):
                candidate = candidates[0]
                text = candidate[1][0] if len(candidate) > 1 and isinstance(candidate[1], list) and candidate[1] else ""
                if text:
                    turn_messages.append({"role": "assistant", "content": str(text)})
            messages[0:0] = turn_messages
    return {"id": conv_id, "messages": messages}


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
