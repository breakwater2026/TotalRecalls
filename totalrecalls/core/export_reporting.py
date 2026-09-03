"""Export integrity checks and observable retry execution."""

from __future__ import annotations

import hashlib
import json
import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from totalrecalls.core.chat_import import ImportValidationError, parse_ai_chat_export_json


@dataclass(frozen=True)
class IntegrityProblem:
    path: str
    message: str


@dataclass
class ExportIntegrityReport:
    root: str
    checked_files: int = 0
    checked_conversations: int = 0
    hashes: dict[str, str] = field(default_factory=dict)
    problems: list[IntegrityProblem] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.problems

    def to_dict(self) -> dict[str, Any]:
        return {
            "root": self.root,
            "ok": self.ok,
            "checked_files": self.checked_files,
            "checked_conversations": self.checked_conversations,
            "hashes": dict(self.hashes),
            "problems": [{"path": item.path, "message": item.message} for item in self.problems],
        }


class ExportIntegrityError(ValueError):
    """Raised by assert_export_integrity when an archive is incomplete."""

    def __init__(self, report: ExportIntegrityReport) -> None:
        self.report = report
        details = "; ".join(f"{p.path}: {p.message}" for p in report.problems[:8])
        super().__init__(f"Export integrity check failed ({len(report.problems)} problem(s)): {details}")


def _safe_relative(root: Path, value: Any, report: ExportIntegrityReport, label: str) -> Path | None:
    if not isinstance(value, str) or not value.strip():
        report.problems.append(IntegrityProblem(label, "manifest path is required"))
        return None
    candidate = Path(value.replace("\\", os.sep))
    if candidate.is_absolute() or ".." in candidate.parts:
        report.problems.append(IntegrityProblem(label, "manifest path escapes export root"))
        return None
    resolved = (root / candidate).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError:
        report.problems.append(IntegrityProblem(label, "manifest path escapes export root"))
        return None
    return resolved


def _hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_export_integrity(root: str | Path) -> ExportIntegrityReport:
    """Validate every manifest-declared conversation and its two output files."""
    root_path = Path(root).expanduser().resolve()
    report = ExportIntegrityReport(str(root_path))
    manifest_path = root_path / "manifest.json"
    if not root_path.is_dir():
        report.problems.append(IntegrityProblem(".", "export root is not a directory"))
        return report
    if not manifest_path.is_file():
        report.problems.append(IntegrityProblem("manifest.json", "manifest is missing"))
        return report
    report.checked_files += 1
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        report.problems.append(IntegrityProblem("manifest.json", f"cannot read manifest: {exc}"))
        return report
    if not isinstance(manifest, dict):
        report.problems.append(IntegrityProblem("manifest.json", "manifest must be an object"))
        return report
    threads = manifest.get("threads")
    if not isinstance(threads, list):
        report.problems.append(IntegrityProblem("manifest.json", "threads must be a list"))
        return report
    declared_total = manifest.get("total_threads")
    if declared_total is not None and declared_total != len(threads):
        report.problems.append(IntegrityProblem("manifest.json", "total_threads does not match threads"))
    seen_paths: set[str] = set()
    seen_ids: set[str] = set()
    for index, thread in enumerate(threads):
        label = f"threads[{index}]"
        if not isinstance(thread, dict):
            report.problems.append(IntegrityProblem(label, "thread entry must be an object"))
            continue
        folder = _safe_relative(root_path, thread.get("path"), report, f"{label}.path")
        if folder is None:
            continue
        rel = folder.relative_to(root_path.resolve()).as_posix()
        if rel in seen_paths:
            report.problems.append(IntegrityProblem(rel, "duplicate manifest path"))
            continue
        seen_paths.add(rel)
        conversation_json = folder / "conversation.json"
        conversation_md = folder / "conversation.md"
        for required in (conversation_json, conversation_md):
            report.checked_files += 1
            if not required.is_file():
                report.problems.append(IntegrityProblem(str(required.relative_to(root_path)), "required file is missing"))
                continue
            try:
                report.hashes[required.relative_to(root_path).as_posix()] = _hash_file(required)
            except OSError as exc:
                report.problems.append(IntegrityProblem(str(required.relative_to(root_path)), f"cannot hash file: {exc}"))
        if conversation_md.is_file():
            try:
                if not conversation_md.read_text(encoding="utf-8"):
                    report.problems.append(
                        IntegrityProblem(str(conversation_md.relative_to(root_path)), "Markdown file is empty")
                    )
            except (OSError, UnicodeDecodeError) as exc:
                report.problems.append(
                    IntegrityProblem(str(conversation_md.relative_to(root_path)), f"cannot read Markdown: {exc}")
                )
        if not conversation_json.is_file():
            continue
        try:
            payload = json.loads(conversation_json.read_text(encoding="utf-8"))
            conversations = parse_ai_chat_export_json(payload, source_name=str(conversation_json))
            if len(conversations) != 1:
                raise ImportValidationError("conversation.json must contain exactly one conversation")
            conv = conversations[0]
            report.checked_conversations += 1
            expected_id = thread.get("id", thread.get("uuid"))
            if expected_id and conv.id and expected_id != conv.id:
                report.problems.append(IntegrityProblem(rel, "manifest id does not match conversation.json"))
            if conv.id:
                if conv.id in seen_ids:
                    report.problems.append(IntegrityProblem(rel, "duplicate conversation id"))
                seen_ids.add(conv.id)
        except (OSError, json.JSONDecodeError, ImportValidationError, ValueError, TypeError) as exc:
            report.problems.append(IntegrityProblem(str(conversation_json.relative_to(root_path)), f"invalid conversation JSON: {exc}"))
    return report


def assert_export_integrity(root: str | Path) -> ExportIntegrityReport:
    report = verify_export_integrity(root)
    if not report.ok:
        raise ExportIntegrityError(report)
    return report


@dataclass(frozen=True)
class RetryAttempt:
    number: int
    succeeded: bool
    error_type: str = ""
    error: str = ""
    delay_seconds: float = 0.0


@dataclass
class RetryReport:
    attempts: list[RetryAttempt] = field(default_factory=list)

    @property
    def succeeded(self) -> bool:
        return bool(self.attempts and self.attempts[-1].succeeded)

    @property
    def retry_count(self) -> int:
        return max(0, len(self.attempts) - 1)

    @property
    def exhausted(self) -> bool:
        return bool(self.attempts) and not self.succeeded

    def to_dict(self) -> dict[str, Any]:
        return {
            "succeeded": self.succeeded,
            "retry_count": self.retry_count,
            "exhausted": self.exhausted,
            "attempts": [
                {
                    "number": item.number,
                    "succeeded": item.succeeded,
                    "error_type": item.error_type,
                    "error": item.error,
                    "delay_seconds": item.delay_seconds,
                }
                for item in self.attempts
            ],
        }


class RetryExhaustedError(RuntimeError):
    """Raised after all configured attempts fail."""

    def __init__(self, report: RetryReport) -> None:
        self.report = report
        last = report.attempts[-1] if report.attempts else None
        message = last.error if last else "operation was not attempted"
        super().__init__(f"Retry budget exhausted after {len(report.attempts)} attempt(s): {message}")


@dataclass(frozen=True)
class RetryResult:
    value: Any
    report: RetryReport


def run_with_retries(
    operation: Callable[[], Any],
    *,
    max_attempts: int = 3,
    retry_if: Callable[[Exception], bool] | None = None,
    backoff_seconds: float = 0.0,
    sleep: Callable[[float], None] = time.sleep,
    on_attempt: Callable[[RetryAttempt], None] | None = None,
) -> RetryResult:
    """Run an operation while recording every attempt and delay."""
    if not callable(operation):
        raise TypeError("operation must be callable")
    if isinstance(max_attempts, bool) or not isinstance(max_attempts, int) or max_attempts < 1:
        raise ValueError("max_attempts must be a positive integer")
    if backoff_seconds < 0:
        raise ValueError("backoff_seconds cannot be negative")
    should_retry = retry_if or (lambda exc: isinstance(exc, (OSError, TimeoutError, ConnectionError)))
    report = RetryReport()
    for number in range(1, max_attempts + 1):
        try:
            value = operation()
        except Exception as exc:
            retryable = bool(should_retry(exc))
            delay = backoff_seconds * (2 ** (number - 1)) if retryable and number < max_attempts else 0.0
            attempt = RetryAttempt(number, False, type(exc).__name__, str(exc), delay)
            report.attempts.append(attempt)
            if on_attempt:
                on_attempt(attempt)
            if not retryable or number >= max_attempts:
                raise RetryExhaustedError(report) from exc
            if delay:
                sleep(delay)
        else:
            attempt = RetryAttempt(number, True)
            report.attempts.append(attempt)
            if on_attempt:
                on_attempt(attempt)
            return RetryResult(value, report)
    raise RetryExhaustedError(report)
