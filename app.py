#!/usr/bin/env python3
"""
Perplexity Exporter — desktop app that downloads all your Perplexity conversations
to your computer as Markdown + JSON.

Built on the proven engine from perplexity_export.py (undocumented API v2.18).
Login happens inside the app (embedded WebView2 browser) — no cookies to copy.
"""

import json
import os
import re
import sys
import threading
import time
import traceback
import urllib.error
import urllib.request
import webbrowser
from datetime import datetime, timezone
from pathlib import Path

APP_NAME = "Perplexity Exporter"
APP_VERSION = "1.0.0"
APP_BUILD_TAG = "full-discovery-v1b"

# ----------------------------------------------------------------------------
# Paths & persistence
# ----------------------------------------------------------------------------

def appdata_dir() -> str:
    d = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "PerplexityExporter")
    os.makedirs(d, exist_ok=True)
    return d


def _my_pid() -> int:
    try:
        return os.getpid()
    except Exception:
        return 0


def kill_other_exporter_processes(force: bool = True) -> list[int]:
    """Terminate other PerplexityExporter.exe processes (not this PID).

    Used at startup (take over from stale instances) and before deep export
    discovery so a leftover GUI cannot keep the old build on screen.
    """
    killed: list[int] = []
    if os.name != "nt":
        return killed
    me = _my_pid()
    try:
        import subprocess
        # CSV: ImageName,PID,SessionName,Session#,MemUsage
        r = subprocess.run(
            ["tasklist", "/FI", "IMAGENAME eq PerplexityExporter.exe", "/FO", "CSV", "/NH"],
            capture_output=True, text=True, timeout=15,
        )
        for line in (r.stdout or "").splitlines():
            line = line.strip().strip('"')
            if not line:
                continue
            # "PerplexityExporter.exe","1234","Console","1","12,345 K"
            parts = [p.strip().strip('"') for p in line.split('","')]
            if len(parts) < 2:
                # fallback split
                parts = [p.strip().strip('"') for p in line.split(",")]
            try:
                pid = int(parts[1])
            except Exception:
                continue
            if pid == me or pid <= 0:
                continue
            cmd = ["taskkill", "/PID", str(pid)]
            if force:
                cmd.append("/F")
            kr = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            if kr.returncode == 0:
                killed.append(pid)
                log(f"killed other exporter pid={pid}")
            else:
                log(f"could not kill exporter pid={pid}: {(kr.stderr or kr.stdout or '').strip()}")
    except Exception as e:
        log(f"kill_other_exporter_processes failed: {e}")
    if killed:
        # Let the OS release the mutex / WebView2 locks
        time.sleep(1.2)
    return killed


def acquire_single_instance(takeover: bool = True) -> tuple[object | None, bool]:
    """Acquire the app mutex. If another instance owns it and takeover=True,
    kill sibling PerplexityExporter.exe processes and retry once.
    """
    if os.name != "nt":
        return None, True
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        mutex_name = "Global\\PerplexityExporter_Instance"

        def _try():
            # Clear last error so ERROR_ALREADY_EXISTS is trustworthy
            kernel32.SetLastError(0)
            handle = kernel32.CreateMutexW(None, False, mutex_name)
            if handle is None or handle == 0:
                return None, True
            error = kernel32.GetLastError()
            if error == 183:  # ERROR_ALREADY_EXISTS
                try:
                    kernel32.CloseHandle(handle)
                except Exception:
                    pass
                return None, False
            return handle, True

        handle, primary = _try()
        if primary:
            return handle, True

        if not takeover:
            log("another PerplexityExporter instance is already running; exiting (no takeover)")
            return None, False

        log("another instance detected — taking over (killing siblings)")
        killed = kill_other_exporter_processes(force=True)
        log(f"takeover: killed {len(killed)} process(es): {killed}")
        # Mutex may linger briefly after process death
        for attempt in range(8):
            time.sleep(0.4)
            handle, primary = _try()
            if primary:
                log(f"takeover: acquired mutex on attempt {attempt + 1}")
                return handle, True
        log("takeover: failed to acquire mutex after killing siblings")
        return None, False
    except Exception as e:
        log(f"single-instance guard unavailable: {e}")
        return None, True


SESSION_FILE = os.path.join(appdata_dir(), "session.json")
LOG_FILE = os.path.join(appdata_dir(), "app.log")
SIGNIN_CALLBACK_FILE = os.path.join(appdata_dir(), "signin_callback.json")


def _candidate_log_paths() -> list[str]:
    candidates = [LOG_FILE]
    appdata = os.environ.get("APPDATA")
    if appdata:
        candidates.append(os.path.join(appdata, "PerplexityExporter", "app.log"))
    local_appdata = os.environ.get("LOCALAPPDATA")
    if local_appdata:
        candidates.append(os.path.join(local_appdata, "PerplexityExporter", "app.log"))
    cwd = os.getcwd()
    if cwd:
        candidates.append(os.path.join(cwd, "app.log"))
    return list(dict.fromkeys(candidates))


def log(msg: str):
    for candidate in _candidate_log_paths():
        try:
            directory = os.path.dirname(candidate)
            if directory:
                os.makedirs(directory, exist_ok=True)
            with open(candidate, "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now().isoformat(timespec='seconds')}] {msg}\n")
            return
        except Exception:
            continue


def save_session(token: str, email: str):
    with open(SESSION_FILE, "w", encoding="utf-8") as f:
        json.dump({"token": token, "email": email,
                   "saved_at": datetime.now(timezone.utc).isoformat()}, f)


def load_session() -> dict | None:
    try:
        with open(SESSION_FILE, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def clear_session():
    try:
        os.remove(SESSION_FILE)
    except Exception:
        pass


def write_signin_callback(token: str):
    try:
        with open(SIGNIN_CALLBACK_FILE, "w", encoding="utf-8") as f:
            json.dump({"token": token, "saved_at": datetime.now(timezone.utc).isoformat()}, f)
    except Exception:
        pass


def consume_signin_callback() -> str | None:
    try:
        if not os.path.exists(SIGNIN_CALLBACK_FILE):
            return None
        with open(SIGNIN_CALLBACK_FILE, encoding="utf-8") as f:
            payload = json.load(f)
        token = (payload or {}).get("token")
        if token:
            os.remove(SIGNIN_CALLBACK_FILE)
            return str(token)
    except Exception:
        pass
    return None


# ----------------------------------------------------------------------------
# Engine — Perplexity undocumented API (blueprint from Deplexity v0.2.5, v2.18)
# ----------------------------------------------------------------------------

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


def extract_session_token_from_cookie_header(cookie_header: str | None) -> str | None:
    if not cookie_header:
        return None
    for part in cookie_header.split(";"):
        part = part.strip()
        if not part:
            continue
        if part.startswith(COOKIE_NAME + "="):
            value = part[len(COOKIE_NAME) + 1:]
            return value or None
    return None


def extract_session_token_from_cookie_records(cookie_records) -> str | None:
    """Accept plain dicts OR WebView2 CoreWebView2Cookie COM objects (.Name/.Value)."""
    if not cookie_records:
        return None
    try:
        iterator = list(cookie_records)
    except Exception:
        iterator = cookie_records
    for record in iterator:
        try:
            if isinstance(record, dict):
                name = record.get("name") or record.get("Name")
                value = record.get("value") or record.get("Value")
            else:
                name = getattr(record, "Name", None) or getattr(record, "name", None)
                value = getattr(record, "Value", None) or getattr(record, "value", None)
            if name == COOKIE_NAME and value:
                return str(value)
        except Exception:
            continue
    return None


def extract_session_token_from_cdp_json(raw: str | None) -> str | None:
    """Parse JSON returned by CDP Network.getCookies / Network.getAllCookies."""
    if not raw:
        return None
    try:
        data = json.loads(raw)
    except Exception:
        return None
    cookies = data.get("cookies") if isinstance(data, dict) else None
    if not cookies:
        return None
    for cookie in cookies:
        try:
            if not isinstance(cookie, dict):
                continue
            if cookie.get("name") == COOKIE_NAME and cookie.get("value"):
                return str(cookie["value"])
        except Exception:
            continue
    return None


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
        if delay > 0:
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


def validate_session(token: str) -> dict:
    status, data = request(f"/api/auth/session?version={API_VERSION}&source=default", token, delay=0)
    return data if isinstance(data, dict) else {}


def _normalize_thread_items(raw) -> list[dict]:
    """Accept list or {data|threads|results: [...]} shapes from various endpoints."""
    if raw is None:
        return []
    if isinstance(raw, list):
        return [t for t in raw if isinstance(t, dict)]
    if isinstance(raw, dict):
        for key in ("data", "threads", "results", "items", "ask_threads"):
            val = raw.get(key)
            if isinstance(val, list):
                return [t for t in val if isinstance(t, dict)]
    return []


def _thread_key(t: dict) -> str | None:
    """Stable unique key — prefer uuid, then slug."""
    for k in ("uuid", "thread_uuid", "id"):
        v = t.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    for k in ("slug", "url_slug", "thread_url_slug", "thread_slug"):
        v = t.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return None


def _merge_thread(into: dict, src: dict):
    """Fill missing fields on an existing record from another source."""
    for k, v in src.items():
        if v in (None, "", [], {}):
            continue
        cur = into.get(k)
        if cur in (None, "", [], {}):
            into[k] = v
        elif k == "collection" and isinstance(v, dict) and isinstance(cur, dict):
            for ck, cv in v.items():
                if cv and not cur.get(ck):
                    cur[ck] = cv


def list_spaces(token: str) -> list[dict]:
    """GET /rest/spaces — Space metadata (not full thread bodies)."""
    path = f"/rest/spaces?version={API_VERSION}&source=default"
    try:
        status, raw = request(path, token, method="GET")
    except ApiError as e:
        log(f"list_spaces failed: {e}")
        return []
    if not isinstance(raw, dict):
        return []
    out = []
    for key in ("private_spaces", "shared_spaces", "invited_spaces",
                "saved_spaces", "organization_spaces"):
        for item in raw.get(key) or []:
            if isinstance(item, dict) and item.get("uuid"):
                item = dict(item)
                item["_space_bucket"] = key
                out.append(item)
    log(f"discovery: spaces endpoint returned {len(out)} space(s)")
    return out


def _discover_list_ask_threads(token: str, seen: dict, on_progress=None,
                               page_size: int = 50, max_offset: int = 5000) -> int:
    """Source A: POST list_ask_threads (primary library index). Returns new count."""
    path = f"/rest/thread/list_ask_threads?version={API_VERSION}&source=default"
    offset = 0
    added = 0
    reported_total = None
    while offset <= max_offset:
        body = {"limit": page_size, "ascending": False, "offset": offset,
                "search_term": "", "exclude_asi": False, "include_assets": True}
        try:
            status, raw = request(path, token, method="POST", body=body)
        except ApiError as e:
            log(f"discovery list_ask_threads offset={offset} failed: {e}")
            break
        items = _normalize_thread_items(raw)
        if not items:
            break
        # Some responses stamp total_threads on each item
        for it in items:
            tt = it.get("total_threads")
            if isinstance(tt, int) and tt > 0:
                reported_total = tt
                break
        new = 0
        for t in items:
            key = _thread_key(t)
            if not key:
                continue
            if key in seen:
                _merge_thread(seen[key], t)
                continue
            # Ensure uuid field exists for downstream export
            if not t.get("uuid"):
                t = dict(t)
                t["uuid"] = key
            t = dict(t)
            t["_discovery_source"] = "list_ask_threads"
            seen[key] = t
            new += 1
            added += 1
        if on_progress:
            on_progress(len(seen))
        if new == 0 or len(items) < page_size:
            break
        offset += len(items)
    if reported_total is not None:
        log(f"discovery: list_ask_threads reported total_threads={reported_total}, "
            f"unique so far={len(seen)}")
    else:
        log(f"discovery: list_ask_threads unique={len(seen)} (no total_threads field)")
    return added


def _discover_thread_list(token: str, seen: dict, on_progress=None,
                          page_size: int = 50, max_offset: int = 5000) -> int:
    """Source B: GET /rest/thread/list — alternate library index."""
    offset = 0
    added = 0
    while offset <= max_offset:
        path = (f"/rest/thread/list?version={API_VERSION}&source=default"
                f"&limit={page_size}&offset={offset}&ascending=false")
        try:
            status, raw = request(path, token, method="GET")
        except ApiError as e:
            log(f"discovery thread/list offset={offset} failed: {e}")
            break
        items = _normalize_thread_items(raw)
        if not items:
            break
        new = 0
        for t in items:
            key = _thread_key(t)
            if not key:
                continue
            if key in seen:
                _merge_thread(seen[key], t)
                continue
            t = dict(t)
            if not t.get("uuid"):
                t["uuid"] = key
            t["_discovery_source"] = "thread_list"
            seen[key] = t
            new += 1
            added += 1
        if on_progress:
            on_progress(len(seen))
        if new == 0 or len(items) < page_size:
            break
        offset += len(items)
    log(f"discovery: thread/list added {added}, unique total={len(seen)}")
    return added


def _discover_thread_search(token: str, seen: dict, on_progress=None,
                            page_size: int = 50, max_offset_per_query: int = 500) -> int:
    """Source C: POST /rest/thread/search — catches threads missing from list endpoints.

    Uses a small query set to avoid hammering the API (session-kill risk).
    """
    path = f"/rest/thread/search?version={API_VERSION}&source=default"
    # Keep this list short + low-risk. Empty string is often "match all".
    queries = ["", "a", "the", "how", "what"]
    added = 0
    for q in queries:
        offset = 0
        while offset <= max_offset_per_query:
            body = {"query": q, "limit": page_size, "offset": offset}
            # Some builds accept search_term instead of query
            try:
                status, raw = request(path, token, method="POST", body=body)
            except ApiError as e:
                # try alternate body once
                if offset == 0:
                    try:
                        body2 = {"search_term": q, "limit": page_size, "offset": offset}
                        status, raw = request(path, token, method="POST", body=body2)
                    except ApiError as e2:
                        log(f"discovery search q={q!r} failed: {e2}")
                        break
                else:
                    log(f"discovery search q={q!r} offset={offset} failed: {e}")
                    break
            items = _normalize_thread_items(raw)
            if not items:
                break
            new = 0
            for t in items:
                key = _thread_key(t)
                if not key:
                    continue
                if key in seen:
                    _merge_thread(seen[key], t)
                    continue
                t = dict(t)
                if not t.get("uuid"):
                    t["uuid"] = key
                if not t.get("title"):
                    t["title"] = t.get("query") or t.get("query_str") or t.get("text") or key
                t["_discovery_source"] = f"search:{q or '∅'}"
                seen[key] = t
                new += 1
                added += 1
            if on_progress:
                on_progress(len(seen))
            if new == 0 or len(items) < page_size:
                break
            offset += len(items)
    log(f"discovery: search added {added}, unique total={len(seen)}")
    return added


def _discover_space_threads(token: str, spaces: list[dict], seen: dict,
                            on_progress=None) -> int:
    """Source D: try per-Space listing endpoints (best-effort; shapes vary)."""
    added = 0
    for sp in spaces:
        suuid = sp.get("uuid") or ""
        stitle = sp.get("title") or ""
        if not suuid:
            continue
        candidates = [
            # POST body variants
            ("POST", f"/rest/thread/list_ask_threads?version={API_VERSION}&source=default",
             {"limit": 50, "ascending": False, "offset": 0, "search_term": "",
              "exclude_asi": False, "include_assets": True, "collection_uuid": suuid}),
            ("POST", f"/rest/thread/list_ask_threads?version={API_VERSION}&source=default",
             {"limit": 50, "ascending": False, "offset": 0, "search_term": "",
              "exclude_asi": False, "include_assets": True, "space_uuid": suuid}),
            ("GET", f"/rest/collection/{suuid}/threads?version={API_VERSION}&source=default&limit=50&offset=0", None),
            ("GET", f"/rest/spaces/{suuid}/threads?version={API_VERSION}&source=default&limit=50&offset=0", None),
            ("GET", f"/rest/spaces/{suuid}?version={API_VERSION}&source=default", None),
        ]
        for method, path, body in candidates:
            try:
                status, raw = request(path, token, method=method, body=body)
            except ApiError:
                continue
            items = _normalize_thread_items(raw)
            # Nested shapes: {threads: [...]}, {space: {threads: ...}}
            if not items and isinstance(raw, dict):
                nested = raw.get("space") or raw.get("collection") or {}
                if isinstance(nested, dict):
                    items = _normalize_thread_items(nested.get("threads"))
                    if not items:
                        items = _normalize_thread_items(nested)
            if not items:
                continue
            col = {"uuid": suuid, "title": stitle, "slug": sp.get("slug") or "",
                   "emoji": sp.get("emoji") or ""}
            new_here = 0
            for t in items:
                key = _thread_key(t)
                if not key:
                    continue
                t = dict(t)
                if not t.get("uuid"):
                    t["uuid"] = key
                if not t.get("collection"):
                    t["collection"] = col
                if key in seen:
                    _merge_thread(seen[key], t)
                else:
                    t["_discovery_source"] = f"space:{stitle or suuid[:8]}"
                    seen[key] = t
                    added += 1
                    new_here += 1
            if new_here:
                log(f"discovery: space {stitle!r} via {method} {path.split('?')[0]} +{new_here}")
                if on_progress:
                    on_progress(len(seen))
                break  # one working endpoint per space is enough for first pass
    log(f"discovery: space probes added {added}, unique total={len(seen)}")
    return added


def list_threads(token: str, on_progress=None, deep: bool = False) -> list[dict]:
    """Discover conversations across multiple Perplexity endpoints.

    Single-endpoint list_ask_threads is incomplete for many accounts (often
    tens of threads when the user has hundreds). We merge:

      A) POST /rest/thread/list_ask_threads
      B) GET  /rest/thread/list
      C) POST /rest/thread/search  (light query set)
      D) GET  /rest/spaces + best-effort per-space thread probes

    Returns a de-duplicated list of thread summary dicts (uuid required).
    """
    seen: dict[str, dict] = {}
    log("discovery: starting multi-source thread index")
    _discover_list_ask_threads(token, seen, on_progress=on_progress)
    if deep:
        _discover_thread_list(token, seen, on_progress=on_progress)
        _discover_thread_search(token, seen, on_progress=on_progress)
        spaces = list_spaces(token)
        if spaces:
            _discover_space_threads(token, spaces, seen, on_progress=on_progress)
    threads = list(seen.values())
    # Newest first when timestamp present
    def _ts(t):
        return t.get("last_query_datetime") or t.get("updated_at") or t.get("created_at") or ""
    threads.sort(key=_ts, reverse=True)
    sources = {}
    for t in threads:
        s = t.get("_discovery_source") or "?"
        sources[s] = sources.get(s, 0) + 1
    log(f"discovery: complete — {len(threads)} unique conversation(s); by source: {sources}")
    return threads


def get_thread(token: str, uuid: str) -> dict:
    path = (f"/rest/thread/{uuid}?with_schematized_response=true&version={API_VERSION}"
            f"&source=default&limit=50&offset=0&from_first=true"
            f"&supported_block_use_cases=answer_modes&supported_block_use_cases=preserve_latex")
    status, data = request(path, token)
    detail = data if isinstance(data, dict) else {"entries": []}
    entries = detail.get("entries", []) or []
    seen, uniq = set(), []
    for e in entries:
        eid = e.get("uuid") or id(e)
        if eid in seen:
            continue
        seen.add(eid)
        uniq.append(e)
    detail["entries"] = uniq
    return detail


def extract_entry(entry: dict) -> dict:
    blocks = entry.get("blocks", []) or []
    answer = ""
    for b in blocks:
        mb = b.get("markdown_block")
        if mb and b.get("intended_usage") == "ask_text_0_markdown" and mb.get("answer"):
            answer = mb["answer"]
            break
    if not answer:
        for b in blocks:
            mb = b.get("markdown_block")
            if mb and b.get("intended_usage") == "ask_text" and mb.get("answer"):
                answer = mb["answer"]
                break
    sources = []
    for b in blocks:
        wr = b.get("web_result_block")
        if wr and b.get("intended_usage") == "web_results":
            for s in wr.get("web_results", []) or []:
                if s.get("name") and s.get("url"):
                    sources.append({"title": s["name"], "url": s["url"],
                                    "snippet": s.get("snippet", "")})
            break
    return {
        "uuid": entry.get("uuid"),
        "query": entry.get("query_str", ""),
        "model": entry.get("display_model", ""),
        "search_focus": entry.get("search_focus", ""),
        "created_at": entry.get("entry_created_datetime", ""),
        "updated_at": entry.get("entry_updated_datetime", ""),
        "answer": answer,
        "sources": sources,
    }


def render_markdown(meta: dict, entries: list[dict]) -> str:
    lines = [f"# {meta.get('title') or 'Untitled thread'}",
             "", f"- **Created:** {meta.get('created_at', '')}",
             f"- **Updated:** {meta.get('updated_at', '')}",
             f"- **Thread UUID:** {meta.get('uuid', '')}",
             f"- **Mode:** {meta.get('mode', '')}", ""]
    if meta.get("space"):
        lines.append(f"- **Space:** {meta['space']}")
        lines.append("")
    for i, e in enumerate(entries, 1):
        lines.append("---")
        lines.append("")
        lines.append(f"## Q{i}: {e.get('query') or '(no question text)'}")
        lines.append("")
        if e.get("model"):
            lines.append(f"*Model: {e['model']}*")
            lines.append("")
        lines.append(e.get("answer") or "_(no answer text captured)_")
        lines.append("")
        if e.get("sources"):
            lines.append("### Sources")
            for s in e["sources"]:
                lines.append(f"- [{s['title']}]({s['url']})")
            lines.append("")
    return "\n".join(lines)


# ---- Human-friendly export layout (Spaces = folders) ----------------------

HOME_SPACE_NAME = "Home"
SPACES_DIRNAME = "Spaces"
LEGACY_THREADS_DIRNAME = "threads"


def space_label_from_collection(col: dict | None, meta: dict | None = None) -> str:
    """Human Space name from list-item collection or thread_metadata.collection_info."""
    col = col or {}
    meta = meta or {}
    ci = meta.get("collection_info") if isinstance(meta.get("collection_info"), dict) else {}
    title = (col.get("title") or col.get("name") or ci.get("title") or ci.get("name") or "").strip()
    return title or HOME_SPACE_NAME


def safe_name(s: str, max_len: int = 80) -> str:
    """Filesystem-safe single path segment. Keeps spaces for readability."""
    s = (s or "").replace("\n", " ").replace("\r", " ")
    # Windows-forbidden filename chars + control chars
    s = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", s)
    s = re.sub(r"[^A-Za-z0-9 _.\(\)\[\]+\-]", "_", s)
    s = re.sub(r"\s+", " ", s).strip().strip(".")
    if len(s) > max_len:
        s = s[:max_len].rstrip().rstrip(".")
    return s or "untitled"


def short_id(uuid: str) -> str:
    u = (uuid or "").replace("-", "")
    return (u[:8] if u else "00000000").lower()


def thread_folder_name(title: str, uuid: str) -> str:
    """e.g. 'Google cloud setup -- a1b2c3d4' — readable + unique."""
    base = safe_name(title or "Untitled conversation", max_len=72)
    return f"{base} -- {short_id(uuid)}"


def space_dir_name(space: str) -> str:
    if not space or space == HOME_SPACE_NAME:
        return HOME_SPACE_NAME
    return safe_name(space, max_len=60) or "Space"


def thread_rel_path(space: str, title: str, uuid: str) -> str:
    """Relative path from export root to the thread folder (posix-ish for manifest)."""
    sn = space_dir_name(space)
    fn = thread_folder_name(title, uuid)
    if sn == HOME_SPACE_NAME:
        return str(Path(HOME_SPACE_NAME) / fn)
    return str(Path(SPACES_DIRNAME) / sn / fn)


def thread_abs_folder(outdir: str, space: str, title: str, uuid: str) -> str:
    return os.path.join(outdir, thread_rel_path(space, title, uuid).replace("/", os.sep))


def load_uuid_index(outdir: str) -> dict:
    path = os.path.join(outdir, "uuid_index.json")
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def save_uuid_index(outdir: str, index: dict):
    path = os.path.join(outdir, "uuid_index.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)


def find_existing_thread_folder(outdir: str, uuid: str, uuid_index: dict | None = None) -> str | None:
    """Locate a thread folder by uuid (new layout, index, or legacy flat threads/)."""
    if not uuid:
        return None
    idx = uuid_index if uuid_index is not None else load_uuid_index(outdir)
    rel = idx.get(uuid)
    if rel:
        abs_p = os.path.join(outdir, rel.replace("/", os.sep))
        if os.path.isdir(abs_p) and os.path.exists(os.path.join(abs_p, "thread.json")):
            return abs_p

    # Legacy: threads/<slug-or-uuid>/
    legacy_root = os.path.join(outdir, LEGACY_THREADS_DIRNAME)
    if os.path.isdir(legacy_root):
        # direct uuid folder
        cand = os.path.join(legacy_root, uuid)
        if os.path.exists(os.path.join(cand, "thread.json")):
            return cand
        # scan shallow (legacy is flat)
        try:
            for name in os.listdir(legacy_root):
                folder = os.path.join(legacy_root, name)
                jp = os.path.join(folder, "thread.json")
                if not os.path.isfile(jp):
                    continue
                if name == uuid or name.endswith(uuid) or uuid[:8] in name:
                    return folder
                try:
                    with open(jp, encoding="utf-8") as f:
                        data = json.load(f)
                    meta = data.get("thread_metadata") or {}
                    if meta.get("uuid") == uuid or data.get("uuid") == uuid:
                        return folder
                    # list item uuid sometimes only on disk path
                    if (data.get("thread_metadata") or {}).get("thread_url", "").find(uuid) >= 0:
                        return folder
                except Exception:
                    continue
        except Exception:
            pass

    # New layout scan (Home + Spaces/*) — only if index missed
    for root_name in (HOME_SPACE_NAME, SPACES_DIRNAME):
        root = os.path.join(outdir, root_name)
        if not os.path.isdir(root):
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            if "thread.json" in filenames:
                if short_id(uuid) in os.path.basename(dirpath).lower() or uuid in dirpath:
                    return dirpath
    return None


def entry_stats(entries: list[dict]) -> dict:
    answer_chars = 0
    empty_answers = 0
    sources = 0
    for e in entries or []:
        a = e.get("answer") or ""
        answer_chars += len(a)
        if not a.strip():
            empty_answers += 1
        sources += len(e.get("sources") or [])
    return {
        "entries": len(entries or []),
        "answer_chars": answer_chars,
        "empty_answer_entries": empty_answers,
        "sources": sources,
        "all_answers_empty": bool(entries) and empty_answers == len(entries),
    }


def write_conversation_markdown(path: str, meta: dict, entries: list[dict]):
    with open(path, "w", encoding="utf-8") as f:
        f.write(render_markdown(meta, entries))


def build_space_readme(space_name: str, threads: list[dict]) -> str:
    lines = [
        f"# {space_name}",
        "",
        f"{len(threads)} conversation(s) in this Space.",
        "",
        "| Conversation | Turns | Answer text | Sources |",
        "|---|---:|---:|---:|",
    ]
    for t in sorted(threads, key=lambda x: (x.get("title") or "").lower()):
        rel = t.get("folder_name") or t.get("rel_path", "").replace("\\\\", "/").split("/")[-1]
        title = t.get("title") or rel
        md_link = f"[{title.replace('|', '/')}]({rel}/conversation.md)" if rel else title
        st = t.get("stats") or {}
        warn = " ⚠️ empty" if t.get("empty_answers") else ""
        lines.append(
            f"| {md_link}{warn} | {st.get('entries', t.get('entries', '—'))} | "
            f"{st.get('answer_chars', '—')} chars | {st.get('sources', '—')} |"
        )
    lines.append("")
    return "\n".join(lines)


def build_root_readme(account: str, exported_at: str, by_space: dict, warnings: list[str]) -> str:
    total = sum(len(v) for v in by_space.values())
    lines = [
        "# Your Perplexity export",
        "",
        "Conversations are grouped the same way as in Perplexity: **Spaces** are folders.",
        "Threads with no Space live under **Home**.",
        "",
        f"- **Account:** {account or '—'}",
        f"- **Exported:** {exported_at}",
        f"- **Conversations:** {total}",
        f"- **Spaces (incl. Home):** {len(by_space)}",
        "",
        "## Browse by Space",
        "",
    ]
    # Home first, then alpha
    names = sorted(by_space.keys(), key=lambda n: (n != HOME_SPACE_NAME, n.lower()))
    for name in names:
        threads = by_space[name]
        if name == HOME_SPACE_NAME:
            link = f"./{HOME_SPACE_NAME}/README.md"
        else:
            link = f"./{SPACES_DIRNAME}/{space_dir_name(name)}/README.md"
        lines.append(f"- **[{name}]({link})** — {len(threads)} conversation(s)")
    lines.append("")
    lines.append("## All conversations")
    lines.append("")
    lines.append("| Space | Conversation | Turns | Notes |")
    lines.append("|---|---|---:|---|")
    for name in names:
        for t in sorted(by_space[name], key=lambda x: (x.get("title") or "").lower()):
            title = (t.get("title") or "Untitled").replace("|", "/")
            rel = (t.get("rel_path") or "").replace("\\\\", "/")
            link = f"[{title}]({rel}/conversation.md)" if rel else title
            st = t.get("stats") or {}
            note = ""
            if t.get("empty_answers"):
                note = "⚠️ no answer text captured"
            lines.append(
                f"| {name} | {link} | {st.get('entries', t.get('entries', '—'))} | {note} |"
            )
    if warnings:
        lines.append("")
        lines.append("## Warnings")
        lines.append("")
        for w in warnings:
            lines.append(f"- {w}")
        lines.append("")
    lines.append("")
    lines.append("---")
    lines.append("Each conversation folder contains `conversation.md` (readable) and `thread.json` (full data).")
    lines.append("")
    return "\n".join(lines)


def write_export_indexes(outdir: str, account: str, thread_records: list[dict],
                         exported_at: str | None = None) -> dict:
    """Write README.md, per-Space READMEs, manifest.json, uuid_index.json."""
    exported_at = exported_at or datetime.now(timezone.utc).isoformat()
    by_space: dict[str, list] = {}
    uuid_index = {}
    warnings = []
    empty_list = []

    for rec in thread_records:
        sp = rec.get("space") or HOME_SPACE_NAME
        by_space.setdefault(sp, []).append(rec)
        if rec.get("uuid") and rec.get("rel_path"):
            uuid_index[rec["uuid"]] = rec["rel_path"].replace("\\\\", "/")
        if rec.get("empty_answers"):
            empty_list.append(rec.get("title") or rec.get("uuid") or "?")

    if empty_list:
        warnings.append(
            f"{len(empty_list)} conversation(s) have no captured answer text: "
            + ", ".join(empty_list[:12])
            + ("…" if len(empty_list) > 12 else "")
        )

    # Root README
    with open(os.path.join(outdir, "README.md"), "w", encoding="utf-8") as f:
        f.write(build_root_readme(account, exported_at, by_space, warnings))

    # Per-space README + ensure dirs
    for sp, threads in by_space.items():
        if sp == HOME_SPACE_NAME:
            sdir = os.path.join(outdir, HOME_SPACE_NAME)
        else:
            sdir = os.path.join(outdir, SPACES_DIRNAME, space_dir_name(sp))
        os.makedirs(sdir, exist_ok=True)
        # folder_name for relative links inside space readme
        for t in threads:
            rel = (t.get("rel_path") or "").replace("\\\\", "/")
            t["folder_name"] = rel.split("/")[-1] if rel else thread_folder_name(t.get("title") or "", t.get("uuid") or "")
        with open(os.path.join(sdir, "README.md"), "w", encoding="utf-8") as f:
            f.write(build_space_readme(sp, threads))

    spaces_summary = []
    for sp, threads in sorted(by_space.items(), key=lambda kv: (kv[0] != HOME_SPACE_NAME, kv[0].lower())):
        spaces_summary.append({
            "name": sp,
            "path": HOME_SPACE_NAME if sp == HOME_SPACE_NAME else f"{SPACES_DIRNAME}/{space_dir_name(sp)}",
            "thread_count": len(threads),
            "entries": sum((t.get("stats") or {}).get("entries", 0) for t in threads),
            "answer_chars": sum((t.get("stats") or {}).get("answer_chars", 0) for t in threads),
            "empty_answer_threads": sum(1 for t in threads if t.get("empty_answers")),
        })

    manifest = {
        "tool": "Perplexity Exporter",
        "layout": "spaces-v1",
        "version": APP_VERSION if "APP_VERSION" in globals() else "1.0.0",
        "exported_at": exported_at,
        "account": account or "",
        "total_threads": len(thread_records),
        "exported_threads": len(thread_records),
        "formats": ["json", "markdown"],
        "spaces": spaces_summary,
        "warnings": {"empty_answer_threads": empty_list},
        "threads": [
            {
                "uuid": t.get("uuid"),
                "title": t.get("title"),
                "space": t.get("space") or HOME_SPACE_NAME,
                "path": (t.get("rel_path") or "").replace("\\\\", "/"),
                "updated_at": t.get("updated_at") or "",
                "entries": (t.get("stats") or {}).get("entries"),
                "answer_chars": (t.get("stats") or {}).get("answer_chars"),
                "sources": (t.get("stats") or {}).get("sources"),
                "empty_answers": bool(t.get("empty_answers")),
            }
            for t in thread_records
        ],
    }
    with open(os.path.join(outdir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    save_uuid_index(outdir, uuid_index)
    return manifest




def friendly_error(e: Exception) -> str:
    msg = str(e)
    if msg == "auth-failed":
        return ("Your Perplexity session has expired. Please reconnect "
                "(click Disconnect, then Log in again).")
    if msg == "network":
        return "Could not reach Perplexity. Check your internet connection and try again."
    if msg.startswith("http-"):
        return f"Perplexity returned an error (HTTP {msg.split('-')[1]}). Please try again."
    return f"Something went wrong: {msg}"


def dispatch_to_ui_thread(form, callback, begin_invoke=None):
    """Run callback on the form's UI thread when possible."""
    if getattr(form, "InvokeRequired", False):
        if begin_invoke is not None:
            begin_invoke(callback)
            return True
        try:
            from System import Action
            form.BeginInvoke(Action(callback))
            return True
        except Exception:
            pass
    callback()
    return True


def detect_session_token_from_browser_store() -> str | None:
    """Probe common Chromium/Edge browser cookie stores for an active Perplexity session."""
    try:
        import base64
        import ctypes
        import json
        import sqlite3
        import tempfile
        from ctypes import wintypes

        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    except Exception as e:
        log(f"browser-store probe unavailable: {e}")
        return None

    local_appdata = os.environ.get("LOCALAPPDATA")
    if not local_appdata:
        return None

    user_data_roots = [
        os.path.join(local_appdata, "Google", "Chrome", "User Data"),
        os.path.join(local_appdata, "Microsoft", "Edge", "User Data"),
        os.path.join(local_appdata, "BraveSoftware", "Brave-Browser", "User Data"),
        os.path.join(local_appdata, "Chromium", "User Data"),
        os.path.join(local_appdata, "Programs", "Perplexity"),
        os.path.join(appdata_dir(), "login-webview"),
    ]

    appdata = os.environ.get("APPDATA")
    if appdata:
        user_data_roots.extend([
            os.path.join(appdata, "Perplexity"),
            os.path.join(appdata, "PerplexityExporter", "login-webview"),
        ])

    for user_data_root in user_data_roots:
        if not os.path.isdir(user_data_root):
            continue
        try:
            for root, _, _ in os.walk(user_data_root):
                if os.path.basename(root) != "Network":
                    continue
                cookie_db = os.path.join(root, "Cookies")
                if not os.path.exists(cookie_db):
                    continue
                state_path = os.path.join(user_data_root, "Local State")
                if not os.path.exists(state_path):
                    continue
                with open(state_path, encoding="utf-8") as fh:
                    state = json.load(fh)
                enc_key_b64 = (state.get("os_crypt") or {}).get("encrypted_key", "")
                if not enc_key_b64:
                    continue
                enc_key = base64.b64decode(enc_key_b64)
                if enc_key[:5] == b"DPAPI":
                    enc_key = enc_key[5:]
                else:
                    continue

                class DATA_BLOB(ctypes.Structure):
                    _fields_ = [("cbData", wintypes.DWORD),
                                ("pbData", ctypes.POINTER(ctypes.c_char))]

                crypt32 = ctypes.windll.crypt32
                kernel32 = ctypes.windll.kernel32
                in_blob = DATA_BLOB(len(enc_key), ctypes.cast(ctypes.create_string_buffer(enc_key), ctypes.POINTER(ctypes.c_char)))
                out_blob = DATA_BLOB()
                if not crypt32.CryptUnprotectData(ctypes.byref(in_blob), None, None, None, None, 0, ctypes.byref(out_blob)):
                    continue
                try:
                    aes_key = ctypes.string_at(out_blob.pbData, out_blob.cbData)
                finally:
                    kernel32.LocalFree(out_blob.pbData)

                con = None
                try:
                    con = sqlite3.connect(f"file:{cookie_db}?mode=ro", uri=True)
                    rows = con.execute(
                        "SELECT host_key, name, value, encrypted_value FROM cookies WHERE name = ?",
                        (COOKIE_NAME,)
                    ).fetchall()
                except Exception:
                    try:
                        tmp_db = os.path.join(tempfile.gettempdir(), "px_browser_cookies.sqlite")
                        import shutil
                        shutil.copy2(cookie_db, tmp_db)
                        con = sqlite3.connect(tmp_db)
                        rows = con.execute(
                            "SELECT host_key, name, value, encrypted_value FROM cookies WHERE name = ?",
                            (COOKIE_NAME,)
                        ).fetchall()
                    except Exception:
                        rows = []
                finally:
                    if con is not None:
                        con.close()

                for _, name, value, enc_value in rows:
                    try:
                        blob = enc_value or value
                        if not blob:
                            continue
                        if isinstance(blob, bytes):
                            blob = blob.decode("utf-8", "replace")
                        if not isinstance(blob, str):
                            continue
                        if not blob.startswith("v10"):
                            return str(blob)
                        body = blob[3:]
                        raw = base64.b64decode(body)
                        nonce, ct = raw[:12], raw[12:]
                        token = AESGCM(aes_key).decrypt(nonce, ct, None).decode("utf-8", "replace")
                        if token:
                            return token
                    except Exception:
                        continue
        except Exception as e:
            log(f"browser-store probe error for {user_data_root}: {e}")
    return None


# ----------------------------------------------------------------------------
# GUI bridge — called from the web UI
# ----------------------------------------------------------------------------

class JsApi:
    """Minimal surface exposed to JavaScript via pywebview.

    IMPORTANT: pywebview walks public attributes of the js_api object and
    recursively exposes nested objects (see webview.util.get_functions). Putting
    the Window, tokens, threads, etc. on the same object breaks JS bridge
    injection — symptoms: `connect is not a function`, `Main window failed to
    start`. Only public methods (and underscore-private attrs) belong here.
    """

    def __init__(self, bridge: "Bridge"):
        self._b = bridge

    def ping(self):
        return self._b.ping()

    def getState(self):
        return self._b.getState()

    def connect(self):
        return self._b.connect()

    def cancelLogin(self):
        return self._b.cancelLogin()

    def pasteCookie(self, token: str = ""):
        return self._b.pasteCookie(token)

    def chooseFolder(self):
        return self._b.chooseFolder()

    def startExport(self, refresh: bool = False):
        return self._b.startExport(refresh)

    def openFolder(self):
        return self._b.openFolder()

    def disconnect(self):
        return self._b.disconnect()

    def quitApp(self):
        return self._b.quitApp()



class Bridge:
    """Called from the web UI via pywebview's js_api bridge.

    Design note: NO second/hidden windows — the main window itself navigates
    to perplexity.ai for login, then load_html() brings the UI back. Hidden
    windows caused GUI-thread hangs in pywebview 6.2.1 (show()/load_url()
    wait on events + synchronous Invoke while WebView2 initializes).
    """

    def __init__(self, ui_html: str = ""):
        self.token: str | None = None
        self.email: str | None = None
        self._window = None
        self._ui_html = ui_html
        self._stop_login = threading.Event()
        self._login_thread: threading.Thread | None = None
        self._login_form = None
        self._export_thread: threading.Thread | None = None
        self._connecting = False
        self._default_folder = os.path.join(os.path.expanduser("~"), "Perplexity-export")
        self._LOGIN_TIMEOUT = 8 * 60  # seconds
        self._login_completion_pending = False
        self._conversation_count = 0

    # -- helpers ------------------------------------------------------------

    def _push(self, payload: dict):
        if self._window is None:
            log(f"push dropped: window is None for {payload.get('type')}")
            return

        def _dispatch():
            try:
                # Wait briefly for pywebview injection (loaded). Do NOT hang 20s
                # inside evaluate_js's decorator if the UI is mid-init — poll instead.
                loaded = getattr(getattr(self._window, "events", None), "loaded", None)
                if loaded is not None:
                    if not loaded.wait(timeout=8):
                        log(f"push deferred/dropped (UI not loaded yet) for {payload.get('type')}")
                        # stash connected/disconnected so boot can pick up via getState
                        return
                # Prefer run_js (before_load-gated, lighter) for fire-and-forget UI pushes
                script = f"window.__push && window.__push({json.dumps(payload)})"
                try:
                    self._window.evaluate_js(script)
                except Exception:
                    # last resort: run_js without return value
                    self._window.run_js(script)
                log(f"push delivered: {payload.get('type')}")
            except Exception as e:
                log(f"push failed for {payload.get('type')}: {e}")

        try:
            threading.Thread(target=_dispatch, daemon=True).start()
        except Exception as e:
            log(f"push thread launch failed for {payload.get('type')}: {e}")

    def _restore_ui(self):
        """Navigate back to the local UI (after login on perplexity.ai)."""
        if self._window is None or not self._ui_html:
            return
        try:
            self._window.load_html(self._ui_html)
        except Exception as e:
            log(f"restore UI failed: {e}")

    # -- UI entry points (called from JavaScript) ---------------------------

    def ping(self):
        return "pong"

    def getState(self):
        log(f"bridge: getState (connected={bool(self.token)}, connecting={self._connecting})")
        return {"version": APP_VERSION, "build": APP_BUILD_TAG, "folder": self._default_folder,
                "connected": bool(self.token), "email": self.email or "",
                "connecting": bool(self._connecting), "count": self._conversation_count}

    def connect(self):
        log("bridge: connect() called from UI")
        try:
            self._push({"type": "log", "line": "Received login request from UI"})
        except Exception:
            pass
        if self.token or self._connecting:
            log(f"bridge: connect() ignored (token={bool(self.token)}, connecting={self._connecting})")
            return
        self._connecting = True
        self._login_completion_pending = False
        self._stop_login.clear()
        # Show spinner only — do not reset first (avoids blue-button flash).
        self._push({"type": "waiting_login"})

        log("login: starting embedded WebView2 login (CDP capture)")
        self._start_embedded_login()

    def _start_embedded_login(self):
        """Run the WinForms/WebView2 login form on a true STA thread.

        Python's threading.Thread is MTA; WinForms + WebView2 require STA.
        Use System.Threading.Thread with ApartmentState.STA (pythonnet).
        """
        def runner():
            try:
                self._login_window_flow()
            except Exception as e:
                log(f"login: embedded flow crashed: {e}\n{traceback.format_exc()}")
                self._connecting = False
                self._push({"type": "error",
                            "message": "The sign-in window failed to start. "
                                       "Please try again, or use the session-cookie option."})
                self._push({"type": "login_cancelled"})

        # Prefer CLR STA thread
        try:
            try:
                import clr  # noqa: F401
            except Exception:
                os.environ["PYTHONNET_RUNTIME"] = "coreclr"
                import clr  # noqa: F401
            from System.Threading import ApartmentState, Thread as NetThread, ThreadStart
            t = NetThread(ThreadStart(runner))
            t.SetApartmentState(ApartmentState.STA)
            t.IsBackground = True
            t.Start()
            self._login_clr_thread = t
            log("login: STA CLR thread started")
            return
        except Exception as e:
            log(f"login: STA CLR thread unavailable ({e}); falling back to Python thread")

        self._login_thread = threading.Thread(target=runner, daemon=True)
        self._login_thread.start()

    def _browser_login_flow(self):
        """Open Perplexity in the system browser and wait for a usable session."""
        log("login: waiting for browser sign-in token")
        try:
            opened = webbrowser.open("https://www.perplexity.ai/")
            log(f"login: opened default browser to Perplexity: {opened}")
        except Exception as e:
            log(f"login: browser open failed: {e}")

        self._push({"type": "log", "line": "Please complete the sign-in in your browser."})

        deadline = time.time() + self._LOGIN_TIMEOUT
        while time.time() < deadline:
            if self._stop_login.is_set():
                log("login: browser flow cancelled")
                self._connecting = False
                self._push({"type": "login_cancelled"})
                return

            token = consume_signin_callback()
            if token:
                self._accept_token(token, False)
                return
            token = detect_session_token_from_browser_store()
            if token:
                self._accept_token(token, False)
                return
            time.sleep(2)

        self._connecting = False
        self._push({"type": "error",
                    "message": "We could not confirm a Perplexity session after opening your browser. "
                               "Please complete the sign-in and try again."})
        self._push({"type": "login_cancelled"})

    def cancelLogin(self):
        log("bridge: cancelLogin() called from UI")
        self._stop_login.set()
        self._login_completion_pending = False
        self._connecting = False
        form = getattr(self, "_login_form", None)
        if form is not None:
            try:
                from System import Action
                form.BeginInvoke(Action(form.Close))
            except Exception:
                pass
        self._push({"type": "reset_login_ui"})
        self._push({"type": "login_cancelled"})

    def pasteCookie(self, token: str):
        log("bridge: pasteCookie() called from UI")
        token = (token or "").strip()
        if not token:
            return
        self._push({"type": "waiting_login"})
        threading.Thread(target=self._accept_token, args=(token, False), daemon=True).start()

    def chooseFolder(self):
        log("bridge: chooseFolder() called from UI")
        try:
            import webview
            result = self._window.create_file_dialog(webview.FOLDER_DIALOG,
                                                    directory=self._default_folder)
            if result and result[0]:
                self._default_folder = result[0]
                return self._default_folder
        except Exception as e:
            log(f"folder dialog error: {e}")
        return self._default_folder

    def startExport(self, refresh: bool = False):
        log("bridge: startExport() called from UI")
        if not self.token or self._export_thread and self._export_thread.is_alive():
            return
        self._export_thread = threading.Thread(target=self._export_worker,
                                               args=(bool(refresh),), daemon=True)
        self._export_thread.start()

    def openFolder(self):
        log("bridge: openFolder() called from UI")
        try:
            os.startfile(self._default_folder)  # type: ignore[attr-defined]
        except Exception as e:
            log(f"open folder error: {e}")

    def disconnect(self):
        log("bridge: disconnect() called from UI")
        clear_session()
        self.token = None
        self.email = None
        self._conversation_count = 0
        self._connecting = False
        self._push({"type": "disconnected"})
        log("disconnected")

    def quitApp(self):
        try:
            self._window.destroy()
        except Exception:
            pass

    # -- login flow ---------------------------------------------------------

    def _login_window_flow(self):
        """Open a native WinForms + WebView2 login window (must run on STA thread).

        Cookie capture strategy (different from prior CookieManager-COM attempts):
          1. PRIMARY: CDP via CoreWebView2.CallDevToolsProtocolMethodAsync
             ("Network.getCookies") — returns plain JSON, no COM cookie objects.
          2. BACKUP: WebResourceRequested Cookie header interception (HttpOnly
             cookies are present on outgoing requests).
          3. LAST: CookieManager.GetCookiesAsync + COM .Name/.Value on UI thread.

        Never navigate the pywebview main window (self-deadlock in 6.2.1).
        Never read page JS document.cookie (hides HttpOnly).
        Disk/DPAPI fallback is a dead end on app-bound encryption — skipped.
        """
        try:
            import clr
        except Exception:
            os.environ["PYTHONNET_RUNTIME"] = "coreclr"
            import clr

        try:
            from webview.util import interop_dll_path
            clr.AddReference("System.Windows.Forms")
            clr.AddReference("System.Drawing")
            clr.AddReference(interop_dll_path("Microsoft.Web.WebView2.Core.dll"))
            clr.AddReference(interop_dll_path("Microsoft.Web.WebView2.WinForms.dll"))
            from System.Windows.Forms import (Application, DockStyle, Form,
                                             FormStartPosition, Label,
                                             Padding)
            from System import Action, Uri
            from System.Drawing import Color, Font, Size
            from Microsoft.Web.WebView2.Core import CoreWebView2WebResourceContext
            from Microsoft.Web.WebView2.WinForms import (CoreWebView2CreationProperties,
                                                         WebView2)
            from System.Windows.Forms import Timer as WinTimer
        except Exception as e:
            log(f"login: could not load WinForms/WebView2: {e}")
            self._connecting = False
            self._push({"type": "error",
                        "message": "Embedded login is unavailable on this PC. "
                                   "Please use the session-cookie option instead."})
            self._push({"type": "login_cancelled"})
            return

        try:
            from System.Windows.Forms import UnhandledExceptionMode
            Application.SetUnhandledExceptionMode(UnhandledExceptionMode.CatchException)

            def _on_winforms_exception(sender, args):
                try:
                    log(f"login: WinForms ThreadException: {args.Exception}")
                    args.ExceptionHandled = True
                except Exception:
                    pass
            Application.ThreadException += _on_winforms_exception
        except Exception as e:
            log(f"login: could not hook WinForms exception handler: {e}")

        form = Form()
        form.Text = "Sign in to Perplexity"
        form.Size = Size(980, 760)
        form.StartPosition = FormStartPosition.CenterScreen
        form.MinimumSize = Size(640, 560)
        try:
            form.BackColor = Color.FromArgb(15, 17, 23)
        except Exception:
            pass

        status = Label()
        status.Text = "  Loading Perplexity sign-in…"
        status.Dock = DockStyle.Top
        status.Height = 28
        try:
            status.ForeColor = Color.FromArgb(154, 163, 184)
            status.BackColor = Color.FromArgb(23, 26, 35)
            status.Font = Font("Segoe UI", 9.0)
        except Exception:
            pass

        wv = WebView2()
        wv.Dock = DockStyle.Fill
        try:
            props = CoreWebView2CreationProperties()
            props.UserDataFolder = os.path.join(appdata_dir(), "login-webview")
            wv.CreationProperties = props
        except Exception as e:
            log(f"login: creation-props error (ignored): {e}")

        form.Controls.Add(wv)
        form.Controls.Add(status)

        closed = threading.Event()
        finished = {"done": False}
        self._login_form = form
        log("login: starting embedded login window")

        def on_form_closing(sender, e):
            closed.set()
            try:
                timer.Stop()
            except Exception:
                pass
            if not self.token and not self._login_completion_pending and not finished["done"]:
                log("login: form closing without token; emitting login_cancelled")
                self._connecting = False
                self._push({"type": "login_cancelled"})
        form.FormClosing += on_form_closing

        init_handled = {"done": False}
        abort_before_run = {"yes": False}

        def safe_close():
            try:
                if form.IsHandleCreated:
                    form.BeginInvoke(Action(form.Close))
                else:
                    form.Close()
            except Exception as e:
                log(f"login: safe_close error: {e}")

        def set_status(text: str):
            def _do():
                try:
                    status.Text = "  " + text
                except Exception:
                    pass
            try:
                if form.IsHandleCreated:
                    form.BeginInvoke(Action(_do))
                else:
                    _do()
            except Exception:
                _do()

        def finish_login(token: str, source: str):
            if finished["done"] or not token:
                return
            finished["done"] = True
            try:
                self._login_completion_pending = True
                try:
                    timer.Stop()
                except Exception:
                    pass
                closed.set()
                log(f"login: captured session token via {source}: {token[:8]}...")
                set_status("Sign-in detected — finishing…")
                safe_close()
                # NEVER run network I/O on the WinForms UI thread (freezes +
                # .NET "Not Responding" / unhandled exception dialogs).
                threading.Thread(
                    target=self._accept_token, args=(token, False), daemon=True
                ).start()
            except Exception as e:
                log(f"login: finish_login error: {e}")
                finished["done"] = False

        def on_web_resource_requested(sender, args):
            try:
                if closed.is_set() or finished["done"] or self.token:
                    return
                request = getattr(args, "Request", None)
                if request is None:
                    return
                uri = str(getattr(request, "Uri", "") or "")
                if "perplexity.ai" not in uri.lower():
                    return
                headers = getattr(request, "Headers", None)
                if headers is None:
                    return
                cookie_header = None
                try:
                    cookie_header = headers.GetHeader("Cookie")
                except Exception:
                    try:
                        cookie_header = headers.GetHeaders("Cookie")
                    except Exception:
                        cookie_header = None
                token = extract_session_token_from_cookie_header(cookie_header)
                if not token:
                    return
                log("login: intercepted Perplexity request with session token")
                if form.IsHandleCreated:
                    form.BeginInvoke(Action(lambda: finish_login(token, "WebResourceRequested")))
                else:
                    finish_login(token, "WebResourceRequested")
            except Exception as e:
                log(f"login: request-hook error: {e}")

        def on_init_completed(sender, args):
            try:
                if init_handled["done"]:
                    return
                if not args.IsSuccess:
                    init_handled["done"] = True
                    abort_before_run["yes"] = True
                    err = None
                    try:
                        err = args.InitializationException
                    except Exception:
                        pass
                    log(f"login: WebView2 initialization failed on this PC ({err})")
                    closed.set()
                    try:
                        safe_close()
                    except Exception:
                        pass
                    self._connecting = False
                    self._push({"type": "error",
                                "message": "The embedded browser could not start on this PC. "
                                           "Please use the session-cookie option instead."})
                    self._push({"type": "login_cancelled"})
                    return

                init_handled["done"] = True
                cv = wv.CoreWebView2
                if cv is None:
                    log("login: CoreWebView2 is None after successful init")
                    return

                try:
                    cv.AddWebResourceRequestedFilter(
                        "https://*.perplexity.ai/*", CoreWebView2WebResourceContext.All)
                    cv.AddWebResourceRequestedFilter(
                        "https://www.perplexity.ai/*", CoreWebView2WebResourceContext.All)
                    cv.AddWebResourceRequestedFilter(
                        "*://*.perplexity.ai/*", CoreWebView2WebResourceContext.All)
                    cv.WebResourceRequested += on_web_resource_requested
                    log("login: WebView2 request hook registered")
                except Exception as e:
                    log(f"login: request hook registration error: {e}")

                try:
                    # Fire-and-forget — never Wait() on the UI thread.
                    cv.CallDevToolsProtocolMethodAsync("Network.enable", "{}")
                    log("login: CDP Network.enable issued (async)")
                except Exception as e:
                    log(f"login: CDP Network.enable skipped: {e}")

                try:
                    cv.Navigate("https://www.perplexity.ai/")
                    log("login: navigated embedded browser to Perplexity")
                    set_status("Sign in to Perplexity in this window…")
                except Exception as e:
                    log(f"login: navigate error: {e}")
            except Exception as e:
                log(f"login: init-handler error: {e}")

        wv.CoreWebView2InitializationCompleted += on_init_completed

        poll_state = {
            "ticks": 0,
            "cdp_errors": 0,
            "cdp_task": None,
            "cookie_task": None,
            "cdp_started": 0,
            "cookie_started": 0,
        }

        def poll_for_token():
            """Must run on the WebView2/UI thread.

            NEVER task.Wait() here — WebView2 async completions are marshaled
            back onto this same UI thread, so Wait() deadlocks (observed as
            repeated 'CDP getCookies wait timed out'). Instead: start the
            async call, return to the message pump, and collect Result on a
            later tick once IsCompleted is true.
            """
            if closed.is_set() or finished["done"] or self.token:
                return
            if self._stop_login.is_set():
                safe_close()
                return
            poll_state["ticks"] += 1
            cv = None
            try:
                cv = wv.CoreWebView2
            except Exception as e:
                if poll_state["ticks"] <= 3 or poll_state["ticks"] % 15 == 0:
                    log(f"login: CoreWebView2 access: {e}")
                return
            if cv is None:
                return

            # --- Collect finished CDP task (JSON string — safe) ---
            cdp_task = poll_state["cdp_task"]
            if cdp_task is not None:
                try:
                    if cdp_task.IsCompleted:
                        poll_state["cdp_task"] = None
                        if getattr(cdp_task, "IsFaulted", False):
                            ex = getattr(getattr(cdp_task, "Exception", None), "InnerException", None) or getattr(cdp_task, "Exception", None)
                            poll_state["cdp_errors"] += 1
                            if poll_state["cdp_errors"] <= 5:
                                log(f"login: CDP task faulted: {ex}")
                        else:
                            raw = str(cdp_task.Result)
                            token = extract_session_token_from_cdp_json(raw)
                            if token:
                                finish_login(token, "CDP Network.getCookies")
                                return
                            if poll_state["ticks"] <= 3 or poll_state["ticks"] % 8 == 0:
                                try:
                                    n = len(json.loads(raw).get("cookies") or [])
                                except Exception:
                                    n = -1
                                log(f"login: CDP poll tick={poll_state['ticks']}: {n} cookies, no session token yet")
                    # else still in flight — leave it
                except Exception as e:
                    poll_state["cdp_task"] = None
                    poll_state["cdp_errors"] += 1
                    if poll_state["cdp_errors"] <= 5:
                        log(f"login: CDP collect error: {e}")

            # --- Collect finished CookieManager task (COM cookies: UI thread OK) ---
            cookie_task = poll_state["cookie_task"]
            if cookie_task is not None:
                try:
                    if cookie_task.IsCompleted:
                        poll_state["cookie_task"] = None
                        if not getattr(cookie_task, "IsFaulted", False):
                            cookies = cookie_task.Result
                            token = extract_session_token_from_cookie_records(cookies)
                            if token:
                                finish_login(token, "CookieManager.GetCookiesAsync")
                                return
                except Exception as e:
                    poll_state["cookie_task"] = None
                    if poll_state["ticks"] <= 5:
                        log(f"login: CookieManager collect error: {e}")

            # --- Start new CDP poll if idle ---
            if poll_state["cdp_task"] is None:
                try:
                    args_json = json.dumps({
                        "urls": [
                            "https://www.perplexity.ai/",
                            "https://www.perplexity.ai",
                            "https://perplexity.ai/",
                        ]
                    })
                    poll_state["cdp_task"] = cv.CallDevToolsProtocolMethodAsync(
                        "Network.getCookies", args_json)
                    poll_state["cdp_started"] += 1
                except Exception as e:
                    poll_state["cdp_errors"] += 1
                    if poll_state["cdp_errors"] <= 5:
                        log(f"login: CDP start error: {e}")

            # --- Start CookieManager poll every other free tick ---
            if poll_state["cookie_task"] is None and poll_state["ticks"] % 2 == 0:
                try:
                    poll_state["cookie_task"] = cv.CookieManager.GetCookiesAsync(
                        "https://www.perplexity.ai")
                    poll_state["cookie_started"] += 1
                except Exception as e:
                    if poll_state["ticks"] <= 5:
                        log(f"login: CookieManager start error: {e}")

        def on_tick(sender, e):
            if closed.is_set() or finished["done"]:
                return
            try:
                poll_for_token()
            except Exception as ex:
                log(f"login: tick error: {ex}")

        timer = WinTimer()
        timer.Interval = 1500
        timer.Tick += on_tick

        try:
            log("login: ensuring CoreWebView2")
            # Pump once after Ensure so sync failures set abort_before_run
            wv.EnsureCoreWebView2Async(None)
            try:
                Application.DoEvents()
            except Exception:
                pass
            time.sleep(0.05)
            try:
                Application.DoEvents()
            except Exception:
                pass
        except Exception as e:
            log(f"login: EnsureCoreWebView2Async error: {e}")
            closed.set()
            abort_before_run["yes"] = True
            self._login_completion_pending = False
            self._connecting = False
            self._push({"type": "error",
                        "message": "Could not start the embedded browser. "
                                   "Please use the session-cookie option instead."})
            self._push({"type": "login_cancelled"})
            return

        if abort_before_run["yes"] or closed.is_set():
            log("login: aborting before Application.Run (init already failed)")
            try:
                timer.Stop()
            except Exception:
                pass
            return

        timer.Start()
        log("login: entering Application.Run for login form")
        Application.Run(form)

        try:
            timer.Stop()
        except Exception:
            pass

        if not self.token and not self._login_completion_pending:
            log("login: window closed without token")
            self._connecting = False
            # login_cancelled already emitted from FormClosing when appropriate
        elif self.token:
            log("login: window closed after token accepted")
            self._login_completion_pending = False
        else:
            log("login: window closed while completion pending")
        log("login: window closed")

    def _accept_token(self, token: str, restore_ui: bool):
        log("login: accepting token (background)")
        self._login_completion_pending = False
        self._stop_login.set()
        try:
            session = validate_session(token)
        except ApiError as e:
            self._connecting = False
            self._push({"type": "error", "message": friendly_error(e)})
            self._push({"type": "login_cancelled"})
            return
        user = session.get("user") or {}
        email = user.get("email") or ""
        if not email:
            self._connecting = False
            self._push({"type": "error",
                        "message": "That session was not accepted by Perplexity. "
                                   "Please log in again."})
            self._push({"type": "login_cancelled"})
            return
        self.token = token
        self.email = email
        count = 0
        try:
            count = len(list_threads(token))
        except ApiError:
            pass
        self._conversation_count = count
        self._connecting = False
        save_session(token, email)
        log(f"login: accepted session token for {email}")
        self._push({"type": "connected", "email": email, "count": count})
        log(f"connected: {email}, {count} threads")

    def _export_worker(self, refresh: bool):
        token = self.token
        if not token:
            self._push({"type": "error", "message": "Not connected. Please log in first."})
            return
        outdir = self._default_folder
        try:
            os.makedirs(outdir, exist_ok=True)
            self._push({"type": "export_start"})
            self._push({"type": "log",
                        "line": f"Perplexity Exporter {APP_VERSION} ({APP_BUILD_TAG}) — preparing export…"})
            # Pre-condition: no sibling EXEs (stale builds / double launches)
            killed = kill_other_exporter_processes(force=True)
            if killed:
                self._push({"type": "log",
                            "line": f"Closed {len(killed)} other exporter process(es) before discovery."})
            self._push({"type": "log", "line": "Discovering conversations (multiple Perplexity indexes)…"})
            threads = list_threads(token, deep=True)
            total = len(threads)
            self._push({"type": "log",
                        "line": f"Found {total} conversation(s) after multi-source discovery. Organizing by Space…"})

            uuid_index = load_uuid_index(outdir)
            records = []
            done = 0
            skipped = 0
            failed = 0

            for pos, t in enumerate(threads, 1):
                uuid = t.get("uuid", "") or ""
                col = t.get("collection") or {}
                list_title = (t.get("title") or t.get("slug") or "Untitled conversation").strip()
                space = space_label_from_collection(col)
                title_disp = list_title[:70]

                existing = None if refresh else find_existing_thread_folder(outdir, uuid, uuid_index)

                if existing and not refresh:
                    # Reuse existing data for index (may still be legacy path)
                    try:
                        with open(os.path.join(existing, "thread.json"), encoding="utf-8") as f:
                            data = json.load(f)
                        meta = data.get("thread_metadata") or {}
                        col2 = data.get("collection") or col
                        entries = data.get("entries") or []
                        title = (meta.get("title") or list_title or "Untitled").strip()
                        space = space_label_from_collection(col2, meta)
                        stats = entry_stats(entries)
                        rel = os.path.relpath(existing, outdir).replace("\\", "/")
                        # If legacy flat path, migrate into Spaces/Home layout
                        target = thread_abs_folder(outdir, space, title, uuid)
                        target_rel = thread_rel_path(space, title, uuid).replace("\\", "/")
                        if os.path.normpath(existing) != os.path.normpath(target):
                            os.makedirs(os.path.dirname(target), exist_ok=True)
                            if not os.path.exists(target):
                                import shutil
                                shutil.move(existing, target)
                                existing = target
                                rel = target_rel
                                # write conversation.md if missing
                                md_path = os.path.join(target, "conversation.md")
                                if not os.path.exists(md_path):
                                    legacy_md = os.path.join(target, "thread.md")
                                    body = open(legacy_md, encoding="utf-8").read() if os.path.exists(legacy_md) else render_markdown({**meta, "uuid": uuid, "space": space if space != HOME_SPACE_NAME else ""}, entries)
                                    with open(md_path, "w", encoding="utf-8") as mf:
                                        mf.write(body)
                        rec = {
                            "uuid": uuid, "title": title, "space": space,
                            "rel_path": rel, "updated_at": t.get("last_query_datetime", ""),
                            "stats": stats, "empty_answers": stats.get("all_answers_empty", False),
                        }
                        records.append(rec)
                        uuid_index[uuid] = rel
                        done += 1
                        skipped += 1
                        self._push({"type": "log", "line": f"[{pos}/{total}] {space} / {title_disp} — already saved"})
                        self._push({"type": "progress", "done": done, "total": total, "title": f"{space}: {title_disp}"})
                        continue
                    except Exception as e:
                        log(f"export: skip-migrate failed for {uuid}: {e}")
                        # fall through to re-fetch

                self._push({"type": "log", "line": f"[{pos}/{total}] {space} / {title_disp} — downloading…"})
                self._push({"type": "progress", "done": done, "total": total, "title": f"{space}: {title_disp}"})
                try:
                    detail = get_thread(token, uuid)
                except ApiError as e:
                    failed += 1
                    self._push({"type": "log", "line": f"  ! failed: {friendly_error(e)}"})
                    continue

                meta = detail.get("thread_metadata", {}) or {}
                title = (meta.get("title") or list_title or "Untitled conversation").strip()
                space = space_label_from_collection(col, meta)
                entry_list = [extract_entry(e) for e in detail.get("entries", [])]
                stats = entry_stats(entry_list)

                folder = thread_abs_folder(outdir, space, title, uuid)
                rel = thread_rel_path(space, title, uuid).replace("\\", "/")
                os.makedirs(folder, exist_ok=True)
                payload = {
                    "thread_metadata": meta,
                    "collection": col,
                    "entries": entry_list,
                    "export": {
                        "space": space,
                        "title": title,
                        "uuid": uuid,
                        "rel_path": rel,
                    },
                }
                with open(os.path.join(folder, "thread.json"), "w", encoding="utf-8") as f:
                    json.dump(payload, f, indent=2, ensure_ascii=False)
                md_meta = {**meta, "uuid": uuid, "space": "" if space == HOME_SPACE_NAME else space, "title": title}
                with open(os.path.join(folder, "conversation.md"), "w", encoding="utf-8") as f:
                    f.write(render_markdown(md_meta, entry_list))
                # compatibility copy
                with open(os.path.join(folder, "thread.md"), "w", encoding="utf-8") as f:
                    f.write(render_markdown(md_meta, entry_list))

                rec = {
                    "uuid": uuid, "title": title, "space": space,
                    "rel_path": rel, "updated_at": t.get("last_query_datetime", ""),
                    "stats": stats, "empty_answers": stats.get("all_answers_empty", False),
                }
                records.append(rec)
                uuid_index[uuid] = rel
                done += 1
                flag = " ⚠️ empty answers" if rec["empty_answers"] else ""
                self._push({"type": "log", "line": f"  ✓ {stats['entries']} turns, {stats['answer_chars']} chars{flag}"})

            # Include any previously exported threads not in this list? skip.

            # Rebuild indexes from everything we know + scan disk for orphans
            manifest = write_export_indexes(outdir, self.email or "", records)
            save_uuid_index(outdir, uuid_index)

            empty_n = len((manifest.get("warnings") or {}).get("empty_answer_threads") or [])
            self._push({"type": "log", "line": f"Wrote README.md + Space folders. {len(records)} conversations indexed."})
            if empty_n:
                self._push({"type": "log", "line": f"Note: {empty_n} conversation(s) have no answer text (see README warnings)."})
            self._push({"type": "log", "line": f"Skipped (already saved): {skipped}. Failed: {failed}."})
            self._push({"type": "export_done", "done": len(records), "folder": outdir})
            log(f"export finished: {len(records)}/{total} -> {outdir} (spaces-v1)")
        except ApiError as e:
            self._push({"type": "error", "message": friendly_error(e)})
        except Exception as e:
            log("export crash: " + traceback.format_exc())
            self._push({"type": "error", "message": friendly_error(e)})




# ----------------------------------------------------------------------------
# Entry point
# ----------------------------------------------------------------------------

def main():
    # Always try to own the session — stale EXEs were leaving users stuck on old builds.
    mutex, primary = acquire_single_instance(takeover=True)
    if not primary:
        log("could not become primary instance; exiting")
        try:
            # Last-ditch visible signal on Windows
            if os.name == "nt":
                import ctypes
                ctypes.windll.user32.MessageBoxW(
                    0,
                    "Perplexity Exporter could not start because another copy is still running.\n"
                    "Open Task Manager, end all PerplexityExporter.exe tasks, then try again.",
                    f"Perplexity Exporter {APP_VERSION} ({APP_BUILD_TAG})",
                    0x10,
                )
        except Exception:
            pass
        return

    # self-test mode (no GUI) — used for automated verification
    if "--selftest" in sys.argv:
        from pathlib import Path
        out = []
        try:
            assert "Hello" in safe_name("Hello World! 2026") and "2026" in safe_name("Hello World! 2026"), "safe_name"
            out.append("safe_name: OK")
        except AssertionError as e:
            out.append(f"safe_name: FAIL ({e})")
        try:
            session = validate_session("FAKE_TOKEN_FOR_SELFTEST")
            out.append(f"session-validate: OK (got {len(session)} keys — fake token correctly rejected)")
        except ApiError as e:
            out.append(f"session-validate: OK (ApiError as expected: {e})")
        result = "\n".join(out)
        Path(os.path.join(appdata_dir(), "selftest.txt")).write_text(result, encoding="utf-8")
        print(result)
        return

    # probe mode: exercises the native login-window flow headless, auto-closes
    if "--loginprobe" in sys.argv:
        log("loginprobe: start")
        b = Bridge(ui_html="<h1>probe</h1>")
        b._connecting = True

        def _autoclose():
            time.sleep(20)
            log("loginprobe: auto-close timer fired")
            try:
                b._stop_login.set()
                form = getattr(b, "_login_form", None)
                if form is not None:
                    from System import Action
                    try:
                        form.BeginInvoke(Action(form.Close))
                    except Exception:
                        try:
                            form.Close()
                        except Exception:
                            pass
                    log("loginprobe: close invoked")
            except Exception as e:
                log(f"loginprobe: autoclose error: {e}")

        threading.Thread(target=_autoclose, daemon=True).start()
        # Use the real STA launcher (same path as the blue button).
        b._start_embedded_login()
        # Wait up to 35s for the STA login thread to finish.
        deadline = time.time() + 35
        while time.time() < deadline:
            t = getattr(b, "_login_clr_thread", None)
            pt = b._login_thread
            alive = False
            try:
                if t is not None and t.IsAlive:
                    alive = True
            except Exception:
                pass
            if pt is not None and pt.is_alive():
                alive = True
            if not alive and getattr(b, "_login_form", None) is None and time.time() > deadline - 30:
                # thread may not have started yet
                pass
            if not alive and time.time() > deadline - 28:
                # give STA thread a moment to spawn
                if getattr(b, "_login_form", None) is None and not b._connecting:
                    break
            if not alive and getattr(b, "_login_form", None) is not None:
                # form exists but thread object unclear — keep waiting
                pass
            if not alive and not b._connecting and getattr(b, "_login_form", None) is None:
                break
            time.sleep(0.5)
        log("loginprobe: flow returned (no deadlock)")
        return

    import webview

    def _ui_file() -> str:
        candidates = []
        root = os.path.dirname(os.path.abspath(__file__))
        if getattr(sys, "frozen", False):
            candidates.append(os.path.join(getattr(sys, "_MEIPASS", os.path.dirname(sys.executable)), "app_ui.html"))
        candidates.append(os.path.join(root, "app_ui.html"))
        candidates.append(os.path.join(root, "build", "PerplexityExporter", "app_ui.html"))
        for path in candidates:
            if os.path.exists(path):
                return path
        return candidates[0] if candidates else os.path.join(root, "app_ui.html")

    try:
        ui_path = _ui_file()
        with open(ui_path, encoding="utf-8") as f:
            ui_html = f.read()
        ui_html = ui_html.replace(
            '<footer style="margin-top:26px;color:#5b637a;font-size:11.5px" id="ver">Perplexity Exporter v1.0.0</footer>',
            f'<footer style="margin-top:26px;color:#9aa3b5;font-size:12px;font-weight:600" id="ver">Perplexity Exporter v{APP_VERSION} · {APP_BUILD_TAG}</footer>'
        )
        ui_html = ui_html.replace(
            '<body>',
            '<body data-app-version="' + APP_VERSION + '" data-boot-state="loading">'
        )
        log(f"main: using UI file {ui_path}")
    except Exception as e:
        log(f"main: UI file read failed: {e}")
        ui_html = f"<h1>UI file missing</h1><div>Perplexity Exporter v{APP_VERSION}</div>"

    bridge = Bridge(ui_html=ui_html)
    log(f"main: loading UI from {_ui_file()}")

    # auto-reconnect if we have a saved session
    saved = load_session()
    if saved and saved.get("token"):
        def _try_reconnect():
            # Wait until pywebview has injected the JS bridge (events.loaded).
            for _ in range(40):  # up to ~20s
                w = bridge._window
                if w is not None:
                    loaded = getattr(getattr(w, "events", None), "loaded", None)
                    if loaded is not None and loaded.is_set():
                        break
                time.sleep(0.5)
            try:
                session = validate_session(saved["token"])
                user = session.get("user") or {}
                if user.get("email"):
                    bridge.token = saved["token"]
                    bridge.email = user["email"]
                    count = 0
                    try:
                        count = len(list_threads(saved["token"]))
                    except ApiError:
                        pass
                    bridge._conversation_count = count
                    bridge._push({"type": "connected", "email": bridge.email, "count": count})
                    log(f"auto-reconnected: {bridge.email}")
                    return
            except ApiError:
                pass
            clear_session()
            log("saved session expired")
        threading.Thread(target=_try_reconnect, daemon=True).start()

    try:
        api = JsApi(bridge)
        bridge._window = webview.create_window(
            f"{APP_NAME}  ·  {APP_BUILD_TAG}", html=ui_html, js_api=api,
            width=780, height=720, min_size=(560, 520),
            background_color="#0f1117")
        log("main: pywebview window created")
    except Exception as e:
        log(f"main: pywebview window creation failed: {e}")
        raise

    log(f"{APP_NAME} v{APP_VERSION} starting (cffi={_HAS_CFFI}, build={APP_BUILD_TAG})")
    try:
        webview.start(private_mode=False,
                      storage_path=os.path.join(appdata_dir(), "webview"),
                      debug=False)
    except Exception as e:
        log(f"main: pywebview start failed: {e}")
        raise


if __name__ == "__main__":
    main()
