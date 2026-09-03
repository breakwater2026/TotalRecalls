"""Strict importers for AI Chat Exporter-compatible JSON and Markdown.

The browser extension has emitted a few closely related JSON shapes over
time.  This module accepts those shapes, plus the unified TotalRecalls shape,
without silently dropping malformed records.
"""

from __future__ import annotations

import json
import re
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from totalrecalls.core.schema import AccountInfo, Citation, Message, UnifiedConversation


class ImportValidationError(ValueError):
    """Raised when an input cannot be converted without losing data."""

    def __init__(self, message: str, *, source: str = "", path: str = "") -> None:
        self.source = source
        self.path = path
        detail = f"{source}: " if source else ""
        detail += f"{path}: " if path else ""
        super().__init__(detail + message)


_ROLE_NAMES = {
    "human": "user",
    "user": "user",
    "me": "user",
    "you": "user",
    "prompt": "user",
    "ai": "assistant",
    "assistant": "assistant",
    "bot": "assistant",
    "chatgpt": "assistant",
    "claude": "assistant",
    "gemini": "assistant",
    "perplexity": "assistant",
    "response": "assistant",
    "system": "system",
    "tool": "tool",
}
_ROLE_MARKER = re.compile(
    r"^\s*(?:(?:#{1,6}\s*)|(?:\*\*|__))?"
    r"(user|human|me|you|prompt|assistant|ai|bot|chatgpt|claude|gemini|perplexity|response|system|tool)"
    r"(?:\s*:)?\s*(?:(?:\*\*|__))?\s*:?\s*$",
    re.IGNORECASE,
)
_FRONTMATTER = re.compile(r"^\s*---\s*$")
_MARKDOWN_LINK = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")


def _fail(message: str, *, source: str, path: str) -> ImportValidationError:
    return ImportValidationError(message, source=source, path=path)


def _as_text(value: Any, *, source: str, path: str) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return str(value)
    raise _fail("expected text", source=source, path=path)


def _optional_text(value: Any, *, source: str, path: str) -> str:
    if value is None or value == "":
        return ""
    return _as_text(value, source=source, path=path)


def _timestamp(value: Any, *, source: str, path: str) -> str:
    if value is None or value == "":
        return ""
    if isinstance(value, bool):
        raise _fail("timestamp cannot be boolean", source=source, path=path)
    if isinstance(value, (int, float)):
        seconds = float(value)
        if seconds > 100_000_000_000:
            seconds /= 1000
        try:
            return datetime.fromtimestamp(seconds, tz=timezone.utc).isoformat()
        except (OverflowError, OSError, ValueError) as exc:
            raise _fail("invalid numeric timestamp", source=source, path=path) from exc
    return _as_text(value, source=source, path=path)


def _role(value: Any, *, source: str, path: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise _fail("message role is required", source=source, path=path)
    normalized = _ROLE_NAMES.get(value.strip().lower())
    if normalized is None:
        raise _fail(f"unsupported message role {value!r}", source=source, path=path)
    return normalized


def _content(value: Any, *, source: str, path: str) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return str(value)
    if isinstance(value, list):
        parts: list[str] = []
        for index, part in enumerate(value):
            if isinstance(part, str):
                parts.append(part)
            elif isinstance(part, dict):
                if "text" in part:
                    parts.append(_as_text(part["text"], source=source, path=f"{path}[{index}].text"))
                elif "value" in part:
                    parts.append(_as_text(part["value"], source=source, path=f"{path}[{index}].value"))
                else:
                    raise _fail("content part has no text or value", source=source, path=f"{path}[{index}]")
            else:
                raise _fail("content part must be text or an object", source=source, path=f"{path}[{index}]")
        return "\n".join(parts)
    if isinstance(value, dict):
        for key in ("text", "value", "answer", "content", "parts"):
            if key in value:
                return _content(value[key], source=source, path=f"{path}.{key}")
    raise _fail("message content is required and must be text-like", source=source, path=path)


def _citations(metadata: Any, *, source: str, path: str) -> list[Citation]:
    if metadata is None:
        return []
    if not isinstance(metadata, dict):
        raise _fail("message metadata must be an object", source=source, path=path)
    values = metadata.get("citations", metadata.get("sources", []))
    if values is None:
        return []
    if not isinstance(values, list):
        raise _fail("citations must be a list", source=source, path=f"{path}.citations")
    result: list[Citation] = []
    for index, value in enumerate(values):
        if not isinstance(value, dict):
            raise _fail("citation must be an object", source=source, path=f"{path}.citations[{index}]")
        result.append(Citation.from_dict(value))
    return result


def _message(record: Any, *, source: str, path: str) -> Message:
    if not isinstance(record, dict):
        raise _fail("message must be an object", source=source, path=path)
    author = record.get("author")
    if isinstance(author, dict):
        role_value = author.get("role") or record.get("role") or record.get("sender")
    else:
        role_value = record.get("role") or record.get("sender")
    role = _role(role_value, source=source, path=f"{path}.role")
    content_value = record.get("content")
    if content_value is None:
        content_value = record.get("content_md", record.get("text"))
    if content_value is None and isinstance(record.get("message"), dict):
        content_value = record["message"].get("content")
    content = _content(content_value, source=source, path=f"{path}.content")
    metadata = record.get("metadata")
    if metadata is None and isinstance(record.get("message"), dict):
        metadata = record["message"].get("metadata")
    external_id = record.get("id", record.get("uuid", record.get("external_id", "")))
    citations = _citations(metadata, source=source, path=f"{path}.metadata")
    if metadata is None and "citations" in record:
        citations = _citations(
            {"citations": record["citations"]},
            source=source,
            path=path,
        )
    return Message(
        role=role,
        content_md=content,
        created_at=_timestamp(
            record.get("created_at", record.get("create_time", record.get("timestamp"))),
            source=source,
            path=f"{path}.created_at",
        ),
        model=_optional_text(
            record.get("model", record.get("model_name", "")),
            source=source,
            path=f"{path}.model",
        ),
        citations=citations,
        external_id=_optional_text(external_id, source=source, path=f"{path}.id"),
    )


def _account(value: Any, *, source: str, path: str) -> AccountInfo:
    if value is None:
        return AccountInfo()
    if not isinstance(value, dict):
        raise _fail("account must be an object", source=source, path=path)
    return AccountInfo.from_dict(value)


def _conversation(record: Any, *, source: str, path: str, fallback_id: str = "") -> UnifiedConversation:
    if not isinstance(record, dict):
        raise _fail("conversation must be an object", source=source, path=path)
    nested = record.get("conversation")
    data = nested if isinstance(nested, dict) else record
    if nested is not None and not isinstance(nested, dict):
        raise _fail("conversation field must be an object", source=source, path=f"{path}.conversation")

    messages_value = data.get("messages")
    if messages_value is not None:
        if not isinstance(messages_value, list):
            raise _fail("messages must be a list", source=source, path=f"{path}.messages")
        messages = [_message(item, source=source, path=f"{path}.messages[{i}]") for i, item in enumerate(messages_value)]
    elif isinstance(data.get("mapping"), dict):
        messages = []
        for node_id, node in data["mapping"].items():
            node_path = f"{path}.mapping[{node_id!r}]"
            if not isinstance(node, dict):
                raise _fail("mapping node must be an object", source=source, path=node_path)
            message = node.get("message")
            if message is None:
                continue  # ChatGPT exports contain a root node without a message.
            messages.append(_message(message, source=source, path=f"{node_path}.message"))
        messages.sort(key=lambda item: (item.created_at == "", item.created_at))
    else:
        raise _fail("conversation has no messages or mapping", source=source, path=path)
    if not messages:
        raise _fail("conversation contains no messages", source=source, path=path)

    raw_id = data.get("id", data.get("uuid", data.get("conversation_id", fallback_id)))
    raw_title = data.get("title", data.get("name", "Imported conversation"))
    if raw_id is None:
        raw_id = fallback_id
    if raw_title is None:
        raw_title = "Imported conversation"
    provider_value = record.get("provider", "imported")
    if provider_value is None:
        provider_value = "imported"
    schema_value = record.get("schema_version") or 1
    if isinstance(schema_value, bool) or not isinstance(schema_value, int):
        raise _fail("schema_version must be an integer", source=source, path=f"{path}.schema_version")
    return UnifiedConversation(
        schema_version=schema_value,
        provider=_as_text(provider_value, source=source, path=f"{path}.provider"),
        account=_account(record.get("account"), source=source, path=f"{path}.account"),
        id=_as_text(raw_id, source=source, path=f"{path}.id") if raw_id != "" else fallback_id,
        title=_as_text(raw_title, source=source, path=f"{path}.title"),
        created_at=_timestamp(data.get("created_at", data.get("create_time")), source=source, path=f"{path}.created_at"),
        updated_at=_timestamp(data.get("updated_at", data.get("update_time")), source=source, path=f"{path}.updated_at"),
        folder=_as_text(data.get("folder", ""), source=source, path=f"{path}.folder")
        if data.get("folder", "") not in ("", None)
        else "",
        messages=messages,
        raw=record,
    )


def parse_ai_chat_export_json(payload: Any, *, provider: str = "imported", source_name: str = "") -> list[UnifiedConversation]:
    """Parse one or more AI Chat Exporter-compatible JSON conversations."""
    source = source_name or "<json>"
    if isinstance(payload, list):
        if not payload:
            raise _fail("JSON array is empty", source=source, path="$")
        if all(isinstance(item, dict) and ("role" in item or "author" in item) for item in payload):
            payload = {"messages": payload}
        else:
            records = payload
            return [
                _conversation(dict(item, provider=provider) if "provider" not in item else item,
                              source=source, path=f"$[{i}]", fallback_id=f"imported-{i + 1}")
                for i, item in enumerate(records)
            ]
    if not isinstance(payload, dict):
        raise _fail("top-level JSON must be an object or array", source=source, path="$")

    if isinstance(payload.get("conversations"), list):
        records = payload["conversations"]
        if not records:
            raise _fail("conversations array is empty", source=source, path="$.conversations")
        return [
            _conversation(dict(item, provider=provider) if isinstance(item, dict) and "provider" not in item else item,
                          source=source, path=f"$.conversations[{i}]", fallback_id=f"imported-{i + 1}")
            for i, item in enumerate(records)
        ]
    if isinstance(payload.get("data"), list):
        records = payload["data"]
        if not records:
            raise _fail("data array is empty", source=source, path="$.data")
        return [
            _conversation(dict(item, provider=provider) if isinstance(item, dict) and "provider" not in item else item,
                          source=source, path=f"$.data[{i}]", fallback_id=f"imported-{i + 1}")
            for i, item in enumerate(records)
        ]
    if "provider" not in payload:
        payload = dict(payload, provider=provider)
    return [_conversation(payload, source=source, path="$", fallback_id="imported-1")]


def parse_ai_chat_export_markdown(
    text: str,
    *,
    provider: str = "imported",
    source_name: str = "",
) -> UnifiedConversation:
    """Parse role-heading Markdown emitted by AI chat export tools."""
    source = source_name or "<markdown>"
    if not isinstance(text, str):
        raise _fail("Markdown input must be text", source=source, path="$")
    lines = text.splitlines()
    if not any(_ROLE_MARKER.match(line) for line in lines):
        raise _fail("Markdown contains no recognized message role headings", source=source, path="$")
    first_marker = next(i for i, line in enumerate(lines) if _ROLE_MARKER.match(line))

    title = ""
    frontmatter: dict[str, str] = {}
    in_frontmatter = bool(lines and _FRONTMATTER.match(lines[0]))
    cursor = 1 if in_frontmatter else 0
    if in_frontmatter:
        while cursor < len(lines) and not _FRONTMATTER.match(lines[cursor]):
            line = lines[cursor]
            if ":" in line:
                key, value = line.split(":", 1)
                frontmatter[key.strip().lower()] = value.strip().strip("\"'")
            cursor += 1
        if cursor >= len(lines):
            raise _fail("unterminated Markdown frontmatter", source=source, path="$")
        cursor += 1
    for line in lines[cursor:]:
        if line.startswith("# ") and line[2:].strip():
            title = line[2:].strip()
            break
    title = title or frontmatter.get("title", "") or "Imported conversation"
    for line_no, line in enumerate(lines[cursor:first_marker], cursor + 1):
        stripped = line.strip()
        if not stripped or (stripped.startswith("# ") and stripped[2:].strip()):
            continue
        if re.match(r"^[-*]\s+\*\*[^*]+\*\*\s*:", stripped):
            continue
        raise _fail(
            "unrecognized Markdown content before the first message",
            source=source,
            path=f"line {line_no}",
        )

    messages: list[Message] = []
    current_role: str | None = None
    body: list[str] = []
    for line_no, line in enumerate(lines, 1):
        marker = _ROLE_MARKER.match(line)
        if marker:
            if current_role is not None:
                messages.append(Message(role=current_role, content_md="\n".join(body).strip()))
            current_role = _role(marker.group(1), source=source, path=f"line {line_no}")
            body = []
            continue
        if current_role is not None:
            body.append(line)
    if current_role is not None:
        messages.append(Message(role=current_role, content_md="\n".join(body).strip()))
    if not messages:
        raise _fail("Markdown contains no messages", source=source, path="$")
    for index, message in enumerate(messages):
        if message.role == "assistant":
            cites = [
                Citation(title=label, url=url)
                for label, url in _MARKDOWN_LINK.findall(message.content_md)
            ]
            messages[index] = replace(message, citations=cites)
    return UnifiedConversation(
        provider=provider,
        id="",
        title=title,
        created_at=frontmatter.get("created_at", frontmatter.get("created", "")),
        updated_at=frontmatter.get("updated_at", ""),
        messages=messages,
        raw={"source_format": "markdown", "source_name": source_name},
    )


def load_ai_chat_export(
    source: str | Path | bytes | bytearray | dict[str, Any] | list[Any],
    *,
    provider: str = "imported",
) -> list[UnifiedConversation]:
    """Load a JSON/Markdown path or in-memory payload with strict validation."""
    if isinstance(source, (dict, list)):
        return parse_ai_chat_export_json(source, provider=provider)
    if isinstance(source, (bytes, bytearray)):
        try:
            text = bytes(source).decode("utf-8-sig")
        except UnicodeDecodeError as exc:
            raise ImportValidationError("input is not valid UTF-8", source="<bytes>") from exc
        source_name = "<bytes>"
    elif isinstance(source, str) and source.lstrip().startswith(("{", "[", "#", "---", "**")) and (
        "\n" in source or source.lstrip().startswith(("{", "["))
    ):
        text = source
        source_name = "<string>"
    else:
        path = Path(source)
        try:
            text = path.read_text(encoding="utf-8-sig")
        except OSError as exc:
            raise ImportValidationError(f"cannot read input: {exc}", source=str(path)) from exc
        source_name = str(path)
    suffix = Path(source_name).suffix.lower()
    if suffix == ".json" or (not suffix and text.lstrip().startswith(("{", "["))):
        try:
            payload = json.loads(text)
        except json.JSONDecodeError as exc:
            raise ImportValidationError(f"invalid JSON: {exc.msg}", source=source_name, path=f"line {exc.lineno}") from exc
        return parse_ai_chat_export_json(payload, provider=provider, source_name=source_name)
    if suffix in {".md", ".markdown"} or text.lstrip().startswith(("#", "---", "**")):
        return [parse_ai_chat_export_markdown(text, provider=provider, source_name=source_name)]
    raise ImportValidationError("cannot determine JSON vs Markdown format", source=source_name)


# Descriptive aliases keep callers independent of the on-disk file format.
import_ai_chat_json = parse_ai_chat_export_json
import_ai_chat_markdown = parse_ai_chat_export_markdown
import_ai_chat_export = load_ai_chat_export
