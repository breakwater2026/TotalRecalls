"""Multi-source Perplexity conversation discovery."""

from __future__ import annotations

from totalrecalls.core.paths import log
from totalrecalls.adapters.perplexity.http import API_VERSION, ApiError, request

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

