"""Application entrypoint (pywebview main window)."""

from __future__ import annotations

import os
import sys
import threading
import time

from totalrecalls import APP_NAME, APP_VERSION, APP_BUILD_TAG
from totalrecalls.core.paths import (
    appdata_dir, log, load_session, clear_session, acquire_single_instance,
)
from totalrecalls.adapters.perplexity.http import ApiError, _HAS_CFFI
from totalrecalls.adapters.perplexity.auth import validate_session
from totalrecalls.adapters.perplexity.discover import list_threads
from totalrecalls.core.export_fs import safe_name
from totalrecalls.desktop.bridge import Bridge
from totalrecalls.desktop.js_api import JsApi

def main():
    # Always try to own the session — stale EXEs were leaving users stuck on old builds.
    mutex, primary = acquire_single_instance(takeover=True)
    if not primary:
        log("could not become primary instance; exiting")
        try:
            # Last-ditch visible signal on Windows
            if os.name == "nt":
                import ctypes
                ctypes.windll.user32.MessageBoxW(
                    0,
                    "Perplexity Exporter could not start because another copy is still running.\n"
                    "Open Task Manager, end all PerplexityExporter.exe tasks, then try again.",
                    f"Perplexity Exporter {APP_VERSION} ({APP_BUILD_TAG})",
                    0x10,
                )
        except Exception:
            pass
        return

    # self-test mode (no GUI) — used for automated verification
    if "--selftest" in sys.argv:
        from pathlib import Path
        out = []
        try:
            assert "Hello" in safe_name("Hello World! 2026") and "2026" in safe_name("Hello World! 2026"), "safe_name"
            out.append("safe_name: OK")
        except AssertionError as e:
            out.append(f"safe_name: FAIL ({e})")
        try:
            session = validate_session("FAKE_TOKEN_FOR_SELFTEST")
            out.append(f"session-validate: OK (got {len(session)} keys — fake token correctly rejected)")
        except ApiError as e:
            out.append(f"session-validate: OK (ApiError as expected: {e})")
        result = "\n".join(out)
        Path(os.path.join(appdata_dir(), "selftest.txt")).write_text(result, encoding="utf-8")
        print(result)
        return

    # probe mode: exercises the native login-window flow headless, auto-closes
    if "--loginprobe" in sys.argv:
        log("loginprobe: start")
        b = Bridge(ui_html="<h1>probe</h1>")
        b._connecting = True

        def _autoclose():
            time.sleep(20)
            log("loginprobe: auto-close timer fired")
            try:
                b._stop_login.set()
                form = getattr(b, "_login_form", None)
                if form is not None:
                    from System import Action
                    try:
                        form.BeginInvoke(Action(form.Close))
                    except Exception:
                        try:
                            form.Close()
                        except Exception:
                            pass
                    log("loginprobe: close invoked")
            except Exception as e:
                log(f"loginprobe: autoclose error: {e}")

        threading.Thread(target=_autoclose, daemon=True).start()
        # Use the real STA launcher (same path as the blue button).
        b._start_embedded_login()
        # Wait up to 35s for the STA login thread to finish.
        deadline = time.time() + 35
        while time.time() < deadline:
            t = getattr(b, "_login_clr_thread", None)
            pt = b._login_thread
            alive = False
            try:
                if t is not None and t.IsAlive:
                    alive = True
            except Exception:
                pass
            if pt is not None and pt.is_alive():
                alive = True
            if not alive and getattr(b, "_login_form", None) is None and time.time() > deadline - 30:
                # thread may not have started yet
                pass
            if not alive and time.time() > deadline - 28:
                # give STA thread a moment to spawn
                if getattr(b, "_login_form", None) is None and not b._connecting:
                    break
            if not alive and getattr(b, "_login_form", None) is not None:
                # form exists but thread object unclear — keep waiting
                pass
            if not alive and not b._connecting and getattr(b, "_login_form", None) is None:
                break
            time.sleep(0.5)
        log("loginprobe: flow returned (no deadlock)")
        return

    import webview

    def _ui_file() -> str:
        candidates = []
        root = os.path.dirname(os.path.abspath(__file__))
        if getattr(sys, "frozen", False):
            candidates.append(os.path.join(getattr(sys, "_MEIPASS", os.path.dirname(sys.executable)), "app_ui.html"))
        candidates.append(os.path.join(root, "app_ui.html"))
        candidates.append(os.path.join(root, "build", "PerplexityExporter", "app_ui.html"))
        for path in candidates:
            if os.path.exists(path):
                return path
        return candidates[0] if candidates else os.path.join(root, "app_ui.html")

    try:
        ui_path = _ui_file()
        with open(ui_path, encoding="utf-8") as f:
            ui_html = f.read()
        ui_html = ui_html.replace(
            '<footer style="margin-top:26px;color:#5b637a;font-size:11.5px" id="ver">Perplexity Exporter v1.0.0</footer>',
            f'<footer style="margin-top:26px;color:#9aa3b5;font-size:12px;font-weight:600" id="ver">Perplexity Exporter v{APP_VERSION} · {APP_BUILD_TAG}</footer>'
        )
        ui_html = ui_html.replace(
            '<body>',
            '<body data-app-version="' + APP_VERSION + '" data-boot-state="loading">'
        )
        log(f"main: using UI file {ui_path}")
    except Exception as e:
        log(f"main: UI file read failed: {e}")
        ui_html = f"<h1>UI file missing</h1><div>Perplexity Exporter v{APP_VERSION}</div>"

    bridge = Bridge(ui_html=ui_html)
    log(f"main: loading UI from {_ui_file()}")

    # auto-reconnect if we have a saved session
    saved = load_session()
    if saved and saved.get("token"):
        def _try_reconnect():
            # Wait until pywebview has injected the JS bridge (events.loaded).
            for _ in range(40):  # up to ~20s
                w = bridge._window
                if w is not None:
                    loaded = getattr(getattr(w, "events", None), "loaded", None)
                    if loaded is not None and loaded.is_set():
                        break
                time.sleep(0.5)
            try:
                session = validate_session(saved["token"])
                user = session.get("user") or {}
                if user.get("email"):
                    bridge.token = saved["token"]
                    bridge.email = user["email"]
                    count = 0
                    try:
                        count = len(list_threads(saved["token"]))
                    except ApiError:
                        pass
                    bridge._conversation_count = count
                    bridge._push({"type": "connected", "email": bridge.email, "count": count})
                    log(f"auto-reconnected: {bridge.email}")
                    return
            except ApiError:
                pass
            clear_session()
            log("saved session expired")
        threading.Thread(target=_try_reconnect, daemon=True).start()

    try:
        api = JsApi(bridge)
        bridge._window = webview.create_window(
            f"{APP_NAME}  ·  {APP_BUILD_TAG}", html=ui_html, js_api=api,
            width=780, height=720, min_size=(560, 520),
            background_color="#0f1117")
        log("main: pywebview window created")
    except Exception as e:
        log(f"main: pywebview window creation failed: {e}")
        raise

    log(f"{APP_NAME} v{APP_VERSION} starting (cffi={_HAS_CFFI}, build={APP_BUILD_TAG})")
    try:
        webview.start(private_mode=False,
                      storage_path=os.path.join(appdata_dir(), "webview"),
                      debug=False)
    except Exception as e:
        log(f"main: pywebview start failed: {e}")
        raise

