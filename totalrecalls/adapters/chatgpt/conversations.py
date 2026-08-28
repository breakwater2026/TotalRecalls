"""ChatGPT conversation list + detail fetch."""

from __future__ import annotations

from totalrecalls.adapters.chatgpt.http import ChatGptApiError, request
from totalrecalls.core.paths import log


# Safety ceiling for deep pagination. The API can serve more, but we cap
# defensively so a misconfigured account can't run forever. 50k is well above
# any single user's real account size and is what the prior 5000 cap was
# meant to approximate — but the prior cap was a floor that left real
# conversations on the table for power users.
_DEEP_MAX_OFFSET = 50_000


def _page_list_conversations(access_token: str, *, offset: int, limit: int,
                             order: str) -> tuple[list[dict], int | None]:
    """One page of /backend-api/conversations. Returns (items, total) or ([], _)."""
    path = f"/backend-api/conversations?offset={offset}&limit={limit}&order={order}"
    try:
        status, data = request(path, access_token=access_token)
    except ChatGptApiError as e:
        log(f"chatgpt list order={order} offset={offset} failed: {e}")
        return [], None
    if not isinstance(data, dict):
        return [], None
    items = data.get("items") or data.get("conversations") or []
    if not isinstance(items, list) or not items:
        return [], data.get("total")
    return items, data.get("total")


def _merge_unique(into: dict[str, dict], items: list[dict]) -> int:
    """Add items to `into` keyed by conversation id, filling empty fields. Returns new count."""
    added = 0
    for it in items:
        if not isinstance(it, dict):
            continue
        cid = it.get("id") or it.get("conversation_id")
        if not cid:
            continue
        cid = str(cid)
        if cid in into:
            # Fill any empty fields from the new source
            for k, v in it.items():
                if v not in (None, "", [], {}) and into[cid].get(k) in (None, "", [], {}):
                    into[cid][k] = v
        else:
            into[cid] = dict(it)
            added += 1
    return added


def list_conversations(access_token: str, *, deep: bool = False) -> list[dict]:
    """Page through backend-api/conversations.

    In deep mode, performs two ordered passes and a search pass to maximize
    the number of conversations captured:
      1) order=updated (recent activity)  — covers most users
      2) order=created (oldest first)     — catches never-updated old threads
      3) empty search_term                 — provider often returns the full set

    Results are de-duplicated by conversation id. The old code had a hard
    5000-offset floor in deep mode, which left conversations on the table
    for accounts that exceed that bound.
    """
    seen: dict[str, dict] = {}

    if not deep:
        # Shallow pass: a few pages is enough for the connect-count badge
        items, _ = _page_list_conversations(access_token, offset=0, limit=28, order="updated")
        _merge_unique(seen, items)
        log(f"chatgpt list: {len(seen)} conversation(s) deep={deep}")
        return list(seen.values())

    # Pass 1: order=updated (newest activity first)
    offset = 0
    limit = 28
    while offset <= _DEEP_MAX_OFFSET:
        items, total = _page_list_conversations(access_token, offset=offset,
                                                limit=limit, order="updated")
        if not items:
            break
        _merge_unique(seen, items)
        offset += len(items)
        if isinstance(total, int) and offset >= total:
            break
        if len(items) < limit:
            break

    # Pass 2: order=created (oldest first) — catches never-updated threads
    # that never show up in the updated-sorted index. Empty/short replies
    # or archived chats often have no update activity.
    offset = 0
    while offset <= _DEEP_MAX_OFFSET:
        items, total = _page_list_conversations(access_token, offset=offset,
                                                limit=limit, order="created")
        if not items:
            break
        _merge_unique(seen, items)
        offset += len(items)
        if isinstance(total, int) and offset >= total:
            break
        if len(items) < limit:
            break

    # Pass 3: search pass with empty term. The provider's search endpoint
    # often returns conversations that the list endpoint omits (archived,
    # shared, custom-gpt threads, etc.). Empty search term usually = "all".
    offset = 0
    while offset <= _DEEP_MAX_OFFSET:
        path = (f"/backend-api/conversations?offset={offset}&limit={limit}"
                f"&order=updated&search_term=")
        try:
            status, data = request(path, access_token=access_token)
        except ChatGptApiError as e:
            log(f"chatgpt search pass offset={offset} failed: {e}")
            break
        if not isinstance(data, dict):
            break
        items = data.get("items") or data.get("conversations") or []
        if not isinstance(items, list) or not items:
            break
        _merge_unique(seen, items)
        offset += len(items)
        if len(items) < limit:
            break

    # Pass 4: walk Custom GPTs (Gizmos). Each gizmo has its own conversation
    # list at /backend-api/gizmos/{gizmo_id}/conversations. Power users keep
    # the majority of their work inside gizmos and the global list only
    # returns Home threads.
    _walk_gizmos(access_token, seen)

    log(f"chatgpt list: {len(seen)} unique conversation(s) deep={deep}")
    return list(seen.values())


def _walk_gizmos(access_token: str, seen: dict[str, dict]) -> None:
    """Pass 4: enumerate Custom GPTs and pull each one's conversation list.

    Mutates `seen` in place; merges by conversation id (a gizmo conversation
    shares the same id space as the global list, so dedup is automatic).
    Best-effort: any gizmo endpoint that 4xx/5xx is silently skipped.
    """
    try:
        status, data = request("/backend-api/gizmos?limit=100", access_token=access_token)
    except ChatGptApiError as e:
        log(f"chatgpt gizmos list failed: {e}")
        return
    if not isinstance(data, dict):
        return
    # Shape varies: {"items": [...]} or {"gizmos": [...]} or a top-level list
    if isinstance(data, list):
        gizmos = data
    else:
        gizmos = (data.get("items") or data.get("gizmos")
                  or data.get("data") or data.get("results") or [])
    if not isinstance(gizmos, list) or not gizmos:
        return
    added = 0
    for g in gizmos:
        if not isinstance(g, dict):
            continue
        gid = g.get("id") or g.get("gizmo_id") or g.get("uuid")
        if not gid:
            continue
        gid = str(gid)
        # Paginate this gizmo's conversation list. Some users have hundreds
        # of conversations in a single gizmo.
        offset = 0
        while offset <= _DEEP_MAX_OFFSET:
            path = (f"/backend-api/gizmos/{gid}/conversations"
                    f"?offset={offset}&limit=28&order=updated")
            try:
                _s, gdata = request(path, access_token=access_token)
            except ChatGptApiError as e:
                log(f"chatgpt gizmo {gid[:8]}… offset={offset} failed: {e}")
                break
            if not isinstance(gdata, dict):
                break
            gitems = gdata.get("items") or gdata.get("conversations") or []
            if not isinstance(gitems, list) or not gitems:
                break
            new_here = _merge_unique(seen, gitems)
            added += new_here
            offset += len(gitems)
            if len(gitems) < 28:
                break
    log(f"chatgpt gizmos: walked {len(gizmos)} gizmo(s), +{added} new conversation(s)")


def get_conversation(access_token: str, conv_id: str) -> dict:
    path = f"/backend-api/conversation/{conv_id}"
    status, data = request(path, access_token=access_token)
    if not isinstance(data, dict):
        raise ChatGptApiError("http-empty")
    return data
