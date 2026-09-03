import json
import tempfile
import unittest
from pathlib import Path

from totalrecalls.core.chat_import import (
    ImportValidationError,
    load_ai_chat_export,
    parse_ai_chat_export_json,
    parse_ai_chat_export_markdown,
)
from totalrecalls.core.export_reporting import (
    RetryExhaustedError,
    assert_export_integrity,
    run_with_retries,
    verify_export_integrity,
)
from totalrecalls.core.schema import Message, UnifiedConversation
from totalrecalls.core.unified_export import write_unified_conversation


class ChatImportTests(unittest.TestCase):
    def test_chatgpt_mapping_json_preserves_order_and_timestamps(self):
        payload = {
            "title": "Mapping export",
            "create_time": 1700000000,
            "mapping": {
                "root": {"id": "root", "message": None},
                "a": {"message": {"id": "a", "author": {"role": "user"}, "content": {"parts": ["Question"]}, "create_time": 1700000001}},
                "b": {"message": {"id": "b", "author": {"role": "assistant"}, "content": {"parts": ["Answer"]}, "create_time": 1700000002}},
            },
        }
        conv = parse_ai_chat_export_json(payload)[0]
        self.assertEqual(conv.title, "Mapping export")
        self.assertEqual([m.role for m in conv.messages], ["user", "assistant"])
        self.assertEqual(conv.messages[1].external_id, "b")
        self.assertTrue(conv.messages[0].created_at.endswith("+00:00"))

    def test_markdown_roles_and_links(self):
        text = "# A chat\n\n## User\n\nWhat is this?\n\n## Assistant\n\nSee [docs](https://example.test/docs)."
        conv = parse_ai_chat_export_markdown(text, provider="chatgpt")
        self.assertEqual(conv.provider, "chatgpt")
        self.assertEqual(len(conv.messages), 2)
        self.assertEqual(conv.messages[1].citations[0].url, "https://example.test/docs")

    def test_invalid_input_is_not_silently_skipped(self):
        with self.assertRaises(ImportValidationError):
            parse_ai_chat_export_json({"messages": [{"role": "user", "content": "ok"}, {"role": "alien", "content": "bad"}]})
        with self.assertRaises(ImportValidationError):
            parse_ai_chat_export_markdown("# title\n\nNo role headings here.")

    def test_load_path_detects_json_and_markdown(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "chat.json").write_text(json.dumps({"title": "x", "messages": [{"role": "user", "content": "q"}]}), encoding="utf-8")
            (root / "chat.md").write_text("# x\n\n**User:**\nq", encoding="utf-8")
            self.assertEqual(load_ai_chat_export(root / "chat.json")[0].messages[0].content_md, "q")
            self.assertEqual(load_ai_chat_export(root / "chat.md")[0].title, "x")


class ExportReportingTests(unittest.TestCase):
    def test_integrity_report_detects_missing_markdown(self):
        conv = UnifiedConversation(provider="chatgpt", id="id-1", title="T", messages=[Message(role="user", content_md="Q")])
        with tempfile.TemporaryDirectory() as tmp:
            write_unified_conversation(tmp, conv)
            manifest = {"total_threads": 1, "threads": [{"id": "id-1", "path": "Library/chatgpt/Home/undated -- T -- id-1"}]}
            Path(tmp, "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
            folder = next(Path(tmp, "Library").rglob("conversation.md")).parent
            (folder / "conversation.md").unlink()
            report = verify_export_integrity(tmp)
            self.assertFalse(report.ok)
            with self.assertRaises(Exception):
                assert_export_integrity(tmp)

    def test_integrity_accepts_unified_json_and_markdown(self):
        conv = UnifiedConversation(
            provider="chatgpt",
            id="id-2",
            title="T",
            messages=[Message(role="user", content_md="Q"), Message(role="assistant", content_md="A")],
        )
        with tempfile.TemporaryDirectory() as tmp:
            record = write_unified_conversation(tmp, conv)
            Path(tmp, "manifest.json").write_text(
                json.dumps({"total_threads": 1, "threads": [{"id": "id-2", "path": record["rel_path"]}]}),
                encoding="utf-8",
            )
            report = assert_export_integrity(tmp)
            self.assertTrue(report.ok)
            self.assertEqual(report.checked_conversations, 1)
            self.assertEqual(len(report.hashes), 2)

    def test_retry_report_records_transient_failures(self):
        calls = []
        sleeps = []

        def operation():
            calls.append(1)
            if len(calls) < 3:
                raise OSError("temporary")
            return "ok"

        result = run_with_retries(operation, max_attempts=3, backoff_seconds=0.25, sleep=sleeps.append)
        self.assertEqual(result.value, "ok")
        self.assertEqual(result.report.retry_count, 2)
        self.assertEqual(sleeps, [0.25, 0.5])

    def test_retry_exhaustion_keeps_attempt_details(self):
        with self.assertRaises(RetryExhaustedError) as raised:
            run_with_retries(lambda: (_ for _ in ()).throw(TimeoutError("down")), max_attempts=2)
        self.assertEqual(len(raised.exception.report.attempts), 2)
        self.assertTrue(raised.exception.report.exhausted)


if __name__ == "__main__":
    unittest.main()
