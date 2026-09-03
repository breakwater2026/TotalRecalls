"""Bridge multi-provider UX: setProvider + chooseTakeoutPath."""

from __future__ import annotations

import unittest
import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

from totalrecalls.desktop.bridge import Bridge
from totalrecalls.desktop.js_api import JsApi
from totalrecalls.core.schema import AccountInfo, Citation, Message, UnifiedConversation


class SetProviderTests(unittest.TestCase):
    def test_latest_export_is_exposed(self):
        api = JsApi(Bridge(ui_html="<html></html>"))
        self.assertTrue(callable(api.startLatestExport))
        self.assertTrue(callable(api.exportLatestPdf))
        self.assertTrue(callable(api.listExportedConversations))
        self.assertTrue(callable(api.getExportedConversation))
        self.assertTrue(callable(api.exportSelectedMessages))

    def test_copy_latest_markdown_requires_export(self):
        b = Bridge(ui_html="<html></html>")
        with patch.object(b, "_push") as push:
            result = b.copyLatestMarkdown()
        self.assertFalse(result["ok"])
        push.assert_called_once()

    def test_pdf_requires_an_export(self):
        b = Bridge(ui_html="<html></html>")
        with tempfile.TemporaryDirectory() as tmp, patch.object(b, "_push") as push:
            b._default_folder = tmp
            result = b.exportLatestPdf()
        self.assertFalse(result["ok"])
        self.assertIn("Export a conversation first", result["message"])
        push.assert_called_once()

    def test_pdf_uses_local_headless_browser_and_cleans_print_file(self):
        b = Bridge(ui_html="<html></html>")
        with tempfile.TemporaryDirectory() as tmp:
            markdown_path = Path(tmp) / "conversation.md"
            markdown_path.write_text("# Hello\n\nSensitive text", encoding="utf-8")
            b._default_folder = tmp
            b._last_markdown_path = str(markdown_path)

            def fake_run(command, **_kwargs):
                pdf_arg = next(arg for arg in command if arg.startswith("--print-to-pdf="))
                Path(pdf_arg.split("=", 1)[1]).write_bytes(b"%PDF-test")
                return MagicMock(returncode=0, stdout="", stderr="")

            with patch.object(Bridge, "_find_headless_browser", return_value=r"C:\Edge\msedge.exe"), \
                 patch("totalrecalls.desktop.bridge.subprocess.run", side_effect=fake_run) as run:
                result = b.exportLatestPdf()
            self.assertTrue(result["ok"])
            self.assertTrue(Path(result["path"]).is_file())
            self.assertIn("--headless", run.call_args.args[0])
            self.assertEqual(list(Path(tmp).glob("conversation.md.print-*.html")), [])

    def test_selection_reads_unified_json_and_exports_indexes(self):
        conv = UnifiedConversation(
            provider="perplexity",
            account=AccountInfo(email="a@b.com"),
            id="conv-1",
            title="A conversation",
            messages=[
                Message(role="user", content_md="Question"),
                Message(role="assistant", content_md="Answer"),
            ],
        )
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "Library" / "perplexity" / "home" / "conversation"
            source.mkdir(parents=True)
            json_path = source / "conversation.json"
            json_path.write_text(json.dumps(conv.to_dict()), encoding="utf-8")
            b = Bridge(ui_html="<html></html>")
            b._default_folder = tmp
            rows = b.listExportedConversations()
            self.assertEqual(len(rows), 1)
            detail = b.getExportedConversation(rows[0]["path"])
            self.assertEqual([m["turn"] for m in detail["messages"]], [1, 1])
            result = b.exportSelectedMessages(rows[0]["path"], [1])
            self.assertTrue(result["ok"])
            self.assertTrue(Path(result["json_path"]).is_file())
            selected = json.loads(Path(result["json_path"]).read_text(encoding="utf-8"))
            self.assertEqual(len(selected["conversation"]["messages"]), 1)
            self.assertEqual(selected["conversation"]["messages"][0]["content_md"], "Answer")

    def test_conversation_preview_includes_metadata_counts_and_size(self):
        conv = UnifiedConversation(
            provider="chatgpt",
            account=AccountInfo(email="a@b.com"),
            id="conv-meta",
            title="Media and sources",
            messages=[
                Message(
                    role="user",
                    content_md="Look at ![chart](https://example.test/chart.png)",
                ),
                Message(
                    role="assistant",
                    content_md="Answer",
                    citations=[
                        Citation(title="Source", url="https://example.test")
                    ],
                ),
            ],
        )
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "Library" / "chatgpt" / "home" / "conversation"
            source.mkdir(parents=True)
            json_path = source / "conversation.json"
            payload = conv.to_dict()
            json_path.write_text(json.dumps(payload), encoding="utf-8")
            (source / "conversation.md").write_text("# preview\n", encoding="utf-8")
            b = Bridge(ui_html="<html></html>")
            b._default_folder = tmp

            row = b.listExportedConversations()[0]
            self.assertEqual(row["title"], "Media and sources")
            self.assertEqual(row["provider"], "chatgpt")
            self.assertEqual(row["message_count"], 2)
            self.assertEqual(row["media_count"], 1)
            self.assertEqual(row["citation_count"], 1)
            self.assertGreater(row["size_bytes"], 0)
            self.assertTrue(row["size"])

            detail = b.getExportedConversation(row["path"])
            self.assertEqual(detail["metadata"]["message_count"], 2)
            self.assertEqual(detail["metadata"]["media_count"], 1)
            self.assertEqual(detail["metadata"]["citation_count"], 1)
            self.assertEqual(detail["metadata"]["size_bytes"], row["size_bytes"])

    def test_selection_rejects_paths_outside_export_root(self):
        b = Bridge(ui_html="<html></html>")
        with tempfile.TemporaryDirectory() as tmp, patch.object(b, "_push"):
            b._default_folder = tmp
            result = b.getExportedConversation("../conversation.json")
        self.assertFalse(result["ok"])
        self.assertIn("exported library", result["message"])

    def test_provider_list_has_no_beta_labels(self):
        b = Bridge(ui_html="<html></html>")
        providers = b.listProviders()
        self.assertFalse(
            any(provider.get("note") == "beta" for provider in providers)
        )

    def test_set_provider_ok_and_push(self):
        b = Bridge(ui_html="<html></html>")
        pushes = []
        with patch.object(b, "_push", side_effect=lambda p: pushes.append(p)):
            r = b.setProvider("chatgpt")
        self.assertTrue(r.get("ok"))
        self.assertEqual(r.get("provider"), "chatgpt")
        self.assertEqual(b._provider_id, "chatgpt")
        self.assertTrue(any(p.get("type") == "provider" and p.get("provider") == "chatgpt" for p in pushes))

    def test_pro_only_provider_blocked_when_free(self):
        b = Bridge(ui_html="<html></html>")
        with patch.object(b, "_push"), patch("totalrecalls.licensing.is_pro", return_value=False):
            r = b.setProvider("gemini")
        self.assertFalse(r.get("ok"))
        self.assertNotEqual(b._provider_id, "gemini")

    def test_pro_only_provider_allowed_when_pro(self):
        b = Bridge(ui_html="<html></html>")
        with patch.object(b, "_push"), patch("totalrecalls.licensing.is_pro", return_value=True):
            r = b.setProvider("gemini")
        self.assertTrue(r.get("ok"))
        self.assertEqual(b._provider_id, "gemini")

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
