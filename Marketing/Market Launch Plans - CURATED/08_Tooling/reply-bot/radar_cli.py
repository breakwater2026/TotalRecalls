"""CLI utility to view, review, and clear high-intent Radar leads.

Usage:
    python radar_cli.py
    python radar_cli.py --clear
"""
import argparse
import json
import time
from pathlib import Path

RADAR_LOG = Path(r"C:\Users\break\Projects\TotalRecalls-Source Code\Marketing\Market Launch Plans - CURATED\08_Tooling\reply-bot\radar_leads.json")


def view_leads():
    if not RADAR_LOG.exists():
        print("No radar leads recorded yet. (The scanner is active and checking every 30 minutes).")
        return

    try:
        leads = json.loads(RADAR_LOG.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"Error reading radar log: {e}")
        return

    if not leads:
        print("Radar log is currently empty.")
        return

    print(f"\n=======================================================")
    print(f"📡 TOTALRECALLS RADAR: {len(leads)} HIGH-INTENT LEADS DETECTED")
    print(f"=======================================================\n")

    for idx, item in enumerate(reversed(leads), 1):
        detected_str = time.strftime("%Y-%m-%d %H:%M", time.localtime(item.get("detected_at", time.time())))
        print(f"[{idx}] {item.get('source')} | Author: u/{item.get('author')} | Detected: {detected_str}")
        print(f"    TITLE: {item.get('title')}")
        print(f"    URL:   {item.get('url')}")
        print(f"    RULES TRIGGERED: {', '.join(item.get('matched_patterns', []))}")
        snippet = item.get('snippet', '').replace('\n', ' ')
        if len(snippet) > 140:
            snippet = snippet[:140] + "..."
        print(f"    SNIPPET: \"{snippet}\"")
        print("-" * 55)


def clear_leads():
    if RADAR_LOG.exists():
        RADAR_LOG.write_text("[]", encoding="utf-8")
        print("Cleared radar leads log.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="View TotalRecalls Community Radar Leads")
    parser.add_argument("--clear", action="store_true", help="Clear the radar log")
    args = parser.parse_args()

    if args.clear:
        clear_leads()
    else:
        view_leads()
