# Robustness plan — 2026-10-17

## Why this exists

Three defects surfaced on launch eve, none of them subtle:

1. The app had been running under an interpreter without `clr`, so pythonnet could
   not dispatch WinForms/WebView2 events. The login timer never ticked and
   `on_init` never fired — silently, for hours, across every code change.
2. The paste dialog imported `Size` from `System.Windows.Forms` (it lives in
   `System.Drawing`) and had raised on every open **since it was written**.
3. Every video stitched after the shared title card was `High 4:4:4 / yuv444p`
   instead of `yuv420p`; Chrome plays it, Safari/iOS/Firefox do not.

Common thread: **all three failed without a word.** No exception reached the UI,
no log line, no test failed (222 passed throughout). The app's failure mode is
"nothing happens".

Secondary finding: `bridge.py` is 2,990 lines (23% of the 13,207-line codebase)
and contains **four copies** of the login flow — four `on_tick`, four `WinTimer()`,
four `*_login_window_flow`. Every fix must land four times, and there is no test
that proves it did.

## Principle

Do not chase line-level style. Make silent failure structurally impossible:
assert at startup, watch liveness at runtime, gate releases on measurements.

## A. Preflight self-check  (small, zero risk — DO FIRST)

`totalrecalls/core/preflight.py`, called once at startup before any window opens.
Checks: python version + path, `clr` importable, pythonnet version, WebView2
runtime version, log file writable. Logs every value as `preflight: ...`.
If `clr` or WebView2 is missing: push a blocking error to the UI naming the exact
missing piece, instead of running half-alive.

Acceptance: a run with a deliberately broken `clr` import shows the blocking
message; a healthy run logs `preflight: all checks passed`.

## B. Login-flow liveness watchdog  (small)

In the generic flow: if the window has been open `WATCHDOG_S = 45` s with zero
ticks and zero captured requests, log `WARN: login flow silent` and push a UI
message: "The embedded login isn't responding. Use the paste path instead, or
restart the app." Fires once per flow, never closes the window.

Acceptance: with the timer deliberately stopped, the warning appears within 45 s.

## C. Error surfacing  (small)

Every failed connect must carry a reason into the UI, not just app.log. Audit the
`except` paths in `connect()` and the flow; replace bare "Unable to connect" with
the exception class + one-line cause (already available via `friendly_error`).

Acceptance: forcing each failure mode shows a distinct, actionable message.

## D. Release gate  (medium, no app risk)

`tools/release_gate.py` — one command, no steps from memory:
build in the clean venv -> PYZ verify (edition, expected strings) -> repackage ZIP
-> recompute + write the page SHA -> deploy -> assert the served bytes match ->
for each render assert `pix_fmt=yuv420p`, `profile=High`, expected duration,
faststart. Exits non-zero on any mismatch.

Acceptance: run against the current artifacts — all pass; flip one to yuv444p and
it fails loudly.

## E. UI-layer smoke harness  (medium)

`tools/smoke_login.py`: for each provider id, start the flow in a subprocess with
a stub WebView2 hook, assert (i) the window is created, (ii) the timer ticks at
least twice, (iii) `on_init` fires, (iv) the flow closes cleanly. This is the tier
that was missing when the paste dialog threw for months.

Acceptance: 8/8 pass; breaking `on_tick` wiring makes the matching provider fail.

## F. De-duplicate the login flow  (large, do LAST behind E)

One parameterised flow replaces the four copies. Providers become data
(cookie names, probe URL, localStorage key, capture mechanism). Target: remove
~1,500 lines from `bridge.py` with zero behaviour change.

Acceptance: E passes 8/8 before and after; `grep -c "def on_tick" bridge.py` == 1.

## Order and why

A -> B -> C (same day, app-side, cheap) -> D (protects the release) -> E (the safety
net) -> F (the refactor, only with E green). F without E is a bet; F with E is a
controlled change.
