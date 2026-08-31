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
                             order: str, is_archived: bool | None = None,
                             is_starred: bool | None = None) -> tuple[list[dict], int | None]:
    """One page of /backend-api/conversations. Returns (items, total) or ([], _)."""
    q = [f"offset={offset}", f"limit={limit}", f"order={order}"]
    if is_archived is not None:
        q.append(f"is_archived={str(is_archived).lower()}")
    if is_starred is not None:
        q.append(f"is_starred={str(is_starred).lower()}")
    path = "/backend-api/conversations?" + "&".join(q)
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


def _paginate(access_token: str, seen: dict[str, dict], *, limit: int = 28,
              order: str = "updated", is_archived: bool | None = None,
              is_starred: bool | None = None) -> int:
    """Paginate one /backend-api/conversations shape into `seen`. Returns new count."""
    offset = 0
    added = 0
    while offset <= _DEEP_MAX_OFFSET:
        items, total = _page_list_conversations(
            access_token, offset=offset, limit=limit, order=order,
            is_archived=is_archived, is_starred=is_starred,
        )
        if not items:
            break
        added += _merge_unique(seen, items)
        offset += len(items)
        if isinstance(total, int) and offset >= total:
            break
        if len(items) < limit:
            break
    return added


def _paginate_search(access_token: str, seen: dict[str, dict], *, limit: int = 28) -> None:
    """Search pass with an empty term — the provider often returns the full set
    including archived/shared/custom-gpt threads the plain list omits."""
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


def list_conversations(access_token: str, *, deep: bool = False) -> list[dict]:
    """Page through backend-api/conversations.

    Deep mode runs several passes to maximize coverage:
      1) order=updated                 — recent activity (covers most users)
      2) order=created                 — never-updated old threads
      3) empty search_term             — archived/shared/custom-gpt threads
      4) is_archived=true (unstarred)  — archived chats excluded by default
      5) is_archived=true (starred)    — archived + starred chats
      6) Custom GPTs (gizmos)          — per-gizmo conversation lists
      7) Projects (snorlax)            — per-project conversation lists

    Results are de-duplicated by conversation id.
    """
    seen: dict[str, dict] = {}

    if not deep:
        # Shallow pass: a few pages is enough for the connect-count badge
        items, _ = _page_list_conversations(access_token, offset=0, limit=28, order="updated")
        _merge_unique(seen, items)
        log(f"chatgpt list: {len(seen)} conversation(s) deep={deep}")
        return list(seen.values())

    _paginate(access_token, seen, order="updated")
    _paginate(access_token, seen, order="created")
    _paginate_search(access_token, seen)
    _paginate(access_token, seen, is_archived=True, is_starred=False)
    _paginate(access_token, seen, is_archived=True, is_starred=True)
    _walk_gizmos(access_token, seen)
    _walk_projects(access_token, seen)

    log(f"chatgpt list: {len(seen)} unique conversation(s) deep={deep}")
    return list(seen.values())


def _walk_gizmos(access_token: str, seen: dict[str, dict]) -> None:
    """Enumerate Custom GPTs and pull each one's conversation list.

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


def _walk_projects(access_token: str, seen: dict[str, dict]) -> None:
    """Enumerate ChatGPT Projects (snorlax) and pull each one's conversations.

    Projects are kept in a separate index from the global list and from Custom
    GPTs, served by /backend-api/gizmos/snorlax/sidebar. Each project is a
    gizmo whose conversation list lives at /backend-api/gizmos/{id}/conversations
    (same surface as Custom GPTs). Best-effort: any 4xx/5xx is skipped.
    """
    try:
        status, data = request(
            "/backend-api/gizmos/snorlax/sidebar?conversations_per_gizmo=5&owned_only=true",
            access_token=access_token,
        )
    except ChatGptApiError as e:
        log(f"chatgpt projects sidebar failed: {e}")
        return
    if isinstance(data, list):
        projects = data
    elif isinstance(data, dict):
        projects = (data.get("gizmos") or data.get("projects")
                    or data.get("items") or data.get("data")
                    or data.get("results") or [])
    else:
        projects = []
    if not isinstance(projects, list) or not projects:
        return
    added = 0
    for p in projects:
        if not isinstance(p, dict):
            continue
        pid = p.get("id") or p.get("gizmo_id") or p.get("uuid") or p.get("project_id")
        if not pid:
            continue
        pid = str(pid)
        offset = 0
        while offset <= _DEEP_MAX_OFFSET:
            path = (f"/backend-api/gizmos/{pid}/conversations"
                    f"?offset={offset}&limit=28&order=updated")
            try:
                _s, gdata = request(path, access_token=access_token)
            except ChatGptApiError as e:
                log(f"chatgpt project {pid[:8]}… offset={offset} failed: {e}")
                break
            if not isinstance(gdata, dict):
                break
            gitems = gdata.get("items") or gdata.get("conversations") or []
            if not isinstance(gitems, list) or not gitems:
                break
            added += _merge_unique(seen, gitems)
            offset += len(gitems)
            if len(gitems) < 28:
                break
    log(f"chatgpt projects: walked {len(projects)} project(s), +{added} new conversation(s)")


def get_conversation(access_token: str, conv_id: str) -> dict:
    path = f"/backend-api/conversation/{conv_id}"
    try:
        status, data = request(path, access_token=access_token)
    except ChatGptApiError:
        # Newer cohorts serve conversation detail at the plural path with
        # include_has_versions. Fall back if the singular endpoint is gone.
        status, data = request(
            f"/backend-api/conversations/{conv_id}?include_has_versions=true",
            access_token=access_token,
        )
    if not isinstance(data, dict):
        raise ChatGptApiError("http-empty")
    return data
