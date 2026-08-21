"""Gemini + Grok adapter tests."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.parse import parse_qs

from totalrecalls.adapters.base import get_adapter, list_provider_ids
from totalrecalls.adapters.gemini.adapter import GeminiAdapter
from totalrecalls.adapters.gemini.http import (
    LIST_CONVERSATIONS_RPC,
    _batchexecute_body,
    _parse_batchexecute_response,
    fetch_conversation_live,
    list_conversations_live,
    load_offline_export,
)
from totalrecalls.adapters.grok.adapter import GrokAdapter
from totalrecalls.core.schema import AccountInfo


class GeminiOfflineTests(unittest.TestCase):
    @staticmethod
    def _frame(part):
        encoded = json.dumps(part, separators=(",", ":"))
        return b")]}'\n" + str(len(encoded)) .encode() + b"\n" + encoded.encode()

    def test_batchexecute_body(self):
        body = parse_qs(_batchexecute_body(LIST_CONVERSATIONS_RPC, [13, None, [1, None, 1]], "token").decode())
        self.assertEqual(body["at"], ["token"])
        request = json.loads(body["f.req"][0])
        self.assertEqual(request[0][0][0], LIST_CONVERSATIONS_RPC)
        self.assertEqual(json.loads(request[0][0][1]), [13, None, [1, None, 1]])

    def test_batchexecute_response_frame(self):
        part = ["wrb.fr", LIST_CONVERSATIONS_RPC, json.dumps([None, None, []])]
        self.assertEqual(_parse_batchexecute_response(self._frame(part))[0], part)

    def test_live_list_and_fetch_mapping(self):
        api_key = "AIza" + "A" * 30
        html = json.dumps({"key": api_key, "SNlM0e": "token"})
        list_part = ["wrb.fr", LIST_CONVERSATIONS_RPC, json.dumps([None, None, [["c1", "One", True]]])]
        turn = ["rid", None, [["Question"]], [[["rcid", ["Answer"]]]]]
        turn_part = ["wrb.fr", "hNvQHb", json.dumps([[turn]])]
        with patch(
            "totalrecalls.adapters.gemini.http._make_rpc_request",
            side_effect=[self._frame(list_part), self._frame(turn_part)],
        ):
            summaries = list_conversations_live(html, "SID=s; SAPISID=p")
            detail = fetch_conversation_live(html, "SID=s; SAPISID=p", "c1")
        self.assertEqual(summaries[0]["title"], "One")
        self.assertEqual([m["role"] for m in detail["messages"]], ["user", "assistant"])
        self.assertEqual(detail["messages"][1]["content"], "Answer")

    def test_registered(self):
        self.assertIn("gemini", list_provider_ids())
        self.assertIsInstance(get_adapter("gemini"), GeminiAdapter)

    def test_offline_takeout_json(self):
        payload = [
            {
                "id": "g1",
                "title": "Gemini chat",
                "messages": [
                    {"role": "user", "content": "Hi"},
                    {"role": "model", "content": "Hello from Gemini"},
                ],
            }
        ]
        with tempfile.TemporaryDirectory() as td:
            fp = Path(td) / "conversations.json"
            fp.write_text(json.dumps(payload), encoding="utf-8")
            items = load_offline_export(str(fp))
            self.assertEqual(len(items), 1)
            adapter = GeminiAdapter()
            acct = adapter.validate(str(fp))
            self.assertIn("takeout", acct.external_id)
            summaries = adapter.list_conversations(str(fp), deep=True)
            self.assertEqual(summaries[0].id, "g1")
            conv = adapter.fetch_conversation(str(fp), "g1")
            self.assertEqual(conv.provider, "gemini")
            self.assertEqual(len(conv.messages), 2)
            self.assertEqual(conv.messages[1].content_md, "Hello from Gemini")

    def test_to_unified_roles(self):
        adapter = GeminiAdapter()
        conv = adapter.to_unified(
            {
                "id": "x",
                "title": "T",
                "messages": [
                    {"role": "user", "content": "Q"},
                    {"role": "assistant", "content": "A"},
                ],
            },
            account=AccountInfo(email="g@x.com"),
        )
        self.assertEqual(conv.messages[0].role, "user")
        self.assertEqual(conv.messages[1].role, "assistant")


class GrokAdapterTests(unittest.TestCase):
    def test_registered(self):
        self.assertIn("grok", list_provider_ids())
        self.assertIsInstance(get_adapter("grok"), GrokAdapter)

    def test_validate_bearer_optimistic(self):
        adapter = GrokAdapter()
        with patch("totalrecalls.adapters.grok.adapter.request", side_effect=Exception("nope")):
            acct = adapter.validate("eyJhbGciOi.test.sig")
        self.assertEqual(acct.display_name, "Grok user")

    def test_list_and_fetch_mapping(self):
        adapter = GrokAdapter()
        with patch("totalrecalls.adapters.grok.adapter.request") as req:
            # validate probes then list then fetch
            req.side_effect = [
                (200, {"user": {"email": "g@x.com", "id": "1"}}),  # validate
                (200, {"conversations": [{"id": "c1", "title": "One"}]}),  # list
                (200, {"user": {"email": "g@x.com", "id": "1"}}),  # validate in fetch
                (200, {"id": "c1", "title": "One", "messages": [
                    {"role": "user", "content": "Hi"},
                    {"role": "assistant", "content": "Hey"},
                ]}),
            ]
            # validate once
            adapter.validate("eyJhbGciOi.test.sig")
            # reset side effect carefully for list
            req.side_effect = [
                (200, {"conversations": [{"id": "c1", "title": "One"}]}),
            ]
            summaries = adapter.list_conversations("eyJhbGciOi.test.sig")
            self.assertEqual(summaries[0].id, "c1")
            req.side_effect = [
                (200, {"user": {"email": "g@x.com"}}),
                (200, {"id": "c1", "messages": [
                    {"role": "user", "content": "Hi"},
                    {"role": "assistant", "content": "Hey"},
                ]}),
            ]
            # fetch_conversation calls validate then request loop
            with patch.object(adapter, "validate", return_value=AccountInfo(email="g@x.com")):
                req.side_effect = [
                    (200, {"id": "c1", "title": "One", "messages": [
                        {"role": "user", "content": "Hi"},
                        {"role": "assistant", "content": "Hey"},
                    ]}),
                ]
                conv = adapter.fetch_conversation("eyJhbGciOi.test.sig", "c1")
            self.assertEqual(conv.provider, "grok")
            self.assertEqual(len(conv.messages), 2)

    def test_to_unified(self):
        conv = GrokAdapter().to_unified(
            {
                "id": "g1",
                "title": "T",
                "messages": [
                    {"role": "user", "content": "Q"},
                    {"role": "assistant", "content": "A"},
                ],
            }
        )
        self.assertEqual(conv.id, "g1")
        self.assertEqual(conv.messages[0].content_md, "Q")


if __name__ == "__main__":
    unittest.main()
