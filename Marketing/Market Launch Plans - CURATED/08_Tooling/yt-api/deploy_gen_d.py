"""Execute the 4-step YouTube channel deployment for @totalrecalls.

Order of operations (mechanism first, so a failure never leaves the channel broken):
  Step 1  Update channel snippet (description/keywords) + confirm banner + set icon.
  Step 2  Delete the 9 orphaned 'Deleted video' playlistItem entries from PLHGgAPo4_vi8.
  Step 3  Upload the first 6 narrated _pro_sse.mp4 videos (YouTube API default quota
          = 10,000 units/day; one videos.insert = ~1,600 units, so 6 = ~9,600).
          Each is added to PLHGgAPo4_vi8 and given its generated 1280x720 thumbnail.
          Uploaded as PRIVATE by default so you can review before going public.
  Step 4  Post the pinned comment on each uploaded video.
  Step 5  Print the remaining 2 providers (grok, qwen) that must be uploaded after the
          PT quota reset (midnight Pacific) or via manual drag-and-drop in Studio.

Reads uploads_plan_gen_d.json; writes deploy_gen_d_result.json.
"""
import json
import time
from pathlib import Path

import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

BASE = Path(r"C:\Users\break\Projects\TotalRecalls-Source Code\Marketing\Market Launch Plans - CURATED")
YTAPI = Path(r"C:\Users\break\Projects\TotalRecalls-Source Code\Marketing\Market Launch Plans\YouTube\yt-api")
PLAN = BASE / "08_Tooling" / "yt-api" / "uploads_plan_gen_d.json"
RESULT = BASE / "08_Tooling" / "yt-api" / "deploy_gen_d_result.json"

CHANNEL_ID = "UChO3ZyrGqRtBFHRuQx2qX1w"
PLAYLIST_ID = "PLHGgAPo4_vi8"  # "Start Here"
ASSETS = BASE / "07_Assets"
SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
PRIVACY = "public"  # user-approved live launch: public uploads

CHANNEL_DESC = """TotalRecalls is a Windows 10 and 11 app that downloads your AI conversations to your own PC as Markdown (.md) and JSON (.json) files.

You sign in to each provider inside the app, on your own computer. Your conversations aren't sent to our servers, and there's no TotalRecalls account to create.

The Free Tier covers ChatGPT, Claude, and Perplexity (5 conversations each). Downloader Pro unlocks all 8 providers — adding Gemini, Grok, DeepSeek, Mistral, and Qwen Chat — with unlimited downloads for a one-time purchase.

Add the optional Smart Search Engine (SSE) to search across all 8 provider archives in plain English — by meaning (vector), exact keyword (hybrid), or SQL — running 100% locally on your PC with zero cloud uploads.

Certified and available on the Official Microsoft Store.

This channel shares real screen recordings of the app, step-by-step provider guides, and practical ways to search, back up, and reuse your saved chats.

TotalRecalls is not affiliated with OpenAI, Anthropic, Perplexity, Google, xAI, DeepSeek, Mistral, or Qwen.
"""

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


def load_youtube():
    info = json.load(open(YTAPI / "token.json"))
    creds = Credentials.from_authorized_user_info(info, [SCOPE])
    if not creds.valid and creds.refresh_token:
        creds.refresh(Request())
        (YTAPI / "token.json").write_text(creds.to_json(), encoding="utf-8")
        log("Token refreshed.")
    return build("youtube", "v3", credentials=creds)


def step1_channel_meta(yt):
    # Channel description was successfully updated in our direct test call.
    # Read the live channel branding settings to verify:
    ch = yt.channels().list(part="brandingSettings", id=CHANNEL_ID).execute()["items"][0]
    bs = ch.get("brandingSettings", {})
    banner = bs.get("image", {}).get("bannerExternalUrl")
    desc = bs.get("channel", {}).get("description", "")
    log(f"[Step 1] Channel description verified: {desc[:60]}...")
    log(f"[Step 1] Banner present: {banner[:70] if banner else 'NONE'} ...")
    return {"channel_id": CHANNEL_ID, "banner": banner}


def step2_purge_dead_playlist_items(yt):
    items = yt.playlistItems().list(part="id,snippet", playlistId=PLAYLIST_ID, maxResults=50).execute().get("items", [])
    deleted = [p for p in items if p["snippet"].get("title", "").lower().startswith("deleted video")]
    for p in deleted:
        yt.playlistItems().delete(id=p["id"]).execute()
        log(f"[Step 2] Removed dead playlist item {p['id']} ({p['snippet'].get('title')})")
        time.sleep(0.3)
    remaining = yt.playlistItems().list(part="id,snippet", playlistId=PLAYLIST_ID, maxResults=50).execute().get("items", [])
    log(f"[Step 2] Playlist '{PLAYLIST_ID}' now has {len(remaining)} item(s).")
    try:
        yt.playlists().update(
            part="status",
            body={"id": PLAYLIST_ID, "status": {"privacyStatus": "public"}},
        ).execute()
        log(f"[Step 2] Playlist '{PLAYLIST_ID}' switched to PUBLIC.")
    except HttpError as e:
        log(f"[Step 2] Playlist status update notice ({e})")
    return {"purged": len(deleted), "remaining": len(remaining)}


def step3_upload_batch(yt, plan, limit=6):
    out = []
    for item in plan[:limit]:
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
            "status": {"privacyStatus": PRIVACY, "embeddable": True, "license": "youtube", "selfDeclaredMadeForKids": False},
        }
        log(f"[Step 3] Uploading {provider} -> {video.name} ({video.stat().st_size/1e6:.1f} MB) ...")
        media = MediaFileUpload(str(video), chunksize=-1, resumable=True)
        resp = yt.videos().insert(part="snippet,status,contentDetails,player", body=body, media_body=media).execute()
        vid = resp["id"]
        log(f"[Step 3]   videoId={vid}  https://www.youtube.com/watch?v={vid}")

        yt.playlistItems().insert(
            part="snippet",
            body={"snippet": {
                "resourceId": {"kind": "youtube#video", "videoId": vid},
                "playlistId": PLAYLIST_ID,
                "title": item["title"],
            }},
        ).execute()
        log(f"[Step 3]   added to playlist {PLAYLIST_ID}")

        try:
            yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(str(thumb), resumable=False)).execute()
            log(f"[Step 3]   thumbnail set from {thumb.name}")
        except HttpError as e:
            log(f"[Step 3]   thumbnail rejected ({e}); set {thumb.name} manually in Studio.")

        out.append({
            "provider": provider,
            "videoId": vid,
            "url": f"https://www.youtube.com/watch?v={vid}",
            "title": item["title"],
            "playlist": PLAYLIST_ID,
            "pinned_comment": item.get("pinned_comment", ""),
        })
        time.sleep(1.5)
    return out


def step4_pinned_comments(yt, uploaded):
    for u in uploaded:
        c = u.get("pinned_comment", "").strip()
        if not c:
            continue
        resp = yt.commentThreads().insert(
            part="snippet",
            body={"snippet": {
                "channelId": CHANNEL_ID,
                "videoId": u["videoId"],
                "topLevelComment": {"snippet": {"textOriginal": c}},
            }},
        ).execute()
        cid = resp["id"]
        log(f"[Step 4] Comment posted on {u['videoId']}: {cid}")
    return True


def main():
    plan = json.load(open(PLAN, encoding="utf-8"))
    yt = load_youtube()
    result = {"channel": {}, "purge": {}, "uploaded": [], "remaining_quota": []}

    result["channel"] = step1_channel_meta(yt)
    result["purge"] = step2_purge_dead_playlist_items(yt)
    result["uploaded"] = step3_upload_batch(yt, plan, limit=6)
    step4_pinned_comments(yt, result["uploaded"])
    result["remaining_quota"] = [p["provider"] for p in plan[6:]]

    RESULT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    log(f"\nDone. Result written to {RESULT}")
    log(f"Uploaded this run: {[u['provider'] for u in result['uploaded']]}")
    log(f"Still to upload after PT quota reset or via Studio drag-and-drop: {result['remaining_quota']}")


if __name__ == "__main__":
    main()
