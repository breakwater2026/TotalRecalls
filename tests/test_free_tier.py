"""Cumulative Free Tier allowance and the canonical default export root."""
from __future__ import annotations

import os
import tempfile
import unittest
from unittest.mock import patch

from totalrecalls.core.free_tier import FreeTierUsage
from totalrecalls.core.paths import default_export_root
from totalrecalls.core.schema import (
    AccountInfo,
    ConversationSummary,
    Message,
    UnifiedConversation,
)
from totalrecalls.core.unified_export import export_via_adapter


class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="tr_free_")

    def test_record_persists_and_counts(self):
        usage = FreeTierUsage(self.tmp)
        usage.record("chatgpt", ["a", "b"])
        again = FreeTierUsage(self.tmp)
        self.assertEqual(again.count("chatgpt"), 2)
        self.assertTrue(again.is_used("ChatGPT", "a"))
        self.assertEqual(again.remaining("chatgpt", 5), 3)

    def test_consume_blocks_after_limit(self):
        usage = FreeTierUsage(self.tmp)
        for i in range(5):
            allowed, reason = usage.consume("chatgpt", f"c{i}", 5)
            self.assertTrue(allowed, reason)
        allowed, reason = usage.consume("chatgpt", "c5", 5)
        self.assertFalse(allowed)
        self.assertIn("Upgrade to Pro", reason)
        self.assertEqual(usage.count("chatgpt"), 5)

    def test_consume_is_idempotent(self):
        usage = FreeTierUsage(self.tmp)
        self.assertTrue(usage.consume("chatgpt", "c1", 1)[0])
        self.assertTrue(usage.consume("chatgpt", "c1", 1)[0])
        self.assertEqual(usage.count("chatgpt"), 1)

    def test_providers_are_independent(self):
        usage = FreeTierUsage(self.tmp)
        for i in range(5):
            usage.consume("chatgpt", f"c{i}", 5)
        self.assertTrue(usage.consume("claude", "x", 5)[0])


class FakeAdapter:
    id = "chatgpt"
    display_name = "ChatGPT"

    def __init__(self, count: int):
        self.count = count
        self.fetched: list[str] = []

    def validate(self, credential):
        return AccountInfo(email="audit@example.com")

    def list_conversations(self, credential, *, deep=False, **kwargs):
        return [
            ConversationSummary(
                id=f"c{i}",
                title=f"Chat {i}",
                created_at=f"2026-11-{i + 1:02d}T10:00:00+00:00",
                folder="Home",
            )
            for i in range(self.count)
        ]

    def fetch_conversation(self, credential, conv_id):
        self.fetched.append(conv_id)
        return UnifiedConversation(
            id=conv_id,
            provider=self.id,
            title=f"Chat {conv_id}",
            created_at="2026-11-01T10:00:00+00:00",
            messages=[Message(role="user", content_md="hello")],
        )


class ExportCapTests(unittest.TestCase):
    def test_cumulative_cap_across_runs(self):
        outdir = tempfile.mkdtemp(prefix="tr_export_")
        usage = FreeTierUsage(outdir)

        first = FakeAdapter(8)
        result = export_via_adapter(first, "token", outdir, usage=usage, provider_limit=5)
        self.assertEqual(result["exported"], 5)
        self.assertEqual(usage.count("chatgpt"), 5)

        second = FakeAdapter(8)
        result = export_via_adapter(second, "token", outdir, usage=usage, provider_limit=5)
        self.assertEqual(result["exported"], 0)
        self.assertEqual(second.fetched, [])

    def test_remaining_slots_fill_on_later_run(self):
        outdir = tempfile.mkdtemp(prefix="tr_export_")
        usage = FreeTierUsage(outdir)
        export_via_adapter(FakeAdapter(3), "token", outdir, usage=usage, provider_limit=5)
        self.assertEqual(usage.count("chatgpt"), 3)

        second = FakeAdapter(8)
        result = export_via_adapter(second, "token", outdir, usage=usage, provider_limit=5)
        self.assertEqual(result["exported"], 2)
        self.assertEqual(usage.count("chatgpt"), 5)
        # The first three ids are already counted and must not be re-fetched.
        self.assertEqual(second.fetched, ["c3", "c4"])


class DefaultRootTests(unittest.TestCase):
    def setUp(self):
        self.home = tempfile.mkdtemp(prefix="tr_home_")

    def test_demo_override_wins(self):
        with patch.dict(os.environ, {"TR_DEMO_FOLDER": r"C:\Demo"}):
            self.assertEqual(default_export_root(home=self.home), r"C:\Demo")

    def test_legacy_root_is_not_orphaned(self):
        legacy = os.path.join(self.home, "TotalRecalls-download")
        os.makedirs(legacy)
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("TR_DEMO_FOLDER", None)
            self.assertEqual(
                default_export_root(home=self.home, canonical_root=os.path.join(self.home, "canon")),
                legacy,
            )

    def test_canonical_root_when_writable(self):
        canon = os.path.join(self.home, "canon")
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("TR_DEMO_FOLDER", None)
            self.assertEqual(
                default_export_root(home=self.home, canonical_root=canon), canon
            )

    def test_user_scoped_fallback_when_canonical_blocked(self):
        blocked = os.path.join(self.home, "blocked")
        with open(blocked, "w", encoding="utf-8") as f:
            f.write("not a directory")
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("TR_DEMO_FOLDER", None)
            self.assertEqual(
                default_export_root(home=self.home, canonical_root=blocked),
                os.path.join(self.home, "TotalRecalls"),
            )


if __name__ == "__main__":
    unittest.main()
