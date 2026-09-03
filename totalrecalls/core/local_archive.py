"""Local archive indexing, search, and resumable backup planning.

The archive layout is the one produced by :mod:`totalrecalls.core.unified_export`:
conversation folders contain ``conversation.json`` and/or Markdown.  This module
keeps the read/search and backup concerns independent of the desktop UI.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Iterable

from totalrecalls.core.schema import UnifiedConversation

BACKUP_STATE_VERSION = 1
DEFAULT_STATE_NAME = ".totalrecalls-backup-state.json"
_CHUNK_SIZE = 1024 * 1024


@dataclass(frozen=True)
class ArchiveRecord:
    """One searchable conversation, represented by its on-disk files."""

    path: Path
    relative_path: str
    title: str
    provider: str
    content: str
    json_path: Path | None = None
    markdown_path: Path | None = None

    def matches(self, query: str, provider: str | None = None) -> bool:
        needle = (query or "").casefold().strip()
        if provider and (provider.casefold() not in self.provider.casefold()):
            return False
        if not needle:
            return True
        return needle in self.title.casefold() or (
            needle in self.provider.casefold()
        ) or (needle in self.content.casefold())


@dataclass
class ArchiveIndex:
    """An in-memory index that can be searched repeatedly without rereading files."""

    root: Path
    records: list[ArchiveRecord] = field(default_factory=list)

    def search(self, query: str = "", *, provider: str | None = None) -> list[ArchiveRecord]:
        return [
            record
            for record in self.records
            if record.matches(query, provider)
        ]


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _json_metadata(path: Path) -> tuple[str, str, str]:
    try:
        payload = json.loads(_read_text(path))
    except (json.JSONDecodeError, TypeError, ValueError):
        return "", "", ""
    if not isinstance(payload, dict):
        return "", "", ""
    try:
        conversation = UnifiedConversation.from_dict(payload)
        title = conversation.title
        provider = conversation.provider
        content = "\n\n".join(
            message.content_md
            for message in conversation.messages
            if message.content_md
        )
        return title, provider, content
    except (TypeError, ValueError, KeyError):
        return (
            str(payload.get("title") or ""),
            str(payload.get("provider") or ""),
            str(payload.get("content") or ""),
        )


def _markdown_metadata(text: str) -> tuple[str, str]:
    title = ""
    provider = ""
    for line in text.splitlines():
        if not title:
            heading = re.match(r"^\s*#\s+(.+?)\s*$", line)
            if heading:
                title = heading.group(1).strip()
        if not provider:
            provider_match = re.match(
                r"^\s*(?:[-*]\s*)?(?:\*\*)?Provider(?:\*\*)?\s*:\s*(?:\*\*)?(.+?)(?:\*\*)?\s*$",
                line,
                flags=re.IGNORECASE,
            )
            if provider_match:
                provider = provider_match.group(1).strip().strip("*")
        if title and provider:
            break
    return title, provider


def _provider_from_path(path: Path) -> str:
    parts = [part.casefold() for part in path.parts]
    try:
        index = parts.index("library")
    except ValueError:
        return ""
    if index + 1 < len(path.parts):
        return path.parts[index + 1]
    return ""


def _markdown_candidates(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix().casefold()):
        if not path.is_file() or path.is_symlink():
            continue
        if path.suffix.casefold() != ".md":
            continue
        if path.name.casefold() in {"readme.md", "manifest.md"}:
            continue
        yield path


def build_archive_index(root: str | os.PathLike[str]) -> ArchiveIndex:
    """Index existing ``conversation.json`` and Markdown files below *root*.

    A JSON file and the Markdown file beside it become one record.  A Markdown
    file without JSON is indexed on its own, which also supports older exports.
    Malformed JSON never prevents the rest of an archive from being searched.
    """

    archive_root = Path(root).expanduser().resolve()
    if not archive_root.is_dir():
        raise NotADirectoryError(f"Archive root is not a directory: {archive_root}")

    json_files = [
        path
        for path in sorted(
            archive_root.rglob("*"),
            key=lambda item: item.as_posix().casefold(),
        )
        if path.is_file()
        and not path.is_symlink()
        and path.name.casefold() == "conversation.json"
    ]
    records: list[ArchiveRecord] = []
    json_parents: set[Path] = set()
    for json_path in json_files:
        json_parents.add(json_path.parent)
        markdown_paths = [
            path
            for path in _markdown_candidates(json_path.parent)
            if path.parent == json_path.parent
        ]
        markdown_path = next(
            (path for path in markdown_paths if path.name.casefold() == "conversation.md"),
            None,
        ) or next(
            (path for path in markdown_paths if path.name.casefold() == "thread.md"),
            None,
        ) or (markdown_paths[0] if markdown_paths else None)
        title, provider, json_content = _json_metadata(json_path)
        markdown_content = _read_text(markdown_path) if markdown_path else ""
        markdown_title, markdown_provider = _markdown_metadata(markdown_content)
        title = title or markdown_title or json_path.parent.name
        provider = provider or markdown_provider or _provider_from_path(json_path)
        content = "\n\n".join(
            value for value in (markdown_content, json_content) if value
        )
        relative = json_path.relative_to(archive_root).as_posix()
        records.append(
            ArchiveRecord(
                path=json_path,
                relative_path=relative,
                title=title,
                provider=provider,
                content=content,
                json_path=json_path,
                markdown_path=markdown_path,
            )
        )

    for markdown_path in _markdown_candidates(archive_root):
        if markdown_path.parent in json_parents:
            continue
        text = _read_text(markdown_path)
        title, provider = _markdown_metadata(text)
        title = title or markdown_path.stem
        provider = provider or _provider_from_path(markdown_path)
        records.append(
            ArchiveRecord(
                path=markdown_path,
                relative_path=markdown_path.relative_to(archive_root).as_posix(),
                title=title,
                provider=provider,
                content=text,
                markdown_path=markdown_path,
            )
        )

    records.sort(key=lambda record: record.relative_path.casefold())
    return ArchiveIndex(root=archive_root, records=records)


def search_archive(
    root: str | os.PathLike[str],
    query: str = "",
    *,
    provider: str | None = None,
) -> list[ArchiveRecord]:
    """Build an index and perform a case-insensitive title/provider/content search."""

    return build_archive_index(root).search(query, provider=provider)


@dataclass(frozen=True)
class BackupItem:
    """A source file that must be copied to the backup destination."""

    relative_path: str
    source: Path
    destination: Path
    size: int
    sha256: str


@dataclass
class BackupState:
    """Durable completion metadata used to resume an interrupted backup."""

    source_root: str = ""
    destination_root: str = ""
    completed: dict[str, dict[str, str | int]] = field(default_factory=dict)
    version: int = BACKUP_STATE_VERSION

    def to_dict(self) -> dict:
        return {
            "version": self.version,
            "source_root": self.source_root,
            "destination_root": self.destination_root,
            "completed": self.completed,
        }

    @classmethod
    def from_dict(cls, payload: object) -> "BackupState":
        if not isinstance(payload, dict):
            return cls()
        completed = payload.get("completed")
        try:
            version = int(payload.get("version") or BACKUP_STATE_VERSION)
        except (TypeError, ValueError):
            version = BACKUP_STATE_VERSION
        return cls(
            source_root=str(payload.get("source_root") or ""),
            destination_root=str(payload.get("destination_root") or ""),
            completed=completed if isinstance(completed, dict) else {},
            version=version,
        )


@dataclass
class BackupPlan:
    source_root: Path
    destination_root: Path
    items: list[BackupItem] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)
    state_path: Path | None = None

    @property
    def pending_count(self) -> int:
        return len(self.items)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(_CHUNK_SIZE), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _ensure_directory(path: Path) -> None:
    if path.exists():
        if path.is_symlink() or not path.is_dir():
            raise ValueError(f"Backup path is not a real directory: {path}")
        return
    if path.parent != path:
        _ensure_directory(path.parent)
    path.mkdir()


def _ensure_safe_child_directory(root: Path, path: Path) -> None:
    """Create a destination directory without traversing symlinked components."""

    relative = path.relative_to(root)
    current = root
    for part in relative.parts:
        current = current / part
        if current.exists():
            if current.is_symlink() or not current.is_dir():
                raise ValueError(f"Backup path is not a real directory: {current}")
        else:
            current.mkdir()


def _validate_roots(source_root: Path, destination_root: Path) -> None:
    if not source_root.is_dir():
        raise NotADirectoryError(f"Source root is not a directory: {source_root}")
    if destination_root == source_root or source_root in destination_root.parents:
        raise ValueError("Backup destination must not be inside the source archive")
    _ensure_directory(destination_root)


def load_backup_state(path: str | os.PathLike[str]) -> BackupState:
    """Load resume metadata; a missing or invalid file starts a fresh state."""

    state_path = Path(path)
    try:
        payload = json.loads(_read_text(state_path))
    except (OSError, json.JSONDecodeError, TypeError, ValueError):
        return BackupState()
    return BackupState.from_dict(payload)


def save_backup_state(
    path: str | os.PathLike[str],
    state: BackupState,
) -> None:
    """Atomically persist resume metadata beside the destination archive."""

    state_path = Path(path)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = state_path.with_name(f"{state_path.name}.partial")
    temporary.write_text(
        json.dumps(state.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    os.replace(temporary, state_path)


def _iter_source_files(root: Path, destination: Path) -> Iterable[Path]:
    destination_prefix = destination.as_posix().casefold().rstrip("/") + "/"
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix().casefold()):
        if not path.is_file() or path.is_symlink():
            continue
        if path.as_posix().casefold().startswith(destination_prefix):
            continue
        yield path


def plan_incremental_backup(
    source_root: str | os.PathLike[str],
    destination_root: str | os.PathLike[str],
    *,
    state_path: str | os.PathLike[str] | None = None,
) -> BackupPlan:
    """Plan only new/changed files, using hashes for reliable incremental copies."""

    source = Path(source_root).expanduser().resolve()
    destination = Path(destination_root).expanduser().absolute()
    _validate_roots(source, destination)
    resume_path = (
        Path(state_path).expanduser().absolute()
        if state_path is not None
        else destination / DEFAULT_STATE_NAME
    )
    if resume_path == source or source in resume_path.parents:
        raise ValueError("Resume metadata must not be stored inside the source archive")
    state = load_backup_state(resume_path)
    state.source_root = str(source)
    state.destination_root = str(destination)
    items: list[BackupItem] = []
    skipped: list[str] = []
    for source_path in _iter_source_files(source, destination):
        relative = source_path.relative_to(source).as_posix()
        destination_path = destination.joinpath(*relative.split("/"))
        digest = _sha256(source_path)
        same_destination = (
            destination_path.is_file()
            and not destination_path.is_symlink()
            and _sha256(destination_path) == digest
        )
        if same_destination:
            skipped.append(relative)
            state.completed[relative] = {"sha256": digest, "size": source_path.stat().st_size}
            continue
        items.append(
            BackupItem(
                relative_path=relative,
                source=source_path,
                destination=destination_path,
                size=source_path.stat().st_size,
                sha256=digest,
            )
        )
    save_backup_state(resume_path, state)
    return BackupPlan(
        source_root=source,
        destination_root=destination,
        items=items,
        skipped=skipped,
        state_path=resume_path,
    )


def execute_backup(
    plan: BackupPlan,
    *,
    on_item: Callable[[BackupItem], None] | None = None,
) -> list[BackupItem]:
    """Copy a plan with per-file atomic replacement and durable resume updates."""

    state_path = plan.state_path or plan.destination_root / DEFAULT_STATE_NAME
    state = load_backup_state(state_path)
    state.source_root = str(plan.source_root)
    state.destination_root = str(plan.destination_root)
    copied: list[BackupItem] = []
    for item in plan.items:
        _ensure_safe_child_directory(plan.destination_root, item.destination.parent)
        if item.destination.exists() and item.destination.is_symlink():
            raise ValueError(f"Refusing to replace symlink: {item.destination}")
        if item.destination.exists() and not item.destination.is_file():
            raise ValueError(f"Refusing to replace non-file: {item.destination}")
        partial = item.destination.with_name(f"{item.destination.name}.partial")
        try:
            with item.source.open("rb") as source_stream, partial.open("wb") as target_stream:
                shutil.copyfileobj(source_stream, target_stream, length=_CHUNK_SIZE)
                target_stream.flush()
                os.fsync(target_stream.fileno())
            if _sha256(partial) != item.sha256:
                raise IOError(f"Source changed while backing up: {item.relative_path}")
            os.replace(partial, item.destination)
        finally:
            if partial.exists():
                partial.unlink()
        state.completed[item.relative_path] = {
            "sha256": item.sha256,
            "size": item.size,
        }
        save_backup_state(state_path, state)
        copied.append(item)
        if on_item:
            on_item(item)
    return copied
