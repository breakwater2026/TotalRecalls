"""Grok (xAI) ProviderAdapter."""

from __future__ import annotations

from totalrecalls.adapters.grok.http import (
    GrokApiError,
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
    cred = (credential or "").strip()
    if not cred:
        raise GrokApiError("auth-failed")
    if looks_like_bearer(cred):
        return normalize_bearer(cred), None
    return None, cookie_header_from_credential(cred)


class GrokAdapter:
    id = "grok"
    display_name = "Grok"

    def validate(self, credential: str) -> AccountInfo:
        token, cookie = _resolve_auth(credential)
        # Probe known session/user endpoints (grok.com since the 2025 move;
        # /api/auth/session verified live — returns {"status": ...}).
        paths = [
            ("/api/auth/session", "https://grok.com"),
            ("/rest/app-chat/conversations", "https://grok.com"),
            ("/rest/user", "https://grok.com"),
        ]
        last_err: Exception | None = None
        for path, base in paths:
            try:
                status, data = request(
                    path, access_token=token, cookie=cookie, delay=0, base=base,
                )
                email = ""
                uid = ""
                name = ""
                if isinstance(data, dict):
                    # /api/auth/session unauthenticated -> {"status": "unauthenticated"}
                    if data.get("status") == "unauthenticated":
                        last_err = GrokApiError("session-unauthenticated")
                        continue
                    user = data.get("user") if isinstance(data.get("user"), dict) else data
                    email = str(user.get("email") or data.get("email") or "")
                    uid = str(user.get("id") or user.get("user_id") or data.get("id") or "")
                    name = str(user.get("name") or user.get("username") or "")
                if email or uid or (isinstance(data, dict) and data.get("status") == "authenticated"):
                    return AccountInfo(
                        email=email or "grok-session@local",
                        external_id=uid or "grok",
                        display_name=name or "Grok user",
                    )
                # Non-empty JSON from a grok.com endpoint = credential accepted
                if data is not None and not (isinstance(data, dict) and "status" in data and len(data) == 1):
                    return AccountInfo(
                        email="grok-session@local",
                        external_id=(token or "cookie")[:16] if (token or cookie) else "grok",
                        display_name="Grok user",
                    )
            except Exception as e:
                last_err = e
                continue
        # Accept bearer/cookie as opaque credential even if probe endpoints moved
        if token or cookie:
            log(f"grok validate: probes failed ({last_err}); accepting credential optimistically")
            return AccountInfo(
                email="grok-session@local",
                external_id=(token or "cookie")[:16],
                display_name="Grok user",
            )
        raise GrokApiError("auth-failed")

    def list_conversations(self, credential: str, *, deep: bool = False) -> list[ConversationSummary]:
        token, cookie = _resolve_auth(credential)
        candidates = [
            ("/rest/app-chat/conversations", "https://grok.com"),
            ("/rest/app-chat/conversations/list", "https://grok.com"),
            ("/rest/conversations", "https://grok.com"),
            ("/api/conversations", "https://grok.com"),
        ]
        items: list = []
        for path, base in candidates:
            try:
                status, data = request(path, access_token=token, cookie=cookie, base=base)
            except GrokApiError as e:
                log(f"grok list {path} failed: {e}")
                continue
            if isinstance(data, list):
                items = data
            elif isinstance(data, dict):
                items = (
                    data.get("conversations")
                    or data.get("items")
                    or data.get("data")
                    or data.get("results")
                    or []
                )
            if items:
                break
        if not items:
            raise GrokApiError(
                "Could not list Grok conversations (API shape may have changed). "
                "Try a fresh browser session token/cookie."
            )
        out: list[ConversationSummary] = []
        for it in items:
            if not isinstance(it, dict):
                continue
            cid = str(it.get("id") or it.get("conversation_id") or it.get("uuid") or "")
            if not cid:
                continue
            title = str(it.get("title") or it.get("name") or it.get("summary") or "Grok conversation")
            out.append(
                ConversationSummary(
                    id=cid,
                    title=title.strip() or "Grok conversation",
                    updated_at=str(it.get("updated_at") or it.get("modified_at") or it.get("create_time") or ""),
                    created_at=str(it.get("created_at") or ""),
                    folder=HOME_SPACE_NAME,
                    raw=it,
                )
            )
        return out

    def fetch_conversation(self, credential: str, conv_id: str) -> UnifiedConversation:
        token, cookie = _resolve_auth(credential)
        # Reuse the account identity from the summary instead of re-validating.
        # The old self.validate() here re-probed up to 3 endpoints before EVERY
        # conversation download — the single biggest contributor to Grok's
        # multi-minute export starts (N conversations × 3 probes × retry
        # backoffs on failing paths).
        if not getattr(self, "_account", None):
            self._account = self.validate(credential)
        account = self._account
        candidates = [
            (f"/rest/app-chat/conversations/{conv_id}/messages", "https://grok.com"),
            (f"/rest/app-chat/conversations/{conv_id}", "https://grok.com"),
            (f"/rest/conversations/{conv_id}", "https://grok.com"),
            (f"/api/conversations/{conv_id}", "https://grok.com"),
        ]
        detail = None
        for path, base in candidates:
            try:
                status, data = request(path, access_token=token, cookie=cookie, base=base)
                if isinstance(data, dict):
                    detail = data
                    break
                if isinstance(data, list):
                    detail = {"id": conv_id, "messages": data}
                    break
            except GrokApiError as e:
                log(f"grok fetch {path}: {e}")
                continue
        if not detail:
            raise GrokApiError("http-empty")
        if "id" not in detail:
            detail = {**detail, "id": conv_id}
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
            or detail.get("name")
            or (summary.title if summary else "")
            or "Grok conversation"
        )
        cid = str(detail.get("id") or detail.get("conversation_id") or (summary.id if summary else "") or "")
        raw_msgs = (
            detail.get("messages")
            or detail.get("items")
            or detail.get("conversation")
            or []
        )
        if isinstance(detail.get("conversation"), dict):
            raw_msgs = detail["conversation"].get("messages") or raw_msgs
        messages: list[Message] = []
        if isinstance(raw_msgs, list):
            for m in raw_msgs:
                if not isinstance(m, dict):
                    continue
                role_raw = str(m.get("role") or m.get("sender") or m.get("author") or "").lower()
                if role_raw in ("user", "human"):
                    role = "user"
                elif role_raw in ("assistant", "grok", "model", "bot"):
                    role = "assistant"
                elif role_raw == "system":
                    role = "system"
                else:
                    role = "assistant" if m.get("content") or m.get("message") else "user"
                text = str(
                    m.get("content")
                    or m.get("message")
                    or m.get("text")
                    or m.get("response")
                    or ""
                ).strip()
                if isinstance(m.get("content"), list):
                    parts = []
                    for p in m["content"]:
                        if isinstance(p, str):
                            parts.append(p)
                        elif isinstance(p, dict) and isinstance(p.get("text"), str):
                            parts.append(p["text"])
                    text = "\n".join(parts).strip()
                if not text:
                    continue
                messages.append(
                    Message(
                        role=role,
                        content_md=text,
                        created_at=str(m.get("created_at") or m.get("timestamp") or ""),
                        model=str(m.get("model") or ""),
                        external_id=str(m.get("id") or ""),
                    )
                )
        return UnifiedConversation(
            provider=self.id,
            account=account or AccountInfo(),
            id=cid,
            title=title.strip() or "Grok conversation",
            created_at=str(detail.get("created_at") or ""),
            updated_at=str(detail.get("updated_at") or ""),
            folder=HOME_SPACE_NAME,
            messages=messages,
            raw={"detail": detail},
        )


ApiError = GrokApiError
