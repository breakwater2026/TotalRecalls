"""Regression tests for Bug A: a dead (401/403) session must NOT be coerced
into "0 conversations".

Every adapter's ``list_conversations`` previously swallowed the provider's
``*ApiError("auth-failed")`` (raised by each http layer on 401/403) into an
empty list. Combined with the lenient ``validate()`` (which accepts a stale
token / any captured cookie), a dead session looked "connected" with 0
downloads — the exact bug the user reported on ChatGPT.

These tests pin the fixed behavior: when the underlying HTTP call fails with
``auth-failed`` on the PRIMARY (first) request, ``list_conversations`` must
RAISE (so the UI can prompt a reconnect), not return ``[]``. A genuine empty
account (server returns 200 with no items) must still return ``[]`` — see the
counter-tests below.
"""

from __future__ import annotations

import unittest
from unittest.mock import patch


def _raises_auth_fail(fn, *args, **kwargs):
    try:
        fn(*args, **kwargs)
    except Exception as e:
        assert "auth-failed" in str(e), (
            f"expected an auth-failed error, got {type(e).__name__}: {e}"
        )
        return
    raise AssertionError(f"{getattr(fn, '__name__', fn)!r} did not raise on auth-failed")


class ChatGptAuthFailTests(unittest.TestCase):
    def test_shallow_list_raises_on_auth_failed(self):
        from totalrecalls.adapters.chatgpt import conversations as conv
        from totalrecalls.adapters.chatgpt.http import ChatGptApiError
        with patch.object(
            conv, "request", side_effect=ChatGptApiError("auth-failed")
        ):
            _raises_auth_fail(conv.list_conversations, "tok", deep=False)

    def test_deep_list_raises_on_auth_failed(self):
        from totalrecalls.adapters.chatgpt import conversations as conv
        from totalrecalls.adapters.chatgpt.http import ChatGptApiError
        with patch.object(
            conv, "request", side_effect=ChatGptApiError("auth-failed")
        ):
            _raises_auth_fail(conv.list_conversations, "tok", deep=True)

    def test_empty_account_still_returns_empty(self):
        # 200 with no items = a real (empty) account, NOT a dead session.
        from totalrecalls.adapters.chatgpt import conversations as conv
        with patch.object(conv, "request", return_value=(200, {"items": [], "total": 0})):
            out = conv.list_conversations("tok", deep=False)
        self.assertEqual(out, [])


class ClaudeAuthFailTests(unittest.TestCase):
    def test_single_org_list_raises_on_auth_failed(self):
        from totalrecalls.adapters.claude import conversations as cc
        from totalrecalls.adapters.claude.http import ClaudeApiError
        with patch.object(cc, "request", side_effect=ClaudeApiError("auth-failed")):
            _raises_auth_fail(cc.list_conversations, "cookie", "org1234567", deep=False)

    def test_multi_org_list_raises_on_auth_failed(self):
        # Session-level rejection must not be skipped across orgs.
        from totalrecalls.adapters.claude import conversations as cc
        from totalrecalls.adapters.claude.http import ClaudeApiError
        with patch.object(cc, "request", side_effect=ClaudeApiError("auth-failed")):
            _raises_auth_fail(cc.list_conversations_multi, "cookie", ["org1", "org2"], deep=False)

    def test_empty_account_still_returns_empty(self):
        from totalrecalls.adapters.claude import conversations as cc
        with patch.object(cc, "request", return_value=(200, {"chat_conversations": []})):
            out = cc.list_conversations("cookie", "org1234567", deep=False)
        self.assertEqual(out, [])

    def test_classify_org_permission_error_is_not_auth_failed(self):
        # A 403 permission_error body ("Invalid authorization for organization")
        # is ORG-scoped, not session-scoped — must NOT collapse to auth-failed.
        from totalrecalls.adapters.claude.http import classify_auth_error
        body = ('{"type":"error","error":{"type":"permission_error",'
                '"message":"Invalid authorization for organization"}}')
        self.assertEqual(classify_auth_error(403, body), "org-forbidden")

    def test_classify_plain_403_is_auth_failed(self):
        # A 403 with no permission_error body is still treated as session-dead.
        from totalrecalls.adapters.claude.http import classify_auth_error
        self.assertEqual(classify_auth_error(403, ""), "auth-failed")
        self.assertEqual(classify_auth_error(401, "anything"), "auth-failed")
        self.assertEqual(classify_auth_error(403, "not-json"), "auth-failed")

    def test_multi_org_skips_org_forbidden_but_keeps_good_org(self):
        # Real account shape: primary chat org returns 200 + data, the API
        # "Individual Org" returns 403 permission_error. The list must return
        # the primary org's conversations, NOT raise auth-failed and NOT drop
        # everything to [].
        from totalrecalls.adapters.claude import conversations as cc
        from totalrecalls.adapters.claude.http import ClaudeApiError

        def fake_request(path, cookie, **kw):
            if "GOODORG" in path:
                return 200, [{"uuid": "c1", "name": "kept"}]
            if "BADORG" in path:
                raise ClaudeApiError("org-forbidden")
            return 200, []

        with patch.object(cc, "request", side_effect=fake_request):
            out = cc.list_conversations_multi("cookie", ["GOODORG", "BADORG"], deep=False)
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["uuid"], "c1")

    def test_multi_org_still_raises_on_true_session_death(self):
        # Contrast: a genuine auth-failed (session dead) must still propagate
        # so the UI prompts a reconnect — the Bug A behavior is preserved.
        from totalrecalls.adapters.claude import conversations as cc
        from totalrecalls.adapters.claude.http import ClaudeApiError
        with patch.object(cc, "request", side_effect=ClaudeApiError("auth-failed")):
            _raises_auth_fail(cc.list_conversations_multi, "cookie", ["org1", "org2"], deep=False)


class GeminiAuthFailTests(unittest.TestCase):
    def test_live_list_raises_on_auth_failed(self):
        from totalrecalls.adapters.gemini import adapter as g
        from totalrecalls.adapters.gemini.http import GeminiApiError
        a = g.GeminiAdapter()
        # Force the live path: not a path credential, cookie mode, HTML cached.
        a._mode = "cookie"
        a._cookie = "__Secure-1PSID=x"
        a._page_html = "<html>cached</html>"
        with patch.object(
            g, "list_conversations_live", side_effect=GeminiApiError("auth-failed")
        ):
            _raises_auth_fail(a.list_conversations, "__Secure-1PSID=x", deep=False)


class GrokAuthFailTests(unittest.TestCase):
    def test_list_raises_on_auth_failed(self):
        from totalrecalls.adapters.grok import adapter as gr
        from totalrecalls.adapters.grok.http import GrokApiError
        a = gr.GrokAdapter()
        # A JWT-ish credential resolves to a bearer token so it reaches
        # _grok_paginate (a bare string is treated as a cookie and rejected
        # earlier, which would test _resolve_auth, not the list fix).
        with patch.object(
            gr, "request", side_effect=GrokApiError("auth-failed")
        ):
            _raises_auth_fail(a.list_conversations, "eyJhbGciOi.test.sig", deep=False)

    def test_list_returns_items_when_one_endpoint_works(self):
        from totalrecalls.adapters.grok import adapter as gr
        def fake_req(path, **kw):
            if "/rest/app-chat/conversations" == path:
                return 200, {"conversations": [{"id": "c1", "title": "T"}]}
            return 200, {"conversations": []}
        a = gr.GrokAdapter()
        with patch.object(gr, "request", side_effect=fake_req):
            out = a.list_conversations("eyJhbGciOi.test.sig", deep=False)
        self.assertEqual(len(out), 1)


class DeepSeekAuthFailTests(unittest.TestCase):
    def test_list_raises_on_auth_failed(self):
        from totalrecalls.adapters.deepseek import adapter as d
        from totalrecalls.adapters.deepseek.http import DeepSeekApiError
        a = d.DeepSeekAdapter()
        with patch.object(d, "request", side_effect=DeepSeekApiError("auth-failed")):
            _raises_auth_fail(a.list_conversations, "tok", deep=False)

    def test_empty_account_still_returns_empty(self):
        from totalrecalls.adapters.deepseek import adapter as d
        # Envelope: 200 + {code:0, data:{biz_code:0, biz_data:{chat_sessions:[]}}}
        with patch.object(
            d, "request",
            return_value=(200, {"code": 0, "data": {"biz_code": 0, "biz_data": {"chat_sessions": []}}}),
        ):
            out = d.DeepSeekAdapter().list_conversations("tok", deep=False)
        self.assertEqual(out, [])

    # --- the 2026-09-13 live bug: a dead token surfaces as the envelope
    # business code api-40002 (Missing Token), NOT the string "auth-failed".
    # validate() previously optimistically accepted it (-> "Connected") and the
    # deep count silently returned []. Both must now fail closed / propagate. ---

    def test_validate_raises_on_api_40002_missing_token(self):
        from totalrecalls.adapters.deepseek import adapter as d
        a = d.DeepSeekAdapter()
        # request() returns a 200 with a non-zero envelope code -> _biz_data
        # raises DeepSeekApiError("api-40002: Missing Token").
        with patch.object(d, "request",
                          return_value=(200, {"code": 40002, "msg": "Missing Token"})):
            with self.assertRaises(Exception) as ctx:
                a.validate("some-captured-token")
        self.assertIn("40002", str(ctx.exception))

    def test_validate_raises_on_api_40003_invalid_token(self):
        from totalrecalls.adapters.deepseek import adapter as d
        a = d.DeepSeekAdapter()
        with patch.object(d, "request",
                          return_value=(200, {"code": 40003, "msg": "Invalid Token"})):
            with self.assertRaises(Exception) as ctx:
                a.validate("some-captured-token")
        self.assertIn("40003", str(ctx.exception))

    def test_validate_raises_on_http_401(self):
        from totalrecalls.adapters.deepseek import adapter as d
        from totalrecalls.adapters.deepseek.http import DeepSeekApiError
        a = d.DeepSeekAdapter()
        with patch.object(d, "request", side_effect=DeepSeekApiError("http-401")):
            with self.assertRaises(Exception) as ctx:
                a.validate("some-captured-token")
        self.assertIn("401", str(ctx.exception))

    def test_validate_soft_accepts_on_transient_network(self):
        from totalrecalls.adapters.deepseek import adapter as d
        from totalrecalls.adapters.deepseek.http import DeepSeekApiError
        a = d.DeepSeekAdapter()
        # A network blip / 5xx is NOT a dead session — validate must accept so a
        # momentary hiccup does not read as "expired".
        with patch.object(d, "request", side_effect=DeepSeekApiError("network: timeout")):
            info = a.validate("some-captured-token")
        # Soft-accepted: a real credential was captured, just not verifiable
        # right now — so it is accepted (external_id is the token prefix).
        self.assertTrue(info.external_id.startswith("some-captured-"))
        self.assertEqual(info.external_id, "some-captured-token"[:16])

    def test_list_raises_on_api_40002_envelope(self):
        from totalrecalls.adapters.deepseek import adapter as d
        a = d.DeepSeekAdapter()
        # Envelope rejection on the first (pinned) request must raise so the
        # bridge's count worker fires login_expired, not return [].
        with patch.object(d, "request",
                          return_value=(200, {"code": 40002, "msg": "Missing Token"})):
            with self.assertRaises(Exception) as ctx:
                a.list_conversations("tok", deep=False)
        self.assertIn("40002", str(ctx.exception))


class IsAuthRejectedTests(unittest.TestCase):
    """The shared classifier is the single source of truth for 'dead session'.
    It must recognize every provider's definitive rejection and reject the
    transient/other errors that must degrade to 0, not a false 'expired'."""
    def test_recognizes_all_dead_session_markers(self):
        from totalrecalls.core.errors import is_auth_rejected, AuthRejected
        self.assertTrue(is_auth_rejected(Exception("auth-failed")))
        self.assertTrue(is_auth_rejected(AuthRejected("api-40002: Missing Token")))
        self.assertTrue(is_auth_rejected("api-40002: Missing Token"))
        self.assertTrue(is_auth_rejected("api-40003: Invalid Token"))
        self.assertTrue(is_auth_rejected(Exception("http-401")))
        self.assertTrue(is_auth_rejected("http-403"))
        self.assertTrue(is_auth_rejected("network: ... auth-failed ..."))

    def test_does_not_flag_transient_or_other_errors(self):
        from totalrecalls.core.errors import is_auth_rejected
        self.assertFalse(is_auth_rejected(Exception("network: timeout")))
        self.assertFalse(is_auth_rejected("http-500"))
        self.assertFalse(is_auth_rejected("http-400"))
        self.assertFalse(is_auth_rejected("biz-40002"))  # substring, not a real marker
        self.assertFalse(is_auth_rejected(""))


class MistralAuthFailTests(unittest.TestCase):
    def test_list_raises_on_auth_failed(self):
        from totalrecalls.adapters.mistral import adapter as m
        from totalrecalls.adapters.mistral.http import MistralApiError
        a = m.MistralAdapter()
        with patch.object(m, "trpc_query", side_effect=MistralApiError("auth-failed")):
            _raises_auth_fail(a.list_conversations, "ory_session_x", deep=False)

    def test_empty_account_still_returns_empty(self):
        from totalrecalls.adapters.mistral import adapter as m
        with patch.object(m, "trpc_query", return_value=(200, {"items": []})):
            out = m.MistralAdapter().list_conversations("ory_session_x", deep=False)
        self.assertEqual(out, [])


class QwenAuthFailTests(unittest.TestCase):
    def test_list_raises_on_auth_failed(self):
        from totalrecalls.adapters.qwen import adapter as q
        from totalrecalls.adapters.qwen.http import QwenChatApiError
        a = q.QwenChatAdapter()
        with patch.object(q, "request", side_effect=QwenChatApiError("auth-failed")):
            _raises_auth_fail(a.list_conversations, "xlly_s=1", deep=False)

    def test_empty_account_still_returns_empty(self):
        from totalrecalls.adapters.qwen import adapter as q
        with patch.object(q, "request", return_value=(200, {"success": True, "data": []})):
            out = q.QwenChatAdapter().list_conversations("xlly_s=1", deep=False)
        self.assertEqual(out, [])


class PerplexityAuthFailTests(unittest.TestCase):
    def test_discover_raises_on_auth_failed(self):
        from totalrecalls.adapters.perplexity import discover
        from totalrecalls.adapters.perplexity.http import ApiError
        with patch.object(discover, "request", side_effect=ApiError("auth-failed")):
            _raises_auth_fail(discover.list_threads, "tok", deep=True)

    def test_discover_returns_items_when_endpoint_works(self):
        from totalrecalls.adapters.perplexity import discover
        def fake_req(path, token, method="GET", body=None, delay=0):
            if "list_ask_threads" in path:
                return 200, [{"uuid": "t1", "title": "Q", "total_threads": 1}]
            return 200, []
        with patch.object(discover, "request", side_effect=fake_req):
            out = discover.list_threads("tok", deep=True)
        self.assertEqual(len(out), 1)


class BridgeCountWorkerAuthFailTests(unittest.TestCase):
    """The connect-time deep count must surface a dead session as
    ``login_expired`` + a cleared token, NOT push ``connected`` with count=0."""

    def test_dead_session_during_count_pushes_login_expired(self):
        import totalrecalls.desktop.bridge as bridge_mod
        from totalrecalls.desktop.bridge import Bridge
        from totalrecalls.core.schema import AccountInfo

        class FakeAdapter:
            id = "chatgpt"
            display_name = "ChatGPT"

            def validate(self, credential):
                return AccountInfo(email="user@example.com")

            def list_conversations(self, credential, *, deep=False):
                raise Exception("auth-failed")

        b = Bridge(ui_html="<html></html>")
        b._provider_id = "chatgpt"
        pushes = []
        import time as _time
        # get_adapter / save_session / clear_session are module-level in bridge.
        # NOTE: return an *instance* — _accept_token calls adapter.validate(token),
        # so the class itself would lose `self` and fail as a "validation error".
        # The deep count runs on a daemon thread whose login_expired push lands
        # AFTER _accept_token returns, so keep the _push patch active while we
        # poll for that signal (a bare join would return before the push lands).
        with patch.object(bridge_mod, "get_adapter", return_value=FakeAdapter()), \
             patch.object(bridge_mod, "save_session"), \
             patch.object(bridge_mod, "clear_session"), \
             patch.object(b, "_push", side_effect=pushes.append):
            b._accept_token("stale-token", restore_ui=False)
            deadline = _time.monotonic() + 5
            while _time.monotonic() < deadline:
                if any(p.get("type") == "login_expired" for p in pushes):
                    break
                _time.sleep(0.02)
        t = getattr(b, "_count_thread", None)
        if t is not None:
            t.join(timeout=2)
        types = [p.get("type") for p in pushes]
        # The definitive "reconnect" signal must be pushed.
        self.assertIn("login_expired", types, f"expected login_expired, got {types}")
        # The stale token must be cleared so the next getState says not connected.
        self.assertIsNone(b.token)
        self.assertEqual(b._conversation_count, 0)
        # Crucially: it must NOT end in a clean "connected, count=0" for a dead
        # session. (The instant placeholder connected uses count=None — that is
        # allowed and expected; a settled count=0 is the bug.)
        settled_zero = [
            p for p in pushes
            if p.get("type") == "connected" and p.get("count") == 0
        ]
        self.assertEqual(settled_zero, [], f"dead session reported as connected/0: {pushes}")

    def test_dead_session_during_fast_count_pushes_login_expired(self):
        """Same as above, but the adapter exposes count_conversations() (the
        fast path). A dead session must STILL surface login_expired — the fast
        path must not swallow the rejection into a settled 0."""
        import totalrecalls.desktop.bridge as bridge_mod
        from totalrecalls.desktop.bridge import Bridge
        from totalrecalls.core.schema import AccountInfo

        class FakeAdapter:
            id = "chatgpt"
            display_name = "ChatGPT"

            def validate(self, credential):
                return AccountInfo(email="user@example.com")

            def count_conversations(self, credential):
                raise Exception("auth-failed")

            def list_conversations(self, credential, *, deep=False):
                raise AssertionError("fast path must not fall back to deep list")

        b = Bridge(ui_html="<html></html>")
        b._provider_id = "chatgpt"
        pushes = []
        import time as _time
        with patch.object(bridge_mod, "get_adapter", return_value=FakeAdapter()), \
             patch.object(bridge_mod, "save_session"), \
             patch.object(bridge_mod, "clear_session"), \
             patch.object(b, "_push", side_effect=pushes.append):
            b._accept_token("stale-token", restore_ui=False)
            deadline = _time.monotonic() + 5
            while _time.monotonic() < deadline:
                if any(p.get("type") == "login_expired" for p in pushes):
                    break
                _time.sleep(0.02)
        t = getattr(b, "_count_thread", None)
        if t is not None:
            t.join(timeout=2)
        types = [p.get("type") for p in pushes]
        self.assertIn("login_expired", types, f"expected login_expired, got {types}")
        self.assertIsNone(b.token)
        settled_zero = [
            p for p in pushes
            if p.get("type") == "connected" and p.get("count") == 0
        ]
        self.assertEqual(settled_zero, [], f"dead session reported as connected/0: {pushes}")

    def test_deepseek_shaped_rejection_during_count_pushes_login_expired(self):
        """The 2026-09-13 live bug, end-to-end at the bridge: a DeepSeek dead
        token surfaces as 'api-40002: Missing Token' (NOT the string
        'auth-failed'). The uniform is_auth_rejected() gate in _count_worker
        must still fire login_expired + clear the token — the old
        '"auth-failed" in str(e)' gate let this through as a settled 0."""
        import totalrecalls.desktop.bridge as bridge_mod
        from totalrecalls.desktop.bridge import Bridge
        from totalrecalls.core.schema import AccountInfo

        class FakeAdapter:
            id = "deepseek"
            display_name = "DeepSeek"

            def validate(self, credential):
                return AccountInfo(email="deepseek-session@local")

            def list_conversations(self, credential, *, deep=False):
                raise Exception("api-40002: Missing Token")

        b = Bridge(ui_html="<html></html>")
        b._provider_id = "deepseek"
        pushes = []
        import time as _time
        with patch.object(bridge_mod, "get_adapter", return_value=FakeAdapter()), \
             patch.object(bridge_mod, "save_session"), \
             patch.object(bridge_mod, "clear_session"), \
             patch.object(b, "_push", side_effect=pushes.append):
            b._accept_token("dead-token", restore_ui=False)
            deadline = _time.monotonic() + 5
            while _time.monotonic() < deadline:
                if any(p.get("type") == "login_expired" for p in pushes):
                    break
                _time.sleep(0.02)
        t = getattr(b, "_count_thread", None)
        if t is not None:
            t.join(timeout=2)
        types = [p.get("type") for p in pushes]
        self.assertIn("login_expired", types, f"expected login_expired, got {types}")
        self.assertIsNone(b.token)
        settled_zero = [
            p for p in pushes
            if p.get("type") == "connected" and p.get("count") == 0
        ]
        self.assertEqual(settled_zero, [], f"dead deepseek session reported as connected/0: {pushes}")

    def test_fast_count_pushes_connected_with_count(self):
        """Happy path: an adapter with count_conversations() gets the instant
        placeholder connected, then a settled connected with the real count."""
        import totalrecalls.desktop.bridge as bridge_mod
        from totalrecalls.desktop.bridge import Bridge
        from totalrecalls.core.schema import AccountInfo

        class FakeAdapter:
            id = "chatgpt"
            display_name = "ChatGPT"

            def validate(self, credential):
                return AccountInfo(email="user@example.com")

            def count_conversations(self, credential):
                return 105

        b = Bridge(ui_html="<html></html>")
        b._provider_id = "chatgpt"
        pushes = []
        import time as _time
        with patch.object(bridge_mod, "get_adapter", return_value=FakeAdapter()), \
             patch.object(bridge_mod, "save_session"), \
             patch.object(bridge_mod, "clear_session"), \
             patch.object(b, "_push", side_effect=pushes.append):
            b._accept_token("tok", restore_ui=False)
            deadline = _time.monotonic() + 5
            while _time.monotonic() < deadline:
                if any(p.get("type") == "connected" and p.get("count") == 105 for p in pushes):
                    break
                _time.sleep(0.02)
        t = getattr(b, "_count_thread", None)
        if t is not None:
            t.join(timeout=2)
        settled = [p for p in pushes if p.get("type") == "connected" and p.get("count") == 105]
        self.assertEqual(len(settled), 1, f"expected exactly one settled connected/105, got {pushes}")
        self.assertEqual(b._conversation_count, 105)
        self.assertIsNotNone(b.token)


class LocalStorageBearingTests(unittest.TestCase):
    """The CDP Runtime.evaluate result parser: DeepSeek's localStorage['userToken']
    is the JSON envelope {"value": "<bearer>", "__version": "0"}; the parser must
    return the inner value, and degrade gracefully on any other shape."""
    def _cdp(self, inner):
        import json as _json
        return _json.dumps({"result": {"type": "string", "value": inner}})

    def test_unwraps_deepseek_envelope(self):
        from totalrecalls.desktop.bridge import _extract_local_storage_bearer
        inner = '{"value": "2LQ97tX1hqbcGIxSkRbBpEUejVPM3le/DV8BWUdHFfigVukUYtCz4e", "__version": "0"}'
        self.assertEqual(_extract_local_storage_bearer(self._cdp(inner), "userToken"),
                         "2LQ97tX1hqbcGIxSkRbBpEUejVPM3le/DV8BWUdHFfigVukUYtCz4e")

    def test_returns_bare_token_when_no_envelope(self):
        from totalrecalls.desktop.bridge import _extract_local_storage_bearer
        self.assertEqual(_extract_local_storage_bearer(self._cdp("plain-opaque-token"), "userToken"),
                         "plain-opaque-token")

    def test_returns_none_when_item_null_or_absent(self):
        from totalrecalls.desktop.bridge import _extract_local_storage_bearer
        # Not signed in: localStorage.getItem -> null (no "value" in result).
        self.assertIsNone(_extract_local_storage_bearer('{"result": {"type": "object"}}', "userToken"))
        self.assertIsNone(_extract_local_storage_bearer("", "userToken"))
        self.assertIsNone(_extract_local_storage_bearer(None, "userToken"))
        self.assertIsNone(_extract_local_storage_bearer("not-json", "userToken"))


class LocalStorageProbeGateTests(unittest.TestCase):
    """The live 2026-09-13 bug: the DeepSeek auth page writes a short opaque
    NONCE under the same localStorage key ('userToken'); the app's home page
    holds the real long bearer. The capture must only close the login window
    after the provider's own validate() accepts the candidate — a nonce that
    fails validate() keeps the window open. _local_storage_probe_ok is the gate.
    """

    def test_probe_ok_true_when_validate_accepts(self):
        from totalrecalls.desktop.bridge import _local_storage_probe_ok
        class _A:
            def validate(self, cred):
                return object()  # accepted
        with patch("totalrecalls.adapters.base.get_adapter", return_value=_A()):
            self.assertTrue(_local_storage_probe_ok("deepseek", "whatever"))

    def test_probe_ok_false_when_validate_raises_api_rejection(self):
        """The exact live symptom: 30-char nonce -> api-40003 -> window stays open."""
        from totalrecalls.desktop.bridge import _local_storage_probe_ok
        class _A:
            def validate(self, cred):
                raise Exception("api-40003: Authorization Failed (invalid token)")
        with patch("totalrecalls.adapters.base.get_adapter", return_value=_A()):
            self.assertFalse(_local_storage_probe_ok("deepseek", "30-char-junk-nonce-value-123"))

    def test_probe_ok_false_on_network_error(self):
        """Cannot confirm -> treat as not-yet-validated (window stays open), never accept."""
        from totalrecalls.desktop.bridge import _local_storage_probe_ok
        class _A:
            def validate(self, cred):
                raise Exception("network: timeout")
        with patch("totalrecalls.adapters.base.get_adapter", return_value=_A()):
            self.assertFalse(_local_storage_probe_ok("deepseek", "some-candidate"))


if __name__ == "__main__":
    unittest.main()
