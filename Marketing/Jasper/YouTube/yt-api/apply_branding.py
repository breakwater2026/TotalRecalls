"""Apply channel branding via API: banner, icon, description.

- banner  -> channelBanners.insert (new-channel endpoint; returns thumbnail URL)
- icon    -> brandThumbnailFiles.upload (profile image) + channels.update brandingSettings
- description -> channels.update snippet
"""
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

BASE = r"C:\Users\break\Projects\TotalRecalls\Marketing\Jasper\YouTube\yt-api"
ASSETS = r"C:\Users\break\Projects\TotalRecalls\Marketing\Jasper\YouTube"
SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
CHANNEL_ID = "UChO3ZyrGqRtBFHRuQx2qX1w"

CHANNEL_DESC = (
    "TotalRecalls saves your AI chats to your own Windows PC as searchable Markdown and JSON files.\n\n"
    "You sign in to each provider inside the app, on your own computer — ChatGPT, Claude, Perplexity, "
    "Gemini, Grok, DeepSeek, Mistral, and Qwen. Your conversations aren't sent to our servers, and there's "
    "no TotalRecalls account to create. No cloud. No account. No subscription.\n\n"
    "NEW VIDEOS: provider guides, weekly\n\n"
    "Download: https://totalrecalls.app\n"
    "Pricing: https://totalrecalls.app/pricing\n"
)

creds = Credentials.from_authorized_user_info(json.load(open(f"{BASE}/token.json")), [SCOPE])
yt = build("youtube", "v3", credentials=creds)

# --- banner ---
banner_thumb = None
try:
    r = yt.channelBanners().insert(
        media_body=MediaFileUpload(f"{ASSETS}/channel_banner_2560x1440.png", resumable=False),
    ).execute()
    banner_thumb = r.get("thumbnails", {}).get("default")
    print(f"banner: uploaded -> {banner_thumb}")
except HttpError as e:
    print(f"banner: {e}")

# --- icon (profile image) ---
icon_thumb = None
if hasattr(yt, "brandThumbnailFiles"):
    try:
        r = yt.brandThumbnailFiles().upload(
            media_body=MediaFileUpload(f"{ASSETS}/channel_icon_800.png", resumable=False),
            body={"alt": "TotalRecalls channel icon"},
        ).execute()
        icon_thumb = r.get("thumbnails", {}).get("default")
        print(f"icon: uploaded -> {icon_thumb}")
    except HttpError as e:
        print(f"icon: {e}")
else:
    print("icon: brandThumbnailFiles not in discovery — set manually in Studio")

# --- description + branding settings ---
body = {"id": CHANNEL_ID, "snippet": {"description": CHANNEL_DESC}}
if icon_thumb:
    body["brandingSettings"] = {"image": {"bannerUrl": banner_thumb or ""} }
try:
    r = yt.channels().update(part="snippet,brandingSettings", body=body).execute()
    print(f"description: SET on channel {r['id']}")
except HttpError as e:
    print(f"description: {e}")

print("done")
