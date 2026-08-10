import builtins
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

from app import (Bridge, JsApi, dispatch_to_ui_thread, safe_name,
                 thread_folder_name, thread_rel_path, space_label_from_collection,
                 HOME_SPACE_NAME, _normalize_thread_items, _thread_key,
                 kill_other_exporter_processes,
                 extract_session_token_from_cookie_header,
                 extract_session_token_from_cookie_records,
                 extract_session_token_from_cdp_json,
                 request)


class LoginTokenExtractionTests(unittest.TestCase):
    def test_extracts_secure_session_token_from_cookie_header(self):
        header = "foo=bar; __Secure-next-auth.session-token=abc123; other=baz"
        self.assertEqual(extract_session_token_from_cookie_header(header), "abc123")

    def test_returns_none_when_token_missing(self):
        self.assertIsNone(extract_session_token_from_cookie_header("foo=bar; other=baz"))

    def test_extracts_session_token_from_cookie_records(self):
        cookies = [
            {"name": "foo", "value": "bar"},
            {"name": "__Secure-next-auth.session-token", "value": "abc123"},
        ]
        self.assertEqual(extract_session_token_from_cookie_records(cookies), "abc123")

    def test_extracts_session_token_from_com_like_objects(self):
        class FakeCookie:
            def __init__(self, name, value):
                self.Name = name
                self.Value = value
        cookies = [FakeCookie("x", "y"), FakeCookie("__Secure-next-auth.session-token", "tok99")]
        self.assertEqual(extract_session_token_from_cookie_records(cookies), "tok99")

    def test_extracts_session_token_from_cdp_json(self):
        raw = '{"cookies":[{"name":"foo","value":"bar"},{"name":"__Secure-next-auth.session-token","value":"cdp-tok"}]}'
        self.assertEqual(extract_session_token_from_cdp_json(raw), "cdp-tok")
        self.assertIsNone(extract_session_token_from_cdp_json('{"cookies":[]}'))

    def test_default_version_footer_is_present_in_html(self):
        html = Path(__file__).resolve().parents[1].joinpath("app_ui.html").read_text(encoding="utf-8")
        self.assertIn('id="ver">Perplexity Exporter v1.0.0</footer>', html)
        self.assertIn('id="err-connect"', html)
        self.assertIn("sign-in window opens inside the app", html.lower())
        self.assertIn('id="btn-connect"', html)

    def test_dispatch_to_ui_thread_runs_callback(self):
        class DummyForm:
            InvokeRequired = False

        calls = []
        dispatch_to_ui_thread(DummyForm(), lambda: calls.append("ok"))
        self.assertEqual(calls, ["ok"])

    def test_accept_token_sets_state_and_count(self):
        bridge = Bridge(ui_html="<html></html>")
        # Bridge binds symbols from totalrecalls.desktop.bridge — patch there.
        with patch("totalrecalls.desktop.bridge.validate_session",
                   return_value={"user": {"email": "user@example.com"}}), \
             patch("totalrecalls.desktop.bridge.list_threads",
                   return_value=[{"uuid": "1"}]), \
             patch.object(bridge, "_push"):
            bridge._accept_token("abc123", False)

        self.assertEqual(bridge.token, "abc123")
        self.assertEqual(bridge.email, "user@example.com")
        self.assertEqual(bridge._conversation_count, 1)

    def test_connect_does_not_kill_the_running_app(self):
        bridge = Bridge(ui_html="<html></html>")
        with patch.object(bridge, "_start_embedded_login") as start, \
             patch("subprocess.run") as mock_run, \
             patch.object(bridge, "_push"):
            bridge.connect()
        mock_run.assert_not_called()
        start.assert_called_once()

    def test_connect_starts_embedded_login_flow(self):
        bridge = Bridge(ui_html="<html></html>")
        with patch.object(bridge, "_push") as mock_push, \
             patch.object(bridge, "_start_embedded_login") as start:
            bridge.connect()

        start.assert_called_once()
        types = [call.args[0]["type"] for call in mock_push.call_args_list]
        self.assertIn("waiting_login", types)
        # Must not flash-reset before waiting
        if "reset_login_ui" in types:
            self.assertGreater(types.index("reset_login_ui"), types.index("waiting_login"))

    def test_connect_shows_waiting_state(self):
        bridge = Bridge(ui_html="<html></html>")
        with patch.object(bridge, "_push") as mock_push, \
             patch.object(bridge, "_start_embedded_login"):
            bridge.connect()
        calls = [call.args[0]["type"] for call in mock_push.call_args_list]
        self.assertIn("waiting_login", calls)
        self.assertTrue(bridge._connecting)

    def test_request_falls_back_to_stdlib_when_cffi_raises_unicode_encode_error(self):
        class DummyResponse:
            status = 200

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

            def read(self):
                return b'{"ok": true}'

        # request() lives in adapters.perplexity.http — patch that module's globals.
        with patch("totalrecalls.adapters.perplexity.http._HAS_CFFI", True), \
             patch("totalrecalls.adapters.perplexity.http._cffi_requests") as mock_cffi, \
             patch("urllib.request.urlopen", return_value=DummyResponse()) as mock_urlopen:
            mock_cffi.request.side_effect = UnicodeEncodeError("ascii", "x", 0, 1, "bad")
            status, payload = request("/api/test", "abc123", delay=0)

        self.assertEqual(status, 200)
        self.assertEqual(payload, {"ok": True})
        mock_urlopen.assert_called_once()

    def test_log_writes_to_fallback_path_when_primary_location_is_unavailable(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            primary = Path(tmpdir) / "primary.log"
            fallback = Path(tmpdir) / "fallback.log"

            original_open = builtins.open

            def fake_open(path, *args, **kwargs):
                if str(path) == str(primary):
                    raise PermissionError("blocked")
                return original_open(path, *args, **kwargs)

            with patch("totalrecalls.core.paths._candidate_log_paths",
                       return_value=[str(primary), str(fallback)]), \
                 patch("builtins.open", side_effect=fake_open):
                from totalrecalls.core.paths import log as core_log
                core_log("fallback-write")

            self.assertIn("fallback-write", fallback.read_text(encoding="utf-8"))


    def test_jsapi_only_exposes_bridge_methods(self):
        bridge = Bridge(ui_html="<html></html>")
        api = JsApi(bridge)
        # Public names pywebview will see — must be methods only (no window/token).
        public = [n for n in dir(api) if not n.startswith("_")]
        for name in public:
            attr = getattr(api, name)
            self.assertTrue(callable(attr), f"{name} should be callable, got {type(attr)}")
        for required in ("connect", "getState", "ping", "cancelLogin", "pasteCookie"):
            self.assertIn(required, public)
        # Must NOT re-export bridge state objects
        self.assertFalse(hasattr(api, "window") and not str(getattr(api, "window", "")).startswith("missing"))
        self.assertFalse(hasattr(api, "token"))

    def test_bridge_window_attr_is_private(self):
        bridge = Bridge(ui_html="<html></html>")
        self.assertTrue(hasattr(bridge, "_window"))
        self.assertFalse(hasattr(bridge, "window"))


    def test_human_thread_folder_uses_title_and_short_id(self):
        name = thread_folder_name("Google cloud setup", "a1b2c3d4-eeee-ffff-0000-111122223333")
        self.assertIn("Google cloud setup", name)
        self.assertIn("a1b2c3d4", name)
        self.assertNotEqual(name, "a1b2c3d4-eeee-ffff-0000-111122223333")

    def test_thread_rel_path_uses_spaces_or_home(self):
        home = thread_rel_path(HOME_SPACE_NAME, "Hello", "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee")
        self.assertTrue(home.replace("\\", "/").startswith("Home/"))
        sp = thread_rel_path("TRADING", "Micro futures", "bbbbbbbb-bbbb-cccc-dddd-eeeeeeeeeeee")
        self.assertIn("Spaces", sp.replace("\\", "/"))
        self.assertIn("TRADING", sp)

    def test_space_label_defaults_to_home(self):
        self.assertEqual(space_label_from_collection({}), HOME_SPACE_NAME)
        self.assertEqual(space_label_from_collection({"title": "PROP FUNDING"}), "PROP FUNDING")


    def test_normalize_thread_items_accepts_wrapped_shapes(self):
        self.assertEqual(len(_normalize_thread_items([{"uuid": "a"}])), 1)
        self.assertEqual(len(_normalize_thread_items({"threads": [{"uuid": "a"}, {"uuid": "b"}]})), 2)
        self.assertEqual(_thread_key({"slug": "x"}), "x")
        self.assertEqual(_thread_key({"uuid": "u", "slug": "x"}), "u")


    def test_kill_other_exporter_processes_returns_list(self):
        # Should not raise; may kill nothing in test env.
        killed = kill_other_exporter_processes(force=True)
        self.assertIsInstance(killed, list)


if __name__ == "__main__":
    unittest.main()
