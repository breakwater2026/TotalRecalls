import tempfile
import threading
import time
import unittest
from pathlib import Path

from totalrecalls.core.backup_scheduler import (
    BackupRunResult,
    BackupScheduleConfig,
    BackupScheduler,
    SchedulerStatus,
    run_backup_once,
    validate_interval,
)


class BackupSchedulerTests(unittest.TestCase):
    def test_interval_validation_rejects_invalid_values(self):
        for value in (0, -1, float("inf"), float("nan"), True, "not-a-number"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    validate_interval(value)
        self.assertEqual(validate_interval("60"), 60.0)

    def test_config_round_trip_is_atomic_and_validated(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "config.json"
            config = BackupScheduleConfig("archive", "backup", 30, run_immediately=False)
            config.save(path)
            self.assertEqual(BackupScheduleConfig.load(path), config)
            self.assertNotIn(".partial", path.read_text(encoding="utf-8"))

    def test_run_once_uses_incremental_resumable_primitives(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "archive"
            destination = root / "backup"
            source.mkdir()
            (source / "one.md").write_text("one", encoding="utf-8")
            config = BackupScheduleConfig(str(source), str(destination), 60)

            first = run_backup_once(config)
            second = run_backup_once(config)

            self.assertEqual(first.copied, 1)
            self.assertEqual(second.copied, 0)
            self.assertEqual(second.skipped, 1)
            self.assertEqual((destination / "one.md").read_text(encoding="utf-8"), "one")

    def test_start_is_explicit_and_stop_cancels_wait(self):
        calls = []
        config = BackupScheduleConfig("source", "destination", 60, run_immediately=False)
        scheduler = BackupScheduler(config, backup_runner=lambda _: calls.append(1))

        self.assertFalse(scheduler.status().running)
        scheduler.start()
        self.assertTrue(scheduler.status().running)
        self.assertIsNotNone(scheduler._thread)
        self.assertFalse(scheduler._thread.daemon)
        self.assertTrue(scheduler.stop(timeout=1))
        self.assertFalse(scheduler.status().running)
        self.assertEqual(calls, [])

    def test_execution_hook_runs_repeatedly_and_status_is_published(self):
        calls = []
        statuses: list[SchedulerStatus] = []
        finished = threading.Event()

        def runner(config):
            calls.append(config.source_root)
            if len(calls) >= 2:
                finished.set()
            now = "2026-01-01T00:00:00+00:00"
            return BackupRunResult(len(calls), 0, now, now)

        scheduler = BackupScheduler(
            BackupScheduleConfig("source", "destination", 0.01),
            backup_runner=runner,
            status_hook=statuses.append,
            poll_seconds=0.005,
        )
        scheduler.start()
        self.assertTrue(finished.wait(1))
        self.assertTrue(scheduler.stop(timeout=1))
        self.assertGreaterEqual(len(calls), 2)
        self.assertEqual(scheduler.status().last_result.copied, len(calls))
        self.assertFalse(scheduler.status().running)
        self.assertTrue(any(status.running for status in statuses))
        self.assertFalse(statuses[-1].running)

    def test_runner_error_is_recorded_and_schedule_remains_stoppable(self):
        calls = []

        def runner(_):
            calls.append(1)
            raise OSError("disk unavailable")

        scheduler = BackupScheduler(
            BackupScheduleConfig("source", "destination", 0.01),
            backup_runner=runner,
            poll_seconds=0.005,
        )
        scheduler.start()
        deadline = time.monotonic() + 1
        while not scheduler.status().last_error and time.monotonic() < deadline:
            time.sleep(0.005)
        self.assertIn("disk unavailable", scheduler.status().last_error)
        self.assertTrue(scheduler.stop(timeout=1))
        self.assertGreaterEqual(len(calls), 1)

    def test_stop_request_hook_is_checked_while_waiting(self):
        stop = threading.Event()
        calls = []
        scheduler = BackupScheduler(
            BackupScheduleConfig("source", "destination", 60, run_immediately=False),
            backup_runner=lambda _: calls.append(1),
            stop_requested=stop.is_set,
            poll_seconds=0.01,
        )
        scheduler.start()
        stop.set()
        self.assertTrue(scheduler.wait(1))
        self.assertEqual(calls, [])
        self.assertFalse(scheduler.status().running)


if __name__ == "__main__":
    unittest.main()
