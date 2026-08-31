"""Tests for totalrecalls.tools.devtools_probe.

Covers: synthesize, replay (all 3 providers), diff, and ensures the
adapter code path actually runs against a synthetic fixture without
touching the network.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def _run(args: list[str], cwd: Path = REPO) -> subprocess.CompletedProcess:
    """Run the probe as a subprocess so we exercise the real CLI surface."""
    return subprocess.run(
        [sys.executable, "-m", "totalrecalls.tools.devtools_probe", *args],
        cwd=cwd, capture_output=True, text=True, timeout=60,
    )


class SynthesizeTests(unittest.TestCase):
    def test_synthesize_deepseek(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "ds.json"
            r = _run(["synthesize", "--provider", "deepseek", "--out", str(out), "--count", "3"])
            self.assertEqual(r.returncode, 0, r.stderr)
            data = json.loads(out.read_text(encoding="utf-8"))
            self.assertTrue(data["_meta"]["synthetic"])
            self.assertEqual(len(data["response"]["data"]["biz_data"]["chat_sessions"]), 3)

    def test_synthesize_qwen(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "q.json"
            r = _run(["synthesize", "--provider", "qwen", "--out", str(out), "--count", "2"])
            self.assertEqual(r.returncode, 0, r.stderr)
            data = json.loads(out.read_text(encoding="utf-8"))
            items = data["response"]["data"]["list"]
            self.assertEqual(len(items), 2)
            self.assertTrue(items[0]["id"].startswith("synth-"))

    def test_synthesize_mistral(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "m.json"
            r = _run(["synthesize", "--provider", "mistral", "--out", str(out), "--count", "4"])
            self.assertEqual(r.returncode, 0, r.stderr)
            data = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(len(data["response"]["conversations"]), 4)


class ReplayTests(unittest.TestCase):
    """Replay a synthetic fixture through the adapter and verify parsing."""

    def _synth_and_replay(self, provider: str, count: int) -> dict:
        with tempfile.TemporaryDirectory() as d:
            fx = Path(d) / f"{provider}.json"
            r1 = _run(["synthesize", "--provider", provider, "--out", str(fx), "--count", str(count)])
            self.assertEqual(r1.returncode, 0, r1.stderr)
            r2 = _run(["replay", "--provider", provider, "--list-fixture", str(fx)])
            self.assertEqual(r2.returncode, 0, r2.stderr)
            return json.loads(r2.stdout)

    def test_replay_deepseek_parses_synthetic(self):
        out = self._synth_and_replay("deepseek", 3)
        self.assertEqual(out["parsed_count"], 3)
        self.assertTrue(all("synth-" in it["id"] for it in out["items"]))

    def test_replay_qwen_parses_synthetic(self):
        out = self._synth_and_replay("qwen", 4)
        self.assertEqual(out["parsed_count"], 4)
        self.assertEqual(out["items"][0]["folder"], "Home")

    def test_replay_mistral_parses_synthetic(self):
        out = self._synth_and_replay("mistral", 5)
        self.assertEqual(out["parsed_count"], 5)
        # Timestamps should be present and non-empty
        for it in out["items"]:
            self.assertTrue(it["created_at"])
            self.assertTrue(it["updated_at"])


class DiffTests(unittest.TestCase):
    def test_diff_against_matching_snapshot_is_clean(self):
        with tempfile.TemporaryDirectory() as d:
            fx = Path(d) / "fx.json"
            _run(["synthesize", "--provider", "deepseek", "--out", str(fx), "--count", "2"])
            # Build the snapshot from the same replay
            rep = _run(["replay", "--provider", "deepseek", "--list-fixture", str(fx)])
            snap = Path(d) / "snap.json"
            snap.write_text(rep.stdout, encoding="utf-8")
            r = _run(["diff", "--provider", "deepseek", "--list-fixture", str(fx), "--snapshot", str(snap)])
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn("identical", r.stderr)

    def test_diff_against_changed_snapshot_shows_diff(self):
        with tempfile.TemporaryDirectory() as d:
            fx = Path(d) / "fx.json"
            _run(["synthesize", "--provider", "qwen", "--out", str(fx), "--count", "2"])
            # A snapshot with a different (extra) id
            snap = Path(d) / "snap.json"
            data = json.loads(fx.read_text(encoding="utf-8"))
            # Mutate one synthetic id
            data["response"]["data"]["list"][0]["id"] = "different-id"
            fake_out = {
                "fixture": str(fx),
                "parsed_count": 0,
                "items": [],
            }
            snap.write_text(json.dumps(fake_out), encoding="utf-8")
            r = _run(["diff", "--provider", "qwen", "--list-fixture", str(fx), "--snapshot", str(snap)])
            # Returncode 1 = diff found, which is what we want
            self.assertEqual(r.returncode, 1, r.stderr)


class RecordTests(unittest.TestCase):
    """`record` makes a real HTTP call; gate it behind an env flag so CI
    doesn't hammer external services."""

    def test_record_requires_cookie_or_bearer(self):
        r = _run(["record", "--provider", "deepseek", "--url", "https://example.com",
                  "--out", os.path.join(tempfile.gettempdir(), "nope.json")])
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("cookie", r.stderr.lower())


if __name__ == "__main__":
    unittest.main()
