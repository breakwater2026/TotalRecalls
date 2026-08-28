"""Mistral (chat.mistral.ai) provider adapter."""

from __future__ import annotations

from totalrecalls.adapters.mistral.http import (
    MistralApiError,
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


class MistralAdapter:
    id = "mistral"
    display_name = "Mistral"

    def validate(self, credential: str) -> AccountInfo:
        cookie = cookie_header_from_credential(credential)
        for path in (
            "/api/chat/conversations?page=1&page_size=1",
            "/api/user/me",
            "/api/me",
        ):
            try:
                status, data = request(path, cookie=cookie, delay=0)
            except MistralApiError as e:
                log(f"mistral validate {path}: {e}")
                continue
            if status == 200 and isinstance(data, dict):
                user = data.get("data") or data.get("user") or data
                if isinstance(user, dict):
                    email = str(user.get("email") or user.get("mail") or "")
                    uid = str(user.get("id") or user.get("user_id") or "")
                    name = str(user.get("nickname") or user.get("name") or user.get("username") or "")
                    if email or uid or name:
                        return AccountInfo(
                            email=email or "mistral-session@local",
                            external_id=uid or "mistral",
                            display_name=name or "Mistral user",
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
        endpoint_candidates = [
            "/api/chat/conversations?page={page}&page_size=50",
            "/api/conversations?page={page}&page_size=50",
        ]
        max_pages = 200 if deep else 1
        for tmpl in endpoint_candidates:
            added_any = False
            for page in range(max_pages):
                path = tmpl.format(page=page + 1)  # Mistral appears to be 1-indexed
                try:
                    status, data = request(path, cookie=cookie)
                except MistralApiError as e:
                    log(f"mistral list {path}: {e}")
                    break
                if status != 200 or not isinstance(data, (dict, list)):
                    break
                if isinstance(data, list):
                    items = data
                else:
                    items = (data.get("conversations") or data.get("items")
                             or data.get("list") or (data.get("data") or {}).get("conversations")
                             or [])
                if not isinstance(items, list) or not items:
                    break
                added_any = True
                for c in items:
                    if not isinstance(c, dict):
                        continue
                    cid = str(c.get("id") or c.get("uuid") or c.get("conversation_id") or "")
                    if not cid or cid in seen:
                        continue
                    seen.add(cid)
                    title = str(c.get("title") or c.get("name") or c.get("summary") or "Mistral conversation")
                    out.append(
                        ConversationSummary(
                            id=cid,
                            title=title.strip() or "Mistral conversation",
                            updated_at=_ts(c.get("updated_at") or c.get("updatedAt") or c.get("modify_time")),
                            created_at=_ts(c.get("created_at") or c.get("createdAt") or c.get("create_time")),
                            folder=HOME_SPACE_NAME,
                            raw=c,
                        )
                    )
                if len(items) < 50:
                    break
            if added_any and out:
                break
        if not out:
            log("mistral list: no conversations returned (auth failed or API shape changed)")
        return out

    def fetch_conversation(self, credential: str, conv_id: str) -> UnifiedConversation:
        cookie = cookie_header_from_credential(credential)
        detail = None
        for path in (
            f"/api/chat/conversations/{conv_id}",
            f"/api/conversations/{conv_id}",
        ):
            try:
                status, data = request(path, cookie=cookie)
            except MistralApiError as e:
                log(f"mistral fetch {path}: {e}")
                continue
            if status == 200 and isinstance(data, (dict, list)):
                detail = data if isinstance(data, dict) else {"id": conv_id, "messages": data}
                break
        if not detail:
            raise MistralApiError("http-empty")
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
            detail.get("title") or detail.get("name")
            or (summary.title if summary else "")
            or "Mistral conversation"
        )
        cid = str(
            detail.get("id") or detail.get("conversation_id") or detail.get("uuid")
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
            title=title.strip() or "Mistral conversation",
            created_at=_ts(detail.get("created_at") or detail.get("createdAt") or detail.get("create_time")),
            updated_at=_ts(detail.get("updated_at") or detail.get("updatedAt") or detail.get("modify_time")),
            folder=HOME_SPACE_NAME,
            messages=messages,
            raw={"detail": detail},
        )
