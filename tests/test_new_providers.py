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
            out = adapter.list_conversations("__login_type__=x", deep=False)
        self.assertEqual(len(out), 5)
        self.assertEqual(out[0].id, "synth-0000")
        self.assertTrue(out[0].title.startswith("Synthetic Qwen"))


class ToUnifiedTests(unittest.TestCase):
    def test_deepseek_preserves_thinking(self):
        conv = DeepSeekAdapter().to_unified(
            {
                "id": "c1",
                "title": "T",
                "messages": [
                    {"role": "user", "content": "Q"},
                    {"role": "assistant", "thinking_content": "hmm", "final_answer": "A"},
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
            {"id": "q1", "messages": [
                {"role": "user", "content": "Hi"},
                {"role": "assistant", "content": "Hey"},
            ]}
        )
        self.assertEqual([m.role for m in conv.messages], ["user", "assistant"])


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
        self.assertEqual(kwargs["cookie_names"], ("__login_type__",))
        emb.assert_not_called(); cg.assert_not_called(); cl.assert_not_called()


if __name__ == "__main__":
    unittest.main()
