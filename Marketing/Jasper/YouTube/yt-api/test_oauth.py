"""Test 2: OAuth -> mine=True channel read (YouTube Data API v3).

First run opens a browser for consent. Token is cached in token.json for reuse.
"""
import json, sys, os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

BASE = r"C:\Users\break\Projects\TotalRecalls\Marketing\Jasper\YouTube\yt-api"
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
TOKEN = f"{BASE}/token.json"

creds = None
if os.path.exists(TOKEN):
    creds = json.load(open(TOKEN))
    print("reusing cached token")
else:
    flow = InstalledAppFlow.from_client_secrets_file(f"{BASE}/credentials.json", SCOPES)
    creds = flow.run_local_server(port=0)

with open(TOKEN, "w") as f:
    json.dump(creds, f)
print("token saved ->", TOKEN)

youtube = build("youtube", "v3", credentials=creds)

req = youtube.channels().list(part="snippet,contentDetails,statistics", mine=True)
resp = req.execute()
items = resp.get("items", [])
print("mine=True returned", len(items), "channel(s)")
for ch in items:
    print("title:      ", ch["snippet"]["title"])
    print("channelId:  ", ch["id"])
    print("handle:     ", ch["snippet"].get("customUrl"))
    print("subscribers:", ch["statistics"].get("subscriberCount"))
    print("videoCount: ", ch["statistics"].get("videoCount"))
    print("uploads playlist id:", ch["contentDetails"]["relatedPlaylists"]["uploads"])

# also list existing playlists
pl = youtube.playlists().list(part="snippet", channelId=items[0]["id"], maxResults=50).execute() if items else {}
print("playlists:", [p["snippet"]["title"] for p in pl.get("items", [])])
