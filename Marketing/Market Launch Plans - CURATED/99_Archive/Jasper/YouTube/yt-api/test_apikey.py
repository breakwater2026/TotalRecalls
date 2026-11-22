"""Test 1: API key -> public channel info (YouTube Data API v3)."""
import json
from googleapiclient.discovery import build

BASE = r"C:\Users\break\Projects\TotalRecalls\Marketing\Jasper\YouTube\yt-api"
API_KEY = open(f"{BASE}/api_key.txt").read().strip()

youtube = build("youtube", "v3", developerKey=API_KEY)

req = youtube.channels().list(
    part="snippet,contentDetails,statistics",
    id="UChO3ZyrGqRtBFHRuQx2qX1w",
)
resp = req.execute()

if not resp.get("items"):
    print("NO CHANNEL RETURNED")
    raise SystemExit(1)

ch = resp["items"][0]
print("=== CHANNEL (API key, public read) ===")
print("title:      ", ch["snippet"]["title"])
print("channelId:  ", ch["id"])
print("handle:     ", ch["snippet"].get("customUrl"))
print("country:    ", ch["snippet"].get("country"))
print("uploadedAt: ", ch["snippet"]["publishedAt"])
print("desc:       ", (ch["snippet"].get("description") or "(empty)")[:120])
print("subscribers:", ch["statistics"].get("subscriberCount"))
print("videoCount: ", ch["statistics"].get("videoCount"))
print("viewCount:  ", ch["statistics"].get("viewCount"))
print("uploads playlist id:", ch["contentDetails"]["relatedPlaylists"]["uploads"])
