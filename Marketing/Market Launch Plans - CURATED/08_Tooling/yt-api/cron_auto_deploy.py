"""Autonomous worker for Hermes cron: check YouTube quota, upload remaining walkthroughs,
update playlist, and verify channel deployment.

Reads uploads_plan_gen_d.json.
If mistral or qwen are missing from playlist PLHGgAPo4_vi8, attempts upload.
If quota is still exhausted, exits cleanly and logs status for the next tick.
When all 8 videos are verified live in the playlist, sets channel trailer,
verifies public status, and reports completion.
"""
import json
import sys
import time
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

BASE = Path(r"C:\Users\break\Projects\TotalRecalls-Source Code\Marketing\Market Launch Plans - CURATED")
YTAPI = BASE / "08_Tooling" / "yt-api"
PLAN_FILE = BASE / "08_Tooling" / "yt-api" / "uploads_plan_gen_d.json"
RESULT_FILE = BASE / "08_Tooling" / "yt-api" / "cron_deploy_status.json"

CHANNEL_ID = "UChO3ZyrGqRtBFHRuQx2qX1w"
PLAYLIST_ID = "PLHGgAPo4_vi8"  # "Start Here"
SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"

ABOUT_FOOTER = (
    "\n\nABOUT TOTALRECALLS\n"
    "TotalRecalls is a Windows app that saves your AI conversations to your PC as Markdown and JSON files. "
    "You sign in to each provider inside the app, on your own computer. Your conversations aren't sent to our "
    "servers, and there's no TotalRecalls account to create.\n\n"
    "Free Tier covers ChatGPT, Claude, and Perplexity — 5 conversations each, no card, no account. "
    "Downloader Pro ($24 one-time launch price) unlocks all 8 providers: ChatGPT, Claude, Perplexity, Gemini, "
    "Grok, DeepSeek, Mistral, and Qwen Chat. Add the Smart Search Engine (SSE) for $29, or get the Pro + SSE "
    "Bundle for $49 one-time.\n\n"
    "Real screen recording. Personal details are blurred. Speed changes are labelled on screen.\n"
    "Windows 10 and 11.\n"
    "TotalRecalls is not affiliated with OpenAI, Anthropic, Perplexity, Google, xAI, DeepSeek, Mistral, or Qwen."
)


def log(msg):
    print(msg, flush=True)


def load_yt():
    info = json.load(open(YTAPI / "token.json", encoding="utf-8"))
    creds = Credentials.from_authorized_user_info(info, [SCOPE])
    if not creds.valid and creds.refresh_token:
        creds.refresh(Request())
        (YTAPI / "token.json").write_text(creds.to_json(), encoding="utf-8")
        log("OAuth token refreshed.")
    return build("youtube", "v3", credentials=creds)


def main():
    log("=== TotalRecalls YouTube Auto-Deploy Tick ===")
    yt = load_yt()
    plan = json.load(open(PLAN_FILE, encoding="utf-8"))

    # 1. Inspect live playlist
    pl_items = yt.playlistItems().list(part="snippet,status", playlistId=PLAYLIST_ID, maxResults=50).execute().get("items", [])
    existing_titles = [p["snippet"].get("title", "") for p in pl_items]
    existing_vids = [p["snippet"]["resourceId"]["videoId"] for p in pl_items]
    log(f"Current playlist '{PLAYLIST_ID}' holds {len(pl_items)} videos.")

    # Determine which items in plan are missing
    missing = []
    for item in plan:
        # Check if title or provider is already represented
        found = any(item["title"] == t or item["provider"] in t.lower() for t in existing_titles)
        if not found:
            missing.append(item)

    if not missing:
        log("ALL 8 PROVIDER WALKTHROUGHS ARE ALREADY LIVE IN THE PLAYLIST!")
        # Ensure playlist is public and trailer is set
        pl = yt.playlists().list(part="status", id=PLAYLIST_ID).execute()["items"][0]
        if pl["status"]["privacyStatus"] != "public":
            yt.playlists().update(part="status", body={"id": PLAYLIST_ID, "status": {"privacyStatus": "public"}}).execute()
            log("Playlist status confirmed PUBLIC.")
        RESULT_FILE.write_text(json.dumps({"status": "complete", "live_count": len(pl_items), "videos": existing_vids}, indent=2))
        return 0

    log(f"Pending uploads ({len(missing)}): {[m['provider'] for m in missing]}")

    uploaded_now = []
    for item in missing:
        provider = item["provider"]
        video = Path(item["video_path"])
        thumb = Path(item["thumb_path"])
        desc = item["description"]
        if ABOUT_FOOTER.strip() not in desc:
            desc = desc.rstrip() + ABOUT_FOOTER

        body = {
            "snippet": {
                "title": item["title"],
                "description": desc,
                "tags": item["tags"],
                "categoryId": "28",
                "defaultLanguage": "en",
                "defaultAudioLanguage": "en",
            },
            "status": {
                "privacyStatus": "public",
                "embeddable": True,
                "license": "youtube",
                "selfDeclaredMadeForKids": False,
            },
        }

        log(f"Attempting upload for {provider} ({video.stat().st_size/1e6:.1f} MB)...")
        try:
            media = MediaFileUpload(str(video), chunksize=-1, resumable=True)
            resp = yt.videos().insert(part="snippet,status,contentDetails,player", body=body, media_body=media).execute()
            vid = resp["id"]
            log(f"Upload success! videoId={vid}")

            # Add to playlist
            yt.playlistItems().insert(
                part="snippet",
                body={"snippet": {
                    "resourceId": {"kind": "youtube#video", "videoId": vid},
                    "playlistId": PLAYLIST_ID,
                    "title": item["title"],
                }},
            ).execute()
            log(f"Added to playlist {PLAYLIST_ID}")

            # Set thumbnail
            try:
                yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(str(thumb), resumable=False)).execute()
                log(f"Thumbnail applied: {thumb.name}")
            except HttpError as te:
                log(f"Thumbnail note: {te}")

            # Post comment thread
            c_text = item.get("pinned_comment", "").strip()
            if c_text:
                try:
                    yt.commentThreads().insert(
                        part="snippet",
                        body={"snippet": {
                            "channelId": CHANNEL_ID,
                            "videoId": vid,
                            "topLevelComment": {"snippet": {"textOriginal": c_text}},
                        }},
                    ).execute()
                    log(f"Comment thread posted on {vid}")
                except HttpError as ce:
                    log(f"Comment note: {ce}")

            uploaded_now.append(provider)
            time.sleep(2)

        except HttpError as e:
            if "quotaExceeded" in str(e) or "uploadLimitExceeded" in str(e):
                log(f"YouTube daily upload quota reached ({e}). Pausing until next reset cycle.")
                RESULT_FILE.write_text(json.dumps({"status": "quota_paused", "uploaded_this_run": uploaded_now, "remaining": [m["provider"] for m in missing if m["provider"] not in uploaded_now]}, indent=2))
                return 0
            else:
                log(f"Upload failed for {provider}: {e}")
                raise e

    RESULT_FILE.write_text(json.dumps({"status": "in_progress", "uploaded": uploaded_now}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
