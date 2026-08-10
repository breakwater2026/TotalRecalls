"""Claude.ai conversation list + detail."""

from __future__ import annotations

from totalrecalls.adapters.claude.http import ClaudeApiError, request
from totalrecalls.core.paths import log


def list_conversations(cookie: str, org_id: str, *, deep: bool = False) -> list[dict]:
    """List chat conversations for an organization."""
    # Claude paginates with last_uuid / limit in some builds; try simple list first.
    path = f"/api/organizations/{org_id}/chat_conversations"
    try:
        status, data = request(path, cookie)
    except ClaudeApiError as e:
        log(f"claude list failed: {e}")
        return []
    items: list = []
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        items = data.get("chat_conversations") or data.get("data") or data.get("conversations") or []
    out = [it for it in items if isinstance(it, dict) and (it.get("uuid") or it.get("id"))]
    if deep and isinstance(data, dict):
        # best-effort extra page if API supports cursor
        cursor = data.get("next") or data.get("cursor")
        pages = 0
        while cursor and pages < 20:
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
    log(f"claude list: {len(out)} conversation(s) org={org_id[:8]}…")
    return out


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
