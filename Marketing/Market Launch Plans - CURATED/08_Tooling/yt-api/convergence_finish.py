"""Idempotent convergence-video upload + playlist move, for cron.

Silent (exit 0, no output) while:
  - already done (marker file exists), OR
  - still hitting the new-channel upload quota (retry next tick).
On success: prints a one-time result summary.

Usage:  <project venv python> convergence_finish.py
"""
import json, os, sys, time, datetime

BASE = r"C:\Users\break\Projects\TotalRecalls\Marketing\Jasper\YouTube"
YT = os.path.join(BASE, "yt-api")
VIDEO = os.path.join(BASE, "videos", "TR_yt_convergence.mp4")
THUMB = os.path.join(BASE, "thumbnails", "tr_thumb_convergence.jpg")
DONE = os.path.join(YT, "convergence_done.json")
WARN = os.path.join(YT, "convergence_warned.flag")
TITLE = "How TotalRecalls Works — 8 AI Providers Into One Local Folder"
PL = "PLHGgAPo4_vi8"

# --- already done? stay silent ---
if os.path.exists(DONE):
    sys.exit(0)

import googleapiclient.errors
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
creds = Credentials.from_authorized_user_info(json.load(open(os.path.join(YT, "token.json"))), [SCOPE])
yt = build("youtube", "v3", credentials=creds)

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


def warn_once(msg):
    if not os.path.exists(WARN):
        try:
            open(WARN, "w").write(msg)
        except OSError:
            pass
        print(msg)


try:
    media = MediaFileUpload(VIDEO, chunksize=-1, resumable=True)
    body = {
        "snippet": {
            "title": TITLE, "description": desc, "tags": tags,
            "categoryId": "28", "defaultLanguage": "en", "defaultAudioLanguage": "en",
        },
        "status": {"privacyStatus": "private", "embeddable": True, "license": "youtube"},
    }
    resp = yt.videos().insert(part="snippet,status", body=body, media_body=media).execute()
    vid = resp["id"]
except googleapiclient.errors.HttpError as e:
    if "uploadLimitExceeded" in str(e) or "exceeded the number of videos" in str(e):
        sys.exit(0)  # quota still down — silent, retry next tick
    warn_once(f"CONVERGENCE upload failed (non-quota), will keep retrying: {str(e)[:300]}")
    sys.exit(0)

# --- add to Start Here, set thumbnail (best-effort), move to position 1 ---
yt.playlistItems().insert(
    part="snippet",
    body={"snippet": {"resourceId": {"kind": "youtube#video", "videoId": vid},
                     "playlistId": PL, "title": TITLE}},
).execute()

thumb_ok = False
try:
    m2 = MediaFileUpload(THUMB, mimetype="image/jpeg", resumable=True)
    yt.thumbnails().set(videoId=vid, media_body=m2).execute()
    thumb_ok = True
except Exception:
    pass  # phone-verify gate likely still active

time.sleep(1)
try:
    r = yt.playlistItems().list(part="contentDetails", playlistId=PL, maxResults=50).execute()
    item = next((it for it in r.get("items", []) if it["contentDetails"]["videoId"] == vid), None)
    if item:
        yt.playlistItems().delete(id=item["id"]).execute()
        time.sleep(1)
        yt.playlistItems().insert(
            part="snippet",
            body={"snippet": {"playlistId": PL, "position": 0,
                             "resourceId": {"kind": "youtube#video", "videoId": vid},
                             "title": TITLE}},
        ).execute()
except Exception as e:
    warn_once(f"convergence playlist move issue: {str(e)[:200]}")

r = yt.playlistItems().list(part="contentDetails", playlistId=PL, maxResults=50).execute()
order = [it["contentDetails"]["videoId"] for it in r.get("items", [])]
pos = order.index(vid) + 1 if vid in order else "?"

out = {"videoId": vid, "url": f"https://www.youtube.com/watch?v={vid}",
       "thumb_set": thumb_ok, "position": pos,
       "ts": datetime.datetime.now().isoformat(timespec="seconds")}
with open(DONE, "w") as f:
    json.dump(out, f, indent=2)

print(f"CONVERGENCE VIDEO UPLOADED (private): {out['url']}")
print(f"  thumbnail set via API: {thumb_ok}" + ("" if thumb_ok else f" (set in Studio: {THUMB})"))
print(f"  'Start Here' position: {pos} of {len(order)} (moved to top)")
print("  REMINDER for user: pin it as the channel trailer in Studio (Customization -> Basic info -> Feature this video).")
print("  Cron job 'convergence-upload' is now a silent no-op — ask Hermes to remove it when convenient.")
