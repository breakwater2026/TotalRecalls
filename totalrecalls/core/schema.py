"""Unified conversation schema shared by all provider adapters.

schema_version 1 — TotalRecalls multi-provider archive format.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

SCHEMA_VERSION = 1


@dataclass
class Citation:
    title: str = ""
    url: str = ""
    snippet: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"title": self.title, "url": self.url, "snippet": self.snippet}

    @classmethod
    def from_dict(cls, d: dict | None) -> "Citation":
        d = d or {}
        return cls(
            title=str(d.get("title") or ""),
            url=str(d.get("url") or ""),
            snippet=str(d.get("snippet") or ""),
        )


@dataclass
class Message:
    role: str  # user | assistant | system | tool
    content_md: str = ""
    created_at: str = ""
    model: str = ""
    citations: list[Citation] = field(default_factory=list)
    external_id: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "role": self.role,
            "content_md": self.content_md,
            "created_at": self.created_at,
            "model": self.model,
            "citations": [c.to_dict() for c in self.citations],
            "external_id": self.external_id,
        }

    @classmethod
    def from_dict(cls, d: dict | None) -> "Message":
        d = d or {}
        cites = [Citation.from_dict(c) for c in (d.get("citations") or []) if isinstance(c, dict)]
        return cls(
            role=str(d.get("role") or "assistant"),
            content_md=str(d.get("content_md") or d.get("content") or ""),
            created_at=str(d.get("created_at") or ""),
            model=str(d.get("model") or ""),
            citations=cites,
            external_id=str(d.get("external_id") or ""),
        )


@dataclass
class AccountInfo:
    email: str = ""
    external_id: str = ""
    display_name: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "email": self.email,
            "external_id": self.external_id,
            "display_name": self.display_name,
        }

    @classmethod
    def from_dict(cls, d: dict | None) -> "AccountInfo":
        d = d or {}
        return cls(
            email=str(d.get("email") or ""),
            external_id=str(d.get("external_id") or d.get("id") or ""),
            display_name=str(d.get("display_name") or d.get("name") or ""),
        )


@dataclass
class ConversationSummary:
    """Lightweight index row from list_conversations()."""

    id: str
    title: str = ""
    updated_at: str = ""
    created_at: str = ""
    folder: str = ""  # Space / Project / Notebook name
    raw: dict = field(default_factory=dict)


@dataclass
class UnifiedConversation:
    """Provider-agnostic full conversation."""

    schema_version: int = SCHEMA_VERSION
    provider: str = ""
    account: AccountInfo = field(default_factory=AccountInfo)
    id: str = ""
    title: str = ""
    created_at: str = ""
    updated_at: str = ""
    folder: str = ""
    messages: list[Message] = field(default_factory=list)
    raw: dict = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version or SCHEMA_VERSION,
            "provider": self.provider,
            "account": self.account.to_dict() if isinstance(self.account, AccountInfo) else AccountInfo.from_dict(self.account).to_dict(),
            "conversation": {
                "id": self.id,
                "title": self.title,
                "created_at": self.created_at,
                "updated_at": self.updated_at,
                "folder": self.folder,
                "messages": [m.to_dict() for m in self.messages],
            },
            "raw": self.raw if isinstance(self.raw, dict) else {},
        }

    @classmethod
    def from_dict(cls, d: dict | None) -> "UnifiedConversation":
        d = d or {}
        conv = d.get("conversation") if isinstance(d.get("conversation"), dict) else d
        conv = conv or {}
        msgs = [
            Message.from_dict(m)
            for m in (conv.get("messages") or [])
            if isinstance(m, dict)
        ]
        return cls(
            schema_version=int(d.get("schema_version") or SCHEMA_VERSION),
            provider=str(d.get("provider") or ""),
            account=AccountInfo.from_dict(d.get("account") if isinstance(d.get("account"), dict) else {}),
            id=str(conv.get("id") or ""),
            title=str(conv.get("title") or ""),
            created_at=str(conv.get("created_at") or ""),
            updated_at=str(conv.get("updated_at") or ""),
            folder=str(conv.get("folder") or ""),
            messages=msgs,
            raw=d.get("raw") if isinstance(d.get("raw"), dict) else {},
        )
