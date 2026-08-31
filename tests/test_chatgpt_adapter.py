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


if __name__ == "__main__":
    unittest.main()
