"""Generate uploads_plan.json from Jasper's Description Templates."""
import json, os

BASE = r"C:\Users\break\Projects\TotalRecalls\Marketing\Jasper\YouTube\yt-api"
VIDEO = "TotalRecalls"

ABOUT = (
    "ABOUT TOTALRECALLS\n"
    "TotalRecalls is a Windows app that saves your AI conversations to your PC as Markdown and JSON files. "
    "You sign in to each provider inside the app, on your own computer. Your conversations aren't sent to our "
    "servers, and there's no TotalRecalls account to create.\n\n"
    "The Free Tier covers ChatGPT, Claude, and Perplexity. Pro adds Gemini (through Google Takeout), Grok, "
    "DeepSeek, Mistral, and Qwen, with unlimited downloads.\n"
)
DISC = "Real screen recording. Personal details are blurred. Loading time is trimmed.\n\nWindows 10 and 11.\n"

PRO = {"gemini": True, "grok": True, "deepseek": True, "mistral": True, "qwen": True}
FREE = {"chatgpt": False, "claude": False, "perplexity": False}

PROVIDERS = [
    ("master", "See TotalRecalls in Action — Every AI Chat, Saved Locally",
     "tr_thumb_master.jpg", "TR_yt_master_chatgpt_placeholder.mp4", "proof-master-demo"),
    ("chatgpt", "How to Save Your ChatGPT Chats as Local Files — TotalRecalls (Windows)",
     "tr_thumb_chatgpt.jpg", "TR_yt_provider_chatgpt.mp4", "guide-chatgpt"),
    ("perplexity", "How to Save Your Perplexity Chats Locally — TotalRecalls (Windows)",
     "tr_thumb_perplexity.jpg", "TR_yt_provider_pplx.mp4", "guide-perplexity"),
    ("gemini", "How to Save Your Gemini Conversations Locally — TotalRecalls (Windows)",
     "tr_thumb_gemini.jpg", "TR_yt_provider_gemini.mp4", "guide-gemini"),
    ("grok", "How to Save Your Grok Chats Locally — TotalRecalls (Windows)",
     "tr_thumb_grok.jpg", "TR_yt_provider_grok.mp4", "guide-grok"),
    ("mistral", "How to Save Your Mistral Chats Locally — TotalRecalls (Windows)",
     "tr_thumb_mistral.jpg", "TR_yt_provider_mistral.mp4", "guide-mistral"),
    ("qwen", "How to Save Your Qwen Chats Locally — TotalRecalls (Windows)",
     "tr_thumb_qwen.jpg", "TR_yt_provider_qwen.mp4", "guide-qwen"),
    ("deepseek", "How to Save Your DeepSeek Chats Locally — TotalRecalls (Windows)",
     "tr_thumb_deepseek.jpg", "TR_yt_provider_deepseek.mp4", "guide-deepseek"),
]

NAMES = {"master": "", "chatgpt": "ChatGPT", "claude": "Claude", "perplexity": "Perplexity",
         "gemini": "Gemini", "grok": "Grok", "mistral": "Mistral", "qwen": "Qwen", "deepseek": "DeepSeek"}


def utm(campaign):
    return f"totalrecalls.app/?utm_source=youtube&utm_medium=video&utm_campaign={campaign}"


def provider_desc(key, campaign):
    n = NAMES[key]
    d = (
        f"How to save your {n} conversations to your PC as Markdown and JSON files, step by step, "
        f"using TotalRecalls on Windows. This video shows signing in, choosing what to save, "
        f"downloading, and where your files land.\n\n"
        f"Download TotalRecalls free: {utm(campaign)}\n"
    )
    if PRO.get(key):
        d += (f"This provider is included in Pro. Compare Free and Pro: "
              f"totalrecalls.app/pricing/?utm_source=youtube&utm_medium=video&utm_campaign={campaign}\n")
    if key == "gemini":
        d += ("Gemini conversations come in through a Google Takeout file. This isn't a one-click "
              "download, and this video shows each step.\n")
    d += (
        f"\nCHAPTERS\n"
        f"0:00 What this video covers\n"
        f"0:05 Open TotalRecalls and choose {n}\n"
        f"0:25 Sign in inside the app\n"
        f"0:40 Download your conversations\n"
        f"0:55 Where your files are saved\n"
        f"\n{ABOUT}\n{DISC}"
        f"Recorded with TotalRecalls v1.0 in September 2026.\n"
    )
    return d


def master_desc(campaign):
    return (
        f"Every day, people lose months of AI conversations — and never realize it until it's too late. "
        f"TotalRecalls is a Windows app that downloads your AI conversations from 8 providers — ChatGPT, "
        f"Claude, Perplexity, Gemini, Grok, DeepSeek, Mistral, and Qwen — into a private folder on your own "
        f"computer, as Markdown and JSON files you own forever. No cloud. No account. No subscription.\n\n"
        f"Download TotalRecalls free: {utm(campaign)}\n\n"
        f"CHAPTERS\n"
        f"0:00 The problem: your chats live on their servers\n"
        f"0:20 Connect a provider inside the app\n"
        f"1:00 Download your full history locally\n"
        f"1:40 Browse and export individual conversations\n"
        f"\n{ABOUT}\n{DISC}"
        f"Launch pricing: TotalRecalls Pro is $24 one-time — no subscription, ever.\n"
    )


plan = []
for key, title, thumb, file, campaign in PROVIDERS:
    desc = master_desc(campaign) if key == "master" else provider_desc(key, campaign)
    tags = ["TotalRecalls"] + (
        ["AI chat", "local", "privacy", "backup", "windows", "local-first", "data ownership"]
        if key == "master"
        else [f"{key}", "AI chat", "local", "privacy", "backup", "windows", "local-first", "data ownership"]
    )
    plan.append({"file": file, "title": title, "desc": desc, "tags": tags, "thumb": thumb,
                 "campaign": campaign})

json.dump(plan, open(f"{BASE}/uploads_plan.json", "w"), indent=2)
print(f"{len(plan)} uploads planned")
for p in plan:
    print(f"  - {p['title'][:60]}  [{p['file']}]")
