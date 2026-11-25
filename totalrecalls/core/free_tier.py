"""Cumulative Free Tier accounting.

The public promise (website is canonical) is **3 providers, 5 conversations per
provider** — not 5 per export run. This ledger records every conversation a
Free user has extracted, whether through a bulk export or a per-message
selection export, so the cap is cumulative across runs and across both paths.

Stored next to the Library as ``free_tier_usage.json``::

    {"chatgpt": ["conv-id-1", "..."], "claude": [...]}

Pro users never touch it. Deleting the file resets the count; this is an
honesty mechanism, not DRM.
"""
from __future__ import annotations

import json
import os
import threading
from typing import Iterable

LEDGER_FILENAME = "free_tier_usage.json"


def _norm(value: str | None) -> str:
    return str(value or "").strip().lower()


class FreeTierUsage:
    """Per-provider set of conversation ids that have been exported."""

    def __init__(self, outdir: str):
        self.path = os.path.join(outdir, LEDGER_FILENAME)
        self._lock = threading.Lock()
        self._data: dict[str, list[str]] = {}
        self._load()

    def _load(self) -> None:
        try:
            with open(self.path, encoding="utf-8") as f:
                raw = json.load(f)
        except (OSError, ValueError, TypeError):
            return
        if not isinstance(raw, dict):
            return
        for provider, ids in raw.items():
            if isinstance(ids, list):
                self._data[_norm(provider)] = sorted({str(i) for i in ids if i})

    def _save(self) -> None:
        folder = os.path.dirname(self.path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        tmp = self.path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2, sort_keys=True)
        os.replace(tmp, self.path)

    def used(self, provider: str) -> set[str]:
        return set(self._data.get(_norm(provider), []))

    def count(self, provider: str) -> int:
        return len(self._data.get(_norm(provider), []))

    def is_used(self, provider: str, conversation_id: str) -> bool:
        cid = str(conversation_id or "")
        return bool(cid) and cid in self.used(provider)

    def remaining(self, provider: str, limit: int) -> int:
        return max(0, int(limit) - self.count(provider))

    def record(self, provider: str, conversation_ids: Iterable[str]) -> None:
        ids = [str(i) for i in conversation_ids if i]
        if not ids:
            return
        with self._lock:
            key = _norm(provider)
            current = set(self._data.get(key, []))
            current.update(ids)
            self._data[key] = sorted(current)
            self._save()

    def consume(self, provider: str, conversation_id: str, limit: int) -> tuple[bool, str]:
        """Allow one conversation against the cumulative allowance.

        Returns ``(allowed, reason)``. Records the id only when allowed. A
        conversation already counted is always allowed (re-exporting something
        you already have does not consume another slot).
        """
        cid = str(conversation_id or "")
        if not cid:
            return False, "This conversation has no id, so it cannot be counted."
        if self.is_used(provider, cid):
            return True, ""
        if self.remaining(provider, limit) <= 0:
            return False, (
                f"Free Tier is limited to {int(limit)} conversations per provider. "
                "Upgrade to Pro for unlimited downloads."
            )
        self.record(provider, [cid])
        return True, ""
