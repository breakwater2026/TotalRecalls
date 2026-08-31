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
    Citation,
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


def _is_error(data) -> bool:
    """Grok returns error envelopes like {code: 5, message: 'Not Found'}."""
    return isinstance(data, dict) and data.get("code") not in (0, None)


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
        # Endpoints known to exist on grok.com. Most return 401/403 with
        # webview-captured cookies — the prior memory note (2026-08-23)
        # documents that all of these reject SSO cookies. We try several
        # shapes and paginate the first one that returns data, in case xAI
        # ever enables a working path. Any 4xx/5xx is silently skipped.
        candidates = [
            "/rest/app-chat/conversations",
            "/rest/app-chat/conversations/list",
            "/rest/conversations",
            "/api/conversations",
            "/rest/user/conversations",          # user-scoped alt
            "/api/conversations/me",             # me-scoped alt
            "/rest/app-chat/users/me/conversations",  # gizmo-style alt
        ]
        seen: dict[str, dict] = {}
        tried_paths: list[str] = []
        for path in candidates:
            items = _grok_paginate(path, token, cookie, base="https://grok.com")
            tried_paths.append(path)
            for it in items:
                cid = _grok_conv_id(it)
                if cid and cid not in seen:
                    seen[cid] = it
            if items and deep:
                # Already got some from a working endpoint — try the next
                # candidate too in case it surfaces a different set.
                continue
            if items:
                break
        items = list(seen.values())
        if not items:
            # Endpoints reachable but no list shape matched (auth rejected or
            # API moved). Raise a soft error: the connection's 0-conversation
            # count is the real signal that the session cookie is dead.
            log(
                "grok list: all candidate endpoints returned no conversations "
                f"(tried {len(tried_paths)} paths, auth rejected or API shape changed)."
            )
            raise GrokApiError(
                "Could not list Grok conversations (API shape may have changed). "
                "Try a fresh browser session token/cookie."
            )
        out: list[ConversationSummary] = []
        for it in items:
            if not isinstance(it, dict):
                continue
            cid = _grok_conv_id(it) or ""
            if not cid:
                continue
            title = str(it.get("title") or it.get("name") or it.get("summary") or "Grok conversation")
            out.append(
                ConversationSummary(
                    id=cid,
                    title=title.strip() or "Grok conversation",
                    updated_at=str(it.get("updated_at") or it.get("modifyTime") or it.get("modified_at") or ""),
                    created_at=str(it.get("createTime") or it.get("created_at") or ""),
                    folder=HOME_SPACE_NAME,
                    raw=it,
                )
            )
        return out

    def fetch_conversation(self, credential: str, conv_id: str) -> UnifiedConversation:
        token, cookie = _resolve_auth(credential)
        # Reuse the account identity from the summary instead of re-validating.
        if not getattr(self, "_account", None):
            self._account = self.validate(credential)
        account = self._account
        detail: dict = {}
        # Grok serves conversation metadata at .../{id} and the message thread
        # at .../{id}/responses (the old .../messages path 404s).
        try:
            status, data = request(
                f"/rest/app-chat/conversations/{conv_id}",
                access_token=token, cookie=cookie,
            )
            if isinstance(data, dict) and not _is_error(data):
                detail.update(data)
        except GrokApiError as e:
            log(f"grok fetch metadata {conv_id[:8]}…: {e}")
        try:
            status, data = request(
                f"/rest/app-chat/conversations/{conv_id}/responses",
                access_token=token, cookie=cookie,
            )
            if isinstance(data, dict) and not _is_error(data):
                detail["responses"] = data.get("responses") or []
        except GrokApiError as e:
            log(f"grok fetch responses {conv_id[:8]}…: {e}")
        detail.setdefault("responses", [])
        detail.setdefault("id", conv_id)
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
        cid = str(
            detail.get("conversationId")
            or detail.get("id")
            or detail.get("conversation_id")
            or (summary.id if summary else "")
            or ""
        )
        raw_msgs = (
            detail.get("responses")
            or detail.get("messages")
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
                role_raw = str(m.get("sender") or m.get("role") or m.get("author") or "").lower()
                if role_raw in ("user", "human"):
                    role = "user"
                elif role_raw in ("assistant", "grok", "model", "bot"):
                    role = "assistant"
                elif role_raw == "system":
                    role = "system"
                else:
                    role = "assistant" if (m.get("content") or m.get("message")) else "user"
                text = str(
                    m.get("message")
                    or m.get("content")
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
                cites: list[Citation] = []
                for c in (m.get("webSearchResults") or []):
                    if isinstance(c, dict):
                        url = str(c.get("url") or "")
                        t = str(c.get("title") or "")
                        if url or t:
                            cites.append(
                                Citation(title=t or url, url=url,
                                         snippet=str(c.get("preview") or ""))
                            )
                messages.append(
                    Message(
                        role=role,
                        content_md=text,
                        created_at=str(m.get("createTime") or m.get("created_at") or m.get("timestamp") or ""),
                        model=str(m.get("model") or ""),
                        citations=cites,
                        external_id=str(m.get("responseId") or m.get("id") or ""),
                    )
                )
        return UnifiedConversation(
            provider=self.id,
            account=account or AccountInfo(),
            id=cid,
            title=title.strip() or "Grok conversation",
            created_at=str(detail.get("createTime") or detail.get("created_at") or ""),
            updated_at=str(detail.get("modifyTime") or detail.get("updated_at") or ""),
            folder=HOME_SPACE_NAME,
            messages=messages,
            raw={"detail": detail},
        )


ApiError = GrokApiError


def _grok_conv_id(it: dict) -> str | None:
    """Extract a conversation id from a Grok response item (shape varies)."""
    for k in ("id", "conversationId", "conversation_id", "uuid", "thread_id"):
        v = it.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return None


def _grok_paginate(path: str, token: str | None, cookie: str | None,
                   *, base: str = "https://grok.com",
                   max_pages: int = 50) -> list[dict]:
    """Paginate a Grok list endpoint. Some shapes return all items at once;
    others (notably /rest/app-chat/conversations) use a lastId cursor.
    """
    out: list[dict] = []
    cursor: str | None = None
    for page in range(max_pages):
        sep = "&" if "?" in path else "?"
        suffix = f"{sep}lastId={cursor}" if cursor else ""
        try:
            status, data = request(path + suffix, access_token=token,
                                   cookie=cookie, base=base)
        except GrokApiError as e:
            log(f"grok list {path} page={page} failed: {e}")
            return out
        if not isinstance(data, (dict, list)):
            return out
        items = data if isinstance(data, list) else (
            data.get("conversations") or data.get("items")
            or data.get("data") or data.get("results") or []
        )
        if not isinstance(items, list) or not items:
            return out
        for it in items:
            if isinstance(it, dict):
                out.append(it)
        # Look for the next cursor in the response envelope
        next_cursor = None
        if isinstance(data, dict):
            for k in ("lastId", "last_id", "next_cursor", "nextCursor", "cursor"):
                v = data.get(k)
                if isinstance(v, str) and v.strip() and v != cursor:
                    next_cursor = v.strip()
                    break
        if not next_cursor or next_cursor == cursor:
            return out
        cursor = next_cursor
    log(f"grok list {path} hit {max_pages}-page safety cap")
    return out
