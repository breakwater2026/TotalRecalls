"""TotalRecalls Outlook Alert & Reminder Dispatcher.

Connects to local Outlook Classic via Windows MAPI COM:
1. When a new community message arrives: sends an urgent notification email with
   the drafted response directly to your inbox (rings your PC & iPhone).
2. If the draft remains unapproved: sends reminders every 10 minutes counting down
   the remaining minutes from the 60-minute window (e.g. 50m left, 40m left...).
3. Stops automatically once approved or once the 60-minute window elapses.
"""
import json
import time
from datetime import datetime, timezone
from pathlib import Path
import win32com.client

REPLY_BOT_DIR = Path(r"C:\Users\break\Projects\TotalRecalls-Source Code\Marketing\Market Launch Plans - CURATED\08_Tooling\reply-bot")
PENDING_DRAFTS_FILE = REPLY_BOT_DIR / "pending_drafts.json"

DEFAULT_ALERT_EMAIL = "breakwatercap@outlook.com"
MAX_WINDOW_MINUTES = 60
REMINDER_INTERVAL_MINUTES = 10


def send_outlook_alert(to_email: str, subject: str, html_body: str, high_importance: bool = True):
    """Dispatch an email via local Outlook Classic MAPI."""
    try:
        outlook = win32com.client.Dispatch("Outlook.Application")
        mail = outlook.CreateItem(0)  # 0 = olMailItem
        mail.To = to_email
        mail.Subject = subject
        mail.HTMLBody = html_body
        if high_importance:
            mail.Importance = 2  # 2 = olImportanceHigh
        mail.Send()
        print(f"[Outlook Alert Sent] -> {to_email} | Subject: {subject}")
        return True
    except Exception as e:
        print(f"[Outlook Error] Failed to send email via Outlook: {e}")
        return False


def build_alert_html(draft: dict, minutes_elapsed: int, minutes_remaining: int) -> str:
    platform = draft.get("platform", "Community")
    author = draft.get("author", "User")
    question = draft.get("question", "")
    response = draft.get("draft_response", "").replace("\n", "<br/>")
    draft_id = draft.get("id", "")

    # Timer badge color based on urgency
    timer_color = "#10b981" if minutes_remaining > 30 else ("#f59e0b" if minutes_remaining > 15 else "#ef4444")

    html = f"""
    <html>
    <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f3f4f6; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; border: 1px solid #e5e7eb; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
            <div style="background-color: #0b132b; padding: 18px 24px; color: #ffffff;">
                <h2 style="margin: 0; font-size: 18px; letter-spacing: 0.5px;">TotalRecalls • Action Required</h2>
                <p style="margin: 4px 0 0; font-size: 13px; color: #94a3b8;">Social Media Community Incoming Message</p>
            </div>
            
            <div style="padding: 24px;">
                <!-- Countdown Pill -->
                <div style="background-color: {timer_color}15; border: 1px solid {timer_color}; border-radius: 6px; padding: 10px 16px; margin-bottom: 20px; display: flex; align-items: center;">
                    <span style="font-weight: 700; font-size: 15px; color: {timer_color};">⏱ {minutes_remaining} MINUTES REMAINING</span>
                    <span style="font-size: 12px; color: #4b5563; margin-left: 10px;">(Optimal 60-min algorithm response window)</span>
                </div>

                <div style="margin-bottom: 18px;">
                    <span style="font-size: 12px; font-weight: 600; text-transform: uppercase; color: #6b7280;">Platform & Author:</span>
                    <div style="font-size: 15px; font-weight: 600; color: #111827; margin-top: 2px;">{platform} — {author}</div>
                </div>

                <div style="margin-bottom: 20px; background-color: #f9fafb; border-left: 4px solid #3b82f6; padding: 12px 16px; border-radius: 0 6px 6px 0;">
                    <span style="font-size: 12px; font-weight: 600; text-transform: uppercase; color: #4b5563;">Incoming Question:</span>
                    <p style="margin: 6px 0 0; font-size: 14px; color: #1f2937; line-height: 1.5;">"{question}"</p>
                </div>

                <div style="margin-bottom: 24px; background-color: #f0fdf4; border: 1px solid #bbf7d0; padding: 16px; border-radius: 6px;">
                    <span style="font-size: 12px; font-weight: 700; text-transform: uppercase; color: #166534;">Drafted Response (Verified vs Canonical Docs):</span>
                    <div style="margin-top: 8px; font-size: 13.5px; color: #14532d; line-height: 1.6;">
                        {response}
                    </div>
                </div>

                <div style="border-top: 1px solid #e5e7eb; padding-top: 16px; font-size: 12px; color: #6b7280; line-height: 1.5;">
                    <b>To Approve & Post:</b><br/>
                    • Open Hermes and say: <code>Approve draft {draft_id}</code><br/>
                    • Or copy the text directly on your iPhone and paste it into the {platform} reply field.
                </div>
            </div>
            
            <div style="background-color: #f8fafc; border-top: 1px solid #e2e8f0; padding: 12px 24px; text-align: center; font-size: 11px; color: #94a3b8;">
                TotalRecalls Autonomous Community Copilot • Alert sent via Outlook Classic MAPI
            </div>
        </div>
    </body>
    </html>
    """
    return html


def process_pending_alerts():
    """Scan pending drafts, send initial alerts, and trigger 10-minute reminders."""
    if not PENDING_DRAFTS_FILE.exists():
        return

    try:
        drafts = json.loads(PENDING_DRAFTS_FILE.read_text(encoding="utf-8"))
    except Exception:
        return

    now = time.time()
    modified = False

    for draft in drafts:
        if draft.get("status") != "pending_founder_approval":
            continue

        created_at = draft.get("created_at", now)
        if "created_at" not in draft:
            draft["created_at"] = now
            created_at = now
            modified = True

        elapsed_seconds = now - created_at
        elapsed_minutes = int(elapsed_seconds // 60)
        remaining_minutes = max(0, MAX_WINDOW_MINUTES - elapsed_minutes)

        last_notified = draft.get("last_notified_at", 0)
        time_since_last_alert = (now - last_notified) / 60.0

        # Scenario A: First notification (never notified)
        if last_notified == 0:
            subject = f"🔴 [ACTION REQUIRED] New {draft['platform']} Message — Draft Ready (60m remaining)"
            body = build_alert_html(draft, minutes_elapsed=0, minutes_remaining=60)
            if send_outlook_alert(DEFAULT_ALERT_EMAIL, subject, body, high_importance=True):
                draft["last_notified_at"] = now
                draft["notification_count"] = 1
                modified = True

        # Scenario B: 10-minute recurring reminder within the 60-minute window
        elif time_since_last_alert >= REMINDER_INTERVAL_MINUTES and remaining_minutes > 0:
            count = draft.get("notification_count", 1) + 1
            subject = f"⏳ [REMINDER #{count}] {draft['platform']} Reply Pending — {remaining_minutes}m Remaining"
            body = build_alert_html(draft, minutes_elapsed=elapsed_minutes, minutes_remaining=remaining_minutes)
            if send_outlook_alert(DEFAULT_ALERT_EMAIL, subject, body, high_importance=True):
                draft["last_notified_at"] = now
                draft["notification_count"] = count
                modified = True

        # Scenario C: Window expired
        elif remaining_minutes <= 0 and not draft.get("expired_notified", False):
            subject = f"⚠️ [WINDOW ELAPSED] 60-Minute Response Window Elapsed for {draft['platform']} Message"
            body = f"<p>The optimal 60-minute response window for message from <b>{draft['author']}</b> has ended. The draft is still retained in Hermes.</p>"
            send_outlook_alert(DEFAULT_ALERT_EMAIL, subject, body, high_importance=False)
            draft["expired_notified"] = True
            modified = True

    if modified:
        PENDING_DRAFTS_FILE.write_text(json.dumps(drafts, indent=2), encoding="utf-8")


if __name__ == "__main__":
    process_pending_alerts()
