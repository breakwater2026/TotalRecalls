"""Tests for ChatGPT adapter + multi-provider registry."""

from __future__ import annotations

import unittest
from unittest.mock import patch

from totalrecalls.adapters.base import get_adapter, list_provider_ids
from totalrecalls.adapters.chatgpt.adapter import ChatGptAdapter, _walk_messages
from totalrecalls.adapters.chatgpt.auth import (
    cookie_header_from_session_token,
    looks_like_bearer_token,
    normalize_bearer,
)
from totalrecalls.core.schema import AccountInfo


class ChatGptAuthHelpersTests(unittest.TestCase):
    def test_looks_like_bearer_jwt(self):
        self.assertTrue(looks_like_bearer_token("eyJhbGciOi.something.signature"))
        self.assertTrue(looks_like_bearer_token("Bearer eyJhbGciOi.something.signature"))
        self.assertFalse(looks_like_bearer_token("not-a-token"))

    def test_normalize_bearer(self):
        self.assertEqual(normalize_bearer("Bearer abc"), "abc")
        self.assertEqual(normalize_bearer("abc"), "abc")

    def test_cookie_header_builds_session_token(self):
        h = cookie_header_from_session_token("sess123")
        self.assertIn("__Secure-next-auth.session-token=sess123", h)


class ChatGptAdapterTests(unittest.TestCase):
    def test_registered(self):
        self.assertIn("chatgpt", list_provider_ids())
        a = get_adapter("chatgpt")
        self.assertIsInstance(a, ChatGptAdapter)
        self.assertEqual(a.id, "chatgpt")

    def test_walk_messages_from_mapping(self):
        detail = {
            "title": "Demo",
            "conversation_id": "c1",
            "current_node": "n3",
            "mapping": {
                "n1": {"id": "n1", "parent": None, "children": ["n2"], "message": None},
                "n2": {
                    "id": "n2",
                    "parent": "n1",
                    "children": ["n3"],
                    "message": {
                        "id": "m1",
                        "author": {"role": "user"},
                        "content": {"content_type": "text", "parts": ["Hello?"]},
                        "create_time": 1700000000,
                    },
                },
                "n3": {
                    "id": "n3",
                    "parent": "n2",
                    "children": [],
                    "message": {
                        "id": "m2",
                        "author": {"role": "assistant"},
                        "content": {"parts": ["Hi there"]},
                        "metadata": {
                            "model_slug": "gpt-4o",
                            "citations": [{"title": "Src", "url": "https://ex.com"}],
                        },
                    },
                },
            },
        }
        msgs = _walk_messages(detail)
        self.assertEqual(len(msgs), 2)
        self.assertEqual(msgs[0].role, "user")
        self.assertEqual(msgs[0].content_md, "Hello?")
        self.assertEqual(msgs[1].role, "assistant")
        self.assertIn("Hi there", msgs[1].content_md)
        self.assertEqual(msgs[1].citations[0].url, "https://ex.com")

    def test_to_unified(self):
        adapter = ChatGptAdapter()
        detail = {
            "title": "T",
            "conversation_id": "cid",
            "mapping": {
                "a": {
                    "parent": None,
                    "children": [],
                    "message": {
                        "author": {"role": "user"},
                        "content": {"parts": ["Q"]},
                    },
                }
            },
            "current_node": "a",
        }
        conv = adapter.to_unified(detail, account=AccountInfo(email="u@x.com"))
        self.assertEqual(conv.provider, "chatgpt")
        self.assertEqual(conv.id, "cid")
        self.assertEqual(conv.title, "T")
        self.assertEqual(conv.account.email, "u@x.com")
        self.assertTrue(any(m.content_md == "Q" for m in conv.messages))

    def test_list_conversations_maps(self):
        adapter = ChatGptAdapter()
        fake_items = [
            {"id": "1", "title": "One", "update_time": 1700000001},
            {"id": "2", "title": "Two"},
        ]
        with patch(
            "totalrecalls.adapters.chatgpt.adapter.validate_credential",
            return_value=(AccountInfo(email="a@b.com"), "tok"),
        ), patch(
            "totalrecalls.adapters.chatgpt.adapter.list_conversations",
            return_value=fake_items,
        ):
            out = adapter.list_conversations("tok", deep=False)
        self.assertEqual(len(out), 2)
        self.assertEqual(out[0].id, "1")
        self.assertEqual(out[0].title, "One")

    def test_validate_uses_auth(self):
        adapter = ChatGptAdapter()
        with patch(
            "totalrecalls.adapters.chatgpt.adapter.validate_credential",
            return_value=(AccountInfo(email="z@z.com"), "abc"),
        ):
            acct = adapter.validate("eyJhbGciOi.test.sig")
        self.assertEqual(acct.email, "z@z.com")


class BridgeProviderTests(unittest.TestCase):
    def test_set_provider_and_list(self):
        from totalrecalls.desktop.bridge import Bridge
        b = Bridge(ui_html="<html></html>")
        with patch.object(b, "_push"):
            r = b.setProvider("chatgpt")
        self.assertTrue(r.get("ok"))
        self.assertEqual(b._provider_id, "chatgpt")
        ids = [p["id"] for p in b.listProviders() if p.get("available")]
        self.assertIn("chatgpt", ids)
        self.assertIn("perplexity", ids)


class ChatGptDeepListTests(unittest.TestCase):
    """Deep listing must cover archived chats and Projects (snorlax)."""

    def test_deep_list_includes_archived_pass(self):
        from totalrecalls.adapters.chatgpt import conversations as conv
        with patch.object(conv, "request", return_value=(200, {"items": [], "total": 0})) as req:
            conv.list_conversations("tok", deep=True)
        paths = [str(c.args[0]) for c in req.call_args_list if c.args]
        self.assertTrue(any("is_archived=true" in p for p in paths))

    def test_deep_list_walks_projects(self):
        from totalrecalls.adapters.chatgpt import conversations as conv
        sidebar = {"gizmos": [{"id": "proj1", "name": "My Project"}]}
        proj_convs = {"items": [{"id": "c1", "title": "In project"}]}

        def fake_req(path, **kw):
            if "snorlax/sidebar" in path:
                return 200, sidebar
            if path.startswith("/backend-api/gizmos/proj1/conversations"):
                return 200, proj_convs
            return 200, {"items": [], "total": 0}

        with patch.object(conv, "request", side_effect=fake_req):
            out = conv.list_conversations("tok", deep=True)
        ids = {str(c.get("id")) for c in out}
        self.assertIn("c1", ids)


class ChatGptCountFastPathTests(unittest.TestCase):
    """The connect badge uses count_conversations() — it COUNTS REAL ITEMS by
    paginating a single order=updated pass (limit=100) to a short page, NOT
    the API's `total` field (a pagination artifact: min(offset+limit+1,
    true_count) — limit=1 returns total=2 for a 105-conversation account) and
    NOT the 7-pass deep sweep. It must re-raise auth-failed (Bug A) but degrade
    a transient mid-count error to the partial count collected so far."""

    def test_count_counts_real_items_across_pages(self):
        from totalrecalls.adapters.chatgpt import conversations as conv
        from totalrecalls.core.schema import AccountInfo
        adapter = ChatGptAdapter()
        # 105 real items: page 0 = 100, page 1 = 5 (short page → stop). The
        # `total` field is garbage (2, 29...) and must be IGNORED.
        def fake_page(token, **kw):
            off = kw["offset"]
            if off == 0:
                return ([{"id": f"c{i}"} for i in range(100)], 2)
            if off == 100:
                return ([{"id": f"c{i}"} for i in range(100, 105)], 29)
            return ([], 0)
        with patch.object(conv, "_page_list_conversations", side_effect=fake_page) as pc, \
             patch(
                 "totalrecalls.adapters.chatgpt.adapter.validate_credential",
                 return_value=(AccountInfo(email="a@b.com"), "tok"),
             ):
            n = adapter.count_conversations("tok")
        self.assertEqual(n, 105)
        self.assertEqual(pc.call_count, 2)
        self.assertEqual(pc.call_args_list[0].kwargs["limit"], 100)
        self.assertEqual(pc.call_args_list[1].kwargs["offset"], 100)

    def test_count_single_short_page(self):
        # One short page (fewer than limit items) → count = page size, stop.
        from totalrecalls.adapters.chatgpt import conversations as conv
        from totalrecalls.core.schema import AccountInfo
        adapter = ChatGptAdapter()
        with patch.object(
            conv, "_page_list_conversations",
            return_value=([{"id": "a"}, {"id": "b"}], 2),
        ), patch(
            "totalrecalls.adapters.chatgpt.adapter.validate_credential",
            return_value=(AccountInfo(email="a@b.com"), "tok"),
        ):
            self.assertEqual(adapter.count_conversations("tok"), 2)

    def test_count_empty_account_is_zero(self):
        from totalrecalls.adapters.chatgpt import conversations as conv
        from totalrecalls.core.schema import AccountInfo
        adapter = ChatGptAdapter()
        with patch.object(
            conv, "_page_list_conversations",
            return_value=([], 0),
        ), patch(
            "totalrecalls.adapters.chatgpt.adapter.validate_credential",
            return_value=(AccountInfo(email="a@b.com"), "tok"),
        ):
            self.assertEqual(adapter.count_conversations("tok"), 0)

    def test_count_raises_on_auth_failed(self):
        from totalrecalls.adapters.chatgpt import conversations as conv
        from totalrecalls.adapters.chatgpt.http import ChatGptApiError
        from totalrecalls.core.schema import AccountInfo
        adapter = ChatGptAdapter()
        with patch.object(
            conv, "_page_list_conversations",
            side_effect=ChatGptApiError("auth-failed"),
        ), patch(
            "totalrecalls.adapters.chatgpt.adapter.validate_credential",
            return_value=(AccountInfo(email="a@b.com"), "tok"),
        ):
            with self.assertRaises(ChatGptApiError) as ctx:
                adapter.count_conversations("tok")
        self.assertIn("auth-failed", str(ctx.exception))

    def test_count_degrades_to_partial_on_transient_error(self):
        from totalrecalls.adapters.chatgpt import conversations as conv
        from totalrecalls.adapters.chatgpt.http import ChatGptApiError
        from totalrecalls.core.schema import AccountInfo
        adapter = ChatGptAdapter()
        # First page returns 100, second page 500s → partial count 100 (not 0).
        def fake_page(token, **kw):
            if kw["offset"] == 0:
                return ([{"id": f"c{i}"} for i in range(100)], 101)
            raise ChatGptApiError("http-500")
        with patch.object(conv, "_page_list_conversations", side_effect=fake_page), \
             patch(
                 "totalrecalls.adapters.chatgpt.adapter.validate_credential",
                 return_value=(AccountInfo(email="a@b.com"), "tok"),
             ):
            self.assertEqual(adapter.count_conversations("tok"), 100)

    def test_count_degrades_to_zero_on_first_page_error(self):
        from totalrecalls.adapters.chatgpt import conversations as conv
        from totalrecalls.adapters.chatgpt.http import ChatGptApiError
        from totalrecalls.core.schema import AccountInfo
        adapter = ChatGptAdapter()
        with patch.object(
            conv, "_page_list_conversations",
            side_effect=ChatGptApiError("http-500"),
        ), patch(
            "totalrecalls.adapters.chatgpt.adapter.validate_credential",
            return_value=(AccountInfo(email="a@b.com"), "tok"),
        ):
            self.assertEqual(adapter.count_conversations("tok"), 0)


if __name__ == "__main__":
    unittest.main()
