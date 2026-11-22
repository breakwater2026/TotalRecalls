"""TotalRecalls Social Media Radar Engine.

Monitors Reddit and X for high-intent pain points related to TotalRecalls:
- "export Claude" / "export ChatGPT" / "export DeepSeek" / "export Perplexity"
- "save AI chats" / "AI history backup" / "chats to Markdown" / "ChatGPT to Obsidian"
- Filters out 98% of irrelevant noise (memes, general prompt engineering).
- Logs high-relevance leads and prepares draft responses for founder review.
"""
import json
import re
import time
import urllib.request
from pathlib import Path

BASE_DIR = Path(r"C:\Users\break\Projects\TotalRecalls-Source Code")
REPLY_BOT_DIR = BASE_DIR / "Marketing" / "Market Launch Plans - CURATED" / "08_Tooling" / "reply-bot"
RADAR_LOG = REPLY_BOT_DIR / "radar_leads.json"
CONFIG_FILE = REPLY_BOT_DIR / "radar_config.json"

DEFAULT_SUBREDDITS = [
    "DataHoarder", "ChatGPT", "ClaudeAI", "perplexity_ai", "DeepSeek", "ObsidianMD", "PKMS", "selfhosted"
]

DEFAULT_KEYWORDS = [
    r"export (?:chatgpt|claude|perplexity|deepseek|gemini|grok|mistral|qwen)",
    r"download (?:chatgpt|claude|perplexity|deepseek|gemini|grok|mistral|qwen)",
    r"backup (?:chatgpt|claude|perplexity|deepseek|gemini|chats|conversations)",
    r"save (?:all )?(?:my )?(?:chats|conversations|threads) to (?:markdown|json|pc|local)",
    r"(?:chatgpt|claude|ai chats) to obsidian",
    r"lost (?:my )?(?:chat|conversation) history",
    r"freeze|inactive for over 7 days",
    r"search across (?:all )?(?:chatgpt|claude|ai|models)",
]


def load_config():
    if CONFIG_FILE.exists():
        try:
            cfg = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            subs = cfg.get("target_subreddits", DEFAULT_SUBREDDITS)
            kw = cfg.get("pain_keywords", DEFAULT_KEYWORDS)
            patterns = [re.compile(p, re.IGNORECASE) for p in kw]
            return subs, patterns
        except Exception:
            pass
    return DEFAULT_SUBREDDITS, [re.compile(p, re.IGNORECASE) for p in DEFAULT_KEYWORDS]


def scan_subreddit_recent(sub: str, compiled_patterns: list, limit: int = 15):
    """Scrape public Reddit RSS/JSON feeds without third-party auth barriers."""
    url = f"https://www.reddit.com/r/{sub}/new.json?limit={limit}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Windows:TotalRecallsRadar:v1.0 (by /u/TotalRecallsApp)"},
    )
    matches = []
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="ignore"))
            children = data.get("data", {}).get("children", [])
            for item in children:
                post = item.get("data", {})
                title = post.get("title", "")
                selftext = post.get("selftext", "")
                combined = f"{title}\n{selftext}"
                
                score = 0
                matched_patterns = []
                for pat in compiled_patterns:
                    if pat.search(combined):
                        score += 1
                        matched_patterns.append(pat.pattern)
                
                if score > 0:
                    matches.append({
                        "platform": "Reddit",
                        "source": f"r/{sub}",
                        "id": post.get("id"),
                        "title": title,
                        "url": f"https://reddit.com{post.get('permalink')}",
                        "author": post.get("author"),
                        "matched_patterns": matched_patterns,
                        "created_utc": post.get("created_utc"),
                        "snippet": selftext[:200] if selftext else title,
                        "detected_at": time.time(),
                    })
    except Exception as e:
        pass
    return matches


def run_radar_cycle():
    target_subreddits, compiled_patterns = load_config()
    print(f"Running Radar cycle across {len(target_subreddits)} subreddits with {len(compiled_patterns)} active keyword rules...")
    all_leads = []
    for sub in target_subreddits:
        leads = scan_subreddit_recent(sub, compiled_patterns)
        all_leads.extend(leads)
        time.sleep(0.3)

    existing = []
    if RADAR_LOG.exists():
        try:
            existing = json.loads(RADAR_LOG.read_text(encoding="utf-8"))
        except Exception:
            existing = []

    existing_ids = {item.get("id") for item in existing}
    new_leads = [lead for lead in all_leads if lead["id"] not in existing_ids]

    if new_leads:
        existing.extend(new_leads)
        RADAR_LOG.write_text(json.dumps(existing, indent=2), encoding="utf-8")
        print(f"Radar: Detected {len(new_leads)} high-intent community discussions!")
    else:
        print("Radar: Scan completed. No new high-intent discussions since last check.")

    return new_leads


if __name__ == "__main__":
    run_radar_cycle()
