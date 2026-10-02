"""Batch upload: master + 7 provider videos, private, into "Start Here".

Usage: python upload_batch.py
Reads uploads_plan.json (list of {file, title, desc, tags, thumb, order}).
Writes upload_batch_result.json.
"""
import json, time
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

BASE = r"C:\Users\break\Projects\TotalRecalls\Marketing\Jasper\YouTube\yt-api"
VID = r"C:\Users\break\Projects\TotalRecalls\Marketing\Jasper\YouTube\videos"
THUMB = r"C:\Users\break\Projects\TotalRecalls\Marketing\Jasper\YouTube\thumbnails"
SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
PLAYLIST = "PLHGgAPo4_vi8"

ABOUT = (
    "ABOUT TOTALRECALLS\n"
    "TotalRecalls is a Windows app that saves your AI conversations to your PC as Markdown and JSON files. "
    "You sign in to each provider inside the app, on your own computer. Your conversations aren't sent to our "
    "servers, and there's no TotalRecalls account to create.\n\n"
    "The Free Tier covers ChatGPT, Claude, and Perplexity. Pro adds Gemini (through Google Takeout), Grok, "
    "DeepSeek, Mistral, and Qwen, with unlimited downloads.\n"
)
DISCLAIMER = "Real screen recording. Personal details are blurred. Loading time is trimmed.\n\nWindows 10 and 11.\n"

creds = Credentials.from_authorized_user_info(json.load(open(f"{BASE}/token.json")), [SCOPE])
yt = build("youtube", "v3", credentials=creds)

plan = json.load(open(f"{BASE}/uploads_plan.json"))
results = []

for i, item in enumerate(plan):
    video = f"{VID}/{item['file']}"
    title = item["title"]
    desc = item["desc"]
    tags = item["tags"]
    thumb = f"{THUMB}/{item['thumb']}"

    body = {
        "snippet": {"title": title, "description": desc, "tags": tags,
                    "categoryId": "28", "defaultLanguage": "en", "defaultAudioLanguage": "en"},
        "status": {"privacyStatus": "private", "embeddable": True, "license": "youtube"},
    }
    print(f"[{i+1}/{len(plan)}] uploading {item['file']} ...")
    media = MediaFileUpload(video, chunksize=-1, resumable=True)
    resp = yt.videos().insert(part="snippet,status,contentDetails,player", body=body, media_body=media).execute()
    vid = resp["id"]
    print(f"  videoId={vid}")

    # playlist add (reliable path)
    yt.playlistItems().insert(
        part="snippet",
        body={"snippet": {
            "resourceId": {"kind": "youtube#video", "videoId": vid},
            "playlistId": PLAYLIST,
            "title": title,
            "position": i,
        }},
    ).execute()
    print(f"  added to playlist (position {i})")

    # custom thumbnail (may 403 until phone verification)
    try:
        yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(thumb, resumable=False)).execute()
        print("  thumbnail SET")
    except HttpError as e:
        print(f"  thumbnail 403 (set in Studio later): {e}")

    results.append({"file": item["file"], "videoId": vid,
                    "url": f"https://www.youtube.com/watch?v={vid}", "title": title})
    time.sleep(2)

json.dump(results, open(f"{BASE}/upload_batch_result.json", "w"), indent=2)
print(f"\n{len(results)} videos uploaded (all private).")
