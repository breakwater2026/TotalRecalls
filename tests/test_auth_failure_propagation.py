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
        new fast path). A dead session must STILL surface login_expired — the
        fast path must not swallow auth-failed into a settled 0."""
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


if __name__ == "__main__":
    unittest.main()
