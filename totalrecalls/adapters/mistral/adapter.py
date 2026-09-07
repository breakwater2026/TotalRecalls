"""Mistral (chat.mistral.ai) provider adapter.

chat.mistral.ai (Le Chat) is a tRPC app.  The conversation list comes from the
``chat.last`` query and a conversation's messages from ``message.all`` (input
``{"chatId": <uuid>}``).  Auth is the Ory Kratos session cookie captured by the
login flow — no Authorization header.
"""

from __future__ import annotations

from totalrecalls.adapters.mistral.http import (
    MistralApiError,
    cookie_header_from_credential,
    trpc_query,
)
from totalrecalls.core.export_fs import HOME_SPACE_NAME
from totalrecalls.core.paths import log
from totalrecalls.core.schema import (
    AccountInfo,
    ConversationSummary,
    Message,
    UnifiedConversation,
)


def _ts(value) -> str:
    """Best-effort timestamp coercion to ISO-ish string."""
    if value is None:
        return ""
    if isinstance(value, (int, float)):
        try:
            from datetime import datetime, timezone
            return datetime.fromtimestamp(float(value), tz=timezone.utc).isoformat()
        except Exception:
            return str(value)
    return str(value)


def _linearize_messages(items: list) -> list[dict]:
    """Order Mistral message versions into a single linear transcript.

    Each message carries version links (``nextVersion``/``prevVersion``) and a
    ``turn`` index.  Keep only the latest version of each message (the one with
    no ``nextVersion``) and order by (turn, role).
    """
    msgs = [m for m in items if isinstance(m, dict)]
    latest = [m for m in msgs if m.get("nextVersion") is None]
    if not latest:
        latest = msgs
    role_rank = {"user": 0, "assistant": 1, "system": -1}
    latest.sort(key=lambda m: (
        int(m.get("turn") or 0),
        role_rank.get(str(m.get("role") or "").lower(), 2),
        str(m.get("id") or ""),
    ))
    return latest


class MistralAdapter:
    id = "mistral"
    display_name = "Mistral"

    def validate(self, credential: str) -> AccountInfo:
        cookie = cookie_header_from_credential(credential)
        try:
            status, data = trpc_query("chat.last", {}, cookie=cookie, delay=0)
        except MistralApiError as e:
            log(f"mistral validate: {e}")
            status, data = 0, None
        if status == 200 and isinstance(data, dict):
            return AccountInfo(
                email="mistral-session@local",
                external_id="mistral",
                display_name="Mistral user",
            )
        if cookie:
            return AccountInfo(
                email="mistral-session@local",
                external_id="mistral",
                display_name="Mistral user",
            )
        raise MistralApiError("auth-failed")

    def list_conversations(self, credential: str, *, deep: bool = False) -> list[ConversationSummary]:
        cookie = cookie_header_from_credential(credential)
        out: list[ConversationSummary] = []
        seen: set[str] = set()
        cursor = None
        max_pages = 200 if deep else 1
        for _ in range(max_pages):
            inp = {} if cursor is None else {"cursor": cursor}
            try:
                status, data = trpc_query("chat.last", inp, cookie=cookie)
            except MistralApiError as e:
                # 401/403 on the first request = dead session (validate() is
                # lenient and accepts any cookie). Mid-pagination means the
                # session was live → break.
                if cursor is None and "auth-failed" in str(e):
                    log(f"mistral list chat.last auth-failed — session rejected: {e}")
                    raise
                log(f"mistral list chat.last: {e}")
                break
            if status != 200 or not isinstance(data, dict):
                break
            items = data.get("items") or []
            next_cursor = data.get("nextCursor")
            if not isinstance(items, list) or not items:
                break
            new_here = 0
            for c in items:
                if not isinstance(c, dict):
                    continue
                cid = str(c.get("id") or "")
                if not cid or cid in seen:
                    continue
                seen.add(cid)
                new_here += 1
                title = str(
                    c.get("userTitle") or c.get("generatedTitle")
                    or c.get("title") or "Mistral conversation"
                )
                out.append(
                    ConversationSummary(
                        id=cid,
                        title=title.strip() or "Mistral conversation",
                        updated_at=_ts(c.get("updatedAt") or c.get("updated_at")),
                        created_at=_ts(c.get("createdAt") or c.get("created_at")),
                        folder=HOME_SPACE_NAME,
                        raw=c,
                    )
                )
            if next_cursor is None or new_here == 0:
                break
            cursor = next_cursor
        if not out:
            log("mistral list: no conversations returned (auth failed or API shape changed)")
        return out

    def fetch_conversation(self, credential: str, conv_id: str) -> UnifiedConversation:
        cookie = cookie_header_from_credential(credential)
        try:
            status, data = trpc_query("message.all", {"chatId": conv_id}, cookie=cookie)
        except MistralApiError as e:
            raise MistralApiError(f"http-empty: {e}") from e
        if status != 200 or not isinstance(data, dict):
            raise MistralApiError("http-empty")
        items = data.get("items") or []
        detail = {"id": conv_id, "messages": items}
        return self.to_unified(detail, account=AccountInfo(
            email="mistral-session@local",
            external_id="mistral",
            display_name="Mistral user",
        ))

    def to_unified(
        self,
        detail: dict,
        *,
        summary: ConversationSummary | None = None,
        account: AccountInfo | None = None,
    ) -> UnifiedConversation:
        detail = detail if isinstance(detail, dict) else {}
        title = str(
            detail.get("title") or detail.get("generatedTitle")
            or (summary.title if summary else "")
            or "Mistral conversation"
        )
        cid = str(
            detail.get("id") or detail.get("conversation_id")
            or (summary.id if summary else "") or ""
        )
        msg_items = detail.get("messages") or detail.get("data") or []
        if isinstance(detail.get("data"), dict):
            msg_items = detail["data"].get("messages") or detail["data"].get("items") or msg_items
        ordered = _linearize_messages(msg_items if isinstance(msg_items, list) else [])
        messages: list[Message] = []
        for m in ordered:
            role_raw = str(m.get("role") or "").lower()
            if role_raw in ("user", "human"):
                role = "user"
            elif role_raw in ("assistant", "model", "bot", "ai"):
                role = "assistant"
            elif role_raw == "system":
                role = "system"
            else:
                role = "assistant"
            text = str(m.get("content") or m.get("message") or m.get("text") or "").strip()
            if not text:
                continue
            messages.append(
                Message(
                    role=role,
                    content_md=text,
                    created_at=_ts(m.get("createdAt") or m.get("created_at")),
                    model=str(m.get("model") or ""),
                    external_id=str(m.get("id") or ""),
                )
            )
        return UnifiedConversation(
            provider=self.id,
            account=account or AccountInfo(),
            id=cid,
            title=title.strip() or "Mistral conversation",
            created_at=_ts(detail.get("createdAt") or detail.get("created_at")),
            updated_at=_ts(detail.get("updatedAt") or detail.get("updated_at")),
            folder=HOME_SPACE_NAME,
            messages=messages,
            raw={"detail": detail},
        )
