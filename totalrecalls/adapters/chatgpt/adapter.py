"""ChatGPT ProviderAdapter."""

from __future__ import annotations

from totalrecalls.adapters.chatgpt.auth import validate_credential
from totalrecalls.adapters.chatgpt.conversations import get_conversation, list_conversations
from totalrecalls.adapters.chatgpt.http import ChatGptApiError
from totalrecalls.core.export_fs import HOME_SPACE_NAME
from totalrecalls.core.paths import log
from totalrecalls.core.schema import (
    AccountInfo,
    Citation,
    ConversationSummary,
    Message,
    UnifiedConversation,
)


def _ts(value) -> str:
    if value is None:
        return ""
    if isinstance(value, (int, float)):
        # ChatGPT often uses unix seconds
        try:
            from datetime import datetime, timezone
            return datetime.fromtimestamp(float(value), tz=timezone.utc).isoformat()
        except Exception:
            return str(value)
    return str(value)


def _walk_messages(detail: dict) -> list[Message]:
    """Convert ChatGPT conversation.mapping tree into ordered Message list."""
    mapping = detail.get("mapping") if isinstance(detail.get("mapping"), dict) else {}
    if not mapping:
        # Some payloads use linear messages
        linear = detail.get("messages") or detail.get("linear_conversation") or []
        msgs: list[Message] = []
        if isinstance(linear, list):
            for m in linear:
                if not isinstance(m, dict):
                    continue
                role = str((m.get("author") or {}).get("role") if isinstance(m.get("author"), dict) else m.get("role") or "")
                content = m.get("content")
                text = _content_to_text(content)
                if role in ("user", "assistant", "system", "tool") and (text or role == "assistant"):
                    msgs.append(Message(role=role, content_md=text, created_at=_ts(m.get("create_time")), external_id=str(m.get("id") or "")))
        return msgs

    # Build children index and find root
    nodes = mapping
    # Prefer current_node chain if present
    ordered_ids: list[str] = []
    current = detail.get("current_node")
    if isinstance(current, str) and current in nodes:
        # walk parents to root then reverse
        chain = []
        seen = set()
        cur = current
        while cur and cur in nodes and cur not in seen:
            seen.add(cur)
            chain.append(cur)
            parent = nodes[cur].get("parent") if isinstance(nodes[cur], dict) else None
            cur = parent
        ordered_ids = list(reversed(chain))
    else:
        # BFS from nodes with no parent
        roots = [k for k, v in nodes.items() if isinstance(v, dict) and not v.get("parent")]
        stack = list(roots)
        seen = set()
        while stack:
            nid = stack.pop(0)
            if nid in seen or nid not in nodes:
                continue
            seen.add(nid)
            ordered_ids.append(nid)
            children = nodes[nid].get("children") if isinstance(nodes[nid], dict) else None
            if isinstance(children, list):
                stack.extend([c for c in children if isinstance(c, str)])

    messages: list[Message] = []
    for nid in ordered_ids:
        node = nodes.get(nid) or {}
        if not isinstance(node, dict):
            continue
        msg = node.get("message")
        if not isinstance(msg, dict):
            continue
        author = msg.get("author") if isinstance(msg.get("author"), dict) else {}
        role = str(author.get("role") or "")
        if role not in ("user", "assistant", "system", "tool"):
            continue
        text = _content_to_text(msg.get("content"))
        # skip empty system noise
        if not text and role != "assistant":
            continue
        cites = _citations_from_message(msg)
        messages.append(
            Message(
                role=role,
                content_md=text,
                created_at=_ts(msg.get("create_time")),
                model=str((msg.get("metadata") or {}).get("model_slug") or "") if isinstance(msg.get("metadata"), dict) else "",
                citations=cites,
                external_id=str(msg.get("id") or nid),
            )
        )
    return messages


def _content_to_text(content) -> str:
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if not isinstance(content, dict):
        return str(content)
    parts = content.get("parts")
    if isinstance(parts, list):
        chunks = []
        for p in parts:
            if isinstance(p, str):
                chunks.append(p)
            elif isinstance(p, dict):
                # multimodal / canvas etc.
                if isinstance(p.get("text"), str):
                    chunks.append(p["text"])
                elif p.get("content_type") == "text" and isinstance(p.get("text"), str):
                    chunks.append(p["text"])
        return "\n".join(chunks).strip()
    if isinstance(content.get("text"), str):
        return content["text"]
    return ""


def _citations_from_message(msg: dict) -> list[Citation]:
    cites: list[Citation] = []
    meta = msg.get("metadata") if isinstance(msg.get("metadata"), dict) else {}
    # common shapes
    for key in ("citations", "source_attributions"):
        block = meta.get(key)
        if isinstance(block, list):
            for c in block:
                if not isinstance(c, dict):
                    continue
                url = str(c.get("url") or c.get("link") or "")
                title = str(c.get("title") or c.get("name") or url)
                if url or title:
                    cites.append(Citation(title=title, url=url, snippet=str(c.get("snippet") or "")))
    return cites


class ChatGptAdapter:
    id = "chatgpt"
    display_name = "ChatGPT"

    def validate(self, credential: str) -> AccountInfo:
        account, _token = validate_credential(credential)
        return account

    def count_conversations(self, credential: str) -> int:
        """Fast conversation count for the connect badge — ONE list request.

        The ChatGPT /backend-api/conversations endpoint returns a ``total``
        field, so an accurate count is a single ~3s request instead of the
        7-pass deep sweep (updated + created + search + archived + Custom GPTs
        + projects). That sweep takes minutes on a populated account and trips
        ChatGPT's limiter (observed live: the connect badge waited 3m39s). The
        full deep enumeration still runs during export, so no conversation is
        ever dropped from a download — only the *badge* gets the fast path.
        """
        from totalrecalls.adapters.chatgpt.conversations import _page_list_conversations
        # NOTE: validate_credential + a 401/403 on the list BOTH raise
        # ChatGptApiError("auth-failed") and must PROPAGATE — the bridge's
        # count-worker turns that into a "session expired, log in again" push.
        # Only non-auth failures (a 500-storm, a transient 5xx) degrade to 0
        # so the badge shows "…/0" quickly instead of eating the full backoff.
        _account, token = validate_credential(credential)
        try:
            # One page, one retry: the badge should degrade fast, never eat
            # the 6-retry / 107s backoff a 500-storm would otherwise trigger.
            items, total = _page_list_conversations(
                token, offset=0, limit=1, order="updated", max_retries=1
            )
        except ChatGptApiError as e:
            if "auth-failed" in str(e):
                raise  # dead session — let the surface handle it (Bug A)
            log(f"chatgpt count: list failed (degrading to 0): {e}")
            return 0
        except Exception as e:
            log(f"chatgpt count: unexpected error (degrading to 0): {e}")
            return 0
        if isinstance(total, int) and total >= 0:
            return total
        return len(items) if isinstance(items, list) else 0

    def list_conversations(self, credential: str, *, deep: bool = False) -> list[ConversationSummary]:
        _account, token = validate_credential(credential)
        items = list_conversations(token, deep=deep)
        out: list[ConversationSummary] = []
        for it in items:
            cid = str(it.get("id") or it.get("conversation_id") or "")
            if not cid:
                continue
            title = str(it.get("title") or "Untitled conversation").strip() or "Untitled conversation"
            out.append(
                ConversationSummary(
                    id=cid,
                    title=title,
                    updated_at=_ts(it.get("update_time") or it.get("updated_at")),
                    created_at=_ts(it.get("create_time") or it.get("created_at")),
                    folder=HOME_SPACE_NAME,
                    raw=it,
                )
            )
        return out

    def fetch_conversation(self, credential: str, conv_id: str) -> UnifiedConversation:
        account, token = validate_credential(credential)
        detail = get_conversation(token, conv_id)
        return self.to_unified(detail, account=account)

    def to_unified(
        self,
        detail: dict,
        *,
        summary: ConversationSummary | None = None,
        account: AccountInfo | None = None,
    ) -> UnifiedConversation:
        detail = detail if isinstance(detail, dict) else {}
        title = str(
            detail.get("title")
            or (summary.title if summary else "")
            or "Untitled conversation"
        ).strip()
        conv_id = str(
            detail.get("conversation_id")
            or detail.get("id")
            or (summary.id if summary else "")
            or ""
        )
        messages = _walk_messages(detail)
        return UnifiedConversation(
            provider=self.id,
            account=account or AccountInfo(),
            id=conv_id,
            title=title or "Untitled conversation",
            created_at=_ts(detail.get("create_time")),
            updated_at=_ts(detail.get("update_time")),
            folder=(summary.folder if summary else HOME_SPACE_NAME) or HOME_SPACE_NAME,
            messages=messages,
            raw={"detail": detail},
        )


# Re-export error type for bridge friendly messages
ApiError = ChatGptApiError
