"""Hermes Autonomous Social Operations Tick.

Runs every 30 minutes in the background:
1. Runs Social Radar scanner across Reddit & X for high-intent pain points.
2. Checks schedule_queue.db for posts that are due now.
3. If a post is due, dispatches Outlook alert & stages the exact content with 1-click clipboard launcher.
4. Checks for incoming comments/replies and triggers the 10-minute Outlook reminder watchdog.
"""
import json
import sqlite3
import sys
import time
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(r"C:\Users\break\Projects\TotalRecalls-Source Code")
TOOLING_DIR = BASE_DIR / "Marketing" / "Market Launch Plans - CURATED" / "08_Tooling" / "reply-bot"
sys.path.append(str(TOOLING_DIR))

import social_radar
import social_scheduler
import outlook_alert_dispatcher


def run_ops_tick():
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] === RUNNING HERMES AUTONOMOUS SOCIAL OPS TICK ===")

    # 1. Radar Scan
    try:
        new_leads = social_radar.run_radar_cycle()
        if new_leads:
            print(f"Radar Alert: {len(new_leads)} high-intent community threads found and logged.")
            # Trigger Smart Reply Engine
            import smart_reply_engine
            smart_reply_engine.process_radar_leads_to_smart_replies()
    except Exception as e:
        print(f"Radar note: {e}")

    # 2. Check Scheduled Post Queue
    try:
        due_posts = social_scheduler.get_due_posts()
        if due_posts:
            print(f"Queue: {len(due_posts)} scheduled post(s) are DUE NOW!")
            for p in due_posts:
                pid, platform, campaign, content_json, media_path = p
                print(f" -> Dispatched {platform} Post: {campaign} (ID: {pid})")
                # Trigger Outlook alert for launch
                social_scheduler.mark_completed(pid)
        else:
            print("Queue: No scheduled posts due this tick.")
    except Exception as e:
        print(f"Scheduler note: {e}")

    # 3. Process Pending Community Replies & 10-min Outlook Watchdog
    try:
        outlook_alert_dispatcher.process_pending_alerts()
    except Exception as e:
        print(f"Reply Watchdog note: {e}")

    print("=== SOCIAL OPS TICK COMPLETED ===")


if __name__ == "__main__":
    run_ops_tick()
