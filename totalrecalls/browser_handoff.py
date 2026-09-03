"""File-based handoff protocol for importing one browser conversation.

The protocol is intentionally local and passive: a browser companion downloads
one JSON file, and the user explicitly imports that file into a TotalRecalls
library.  No browser credentials, localhost listener, or network calls are
involved.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from totalrecalls.core.schema import UnifiedConversation
from totalrecalls.core.unified_export import write_unified_conversation

HANDOFF_PROTOCOL = "totalrecalls-browser-handoff"
HANDOFF_VERSION = 1


class HandoffError(ValueError):
    """Raised when a browser handoff is malformed or unsupported."""


def _as_object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise HandoffError(f"{label} must be a JSON object.")
    return value


def _derived_id(provider: str, conversation: dict[str, Any], source: dict[str, Any]) -> str:
    """Create a stable id when a provider's URL does not expose one."""
    material = {
        "provider": provider,
        "url": source.get("url") or "",
        "title": conversation.get("title") or "",
        "messages": conversation.get("messages") or [],
    }
    encoded = json.dumps(material, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return f"browser-{hashlib.sha256(encoded.encode('utf-8')).hexdigest()[:20]}"


def conversation_from_handoff(payload: dict[str, Any]) -> UnifiedConversation:
    """Validate and normalize a version-1 browser handoff payload."""
    payload = _as_object(payload, "Handoff")
    protocol = payload.get("protocol")
    if protocol != HANDOFF_PROTOCOL:
        raise HandoffError(f"Unsupported handoff protocol: {protocol or 'missing'!r}.")
    version = payload.get("version")
    if isinstance(version, bool) or not isinstance(version, int) or version != HANDOFF_VERSION:
        raise HandoffError(f"Unsupported handoff version: {version!r}.")
    schema_version = payload.get("schema_version", 1)
    if isinstance(schema_version, bool) or not isinstance(schema_version, int) or schema_version != 1:
        raise HandoffError(f"Unsupported conversation schema version: {schema_version!r}.")

    source = payload.get("source") or {}
    source = _as_object(source, "source")
    conversation = _as_object(payload.get("conversation"), "conversation")
    messages = conversation.get("messages")
    if not isinstance(messages, list) or not messages:
        raise HandoffError("conversation.messages must contain at least one message.")

    provider = str(payload.get("provider") or source.get("provider") or "").strip().lower()
    if not provider:
        raise HandoffError("A provider is required (for example, chatgpt or claude).")

    normalized_messages: list[dict[str, Any]] = []
    for index, message in enumerate(messages):
        message = _as_object(message, f"conversation.messages[{index}]")
        role = str(message.get("role") or "").strip().lower()
        if not role:
            raise HandoffError(f"conversation.messages[{index}].role is required.")
        content = message.get("content_md", message.get("content", ""))
        if not isinstance(content, str):
            raise HandoffError(f"conversation.messages[{index}].content must be text.")
        normalized = dict(message)
        normalized["role"] = role
        normalized["content_md"] = content
        normalized_messages.append(normalized)

    normalized_conversation = dict(conversation)
    normalized_conversation["messages"] = normalized_messages
    if not str(normalized_conversation.get("id") or "").strip():
        normalized_conversation["id"] = _derived_id(provider, normalized_conversation, source)

    normalized_payload = {
        "schema_version": schema_version,
        "provider": provider,
        "account": payload.get("account") if isinstance(payload.get("account"), dict) else {},
        "conversation": normalized_conversation,
        "raw": {
            "handoff": {
                "protocol": HANDOFF_PROTOCOL,
                "version": HANDOFF_VERSION,
                "source": source,
            }
        },
    }
    return UnifiedConversation.from_dict(normalized_payload)


def load_handoff(path: str | Path) -> UnifiedConversation:
    """Read and validate a JSON handoff file without making network calls."""
    path = Path(path)
    try:
        with path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
    except FileNotFoundError as exc:
        raise HandoffError(f"Handoff file not found: {path}") from exc
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise HandoffError(f"Could not read JSON handoff file {path}: {exc}") from exc
    return conversation_from_handoff(payload)


def import_handoff(handoff: str | Path | dict[str, Any], output_dir: str | Path) -> dict[str, Any]:
    """Import one handoff into the normal ``Library/<provider>/...`` layout."""
    conversation = (
        load_handoff(handoff)
        if isinstance(handoff, (str, Path))
        else conversation_from_handoff(handoff)
    )
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    return write_unified_conversation(str(output_dir), conversation)
