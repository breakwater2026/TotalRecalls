import json
import shutil
import unittest
import uuid
from pathlib import Path

from totalrecalls.core.local_archive import (
    build_archive_index,
    execute_backup,
    load_backup_state,
    plan_incremental_backup,
    search_archive,
)


class LocalArchiveSearchTests(unittest.TestCase):
    def setUp(self):
        self.root = Path.cwd() / f".test_local_archive_{uuid.uuid4().hex}"
        self.root.mkdir()

    def tearDown(self):
        shutil.rmtree(self.root, ignore_errors=True)

    def test_indexes_json_and_markdown_and_searches_case_insensitively(self):
        conversation = self.root / "Library" / "Perplexity" / "Home" / "one"
        conversation.mkdir(parents=True)
        (conversation / "conversation.json").write_text(
            json.dumps(
                {
                    "provider": "Perplexity",
                    "conversation": {
                        "title": "Cloud Costs",
                        "messages": [
                            {"role": "user", "content_md": "How can I reduce GCP spend?"},
                            {"role": "assistant", "content_md": "Use committed use discounts."},
                        ],
                    },
                }
            ),
            encoding="utf-8",
        )
        (conversation / "conversation.md").write_text(
            "# Cloud Costs\n\n- **Provider:** Perplexity\n\nGCP spend guidance",
            encoding="utf-8",
        )
        legacy = self.root / "old" / "notes.md"
        legacy.parent.mkdir()
        legacy.write_text(
            "# Local Notes\n\n- **Provider:** Gemini\n\nA private archive entry",
            encoding="utf-8",
        )

        index = build_archive_index(self.root)
        self.assertEqual(len(index.records), 2)
        self.assertEqual(search_archive(self.root, "CLOUD")[0].title, "Cloud Costs")
        self.assertEqual(search_archive(self.root, "PERPLEXITY")[0].provider, "Perplexity")
        self.assertEqual(search_archive(self.root, "committed use")[0].title, "Cloud Costs")
        self.assertEqual(search_archive(self.root, "PRIVATE", provider="gem")[0].title, "Local Notes")

    def test_malformed_json_falls_back_to_markdown(self):
        folder = self.root / "Library" / "Claude" / "Home" / "broken"
        folder.mkdir(parents=True)
        (folder / "conversation.json").write_text("{not json", encoding="utf-8")
        (folder / "conversation.md").write_text(
            "# Recovery Plan\n\n- **Provider:** Claude\n\nKeep this searchable.",
            encoding="utf-8",
        )

        record = build_archive_index(self.root).records[0]
        self.assertEqual(record.title, "Recovery Plan")
        self.assertEqual(record.provider, "Claude")
        self.assertIn("searchable", record.content)


class IncrementalBackupTests(unittest.TestCase):
    def setUp(self):
        self.root = Path.cwd() / f".test_local_backup_{uuid.uuid4().hex}"
        self.source = self.root / "archive"
        self.destination = self.root / "backup"
        self.source.mkdir(parents=True)

    def tearDown(self):
        shutil.rmtree(self.root, ignore_errors=True)

    def test_incremental_plan_executes_and_resumes(self):
        (self.source / "conversation.json").write_text('{"title":"One"}', encoding="utf-8")
        (self.source / "nested").mkdir()
        (self.source / "nested" / "conversation.md").write_text("# Two", encoding="utf-8")

        first = plan_incremental_backup(self.source, self.destination)
        self.assertEqual(first.pending_count, 2)
        self.assertEqual(len(execute_backup(first)), 2)
        state = load_backup_state(self.destination / ".totalrecalls-backup-state.json")
        self.assertEqual(set(state.completed), {"conversation.json", "nested/conversation.md"})

        second = plan_incremental_backup(self.source, self.destination)
        self.assertEqual(second.pending_count, 0)
        self.assertEqual(len(second.skipped), 2)

        (self.source / "nested" / "conversation.md").write_text("# Two, revised", encoding="utf-8")
        third = plan_incremental_backup(self.source, self.destination)
        self.assertEqual(third.pending_count, 1)
        self.assertEqual(third.items[0].relative_path, "nested/conversation.md")
        execute_backup(third)
        self.assertEqual(
            (self.destination / "nested" / "conversation.md").read_text(encoding="utf-8"),
            "# Two, revised",
        )

    def test_backup_destination_inside_source_is_rejected(self):
        with self.assertRaises(ValueError):
            plan_incremental_backup(self.source, self.source / "backup")


if __name__ == "__main__":
    unittest.main()
