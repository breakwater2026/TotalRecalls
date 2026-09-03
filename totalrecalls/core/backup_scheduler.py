"""Explicit, recurring local backups built on the incremental archive API.

The scheduler is deliberately an opt-in foreground service.  Constructing a
``BackupScheduler`` does not start a thread; callers must call :meth:`start`
and later :meth:`stop`.  The worker is non-daemon and cancellation is checked
while waiting between runs, so stopping a schedule never leaves a hidden
background process behind.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import threading
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from totalrecalls.core.local_archive import (
    BackupItem,
    execute_backup,
    plan_incremental_backup,
)

DEFAULT_CONFIG_NAME = "backup-config.json"
DEFAULT_STATUS_NAME = "backup-status.json"
DEFAULT_STOP_NAME = "backup-stop"


def validate_interval(value: Any) -> float:
    """Return a finite, positive interval in seconds.

    Strings are accepted for command-line/configuration boundaries, while
    booleans are rejected even though ``bool`` is an ``int`` subclass.
    """

    if isinstance(value, bool):
        raise ValueError("interval_seconds must be a positive number")
    try:
        interval = float(value)
    except (TypeError, ValueError):
        raise ValueError("interval_seconds must be a positive number") from None
    if not math.isfinite(interval) or interval <= 0:
        raise ValueError("interval_seconds must be a positive, finite number")
    return interval


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def default_config_path() -> Path:
    """Return the per-user configuration path without creating a schedule."""

    base = os.environ.get("APPDATA") or os.environ.get("LOCALAPPDATA")
    root = Path(base).expanduser() / "TotalRecalls" if base else Path.home() / ".totalrecalls"
    return root / DEFAULT_CONFIG_NAME


@dataclass(frozen=True)
class BackupScheduleConfig:
    """Configuration for one recurring archive backup."""

    source_root: str
    destination_root: str
    interval_seconds: float
    state_path: str | None = None
    run_immediately: bool = True

    def __post_init__(self) -> None:
        source_root = "" if self.source_root is None else str(self.source_root).strip()
        destination_root = (
            "" if self.destination_root is None else str(self.destination_root).strip()
        )
        if not source_root:
            raise ValueError("source_root is required")
        if not destination_root:
            raise ValueError("destination_root is required")
        object.__setattr__(self, "source_root", source_root)
        object.__setattr__(self, "destination_root", destination_root)
        object.__setattr__(self, "interval_seconds", validate_interval(self.interval_seconds))

    @classmethod
    def from_dict(cls, payload: object) -> "BackupScheduleConfig":
        if not isinstance(payload, dict):
            raise ValueError("backup configuration must be a JSON object")
        try:
            source = payload["source_root"]
            destination = payload["destination_root"]
            interval = payload["interval_seconds"]
        except KeyError as exc:
            raise ValueError(f"missing backup configuration field: {exc.args[0]}") from None
        state_path = payload.get("state_path")
        return cls(
            source_root=source,
            destination_root=destination,
            interval_seconds=interval,
            state_path=str(state_path) if state_path else None,
            run_immediately=bool(payload.get("run_immediately", True)),
        )

    @classmethod
    def load(cls, path: str | os.PathLike[str]) -> "BackupScheduleConfig":
        config_path = Path(path)
        try:
            payload = json.loads(config_path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            raise FileNotFoundError(f"backup configuration not found: {config_path}") from None
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError(f"could not read backup configuration: {exc}") from exc
        return cls.from_dict(payload)

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_root": self.source_root,
            "destination_root": self.destination_root,
            "interval_seconds": self.interval_seconds,
            "state_path": self.state_path,
            "run_immediately": self.run_immediately,
        }

    def save(self, path: str | os.PathLike[str]) -> Path:
        config_path = Path(path).expanduser()
        config_path.parent.mkdir(parents=True, exist_ok=True)
        temporary = config_path.with_name(f"{config_path.name}.partial")
        temporary.write_text(
            json.dumps(self.to_dict(), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        os.replace(temporary, config_path)
        return config_path


@dataclass(frozen=True)
class BackupRunResult:
    copied: int
    skipped: int
    started_at: str
    finished_at: str


@dataclass(frozen=True)
class SchedulerStatus:
    running: bool
    run_count: int
    started_at: str | None = None
    last_started_at: str | None = None
    last_finished_at: str | None = None
    last_result: BackupRunResult | None = None
    last_error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self.last_result) if self.last_result else None
        return {
            "running": self.running,
            "run_count": self.run_count,
            "started_at": self.started_at,
            "last_started_at": self.last_started_at,
            "last_finished_at": self.last_finished_at,
            "last_result": result,
            "last_error": self.last_error,
        }


BackupRunner = Callable[[BackupScheduleConfig], BackupRunResult]
StatusHook = Callable[[SchedulerStatus], None]
StopRequested = Callable[[], bool]


def run_backup_once(
    config: BackupScheduleConfig,
    *,
    on_item: Callable[[BackupItem], None] | None = None,
) -> BackupRunResult:
    """Plan and execute one incremental, resumable backup."""

    started = _timestamp()
    plan = plan_incremental_backup(
        config.source_root,
        config.destination_root,
        state_path=config.state_path,
    )
    copied = execute_backup(plan, on_item=on_item)
    return BackupRunResult(
        copied=len(copied),
        skipped=len(plan.skipped),
        started_at=started,
        finished_at=_timestamp(),
    )


class BackupScheduler:
    """Run a backup repeatedly until explicitly stopped.

    ``backup_runner`` is injectable so callers can test scheduling without
    touching disk.  ``status_hook`` can persist status for a CLI or UI, and
    ``stop_requested`` can bridge an external stop request to this scheduler.
    """

    def __init__(
        self,
        config: BackupScheduleConfig,
        *,
        backup_runner: BackupRunner = run_backup_once,
        status_hook: StatusHook | None = None,
        stop_requested: StopRequested | None = None,
        poll_seconds: float = 0.5,
    ) -> None:
        self.config = config
        self.backup_runner = backup_runner
        self.status_hook = status_hook
        self.stop_requested = stop_requested
        self.poll_seconds = validate_interval(poll_seconds)
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None
        self._lock = threading.RLock()
        self._status = SchedulerStatus(running=False, run_count=0)

    def start(self) -> None:
        """Start the non-daemon worker; does nothing implicitly at construction."""

        with self._lock:
            if self._thread is not None and self._thread.is_alive():
                raise RuntimeError("backup scheduler is already running")
            self._stop_event.clear()
            self._status = SchedulerStatus(
                running=True,
                run_count=self._status.run_count,
                started_at=_timestamp(),
            )
            self._publish_status()
            self._thread = threading.Thread(
                target=self._run_loop,
                name="TotalRecallsBackupScheduler",
                daemon=False,
            )
            self._thread.start()

    def stop(self, timeout: float | None = None) -> bool:
        """Request cancellation and wait for the worker when possible.

        The return value is ``True`` when the worker has stopped.  ``False``
        means a user-supplied timeout expired while a backup hook was still
        running; the worker is never force-killed.
        """

        with self._lock:
            thread = self._thread
            self._stop_event.set()
        if thread is None or thread is threading.current_thread():
            return True
        thread.join(timeout)
        return not thread.is_alive()

    def run_once(self) -> BackupRunResult:
        """Execute one backup synchronously through the configured hook."""

        with self._lock:
            if self._status.running and self._thread is not threading.current_thread():
                raise RuntimeError("cannot run a synchronous backup while scheduler is running")
            self._status = SchedulerStatus(
                running=self._status.running,
                run_count=self._status.run_count + 1,
                started_at=self._status.started_at,
                last_started_at=_timestamp(),
                last_finished_at=self._status.last_finished_at,
                last_result=self._status.last_result,
                last_error=None,
            )
            self._publish_status()
        try:
            result = self.backup_runner(self.config)
        except Exception as exc:
            with self._lock:
                self._status = SchedulerStatus(
                    running=self._status.running,
                    run_count=self._status.run_count,
                    started_at=self._status.started_at,
                    last_started_at=self._status.last_started_at,
                    last_finished_at=_timestamp(),
                    last_result=self._status.last_result,
                    last_error=f"{type(exc).__name__}: {exc}",
                )
                self._publish_status()
            raise
        with self._lock:
            self._status = SchedulerStatus(
                running=self._status.running,
                run_count=self._status.run_count,
                started_at=self._status.started_at,
                last_started_at=self._status.last_started_at,
                last_finished_at=result.finished_at,
                last_result=result,
                last_error=None,
            )
            self._publish_status()
        return result

    def status(self) -> SchedulerStatus:
        with self._lock:
            return self._status

    def wait(self, timeout: float | None = None) -> bool:
        """Wait for a started worker, returning whether it has stopped."""

        with self._lock:
            thread = self._thread
        if thread is None:
            return True
        thread.join(timeout)
        return not thread.is_alive()

    def _publish_status(self) -> None:
        if self.status_hook:
            self.status_hook(self._status)

    def _should_stop(self) -> bool:
        if self._stop_event.is_set():
            return True
        if self.stop_requested:
            try:
                if self.stop_requested():
                    self._stop_event.set()
                    return True
            except Exception as exc:
                with self._lock:
                    self._status = SchedulerStatus(
                        running=self._status.running,
                        run_count=self._status.run_count,
                        started_at=self._status.started_at,
                        last_started_at=self._status.last_started_at,
                        last_finished_at=self._status.last_finished_at,
                        last_result=self._status.last_result,
                        last_error=f"stop request failed: {type(exc).__name__}: {exc}",
                    )
                    self._publish_status()
        return False

    def _wait_for_interval(self) -> bool:
        remaining = self.config.interval_seconds
        while remaining > 0:
            if self._should_stop():
                return True
            wait_for = min(remaining, self.poll_seconds)
            started = time.monotonic()
            if self._stop_event.wait(wait_for):
                return True
            remaining -= max(time.monotonic() - started, wait_for)
        return self._should_stop()

    def _run_loop(self) -> None:
        try:
            if self.config.run_immediately and not self._should_stop():
                try:
                    self.run_once()
                except Exception:
                    # The error is recorded in status; a transient failed run
                    # must not silently terminate a recurring schedule.
                    pass
            while not self._should_stop():
                if self._wait_for_interval():
                    break
                try:
                    self.run_once()
                except Exception:
                    pass
        finally:
            with self._lock:
                self._status = SchedulerStatus(
                    running=False,
                    run_count=self._status.run_count,
                    started_at=self._status.started_at,
                    last_started_at=self._status.last_started_at,
                    last_finished_at=self._status.last_finished_at,
                    last_result=self._status.last_result,
                    last_error=self._status.last_error,
                )
                self._publish_status()


def _runtime_path(config_path: Path, name: str) -> Path:
    return config_path.with_name(name)


def _write_status(path: Path, status: SchedulerStatus) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = status.to_dict()
    payload["pid"] = os.getpid()
    temporary = path.with_name(f"{path.name}.partial")
    temporary.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    os.replace(temporary, path)


def _read_status(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {"running": False, "message": "scheduler has not been started"}
    except (OSError, json.JSONDecodeError):
        return {"running": False, "message": "scheduler status is unavailable"}


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage explicit recurring TotalRecalls backups")
    parser.add_argument("--config", type=Path, default=default_config_path())
    subparsers = parser.add_subparsers(dest="command", required=True)

    configure = subparsers.add_parser("configure", help="write backup configuration")
    configure.add_argument("--source-root", required=True)
    configure.add_argument("--destination-root", required=True)
    configure.add_argument("--interval-seconds", required=True, type=float)
    configure.add_argument("--state-path")
    configure.add_argument("--no-run-immediately", action="store_true")

    start = subparsers.add_parser("start", help="run the schedule in the foreground")
    start.add_argument("--no-run-immediately", action="store_true")

    subparsers.add_parser("stop", help="request cancellation of a foreground schedule")
    subparsers.add_parser("status", help="show the last persisted scheduler status")
    subparsers.add_parser("run-once", help="execute one incremental backup")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    config_path = args.config.expanduser()
    status_path = _runtime_path(config_path, DEFAULT_STATUS_NAME)
    stop_path = _runtime_path(config_path, DEFAULT_STOP_NAME)

    if args.command == "configure":
        config = BackupScheduleConfig(
            source_root=args.source_root,
            destination_root=args.destination_root,
            interval_seconds=args.interval_seconds,
            state_path=args.state_path,
            run_immediately=not args.no_run_immediately,
        )
        config.save(config_path)
        print(f"saved {config_path}")
        return 0
    if args.command == "status":
        print(json.dumps(_read_status(status_path), indent=2))
        return 0
    if args.command == "stop":
        stop_path.parent.mkdir(parents=True, exist_ok=True)
        stop_path.write_text("stop\n", encoding="utf-8")
        print(f"stop requested via {stop_path}")
        return 0

    config = BackupScheduleConfig.load(config_path)
    if args.command == "run-once":
        result = run_backup_once(config)
        print(json.dumps(asdict(result), indent=2))
        return 0

    stop_path.unlink(missing_ok=True)
    if _read_status(status_path).get("running"):
        raise SystemExit("backup scheduler already reports a running foreground process")
    config = BackupScheduleConfig(
        source_root=config.source_root,
        destination_root=config.destination_root,
        interval_seconds=config.interval_seconds,
        state_path=config.state_path,
        run_immediately=not args.no_run_immediately and config.run_immediately,
    )
    scheduler = BackupScheduler(
        config,
        status_hook=lambda status: _write_status(status_path, status),
        stop_requested=stop_path.exists,
    )
    scheduler.start()
    try:
        scheduler.wait()
    except KeyboardInterrupt:
        scheduler.stop(timeout=5)
        return 130
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
