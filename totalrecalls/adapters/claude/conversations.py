"""Claude.ai conversation list + detail."""

from __future__ import annotations

from totalrecalls.adapters.claude.http import ClaudeApiError, request
from totalrecalls.core.paths import log


# Safety ceiling for cursor pagination. The old code capped at 20 pages
# (~1000 conversations at 50/page); bumped to 100 to reach deep accounts.
_MAX_CLAUDE_PAGES = 100


def list_conversations(cookie: str, org_id: str, *, deep: bool = False) -> list[dict]:
    """List chat conversations for an organization.

    Claude paginates with a cursor. In deep mode we follow up to
    _MAX_CLAUDE_PAGES pages, well above the old 20-page floor. We also
    walk Projects (`/api/organizations/{org}/projects`), which keeps a
    separate conversation index that the global list does not surface.
    """
    path = f"/api/organizations/{org_id}/chat_conversations"
    try:
        status, data = request(path, cookie)
    except ClaudeApiError as e:
        # A 401/403 on the primary list means the session cookie is dead —
        # surface it so the UI can prompt a reconnect. (multi-org callers
        # still catch per-org; an all-orgs 401 is a dead session too.)
        if "auth-failed" in str(e):
            log(f"claude list org={org_id[:8]}… auth-failed: {e}")
            raise
        log(f"claude list failed: {e}")
        return []
    items: list = []
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        items = data.get("chat_conversations") or data.get("data") or data.get("conversations") or []
    out = [it for it in items if isinstance(it, dict) and (it.get("uuid") or it.get("id"))]
    if deep and isinstance(data, dict):
        # best-effort extra pages if API supports cursor
        cursor = data.get("next") or data.get("cursor")
        pages = 0
        while cursor and pages < _MAX_CLAUDE_PAGES:
            pages += 1
            try:
                _s, more = request(f"{path}?cursor={cursor}", cookie)
            except ClaudeApiError:
                break
            batch = more if isinstance(more, list) else (more.get("chat_conversations") if isinstance(more, dict) else [])
            if not batch:
                break
            out.extend([it for it in batch if isinstance(it, dict)])
            cursor = more.get("next") or more.get("cursor") if isinstance(more, dict) else None
        # Walk Projects — Claude keeps Project chats in a separate index.
        _walk_projects(cookie, org_id, out)
    log(f"claude list: {len(out)} conversation(s) org={org_id[:8]}…")
    return out


def _walk_projects(cookie: str, org_id: str, out: list[dict]) -> None:
    """Enumerate Claude Projects and pull each one's conversation list.

    Mutates `out` in place. Best-effort: any 4xx/5xx is silently skipped.
    """
    try:
        _s, data = request(f"/api/organizations/{org_id}/projects?limit=100", cookie)
    except ClaudeApiError as e:
        log(f"claude projects list failed: {e}")
        return
    if not isinstance(data, dict):
        return
    projects = (data.get("data") or data.get("projects")
                or data.get("results") or data.get("items") or [])
    if not isinstance(projects, list) or not projects:
        return
    seen_ids: set[str] = set()
    for it in out:
        cid = it.get("uuid") or it.get("id")
        if isinstance(cid, str):
            seen_ids.add(cid)
    added = 0
    for proj in projects:
        if not isinstance(proj, dict):
            continue
        pid = proj.get("uuid") or proj.get("id") or proj.get("project_id")
        if not pid:
            continue
        # Two common shapes:
        #   A) /api/organizations/{org}/projects/{pid}/chat_conversations
        #   B) /api/projects/{pid}/chat_conversations
        candidates = [
            f"/api/organizations/{org_id}/projects/{pid}/chat_conversations",
            f"/api/projects/{pid}/chat_conversations",
        ]
        for proj_path in candidates:
            try:
                _s, pdata = request(proj_path, cookie)
            except ClaudeApiError:
                continue
            if not isinstance(pdata, (dict, list)):
                continue
            pitems = (pdata if isinstance(pdata, list)
                      else (pdata.get("chat_conversations") or pdata.get("data")
                            or pdata.get("conversations") or []))
            if not isinstance(pitems, list) or not pitems:
                continue
            for it in pitems:
                if not isinstance(it, dict):
                    continue
                cid = it.get("uuid") or it.get("id")
                if not cid or cid in seen_ids:
                    continue
                # Tag the project on the item so the export path can route
                # it under Spaces/<project title> rather than Home.
                it = dict(it)
                it["_project_uuid"] = pid
                it["_project_title"] = (proj.get("name") or proj.get("title") or "")
                out.append(it)
                seen_ids.add(str(cid))
                added += 1
            break  # one working endpoint per project is enough for first pass
    log(f"claude projects: walked {len(projects)} project(s), +{added} new conversation(s)")


def get_conversation(cookie: str, org_id: str, conv_id: str) -> dict:
    path = (
        f"/api/organizations/{org_id}/chat_conversations/{conv_id}"
        f"?tree=True&rendering_mode=messages&render_all_tools=true"
    )
    try:
        status, data = request(path, cookie)
    except ClaudeApiError:
        # fallback without query flags
        status, data = request(
            f"/api/organizations/{org_id}/chat_conversations/{conv_id}",
            cookie,
        )
    if not isinstance(data, dict):
        raise ClaudeApiError("http-empty")
    return data


def list_conversations_multi(cookie: str, org_ids: list[str], *, deep: bool = False) -> list[dict]:
    """List conversations across every organization the session can access.

    Multi-org accounts keep a separate conversation index per organization;
    the old single-org path only ever surfaced the first org. This walks all
    of them and tags each item with `_org_id` so callers can disambiguate.
    """
    out: list[dict] = []
    seen: set[str] = set()
    for org_id in org_ids:
        try:
            items = list_conversations(cookie, org_id, deep=deep)
        except ClaudeApiError as e:
            # A 401/403 is a SESSION-level signal — the same cookie is used for
            # every org, so if it's rejected on one it's dead for all. Propagate
            # it (don't continue past it) so the UI can prompt a reconnect
            # instead of silently returning [] for a dead session.
            if "auth-failed" in str(e):
                log(f"claude list org {org_id[:8]}… auth-failed — session rejected: {e}")
                raise
            log(f"claude list org {org_id[:8]}… failed: {e}")
            continue
        for it in items:
            if not isinstance(it, dict):
                continue
            cid = it.get("uuid") or it.get("id")
            key = str(cid) if cid else None
            if key and key in seen:
                continue
            if key:
                seen.add(key)
            tagged = dict(it)
            tagged["_org_id"] = org_id
            out.append(tagged)
    return out


def get_conversation_multi(cookie: str, org_ids: list[str], conv_id: str) -> dict:
    """Fetch a conversation across orgs, returning the first org that has it."""
    for org_id in org_ids:
        try:
            detail = get_conversation(cookie, org_id, conv_id)
        except ClaudeApiError:
            continue
        # Some orgs return an error-shaped dict instead of 404ing.
        if isinstance(detail, dict) and detail.get("error"):
            continue
        return detail
    raise ClaudeApiError("http-empty")
