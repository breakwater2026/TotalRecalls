from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from totalrecalls.browser_handoff import (
    HANDOFF_PROTOCOL,
    HandoffError,
    conversation_from_handoff,
    import_handoff,
)


def handoff(**overrides):
    payload = {
        "protocol": HANDOFF_PROTOCOL,
        "version": 1,
        "provider": "chatgpt",
        "source": {"url": "https://chatgpt.com/c/current", "provider": "chatgpt"},
        "conversation": {
            "id": "conversation-1",
            "title": "Current chat",
            "created_at": "2026-09-02T18:00:00Z",
            "updated_at": "2026-09-02T19:00:00Z",
            "messages": [
                {"role": "user", "content": "What changed?"},
                {"role": "assistant", "content": "The handoff works.", "model": "test-model"},
            ],
        },
    }
    payload.update(overrides)
    return payload


class BrowserHandoffTests(unittest.TestCase):
    def test_normalizes_content_and_preserves_source(self):
        conversation = conversation_from_handoff(handoff())
        self.assertEqual(conversation.provider, "chatgpt")
        self.assertEqual(conversation.messages[0].content_md, "What changed?")
        self.assertEqual(conversation.messages[1].model, "test-model")
        self.assertEqual(
            conversation.raw["handoff"]["source"]["url"],
            "https://chatgpt.com/c/current",
        )

    def test_derives_stable_id_when_missing(self):
        payload = handoff()
        del payload["conversation"]["id"]
        first = conversation_from_handoff(payload)
        second = conversation_from_handoff(payload)
        self.assertTrue(first.id.startswith("browser-"))
        self.assertEqual(first.id, second.id)

    def test_rejects_wrong_protocol_and_empty_messages(self):
        with self.assertRaises(HandoffError):
            conversation_from_handoff(handoff(protocol="other"))
        with self.assertRaises(HandoffError):
            conversation_from_handoff(handoff(conversation={"messages": []}))

    def test_import_writes_standard_library_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            record = import_handoff(handoff(), tmp)
            folder = Path(tmp).joinpath(*record["rel_path"].split("/"))
            self.assertTrue((folder / "conversation.json").is_file())
            self.assertTrue((folder / "conversation.md").is_file())
            data = json.loads((folder / "conversation.json").read_text(encoding="utf-8"))
            self.assertEqual(data["conversation"]["id"], "conversation-1")
            self.assertIn("The handoff works.", (folder / "conversation.md").read_text(encoding="utf-8"))

    def test_cli_reports_import(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "handoff.json"
            output = Path(tmp) / "library"
            source.write_text(json.dumps(handoff()), encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    "tools/import_browser_handoff.py",
                    str(source),
                    "--output",
                    str(output),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('"imported": true', result.stdout)

