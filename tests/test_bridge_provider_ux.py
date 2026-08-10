"""Bridge multi-provider UX: setProvider + chooseTakeoutPath."""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch

from totalrecalls.desktop.bridge import Bridge
from totalrecalls.desktop.js_api import JsApi


class SetProviderTests(unittest.TestCase):
    def test_set_provider_ok_and_push(self):
        b = Bridge(ui_html="<html></html>")
        pushes = []
        with patch.object(b, "_push", side_effect=lambda p: pushes.append(p)):
            r = b.setProvider("gemini")
        self.assertTrue(r.get("ok"))
        self.assertEqual(r.get("provider"), "gemini")
        self.assertEqual(b._provider_id, "gemini")
        self.assertTrue(any(p.get("type") == "provider" and p.get("provider") == "gemini" for p in pushes))

    def test_switch_clears_session(self):
        b = Bridge(ui_html="<html></html>")
        b._provider_id = "perplexity"
        b.token = "tok"
        b.email = "a@b.com"
        b._conversation_count = 2
        pushes = []
        with patch.object(b, "_push", side_effect=lambda p: pushes.append(p)), patch(
            "totalrecalls.desktop.bridge.clear_session"
        ) as cs:
            r = b.setProvider("claude")
        self.assertTrue(r.get("cleared"))
        self.assertIsNone(b.token)
        self.assertIsNone(b.email)
        self.assertEqual(b._conversation_count, 0)
        self.assertTrue(cs.called)
        types = [p.get("type") for p in pushes]
        self.assertIn("disconnected", types)
        self.assertIn("provider", types)

    def test_unknown_provider(self):
        b = Bridge(ui_html="<html></html>")
        with patch.object(b, "_push"):
            r = b.setProvider("not-a-real-provider")
        self.assertFalse(r.get("ok"))


class ChooseTakeoutPathTests(unittest.TestCase):
    def test_jsapi_exposes_method(self):
        api = JsApi(Bridge(ui_html="<html></html>"))
        self.assertTrue(callable(api.chooseTakeoutPath))

    def test_no_window_returns_empty(self):
        b = Bridge(ui_html="<html></html>")
        b._window = None
        self.assertEqual(b.chooseTakeoutPath(), "")

    def test_folder_dialog(self):
        b = Bridge(ui_html="<html></html>")

        class Win:
            def create_file_dialog(self, *a, **k):
                return [r"C:\Takeout"]

        b._window = Win()
        pushes = []
        with patch.object(b, "_push", side_effect=lambda p: pushes.append(p)):
            path = b.chooseTakeoutPath()
        self.assertEqual(path, r"C:\Takeout")
        self.assertTrue(any(p.get("type") == "takeout_path" and p.get("path") == path for p in pushes))

    def test_json_fallback_after_folder_cancel(self):
        b = Bridge(ui_html="<html></html>")

        class Win:
            def __init__(self):
                self.n = 0

            def create_file_dialog(self, *a, **k):
                self.n += 1
                if self.n == 1:
                    return None
                return [r"C:\data\conversations.json"]

        b._window = Win()
        with patch.object(b, "_push"):
            self.assertEqual(b.chooseTakeoutPath(), r"C:\data\conversations.json")


if __name__ == "__main__":
    unittest.main()
