"""TotalRecalls soak test: run N consecutive export cycles per provider, unattended.

Measures success rate, failures by type, and timing across runs so stability can be
quantified (e.g. "40/40 ChatGPT exports completed with 0 failed conversations").

Usage:
    python tools/soak_test.py --provider chatgpt --runs 10
    python tools/soak_test.py --provider perplexity --runs 20 --limit 5
    python tools/soak_test.py --all --runs 10

Credentials are read from the app's session store (%APPDATA%/PerplexityExporter/session.json)
when present; otherwise pass --token per provider or set TR_SOAK_TOKEN_<PROVIDER> env vars.

Each "run" = one full export_via_adapter cycle into a fresh per-run output folder.
Run results append to soak_results.json for later analysis.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import statistics
import sys
import time
import traceback
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from totalrecalls.adapters.base import get_adapter          # noqa: E402
from totalrecalls.core.unified_export import export_via_adapter  # noqa: E402

APPDATA = os.path.join(os.environ.get("APPDATA", ""), "PerplexityExporter")
RESULTS_FILE = os.path.join(APPDATA, "soak_results.json")


def load_credential(provider: str, cli_token: str | None) -> str | None:
    if cli_token:
        return cli_token
    env = os.environ.get(f"TR_SOAK_TOKEN_{provider.upper()}")
    if env:
        return env
    sj = os.path.join(APPDATA, "session.json")
    try:
        with open(sj, encoding="utf-8") as f:
            d = json.load(f)
        if d.get("provider") == provider and d.get("token"):
            return d["token"]
    except Exception:
        pass
    return None


def load_results() -> list[dict]:
    try:
        with open(RESULTS_FILE, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def save_results(rows: list[dict]) -> None:
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=1)


def summarize(rows: list[dict], provider: str) -> dict:
    rs = [r for r in rows if r["provider"] == provider]
    if not rs:
        return {}
    times = [r["seconds"] for r in rs if r["ok"]]
    fails: dict[str, int] = {}
    for r in rs:
        if not r["ok"]:
            key = r.get("error_type", "unknown")
            fails[key] = fails.get(key, 0) + 1
    out = {
        "provider": provider,
        "runs": len(rs),
        "passed": sum(1 for r in rs if r["ok"]),
        "failed": sum(1 for r in rs if not r["ok"]),
        "failure_types": fails,
        "success_rate_pct": round(100.0 * sum(1 for r in rs if r["ok"]) / len(rs), 1),
    }
    convs = [r.get("exported", 0) for r in rs if r["ok"]]
    if convs:
        out["conversations_per_run"] = {"min": min(convs), "max": max(convs)}
    if times:
        out["duration_sec"] = {
            "min": round(min(times), 1),
            "median": round(statistics.median(times), 1),
            "max": round(max(times), 1),
        }
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--provider", help="provider id (chatgpt, claude, gemini, grok, perplexity)")
    ap.add_argument("--all", action="store_true", help="run every provider sequentially")
    ap.add_argument("--runs", type=int, default=10, help="number of export cycles per provider")
    ap.add_argument("--limit", type=int, default=0, help="cap conversations per run (0 = all)")
    ap.add_argument("--cooldown", type=float, default=30.0,
                    help="seconds between runs (rate-limit hygiene)")
    ap.add_argument("--outdir", default=os.path.join(APPDATA, "soak_runs"))
    args = ap.parse_args()

    providers = ["chatgpt", "claude", "gemini", "grok", "perplexity"] if args.all else [args.provider]
    rows = load_results()

    for provider in providers:
        cred = load_credential(provider, os.environ.get("TR_SOAK_TOKEN", ""))
        if not cred:
            print(f"[{provider}] no credential found — connect once in the app first. Skipping.")
            continue
        adapter = get_adapter(provider)

        passed = failed = 0
        for run_no in range(1, args.runs + 1):
            outdir = os.path.join(args.outdir, f"{provider}_run{run_no:03d}")
            shutil.rmtree(outdir, ignore_errors=True)
            t0 = time.time()
            row = {
                "provider": provider,
                "run": run_no,
                "started_utc": datetime.now(timezone.utc).isoformat(),
                "ok": False,
            }
            try:
                result = export_via_adapter(adapter, credential=cred, outdir=outdir, deep=True)
                row.update({
                    "ok": True,
                    "exported": result.get("exported", 0),
                    "skipped": result.get("skipped", 0),
                    "failed": result.get("failed", 0),
                })
                passed += 1
                status = "PASS"
            except Exception as e:
                row.update({
                    "error_type": type(e).__name__,
                    "error_message": str(e)[:200],
                })
                failed += 1
                status = "FAIL"
                traceback.print_exc()
            row["seconds"] = round(time.time() - t0, 1)
            rows.append(row)
            save_results(rows)
            print(f"[{provider}] run {run_no}/{args.runs}: {status} "
                  f"({row['seconds']}s, exported={row.get('exported', '-')})")
            if run_no < args.runs:
                time.sleep(args.cooldown)

        s = summarize(rows, provider)
        print(f"\n=== {provider} summary ===\n{json.dumps(s, indent=1)}\n")

    print(f"results appended to {RESULTS_FILE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
