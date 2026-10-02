"""Upload a video to the TotalRecalls channel (first upload test).
Usage: python upload_video.py <video.mp4> <title> [--playlist-id ID] [--privacy private|unlisted|public]
Writes upload_result.json with the videoId + web page URL.
"""
import json, os, sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

BASE = r"C:\Users\break\Projects\TotalRecalls\Marketing\Jasper\YouTube\yt-api"
SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"

args = [a for a in sys.argv[1:]]
video = args[0]
title = args[1]
playlist_id = None
privacy = "private"
i = 2
while i < len(args):
    if args[i] == "--playlist-id":
        playlist_id = args[i + 1]; i += 2
    elif args[i] == "--privacy":
        privacy = args[i + 1]; i += 2
    else:
        i += 1

desc = (
    "Eight AI providers. One folder on your own computer.\n"
    "TotalRecalls pulls your conversations from ChatGPT, Claude, Perplexity, Gemini, "
    "Grok, DeepSeek, Mistral, and Qwen into a private local library — Markdown and JSON "
    "files you own forever. No cloud. No account. No subscription.\n"
    "This is the convergence: 8 sources flowing into one local folder.\n\n"
    "Try the Free Tier today: https://totalrecalls.app\n"
    "Windows app — visit from desktop to download.\n"
    "Launch pricing: TotalRecalls Pro is $24 one-time — no subscription, ever.\n\n"
    "#AITools #DataPrivacy #LocalFirst #ChatGPT #Claude"
)
tags = ["TotalRecalls", "AI chat", "local", "privacy", "backup", "convergence", "8 providers"]
# Custom thumbnail: set post-upload via thumbnails().set (needs the videoId).
# (thumbnails[] at insert-time wants an image URL, not the video itself.)
thumbnails = None

creds = Credentials.from_authorized_user_info(json.load(open(f"{BASE}/token.json")), [SCOPE])
yt = build("youtube", "v3", credentials=creds)

media = MediaFileUpload(video, chunksize=-1, resumable=True)
body = {
    "snippet": {
        "title": title,
        "description": desc,
        "tags": tags,
        "categoryId": "28",
        "defaultLanguage": "en",
        "defaultAudioLanguage": "en",
    },
    "status": {"privacyStatus": privacy, "embeddable": True, "license": "youtube"},
}
request = yt.videos().insert(part="snippet,status,contentDetails,player", body=body, media_body=media)
resp = request.execute()
# NOTE: top-level playlistId in videos.insert proved unreliable — add via playlistItems.insert.
if playlist_id:
    yt.playlistItems().insert(
        part="snippet",
        body={"snippet": {
            "resourceId": {"kind": "youtube#video", "videoId": resp["id"]},
            "playlistId": playlist_id,
            "title": title,
        }},
    ).execute()
out = {"videoId": resp["id"], "title": title, "url": resp.get("contentDetails", {}).get("uploadStatus", ""),
       "page": f"https://www.youtube.com/watch?v={resp['id']}", "privacy": privacy,
       "playlistId": playlist_id}
with open(f"{BASE}/upload_result.json", "w") as f:
    json.dump(out, f, indent=2)
print(json.dumps(out, indent=2))
