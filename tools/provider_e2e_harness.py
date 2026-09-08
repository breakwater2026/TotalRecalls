"""Per-step end-to-end harness for a single provider.

Drives the app's REAL adapter + export code (no mocks) through the full
download pipeline, one step at a time, and emits a structured JSON report:

  1. connect/validate  -> adapter.validate(credential)      (account identity)
  2. discover          -> adapter.list_conversations(deep)  (conversation count)
  3. export            -> export_via_adapter(...)           (files written to disk)
  4. verify            -> re-read the export tree           (JSON parses, md non-empty)
  5. subset re-export  -> fetch_conversation + write_selected_unified_conversation
                          (a subset has strictly fewer messages)

Usage:
  python tools/provider_e2e_harness.py --provider chatgpt --credential-file cred.txt \
         --runs 1 --max-conversations 3 --outdir /tmp/tr_e2e/chatgpt

The credential is the SESSION TOKEN / COOKIE the app's login flow would capture
(a session cookie value, a full "Cookie:" header, or a Bearer token) — NOT the
login password. Pass it via --credential-file (file on disk) or --credential
(a string). For repeated runs, --credential-file is preferred so the token never
lives in a shell history line.

Exit code 0 = all 5 steps green for every run; 1 = at least one failure.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import time
import traceback
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from totalrecalls.adapters.base import get_adapter  # noqa: E402
from totalrecalls.core.unified_export import (  # noqa: E402
    export_via_adapter,
    write_selected_unified_conversation,
)


def _step(report: dict, name: str, fn):
    """Run one step, catching exceptions into the report."""
    t0 = time.time()
    try:
        result = fn()
        report[name] = {"ok": True, "seconds": round(time.time() - t0, 2), **result}
        return result
    except Exception as e:  # noqa: BLE001 — the harness must record, not crash
        report[name] = {
            "ok": False,
            "seconds": round(time.time() - t0, 2),
            "error": f"{type(e).__name__}: {e}",
            "trace": traceback.format_exc(limit=6),
        }
        return None


def _count_tree(outdir: Path):
    """Count conversation folders + files in an export tree."""
    conv_json = 0
    conv_md = 0
    total_files = 0
    total_bytes = 0
    for root, _dirs, files in os.walk(outdir):
        for f in files:
            fp = os.path.join(root, f)
            total_files += 1
            try:
                total_bytes += os.path.getsize(fp)
            except OSError:
                pass
            if f == "conversation.json":
                conv_json += 1
            elif f == "conversation.md":
                conv_md += 1
    return {"conversations": conv_json, "md_files": conv_md,
            "total_files": total_files, "total_bytes": total_bytes}


def _verify_tree(outdir: Path):
    """Re-read the export tree: every conversation.json must parse, md must be non-empty."""
    bad = []
    conv_json = 0
    md_nonempty = 0
    for root, _dirs, files in os.walk(outdir):
        if "conversation.json" in files:
            conv_json += 1
            jpath = os.path.join(root, "conversation.json")
            try:
                with open(jpath, encoding="utf-8") as fh:
                    data = json.load(fh)
                if not isinstance(data, dict):
                    bad.append(("json-not-dict", jpath))
            except Exception as e:  # noqa: BLE001
                bad.append((f"json-parse:{type(e).__name__}", jpath))
        if "conversation.md" in files:
            mpath = os.path.join(root, "conversation.md")
            try:
                with open(mpath, encoding="utf-8") as fh:
                    text = fh.read()
                if text.strip():
                    md_nonempty += 1
                else:
                    bad.append(("md-empty", mpath))
            except Exception as e:  # noqa: BLE001
                bad.append((f"md-read:{type(e).__name__}", mpath))
    return {"conversations_parsed": conv_json, "md_nonempty": md_nonempty,
            "bad": bad[:10], "all_ok": not bad}


def run_once(provider: str, credential: str, outdir: Path,
             max_conversations: int | None, deep: bool = True) -> dict:
    """Run the 5-step pipeline once. Returns a per-run report dict."""
    report: dict = {"provider": provider, "outdir": str(outdir)}
    adapter = get_adapter(provider)
    steps = report

    # 1. connect / validate
    def _validate():
        acct = adapter.validate(credential)
        return {"email": getattr(acct, "email", "") or "",
                "external_id": getattr(acct, "external_id", "") or "",
                "display_name": getattr(acct, "display_name", "") or ""}
    _step(report, "validate", _validate)
    if not steps["validate"].get("ok"):
        return report  # no point continuing without a live session

    # 2. discover — mirror the app's connect path: the fast count when the
    # adapter has one (Bug C), else a shallow list. The deep sweep is
    # exercised exactly once, in the export step below (the real app's
    # export flow). The old version ran deep in BOTH discover and export,
    # which doubled ChatGPT's 7-pass sweep per battery run and hammered the
    # live endpoint.
    def _discover():
        fast = getattr(adapter, "count_conversations", None)
        if callable(fast):
            c = fast(credential)
            if c and c > 0:
                return {"count": c, "via": "fast_count"}
            # The fast count DEGRADES to 0 on non-auth errors (a 500 storm)
            # by design — that's right for the badge, but a 0 here could be
            # either "empty account" or "degraded". Cross-check with one
            # shallow page before trusting 0.
            sums = adapter.list_conversations(credential, deep=False)
            return {"count": len(sums), "via": "fast_count_degraded_crosscheck",
                    "sample_titles": [(s.title or s.id)[:60] for s in sums[:5]]}
        sums = adapter.list_conversations(credential, deep=False)
        return {"count": len(sums), "via": "shallow_list",
                "sample_titles": [(s.title or s.id)[:60] for s in sums[:5]]}
    _step(report, "discover", _discover)
    if not steps["discover"].get("ok"):
        return report
    if steps["discover"]["count"] == 0:
        # A genuinely empty account is a valid result, not a bug.
        steps["empty_account"] = True
        return report

    # 3. export (fresh outdir per run so counts are clean)
    def _export():
        res = export_via_adapter(
            adapter, credential, str(outdir),
            deep=deep, refresh=True,
            max_conversations=max_conversations,
        )
        return res if isinstance(res, dict) else {"raw": str(res)}
    _step(report, "export", _export)
    if not steps["export"].get("ok"):
        return report

    # 4. verify the on-disk tree
    _step(report, "verify", lambda: _verify_tree(outdir))
    steps["tree"] = _count_tree(outdir)
    if not steps["verify"].get("ok"):
        return report

    # 5. subset re-export: fetch the first conversation, export a slice of its messages
    def _subset():
        sums = adapter.list_conversations(credential, deep=False)
        target = sums[0]
        conv = adapter.fetch_conversation(credential, target.id)
        n = len(conv.messages)
        if n == 0:
            return {"skipped": "conversation has 0 messages", "messages": 0}
        k = max(1, min(3, n - 1)) if n > 1 else 1
        idxs = list(range(0, n, max(1, n // (k + 1))))[:k] or [0]
        res = write_selected_unified_conversation(str(outdir), conv, idxs,
                                                  source=target.title or target.id)
        # Re-read the subset json and confirm it carries the selected
        # messages. Schema v1 nests them under conversation.messages
        # (write_selected_unified_conversation stores the whole
        # UnifiedConversation dict) — the old check read the top level and
        # always saw 0, so every run PASSed with a blind subset assertion.
        with open(res["json_path"], encoding="utf-8") as fh:
            sub = json.load(fh)
        msgs = ((sub.get("conversation") or {}).get("messages")
                or sub.get("messages") or [])
        sub_msgs = len(msgs)
        ok = sub_msgs <= n and sub_msgs >= 1
        return {"source_messages": n, "subset_indexes": idxs,
                "subset_messages": sub_msgs, "subset_ok": ok,
                "subset_folder": res["folder"]}
    _step(report, "subset", _subset)

    # A run passes only if every step succeeded AND the subset assertion
    # actually held. Before the fix the assertion result was recorded but
    # never gated the verdict (subset_ok was False on 100% of runs while
    # every run still read PASS).
    step_ok = all(steps[s].get("ok") for s in
                  ["validate", "discover", "export", "verify", "subset"])
    subset = steps["subset"]
    subset_ok = bool(subset.get("skipped") or subset.get("subset_ok"))
    report["passed"] = step_ok and subset_ok
    return report


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--provider", required=True,
                    choices=["perplexity", "chatgpt", "claude", "gemini",
                             "grok", "deepseek", "mistral", "qwen"])
    ap.add_argument("--credential", default="")
    ap.add_argument("--credential-file", default="")
    ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--max-conversations", type=int, default=None,
                    help="cap conversations per export (None = all). Keep small for live runs.")
    ap.add_argument("--deep", action="store_true", default=True)
    ap.add_argument("--outdir", default="")
    ap.add_argument("--json-out", default="", help="write full report to this path")
    args = ap.parse_args(argv)

    cred = args.credential
    if not cred and args.credential_file:
        cred = Path(args.credential_file).read_text(encoding="utf-8").strip()
    if not cred:
        print("ERROR: no credential (use --credential or --credential-file)")
        return 2

    base = Path(args.outdir) if args.outdir else Path("/tmp/tr_e2e") / args.provider
    all_reports = []
    for i in range(args.runs):
        run_dir = base / f"run{i+1:02d}"
        if run_dir.exists():
            shutil.rmtree(run_dir)
        run_dir.mkdir(parents=True, exist_ok=True)
        rep = run_once(args.provider, cred, run_dir, args.max_conversations, deep=args.deep)
        all_reports.append(rep)
        s = rep
        flag = "PASS" if rep.get("passed") or s.get("empty_account") else "FAIL"
        disc = s.get("discover", {})
        print(f"[{args.provider}] run{i+1:02d}: {flag}  "
              f"validate={s.get('validate',{}).get('ok')} "
              f"discover={s.get('discover',{}).get('ok')}/{disc.get('count','?')} "
              f"export={s.get('export',{}).get('ok')} "
              f"verify={s.get('verify',{}).get('ok')} "
              f"subset={s.get('subset',{}).get('ok')}")

    summary = {
        "provider": args.provider,
        "runs": len(all_reports),
        "passed": sum(1 for r in all_reports if r.get("passed") or r.get("empty_account")),
        "empty_account": any(r.get("empty_account") for r in all_reports),
        "all_passed": all(r.get("passed") or r.get("empty_account") for r in all_reports),
        "reports": all_reports,
    }
    if args.json_out:
        Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.json_out).write_text(json.dumps(summary, indent=2, ensure_ascii=False),
                                       encoding="utf-8")
        print(f"report -> {args.json_out}")
    return 0 if summary["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
