"""Qwen Chat (chat.qwen.ai) provider adapter.

The web app at chat.qwen.ai uses Alibaba's internal REST API surface.
We try a few candidate endpoint shapes and fail soft. The exact paths
need a live DevTools probe to confirm; this scaffold is best-effort.
"""

from __future__ import annotations

from totalrecalls.adapters.qwen.http import (
    BASE,
    QwenChatApiError,
    cookie_header_from_credential,
    request,
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
    """Best-effort timestamp coercion."""
    if value is None:
        return ""
    if isinstance(value, (int, float)):
        try:
            from datetime import datetime, timezone
            return datetime.fromtimestamp(float(value), tz=timezone.utc).isoformat()
        except Exception:
            return str(value)
    return str(value)


class QwenChatAdapter:
    id = "qwen"
    display_name = "Qwen Chat"

    def validate(self, credential: str) -> AccountInfo:
        cookie = cookie_header_from_credential(credential)
        # Try a few user-info / me endpoints
        for path in (
            "/api/v1/users/me",
            "/api/user/info",
            "/api/me",
            "/api/v1/me",
        ):
            try:
                status, data = request(path, cookie=cookie, delay=0)
            except QwenChatApiError as e:
                log(f"qwen validate {path}: {e}")
                continue
            if status == 200 and isinstance(data, dict):
                user = data.get("data") or data.get("user") or data
                if isinstance(user, dict):
                    email = str(user.get("email") or user.get("mail") or "")
                    uid = str(user.get("id") or user.get("user_id") or "")
                    name = str(user.get("nickname") or user.get("name") or user.get("username") or "")
                    if email or uid or name:
                        return AccountInfo(
                            email=email or "qwen-session@local",
                            external_id=uid or "qwen",
                            display_name=name or "Qwen user",
                        )
        # Optimistic accept
        if cookie:
            return AccountInfo(
                email="qwen-session@local",
                external_id="qwen",
                display_name="Qwen user",
            )
        raise QwenChatApiError("auth-failed")

    def list_conversations(self, credential: str, *, deep: bool = False) -> list[ConversationSummary]:
        cookie = cookie_header_from_credential(credential)
        out: list[ConversationSummary] = []
        seen: set[str] = set()
        endpoint_candidates = [
            "/api/v1/chat/sessions?page={page}&page_size=50",
            "/api/chat/list?page={page}&page_size=50",
            "/api/v1/conversations?page={page}&page_size=50",
        ]
        max_pages = 200 if deep else 1
        for tmpl in endpoint_candidates:
            added_any = False
            for page in range(max_pages):
                path = tmpl.format(page=page)
                try:
                    status, data = request(path, cookie=cookie)
                except QwenChatApiError as e:
                    log(f"qwen list {path}: {e}")
                    break
                if status != 200 or not isinstance(data, (dict, list)):
                    break
                if isinstance(data, list):
                    items = data
                else:
                    items = (data.get("data") or {}).get("list") if isinstance(data.get("data"), dict) else None
                    if items is None:
                        items = (data.get("sessions") or data.get("conversations")
                                 or data.get("items") or data.get("history") or [])
                if not isinstance(items, list) or not items:
                    break
                added_any = True
                for it in items:
                    if not isinstance(it, dict):
                        continue
                    cid = str(
                        it.get("id") or it.get("session_id") or it.get("chat_id")
                        or it.get("conversation_id") or it.get("uuid") or ""
                    )
                    if not cid or cid in seen:
                        continue
                    seen.add(cid)
                    title = str(
                        it.get("title") or it.get("name") or it.get("summary")
                        or "Qwen conversation"
                    )
                    out.append(
                        ConversationSummary(
                            id=cid,
                            title=title.strip() or "Qwen conversation",
                            updated_at=_ts(it.get("updated_at") or it.get("updatedAt") or it.get("modify_time")),
                            created_at=_ts(it.get("created_at") or it.get("createdAt") or it.get("create_time")),
                            folder=HOME_SPACE_NAME,
                            raw=it,
                        )
                    )
                if len(items) < 50:
                    break
            if added_any and out:
                break
        if not out:
            log("qwen list: no conversations returned (auth failed or API shape changed)")
        return out

    def fetch_conversation(self, credential: str, conv_id: str) -> UnifiedConversation:
        cookie = cookie_header_from_credential(credential)
        detail = None
        for path in (
            f"/api/v1/chat/sessions/{conv_id}",
            f"/api/chat/session/{conv_id}",
            f"/api/v1/conversations/{conv_id}",
        ):
            try:
                status, data = request(path, cookie=cookie)
            except QwenChatApiError as e:
                log(f"qwen fetch {path}: {e}")
                continue
            if status == 200 and isinstance(data, (dict, list)):
                if isinstance(data, list):
                    detail = {"id": conv_id, "messages": data}
                else:
                    detail = data
                break
        if not detail:
            raise QwenChatApiError("http-empty")
        return self.to_unified(detail, account=AccountInfo(
            email="qwen-session@local",
            external_id="qwen",
            display_name="Qwen user",
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
            detail.get("title") or detail.get("name")
            or (summary.title if summary else "")
            or "Qwen conversation"
        )
        cid = str(
            detail.get("id") or detail.get("session_id") or detail.get("chat_id")
            or (summary.id if summary else "")
            or ""
        )
        msg_data = (
            detail.get("messages") or detail.get("data")
            or detail.get("conversation") or []
        )
        if isinstance(detail.get("data"), dict):
            msg_data = detail["data"].get("messages") or msg_data
        messages: list[Message] = []
        for m in msg_data if isinstance(msg_data, list) else []:
            if not isinstance(m, dict):
                continue
            role_raw = str(m.get("role") or m.get("sender") or "").lower()
            if role_raw in ("user", "human"):
                role = "user"
            elif role_raw in ("assistant", "model", "bot", "ai"):
                role = "assistant"
            else:
                role = "assistant"
            text = str(
                m.get("content") or m.get("message") or m.get("text") or ""
            ).strip()
            if not text:
                continue
            messages.append(
                Message(
                    role=role,
                    content_md=text,
                    created_at=_ts(m.get("created_at") or m.get("createdAt") or m.get("timestamp")),
                    model=str(m.get("model") or ""),
                    external_id=str(m.get("id") or m.get("message_id") or ""),
                )
            )
        return UnifiedConversation(
            provider=self.id,
            account=account or AccountInfo(),
            id=cid,
            title=title.strip() or "Qwen conversation",
            created_at=_ts(detail.get("created_at") or detail.get("createdAt") or detail.get("create_time")),
            updated_at=_ts(detail.get("updated_at") or detail.get("updatedAt") or detail.get("modify_time")),
            folder=HOME_SPACE_NAME,
            messages=messages,
            raw={"detail": detail},
        )
