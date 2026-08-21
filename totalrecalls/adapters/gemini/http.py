"""Gemini adapter transport helpers.

Supports:
  1) Offline Google Takeout / exported JSON (preferred, stable)
  2) Live cookie credential (browser session via gemini.google.com)
"""

from __future__ import annotations

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


def extract_page_config(html: str) -> tuple[str | None, str | None, str | None, str | None, str | None, str | None]:
    """Extract RPC endpoint config from the Gemini page HTML.

    Returns (base_url, list_rpc_path, api_key, at_token, build_label, session_id):
      - at_token: SNlM0e anti-XSRF token (sent as the `at` form field)
      - build_label: cfb2h build identifier (sent as the `bl` query param)
      - session_id: FdrFJe frontend session id (sent as the `f.sid` query param)
    """
    if not html:
        return None, None, None, None, None, None

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

    # Extract at token (Anti-XSRF) — SNlM0e (current) or thykhd (older builds)
    at_token = None
    for token_key in ["SNlM0e", "thykhd"]:
        for pattern in [
            rf'"{token_key}":"([^"]+)"',
            rf'\\"{token_key}\\":\\"([^\\"]+)',
        ]:
            m = re.search(pattern, html)
            if m:
                at_token = m.group(1).replace("\\", "")
                break
        if at_token:
            break

    # Extract build label (cfb2h) and frontend session id (FdrFJe) — sent as
    # the `bl` and `f.sid` query params on batchexecute calls, mirroring the
    # gemini-webapi reference client.
    build_label = None
    m = re.search(r'"cfb2h":\s*"([^"]*)"', html)
    if m:
        build_label = m.group(1) or None

    session_id = None
    m = re.search(r'"FdrFJe":\s*"([^"]*)"', html)
    if m:
        session_id = m.group(1) or None

    return base_url, rpc_path, api_key, at_token, build_label, session_id


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
                    impersonate="chrome145", allow_redirects=True,
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


def _make_rpc_request(rpc_body: bytes, cookie: str, rpc_ids: str,
                      source_path: str = "/app",
                      build_label: str | None = None,
                      session_id: str | None = None) -> bytes:
    """POST a batchexecute RPC body to Gemini.

    Mirrors the gemini-webapi reference client exactly: BardChatUi
    batchexecute endpoint, form body with at + f.req, query params
    rpcids/hl/_reqid/rt/source-path (+bl/f.sid when the page provides
    them), and only the headers the real web client sends.  Extra
    headers (SAPISIDHASH Authorization, X-Goog-Auth*, etc.) are NOT
    sent — Google's gateway rejects requests that carry auth headers it
    didn't expect.
    """
    global _BATCH_REQUEST_ID
    request_id = _BATCH_REQUEST_ID
    _BATCH_REQUEST_ID += 100000

    params = {
        "rpcids": rpc_ids,
        "hl": "en",
        "_reqid": request_id,
        "rt": "c",
        "source-path": source_path,
    }
    if build_label:
        params["bl"] = build_label
    if session_id:
        params["f.sid"] = session_id
    request_url = f"{BATCH_EXECUTE}?{urllib.parse.urlencode(params)}"

    # Model header: the reference parses the base jsp array and appends
    # the client's own session UUID as the trailing element (17 total).
    model_header = [1, None, None, None, None, None, None, None, [4, 5, 6, 8],
                    None, None, None, None, None, None, None]
    model_header.append(_BATCH_SESSION_ID)
    headers = {
        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
        "Origin": "https://gemini.google.com",
        "Referer": "https://gemini.google.com/",
        "X-Same-Domain": "1",
        "Cookie": cookie,
        "x-goog-ext-525001261-jspb": json.dumps(model_header),
        "x-goog-ext-73010989-jspb": "[0]",
    }

    log(f"gemini rpc: POST batchexecute rpcids={rpc_ids} body_len={len(rpc_body)}")
    if _HAS_CFFI and _cffi_requests is not None:
        try:
            resp = _cffi_requests.post(
                request_url, data=rpc_body, headers=headers, timeout=60,
                impersonate="chrome145", allow_redirects=True,
            )
        except Exception as e:
            # Do NOT silently fall back to urllib — stdlib requests are
            # always rejected by Google and a silent fallback masks real
            # errors (this is what hid the chrome151 impersonate bug).
            log(f"gemini rpc cffi fail: {type(e).__name__}: {e}")
            raise GeminiApiError("network") from e
        if resp.status_code in (401, 403):
            raise GeminiApiError("auth-failed")
        if resp.status_code >= 400:
            log(f"gemini rpc HTTP {resp.status_code}: {resp.text[:200]}")
            return b""
        return resp.content
    # No curl_cffi available (tests / unusual environments)
    try:
        req = urllib.request.Request(request_url, data=rpc_body, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.read()
    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            raise GeminiApiError("auth-failed")
        raise GeminiApiError(f"http-{e.code}") from e
    except Exception as e:
        log(f"gemini rpc urllib fail: {e}")
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
    """Parse Google's XSSI-prefixed, length-framed batchexecute response.

    Each frame is ``<byte-length>\n<JSON>`` where the declared length
    INCLUDES the frame's trailing newline, so slicing exactly
    ``length`` chars and calling json.loads hits "Extra data" on the
    trailing \\n.  Use raw_decode to read one JSON value per frame.
    """
    text = raw.decode("utf-8", "replace").lstrip()
    if text.startswith(")]}'"):
        text = text[4:].lstrip("\r\n")

    decoder = json.JSONDecoder()
    frames: list = []
    offset = 0
    while offset < len(text):
        while offset < len(text) and text[offset] in " \t\r\n":
            offset += 1
        if offset >= len(text):
            break
        newline = text.find("\n", offset)
        if newline < 0:
            break
        length_text = text[offset:newline].strip()
        if not length_text.isdigit():
            break
        length = int(length_text)
        start = newline + 1
        try:
            obj, end = decoder.raw_decode(text, start)
            frames.append(obj)
            offset = end
        except json.JSONDecodeError:
            frame = text[start:start + length].strip()
            try:
                frames.append(json.loads(frame))
            except json.JSONDecodeError:
                pass
            offset = start + length

    if frames:
        return frames
    try:
        parsed = json.loads(text.strip())
    except json.JSONDecodeError as exc:
        raise GeminiApiError("http-empty") from exc
    return parsed if isinstance(parsed, list) else [parsed]


def _rpc_response_bodies(raw: bytes) -> list[list]:
    """Return decoded RPC body arrays from a batchexecute response.

    Google wraps each chunked frame as an ARRAY of envelopes:
    ``[["wrb.fr", rpcid, body, ...], ["di", ...], ["af.httprm", ...]]``.
    Only ``wrb.fr`` envelopes carry an RPC body.  A single bare envelope
    (test fixtures) is handled too.
    """
    bodies: list[list] = []
    for part in _parse_batchexecute_response(raw):
        if not isinstance(part, list):
            continue
        if part and part[0] == "wrb.fr":
            envelopes = [part]
        else:
            envelopes = part
        for env in envelopes:
            if not isinstance(env, list) or len(env) < 3 or env[0] != "wrb.fr":
                continue
            body = env[2]
            if isinstance(body, str):
                try:
                    body = json.loads(body)
                except json.JSONDecodeError:
                    continue
            if isinstance(body, list):
                bodies.append(body)
    return bodies


def _list_chats_page(cookie: str, at_token: str | None, build_label: str | None,
                     session_id: str | None, count: int,
                     continuation: str | None) -> tuple[list, str | None]:
    """One MaZiqc page. Returns (chat rows, next continuation token)."""
    raw = _make_rpc_request(
        _batchexecute_body(LIST_CONVERSATIONS_RPC, [count, continuation, [0, None, 1]], at_token),
        cookie,
        LIST_CONVERSATIONS_RPC,
        build_label=build_label,
        session_id=session_id,
    )
    chats: list = []
    token: str | None = None
    for body in _rpc_response_bodies(raw):
        if len(body) > 2 and isinstance(body[2], list):
            chats.extend(body[2])
        if len(body) > 1 and isinstance(body[1], str) and len(body[1]) > 30:
            token = body[1]
    return chats, token


def list_conversations_live(html: str, cookie: str, *, deep: bool = True) -> list[dict]:
    """Fetch Gemini conversations via the MaZiqc batchexecute RPC.

    Paginates with the continuation token (body slot 1) until exhausted.
    deep=True walks every page (50/page); deep=False fetches one page.
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

    _, _, _, at_token, build_label, session_id = extract_page_config(html)
    conversations: list[dict] = []
    seen: set[str] = set()
    continuation: str | None = None
    page = 0
    max_pages = 200 if deep else 1
    while page < max_pages:
        chats, continuation = _list_chats_page(
            cookie, at_token, build_label, session_id, 50, continuation)
        added = 0
        for item in chats:
            if not isinstance(item, list) or len(item) < 2:
                continue
            cid = str(item[0] or "")
            if not cid or cid in seen:
                continue
            seen.add(cid)
            timestamp = item[5] if len(item) > 5 else None
            updated_at = str(timestamp[0]) if isinstance(timestamp, list) and timestamp else ""
            conversations.append({
                "id": cid,
                "title": str(item[1] or "Gemini conversation").strip(),
                "updated_at": updated_at,
                "created_at": "",
                "raw": item,
            })
            added += 1
        page += 1
        if not continuation or added == 0:
            break
    log(f"gemini live list: {len(conversations)} conversation(s) in {page} page(s)")
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

    _, _, _, at_token, build_label, session_id = extract_page_config(html)
    rpc_body = _batchexecute_body(
        LIST_CONVERSATION_TURNS_RPC,
        [conv_id, 100, None, 1, [1], [4], None, 1],
        at_token,
    )

    try:
        raw = _make_rpc_request(
            rpc_body,
            cookie,
            LIST_CONVERSATION_TURNS_RPC,
            build_label=build_label,
            session_id=session_id,
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
    turn_timestamps: list[int] = []
    for body in bodies:
        turns = body[0] if body else []
        if not isinstance(turns, list):
            continue
        for turn in turns:
            if not isinstance(turn, list):
                continue
            # Per-turn epoch timestamp lives in slot 4: [seconds, nanos]
            if len(turn) > 4 and isinstance(turn[4], list) and turn[4] and isinstance(turn[4][0], (int, float)):
                turn_timestamps.append(int(turn[4][0]))
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
    result: dict = {"id": conv_id, "messages": messages}
    if turn_timestamps:
        result["created_at"] = str(min(turn_timestamps))
        result["updated_at"] = str(max(turn_timestamps))
    return result


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
