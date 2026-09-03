# Recurring local backups

TotalRecalls can run incremental, resumable backups on a user-selected
interval. The scheduler is always explicit: creating a scheduler does not
start a thread, and the command-line `start` command stays in the foreground.
There is no hidden daemon or OS startup task.

## Configure

```powershell
python -m totalrecalls.core.backup_scheduler configure `
  --source-root "C:\Users\me\TotalRecalls" `
  --destination-root "E:\Backups\TotalRecalls" `
  --interval-seconds 3600
```

Configuration is JSON. The default location is
`%APPDATA%\TotalRecalls\backup-config.json` (or
`~\.totalrecalls\backup-config.json` outside Windows):

```json
{
  "source_root": "C:\\Users\\me\\TotalRecalls",
  "destination_root": "E:\\Backups\\TotalRecalls",
  "interval_seconds": 3600,
  "state_path": null,
  "run_immediately": true
}
```

`interval_seconds` must be finite and greater than zero. The archive backup
state defaults to
`.totalrecalls-backup-state.json` in the destination. It is written after
each file, so an interrupted copy resumes safely.

## Start, stop, and status

```powershell
python -m totalrecalls.core.backup_scheduler start
python -m totalrecalls.core.backup_scheduler status
python -m totalrecalls.core.backup_scheduler stop
```

`start` is a foreground process. Pressing Ctrl+C requests cancellation. `stop`
writes a cancellation request next to the config; a foreground scheduler
observes it while waiting and exits without force-killing an in-progress
backup. Status is persisted to `backup-status.json`. Use a separate
`--config path\to\backup-config.json` with each command for another schedule.

To perform one backup without starting a recurring schedule:

```powershell
python -m totalrecalls.core.backup_scheduler run-once
```

The Python API also exposes `BackupScheduler.start()`,
`BackupScheduler.stop(timeout=...)`, `BackupScheduler.status()`, and
`BackupScheduler.run_once()`. Inject `backup_runner` and `status_hook` in
tests or integrations; `stop()` never force-terminates a worker and returns
`False` if a supplied timeout expires.
