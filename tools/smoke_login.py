"""Runtime capability probe for the login event layer.

This is the tier that was missing on 2026-10-17: 224 unit tests passed while the
runtime could not dispatch a single .NET event, so every login flow was silently
dead. A unit test cannot see that. This probe can, without touching a provider.

It asserts, in isolation (no network, no provider, no login profile):
  1. preflight.run() reports no missing capability
  2. a WinForms Form + Timer can be created on an STA thread and the Tick fires
     -> pythonnet event dispatch works, which is what every login flow depends on
  3. Application.Run starts and exits cleanly

Run:  python tools/smoke_login.py     (exit 0 = healthy layer)
"""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)


def main() -> int:
    failures = []

    # 1. capabilities
    try:
        from totalrecalls.core import preflight
        problems = preflight.run()
    except Exception as e:
        problems = [f"preflight itself failed: {type(e).__name__}: {e}"]
    print(f"{'PASS' if not problems else 'FAIL'}  preflight capabilities")
    for p in problems:
        print(f"        {p}")
    if problems:
        failures.append("preflight")

    # 2 + 3. the event layer, in isolation
    ticks = []
    try:
        import clr  # noqa: F401
        clr.AddReference("System.Windows.Forms")
        clr.AddReference("System.Drawing")
        from System.Windows.Forms import Form, Timer, Application
        from System.Threading import Thread, ThreadStart, ApartmentState

        def runner():
            form = Form()
            form.Text = "smoke"
            # keep it out of sight: no focus steal, no visible flash
            try:
                form.StartPosition = 0
                form.Left = -3000
                form.Top = -3000
                form.Width = 200
                form.Height = 100
            except Exception:
                pass

            timer = Timer()
            timer.Interval = 300

            def on_tick(sender, args):
                ticks.append(1)
                if len(ticks) >= 3:
                    timer.Stop()
                    form.Close()

            globals()["_keep"] = on_tick  # keep the delegate alive
            timer.Tick += on_tick
            form.Show()
            timer.Start()
            Application.Run(form)

        t = Thread(ThreadStart(runner))
        t.SetApartmentState(ApartmentState.STA)
        t.IsBackground = True
        t.Start()
        t.Join(15000)
    except Exception as e:
        print(f"FAIL  event layer ({type(e).__name__}: {e})")
        failures.append("event-layer")
        ticks = ticks or []

    ok_ticks = len(ticks) >= 3
    print(f"{'PASS' if ok_ticks else 'FAIL'}  WinForms Tick fired ({len(ticks)} ticks)")
    if not ok_ticks:
        failures.append("ticks")

    print()
    if failures:
        print("SMOKE FAILED: " + ", ".join(failures))
        return 1
    print("SMOKE PASSED — host event layer is alive")
    return 0


if __name__ == "__main__":
    sys.exit(main())
