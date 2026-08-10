"""Perplexity ProviderAdapter — wraps the v1 engine modules."""

from __future__ import annotations

from totalrecalls.core.export_fs import HOME_SPACE_NAME, space_label_from_collection
from totalrecalls.core.schema import (
    AccountInfo,
    Citation,
    ConversationSummary,
    Message,
    UnifiedConversation,
)
from totalrecalls.adapters.perplexity.auth import validate_session
from totalrecalls.adapters.perplexity.discover import list_threads, _thread_key
from totalrecalls.adapters.perplexity.http import ApiError
from totalrecalls.adapters.perplexity.thread import extract_entry, get_thread


class PerplexityAdapter:
    id = "perplexity"
    display_name = "Perplexity"

    def validate(self, credential: str) -> AccountInfo:
        session = validate_session(credential)
        user = session.get("user") if isinstance(session, dict) else {}
        user = user or {}
        email = str(user.get("email") or "")
        if not email:
            # Match prior behavior: empty session / no email → auth failure
            raise ApiError("auth-failed")
        return AccountInfo(
            email=email,
            external_id=str(user.get("id") or user.get("user_id") or ""),
            display_name=str(user.get("name") or user.get("username") or ""),
        )

    def list_conversations(
        self, credential: str, *, deep: bool = False
    ) -> list[ConversationSummary]:
        threads = list_threads(credential, deep=deep)
        out: list[ConversationSummary] = []
        for t in threads:
            if not isinstance(t, dict):
                continue
            key = _thread_key(t) or str(t.get("uuid") or "")
            if not key:
                continue
            col = t.get("collection") if isinstance(t.get("collection"), dict) else {}
            folder = space_label_from_collection(col)
            title = (
                t.get("title")
                or t.get("slug")
                or t.get("query")
                or t.get("query_str")
                or "Untitled conversation"
            )
            out.append(
                ConversationSummary(
                    id=key,
                    title=str(title).strip(),
                    updated_at=str(
                        t.get("last_query_datetime")
                        or t.get("updated_at")
                        or t.get("created_at")
                        or ""
                    ),
                    created_at=str(t.get("created_at") or ""),
                    folder=folder,
                    raw=t,
                )
            )
        return out

    def fetch_conversation(self, credential: str, conv_id: str) -> UnifiedConversation:
        detail = get_thread(credential, conv_id)
        summary = ConversationSummary(id=conv_id, title="", folder=HOME_SPACE_NAME)
        return self.to_unified(detail, summary=summary)

    def to_unified(
        self,
        detail: dict,
        *,
        summary: ConversationSummary | None = None,
        account: AccountInfo | None = None,
    ) -> UnifiedConversation:
        """Map Perplexity thread detail (+ optional list summary) → unified schema."""
        detail = detail if isinstance(detail, dict) else {}
        meta = detail.get("thread_metadata") if isinstance(detail.get("thread_metadata"), dict) else {}
        meta = meta or {}
        summary = summary or ConversationSummary(id=str(meta.get("uuid") or ""), title="")
        col = {}
        if isinstance(summary.raw, dict):
            col = summary.raw.get("collection") if isinstance(summary.raw.get("collection"), dict) else {}
        if not col and isinstance(detail.get("collection"), dict):
            col = detail["collection"]

        title = (
            meta.get("title")
            or summary.title
            or "Untitled conversation"
        )
        folder = summary.folder or space_label_from_collection(col, meta)
        conv_id = str(meta.get("uuid") or summary.id or "")

        messages: list[Message] = []
        for raw_entry in detail.get("entries") or []:
            if not isinstance(raw_entry, dict):
                continue
            # Prefer already-normalized entries; else extract from API shape
            if "answer" in raw_entry or "query" in raw_entry:
                entry = raw_entry
            else:
                entry = extract_entry(raw_entry)
            q = str(entry.get("query") or "")
            a = str(entry.get("answer") or "")
            created = str(entry.get("created_at") or "")
            model = str(entry.get("model") or "")
            eid = str(entry.get("uuid") or "")
            if q:
                messages.append(
                    Message(
                        role="user",
                        content_md=q,
                        created_at=created,
                        external_id=f"{eid}:q" if eid else "",
                    )
                )
            cites = []
            for s in entry.get("sources") or []:
                if not isinstance(s, dict):
                    continue
                cites.append(
                    Citation(
                        title=str(s.get("title") or s.get("name") or ""),
                        url=str(s.get("url") or ""),
                        snippet=str(s.get("snippet") or ""),
                    )
                )
            messages.append(
                Message(
                    role="assistant",
                    content_md=a,
                    created_at=str(entry.get("updated_at") or created),
                    model=model,
                    citations=cites,
                    external_id=eid,
                )
            )

        return UnifiedConversation(
            provider=self.id,
            account=account or AccountInfo(),
            id=conv_id,
            title=str(title).strip(),
            created_at=str(meta.get("created_at") or summary.created_at or ""),
            updated_at=str(
                meta.get("updated_at")
                or summary.updated_at
                or meta.get("last_query_datetime")
                or ""
            ),
            folder=folder or HOME_SPACE_NAME,
            messages=messages,
            raw={"thread_metadata": meta, "collection": col, "detail": detail},
        )
