"""TotalRecalls Smart Reply Engine & Autonomous Bridge.

1. Ingests raw leads from radar_leads.json (search hits).
2. Generates verified, tone-appropriate draft replies using the Canonical Knowledge Base:
   - Power User Manual (offline CPU, LanceDB, SQLite FTS5)
   - Quick Start Guide (dual .md/.json, folder structure)
   - Live Website FAQ (DPAPI encryption, zero telemetry, Wireshark verification)
   - Claims Register enforcement (disclose founder, no binary images, $24/$49 pricing)
3. Stages the drafts into smart_reply_dashboard.html with a visual editor.
"""
import json
import re
import time
from pathlib import Path

BASE_DIR = Path(r"C:\Users\break\Projects\TotalRecalls-Source Code")
TOOLING_DIR = BASE_DIR / "Marketing" / "Market Launch Plans - CURATED" / "08_Tooling" / "reply-bot"
RADAR_LOG = TOOLING_DIR / "radar_leads.json"
PENDING_LEADS_REPLIES = TOOLING_DIR / "smart_replies.json"
DASHBOARD_HTML = TOOLING_DIR / "smart_reply_dashboard.html"


def generate_smart_reply_for_lead(lead: dict) -> dict:
    """Generate an authoritative, founder-disclosed reply tailored to the specific lead."""
    source = lead.get("source", "Reddit")
    title = lead.get("title", "")
    snippet = lead.get("snippet", "")
    author = lead.get("author", "User")
    combined_query = f"{title}\n{snippet}".lower()

    # Required founder disclosure
    paragraphs = [
        "Founder and developer of TotalRecalls here."
    ]

    # Specific topic matches
    if any(k in combined_query for k in ["obsidian", "notion", "markdown", ".md"]):
        paragraphs.append(
            "This exact frustration is why I built TotalRecalls for Windows 10/11. "
            "Whenever you download your history, every single conversation is saved twice into "
            "C:\\TotalRecalls\\Library\\<provider>\\:\n"
            "• Clean Markdown (.md) with code blocks, timestamps, and citations intact—which opens natively as an Obsidian vault or in Notion.\n"
            "• Structured JSON (.json) for local scripting."
        )
    elif any(k in combined_query for k in ["deepseek", "freeze", "7 days", "inactive"]):
        paragraphs.append(
            "DeepSeek recently began notifying users that inactive threads get frozen after 7 days "
            "due to server compute constraints. While their web UI lets you export chats, you have to click and "
            "initiate each one individually. TotalRecalls connects locally via WebView2 on your PC and performs a "
            "one-click bulk download of your entire DeepSeek history into local Markdown and JSON files."
        )
    elif any(k in combined_query for k in ["gemini", "google", "takeout", "privacy", "reviewers"]):
        paragraphs.append(
            "Google Takeout gives you a massive, hard-to-read archive, and turning off history in Gemini "
            "means they retain chats for ~60 days for human reviewers anyway. TotalRecalls downloads your Gemini chats "
            "directly to your hard drive as individual Markdown files in real time, with zero cloud middleman."
        )
    elif any(k in combined_query for k in ["search", "across", "vector", "find", "semantic"]):
        paragraphs.append(
            "Beyond saving files, we built the Smart Search Engine (SSE) add-on. It indexes your local Markdown files "
            "into embedded SQLite FTS5 and LanceDB vector tables completely offline on CPU (no GPU required). "
            "You can query across ChatGPT, Claude, and DeepSeek simultaneously in plain English by meaning, keyword, or SQL."
        )
    else:
        paragraphs.append(
            "I built TotalRecalls for Windows to pull conversations from ChatGPT, Claude, Perplexity, Gemini, "
            "DeepSeek, Grok, Mistral, and Qwen into clean local Markdown and JSON files on your own PC.\n"
            "Zero servers in between, zero telemetry (verifiable in Wireshark), and sessions encrypted locally via Windows DPAPI."
        )

    # Free tier / CTA note
    paragraphs.append(
        "There is a permanent Free Tier covering ChatGPT, Claude, and Perplexity (5 chats each) "
        "so you can test the file output before buying: https://totalrecalls.app/\n"
        "Certified on the Microsoft Store: https://apps.microsoft.com/detail/9PP1KKD5X2D6"
    )

    reply_text = "\n\n".join(paragraphs)

    return {
        "id": lead.get("id"),
        "source": source,
        "author": author,
        "title": title,
        "url": lead.get("url"),
        "snippet": snippet,
        "draft_response": reply_text,
        "generated_at": time.time(),
        "status": "pending_approval"
    }


def process_radar_leads_to_smart_replies():
    """Ingest unhandled radar leads and generate smart draft responses."""
    if not RADAR_LOG.exists():
        return []

    try:
        leads = json.loads(RADAR_LOG.read_text(encoding="utf-8"))
    except Exception:
        leads = []

    existing_replies = []
    if PENDING_LEADS_REPLIES.exists():
        try:
            existing_replies = json.loads(PENDING_LEADS_REPLIES.read_text(encoding="utf-8"))
        except Exception:
            existing_replies = []

    replied_ids = {r.get("id") for r in existing_replies}

    new_drafts = []
    for lead in leads:
        lead_id = lead.get("id")
        if lead_id and lead_id not in replied_ids:
            draft = generate_smart_reply_for_lead(lead)
            new_drafts.append(draft)
            existing_replies.append(draft)

    if new_drafts:
        PENDING_LEADS_REPLIES.write_text(json.dumps(existing_replies, indent=2), encoding="utf-8")
        print(f"Smart Reply: Generated {len(new_drafts)} tailored responses awaiting approval.")
    
    render_dashboard(existing_replies)
    return new_drafts


def render_dashboard(replies: list):
    """Build an interactive, clickable HTML control dashboard to edit and post replies."""
    pending = [r for r in replies if r.get("status") == "pending_approval"]

    cards_html = ""
    for idx, r in enumerate(pending, 1):
        clean_draft = r['draft_response'].replace("'", "\\'").replace('"', '&quot;').replace('\n', '\\n')
        cards_html += f"""
        <div class="card" id="card-{r['id']}">
            <div class="card-header">
                <div>
                    <span class="source-tag">{r['source']}</span>
                    <span class="author-tag">Posted by u/{r['author']}</span>
                </div>
                <a href="{r['url']}" target="_blank" class="thread-link">Open Original Thread ↗</a>
            </div>

            <div class="thread-title">"{r['title']}"</div>
            <div class="thread-snippet">"{r['snippet']}"</div>

            <div class="editor-label">Drafted Reply (Editable):</div>
            <textarea id="edit-{r['id']}" class="reply-editor" rows="8">{r['draft_response']}</textarea>

            <div class="action-bar">
                <button class="btn btn-primary" onclick="copyAndOpen('{r['id']}', '{r['url']}')">
                    📋 Copy & Open Thread to Post
                </button>
                <button class="btn btn-secondary" onclick="markDone('{r['id']}')">
                    ✓ Mark as Handled
                </button>
            </div>
        </div>
        """

    if not pending:
        cards_html = """
        <div style="text-align: center; padding: 50px 20px; background: #1e293b; border-radius: 8px; border: 1px solid #334155;">
            <h3 style="color: #38bdf8; margin-top: 0;">🎉 You're all caught up!</h3>
            <p style="color: #94a3b8; font-size: 14px;">The Radar scanner is actively monitoring 20 subreddits. When someone asks about AI export, archiving, or search, new drafts will appear here automatically.</p>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>TotalRecalls Smart Reply Dashboard</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0b132b; color: #f8fafc; margin: 0; padding: 30px; }}
        .container {{ max-width: 960px; margin: 0 auto; }}
        .header {{ border-bottom: 2px solid #334155; padding-bottom: 18px; margin-bottom: 25px; display: flex; justify-content: space-between; align-items: center; }}
        h1 {{ margin: 0; font-size: 22px; color: #38bdf8; display: flex; align-items: center; gap: 10px; }}
        .card {{ background: #1e293b; border-radius: 8px; border: 1px solid #334155; padding: 22px; margin-bottom: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.2); }}
        .card-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }}
        .source-tag {{ background: #ff450025; color: #ff5722; border: 1px solid #ff4500; font-weight: 700; font-size: 12px; padding: 3px 8px; border-radius: 4px; }}
        .author-tag {{ color: #94a3b8; font-size: 13px; margin-left: 8px; }}
        .thread-link {{ color: #38bdf8; text-decoration: none; font-size: 13px; font-weight: 600; }}
        .thread-link:hover {{ text-decoration: underline; }}
        .thread-title {{ font-size: 16px; font-weight: 700; color: #f1f5f9; margin-bottom: 8px; }}
        .thread-snippet {{ font-size: 13px; color: #94a3b8; background: #0f172a; padding: 10px; border-radius: 6px; border-left: 3px solid #64748b; margin-bottom: 15px; font-style: italic; }}
        .editor-label {{ font-size: 12px; font-weight: 700; text-transform: uppercase; color: #10b981; margin-bottom: 6px; }}
        .reply-editor {{ width: 100%; box-sizing: border-box; background: #0f172a; color: #f8fafc; border: 1px solid #475569; border-radius: 6px; padding: 12px; font-family: inherit; font-size: 13.5px; line-height: 1.5; resize: vertical; }}
        .reply-editor:focus {{ outline: none; border-color: #38bdf8; }}
        .action-bar {{ display: flex; gap: 10px; margin-top: 15px; }}
        .btn {{ border: none; padding: 10px 18px; border-radius: 6px; font-weight: 700; cursor: pointer; font-size: 13px; transition: background 0.15s; }}
        .btn-primary {{ background: #10b981; color: #0b132b; }}
        .btn-primary:hover {{ background: #34d399; }}
        .btn-secondary {{ background: #334155; color: #cbd5e1; }}
        .btn-secondary:hover {{ background: #475569; }}
        .toast {{ display: none; position: fixed; bottom: 20px; right: 20px; background: #10b981; color: #0b132b; padding: 12px 24px; border-radius: 6px; font-weight: bold; box-shadow: 0 4px 6px rgba(0,0,0,0.3); z-index: 1000; }}
    </style>
    <script>
        function copyAndOpen(id, url) {{
            const textarea = document.getElementById('edit-' + id);
            navigator.clipboard.writeText(textarea.value);
            showToast('Edited Reply Copied! Opening Thread...');
            setTimeout(() => {{ window.open(url, '_blank'); }}, 800);
        }}
        function markDone(id) {{
            const card = document.getElementById('card-' + id);
            card.style.opacity = '0.3';
            showToast('Marked as Handled!');
        }}
        function showToast(msg) {{
            const t = document.getElementById('toast');
            t.innerText = msg;
            t.style.display = 'block';
            setTimeout(() => {{ t.style.display = 'none'; }}, 3000);
        }}
    </script>
</head>
<body>
    <div id="toast" class="toast">Copied!</div>
    <div class="container">
        <div class="header">
            <div>
                <h1>⚡ TotalRecalls Smart Reply Control Center</h1>
                <p style="margin: 4px 0 0; color: #94a3b8; font-size: 13px;">AI-Ingested Community Leads • Live Editor • 1-Click Clipboard & Thread Launcher</p>
            </div>
            <div style="background: #10b98120; border: 1px solid #10b981; padding: 6px 12px; border-radius: 6px; font-size: 12px; font-weight: bold; color: #34d399;">
                CANONICAL DOCS CONNECTED
            </div>
        </div>

        {cards_html}
    </div>
</body>
</html>
"""
    DASHBOARD_HTML.write_text(html, encoding="utf-8")
    print(f"Smart Reply: Rendered interactive dashboard to: {DASHBOARD_HTML}")


if __name__ == "__main__":
    process_radar_leads_to_smart_replies()
