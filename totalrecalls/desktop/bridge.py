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
        self._default_folder = os.path.join(os.path.expanduser("~"), "Perplexity-export")
        self._LOGIN_TIMEOUT = 8 * 60  # seconds
        self._login_completion_pending = False
        self._conversation_count = 0

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

    def ping(self):
        return "pong"

    def getState(self):
        log(f"bridge: getState (connected={bool(self.token)}, connecting={self._connecting})")
        return {"version": APP_VERSION, "build": APP_BUILD_TAG, "folder": self._default_folder,
                "connected": bool(self.token), "email": self.email or "",
                "connecting": bool(self._connecting), "count": self._conversation_count}

    def connect(self):
        log("bridge: connect() called from UI")
        try:
            self._push({"type": "log", "line": "Received login request from UI"})
        except Exception:
            pass
        if self.token or self._connecting:
            log(f"bridge: connect() ignored (token={bool(self.token)}, connecting={self._connecting})")
            return
        self._connecting = True
        self._login_completion_pending = False
        self._stop_login.clear()
        # Show spinner only — do not reset first (avoids blue-button flash).
        self._push({"type": "waiting_login"})

        log("login: starting embedded WebView2 login (CDP capture)")
        self._start_embedded_login()

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

    def startExport(self, refresh: bool = False):
        log("bridge: startExport() called from UI")
        if not self.token or self._export_thread and self._export_thread.is_alive():
            return
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
        self._push({"type": "disconnected"})
        log("disconnected")

    def quitApp(self):
        try:
            self._window.destroy()
        except Exception:
            pass

    # -- login flow ---------------------------------------------------------

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
        form.Size = Size(980, 760)
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
        try:
            session = validate_session(token)
        except ApiError as e:
            self._connecting = False
            self._push({"type": "error", "message": friendly_error(e)})
            self._push({"type": "login_cancelled"})
            return
        user = session.get("user") or {}
        email = user.get("email") or ""
        if not email:
            self._connecting = False
            self._push({"type": "error",
                        "message": "That session was not accepted by Perplexity. "
                                   "Please log in again."})
            self._push({"type": "login_cancelled"})
            return
        self.token = token
        self.email = email
        count = 0
        try:
            count = len(list_threads(token))
        except ApiError:
            pass
        self._conversation_count = count
        self._connecting = False
        save_session(token, email)
        log(f"login: accepted session token for {email}")
        self._push({"type": "connected", "email": email, "count": count})
        log(f"connected: {email}, {count} threads")

    def _export_worker(self, refresh: bool):
        token = self.token
        if not token:
            self._push({"type": "error", "message": "Not connected. Please log in first."})
            return
        outdir = self._default_folder
        try:
            os.makedirs(outdir, exist_ok=True)
            self._push({"type": "export_start"})
            self._push({"type": "log",
                        "line": f"Perplexity Exporter {APP_VERSION} ({APP_BUILD_TAG}) — preparing export…"})
            # Pre-condition: no sibling EXEs (stale builds / double launches)
            killed = kill_other_exporter_processes(force=True)
            if killed:
                self._push({"type": "log",
                            "line": f"Closed {len(killed)} other exporter process(es) before discovery."})
            self._push({"type": "log", "line": "Discovering conversations (multiple Perplexity indexes)…"})
            threads = list_threads(token, deep=True)
            total = len(threads)
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
                    # Reuse existing data for index (may still be legacy path)
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
                        # If legacy flat path, migrate into Spaces/Home layout
                        target = thread_abs_folder(outdir, space, title, uuid)
                        target_rel = thread_rel_path(space, title, uuid).replace("\\", "/")
                        if os.path.normpath(existing) != os.path.normpath(target):
                            os.makedirs(os.path.dirname(target), exist_ok=True)
                            if not os.path.exists(target):
                                import shutil
                                shutil.move(existing, target)
                                existing = target
                                rel = target_rel
                                # write conversation.md if missing
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
                        # fall through to re-fetch

                self._push({"type": "log", "line": f"[{pos}/{total}] {space} / {title_disp} — downloading…"})
                self._push({"type": "progress", "done": done, "total": total, "title": f"{space}: {title_disp}"})
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
                # compatibility copy
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

            # Include any previously exported threads not in this list? skip.

            # Rebuild indexes from everything we know + scan disk for orphans
            manifest = write_export_indexes(outdir, self.email or "", records)
            save_uuid_index(outdir, uuid_index)

            empty_n = len((manifest.get("warnings") or {}).get("empty_answer_threads") or [])
            self._push({"type": "log", "line": f"Wrote README.md + Space folders. {len(records)} conversations indexed."})
            if empty_n:
                self._push({"type": "log", "line": f"Note: {empty_n} conversation(s) have no answer text (see README warnings)."})
            self._push({"type": "log", "line": f"Skipped (already saved): {skipped}. Failed: {failed}."})
            self._push({"type": "export_done", "done": len(records), "folder": outdir})
            log(f"export finished: {len(records)}/{total} -> {outdir} (spaces-v1)")
        except ApiError as e:
            self._push({"type": "error", "message": friendly_error(e)})
        except Exception as e:
            log("export crash: " + traceback.format_exc())
            self._push({"type": "error", "message": friendly_error(e)})

