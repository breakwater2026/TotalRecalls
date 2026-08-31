"""DeepSeek chat provider adapter (chat.deepseek.com)."""

from __future__ import annotations

from totalrecalls.adapters.deepseek.http import (
    DeepSeekApiError,
    cookie_header_from_credential,
    looks_like_bearer,
    normalize_bearer,
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


def _resolve_auth(credential: str) -> tuple[str | None, str | None]:
    """Split a credential into (access_token, cookie).

    The login flow captures either a Bearer token (JWT or DeepSeek's opaque
    non-JWT token) or a cookie header. A bare token has no '=' or ';'; a
    cookie always carries 'name=value' pairs.
    """
    cred = (credential or "").strip()
    if not cred:
        raise DeepSeekApiError("auth-failed")
    if looks_like_bearer(cred):
        return normalize_bearer(cred), None
    if "=" not in cred and ";" not in cred:
        # Bare opaque bearer token (DeepSeek's token is not a standard JWT).
        return cred, None
    return None, cookie_header_from_credential(cred)


def _ts(value) -> str:
    """Best-effort timestamp coercion to ISO-ish string."""
    if value is None:
        return ""
    if isinstance(value, (int, float)):
        # Treat as seconds since epoch
        try:
            from datetime import datetime, timezone
            return datetime.fromtimestamp(float(value), tz=timezone.utc).isoformat()
        except Exception:
            return str(value)
    return str(value)


class DeepSeekAdapter:
    id = "deepseek"
    display_name = "DeepSeek"

    def validate(self, credential: str) -> AccountInfo:
        token, cookie = _resolve_auth(credential)
        # Probe an account-scoped endpoint. /api/v0/user/info or /api/user/profile
        # are common shapes; fall back to listing the first page.
        for path in ("/api/v0/user/info", "/api/user/profile", "/api/v0/chat/sessions?page=0&page_size=1"):
            try:
                status, data = request(path, access_token=token, cookie=cookie, delay=0)
            except DeepSeekApiError as e:
                log(f"deepseek validate {path}: {e}")
                continue
            if status == 200 and isinstance(data, dict):
                user = data.get("data") or data.get("user") or data
                if isinstance(user, dict):
                    email = str(user.get("email") or user.get("mail") or "")
                    uid = str(user.get("id") or user.get("user_id") or "")
                    name = str(user.get("nickname") or user.get("name") or user.get("username") or "")
                    if email or uid or name:
                        return AccountInfo(
                            email=email or "deepseek-session@local",
                            external_id=uid or "deepseek",
                            display_name=name or "DeepSeek user",
                        )
        # Optimistic accept if we got anything at all
        if cookie:
            return AccountInfo(
                email="deepseek-session@local",
                external_id="deepseek",
                display_name="DeepSeek user",
            )
        raise DeepSeekApiError("auth-failed")

    def list_conversations(self, credential: str, *, deep: bool = False) -> list[ConversationSummary]:
        token, cookie = _resolve_auth(credential)
        out: list[ConversationSummary] = []
        seen: set[str] = set()
        # Try a few list endpoint shapes; DeepSeek's API has shifted over time.
        endpoint_candidates = [
            "/api/v0/chat/sessions?page={page}&page_size=50",
            "/api/chat/sessions?page={page}&page_size=50",
        ]
        max_pages = 200 if deep else 1
        for tmpl in endpoint_candidates:
            added_any = False
            for page in range(max_pages):
                path = tmpl.format(page=page)
                try:
                    status, data = request(path, access_token=token, cookie=cookie)
                except DeepSeekApiError as e:
                    log(f"deepseek list {path}: {e}")
                    break
                if status != 200 or not isinstance(data, (dict, list)):
                    break
                # Shape: {data: {business_history_list: [...]}} or {sessions: [...]} or [...]
                if isinstance(data, list):
                    items = data
                else:
                    items = (data.get("data") or {}).get("business_history_list") if isinstance(data.get("data"), dict) else None
                    if items is None:
                        items = data.get("sessions") or data.get("conversations") or data.get("items") or data.get("list") or []
                if not isinstance(items, list) or not items:
                    break
                added_any = True
                for it in items:
                    if not isinstance(it, dict):
                        continue
                    cid = str(
                        it.get("chat_session_id") or it.get("session_id")
                        or it.get("id") or it.get("conv_id") or it.get("uuid") or ""
                    )
                    if not cid or cid in seen:
                        continue
                    seen.add(cid)
                    title = str(
                        it.get("title") or it.get("name") or it.get("summary")
                        or "DeepSeek conversation"
                    )
                    out.append(
                        ConversationSummary(
                            id=cid,
                            title=title.strip() or "DeepSeek conversation",
                            updated_at=_ts(it.get("updated_time") or it.get("updated_at") or it.get("modify_time")),
                            created_at=_ts(it.get("created_time") or it.get("created_at") or it.get("create_time")),
                            folder=HOME_SPACE_NAME,
                            raw=it,
                        )
                    )
                if len(items) < 50:
                    break
            if added_any and out:
                # Got data from this endpoint; don't try the others.
                break
        if not out:
            log("deepseek list: no conversations returned (auth failed or API shape changed)")
        return out

    def fetch_conversation(self, credential: str, conv_id: str) -> UnifiedConversation:
        token, cookie = _resolve_auth(credential)
        # Reuse account identity from validate (caller can pass a summary to skip reprobe)
        detail = None
        for path in (
            f"/api/v0/chat/session/{conv_id}",
            f"/api/chat/session/{conv_id}",
            f"/api/v0/chat/sessions/{conv_id}",
        ):
            try:
                status, data = request(path, access_token=token, cookie=cookie)
            except DeepSeekApiError as e:
                log(f"deepseek fetch {path}: {e}")
                continue
            if status == 200 and isinstance(data, (dict, list)):
                if isinstance(data, list):
                    detail = {"id": conv_id, "messages": data}
                else:
                    detail = data
                break
        if not detail:
            raise DeepSeekApiError("http-empty")
        return self.to_unified(detail, account=AccountInfo(
            email="deepseek-session@local",
            external_id="deepseek",
            display_name="DeepSeek user",
        ))

    def to_unified(
        self,
        detail: dict,
        *,
        summary: ConversationSummary | None = None,
        account: AccountInfo | None = None,
    ) -> UnifiedConversation:
        detail = detail if isinstance(detail, dict) else {}
        # Title
        title = str(
            detail.get("title") or detail.get("name")
            or (summary.title if summary else "")
            or "DeepSeek conversation"
        )
        cid = str(
            detail.get("id") or detail.get("chat_session_id")
            or detail.get("session_id")
            or (summary.id if summary else "")
            or ""
        )
        # DeepSeek serves thinking_content + final_answer; both are valuable
        msg_data = (
            detail.get("messages")
            or detail.get("data")
            or detail.get("conversation")
            or []
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
            # DeepSeek exposes both thinking and final answer text
            text = str(
                m.get("final_answer") or m.get("content") or m.get("message")
                or m.get("text") or ""
            ).strip()
            thinking = str(m.get("thinking_content") or "").strip()
            if thinking:
                # Preserve chain-of-thought in markdown; it is often the most
                # valuable part of a DeepSeek export.
                text = f"<details><summary>Thinking</summary>\n\n{thinking}\n\n</details>\n\n{text}"
            if not text.strip():
                continue
            messages.append(
                Message(
                    role=role,
                    content_md=text,
                    created_at=_ts(m.get("created_time") or m.get("timestamp") or m.get("created_at")),
                    model=str(m.get("model") or ""),
                    external_id=str(m.get("id") or m.get("message_id") or ""),
                )
            )
        return UnifiedConversation(
            provider=self.id,
            account=account or AccountInfo(),
            id=cid,
            title=title.strip() or "DeepSeek conversation",
            created_at=_ts(detail.get("created_time") or detail.get("created_at") or detail.get("create_time")),
            updated_at=_ts(detail.get("updated_time") or detail.get("updated_at") or detail.get("modify_time")),
            folder=HOME_SPACE_NAME,
            messages=messages,
            raw={"detail": detail},
        )
