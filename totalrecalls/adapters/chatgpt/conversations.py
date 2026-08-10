"""ChatGPT conversation list + detail fetch."""

from __future__ import annotations

from totalrecalls.adapters.chatgpt.http import ChatGptApiError, request
from totalrecalls.core.paths import log


def list_conversations(access_token: str, *, deep: bool = False) -> list[dict]:
    """Page through backend-api/conversations."""
    out: list[dict] = []
    offset = 0
    limit = 28
    max_offset = 5000 if deep else 500
    while offset <= max_offset:
        path = f"/backend-api/conversations?offset={offset}&limit={limit}&order=updated"
        try:
            status, data = request(path, access_token=access_token)
        except ChatGptApiError as e:
            log(f"chatgpt list offset={offset} failed: {e}")
            break
        if not isinstance(data, dict):
            break
        items = data.get("items") or data.get("conversations") or []
        if not isinstance(items, list) or not items:
            break
        for it in items:
            if isinstance(it, dict) and (it.get("id") or it.get("conversation_id")):
                out.append(it)
        total = data.get("total")
        offset += len(items)
        if isinstance(total, int) and offset >= total:
            break
        if len(items) < limit:
            break
        if not deep and offset >= limit * 3:
            # shallow: a few pages is enough for connect-count
            break
    log(f"chatgpt list: {len(out)} conversation(s) deep={deep}")
    return out


def get_conversation(access_token: str, conv_id: str) -> dict:
    path = f"/backend-api/conversation/{conv_id}"
    status, data = request(path, access_token=access_token)
    if not isinstance(data, dict):
        raise ChatGptApiError("http-empty")
    return data
