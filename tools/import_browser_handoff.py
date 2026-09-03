"""Import a browser companion JSON handoff into a TotalRecalls library.

Usage:
    python tools/import_browser_handoff.py handoff.json --output C:\TotalRecalls
"""

from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from totalrecalls.browser_handoff import HandoffError, import_handoff


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Import one browser conversation handoff.")
    parser.add_argument("handoff", help="path to the downloaded handoff JSON file")
    parser.add_argument("--output", required=True, help="TotalRecalls library directory")
    args = parser.parse_args(argv)

    try:
        record = import_handoff(args.handoff, args.output)
    except HandoffError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(json.dumps({
        "imported": True,
        "provider": record["provider"],
        "title": record["title"],
        "folder": record["rel_path"],
        "messages": record["stats"]["messages"],
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
