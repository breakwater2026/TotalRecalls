"""Claude adapter unit tests."""

from __future__ import annotations

import unittest
from unittest.mock import patch

from totalrecalls.adapters.base import get_adapter, list_provider_ids
from totalrecalls.adapters.claude.adapter import ClaudeAdapter, _messages_from_detail
from totalrecalls.adapters.claude.http import cookie_header_from_credential
from totalrecalls.core.schema import AccountInfo


class ClaudeHelpersTests(unittest.TestCase):
    def test_cookie_header_from_bare_key(self):
        h = cookie_header_from_credential("sk-ant-abc")
        self.assertEqual(h, "sessionKey=sk-ant-abc")

    def test_cookie_header_passthrough(self):
        h = cookie_header_from_credential("sessionKey=xyz; other=1")
        self.assertIn("sessionKey=xyz", h)


class ClaudeAdapterTests(unittest.TestCase):
    def test_registered(self):
        self.assertIn("claude", list_provider_ids())
        a = get_adapter("claude")
        self.assertIsInstance(a, ClaudeAdapter)

    def test_messages_from_detail(self):
        detail = {
            "uuid": "c1",
            "name": "Chat",
            "chat_messages": [
                {"sender": "human", "text": "Hi", "uuid": "m1"},
                {"sender": "assistant", "text": "Hello", "uuid": "m2",
                 "citations": [{"title": "Doc", "url": "https://d.example"}]},
            ],
        }
        msgs = _messages_from_detail(detail)
        self.assertEqual(len(msgs), 2)
        self.assertEqual(msgs[0].role, "user")
        self.assertEqual(msgs[1].role, "assistant")
        self.assertEqual(msgs[1].citations[0].url, "https://d.example")

    def test_to_unified(self):
        a = ClaudeAdapter()
        detail = {
            "uuid": "u1",
            "name": "Title",
            "chat_messages": [{"sender": "human", "text": "Q"}],
        }
        conv = a.to_unified(detail, account=AccountInfo(email="c@x.com"))
        self.assertEqual(conv.provider, "claude")
        self.assertEqual(conv.id, "u1")
        self.assertEqual(conv.title, "Title")
        self.assertEqual(conv.account.email, "c@x.com")

    def test_list_conversations(self):
        a = ClaudeAdapter()
        with patch(
            "totalrecalls.adapters.claude.adapter.validate_credential",
            return_value=(AccountInfo(email="a@b.com"), "cookie", "org1"),
        ), patch(
            "totalrecalls.adapters.claude.adapter.list_org_ids",
            return_value=["org1"],
        ), patch(
            "totalrecalls.adapters.claude.adapter.list_conversations_multi",
            return_value=[{"uuid": "1", "name": "One"}, {"uuid": "2", "name": "Two"}],
        ):
            out = a.list_conversations("sess", deep=False)
        self.assertEqual(len(out), 2)
        self.assertEqual(out[0].title, "One")


class ClaudeMultiOrgTests(unittest.TestCase):
    def test_list_org_ids(self):
        from totalrecalls.adapters.claude import auth as ca
        with patch.object(ca, "request", return_value=(200, {"organizations": [{"uuid": "o1"}, {"uuid": "o2"}]})):
            self.assertEqual(ca.list_org_ids("cookie"), ["o1", "o2"])

    def test_list_org_ids_list_shape(self):
        from totalrecalls.adapters.claude import auth as ca
        with patch.object(ca, "request", return_value=(200, [{"id": "o1"}, {"id": "o2"}])):
            self.assertEqual(ca.list_org_ids("cookie"), ["o1", "o2"])

    def test_list_conversations_multi_merges_orgs(self):
        from totalrecalls.adapters.claude import conversations as cc
        with patch.object(cc, "list_conversations", side_effect=[
            [{"uuid": "a", "name": "A"}],
            [{"uuid": "b", "name": "B"}],
        ]) as lc:
            out = cc.list_conversations_multi("cookie", ["org1", "org2"], deep=True)
        self.assertEqual({it["uuid"] for it in out}, {"a", "b"})
        self.assertEqual(lc.call_count, 2)
        self.assertEqual({it["_org_id"] for it in out}, {"org1", "org2"})

    def test_get_conversation_multi_tries_orgs(self):
        from totalrecalls.adapters.claude import conversations as cc
        from totalrecalls.adapters.claude.http import ClaudeApiError
        with patch.object(cc, "get_conversation", side_effect=[
            ClaudeApiError("http-empty"),
            {"uuid": "c1", "name": "Found"},
        ]) as gc:
            detail = cc.get_conversation_multi("cookie", ["org1", "org2"], "c1")
        self.assertEqual(detail["uuid"], "c1")
        self.assertEqual(gc.call_count, 2)


if __name__ == "__main__":
    unittest.main()
