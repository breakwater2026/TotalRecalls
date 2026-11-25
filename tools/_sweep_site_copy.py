"""Claim-drift gate: fail when product copy contradicts the canonical website.

The website is the canonical artifact. This gate covers the claim classes that
have actually drifted — refund promises, engine/model claims, the canonical
Library path, stale versions and dates — across every artifact that makes a
claim: site source, built HTML, product manuals, shipped READMEs, the SSE
README and the fulfillment email template.

Deliberately narrow: each check must be actionable and low-false-positive, so
the gate can run in CI instead of being a report nobody reads.

Policy reference:
  - no refund on Downloader Pro; 7 days on SSE          (/legals/)
  - Free Tier: 3 providers, 5 conversations per provider (/faq/)
  - Library: C:\\TotalRecalls\\Library                      (/library/)
  - no model download; hash embeddings in-page          (/privacy/)
"""
from __future__ import annotations

import glob
import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SRC = str(REPO / "site" / "src")
DIST = str(REPO / "site" / "dist")
DOC_FILES = [
    str(REPO / "docs" / "TOTALRECALLS_POWER_USER_MANUAL.md"),
    str(REPO / "docs" / "TOTALRECALLS_SSE_QUICK_START_GUIDE.md"),
]
PUBLIC_DOWNLOADS = str(REPO / "site" / "public" / "downloads")
WORKER = str(REPO / "paddle-fulfillment-worker" / "src" / "worker.js")
SSE_README = str(REPO / "Modules" / "smart-search-engine" / "README-SSE.md")

CHECKS = [
    ("old product name", re.compile(r"Perplexity Exporter", re.I)),
    # A bare "refund" is legitimate (the policy says there is no refund).
    ("refund promise", re.compile(r"30[- ]day (?:money|refund|guarantee|no-questions)|money[- ]back|money back|refund guarantee", re.I)),
    ("14-day refund", re.compile(r"14[- ]day", re.I)),
    ("version drift 1.3/1.2", re.compile(r"1\.[23]\.\d")),
    ("stale engine claim", re.compile(r"HNSW indexed|bge-small", re.I)),
    ("stale model-download claim", re.compile(r"one-time (?:search-)?model download|search-model download", re.I)),
    # Matches the full legacy path, not the migration note that names the folder.
    ("legacy library path", re.compile(r"TotalRecalls-download[\\/]Library")),
    ("stale year 2025", re.compile(r"\b2025\b")),
]

SKIP_DIRS = ("node_modules", "_astro", ".git", "__pycache__")


def scan(base: str, exts: tuple[str, ...]) -> list[tuple[str, str, int, str]]:
    hits: list[tuple[str, str, int, str]] = []
    if not os.path.exists(base):
        return hits
    for root, _dirs, files in os.walk(base):
        if any(part in root for part in SKIP_DIRS):
            continue
        for name in files:
            if not any(name.endswith(e) for e in exts):
                continue
            path = os.path.join(root, name)
            try:
                text = open(path, encoding="utf-8", errors="replace").read()
            except Exception:
                continue
            for i, line in enumerate(text.splitlines(), 1):
                for label, pattern in CHECKS:
                    if pattern.search(line):
                        hits.append((label, os.path.relpath(path, REPO), i, line.strip()[:120]))
    return hits


def scan_file(path: str, exts: tuple[str, ...]) -> list[tuple[str, str, int, str]]:
    if not os.path.isfile(path) or not any(path.endswith(e) for e in exts):
        return []
    hits: list[tuple[str, str, int, str]] = []
    for i, line in enumerate(open(path, encoding="utf-8", errors="replace").read().splitlines(), 1):
        for label, pattern in CHECKS:
            if pattern.search(line):
                hits.append((label, os.path.relpath(path, REPO), i, line.strip()[:120]))
    return hits


def main() -> int:
    sections = [
        ("site/src", scan(SRC, (".astro", ".jsx", ".js", ".json"))),
        ("site/dist", scan(DIST, (".html",))),
        ("product manuals", sum((scan_file(f, (".md",)) for f in DOC_FILES), [])),
        ("shipped READMEs", scan(PUBLIC_DOWNLOADS, (".txt",))),
        ("SSE README", scan_file(SSE_README, (".md",))),
        ("fulfillment worker", scan_file(WORKER, (".js",))),
    ]

    total = 0
    for title, hits in sections:
        print(f"=== {title} ===")
        for label, path, line_no, line in hits:
            print(f"  [{label}] {path}:{line_no}: {line}")
        print(f"  total: {len(hits)}")
        total += len(hits)

    sitemap = os.path.join(DIST, "sitemap.xml")
    if os.path.isfile(sitemap):
        urls = re.findall(r"<loc>([^<]+)</loc>", open(sitemap, encoding="utf-8").read())
        pages = {
            os.path.relpath(p, DIST).replace("\\", "/").rsplit(".html", 1)[0]
            for p in glob.glob(os.path.join(DIST, "**", "*.html"), recursive=True)
            if "_astro" not in p.replace("\\", "/")
        }
        print(f"\n=== sitemap === urls: {len(urls)} pages: {len(pages)}")

    print(f"\nTOTAL HITS: {total}")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
