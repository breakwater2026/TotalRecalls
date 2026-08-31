"""DeepSeek, Mistral, Qwen adapter + login-wiring tests.

Covers the three providers added in the 8-provider release: registry
registration, credential (bearer vs cookie) resolution, list/fetch mapping
against the synthetic fixtures, and the desktop login-flow wiring.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from totalrecalls.adapters.base import get_adapter, list_provider_ids
from totalrecalls.adapters.deepseek.adapter import DeepSeekAdapter, _resolve_auth
from totalrecalls.adapters.mistral.adapter import MistralAdapter
from totalrecalls.adapters.qwen.adapter import QwenChatAdapter
from totalrecalls.core.schema import AccountInfo
from totalrecalls.desktop.bridge import Bridge

FIXTURES = Path(__file__).parent / "fixtures"


def _load_fixture(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))["response"]


class RegistrationTests(unittest.TestCase):
    def test_all_eight_providers_registered(self):
        ids = list_provider_ids()
        for pid in ("perplexity", "chatgpt", "claude", "gemini", "grok",
                    "deepseek", "mistral", "qwen"):
            self.assertIn(pid, ids)

    def test_new_adapters_instantiate(self):
        self.assertIsInstance(get_adapter("deepseek"), DeepSeekAdapter)
        self.assertIsInstance(get_adapter("mistral"), MistralAdapter)
        self.assertIsInstance(get_adapter("qwen"), QwenChatAdapter)

    def test_new_adapters_have_ids_and_names(self):
        self.assertEqual(get_adapter("deepseek").id, "deepseek")
        self.assertEqual(get_adapter("mistral").id, "mistral")
        self.assertEqual(get_adapter("qwen").id, "qwen")
        for pid in ("deepseek", "mistral", "qwen"):
            self.assertTrue(get_adapter(pid).display_name)


class DeepSeekAuthTests(unittest.TestCase):
    def test_resolve_bearer_jwt(self):
        token, cookie = _resolve_auth("eyJhbGciOi.eyJzdWIi.sig")
        self.assertEqual(token, "eyJhbGciOi.eyJzdWIi.sig")
        self.assertIsNone(cookie)

    def test_resolve_bearer_prefixed(self):
        token, cookie = _resolve_auth("Bearer sm1234567890abcdef")
        self.assertEqual(token, "sm1234567890abcdef")
        self.assertIsNone(cookie)

    def test_resolve_opaque_non_jwt_bearer(self):
        # DeepSeek's bearer token is NOT a JWT — no '=' or ';' present.
        token, cookie = _resolve_auth("smxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        self.assertEqual(token, "smxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        self.assertIsNone(cookie)

    def test_resolve_cookie(self):
        token, cookie = _resolve_auth("ds_session_id=abc123; other=x")
        self.assertIsNone(token)
        self.assertEqual(cookie, "ds_session_id=abc123; other=x")

    def test_resolve_empty_raises(self):
        with self.assertRaises(Exception):
            _resolve_auth("")


class ListMappingTests(unittest.TestCase):
    def _mock_request(self, adapter_module, fixture):
        req = MagicMock()
        req.return_value = (200, _load_fixture(fixture))
        return patch(f"{adapter_module}.request", req)

    def test_deepseek_list_maps_fixture(self):
        adapter = DeepSeekAdapter()
        with self._mock_request("totalrecalls.adapters.deepseek.adapter", "deepseek/list_synthetic.json"):
            out = adapter.list_conversations("smxxx", deep=False)
        self.assertEqual(len(out), 5)
        self.assertEqual(out[0].id, "synth-0000")
        self.assertTrue(out[0].title.startswith("Synthetic DeepSeek"))

    def test_mistral_list_maps_fixture(self):
        adapter = MistralAdapter()
        with self._mock_request("totalrecalls.adapters.mistral.adapter", "mistral/list_synthetic.json"):
            out = adapter.list_conversations("ory_session_xyz", deep=False)
        self.assertEqual(len(out), 5)
        self.assertEqual(out[0].id, "synth-0000")
        self.assertTrue(out[0].title.startswith("Synthetic Mistral"))

    def test_qwen_list_maps_fixture(self):
        adapter = QwenChatAdapter()
        with self._mock_request("totalrecalls.adapters.qwen.adapter", "qwen/list_synthetic.json"):
            out = adapter.list_conversations("xlly_s=deadbeef", deep=False)
        self.assertEqual(len(out), 5)
        self.assertEqual(out[0].id, "synth-0000")
        self.assertTrue(out[0].title.startswith("Synthetic Qwen"))


class ToUnifiedTests(unittest.TestCase):
    def test_deepseek_preserves_thinking(self):
        conv = DeepSeekAdapter().to_unified(
            {
                "chat_session": {"id": "c1", "title": "T", "model_type": "default"},
                "chat_messages": [
                    {"message_id": 1, "role": "USER", "fragments": [{"type": "REQUEST", "content": "Q"}]},
                    {"message_id": 2, "role": "ASSISTANT", "fragments": [
                        {"type": "THINK", "content": "hmm"},
                        {"type": "RESPONSE", "content": "A"},
                    ]},
                ],
            },
            account=AccountInfo(email="d@x.com"),
        )
        self.assertEqual(conv.provider, "deepseek")
        self.assertEqual(conv.messages[0].role, "user")
        self.assertIn("Thinking", conv.messages[1].content_md)
        self.assertIn("A", conv.messages[1].content_md)

    def test_mistral_to_unified_roles(self):
        conv = MistralAdapter().to_unified(
            {"id": "m1", "messages": [
                {"role": "user", "content": "Hi"},
                {"role": "assistant", "content": "Hey"},
            ]}
        )
        self.assertEqual(conv.id, "m1")
        self.assertEqual([m.role for m in conv.messages], ["user", "assistant"])

    def test_qwen_to_unified_roles(self):
        conv = QwenChatAdapter().to_unified(
            {
                "id": "q1",
                "title": "Qwen demo",
                "history": {
                    "currentId": "a1",
                    "messages": {
                        "u1": {"id": "u1", "role": "user", "content": "Hi",
                               "parentId": None, "childrenIds": ["a1"]},
                        "a1": {"id": "a1", "role": "assistant", "parentId": "u1",
                               "childrenIds": [],
                               "content_list": [
                                   {"phase": "thinking_summary", "content": "thinking..."},
                                   {"phase": "answer", "content": "Hey"},
                               ]},
                    },
                },
            }
        )
        self.assertEqual(conv.id, "q1")
        self.assertEqual([m.role for m in conv.messages], ["user", "assistant"])
        # Only the "answer" phase is surfaced, not the thinking summary.
        self.assertEqual(conv.messages[1].content_md, "Hey")


class LoginWiringTests(unittest.TestCase):
    """connect() must route the 3 new providers to the generic cookie login."""

    def _run_connect(self, provider):
        b = Bridge(ui_html="<html></html>")
        b._provider_id = provider
        with patch.object(b, "_push"), patch.object(
            b, "_start_generic_cookie_login"
        ) as login, patch.object(b, "_start_embedded_login") as emb, \
             patch.object(b, "_start_chatgpt_embedded_login") as cg, \
             patch.object(b, "_start_claude_embedded_login") as cl:
            b.connect()
            return login, emb, cg, cl

    def test_deepseek_routes_to_generic_cookie_login(self):
        login, emb, cg, cl = self._run_connect("deepseek")
        login.assert_called_once()
        kwargs = login.call_args.kwargs
        self.assertEqual(kwargs["start_url"], "https://chat.deepseek.com/")
        self.assertEqual(kwargs["host_substr"], "deepseek.com")
        self.assertTrue(kwargs["prefer_bearer"])
        self.assertEqual(kwargs["cookie_names"], ("ds_session_id",))
        emb.assert_not_called(); cg.assert_not_called(); cl.assert_not_called()

    def test_mistral_routes_to_generic_cookie_login(self):
        login, emb, cg, cl = self._run_connect("mistral")
        login.assert_called_once()
        kwargs = login.call_args.kwargs
        self.assertEqual(kwargs["start_url"], "https://chat.mistral.ai/")
        self.assertEqual(kwargs["cookie_filter"], "ory_session_")
        self.assertFalse(kwargs["prefer_bearer"])
        emb.assert_not_called(); cg.assert_not_called(); cl.assert_not_called()

    def test_qwen_routes_to_generic_cookie_login(self):
        login, emb, cg, cl = self._run_connect("qwen")
        login.assert_called_once()
        kwargs = login.call_args.kwargs
        self.assertEqual(kwargs["start_url"], "https://chat.qwen.ai/")
        self.assertEqual(kwargs["cookie_names"], ("xlly_s",))
        emb.assert_not_called(); cg.assert_not_called(); cl.assert_not_called()


def _env(biz_data):
    """Wrap a biz_data payload in the DeepSeek two-level envelope."""
    return {"code": 0, "msg": "", "data": {"biz_code": 0, "biz_msg": "", "biz_data": biz_data}}


class DeepSeekApiTests(unittest.TestCase):
    """DeepSeek adapter behavior against the verified API surface."""

    def test_validate_users_current(self):
        adapter = DeepSeekAdapter()
        req = MagicMock(return_value=(200, _env({"id": "u1", "email": "d@x.com"})))
        with patch("totalrecalls.adapters.deepseek.adapter.request", req):
            acct = adapter.validate("smxxx")
        self.assertEqual(acct.email, "d@x.com")
        self.assertEqual(acct.external_id, "u1")

    def test_list_follows_keyset_cursor(self):
        adapter = DeepSeekAdapter()
        s0 = {"id": "a", "title": "A", "updated_at": 300.0, "inserted_at": 100.0}
        s1 = {"id": "b", "title": "B", "updated_at": 200.0, "inserted_at": 100.0}
        s2 = {"id": "c", "title": "C", "updated_at": 100.0, "inserted_at": 100.0}
        page1 = _env({"chat_sessions": [s0, s1], "has_more": True})
        page2 = _env({"chat_sessions": [s2], "has_more": False})
        empty = _env({"chat_sessions": [], "has_more": False})
        req = MagicMock(side_effect=[(200, page1), (200, page2), (200, empty)])
        with patch("totalrecalls.adapters.deepseek.adapter.request", req):
            out = adapter.list_conversations("smxxx", deep=True)
        self.assertEqual({o.id for o in out}, {"a", "b", "c"})
        # The second request must carry the keyset cursor from page one.
        second_path = req.call_args_list[1].args[0]
        self.assertIn("lte_cursor.updated_at=", second_path)
        self.assertIn("lte_cursor.id=", second_path)

    def test_fetch_history_messages(self):
        adapter = DeepSeekAdapter()
        payload = _env({
            "chat_session": {"id": "c1", "title": "T", "model_type": "default"},
            "chat_messages": [
                {"message_id": 1, "role": "USER", "fragments": [{"type": "REQUEST", "content": "Hi"}]},
                {"message_id": 2, "role": "ASSISTANT", "fragments": [
                    {"type": "THINK", "content": "hmm"},
                    {"type": "RESPONSE", "content": "Hello",
                     "references": [{"url": "https://x.com", "title": "X"}]},
                ]},
            ],
        })
        req = MagicMock(return_value=(200, payload))
        with patch("totalrecalls.adapters.deepseek.adapter.request", req):
            conv = adapter.fetch_conversation("smxxx", "c1")
        self.assertEqual(conv.id, "c1")
        self.assertEqual(conv.title, "T")
        self.assertEqual([m.role for m in conv.messages], ["user", "assistant"])
        self.assertIn("Hello", conv.messages[1].content_md)
        self.assertIn("Thinking", conv.messages[1].content_md)
        self.assertEqual(conv.messages[1].citations[0].url, "https://x.com")


if __name__ == "__main__":
    unittest.main()
