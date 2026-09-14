"""Provider-agnostic export of UnifiedConversation trees.

Layout:
  <outdir>/
    Library/<provider>/<Home|Spaces/...>/<YYYY-MM-DD HH-MM> -- <Title> -- <shortid>/
      conversation.md
      conversation.json   # unified schema
    README.md
    manifest.json
    uuid_index.json       # provider:id → rel_path
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from dataclasses import replace
from pathlib import Path
from typing import Callable

from totalrecalls import APP_VERSION
from totalrecalls.adapters.base import ProviderAdapter
from totalrecalls.core.export_fs import (
    HOME_SPACE_NAME,
    SPACES_DIRNAME,
    safe_name,
    short_id,
)
from totalrecalls.core.paths import log
from totalrecalls.core.schema import UnifiedConversation


def _parse_iso(ts: str) -> datetime | None:
    """Best-effort ISO-8601 parser. Accepts 'Z' suffix and '+00:00'.

    Returns None on empty/garbage input so callers can fall back gracefully.
    """
    if not ts:
        return None
    s = ts.strip()
    if not s:
        return None
    # Normalize trailing Z to +00:00 for fromisoformat
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    try:
        return datetime.fromisoformat(s)
    except (ValueError, TypeError):
        return None


def conversation_occurred(conv: UnifiedConversation) -> datetime | None:
    """When the conversation took place — prefer created_at, fall back to updated_at."""
    dt = _parse_iso(getattr(conv, "created_at", "") or "")
    if dt is not None:
        return dt
    return _parse_iso(getattr(conv, "updated_at", "") or "")


def conversation_occurred_slug(conv: UnifiedConversation) -> str:
    """Filesystem-safe prefix for the leaf folder: 'YYYY-MM-DD HH-MM' (or 'undated').

    Uses hyphen instead of colon so the string is a valid Windows path segment
    even on systems where `:` is forbidden in filenames.
    """
    dt = conversation_occurred(conv)
    if dt is None:
        return "undated"
    return dt.strftime("%Y-%m-%d %H-%M")


def conversation_occurred_display(conv: UnifiedConversation) -> str:
    """Human-readable timestamp for the website and markdown frontmatter: 'YYYY-MM-DD HH:MM'."""
    dt = conversation_occurred(conv)
    if dt is None:
        return "—"
    return dt.strftime("%Y-%m-%d %H:%M")


def conversation_rel_path(conv: UnifiedConversation) -> str:
    """Relative path (posix) from export root to conversation folder.

    The leaf folder name is prefixed with the conversation's occurred timestamp
    so a parent-directory listing in Explorer (or any file browser) shows the
    date/time next to the title. Falls back to 'undated' if no timestamp.
    """
    provider = safe_name(conv.provider or "unknown", max_len=40) or "unknown"
    folder = (conv.folder or HOME_SPACE_NAME).strip() or HOME_SPACE_NAME
    title = conv.title or "Untitled conversation"
    leaf = f"{conversation_occurred_slug(conv)} -- {safe_name(title, max_len=72)} -- {short_id(conv.id)}"
    if folder == HOME_SPACE_NAME:
        mid = HOME_SPACE_NAME
    else:
        mid = f"{SPACES_DIRNAME}/{safe_name(folder, max_len=60) or 'Space'}"
    return f"Library/{provider}/{mid}/{leaf}"


def render_unified_markdown(conv: UnifiedConversation) -> str:
    lines = [
        f"# {conv.title or 'Untitled conversation'}",
        "",
        f"- **Provider:** {conv.provider or '—'}",
        f"- **Account:** {(conv.account.email if conv.account else '') or '—'}",
        f"- **Folder:** {conv.folder or HOME_SPACE_NAME}",
        f"- **ID:** {conv.id or '—'}",
        f"- **Occurred:** {conversation_occurred_display(conv)}",
        f"- **Created:** {conv.created_at or '—'}",
        f"- **Updated:** {conv.updated_at or '—'}",
        "",
    ]
    turn = 0
    for msg in conv.messages:
        role = (msg.role or "").lower()
        body = msg.content_md or ""
        if role == "user":
            turn += 1
            first = body.splitlines()[0][:120] if body else "(no question text)"
            lines.append("---")
            lines.append("")
            lines.append(f"## Q{turn}: {first}")
            lines.append("")
            # Always include full user text so single-line questions appear in body too
            lines.append(body or "_(no question text)_")
            lines.append("")
        elif role == "assistant":
            if msg.model:
                lines.append(f"*Model: {msg.model}*")
                lines.append("")
            lines.append(body or "_(no answer text captured)_")
            lines.append("")
            if msg.citations:
                lines.append("### Sources")
                for c in msg.citations:
                    title = c.title or c.url or "source"
                    if c.url:
                        lines.append(f"- [{title}]({c.url})")
                    else:
                        lines.append(f"- {title}")
                lines.append("")
        else:
            lines.append(f"### {role or 'message'}")
            lines.append("")
            lines.append(body)
            lines.append("")
    return "\n".join(lines)


def conversation_turn_ranges(conv: UnifiedConversation) -> list[dict]:
    """Return 1-based turn groups, preserving every message in each turn.

    A turn starts at a user message and includes following assistant/tool/system
    messages until the next user message. Leading non-user messages are kept in
    the first group, and conversations without user messages are one group.
    """
    if not conv.messages:
        return []
    groups: list[list[int]] = []
    current: list[int] = []
    for index, message in enumerate(conv.messages):
        if current and (message.role or "").lower() == "user":
            groups.append(current)
            current = []
        current.append(index)
    if current:
        groups.append(current)
    return [
        {
            "turn": number,
            "indexes": indexes,
            "preview": next(
                (
                    (conv.messages[i].content_md or "").splitlines()[0][:120]
                    for i in indexes
                    if (conv.messages[i].role or "").lower() == "user"
                    and (conv.messages[i].content_md or "").strip()
                ),
                "(no question text)",
            ),
        }
        for number, indexes in enumerate(groups, 1)
    ]


def select_unified_messages(
    conv: UnifiedConversation,
    message_indexes: list[int],
) -> tuple[UnifiedConversation, list[int]]:
    """Validate and return a conversation containing the requested messages."""
    if not isinstance(message_indexes, list) or not message_indexes:
        raise ValueError("Select at least one message to export.")
    indexes: list[int] = []
    for value in message_indexes:
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError("Message selections must be numeric indexes.")
        if value < 0 or value >= len(conv.messages):
            raise ValueError("A selected message is no longer available.")
        if value not in indexes:
            indexes.append(value)
    indexes.sort()
    return replace(conv, messages=[conv.messages[i] for i in indexes]), indexes


def write_selected_unified_conversation(
    outdir: str,
    conv: UnifiedConversation,
    message_indexes: list[int],
    *,
    source: str = "",
) -> dict:
    """Write a validated message selection as Markdown and unified JSON."""
    selected, indexes = select_unified_messages(conv, message_indexes)
    stamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    title = safe_name(selected.title or "Untitled conversation", max_len=72) or "Untitled conversation"
    leaf = f"{stamp} -- {title} -- {short_id(selected.id) or 'selection'}"
    folder = os.path.join(outdir, "Selected exports", leaf)
    suffix = 2
    while os.path.exists(folder):
        folder = os.path.join(outdir, "Selected exports", f"{leaf} ({suffix})")
        suffix += 1
    os.makedirs(folder, exist_ok=True)
    markdown_path = os.path.join(folder, "conversation.md")
    json_path = os.path.join(folder, "conversation.json")
    with open(markdown_path, "w", encoding="utf-8") as f:
        f.write(render_unified_markdown(selected))
    payload = selected.to_dict()
    payload["selection"] = {
        "source": source,
        "message_indexes": indexes,
        "message_count": len(indexes),
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    return {
        "folder": folder,
        "markdown_path": markdown_path,
        "json_path": json_path,
        "message_indexes": indexes,
        "message_count": len(indexes),
    }


def _message_stats(conv: UnifiedConversation) -> dict:
    answer_chars = 0
    empty_answers = 0
    sources = 0
    assistants = 0
    for m in conv.messages:
        if (m.role or "").lower() != "assistant":
            continue
        assistants += 1
        a = m.content_md or ""
        answer_chars += len(a)
        if not a.strip():
            empty_answers += 1
        sources += len(m.citations or [])
    return {
        "entries": assistants,
        "answer_chars": answer_chars,
        "empty_answer_entries": empty_answers,
        "sources": sources,
        "all_answers_empty": bool(assistants) and empty_answers == assistants,
        "messages": len(conv.messages),
    }


def write_unified_conversation(outdir: str, conv: UnifiedConversation) -> dict:
    """Write one conversation folder. Returns index record dict.

    The folder's filesystem mtime is set to the conversation's occurred time
    (created_at, falling back to updated_at) so Explorer's "Date modified"
    column reflects when the conversation took place, not when it was exported.
    """
    rel = conversation_rel_path(conv).replace("\\", "/")
    folder = os.path.join(outdir, *rel.split("/"))
    os.makedirs(folder, exist_ok=True)

    md = render_unified_markdown(conv)
    with open(os.path.join(folder, "conversation.md"), "w", encoding="utf-8") as f:
        f.write(md)
    # compatibility alias used by older Perplexity layout readers
    with open(os.path.join(folder, "thread.md"), "w", encoding="utf-8") as f:
        f.write(md)

    payload = conv.to_dict()
    with open(os.path.join(folder, "conversation.json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    # Best-effort: set the folder mtime so Explorer's "Date modified" column
    # surfaces the conversation's true occurred time, not the export time.
    # Naive datetimes are assumed to be in the local timezone of the export.
    occurred_dt = conversation_occurred(conv)
    if occurred_dt is not None:
        try:
            from datetime import datetime as _dt
            ts = occurred_dt
            if ts.tzinfo is not None:
                # Convert to a naive UTC timestamp for os.utime
                ts = ts.astimezone(timezone.utc).replace(tzinfo=None)
            mtime = ts.timestamp()
            os.utime(folder, (mtime, mtime))
        except OSError:
            # Read-only or unsupported FS — don't fail the export over a cosmetic detail
            pass

    stats = _message_stats(conv)
    return {
        "uuid": conv.id,
        "id": conv.id,
        "provider": conv.provider,
        "title": conv.title,
        "space": conv.folder or HOME_SPACE_NAME,
        "folder": conv.folder or HOME_SPACE_NAME,
        "rel_path": rel,
        "occurred_at": conversation_occurred_display(conv),
        "updated_at": conv.updated_at,
        "stats": stats,
        "empty_answers": stats.get("all_answers_empty", False),
    }


def _write_manifest(outdir: str, account: str, provider: str, records: list[dict],
                    exported_at: str) -> dict:
    by_space: dict[str, list] = {}
    for rec in records:
        sp = rec.get("space") or HOME_SPACE_NAME
        by_space.setdefault(sp, []).append(rec)

    lines = [
        f"# TotalRecalls export — {provider}",
        "",
        f"- **Account:** {account or '—'}",
        f"- **Provider:** {provider}",
        f"- **Exported:** {exported_at}",
        f"- **Conversations:** {len(records)}",
        "",
        "Conversations live under `Library/<provider>/home` as `conversation.md` + `conversation.json`.",
        "",
        "## Conversations",
        "",
        "| Folder | Title | Turns | Notes |",
        "|---|---|---:|---|",
    ]
    for rec in sorted(records, key=lambda r: ((r.get("space") or ""), (r.get("title") or "").lower())):
        title = (rec.get("title") or "Untitled").replace("|", "/")
        rel = (rec.get("rel_path") or "").replace("\\", "/")
        link = f"[{title}]({rel}/conversation.md)" if rel else title
        st = rec.get("stats") or {}
        note = "⚠️ empty answers" if rec.get("empty_answers") else ""
        lines.append(
            f"| {rec.get('space') or HOME_SPACE_NAME} | {link} | {st.get('entries', '—')} | {note} |"
        )
    lines.append("")
    readme = "\n".join(lines)
    with open(os.path.join(outdir, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme)

    empty_list = [r.get("title") or r.get("id") or "?" for r in records if r.get("empty_answers")]
    uuid_index = {}
    for r in records:
        key = r.get("id") or r.get("uuid")
        if key and r.get("rel_path"):
            uuid_index[f"{provider}:{key}"] = r["rel_path"].replace("\\", "/")
            uuid_index[str(key)] = r["rel_path"].replace("\\", "/")

    manifest = {
        "tool": "TotalRecalls",
        "layout": "library-v1",
        "version": APP_VERSION,
        "schema_version": 1,
        "provider": provider,
        "exported_at": exported_at,
        "account": account or "",
        "total_threads": len(records),
        "formats": ["json", "markdown"],
        "warnings": {"empty_answer_threads": empty_list},
        "threads": [
            {
                "id": r.get("id") or r.get("uuid"),
                "provider": provider,
                "title": r.get("title"),
                "folder": r.get("space"),
                "path": (r.get("rel_path") or "").replace("\\", "/"),
                "updated_at": r.get("updated_at") or "",
                "entries": (r.get("stats") or {}).get("entries"),
                "answer_chars": (r.get("stats") or {}).get("answer_chars"),
                "empty_answers": bool(r.get("empty_answers")),
            }
            for r in records
        ],
    }
    with open(os.path.join(outdir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    with open(os.path.join(outdir, "uuid_index.json"), "w", encoding="utf-8") as f:
        json.dump(uuid_index, f, indent=2, ensure_ascii=False)
    return manifest


def export_via_adapter(
    adapter: ProviderAdapter,
    credential: str,
    outdir: str,
    *,
    deep: bool = True,
    refresh: bool = False,
    on_progress: Callable[[dict], None] | None = None,
    on_log: Callable[[str], None] | None = None,
    on_first_download: Callable[[], None] | None = None,
    max_conversations: int | None = None,
    latest_only: bool = False,
    stop_event=None,
) -> dict:
    """Run a full export through a ProviderAdapter into Library/<provider>/.

    ``stop_event``: optional threading.Event for caller-side cancellation
    (the desktop bridge sets it on disconnect). Forwarded to adapters that
    accept it so an export aborts its in-flight retry chain promptly instead
    of orphaning network activity after the user has disconnected.
    """

    def _log(msg: str):
        log(msg)
        if on_log:
            on_log(msg)

    def _prog(payload: dict):
        if on_progress:
            on_progress(payload)

    os.makedirs(outdir, exist_ok=True)
    from totalrecalls.adapters.base import call_with_stop
    account = call_with_stop(adapter.validate, credential, stop_event=stop_event)
    _log(f"Connected as {account.email or account.external_id or 'account'} via {adapter.id}")
    summaries = call_with_stop(adapter.list_conversations, credential, deep=deep,
                               stop_event=stop_event)
    if latest_only:
        summaries.sort(
            key=lambda s: (s.updated_at or s.created_at or ""),
            reverse=True,
        )
        max_conversations = 1
        _log("Quick export: selecting the latest conversation.")
    total = len(summaries)
    _log(f"Found {total} conversation(s) on {adapter.display_name}")
    if max_conversations is not None and total > max_conversations:
        _log(f"Free tier: downloading the first {max_conversations} of {total} conversations. "
             f"Upgrade to Pro for unlimited downloads.")
        summaries = summaries[:max_conversations]
        total = max_conversations

    # load prior index for skip
    index_path = os.path.join(outdir, "uuid_index.json")
    prior = {}
    try:
        with open(index_path, encoding="utf-8") as f:
            prior = json.load(f) or {}
    except Exception:
        prior = {}

    records: list[dict] = []
    done = 0
    skipped = 0
    failed = 0
    first_download_noted = False

    for pos, summary in enumerate(summaries, 1):
        title_disp = (summary.title or summary.id)[:70]
        folder_label = summary.folder or HOME_SPACE_NAME
        # skip if present
        prior_rel = prior.get(f"{adapter.id}:{summary.id}") or prior.get(summary.id)
        if prior_rel and not refresh:
            abs_existing = os.path.join(outdir, prior_rel.replace("/", os.sep))
            if os.path.isdir(abs_existing) and (
                os.path.isfile(os.path.join(abs_existing, "conversation.json"))
                or os.path.isfile(os.path.join(abs_existing, "thread.json"))
            ):
                rec = {
                    "uuid": summary.id,
                    "id": summary.id,
                    "provider": adapter.id,
                    "title": summary.title,
                    "space": folder_label,
                    "rel_path": prior_rel.replace("\\", "/"),
                    "updated_at": summary.updated_at,
                    "stats": {},
                    "empty_answers": False,
                }
                records.append(rec)
                done += 1
                skipped += 1
                _log(f"[{pos}/{total}] {folder_label} / {title_disp} — already saved")
                _prog({"done": done, "total": total, "title": f"{folder_label}: {title_disp}"})
                continue

        _log(f"[{pos}/{total}] {folder_label} / {title_disp} — downloading…")
        _prog({"done": done, "total": total, "title": f"{folder_label}: {title_disp}"})
        if on_first_download and not first_download_noted:
            first_download_noted = True
            on_first_download()
        try:
            conv = call_with_stop(adapter.fetch_conversation, credential, summary.id,
                                  stop_event=stop_event)
            # ensure folder/title from summary when detail is sparse or generic.
            # Gemini/Grok fetch paths fall back to "<Provider> conversation" as the
            # title even when the listing knew the real name — the summary title is
            # always the authoritative one, so replace generic fallbacks outright.
            if not conv.folder:
                conv.folder = summary.folder
            generic_title = conv.title.strip().lower() in (
                "", f"{adapter.display_name.lower()} conversation",
                f"{adapter.id} conversation", "untitled conversation",
            )
            if not conv.title or generic_title:
                conv.title = summary.title
            if not conv.account.email and account.email:
                conv.account = account
            # Some providers (Grok) return conversation timestamps only in the
            # list response, not the detail fetch — fall back to the summary's
            # timestamps so the export is never "undated".
            if not conv.created_at and summary.created_at:
                conv.created_at = summary.created_at
            if not conv.updated_at and summary.updated_at:
                conv.updated_at = summary.updated_at
            rec = write_unified_conversation(outdir, conv)
            records.append(rec)
            done += 1
            st = rec.get("stats") or {}
            flag = " ⚠️ empty answers" if rec.get("empty_answers") else ""
            _log(f"  ✓ {st.get('entries', 0)} turns, {st.get('answer_chars', 0)} chars{flag}")
        except Exception as e:
            failed += 1
            _log(f"  ! failed: {e}")
            log(f"export_via_adapter fail {summary.id}: {e}")

    exported_at = datetime.now(timezone.utc).isoformat()
    manifest = _write_manifest(outdir, account.email, adapter.id, records, exported_at)
    _log(f"Wrote Library/{adapter.id}/ — {len(records)} conversation(s). Skipped {skipped}, failed {failed}.")
    return {
        "exported": len(records) - skipped,
        "skipped": skipped,
        "failed": failed,
        "total": total,
        "records": records,
        "manifest": manifest,
        "folder": outdir,
        "account": account.email,
    }
