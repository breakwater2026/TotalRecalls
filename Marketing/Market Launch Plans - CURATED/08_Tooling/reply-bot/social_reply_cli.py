import argparse
import json
import sys
import time
from pathlib import Path

REPLY_BOT_DIR = Path(r"C:\Users\break\Projects\TotalRecalls-Source Code\Marketing\Market Launch Plans - CURATED\08_Tooling\reply-bot")
PENDING_DRAFTS_FILE = REPLY_BOT_DIR / "pending_drafts.json"
HISTORY_FILE = REPLY_BOT_DIR / "approved_history.json"


def list_pending():
    if not PENDING_DRAFTS_FILE.exists():
        print("No pending drafts.")
        return
    drafts = json.loads(PENDING_DRAFTS_FILE.read_text(encoding="utf-8"))
    pending = [d for d in drafts if d.get("status") == "pending_founder_approval"]
    if not pending:
        print("No pending drafts awaiting review.")
        return
    print(f"\n=== {len(pending)} PENDING SOCIAL REPLIES AWAITING APPROVAL ===")
    for idx, d in enumerate(pending, 1):
        print(f"\n[{idx}] ID: {d['id']} | Platform: {d['platform']} | Author: {d['author']}")
        print(f"Question: {d['question']}")
        print("-" * 50)
        print("DRAFT RESPONSE:")
        print(d["draft_response"])
        print("-" * 50)


def approve(draft_id: str):
    if not PENDING_DRAFTS_FILE.exists():
        print("No drafts found.")
        return
    drafts = json.loads(PENDING_DRAFTS_FILE.read_text(encoding="utf-8"))
    found = False
    for d in drafts:
        if d["id"] == draft_id:
            d["status"] = "approved"
            found = True
            print(f"Draft {draft_id} marked as APPROVED.")
            # Record in history
            history = []
            if HISTORY_FILE.exists():
                try:
                    history = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
                except Exception:
                    history = []
            history.append(d)
            HISTORY_FILE.write_text(json.dumps(history, indent=2), encoding="utf-8")

            # Format for YouTube Community Post
            yt_post_file = REPLY_BOT_DIR / "youtube_community_posts.md"
            timestamp = time.strftime("%Y-%m-%d %H:%M")
            yt_block = (
                f"\n\n---\n"
                f"### Community Q&A from {d.get('platform', 'Social Media')} ({timestamp})\n\n"
                f"**Question from {d.get('author', 'User')}:**\n"
                f"> \"{d.get('question', '').strip()}\"\n\n"
                f"**Founder Answer:**\n"
                f"{d.get('draft_response', '').strip()}\n\n"
                f"---\n"
            )
            with open(yt_post_file, "a", encoding="utf-8") as f:
                f.write(yt_block)
            print(f"Appended Q&A to YouTube Posts log: {yt_post_file}")
            break
    if found:
        remaining = [d for d in drafts if d["id"] != draft_id]
        PENDING_DRAFTS_FILE.write_text(json.dumps(remaining, indent=2), encoding="utf-8")
    else:
        print(f"Draft ID {draft_id} not found.")


def main():
    parser = argparse.ArgumentParser(description="TotalRecalls Social Reply Manager")
    parser.add_argument("--list", action="store_true", help="List all pending drafts")
    parser.add_argument("--approve", type=str, help="Approve draft by ID")
    args = parser.parse_args()

    if args.list:
        list_pending()
    elif args.approve:
        approve(args.approve)
    else:
        list_pending()


if __name__ == "__main__":
    main()
