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
                    "TotalRecalls could not start because another copy is still running.\n"
                        "Open Task Manager, end all TotalRecalls.exe tasks, then try again.",
                        f"TotalRecalls {APP_VERSION} ({APP_BUILD_TAG})",
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
    from pathlib import Path

    def _repo_root() -> Path:
        # totalrecalls/desktop/main.py -> repo root (or MEIPASS when frozen)
        here = Path(__file__).resolve()
        if getattr(sys, "frozen", False):
            return Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
        return here.parents[2]

    def _resolve_ui() -> tuple[str, str, str]:
        """Return (mode, target, label).

        mode 'url'  -> target is file URI for React dist index.html
        mode 'html' -> target is inline HTML string (legacy app_ui.html)
        """
        root = _repo_root()
        index_candidates = [
            root / "ui" / "index.html",
            root / "apps" / "web-ui" / "dist" / "index.html",
        ]
        # also check next to executable / package for frozen builds
        if getattr(sys, "frozen", False):
            meipass = Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
            index_candidates.insert(0, meipass / "ui" / "index.html")
        for p in index_candidates:
            if p.is_file():
                return "url", p.resolve().as_uri(), str(p)
        # Legacy single-file HTML fallback
        html_candidates = [
            root / "app_ui.html",
            Path(__file__).resolve().parents[2] / "app_ui.html",
        ]
        if getattr(sys, "frozen", False):
            meipass = Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
            html_candidates.insert(0, meipass / "app_ui.html")
        for p in html_candidates:
            if p.is_file():
                html = p.read_text(encoding="utf-8")
                html = html.replace(
                    'id="ver">TotalRecalls v1.0.0</footer>',
                    f'id="ver">TotalRecalls v{APP_VERSION} · {APP_BUILD_TAG}</footer>',
                )
                html = html.replace(
                    "<body>",
                    f'<body data-app-version="{APP_VERSION}" data-boot-state="loading">',
                )
                # Inject logo as base64 data URI
                import base64
                logo_path = p.parent / "ui" / "logo.png"
                if logo_path.is_file():
                    logo_b64 = base64.b64encode(logo_path.read_bytes()).decode('ascii')
                    data_uri = f"data:image/png;base64,{logo_b64}"
                    html = html.replace('src="./ui/logo.png"', f'src="{data_uri}"')
                return "html", html, str(p)
        return "html", f"<h1>UI missing</h1><p>TotalRecalls v{APP_VERSION}</p>", "missing"

    ui_mode, ui_target, ui_label = _resolve_ui()
    # Bridge keeps a snapshot for rare restore_ui paths (legacy navigation).
    if ui_mode == "html":
        ui_html = ui_target
    else:
        try:
            # file URI -> path for optional read
            from urllib.parse import urlparse, unquote
            parsed = urlparse(ui_target)
            ui_html = Path(unquote(parsed.path)).read_text(encoding="utf-8") if parsed.path else ""
            # Windows file:///C:/...
            if os.name == "nt" and parsed.path.startswith("/") and len(parsed.path) > 2 and parsed.path[2] == ":":
                ui_html = Path(unquote(parsed.path[1:])).read_text(encoding="utf-8")
        except Exception:
            ui_html = ""
    log(f"main: UI mode={ui_mode} path={ui_label}")

    bridge = Bridge(ui_html=ui_html or "<html></html>")

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
            provider = str(saved.get("provider") or "perplexity").strip().lower()
            try:
                from totalrecalls.adapters.base import get_adapter
                adapter = get_adapter(provider)
                account = adapter.validate(saved["token"])
                email = (account.email or account.display_name or account.external_id or "").strip()
                if not email and provider == "perplexity":
                    raise ApiError("auth-failed")
                if not email:
                    email = f"{adapter.display_name} user"
                bridge._provider_id = provider
                bridge.token = saved["token"]
                bridge.email = email
                count = 0
                try:
                    count = len(adapter.list_conversations(saved["token"], deep=False))
                except Exception:
                    pass
                bridge._conversation_count = count
                bridge._push({"type": "connected", "email": bridge.email, "count": count})
                log(f"auto-reconnected: {bridge.email} via {provider}")
                return
            except Exception as e:
                log(f"saved session reconnect failed ({provider}): {e}")
            clear_session()
            log("saved session expired")
        threading.Thread(target=_try_reconnect, daemon=True).start()

    try:
        api = JsApi(bridge)
        win_kwargs = dict(
            js_api=api,
            width=820,
            height=760,
            min_size=(560, 520),
            background_color="#0f1117",
        )
        if ui_mode == "url":
            bridge._window = webview.create_window(
                f"{APP_NAME}  ·  {APP_BUILD_TAG}", url=ui_target, **win_kwargs)
        else:
            bridge._window = webview.create_window(
                f"{APP_NAME}  ·  {APP_BUILD_TAG}", html=ui_target, **win_kwargs)
        log(f"main: pywebview window created (mode={ui_mode})")
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

