"""DeepSeek chat provider adapter (chat.deepseek.com).

Verified against Aver005/deep-reverse (live-captured 2026-06-27). Endpoints:

    validate -> GET /api/v0/users/current
    list     -> GET /api/v0/chat_session/fetch_page   (keyset cursor + has_more)
    fetch    -> GET /api/v0/chat/history_messages?chat_session_id=<uuid>

Every response is the {code, msg, data: {biz_code, biz_msg, biz_data}} envelope.
DeepSeek's full-history list is cursor-paginated (`lte_cursor.updated_at` +
`lte_cursor.id`); the old `/api/v0/chat/sessions?page=` guess silently returned
only the first page (~50), which is what caused the shallow listing.
"""

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
    Citation,
    ConversationSummary,
    Message,
    UnifiedConversation,
)

# Safety cap for keyset-cursor pagination, per pinned pass.
_MAX_DEEP_PAGES = 200


def _resolve_auth(credential: str) -> tuple[str | None, str | None]:
    """Split a credential into (access_token, cookie).

    The login flow captures a Bearer token (JWT or DeepSeek's opaque non-JWT
    token). A bare token has no '=' or ';'; a cookie always carries
    'name=value' pairs.
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


def _biz_data(data) -> object:
    """Unwrap the {code,msg,data:{biz_code,biz_msg,biz_data}} envelope."""
    if not isinstance(data, dict):
        return data
    if data.get("code") not in (0, None):
        raise DeepSeekApiError(f"api-{data.get('code')}: {data.get('msg', '')}")
    inner = data.get("data")
    if isinstance(inner, dict):
        if inner.get("biz_code") not in (0, None):
            raise DeepSeekApiError(f"biz-{inner.get('biz_code')}: {inner.get('biz_msg', '')}")
        bd = inner.get("biz_data")
        if bd is not None:
            return bd
    return data


def _ts(value) -> str:
    """Best-effort timestamp coercion (DeepSeek uses fractional epoch seconds)."""
    if value is None:
        return ""
    if isinstance(value, (int, float)):
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
        user = None
        try:
            status, data = request("/api/v0/users/current", access_token=token, cookie=cookie, delay=0)
            user = _biz_data(data)
        except DeepSeekApiError as e:
            log(f"deepseek validate users/current: {e}")
        if isinstance(user, dict):
            email = str(user.get("email") or "")
            uid = str(user.get("id") or "")
            if email or uid:
                return AccountInfo(
                    email=email or "deepseek-session@local",
                    external_id=uid or "deepseek",
                    display_name=email or "DeepSeek user",
                )
        # Optimistic accept: login captured a real Bearer token.
        if token or cookie:
            return AccountInfo(
                email="deepseek-session@local",
                external_id=(token or "cookie")[:16],
                display_name="DeepSeek user",
            )
        raise DeepSeekApiError("auth-failed")

    def list_conversations(self, credential: str, *, deep: bool = False) -> list[ConversationSummary]:
        token, cookie = _resolve_auth(credential)
        seen: dict[str, dict] = {}
        # DeepSeek separates pinned and unpinned sessions; walk both to avoid
        # missing pinned chats (which the default list omits).
        max_pages = _MAX_DEEP_PAGES if deep else 1
        for pinned in (True, False):
            cursor_ts: float | None = None
            cursor_id: str | None = None
            pages = 0
            while pages < max_pages:
                pages += 1
                params = [f"lte_cursor.pinned={str(pinned).lower()}"]
                if cursor_ts is not None:
                    params.append(f"lte_cursor.updated_at={cursor_ts}")
                if cursor_id:
                    params.append(f"lte_cursor.id={cursor_id}")
                path = "/api/v0/chat_session/fetch_page?" + "&".join(params)
                try:
                    status, data = request(path, access_token=token, cookie=cookie)
                except DeepSeekApiError as e:
                    log(f"deepseek list {path}: {e}")
                    break
                payload = _biz_data(data)
                if not isinstance(payload, dict):
                    break
                sessions = payload.get("chat_sessions") or []
                if not isinstance(sessions, list) or not sessions:
                    break
                for s in sessions:
                    if not isinstance(s, dict):
                        continue
                    sid = str(s.get("id") or "")
                    if sid and sid not in seen:
                        seen[sid] = s
                if not payload.get("has_more", False):
                    break
                last = sessions[-1]
                cursor_ts = last.get("updated_at")
                cursor_id = str(last.get("id") or "") or None
                if cursor_ts is None and not cursor_id:
                    break

        out: list[ConversationSummary] = []
        for s in seen.values():
            sid = str(s.get("id") or "")
            title = str(s.get("title") or "").strip() or "DeepSeek conversation"
            out.append(
                ConversationSummary(
                    id=sid,
                    title=title,
                    updated_at=_ts(s.get("updated_at")),
                    created_at=_ts(s.get("inserted_at") or s.get("created_at")),
                    folder=HOME_SPACE_NAME,
                    raw=s,
                )
            )
        if not out:
            log("deepseek list: no conversations returned (auth failed or API shape changed)")
        return out

    def fetch_conversation(self, credential: str, conv_id: str) -> UnifiedConversation:
        token, cookie = _resolve_auth(credential)
        status, data = request(
            f"/api/v0/chat/history_messages?chat_session_id={conv_id}",
            access_token=token, cookie=cookie,
        )
        payload = _biz_data(data)
        if not isinstance(payload, dict):
            raise DeepSeekApiError("http-empty")
        return self.to_unified(
            payload,
            summary=ConversationSummary(id=conv_id, title="", folder=HOME_SPACE_NAME),
        )

    def to_unified(
        self,
        detail: dict,
        *,
        summary: ConversationSummary | None = None,
        account: AccountInfo | None = None,
    ) -> UnifiedConversation:
        detail = detail if isinstance(detail, dict) else {}
        session = detail.get("chat_session") if isinstance(detail.get("chat_session"), dict) else {}
        title = str(
            session.get("title")
            or detail.get("title")
            or (summary.title if summary else "")
        ).strip() or "DeepSeek conversation"
        cid = str(
            session.get("id")
            or detail.get("id")
            or (summary.id if summary else "")
            or ""
        )
        model_type = str(session.get("model_type") or "")
        return UnifiedConversation(
            provider=self.id,
            account=account or AccountInfo(),
            id=cid,
            title=title,
            created_at=_ts(session.get("inserted_at") or detail.get("inserted_at")),
            updated_at=_ts(session.get("updated_at") or detail.get("updated_at")),
            folder=(summary.folder if summary else HOME_SPACE_NAME) or HOME_SPACE_NAME,
            messages=self._messages_from_detail(detail, model_type),
            raw={"detail": detail},
        )

    def _messages_from_detail(self, detail: dict, model_type: str = "") -> list[Message]:
        msgs = detail.get("chat_messages") or []
        messages: list[Message] = []
        if not isinstance(msgs, list):
            return messages
        for m in msgs:
            if not isinstance(m, dict):
                continue
            role_raw = str(m.get("role") or "").lower()
            if role_raw == "user":
                role = "user"
            elif role_raw == "assistant":
                role = "assistant"
            else:
                continue
            fragments = m.get("fragments") or []
            text_parts: list[str] = []
            thinking_parts: list[str] = []
            cites: list[Citation] = []
            if isinstance(fragments, list):
                for f in fragments:
                    if not isinstance(f, dict):
                        continue
                    ftype = str(f.get("type") or "").upper()
                    content = str(f.get("content") or "")
                    if ftype in ("REQUEST", "RESPONSE"):
                        text_parts.append(content)
                    elif ftype == "THINK":
                        thinking_parts.append(content)
                    refs = f.get("references")
                    if isinstance(refs, list):
                        for r in refs:
                            if isinstance(r, dict):
                                url = str(r.get("url") or r.get("link") or "")
                                t = str(r.get("title") or r.get("name") or url)
                                if url or t:
                                    cites.append(Citation(title=t, url=url))
            text = "\n".join(p for p in text_parts if p.strip()).strip()
            thinking = "\n".join(p for p in thinking_parts if p.strip()).strip()
            if thinking:
                # Preserve chain-of-thought; often the most valuable part.
                text = f"<details><summary>Thinking</summary>\n\n{thinking}\n\n</details>\n\n{text}"
            if not text.strip():
                continue
            messages.append(
                Message(
                    role=role,
                    content_md=text,
                    created_at=_ts(m.get("inserted_at") or m.get("created_at")),
                    model=model_type,
                    citations=cites,
                    external_id=str(m.get("message_id") or ""),
                )
            )
        return messages
