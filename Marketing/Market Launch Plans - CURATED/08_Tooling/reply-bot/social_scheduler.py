"""TotalRecalls Automated Campaign Scheduler & Queue Engine.

Manages the pre-populated 4-week content calendar across X, LinkedIn, and Reddit.
Stores posts in a local SQLite database (schedule_queue.db).
Automates time-delayed execution (e.g. 08:30 AM, 12:00 PM, 17:30 PM).
"""
import json
import sqlite3
import time
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(r"C:\Users\break\Projects\TotalRecalls-Source Code")
TOOLING_DIR = BASE_DIR / "Marketing" / "Market Launch Plans - CURATED" / "08_Tooling" / "reply-bot"
DB_PATH = TOOLING_DIR / "schedule_queue.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS queued_posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        platform TEXT NOT NULL,
        campaign_name TEXT NOT NULL,
        scheduled_for TEXT NOT NULL,
        status TEXT DEFAULT 'pending',
        post_type TEXT DEFAULT 'single',
        content_json TEXT NOT NULL,
        media_path TEXT,
        published_at TEXT
    )
    """)
    conn.commit()
    conn.close()


def add_post(platform: str, campaign: str, scheduled_for_iso: str, content, media_path=None, post_type: str = "single"):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    if isinstance(content, list):
        content_json = json.dumps(content)
        post_type = "thread"
    else:
        content_json = json.dumps([content])
        
    cur.execute("""
    INSERT INTO queued_posts (platform, campaign_name, scheduled_for, status, post_type, content_json, media_path)
    VALUES (?, ?, ?, 'pending', ?, ?, ?)
    """, (platform, campaign, scheduled_for_iso, post_type, content_json, media_path))
    conn.commit()
    post_id = cur.lastrowid
    conn.close()
    print(f"Queued {platform} [{campaign}] for {scheduled_for_iso} (ID: {post_id})")
    return post_id


def list_queued():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, platform, campaign_name, scheduled_for, status, post_type FROM queued_posts ORDER BY scheduled_for ASC")
    rows = cur.fetchall()
    conn.close()
    return rows


def get_due_posts():
    init_db()
    now_iso = datetime.now().isoformat()[:16]  # Match YYYY-MM-DDTHH:MM
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, platform, campaign_name, content_json, media_path FROM queued_posts WHERE status = 'pending' AND scheduled_for <= ? ORDER BY scheduled_for ASC", (now_iso,))
    rows = cur.fetchall()
    conn.close()
    return rows


def mark_completed(post_id: int):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("UPDATE queued_posts SET status = 'completed', published_at = ? WHERE id = ?", (datetime.now().isoformat(), post_id))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    # Check queue
    queue = list_queued()
    print(f"Current Queue holds {len(queue)} items.")
    for q in queue:
        print(f" - [{q[4].upper()}] ID {q[0]} | {q[1]} | {q[2]} | Due: {q[3]}")
