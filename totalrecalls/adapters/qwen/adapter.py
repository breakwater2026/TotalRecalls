"""Qwen Chat (chat.qwen.ai) provider adapter.

The web app at chat.qwen.ai authenticates the web client purely via session
cookies (no Authorization header) against the `/api/v2/*` REST surface,
reverse-engineered from the qwen-chat-fe frontend bundle:

  GET /api/v2/chats/?page=<n>&exclude_project=true -> {success, data:[{id,title,...}]}
  GET /api/v2/chats/<id>                           -> {success, data:{chat:{history:{...}, title, ...}}}

`history.messages` is an OBJECT MAP keyed by message id (not a list).
Messages form a tree via `parentId`/`childrenIds`; an assistant's
`parentId` points at the user message it answers. Assistant text lives in
`content_list` items whose `phase == "answer"`; web-search citations live
in `phase == "web_search"` items (`extra.web_search_info`).
"""

from __future__ import annotations

from totalrecalls.adapters.qwen.http import (
    BASE_V2,
    QwenChatApiError,
    cookie_header_from_credential,
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

_DEFAULT_ACCOUNT = AccountInfo(
    email="qwen-session@local",
    external_id="qwen",
    display_name="Qwen user",
)

_LIST_PATH = f"{BASE_V2}/chats/?page={{page}}&exclude_project=true"


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


def _first(d: dict, *keys):
    for k in keys:
        v = d.get(k)
        if v not in (None, "", [], {}):
            return v
    return None


class QwenChatAdapter:
    id = "qwen"
    display_name = "Qwen Chat"

    # -- transport ---------------------------------------------------------

    def validate(self, credential: str) -> AccountInfo:
        cookie = cookie_header_from_credential(credential)
        status, data = request(_LIST_PATH.format(page=1), cookie=cookie, delay=0)
        if status != 200:
            raise QwenChatApiError(f"http-{status}")
        if isinstance(data, dict) and data.get("success") is False:
            raise QwenChatApiError("auth-failed")
        # The list probe above is the real auth check. Account identity is a
        # best-effort enrichment — never let it fail a valid session.
        email, uid, name = (
            _DEFAULT_ACCOUNT.email,
            _DEFAULT_ACCOUNT.external_id,
            _DEFAULT_ACCOUNT.display_name,
        )
        try:
            s2, ud = request(f"{BASE_V2}/users/status", cookie=cookie, delay=0)
            if s2 == 200 and isinstance(ud, dict):
                u = ud.get("data") if isinstance(ud.get("data"), dict) else ud
                if isinstance(u, dict):
                    email = str(u.get("email") or u.get("mail") or email)
                    uid = str(u.get("id") or u.get("user_id") or u.get("uid") or uid)
                    name = str(u.get("nickname") or u.get("name") or u.get("username") or name)
        except Exception:
            pass
        return AccountInfo(email=email, external_id=uid, display_name=name)

    def list_conversations(self, credential: str, *, deep: bool = False) -> list[ConversationSummary]:
        cookie = cookie_header_from_credential(credential)
        out: list[ConversationSummary] = []
        seen: set[str] = set()
        max_pages = 200 if deep else 3
        for page in range(1, max_pages + 1):
            path = _LIST_PATH.format(page=page)
            try:
                status, data = request(path, cookie=cookie)
            except QwenChatApiError as e:
                log(f"qwen list page {page}: {e}")
                break
            if status != 200:
                break
            if isinstance(data, dict):
                if data.get("success") is False:
                    log(f"qwen list page {page}: success=false (auth/empty)")
                    break
                items = data.get("data")
            else:
                items = data
            if not isinstance(items, list) or not items:
                break  # exhausted pages
            for it in items:
                if not isinstance(it, dict):
                    continue
                cid = str(it.get("id") or it.get("chat_id") or "")
                if not cid or cid in seen:
                    continue
                seen.add(cid)
                title = str(it.get("title") or "").strip() or "Qwen conversation"
                out.append(
                    ConversationSummary(
                        id=cid,
                        title=title,
                        updated_at=_ts(_first(it, "update_time", "updated_at", "updatedAt",
                                              "modify_time", "last_modified", "updateTime")),
                        created_at=_ts(_first(it, "create_time", "created_at", "createdAt", "createTime")),
                        folder=HOME_SPACE_NAME,
                        raw=it,
                    )
                )
        if not out:
            log("qwen list: no conversations returned (auth failed or empty account)")
        return out

    def fetch_conversation(self, credential: str, conv_id: str) -> UnifiedConversation:
        cookie = cookie_header_from_credential(credential)
        status, data = request(f"{BASE_V2}/chats/{conv_id}", cookie=cookie)
        if status != 200:
            raise QwenChatApiError(f"http-{status}")
        if not isinstance(data, dict):
            raise QwenChatApiError("http-empty")
        if data.get("success") is False:
            raise QwenChatApiError("auth-failed")
        payload = data.get("data")
        chat = None
        if isinstance(payload, dict):
            chat = payload.get("chat") if isinstance(payload.get("chat"), dict) else payload
        if not isinstance(chat, dict):
            chat = {"id": conv_id}
        return self.to_unified(chat, account=_DEFAULT_ACCOUNT)

    # -- parsing -----------------------------------------------------------

    def to_unified(
        self,
        detail: dict,
        *,
        summary: ConversationSummary | None = None,
        account: AccountInfo | None = None,
    ) -> UnifiedConversation:
        detail = detail if isinstance(detail, dict) else {}
        history = detail.get("history") if isinstance(detail.get("history"), dict) else {}
        messages_map = history.get("messages")
        if not isinstance(messages_map, dict):
            messages_map = {}
        current_id = str(history.get("currentId") or history.get("current_id") or "")

        cid = str(detail.get("id") or detail.get("chat_id")
                  or (summary.id if summary else "") or "")
        title = str(detail.get("title") or "").strip() \
            or (summary.title if summary else "") or "Qwen conversation"

        linear = self._linearize(messages_map, current_id)
        messages: list[Message] = []
        for m in linear:
            role = "user" if m.get("role") == "user" else "assistant"
            text = self._extract_text(m)
            if not text:
                continue
            messages.append(
                Message(
                    role=role,
                    content_md=text,
                    created_at=_ts(_first(m, "timestamp", "created_at", "create_time",
                                         "createdAt", "createTime", "msg_time")),
                    model=str(m.get("model") or ""),
                    citations=self._extract_citations(m),
                    external_id=str(m.get("id") or m.get("fid") or ""),
                )
            )

        return UnifiedConversation(
            provider=self.id,
            account=account or _DEFAULT_ACCOUNT,
            id=cid,
            title=title,
            created_at=_ts(_first(detail, "create_time", "created_at", "createdAt", "createTime")),
            updated_at=_ts(_first(detail, "update_time", "updated_at", "updatedAt",
                                  "modify_time", "last_modified")),
            folder=HOME_SPACE_NAME,
            messages=messages,
            raw={"detail": detail},
        )

    @staticmethod
    def _extract_text(m: dict) -> str:
        """Return the visible assistant/user text for one message."""
        content_list = m.get("content_list")
        if isinstance(content_list, list):
            parts: list[str] = []
            for item in content_list:
                if isinstance(item, str):
                    parts.append(item)
                elif isinstance(item, dict) and item.get("phase") == "answer":
                    parts.append(str(item.get("content") or ""))
            text = "".join(parts).strip()
            if text:
                return text
        c = m.get("content")
        if isinstance(c, str) and c.strip():
            return c.strip()
        # last resort: join every phase's content
        if isinstance(content_list, list):
            bits: list[str] = []
            for item in content_list:
                if isinstance(item, dict):
                    bits.append(str(item.get("content") or ""))
                elif isinstance(item, str):
                    bits.append(item)
            joined = "".join(bits).strip()
            if joined:
                return joined
        return ""

    @staticmethod
    def _extract_citations(m: dict) -> list[Citation]:
        out: list[Citation] = []
        content_list = m.get("content_list")
        if not isinstance(content_list, list):
            return out
        for item in content_list:
            if not isinstance(item, dict):
                continue
            if item.get("phase") not in ("web_search", "agent_web_search"):
                continue
            extra = item.get("extra") if isinstance(item.get("extra"), dict) else {}
            info = extra.get("web_search_info") or extra.get("webSearchInfo")
            if not isinstance(info, list):
                continue
            for w in info:
                if not isinstance(w, dict):
                    continue
                out.append(
                    Citation(
                        title=str(w.get("title") or ""),
                        url=str(w.get("url") or w.get("link") or ""),
                        snippet=str(w.get("snippet") or w.get("description")
                                    or w.get("summary") or ""),
                    )
                )
        return out

    @staticmethod
    def _linearize(messages_map: dict, current_id: str) -> list[dict]:
        """Flatten the message tree into root->leaf order (Qwen's `lc`)."""
        if not messages_map:
            return []
        msgs: list[dict] = []
        for key, raw in messages_map.items():
            if not isinstance(raw, dict):
                continue
            m = dict(raw)
            m["id"] = str(m.get("id") or m.get("fid") or key)
            parent = m.get("parentId") if m.get("parentId") is not None else m.get("parent_id")
            m["parentId"] = str(parent) if parent not in (None, "") else None
            msgs.append(m)
        by_id = {m["id"]: m for m in msgs}

        children: dict[str, list[str]] = {m["id"]: [] for m in msgs}
        for m in msgs:
            p = m.get("parentId")
            if p and p in by_id:
                children[p].append(m["id"])

        start = current_id if current_id in by_id else None
        if start is None:
            leaves = [m["id"] for m in msgs if not children[m["id"]]]
            if not leaves:
                # cyclic / malformed — fall back to server insertion order
                return msgs
            start = leaves[-1]  # last leaf in insertion order == most recent

        chain: list[dict] = []
        seen: set[str] = set()
        node = start
        while node and node in by_id and node not in seen:
            seen.add(node)
            chain.append(by_id[node])
            node = by_id[node].get("parentId")
        chain.reverse()
        return chain
