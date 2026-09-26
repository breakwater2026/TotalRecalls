"""Fail the build if the UI calls a bridge method that pywebview does not expose.

`window.pywebview.api` is the JsApi facade, NOT the Bridge. If app_ui.html calls
a method that JsApi does not delegate, the call throws "not a function" inside
the webview: the handler dies mid-way (leaving whatever status text was set
last on screen), Python is never called, and nothing appears in any log. That is
exactly how the Activate button shipped broken (2026-09-26): Bridge.activateLicense
existed and worked, but JsApi did not delegate it, so the button sat on
"Activating…" forever and the license server never heard from the app.

Run this before packaging. Exit 0 = the UI and the facade agree.
"""
from __future__ import annotations

import io
import re
import sys

UI = r"C:\Users\break\Projects\TotalRecalls\app_ui.html"
FACADE = r"C:\Users\break\Projects\TotalRecalls\totalrecalls\desktop\js_api.py"
BRIDGE = r"C:\Users\break\Projects\TotalRecalls\totalrecalls\desktop\bridge.py"

# JS members that are not bridge calls (property access on the same expressions).
JS_MEMBERS = {
    "then", "catch", "finally", "textContent", "value", "classList",
    "innerHTML", "querySelector", "querySelectorAll", "style", "dataset",
    "addEventListener", "focus", "blur", "click", "disabled", "checked",
    "setAttribute", "getAttribute", "removeAttribute", "appendChild",
    "removeChild", "insertBefore", "scrollIntoView", "getContext",
    "classList", "title", "href", "src", "play", "pause",
}


def main() -> int:
    ui = io.open(UI, encoding="utf-8").read()
    facade_src = io.open(FACADE, encoding="utf-8").read()
    bridge_src = io.open(BRIDGE, encoding="utf-8").read()

    called = {
        m.group(1)
        for m in re.finditer(r"\b(?:a|api|window\.pywebview\.api)\.([A-Za-z_]\w*)\s*\(", ui)
    } - JS_MEMBERS
    exposed = set(re.findall(r"^    def (\w+)\(", facade_src, re.M))
    on_bridge = set(re.findall(r"^    def (\w+)\(", bridge_src, re.M))

    missing = sorted(m for m in called if m not in exposed)
    # A method the UI calls must exist somewhere callable.
    nonexistent = sorted(m for m in called if m not in on_bridge and m not in exposed)

    print("UI calls %d bridge method(s); JsApi exposes %d." % (len(called), len(exposed)))
    for m in missing:
        print("  NOT DELEGATED: %s()  (on Bridge: %s)" % (m, m in on_bridge))

    if missing:
        print("\nFAIL — these UI calls will throw 'not a function' in the webview.")
        return 1
    if nonexistent:
        print("\nFAIL — the UI calls methods that do not exist at all: %s" % (nonexistent,))
        return 1
    print("OK — every method the UI calls is exposed by the JsApi facade.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
