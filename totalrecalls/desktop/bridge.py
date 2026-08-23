"""Desktop Bridge: login window, export worker, UI state push."""

from __future__ import annotations

import json
import os
import threading
import time
import traceback

from totalrecalls import APP_VERSION, APP_BUILD_TAG
from totalrecalls.core.paths import (
    appdata_dir, log, save_session, load_session, clear_session,
    kill_other_exporter_processes,
)
from totalrecalls.core.errors import friendly_error
from totalrecalls.core.export_fs import (
    HOME_SPACE_NAME, load_uuid_index, save_uuid_index,
    find_existing_thread_folder, entry_stats, thread_abs_folder,
    thread_rel_path, space_label_from_collection, write_export_indexes,
)
from totalrecalls.adapters.perplexity.http import ApiError
from totalrecalls.adapters.perplexity.auth import (
    extract_session_token_from_cookie_header,
    extract_session_token_from_cookie_records,
    extract_session_token_from_cdp_json,
    validate_session,
)
from totalrecalls.adapters.perplexity.discover import list_threads
from totalrecalls.adapters.perplexity.thread import get_thread, extract_entry, render_markdown
from totalrecalls.adapters.base import get_adapter
from totalrecalls.core.unified_export import export_via_adapter
from totalrecalls.adapters.perplexity.adapter import PerplexityAdapter

class Bridge:
    """Called from the web UI via pywebview's js_api bridge.

    Design note: NO second/hidden windows — the main window itself navigates
    to perplexity.ai for login, then load_html() brings the UI back. Hidden
    windows caused GUI-thread hangs in pywebview 6.2.1 (show()/load_url()
    wait on events + synchronous Invoke while WebView2 initializes).
    """

    def __init__(self, ui_html: str = ""):
        self.token: str | None = None
        self.email: str | None = None
        self._window = None
        self._ui_html = ui_html
        self._stop_login = threading.Event()
        self._login_thread: threading.Thread | None = None
        self._login_form = None
        self._export_thread: threading.Thread | None = None
        self._connecting = False
        self._default_folder = os.path.join(os.path.expanduser("~"), "TotalRecalls-export")
        self._LOGIN_TIMEOUT = 8 * 60  # seconds
        self._login_completion_pending = False
        self._conversation_count = 0
        self._provider_id = "perplexity"
        self._connected_at: float | None = None  # monotonic ts of connection established
        self._first_download_at: float | None = None

    # -- helpers ------------------------------------------------------------

    def _push(self, payload: dict):
        if self._window is None:
            log(f"push dropped: window is None for {payload.get('type')}")
            return

        def _dispatch():
            try:
                # Wait briefly for pywebview injection (loaded). Do NOT hang 20s
                # inside evaluate_js's decorator if the UI is mid-init — poll instead.
                loaded = getattr(getattr(self._window, "events", None), "loaded", None)
                if loaded is not None:
                    if not loaded.wait(timeout=8):
                        log(f"push deferred/dropped (UI not loaded yet) for {payload.get('type')}")
                        # stash connected/disconnected so boot can pick up via getState
                        return
                # Prefer run_js (before_load-gated, lighter) for fire-and-forget UI pushes
                script = f"window.__push && window.__push({json.dumps(payload)})"
                try:
                    self._window.evaluate_js(script)
                except Exception:
                    # last resort: run_js without return value
                    self._window.run_js(script)
                log(f"push delivered: {payload.get('type')}")
            except Exception as e:
                log(f"push failed for {payload.get('type')}: {e}")

        try:
            threading.Thread(target=_dispatch, daemon=True).start()
        except Exception as e:
            log(f"push thread launch failed for {payload.get('type')}: {e}")

    def _restore_ui(self):
        """Navigate back to the local UI (after login on perplexity.ai)."""
        if self._window is None or not self._ui_html:
            return
        try:
            self._window.load_html(self._ui_html)
        except Exception as e:
            log(f"restore UI failed: {e}")

    # -- UI entry points (called from JavaScript) ---------------------------

    def _note_first_download(self):
        """Troubleshooting timer: seconds between connection-established and the
        first conversation download. Emitted once to log + UI."""
        if getattr(self, "_first_download_at", None) is not None:
            return  # already recorded
        self._first_download_at = time.monotonic()
        started = getattr(self, "_connected_at", None)
        if started is None:
            return
        elapsed = self._first_download_at - started
        mins, secs = divmod(int(elapsed), 60)
        label = f"{mins}m {secs:02d}s" if mins else f"{secs:02d}s"
        log(f"timer: connection -> first download = {label} ({elapsed:.1f}s)")
        self._push({"type": "timer", "label": "connect->first download", "seconds": round(elapsed, 1)})

    def ping(self):
        return "pong"

    def getState(self):
        log(f"bridge: getState (connected={bool(self.token)}, connecting={self._connecting})")
        return {
            "version": APP_VERSION,
            "build": APP_BUILD_TAG,
            "folder": self._default_folder,
            "connected": bool(self.token),
            "email": self.email or "",
            "connecting": bool(self._connecting),
            "count": self._conversation_count,
            "provider": getattr(self, "_provider_id", "perplexity"),
        }

    def listProviders(self):
        """UI provider picker — available flags track registry + product roadmap."""
        known = [
            {"id": "perplexity", "name": "Perplexity", "available": True},
            {"id": "chatgpt", "name": "ChatGPT", "available": True},
            {"id": "claude", "name": "Claude", "available": True},
            {"id": "gemini", "name": "Gemini", "available": True},
            {"id": "grok", "name": "Grok", "available": True},
        ]
        try:
            from totalrecalls.adapters.base import list_provider_ids
            live = set(list_provider_ids())
            for row in known:
                if row["id"] in live:
                    row["available"] = True
                    row.pop("note", None)
        except Exception:
            pass
        return known


    def setProvider(self, provider_id: str = "perplexity"):
        """Select active provider for login/export (UI dropdown)."""
        pid = (provider_id or "perplexity").strip().lower()
        try:
            get_adapter(pid)
        except Exception:
            self._push({"type": "error", "message": f"Unknown or unavailable provider: {provider_id}"})
            return {"ok": False, "provider": getattr(self, "_provider_id", "perplexity")}
        # Switching provider clears session (credentials are provider-specific)
        cleared = False
        if pid != getattr(self, "_provider_id", None) and self.token:
            self.token = None
            self.email = None
            self._conversation_count = 0
            clear_session()
            cleared = True
            self._push({"type": "disconnected"})
            self._push({"type": "clear_results"})  # Clear old results from UI
        self._provider_id = pid
        # Keep UI in sync even when host state poll is slow
        self._push({
            "type": "provider",
            "provider": pid,
            "cleared": cleared,
            "connected": bool(self.token),
        })
        log(f"provider set: {pid} (cleared={cleared})")
        return {"ok": True, "provider": pid, "cleared": cleared}


    def connect(self):
        log("bridge: connect() called from UI")
        if self.token or self._connecting:
            log(f"bridge: connect() ignored (token={bool(self.token)}, connecting={self._connecting})")
            return
        try:
            self._push({"type": "log", "line": "Received login request from UI"})
        except Exception:
            pass
        self._connecting = True
        self._login_completion_pending = False
        self._stop_login.clear()
        # Clear cached WebView2 session data to force a fresh sign-in window
        # (supports users with multiple accounts at the same provider)
        provider = getattr(self, "_provider_id", "perplexity") or "perplexity"
        udf = os.path.join(appdata_dir(), f"login-webview-{provider}")
        try:
            import shutil
            if os.path.exists(udf):
                log(f"login: clearing cached WebView2 data for {provider}")
                shutil.rmtree(udf, ignore_errors=True)
        except Exception as e:
            log(f"login: could not clear WebView2 cache ({e})")
        # Show spinner only — do not reset first (avoids blue-button flash).
        self._push({"type": "waiting_login"})

        provider = getattr(self, "_provider_id", "perplexity") or "perplexity"
        if provider == "perplexity":
            log("login: starting embedded WebView2 login for Perplexity (CDP capture)")
            self._start_embedded_login()
        elif provider == "chatgpt":
            log("login: starting embedded WebView2 login for ChatGPT")
            self._start_chatgpt_embedded_login()
        elif provider == "claude":
            log("login: starting embedded WebView2 login for Claude")
            self._start_claude_embedded_login()
        elif provider == "grok":
            log("login: starting embedded WebView2 login for Grok")
            self._start_generic_cookie_login(
                title="Sign in to Grok",
                start_url="https://grok.com/",
                host_substr="grok.com",
                profile_suffix="grok",
                prefer_bearer=True,
                cookie_names=("sso", "sso_rw"),
            )
        elif provider == "gemini":
            log("login: starting embedded WebView2 login for Gemini")
            self._start_generic_cookie_login(
                title="Sign in to Gemini",
                start_url="https://gemini.google.com/app",
                host_substr="gemini.google.com",
                profile_suffix="gemini",
                prefer_bearer=False,
                cookie_filter="__Secure-1PSID",
            )
        else:
            self._connecting = False
            self._push({"type": "error",
                        "message": f"Embedded login for {provider} is not ready yet. "
                                   "Use the session-token / cookie paste option."})
            self._push({"type": "login_cancelled"})

    def _start_embedded_login(self):
        """Run the WinForms/WebView2 login form on a true STA thread.

        Python's threading.Thread is MTA; WinForms + WebView2 require STA.
        Use System.Threading.Thread with ApartmentState.STA (pythonnet).
        """
        def runner():
            try:
                self._login_window_flow()
            except Exception as e:
                log(f"login: embedded flow crashed: {e}\n{traceback.format_exc()}")
                self._connecting = False
                self._push({"type": "error",
                            "message": "The sign-in window failed to start. "
                                       "Please try again, or use the session-cookie option."})
                self._push({"type": "login_cancelled"})

        # Prefer CLR STA thread
        try:
            try:
                import clr  # noqa: F401
            except Exception:
                os.environ["PYTHONNET_RUNTIME"] = "coreclr"
                import clr  # noqa: F401
            from System.Threading import ApartmentState, Thread as NetThread, ThreadStart
            t = NetThread(ThreadStart(runner))
            t.SetApartmentState(ApartmentState.STA)
            t.IsBackground = True
            t.Start()
            self._login_clr_thread = t
            log("login: STA CLR thread started")
            return
        except Exception as e:
            log(f"login: STA CLR thread unavailable ({e}); falling back to Python thread")

        self._login_thread = threading.Thread(target=runner, daemon=True)
        self._login_thread.start()

    def _browser_login_flow(self):
        """Open Perplexity in the system browser and wait for a usable session."""
        log("login: waiting for browser sign-in token")
        try:
            opened = webbrowser.open("https://www.perplexity.ai/")
            log(f"login: opened default browser to Perplexity: {opened}")
        except Exception as e:
            log(f"login: browser open failed: {e}")

        self._push({"type": "log", "line": "Please complete the sign-in in your browser."})

        deadline = time.time() + self._LOGIN_TIMEOUT
        while time.time() < deadline:
            if self._stop_login.is_set():
                log("login: browser flow cancelled")
                self._connecting = False
                self._push({"type": "login_cancelled"})
                return

            token = consume_signin_callback()
            if token:
                self._accept_token(token, False)
                return
            token = detect_session_token_from_browser_store()
            if token:
                self._accept_token(token, False)
                return
            time.sleep(2)

        self._connecting = False
        self._push({"type": "error",
                    "message": "We could not confirm a Perplexity session after opening your browser. "
                               "Please complete the sign-in and try again."})
        self._push({"type": "login_cancelled"})

    def cancelLogin(self):
        log("bridge: cancelLogin() called from UI")
        self._stop_login.set()
        self._login_completion_pending = False
        self._connecting = False
        form = getattr(self, "_login_form", None)
        if form is not None:
            try:
                from System import Action
                form.BeginInvoke(Action(form.Close))
            except Exception:
                pass
        self._push({"type": "reset_login_ui"})
        self._push({"type": "login_cancelled"})

    def pasteCookie(self, token: str):
        log("bridge: pasteCookie() called from UI")
        token = (token or "").strip()
        if not token:
            return
        self._push({"type": "waiting_login"})
        threading.Thread(target=self._accept_token, args=(token, False), daemon=True).start()

    def chooseFolder(self):
        log("bridge: chooseFolder() called from UI")
        try:
            import webview
            result = self._window.create_file_dialog(webview.FOLDER_DIALOG,
                                                    directory=self._default_folder)
            if result and result[0]:
                self._default_folder = result[0]
                return self._default_folder
        except Exception as e:
            log(f"folder dialog error: {e}")
        return self._default_folder

    def chooseTakeoutPath(self):
        """Folder or JSON file picker for Gemini Takeout imports."""
        log("bridge: chooseTakeoutPath() called from UI")
        if self._window is None:
            return ""
        try:
            try:
                import webview as _wv
                folder_dlg = getattr(_wv, "FOLDER_DIALOG", "FOLDER_DIALOG")
                open_dlg = getattr(_wv, "OPEN_DIALOG", "OPEN_DIALOG")
            except Exception:
                # Tests / headless CI may not have pywebview installed
                folder_dlg = "FOLDER_DIALOG"
                open_dlg = "OPEN_DIALOG"
            # Prefer folder dialog first (Takeout root)
            result = self._window.create_file_dialog(
                folder_dlg,
                directory=os.path.expanduser("~"),
            )
            if result and result[0]:
                path = result[0]
                self._push({"type": "takeout_path", "path": path})
                return path
            # Fallback: allow picking a JSON file
            result = self._window.create_file_dialog(
                open_dlg,
                allow_multiple=False,
                file_types=("JSON Files (*.json)", "All files (*.*)"),
                directory=os.path.expanduser("~"),
            )
            if result and result[0]:
                path = result[0]
                self._push({"type": "takeout_path", "path": path})
                return path
        except Exception as e:
            log(f"takeout path dialog error: {e}")
        return ""


    def startExport(self, refresh: bool = False):
        log("bridge: startExport() called from UI")
        if not self.token:
            self._push({"type": "error", "message": "Please log in to a provider first."})
            return
        if self._export_thread and self._export_thread.is_alive():
            return
        # Re-arm the connect->first-download timer for this run.
        self._first_download_at = None
        self._export_thread = threading.Thread(target=self._export_worker,
                                               args=(bool(refresh),), daemon=True)
        self._export_thread.start()

    def openFolder(self):
        log("bridge: openFolder() called from UI")
        try:
            os.startfile(self._default_folder)  # type: ignore[attr-defined]
        except Exception as e:
            log(f"open folder error: {e}")

    def disconnect(self):
        log("bridge: disconnect() called from UI")
        clear_session()
        self.token = None
        self.email = None
        self._conversation_count = 0
        self._connecting = False
        self._push({"type": "clear_results"})  # Clear stale results
        self._push({"type": "disconnected"})
        log("disconnected")

    def quitApp(self):
        try:
            self._window.destroy()
        except Exception:
            pass

    # -- login flow ---------------------------------------------------------




    def _start_generic_cookie_login(self, *, title: str, start_url: str, host_substr: str,
                                    profile_suffix: str, prefer_bearer: bool = False,
                                    cookie_filter: str | None = None,
                                    cookie_names: tuple | None = None):
        """STA WebView2 login that captures Cookie header and optional Bearer tokens.

        cookie_filter: optional cookie name to require (e.g. '__Secure-1PSID' for
        Gemini).  When set, the flow waits for this specific cookie to appear.
        cookie_names: optional set of cookie names to poll for via CookieManager
        every tick (works even when request headers don't carry a Cookie header).
        """
        # Clear cached WebView2 data to force a fresh sign-in (supports
        # multi-account users who need to pick a different account)
        udf = os.path.join(appdata_dir(), f"login-webview-{profile_suffix}")
        try:
            import shutil
            if os.path.exists(udf):
                log(f"login: clearing cached WebView2 data at {udf}")
                shutil.rmtree(udf, ignore_errors=True)
        except Exception as e:
            log(f"login: could not clear WebView2 cache ({e})")
        if os.path.exists(udf):
            # Profile folder is locked (e.g. orphaned WebView2 processes from a
            # previous crash). A locked profile makes WebView2 init hang with a
            # blank window — fall back to a unique folder for this attempt.
            fallback = f"{udf}-{os.getpid()}"
            log(f"login: profile folder still locked; using temporary folder {os.path.basename(fallback)}")
            udf = fallback
        try:
            import clr
            from System.Threading import Thread, ThreadStart, ApartmentState
            def runner():
                try:
                    self._generic_cookie_login_flow(title, start_url, host_substr, profile_suffix, prefer_bearer, cookie_filter, udf, cookie_names)
                except Exception as e:
                    # Without this wrapper an exception on the CLR thread is
                    # unobserved and kills the whole process silently.
                    log(f"generic login flow crashed: {e}\n{traceback.format_exc()}")
                    self._connecting = False
                    self._push({"type": "error", "message": f"{title} embedded login failed to start. Try again, or paste a session token/cookie instead."})
                    self._push({"type": "login_cancelled"})
            th = Thread(ThreadStart(runner))
            th.SetApartmentState(ApartmentState.STA)
            th.IsBackground = True
            self._login_clr_thread = th
            log(f"login: STA CLR thread started ({profile_suffix})")
            th.Start()
        except Exception as e:
            log(f"generic login STA failed: {e}")
            self._connecting = False
            self._push({"type": "error", "message": f"{title} embedded login unavailable. Paste a session token/cookie instead."})
            self._push({"type": "login_cancelled"})

    def _generic_cookie_login_flow(self, title, start_url, host_substr, profile_suffix, prefer_bearer, cookie_filter=None, udf=None, cookie_names=None):
        if udf is None:
            udf = os.path.join(appdata_dir(), f"login-webview-{profile_suffix}")
        log(f"{profile_suffix} login: flow starting (profile={os.path.basename(udf)})")
        try:
            import clr
        except Exception:
            import os as _os
            _os.environ["PYTHONNET_RUNTIME"] = "coreclr"
            import clr
        try:
            from webview.util import interop_dll_path
            clr.AddReference("System.Windows.Forms")
            clr.AddReference("System.Drawing")
            clr.AddReference(interop_dll_path("Microsoft.Web.WebView2.Core.dll"))
            clr.AddReference(interop_dll_path("Microsoft.Web.WebView2.WinForms.dll"))
            from System.Windows.Forms import Application, DockStyle, Form, FormStartPosition, Label
            from System import Action
            from System.Drawing import Size
            from Microsoft.Web.WebView2.Core import CoreWebView2WebResourceContext
            from Microsoft.Web.WebView2.WinForms import CoreWebView2CreationProperties, WebView2
            from System.Windows.Forms import Timer as WinTimer
        except Exception as e:
            log(f"generic login WebView2 load failed: {e}")
            self._connecting = False
            self._push({"type": "error", "message": "Embedded login unavailable. Paste token/cookie instead."})
            self._push({"type": "login_cancelled"})
            return

        form = Form(); form.Text = title; form.Size = Size(980, 760); form.TopMost = True
        form.StartPosition = FormStartPosition.CenterScreen
        from System.Windows.Forms import Button as WinButton
        status = Label(); status.Text = f"  Loading {title}…"; status.Dock = DockStyle.Top; status.Height = 28
        # Paste token button — an alternative to the embedded WebView2 login
        paste_panel = WinButton(); paste_panel.Text = "Can't sign in? Paste session token/cookie"; paste_panel.Height = 32
        paste_panel.Dock = DockStyle.Bottom
        paste_panel.Click += lambda s, e: _show_paste_dialog(profile_suffix, title, finished, closed, timer)
        wv = WebView2(); wv.Dock = DockStyle.Fill
        try:
            props = CoreWebView2CreationProperties()
            props.UserDataFolder = udf
            wv.CreationProperties = props
        except Exception:
            pass
        form.Controls.Add(wv); form.Controls.Add(status); form.Controls.Add(paste_panel)
        closed = threading.Event(); finished = {"done": False}
        self._login_form = form

        def _show_paste_dialog(suffix, dlg_title, finished_dict, closed_evt, timer_obj):
            """Show a simple dialog allowing the user to paste a session token/cookie."""
            try:
                from System.Windows.Forms import Form as DForm, Label as DLabel, Button as DBtn, TextBox as DText, DockStyle as DDock, FormStartPosition as DStart, Size as DSize
                from System.Drawing import Size as DSize2
                dlg = DForm()
                dlg.Text = "Paste session token — " + dlg_title
                dlg.Size = DSize2(600, 200)
                dlg.StartPosition = DStart.CenterScreen
                dlg.TopMost = True
                lbl = DLabel()
                lbl.Text = "Paste your session token or cookie here, then click OK:"
                lbl.Dock = DDock.Top
                lbl.Height = 26
                txt = DText()
                txt.Multiline = True
                txt.Dock = DDock.Fill
                txt.ScrollBars = 2  # Vertical
                btn_panel = DForm()  # placeholder
                btn_ok = DBtn(); btn_ok.Text = "OK"; btn_ok.DialogResult = 1
                btn_cancel = DBtn(); btn_cancel.Text = "Cancel"; btn_cancel.DialogResult = 2
                from System.Windows.Forms import FlowLayoutPanel
                flp = FlowLayoutPanel(); flp.Dock = DDock.Bottom; flp.Height = 40
                flp.Controls.Add(btn_ok); flp.Controls.Add(btn_cancel)
                dlg.Controls.Add(txt); dlg.Controls.Add(flp); dlg.Controls.Add(lbl)
                dlg.AcceptButton = btn_ok
                dlg.CancelButton = btn_cancel
                result = dlg.ShowDialog()
                if result == 1:
                    val = (txt.Text or "").strip()
                    if val:
                        finished_dict["done"] = True
                        try: timer_obj.Stop()
                        except Exception: pass
                        closed_evt.set()
                        log(f"{suffix} login: pasted token ({len(val)} chars)")
                        safe_close()
                        threading.Thread(target=self._accept_token, args=(val, False), daemon=True).start()
            except Exception as e:
                log(f"paste dialog error: {e}")

        def safe_close():
            try:
                if form.IsHandleCreated: form.BeginInvoke(Action(form.Close))
                else: form.Close()
            except Exception:
                pass

        def finish(token: str, source: str):
            if finished["done"] or not token: return
            finished["done"] = True
            try: timer.Stop()
            except Exception: pass
            closed.set()
            log(f"{profile_suffix} login: captured via {source}")
            safe_close()
            threading.Thread(target=self._accept_token, args=(token, False), daemon=True).start()

        def on_closing(sender, e):
            closed.set()
            if not self.token and not finished["done"]:
                self._connecting = False
                self._push({"type": "login_cancelled"})
        form.FormClosing += on_closing

        def on_req(sender, args):
            try:
                if closed.is_set() or finished["done"]: return
                req = getattr(args, "Request", None)
                if req is None: return
                uri = str(getattr(req, "Uri", "") or "").lower()
                # For Gemini, also capture cookies from google.com / accounts.google.com
                # (Google auth redirects through these domains before landing on gemini.google.com)
                if (host_substr.lower() not in uri
                        and "x.com" not in uri
                        and "google.com" not in uri
                        and "googleapis.com" not in uri): return
                headers = getattr(req, "Headers", None)
                if headers is None: return
                if prefer_bearer:
                    try: auth = headers.GetHeader("Authorization")
                    except Exception: auth = None
                    if auth and "bearer" in str(auth).lower():
                        tok = str(auth).split(None, 1)[-1].strip()
                        if tok.startswith("eyJ"):
                            if form.IsHandleCreated:
                                form.BeginInvoke(Action(lambda: finish(tok, "Bearer")))
                            else:
                                finish(tok, "Bearer")
                            return
                try: cookie_header = headers.GetHeader("Cookie")
                except Exception: cookie_header = None
                if cookie_header and len(cookie_header) > 20:
                    # If a cookie_filter is specified, make sure the required cookie is present
                    if cookie_filter and cookie_filter not in cookie_header:
                        # Still intercept — the user might be in the middle of auth redirect
                        # Don't finish, just let it through (cookie might arrive on next request)
                        return
                    # Named-cookie gate (grok.com): do NOT finish on logged-out
                    # baseline cookies (grok.com sets grok_device_id instantly on
                    # any visit — capturing it "connects" with a dead credential).
                    # Require one of cookie_names, or at least one non-baseline
                    # cookie, before accepting.
                    if cookie_names:
                        _BL = {"grok_device_id", "__cf_bm", "cf_clearance", "__cfruid", "_cfuvid"}
                        try:
                            names_present = {p.split("=", 1)[0].strip() for p in cookie_header.split(";") if "=" in p}
                        except Exception:
                            names_present = set()
                        if not (names_present & set(cookie_names)) and not (names_present - _BL):
                            return
                    # For cookie-only providers: if cookie_filter is set and the cookie
                    # is present, we're done.  Otherwise accept any cookie from the host.
                    if cookie_filter or host_substr.lower() in uri:
                        if form.IsHandleCreated:
                            form.BeginInvoke(Action(lambda: finish(cookie_header, "Cookie")))
                        else:
                            finish(cookie_header, "Cookie")
            except Exception as e:
                log(f"generic login hook error: {e}")

        def on_init(sender, args):
            try:
                if not args.IsSuccess:
                    self._connecting = False
                    self._push({"type": "error", "message": "Could not start embedded login browser."})
                    self._push({"type": "login_cancelled"}); safe_close(); return
                cv = wv.CoreWebView2
                cv.AddWebResourceRequestedFilter("https://*/*", CoreWebView2WebResourceContext.All)
                cv.WebResourceRequested += on_req
                # For Gemini: use CookieManager to extract ALL session cookies
                # after navigation completes. The WebResourceRequested event
                # only captures the Cookie header from individual requests, which
                # may be incomplete (Google sets cookies on multiple domains:
                # accounts.google.com, google.com, gemini.google.com).
                def on_nav_completed(sender, args):
                    try:
                        if closed.is_set() or finished["done"]: return
                        uri = str(getattr(args, "Uri", "") or "").lower()
                        if cookie_filter and cookie_filter:
                            # For cookie-filtered providers (Gemini), extract ALL
                            # cookies via the CookieManager when we reach the target host
                            if host_substr.lower() in uri:
                                cm = cv.CookieManager
                                if cm:
                                    cookies = cm.GetCookies(uri)
                                    parts = []
                                    seen_names = set()
                                    for c in cookies:
                                        try:
                                            name = str(getattr(c, "Name", ""))
                                            value = str(getattr(c, "Value", ""))
                                            if name and value and name not in seen_names:
                                                seen_names.add(name)
                                                parts.append(f"{name}={value}")
                                        except Exception:
                                            pass
                                    
                                    # Also pull cookies from google.com / accounts.google.com
                                    # which Set-Cookie on the .google.com parent domain
                                    # these are needed for clients6.google.com RPC calls
                                    for extra_uri in ["https://www.google.com/", "https://accounts.google.com/"]:
                                        try:
                                            extra_cookies = cm.GetCookies(extra_uri)
                                            for c in extra_cookies:
                                                try:
                                                    name = str(getattr(c, "Name", ""))
                                                    value = str(getattr(c, "Value", ""))
                                                    if name and value and name not in seen_names:
                                                        seen_names.add(name)
                                                        parts.append(f"{name}={value}")
                                                except Exception:
                                                    pass
                                        except Exception:
                                            pass
                                    
                                    if parts:
                                        cookie_str = "; ".join(parts)
                                        if cookie_filter in cookie_str:
                                            log(f"{profile_suffix} login: captured all cookies via CookieManager ({len(parts)} cookies)")
                                            if form.IsHandleCreated:
                                                form.BeginInvoke(Action(lambda: finish(cookie_str, "CookieManager")))
                                            else:
                                                finish(cookie_str, "CookieManager")
                    except Exception as e:
                        log(f"{profile_suffix} nav_completed hook error: {e}")
                cv.NavigationCompleted += on_nav_completed
                cv.Navigate(start_url)
                status.Text = f"  Sign in, then continue in this window…"
            except Exception as e:
                log(f"generic login init error: {e}")

        wv.CoreWebView2InitializationCompleted += on_init
        timer = WinTimer(); timer.Interval = 2500
        # Cookies that exist even when logged OUT — their presence alone does
        # not mean login succeeded.  Anything else on the host = session cookie.
        _BASELINE_COOKIES = {"grok_device_id", "__cf_bm", "cf_clearance", "__cfruid", "_cfuvid"}
        def on_tick(sender, e):
            if closed.is_set() or finished["done"] or self.token: return
            if self._stop_login.is_set():
                safe_close(); return
            # Poll the CookieManager directly — works even when intercepted
            # requests don't expose a readable Cookie header (e.g. grok.com).
            if cookie_names:
                try:
                    cv = wv.CoreWebView2
                    if cv is None: return
                    cm = cv.CookieManager
                    if cm is None: return
                    cookies = cm.GetCookies(start_url)
                    parts = []
                    names_seen = set()
                    for c in cookies:
                        try:
                            nm = str(getattr(c, "Name", ""))
                            val = str(getattr(c, "Value", ""))
                            if nm and val and nm not in names_seen:
                                names_seen.add(nm)
                                parts.append(f"{nm}={val}")
                        except Exception:
                            pass
                    if not parts: return
                    hit = [n for n in names_seen if n in cookie_names]
                    extra = [n for n in names_seen if n not in _BASELINE_COOKIES]
                    if hit or extra:
                        cookie_str = "; ".join(parts)
                        log(f"{profile_suffix} login: cookie poll captured {len(parts)} cookies (names: {sorted(names_seen)})")
                        finish(cookie_str, "CookiePoll")
                except Exception as ex:
                    log(f"{profile_suffix} cookie poll error: {ex}")
        timer.Tick += on_tick
        try:
            wv.EnsureCoreWebView2Async(None)
        except Exception as e:
            log(f"generic ensure error: {e}")
            self._connecting = False
            self._push({"type": "error", "message": "Could not start embedded login browser."})
            self._push({"type": "login_cancelled"})
            return
        timer.Start()
        try:
            form.Show()
            form.BringToFront()
            form.Activate()
        except Exception:
            pass
        Application.Run(form)
        try: timer.Stop()
        except Exception: pass
        self._login_form = None
        log(f"{profile_suffix} login: window closed")

    def _start_claude_embedded_login(self):
        """Open claude.ai; capture sessionKey cookie for ClaudeAdapter."""
        try:
            import clr
            from System.Threading import Thread, ThreadStart, ApartmentState
            def runner():
                self._claude_login_window_flow()
            t = Thread(ThreadStart(runner))
            t.SetApartmentState(ApartmentState.STA)
            t.IsBackground = True
            self._login_clr_thread = t
            log("login: STA CLR thread started (claude)")
            t.Start()
        except Exception as e:
            log(f"claude login STA failed: {e}")
            self._connecting = False
            self._push({"type": "error",
                        "message": "Embedded Claude login unavailable. Paste your sessionKey cookie value instead."})
            self._push({"type": "login_cancelled"})

    def _claude_login_window_flow(self):
        try:
            import clr
        except Exception:
            import os as _os
            _os.environ["PYTHONNET_RUNTIME"] = "coreclr"
            import clr
        try:
            from webview.util import interop_dll_path
            clr.AddReference("System.Windows.Forms")
            clr.AddReference("System.Drawing")
            clr.AddReference(interop_dll_path("Microsoft.Web.WebView2.Core.dll"))
            clr.AddReference(interop_dll_path("Microsoft.Web.WebView2.WinForms.dll"))
            from System.Windows.Forms import Application, DockStyle, Form, FormStartPosition, Label
            from System import Action
            from System.Drawing import Color, Size
            from Microsoft.Web.WebView2.Core import CoreWebView2WebResourceContext
            from Microsoft.Web.WebView2.WinForms import CoreWebView2CreationProperties, WebView2
            from System.Windows.Forms import Timer as WinTimer
        except Exception as e:
            log(f"claude login: WebView2 load failed: {e}")
            self._connecting = False
            self._push({"type": "error", "message": "Embedded Claude login unavailable. Paste sessionKey instead."})
            self._push({"type": "login_cancelled"})
            return

        form = Form()
        form.Text = "Sign in to Claude"
        form.Size = Size(980, 760); form.TopMost = True
        form.StartPosition = FormStartPosition.CenterScreen
        status = Label(); status.Text = "  Loading Claude…"; status.Dock = DockStyle.Top; status.Height = 28
        wv = WebView2(); wv.Dock = DockStyle.Fill
        try:
            props = CoreWebView2CreationProperties()
            props.UserDataFolder = os.path.join(appdata_dir(), "login-webview-claude")
            wv.CreationProperties = props
        except Exception:
            pass
        form.Controls.Add(wv); form.Controls.Add(status)
        closed = threading.Event(); finished = {"done": False}
        self._login_form = form

        def safe_close():
            try:
                if form.IsHandleCreated: form.BeginInvoke(Action(form.Close))
                else: form.Close()
            except Exception: pass

        def finish(token: str, source: str):
            if finished["done"] or not token: return
            finished["done"] = True
            try: timer.Stop()
            except Exception: pass
            closed.set()
            log(f"claude login: captured via {source}")
            safe_close()
            threading.Thread(target=self._accept_token, args=(token, False), daemon=True).start()

        def on_closing(sender, e):
            closed.set()
            if not self.token and not finished["done"]:
                self._connecting = False
                self._push({"type": "login_cancelled"})
        form.FormClosing += on_closing

        def on_req(sender, args):
            try:
                if closed.is_set() or finished["done"]: return
                req = getattr(args, "Request", None)
                if req is None: return
                uri = str(getattr(req, "Uri", "") or "").lower()
                if "claude.ai" not in uri: return
                headers = getattr(req, "Headers", None)
                if headers is None: return
                try: cookie_header = headers.GetHeader("Cookie")
                except Exception: cookie_header = None
                if cookie_header and "sessionKey=" in cookie_header:
                    if form.IsHandleCreated:
                        form.BeginInvoke(Action(lambda: finish(cookie_header, "Cookie header")))
                    else:
                        finish(cookie_header, "Cookie header")
            except Exception as e:
                log(f"claude login hook error: {e}")

        def on_init(sender, args):
            try:
                if not args.IsSuccess:
                    self._connecting = False
                    self._push({"type": "error", "message": "Could not start Claude login browser."})
                    self._push({"type": "login_cancelled"}); safe_close(); return
                cv = wv.CoreWebView2
                cv.AddWebResourceRequestedFilter("https://*.claude.ai/*", CoreWebView2WebResourceContext.All)
                cv.AddWebResourceRequestedFilter("https://claude.ai/*", CoreWebView2WebResourceContext.All)
                cv.WebResourceRequested += on_req
                cv.Navigate("https://claude.ai/")
                status.Text = "  Sign in to Claude in this window…"
            except Exception as e:
                log(f"claude login init error: {e}")

        wv.CoreWebView2InitializationCompleted += on_init
        timer = WinTimer(); timer.Interval = 2000
        def on_tick(sender, e):
            if closed.is_set() or finished["done"] or self.token: return
            if self._stop_login.is_set():
                safe_close(); return
            try:
                cv = wv.CoreWebView2
                if cv is None: return
                task = cv.CookieManager.GetCookiesAsync("https://claude.ai")
                if task.IsCompleted and not getattr(task, "IsFaulted", False):
                    parts = []
                    sk = None
                    for c in task.Result:
                        name = getattr(c, "Name", None) or getattr(c, "name", None)
                        value = getattr(c, "Value", None) or getattr(c, "value", None)
                        if name and value is not None:
                            parts.append(f"{name}={value}")
                            if name == "sessionKey" and value:
                                sk = str(value)
                    if sk:
                        finish("; ".join(parts), "CookieManager")
            except Exception:
                pass
        timer.Tick += on_tick
        try:
            wv.EnsureCoreWebView2Async(None)
        except Exception as e:
            log(f"claude ensure error: {e}")
            self._connecting = False
            self._push({"type": "error", "message": "Could not start Claude login browser."})
            self._push({"type": "login_cancelled"})
            return
        timer.Start()
        try:
            form.Show()
            form.BringToFront()
            form.Activate()
        except Exception:
            pass
        Application.Run(form)
        try: timer.Stop()
        except Exception: pass
        self._login_form = None
        log("claude login: window closed")

    def _start_chatgpt_embedded_login(self):
        """Open ChatGPT in embedded WebView2; capture access token via session cookie / Bearer."""
        self._login_thread = threading.Thread(target=self._chatgpt_login_window_flow, daemon=True)
        # Prefer CLR STA like Perplexity when available
        try:
            self._start_embedded_login_chatgpt_sta()
        except Exception as e:
            log(f"chatgpt login STA path failed, python thread fallback: {e}")
            self._login_thread.start()

    def _start_embedded_login_chatgpt_sta(self):
        import clr
        from System.Threading import Thread, ThreadStart, ApartmentState
        def runner():
            self._chatgpt_login_window_flow()
        t = Thread(ThreadStart(runner))
        t.SetApartmentState(ApartmentState.STA)
        t.IsBackground = True
        self._login_clr_thread = t
        log("login: STA CLR thread started (chatgpt)")
        t.Start()

    def _chatgpt_login_window_flow(self):
        """Native login window aimed at chatgpt.com; capture Bearer or session cookie."""
        try:
            import clr
        except Exception:
            import os as _os
            _os.environ["PYTHONNET_RUNTIME"] = "coreclr"
            import clr
        try:
            from webview.util import interop_dll_path
            clr.AddReference("System.Windows.Forms")
            clr.AddReference("System.Drawing")
            clr.AddReference(interop_dll_path("Microsoft.Web.WebView2.Core.dll"))
            clr.AddReference(interop_dll_path("Microsoft.Web.WebView2.WinForms.dll"))
            from System.Windows.Forms import Application, DockStyle, Form, FormStartPosition, Label
            from System import Action, Uri
            from System.Drawing import Color, Font, Size
            from Microsoft.Web.WebView2.Core import CoreWebView2WebResourceContext
            from Microsoft.Web.WebView2.WinForms import CoreWebView2CreationProperties, WebView2
            from System.Windows.Forms import Timer as WinTimer
        except Exception as e:
            log(f"chatgpt login: could not load WinForms/WebView2: {e}")
            self._connecting = False
            self._push({"type": "error",
                        "message": "Embedded ChatGPT login is unavailable. Paste an access token instead."})
            self._push({"type": "login_cancelled"})
            return

        form = Form()
        form.Text = "Sign in to ChatGPT"
        form.Size = Size(980, 760); form.TopMost = True
        form.StartPosition = FormStartPosition.CenterScreen
        form.MinimumSize = Size(640, 560)
        try:
            form.BackColor = Color.FromArgb(15, 17, 23)
        except Exception:
            pass
        status = Label()
        status.Text = "  Loading ChatGPT sign-in…"
        status.Dock = DockStyle.Top
        status.Height = 28
        wv = WebView2()
        wv.Dock = DockStyle.Fill
        try:
            props = CoreWebView2CreationProperties()
            props.UserDataFolder = os.path.join(appdata_dir(), "login-webview-chatgpt")
            wv.CreationProperties = props
        except Exception as e:
            log(f"chatgpt login: creation-props error: {e}")
        form.Controls.Add(wv)
        form.Controls.Add(status)
        closed = threading.Event()
        finished = {"done": False}
        self._login_form = form

        def safe_close():
            try:
                if form.IsHandleCreated:
                    form.BeginInvoke(Action(form.Close))
                else:
                    form.Close()
            except Exception as e:
                log(f"chatgpt login: safe_close error: {e}")

        def finish(token: str, source: str):
            if finished["done"] or not token:
                return
            finished["done"] = True
            try:
                timer.Stop()
            except Exception:
                pass
            closed.set()
            log(f"chatgpt login: captured credential via {source}: {token[:10]}...")
            safe_close()
            threading.Thread(target=self._accept_token, args=(token, False), daemon=True).start()

        def on_form_closing(sender, e):
            closed.set()
            if not self.token and not finished["done"] and not self._login_completion_pending:
                self._connecting = False
                self._push({"type": "login_cancelled"})
        form.FormClosing += on_form_closing

        def on_web_resource_requested(sender, args):
            try:
                if closed.is_set() or finished["done"] or self.token:
                    return
                request = getattr(args, "Request", None)
                if request is None:
                    return
                uri = str(getattr(request, "Uri", "") or "")
                low = uri.lower()
                if "chatgpt.com" not in low and "openai.com" not in low and "chat.openai.com" not in low:
                    return
                headers = getattr(request, "Headers", None)
                if headers is None:
                    return
                # Bearer capture from backend-api
                try:
                    auth = headers.GetHeader("Authorization")
                except Exception:
                    auth = None
                if auth and "bearer" in str(auth).lower():
                    tok = str(auth).split(None, 1)[-1].strip()
                    if tok.startswith("eyJ"):
                        if form.IsHandleCreated:
                            form.BeginInvoke(Action(lambda: finish(tok, "Authorization Bearer")))
                        else:
                            finish(tok, "Authorization Bearer")
                        return
                # Cookie session token
                try:
                    cookie_header = headers.GetHeader("Cookie")
                except Exception:
                    cookie_header = None
                if cookie_header and "__Secure-next-auth.session-token=" in cookie_header:
                    # Pass full cookie header for exchange
                    if form.IsHandleCreated:
                        form.BeginInvoke(Action(lambda: finish(cookie_header, "Cookie header")))
                    else:
                        finish(cookie_header, "Cookie header")
            except Exception as e:
                log(f"chatgpt login: request-hook error: {e}")

        def on_init_completed(sender, args):
            try:
                if not args.IsSuccess:
                    self._connecting = False
                    self._push({"type": "error", "message": "Embedded browser failed to start for ChatGPT login."})
                    self._push({"type": "login_cancelled"})
                    safe_close()
                    return
                cv = wv.CoreWebView2
                try:
                    cv.AddWebResourceRequestedFilter("https://*.chatgpt.com/*", CoreWebView2WebResourceContext.All)
                    cv.AddWebResourceRequestedFilter("https://chatgpt.com/*", CoreWebView2WebResourceContext.All)
                    cv.AddWebResourceRequestedFilter("https://*.openai.com/*", CoreWebView2WebResourceContext.All)
                    cv.WebResourceRequested += on_web_resource_requested
                except Exception as e:
                    log(f"chatgpt login: filter error: {e}")
                try:
                    cv.Navigate("https://chatgpt.com/")
                    status.Text = "  Sign in to ChatGPT in this window…"
                except Exception as e:
                    log(f"chatgpt login: navigate error: {e}")
            except Exception as e:
                log(f"chatgpt login: init error: {e}")

        wv.CoreWebView2InitializationCompleted += on_init_completed
        timer = WinTimer()
        timer.Interval = 2000

        def on_tick(sender, e):
            if closed.is_set() or finished["done"] or self.token:
                return
            if self._stop_login.is_set():
                safe_close()
                return
            # Periodically try CookieManager for session cookie
            try:
                cv = wv.CoreWebView2
                if cv is None:
                    return
                task = cv.CookieManager.GetCookiesAsync("https://chatgpt.com")
                # non-blocking: only read if completed immediately-ish next ticks
                if task.IsCompleted and not getattr(task, "IsFaulted", False):
                    cookies = task.Result
                    # Build cookie header
                    parts = []
                    token_val = None
                    for c in cookies:
                        try:
                            name = getattr(c, "Name", None) or getattr(c, "name", None)
                            value = getattr(c, "Value", None) or getattr(c, "value", None)
                            if name and value is not None:
                                parts.append(f"{name}={value}")
                                if name == "__Secure-next-auth.session-token" and value:
                                    token_val = str(value)
                        except Exception:
                            continue
                    if token_val:
                        finish("; ".join(parts) if parts else token_val, "CookieManager")
            except Exception:
                pass

        timer.Tick += on_tick
        try:
            wv.EnsureCoreWebView2Async(None)
        except Exception as e:
            log(f"chatgpt login: ensure error: {e}")
            self._connecting = False
            self._push({"type": "error", "message": "Could not start ChatGPT login browser."})
            self._push({"type": "login_cancelled"})
            return
        timer.Start()
        try:
            form.Show()
            form.BringToFront()
            form.Activate()
        except Exception:
            pass
        Application.Run(form)
        try:
            timer.Stop()
        except Exception:
            pass
        self._login_form = None
        log("chatgpt login: window closed")

    def _login_window_flow(self):
        """Open a native WinForms + WebView2 login window (must run on STA thread).

        Cookie capture strategy (different from prior CookieManager-COM attempts):
          1. PRIMARY: CDP via CoreWebView2.CallDevToolsProtocolMethodAsync
             ("Network.getCookies") — returns plain JSON, no COM cookie objects.
          2. BACKUP: WebResourceRequested Cookie header interception (HttpOnly
             cookies are present on outgoing requests).
          3. LAST: CookieManager.GetCookiesAsync + COM .Name/.Value on UI thread.

        Never navigate the pywebview main window (self-deadlock in 6.2.1).
        Never read page JS document.cookie (hides HttpOnly).
        Disk/DPAPI fallback is a dead end on app-bound encryption — skipped.
        """
        try:
            import clr
        except Exception:
            os.environ["PYTHONNET_RUNTIME"] = "coreclr"
            import clr

        try:
            from webview.util import interop_dll_path
            clr.AddReference("System.Windows.Forms")
            clr.AddReference("System.Drawing")
            clr.AddReference(interop_dll_path("Microsoft.Web.WebView2.Core.dll"))
            clr.AddReference(interop_dll_path("Microsoft.Web.WebView2.WinForms.dll"))
            from System.Windows.Forms import (Application, DockStyle, Form,
                                             FormStartPosition, Label,
                                             Padding)
            from System import Action, Uri
            from System.Drawing import Color, Font, Size
            from Microsoft.Web.WebView2.Core import CoreWebView2WebResourceContext
            from Microsoft.Web.WebView2.WinForms import (CoreWebView2CreationProperties,
                                                         WebView2)
            from System.Windows.Forms import Timer as WinTimer
        except Exception as e:
            log(f"login: could not load WinForms/WebView2: {e}")
            self._connecting = False
            self._push({"type": "error",
                        "message": "Embedded login is unavailable on this PC. "
                                   "Please use the session-cookie option instead."})
            self._push({"type": "login_cancelled"})
            return

        try:
            from System.Windows.Forms import UnhandledExceptionMode
            Application.SetUnhandledExceptionMode(UnhandledExceptionMode.CatchException)

            def _on_winforms_exception(sender, args):
                try:
                    log(f"login: WinForms ThreadException: {args.Exception}")
                    args.ExceptionHandled = True
                except Exception:
                    pass
            Application.ThreadException += _on_winforms_exception
        except Exception as e:
            log(f"login: could not hook WinForms exception handler: {e}")

        form = Form()
        form.Text = "Sign in to Perplexity"
        form.Size = Size(980, 760); form.TopMost = True
        form.StartPosition = FormStartPosition.CenterScreen
        form.MinimumSize = Size(640, 560)
        try:
            form.BackColor = Color.FromArgb(15, 17, 23)
        except Exception:
            pass

        status = Label()
        status.Text = "  Loading Perplexity sign-in…"
        status.Dock = DockStyle.Top
        status.Height = 28
        try:
            status.ForeColor = Color.FromArgb(154, 163, 184)
            status.BackColor = Color.FromArgb(23, 26, 35)
            status.Font = Font("Segoe UI", 9.0)
        except Exception:
            pass

        wv = WebView2()
        wv.Dock = DockStyle.Fill
        try:
            props = CoreWebView2CreationProperties()
            props.UserDataFolder = os.path.join(appdata_dir(), "login-webview")
            wv.CreationProperties = props
        except Exception as e:
            log(f"login: creation-props error (ignored): {e}")

        form.Controls.Add(wv)
        form.Controls.Add(status)

        closed = threading.Event()
        finished = {"done": False}
        self._login_form = form
        log("login: starting embedded login window")

        def on_form_closing(sender, e):
            closed.set()
            try:
                timer.Stop()
            except Exception:
                pass
            if not self.token and not self._login_completion_pending and not finished["done"]:
                log("login: form closing without token; emitting login_cancelled")
                self._connecting = False
                self._push({"type": "login_cancelled"})
        form.FormClosing += on_form_closing

        init_handled = {"done": False}
        abort_before_run = {"yes": False}

        def safe_close():
            try:
                if form.IsHandleCreated:
                    form.BeginInvoke(Action(form.Close))
                else:
                    form.Close()
            except Exception as e:
                log(f"login: safe_close error: {e}")

        def set_status(text: str):
            def _do():
                try:
                    status.Text = "  " + text
                except Exception:
                    pass
            try:
                if form.IsHandleCreated:
                    form.BeginInvoke(Action(_do))
                else:
                    _do()
            except Exception:
                _do()

        def finish_login(token: str, source: str):
            if finished["done"] or not token:
                return
            finished["done"] = True
            try:
                self._login_completion_pending = True
                try:
                    timer.Stop()
                except Exception:
                    pass
                closed.set()
                log(f"login: captured session token via {source}: {token[:8]}...")
                set_status("Sign-in detected — finishing…")
                safe_close()
                # NEVER run network I/O on the WinForms UI thread (freezes +
                # .NET "Not Responding" / unhandled exception dialogs).
                threading.Thread(
                    target=self._accept_token, args=(token, False), daemon=True
                ).start()
            except Exception as e:
                log(f"login: finish_login error: {e}")
                finished["done"] = False

        def on_web_resource_requested(sender, args):
            try:
                if closed.is_set() or finished["done"] or self.token:
                    return
                request = getattr(args, "Request", None)
                if request is None:
                    return
                uri = str(getattr(request, "Uri", "") or "")
                if "perplexity.ai" not in uri.lower():
                    return
                headers = getattr(request, "Headers", None)
                if headers is None:
                    return
                cookie_header = None
                try:
                    cookie_header = headers.GetHeader("Cookie")
                except Exception:
                    try:
                        cookie_header = headers.GetHeaders("Cookie")
                    except Exception:
                        cookie_header = None
                token = extract_session_token_from_cookie_header(cookie_header)
                if not token:
                    return
                log("login: intercepted Perplexity request with session token")
                if form.IsHandleCreated:
                    form.BeginInvoke(Action(lambda: finish_login(token, "WebResourceRequested")))
                else:
                    finish_login(token, "WebResourceRequested")
            except Exception as e:
                log(f"login: request-hook error: {e}")

        def on_init_completed(sender, args):
            try:
                if init_handled["done"]:
                    return
                if not args.IsSuccess:
                    init_handled["done"] = True
                    abort_before_run["yes"] = True
                    err = None
                    try:
                        err = args.InitializationException
                    except Exception:
                        pass
                    log(f"login: WebView2 initialization failed on this PC ({err})")
                    closed.set()
                    try:
                        safe_close()
                    except Exception:
                        pass
                    self._connecting = False
                    self._push({"type": "error",
                                "message": "The embedded browser could not start on this PC. "
                                           "Please use the session-cookie option instead."})
                    self._push({"type": "login_cancelled"})
                    return

                init_handled["done"] = True
                cv = wv.CoreWebView2
                if cv is None:
                    log("login: CoreWebView2 is None after successful init")
                    return

                try:
                    cv.AddWebResourceRequestedFilter(
                        "https://*.perplexity.ai/*", CoreWebView2WebResourceContext.All)
                    cv.AddWebResourceRequestedFilter(
                        "https://www.perplexity.ai/*", CoreWebView2WebResourceContext.All)
                    cv.AddWebResourceRequestedFilter(
                        "*://*.perplexity.ai/*", CoreWebView2WebResourceContext.All)
                    cv.WebResourceRequested += on_web_resource_requested
                    log("login: WebView2 request hook registered")
                except Exception as e:
                    log(f"login: request hook registration error: {e}")

                try:
                    # Fire-and-forget — never Wait() on the UI thread.
                    cv.CallDevToolsProtocolMethodAsync("Network.enable", "{}")
                    log("login: CDP Network.enable issued (async)")
                except Exception as e:
                    log(f"login: CDP Network.enable skipped: {e}")

                try:
                    cv.Navigate("https://www.perplexity.ai/")
                    log("login: navigated embedded browser to Perplexity")
                    set_status("Sign in to Perplexity in this window…")
                except Exception as e:
                    log(f"login: navigate error: {e}")
            except Exception as e:
                log(f"login: init-handler error: {e}")

        wv.CoreWebView2InitializationCompleted += on_init_completed

        poll_state = {
            "ticks": 0,
            "cdp_errors": 0,
            "cdp_task": None,
            "cookie_task": None,
            "cdp_started": 0,
            "cookie_started": 0,
        }

        def poll_for_token():
            """Must run on the WebView2/UI thread.

            NEVER task.Wait() here — WebView2 async completions are marshaled
            back onto this same UI thread, so Wait() deadlocks (observed as
            repeated 'CDP getCookies wait timed out'). Instead: start the
            async call, return to the message pump, and collect Result on a
            later tick once IsCompleted is true.
            """
            if closed.is_set() or finished["done"] or self.token:
                return
            if self._stop_login.is_set():
                safe_close()
                return
            poll_state["ticks"] += 1
            cv = None
            try:
                cv = wv.CoreWebView2
            except Exception as e:
                if poll_state["ticks"] <= 3 or poll_state["ticks"] % 15 == 0:
                    log(f"login: CoreWebView2 access: {e}")
                return
            if cv is None:
                return

            # --- Collect finished CDP task (JSON string — safe) ---
            cdp_task = poll_state["cdp_task"]
            if cdp_task is not None:
                try:
                    if cdp_task.IsCompleted:
                        poll_state["cdp_task"] = None
                        if getattr(cdp_task, "IsFaulted", False):
                            ex = getattr(getattr(cdp_task, "Exception", None), "InnerException", None) or getattr(cdp_task, "Exception", None)
                            poll_state["cdp_errors"] += 1
                            if poll_state["cdp_errors"] <= 5:
                                log(f"login: CDP task faulted: {ex}")
                        else:
                            raw = str(cdp_task.Result)
                            token = extract_session_token_from_cdp_json(raw)
                            if token:
                                finish_login(token, "CDP Network.getCookies")
                                return
                            if poll_state["ticks"] <= 3 or poll_state["ticks"] % 8 == 0:
                                try:
                                    n = len(json.loads(raw).get("cookies") or [])
                                except Exception:
                                    n = -1
                                log(f"login: CDP poll tick={poll_state['ticks']}: {n} cookies, no session token yet")
                    # else still in flight — leave it
                except Exception as e:
                    poll_state["cdp_task"] = None
                    poll_state["cdp_errors"] += 1
                    if poll_state["cdp_errors"] <= 5:
                        log(f"login: CDP collect error: {e}")

            # --- Collect finished CookieManager task (COM cookies: UI thread OK) ---
            cookie_task = poll_state["cookie_task"]
            if cookie_task is not None:
                try:
                    if cookie_task.IsCompleted:
                        poll_state["cookie_task"] = None
                        if not getattr(cookie_task, "IsFaulted", False):
                            cookies = cookie_task.Result
                            token = extract_session_token_from_cookie_records(cookies)
                            if token:
                                finish_login(token, "CookieManager.GetCookiesAsync")
                                return
                except Exception as e:
                    poll_state["cookie_task"] = None
                    if poll_state["ticks"] <= 5:
                        log(f"login: CookieManager collect error: {e}")

            # --- Start new CDP poll if idle ---
            if poll_state["cdp_task"] is None:
                try:
                    args_json = json.dumps({
                        "urls": [
                            "https://www.perplexity.ai/",
                            "https://www.perplexity.ai",
                            "https://perplexity.ai/",
                        ]
                    })
                    poll_state["cdp_task"] = cv.CallDevToolsProtocolMethodAsync(
                        "Network.getCookies", args_json)
                    poll_state["cdp_started"] += 1
                except Exception as e:
                    poll_state["cdp_errors"] += 1
                    if poll_state["cdp_errors"] <= 5:
                        log(f"login: CDP start error: {e}")

            # --- Start CookieManager poll every other free tick ---
            if poll_state["cookie_task"] is None and poll_state["ticks"] % 2 == 0:
                try:
                    poll_state["cookie_task"] = cv.CookieManager.GetCookiesAsync(
                        "https://www.perplexity.ai")
                    poll_state["cookie_started"] += 1
                except Exception as e:
                    if poll_state["ticks"] <= 5:
                        log(f"login: CookieManager start error: {e}")

        def on_tick(sender, e):
            if closed.is_set() or finished["done"]:
                return
            try:
                poll_for_token()
            except Exception as ex:
                log(f"login: tick error: {ex}")

        timer = WinTimer()
        timer.Interval = 1500
        timer.Tick += on_tick

        try:
            log("login: ensuring CoreWebView2")
            # Pump once after Ensure so sync failures set abort_before_run
            wv.EnsureCoreWebView2Async(None)
            try:
                Application.DoEvents()
            except Exception:
                pass
            time.sleep(0.05)
            try:
                Application.DoEvents()
            except Exception:
                pass
        except Exception as e:
            log(f"login: EnsureCoreWebView2Async error: {e}")
            closed.set()
            abort_before_run["yes"] = True
            self._login_completion_pending = False
            self._connecting = False
            self._push({"type": "error",
                        "message": "Could not start the embedded browser. "
                                   "Please use the session-cookie option instead."})
            self._push({"type": "login_cancelled"})
            return

        if abort_before_run["yes"] or closed.is_set():
            log("login: aborting before Application.Run (init already failed)")
            try:
                timer.Stop()
            except Exception:
                pass
            return

        timer.Start()
        log("login: entering Application.Run for login form")
        Application.Run(form)

        try:
            timer.Stop()
        except Exception:
            pass

        if not self.token and not self._login_completion_pending:
            log("login: window closed without token")
            self._connecting = False
            # login_cancelled already emitted from FormClosing when appropriate
        elif self.token:
            log("login: window closed after token accepted")
            self._login_completion_pending = False
        else:
            log("login: window closed while completion pending")
        log("login: window closed")

    def _accept_token(self, token: str, restore_ui: bool):
        log("login: accepting token (background)")
        self._login_completion_pending = False
        self._stop_login.set()
        provider = getattr(self, "_provider_id", "perplexity") or "perplexity"
        try:
            adapter = get_adapter(provider)
            account = adapter.validate(token)
        except Exception as e:
            self._connecting = False
            self._push({"type": "error", "message": friendly_error(e)})
            self._push({"type": "login_cancelled"})
            return
        email = (account.email or account.display_name or account.external_id or "").strip()
        if not email and provider == "perplexity":
            self._connecting = False
            self._push({"type": "error",
                        "message": "That session was not accepted by Perplexity. "
                                   "Please log in again."})
            self._push({"type": "login_cancelled"})
            return
        if not email:
            email = f"{adapter.display_name} user"
        self.token = token
        self.email = email
        # Show "Connected" INSTANTLY; stream the deep conversation count in
        # right after. The old blocking deep list here held the Connected
        # state hostage after login had already succeeded (Gemini/Grok
        # pagination can take minutes) — the worst perceived-latency spot
        # in the app. The UI just displays whatever count arrives.
        self._conversation_count = 0
        self._connecting = False
        self._connected_at = time.monotonic()
        self._first_download_at: float | None = None

        def _count_worker():
            try:
                # Deep listing so the displayed count matches what the export
                # will actually download (shallow/single-page undercounts,
                # e.g. Gemini caps one page at 50 while deep pagination
                # reaches all).
                n = len(adapter.list_conversations(token, deep=True))
            except Exception:
                n = 0
            self._conversation_count = n
            self._push({"type": "connected", "email": email, "count": n,
                        "provider": provider})
            log(f"login: deep count ready for {email} via {provider}: {n}")

        save_session(token, email)
        # Notify UI of successful connection with account selection prompt
        if provider in ("perplexity", "chatgpt", "grok", "gemini", "claude"):
            self._push({"type": "log", "line": f"Connected to {provider}. If you have multiple accounts, select the correct one in the sign-in window."})
        # persist provider with session for reconnect awareness
        try:
            import json as _json
            from totalrecalls.core.paths import SESSION_FILE
            with open(SESSION_FILE, encoding="utf-8") as f:
                data = _json.load(f)
            data["provider"] = provider
            with open(SESSION_FILE, "w", encoding="utf-8") as f:
                _json.dump(data, f)
        except Exception:
            pass
        log(f"login: accepted session token for {email} via {provider}")
        # Instant Connected state; the real count arrives from _count_worker.
        self._count_pending = True
        self._push({"type": "connected", "email": email, "count": None,
                    "provider": provider})
        self._count_thread = threading.Thread(target=_count_worker, daemon=True)
        self._count_thread.start()
        log(f"connected: {email} ({provider}); deep conversation count pending")


    def _export_worker(self, refresh: bool):
        token = self.token
        if not token:
            self._push({"type": "error", "message": "Not connected. Please log in first."})
            return
        outdir = self._default_folder
        provider_name = getattr(self, "_provider_id", "perplexity") or "perplexity"
        # Opt-in classic Spaces/Home-at-root layout (pre-Phase-3). Default = Library/<provider>/.
        classic = os.environ.get("TOTALRECALLS_CLASSIC_EXPORT", "").strip().lower() in ("1", "true", "yes")
        try:
            os.makedirs(outdir, exist_ok=True)
            self._push({"type": "export_start"})
            self._push({"type": "log",
                        "line": f"TotalRecalls v{APP_VERSION} — preparing export…"})
            killed = kill_other_exporter_processes(force=True)
            if killed:
                self._push({"type": "log",
                            "line": f"Closed {len(killed)} other exporter process(es) before discovery."})

            if not classic:
                adapter = get_adapter(getattr(self, "_provider_id", "perplexity") or "perplexity")

                def on_log(line: str):
                    self._push({"type": "log", "line": line})

                def on_progress(p: dict):
                    self._push({
                        "type": "progress",
                        "done": p.get("done", 0),
                        "total": p.get("total", 0),
                        "title": p.get("title", ""),
                    })

                self._push({"type": "log", "line": f"Export via {adapter.display_name} adapter → Library/{adapter.id}/ …"})
                result = export_via_adapter(
                    adapter,
                    credential=token,
                    outdir=outdir,
                    deep=True,
                    refresh=refresh,
                    on_log=on_log,
                    on_progress=on_progress,
                    on_first_download=self._note_first_download,
                )
                empty_n = len(
                    ((result.get("manifest") or {}).get("warnings") or {}).get("empty_answer_threads") or []
                )
                if empty_n:
                    self._push({"type": "log",
                                "line": f"Note: {empty_n} conversation(s) have no answer text (see README warnings)."})
                self._push({
                    "type": "log",
                    "line": (
                        f"Skipped (already saved): {result.get('skipped', 0)}. "
                        f"Failed: {result.get('failed', 0)}."
                    ),
                })
                self._push({"type": "export_done", "done": len(result.get("records") or []),
                            "folder": outdir,
                            "provider_path": f"Library/{provider_name}/home"})
                log(f"export finished via adapter: {result.get('exported')} new, "
                    f"{result.get('skipped')} skipped -> {outdir} (library-v1)")
                return

            # ----- classic path (TOTALRECALLS_CLASSIC_EXPORT=1) -----
            try:
                adapter = get_adapter(provider_name)
                provider_display = adapter.display_name
            except Exception:
                provider_display = provider_name.capitalize()
            self._push({"type": "log", "line": f"Discovering conversations ({provider_display})…"})
            threads = list_threads(token, deep=True)
            total = len(threads)
            # Update the conversation count displayed in the UI (may differ from
            # the shallow count shown during connect)
            self._conversation_count = total
            self._push({"type": "connected", "email": self.email or "",
                        "count": total, "provider": provider_name})
            self._push({"type": "log",
                        "line": f"Found {total} conversation(s) after multi-source discovery. Organizing by Space…"})

            uuid_index = load_uuid_index(outdir)
            records = []
            done = 0
            skipped = 0
            failed = 0

            for pos, t in enumerate(threads, 1):
                uuid = t.get("uuid", "") or ""
                col = t.get("collection") or {}
                list_title = (t.get("title") or t.get("slug") or "Untitled conversation").strip()
                space = space_label_from_collection(col)
                title_disp = list_title[:70]

                existing = None if refresh else find_existing_thread_folder(outdir, uuid, uuid_index)

                if existing and not refresh:
                    try:
                        with open(os.path.join(existing, "thread.json"), encoding="utf-8") as f:
                            data = json.load(f)
                        meta = data.get("thread_metadata") or {}
                        col2 = data.get("collection") or col
                        entries = data.get("entries") or []
                        title = (meta.get("title") or list_title or "Untitled").strip()
                        space = space_label_from_collection(col2, meta)
                        stats = entry_stats(entries)
                        rel = os.path.relpath(existing, outdir).replace("\\", "/")
                        target = thread_abs_folder(outdir, space, title, uuid)
                        target_rel = thread_rel_path(space, title, uuid).replace("\\", "/")
                        if os.path.normpath(existing) != os.path.normpath(target):
                            os.makedirs(os.path.dirname(target), exist_ok=True)
                            if not os.path.exists(target):
                                import shutil
                                shutil.move(existing, target)
                                existing = target
                                rel = target_rel
                                md_path = os.path.join(target, "conversation.md")
                                if not os.path.exists(md_path):
                                    legacy_md = os.path.join(target, "thread.md")
                                    body = open(legacy_md, encoding="utf-8").read() if os.path.exists(legacy_md) else render_markdown({**meta, "uuid": uuid, "space": space if space != HOME_SPACE_NAME else ""}, entries)
                                    with open(md_path, "w", encoding="utf-8") as mf:
                                        mf.write(body)
                        rec = {
                            "uuid": uuid, "title": title, "space": space,
                            "rel_path": rel, "updated_at": t.get("last_query_datetime", ""),
                            "stats": stats, "empty_answers": stats.get("all_answers_empty", False),
                        }
                        records.append(rec)
                        uuid_index[uuid] = rel
                        done += 1
                        skipped += 1
                        self._push({"type": "log", "line": f"[{pos}/{total}] {space} / {title_disp} — already saved"})
                        self._push({"type": "progress", "done": done, "total": total, "title": f"{space}: {title_disp}"})
                        continue
                    except Exception as e:
                        log(f"export: skip-migrate failed for {uuid}: {e}")

                self._push({"type": "log", "line": f"[{pos}/{total}] {space} / {title_disp} — downloading…"})
                self._push({"type": "progress", "done": done, "total": total, "title": f"{space}: {title_disp}"})
                self._note_first_download()
                try:
                    detail = get_thread(token, uuid)
                except ApiError as e:
                    failed += 1
                    self._push({"type": "log", "line": f"  ! failed: {friendly_error(e)}"})
                    continue

                meta = detail.get("thread_metadata", {}) or {}
                title = (meta.get("title") or list_title or "Untitled conversation").strip()
                space = space_label_from_collection(col, meta)
                entry_list = [extract_entry(e) for e in detail.get("entries", [])]
                stats = entry_stats(entry_list)

                folder = thread_abs_folder(outdir, space, title, uuid)
                rel = thread_rel_path(space, title, uuid).replace("\\", "/")
                os.makedirs(folder, exist_ok=True)
                payload = {
                    "thread_metadata": meta,
                    "collection": col,
                    "entries": entry_list,
                    "export": {
                        "space": space,
                        "title": title,
                        "uuid": uuid,
                        "rel_path": rel,
                    },
                }
                with open(os.path.join(folder, "thread.json"), "w", encoding="utf-8") as f:
                    json.dump(payload, f, indent=2, ensure_ascii=False)
                md_meta = {**meta, "uuid": uuid, "space": "" if space == HOME_SPACE_NAME else space, "title": title}
                with open(os.path.join(folder, "conversation.md"), "w", encoding="utf-8") as f:
                    f.write(render_markdown(md_meta, entry_list))
                with open(os.path.join(folder, "thread.md"), "w", encoding="utf-8") as f:
                    f.write(render_markdown(md_meta, entry_list))

                rec = {
                    "uuid": uuid, "title": title, "space": space,
                    "rel_path": rel, "updated_at": t.get("last_query_datetime", ""),
                    "stats": stats, "empty_answers": stats.get("all_answers_empty", False),
                }
                records.append(rec)
                uuid_index[uuid] = rel
                done += 1
                flag = " ⚠️ empty answers" if rec["empty_answers"] else ""
                self._push({"type": "log", "line": f"  ✓ {stats['entries']} turns, {stats['answer_chars']} chars{flag}"})

            manifest = write_export_indexes(outdir, self.email or "", records)
            save_uuid_index(outdir, uuid_index)

            empty_n = len((manifest.get("warnings") or {}).get("empty_answer_threads") or [])
            self._push({"type": "log", "line": f"Wrote README.md + Space folders. {len(records)} conversations indexed."})
            if empty_n:
                self._push({"type": "log", "line": f"Note: {empty_n} conversation(s) have no answer text (see README warnings)."})
            self._push({"type": "log", "line": f"Skipped (already saved): {skipped}. Failed: {failed}."})
            self._push({"type": "export_done", "done": len(records), "folder": outdir,
                        "provider_path": f"Library/{provider_name}/home"})
            log(f"export finished: {len(records)}/{total} -> {outdir} (spaces-v1 classic)")
        except ApiError as e:
            self._push({"type": "error", "message": friendly_error(e)})
        except Exception as e:
            log("export crash: " + traceback.format_exc())
            self._push({"type": "error", "message": friendly_error(e)})

