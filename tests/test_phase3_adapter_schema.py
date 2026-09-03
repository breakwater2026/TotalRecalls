"""Phase 3: unified schema + ProviderAdapter + PerplexityAdapter + export."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from totalrecalls.core.schema import (
    SCHEMA_VERSION,
    AccountInfo,
    Citation,
    ConversationSummary,
    Message,
    UnifiedConversation,
)
from totalrecalls.adapters.base import ProviderAdapter, get_adapter, list_provider_ids
from totalrecalls.adapters.perplexity.adapter import PerplexityAdapter
from totalrecalls.core.unified_export import (
    render_unified_markdown,
    write_unified_conversation,
    conversation_turn_ranges,
    select_unified_messages,
    write_selected_unified_conversation,
    conversation_rel_path,
    export_via_adapter,
)


class SchemaTests(unittest.TestCase):
    def test_unified_roundtrip_dict(self):
        conv = UnifiedConversation(
            provider="perplexity",
            account=AccountInfo(email="a@b.com", external_id="u1"),
            id="thread-1",
            title="Hello",
            folder="Home",
            messages=[
                Message(role="user", content_md="Hi?", created_at="2026-01-01"),
                Message(
                    role="assistant",
                    content_md="Hello!",
                    citations=[Citation(title="T", url="https://ex.com", snippet="s")],
                ),
            ],
        )
        d = conv.to_dict()
        self.assertEqual(d["schema_version"], SCHEMA_VERSION)
        self.assertEqual(d["provider"], "perplexity")
        self.assertEqual(d["conversation"]["id"], "thread-1")
        self.assertEqual(len(d["conversation"]["messages"]), 2)
        back = UnifiedConversation.from_dict(d)
        self.assertEqual(back.id, "thread-1")
        self.assertEqual(back.messages[1].citations[0].url, "https://ex.com")
        self.assertEqual(back.account.email, "a@b.com")

    def test_summary_fields(self):
        s = ConversationSummary(id="x", title="T", folder="Space A", updated_at="t")
        self.assertEqual(s.id, "x")
        self.assertEqual(s.folder, "Space A")


class AdapterRegistryTests(unittest.TestCase):
    def test_perplexity_registered(self):
        self.assertIn("perplexity", list_provider_ids())
        a = get_adapter("perplexity")
        self.assertIsInstance(a, PerplexityAdapter)
        self.assertEqual(a.id, "perplexity")
        self.assertTrue(a.display_name)

    def test_unknown_provider_raises(self):
        with self.assertRaises(KeyError):
            get_adapter("nope-provider")

    def test_adapter_satisfies_protocol(self):
        a = PerplexityAdapter()
        # Structural: required attributes/methods
        self.assertTrue(hasattr(a, "list_conversations"))
        self.assertTrue(hasattr(a, "fetch_conversation"))
        self.assertTrue(hasattr(a, "validate"))


class PerplexityAdapterTests(unittest.TestCase):
    def test_to_unified_from_detail_and_summary(self):
        adapter = PerplexityAdapter()
        summary = ConversationSummary(
            id="uuid-1",
            title="List title",
            folder="TRADING",
            updated_at="2026-02-01",
            raw={"collection": {"title": "TRADING"}},
        )
        detail = {
            "thread_metadata": {
                "title": "Meta title",
                "uuid": "uuid-1",
                "created_at": "2026-01-01",
                "updated_at": "2026-02-01",
            },
            "entries": [
                {
                    "uuid": "e1",
                    "query_str": "What is futures?",
                    "display_model": "pplx",
                    "entry_created_datetime": "2026-01-01",
                    "blocks": [
                        {
                            "intended_usage": "ask_text_0_markdown",
                            "markdown_block": {"answer": "Derivatives."},
                        },
                        {
                            "intended_usage": "web_results",
                            "web_result_block": {
                                "web_results": [
                                    {"name": "Wiki", "url": "https://w.example", "snippet": "s"}
                                ]
                            },
                        },
                    ],
                }
            ],
        }
        conv = adapter.to_unified(detail, summary=summary, account=AccountInfo(email="u@x.com"))
        self.assertEqual(conv.provider, "perplexity")
        self.assertEqual(conv.id, "uuid-1")
        self.assertEqual(conv.title, "Meta title")
        self.assertEqual(conv.folder, "TRADING")
        self.assertEqual(conv.account.email, "u@x.com")
        self.assertEqual(len(conv.messages), 2)
        self.assertEqual(conv.messages[0].role, "user")
        self.assertEqual(conv.messages[0].content_md, "What is futures?")
        self.assertEqual(conv.messages[1].role, "assistant")
        self.assertIn("Derivatives", conv.messages[1].content_md)
        self.assertEqual(conv.messages[1].citations[0].title, "Wiki")

    def test_list_conversations_maps_summary(self):
        adapter = PerplexityAdapter()
        fake = [
            {
                "uuid": "a",
                "title": "One",
                "last_query_datetime": "t1",
                "collection": {"title": "SpaceX"},
            },
            {"uuid": "b", "slug": "two", "collection": {}},
        ]
        with patch("totalrecalls.adapters.perplexity.adapter.list_threads", return_value=fake):
            out = adapter.list_conversations("tok", deep=False)
        self.assertEqual(len(out), 2)
        self.assertEqual(out[0].id, "a")
        self.assertEqual(out[0].folder, "SpaceX")
        self.assertEqual(out[1].id, "b")
        self.assertEqual(out[1].title, "two")

    def test_validate_maps_account(self):
        adapter = PerplexityAdapter()
        with patch(
            "totalrecalls.adapters.perplexity.adapter.validate_session",
            return_value={"user": {"email": "e@x.com", "id": "99"}},
        ):
            acct = adapter.validate("tok")
        self.assertEqual(acct.email, "e@x.com")
        self.assertEqual(acct.external_id, "99")


class UnifiedExportTests(unittest.TestCase):
    def test_rel_path_uses_library_provider_folder(self):
        conv = UnifiedConversation(
            provider="perplexity",
            id="aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
            title="Hello World",
            folder="Home",
        )
        rel = conversation_rel_path(conv).replace("\\", "/")
        self.assertTrue(rel.startswith("Library/perplexity/"))
        self.assertIn("Home", rel)
        self.assertIn("Hello World", rel)
        self.assertIn("aaaaaaaa", rel)
        # The leaf must be prefixed with an 'undated' marker when no timestamp
        # is set on the conversation, so the folder name sorts predictably.
        self.assertIn("undated", rel)

    def test_rel_path_prefixes_occurred_timestamp_when_available(self):
        conv = UnifiedConversation(
            provider="perplexity",
            id="aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
            title="Hello World",
            folder="Home",
            created_at="2024-02-18T14:32:00+00:00",
        )
        rel = conversation_rel_path(conv).replace("\\", "/")
        # Slug form: YYYY-MM-DD HH-MM (filename-safe, hyphen not colon)
        self.assertIn("2024-02-18 14-32", rel)
        # Display form: YYYY-MM-DD HH:MM (human-readable, with colon)
        from totalrecalls.core.unified_export import conversation_occurred_display
        self.assertEqual(conversation_occurred_display(conv), "2024-02-18 14:32")

    def test_rel_path_falls_back_to_updated_at(self):
        conv = UnifiedConversation(
            provider="perplexity",
            id="aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
            title="Hello World",
            folder="Home",
            updated_at="2025-01-09T09:00:00Z",
        )
        rel = conversation_rel_path(conv).replace("\\", "/")
        self.assertIn("2025-01-09 09-00", rel)
        self.assertNotIn("undated", rel)

    def test_write_unified_conversation_files(self):
        conv = UnifiedConversation(
            provider="chatgpt",
            account=AccountInfo(email="u@x.com"),
            id="bbbbbbbb-bbbb-cccc-dddd-eeeeeeeeeeee",
            title="Sample",
            folder="Projects",
            messages=[
                Message(role="user", content_md="Q"),
                Message(role="assistant", content_md="A", citations=[
                    Citation(title="S", url="https://s.example")
                ]),
            ],
        )
        with tempfile.TemporaryDirectory() as tmp:
            rec = write_unified_conversation(tmp, conv)
            folder = Path(tmp) / rec["rel_path"].replace("/", "\\") if "\\" in str(Path(tmp)) else Path(tmp) / rec["rel_path"]
            # normalize
            folder = Path(tmp).joinpath(*rec["rel_path"].split("/"))
            self.assertTrue(folder.is_dir())
            self.assertTrue((folder / "conversation.md").is_file())
            self.assertTrue((folder / "conversation.json").is_file())
            md = (folder / "conversation.md").read_text(encoding="utf-8")
            self.assertIn("Sample", md)
            self.assertIn("Q", md)
            self.assertIn("A", md)
            self.assertIn("https://s.example", md)
            data = json.loads((folder / "conversation.json").read_text(encoding="utf-8"))
            self.assertEqual(data["provider"], "chatgpt")
            self.assertEqual(data["conversation"]["id"], conv.id)

    def test_render_unified_markdown_has_roles(self):
        conv = UnifiedConversation(
            provider="perplexity",
            id="x",
            title="T",
            messages=[
                Message(role="user", content_md="Question"),
                Message(role="assistant", content_md="Answer"),
            ],
        )
        md = render_unified_markdown(conv)
        self.assertIn("# T", md)
        self.assertIn("Question", md)
        self.assertIn("Answer", md)

    def test_selection_validates_indexes_and_groups_turns(self):
        conv = UnifiedConversation(
            provider="perplexity",
            id="selection",
            title="Selection",
            messages=[
                Message(role="user", content_md="First question"),
                Message(role="assistant", content_md="First answer"),
                Message(role="user", content_md="Second question"),
            ],
        )
        groups = conversation_turn_ranges(conv)
        self.assertEqual([g["indexes"] for g in groups], [[0, 1], [2]])
        selected, indexes = select_unified_messages(conv, [2, 0, 2])
        self.assertEqual(indexes, [0, 2])
        self.assertEqual([m.content_md for m in selected.messages], ["First question", "Second question"])
        with self.assertRaises(ValueError):
            select_unified_messages(conv, [])
        with self.assertRaises(ValueError):
            select_unified_messages(conv, [99])

    def test_write_selected_conversation_keeps_original_untouched(self):
        conv = UnifiedConversation(
            provider="chatgpt",
            id="selection-id",
            title="Selected",
            messages=[
                Message(role="user", content_md="Keep"),
                Message(role="assistant", content_md="Drop"),
                Message(role="user", content_md="Keep too"),
            ],
        )
        with tempfile.TemporaryDirectory() as tmp:
            result = write_selected_unified_conversation(tmp, conv, [0, 2], source="Library/chatgpt/conversation.json")
            self.assertTrue(Path(result["markdown_path"]).is_file())
            payload = json.loads(Path(result["json_path"]).read_text(encoding="utf-8"))
            self.assertEqual(payload["selection"]["message_indexes"], [0, 2])
            self.assertEqual(len(payload["conversation"]["messages"]), 2)
            self.assertNotIn("Drop", Path(result["markdown_path"]).read_text(encoding="utf-8"))

    def test_export_via_adapter_writes_library_tree(self):
        adapter = PerplexityAdapter()
        summary = ConversationSummary(id="cccccccc-cccc-cccc-cccc-cccccccccccc", title="Only", folder="Home")
        detail = {
            "thread_metadata": {"title": "Only", "uuid": summary.id},
            "entries": [
                {
                    "uuid": "e1",
                    "query_str": "Hi",
                    "blocks": [
                        {
                            "intended_usage": "ask_text_0_markdown",
                            "markdown_block": {"answer": "Yo"},
                        }
                    ],
                }
            ],
        }

        def fake_list(cred, *, deep=False):
            return [summary]

        def fake_fetch(cred, cid):
            self.assertEqual(cid, summary.id)
            return adapter.to_unified(detail, summary=summary, account=AccountInfo(email="a@b.com"))

        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(adapter, "list_conversations", side_effect=fake_list), \
                 patch.object(adapter, "fetch_conversation", side_effect=fake_fetch), \
                 patch.object(adapter, "validate", return_value=AccountInfo(email="a@b.com")):
                result = export_via_adapter(
                    adapter,
                    credential="tok",
                    outdir=tmp,
                    deep=True,
                    refresh=True,
                )
            self.assertEqual(result["exported"], 1)
            self.assertEqual(result["failed"], 0)
            lib = Path(tmp) / "Library" / "perplexity"
            self.assertTrue(lib.is_dir())
            # at least one conversation.json under tree
            jsons = list(lib.rglob("conversation.json"))
            self.assertEqual(len(jsons), 1)
            payload = json.loads(jsons[0].read_text(encoding="utf-8"))
            self.assertEqual(payload["provider"], "perplexity")
            self.assertTrue((Path(tmp) / "manifest.json").is_file())
            self.assertTrue((Path(tmp) / "README.md").is_file())

    def test_export_via_adapter_latest_only_selects_newest(self):
        adapter = PerplexityAdapter()
        old = ConversationSummary(
            id="old", title="Old", updated_at="2024-01-01T00:00:00Z", folder="Home"
        )
        new = ConversationSummary(
            id="new", title="New", updated_at="2024-02-01T00:00:00Z", folder="Home"
        )

        def fake_list(cred, *, deep=False):
            return [old, new]

        def fake_fetch(cred, cid):
            return UnifiedConversation(
                provider="perplexity",
                account=AccountInfo(email="a@b.com"),
                id=cid,
                title=cid,
                folder="Home",
                messages=[Message(role="assistant", content_md="Answer")],
            )

        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(adapter, "list_conversations", side_effect=fake_list), \
                 patch.object(adapter, "fetch_conversation", side_effect=fake_fetch), \
                 patch.object(adapter, "validate", return_value=AccountInfo(email="a@b.com")):
                result = export_via_adapter(
                    adapter,
                    credential="tok",
                    outdir=tmp,
                    latest_only=True,
                )
        self.assertEqual(result["total"], 1)
        self.assertEqual(result["records"][0]["id"], "new")


if __name__ == "__main__":
    unittest.main()
