"""Claude.ai ProviderAdapter."""

from __future__ import annotations

from totalrecalls.adapters.claude.auth import validate_credential
from totalrecalls.adapters.claude.conversations import get_conversation, list_conversations
from totalrecalls.adapters.claude.http import ClaudeApiError
from totalrecalls.core.export_fs import HOME_SPACE_NAME
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
    return str(value)


def _messages_from_detail(detail: dict) -> list[Message]:
    msgs: list[Message] = []
    # Common shapes: chat_messages list
    raw_list = (
        detail.get("chat_messages")
        or detail.get("messages")
        or detail.get("history")
        or []
    )
    if not isinstance(raw_list, list):
        return msgs
    for m in raw_list:
        if not isinstance(m, dict):
            continue
        sender = str(m.get("sender") or m.get("role") or "").lower()
        if sender in ("human", "user"):
            role = "user"
        elif sender in ("assistant", "claude", "bot"):
            role = "assistant"
        elif sender in ("system",):
            role = "system"
        else:
            # skip tool/noise unless text present as assistant
            role = "assistant" if m.get("text") or m.get("content") else ""
        if not role:
            continue
        text = _content_text(m)
        if not text and role != "assistant":
            continue
        cites = []
        for c in m.get("citations") or []:
            if isinstance(c, dict):
                cites.append(
                    Citation(
                        title=str(c.get("title") or c.get("filename") or ""),
                        url=str(c.get("url") or ""),
                        snippet=str(c.get("excerpt") or c.get("snippet") or ""),
                    )
                )
        msgs.append(
            Message(
                role=role,
                content_md=text,
                created_at=_ts(m.get("created_at") or m.get("updated_at")),
                model=str(m.get("model") or ""),
                citations=cites,
                external_id=str(m.get("uuid") or m.get("id") or ""),
            )
        )
    return msgs


def _content_text(m: dict) -> str:
    if isinstance(m.get("text"), str) and m["text"].strip():
        return m["text"].strip()
    content = m.get("content")
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict):
                if isinstance(block.get("text"), str):
                    parts.append(block["text"])
                elif block.get("type") == "text" and isinstance(block.get("text"), str):
                    parts.append(block["text"])
        return "\n".join(parts).strip()
    return ""


class ClaudeAdapter:
    id = "claude"
    display_name = "Claude"

    def validate(self, credential: str) -> AccountInfo:
        account, _cookie, _org = validate_credential(credential)
        return account

    def list_conversations(self, credential: str, *, deep: bool = False) -> list[ConversationSummary]:
        _account, cookie, org_id = validate_credential(credential)
        items = list_conversations(cookie, org_id, deep=deep)
        out: list[ConversationSummary] = []
        for it in items:
            cid = str(it.get("uuid") or it.get("id") or "")
            if not cid:
                continue
            title = str(it.get("name") or it.get("title") or "Untitled conversation").strip()
            # If the conversations walker tagged this with a project, route it
            # under the project name as a Space rather than dumping everything
            # in Home.
            project = (it.get("_project_title") or "").strip()
            folder = project or HOME_SPACE_NAME
            out.append(
                ConversationSummary(
                    id=cid,
                    title=title or "Untitled conversation",
                    updated_at=_ts(it.get("updated_at") or it.get("modified_at")),
                    created_at=_ts(it.get("created_at")),
                    folder=folder,
                    raw=it,
                )
            )
        return out

    def fetch_conversation(self, credential: str, conv_id: str) -> UnifiedConversation:
        account, cookie, org_id = validate_credential(credential)
        detail = get_conversation(cookie, org_id, conv_id)
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
            detail.get("name")
            or detail.get("title")
            or (summary.title if summary else "")
            or "Untitled conversation"
        ).strip()
        conv_id = str(
            detail.get("uuid")
            or detail.get("id")
            or (summary.id if summary else "")
            or ""
        )
        return UnifiedConversation(
            provider=self.id,
            account=account or AccountInfo(),
            id=conv_id,
            title=title or "Untitled conversation",
            created_at=_ts(detail.get("created_at")),
            updated_at=_ts(detail.get("updated_at")),
            folder=(summary.folder if summary else HOME_SPACE_NAME) or HOME_SPACE_NAME,
            messages=_messages_from_detail(detail),
            raw={"detail": detail},
        )


ApiError = ClaudeApiError
