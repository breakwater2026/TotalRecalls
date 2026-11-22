"""OAuth test 2, v3.
authorization_url() first (writes url.txt immediately), then a thread
blocks on fetch_token() (which runs the localhost callback server).
"""
import json, os, time, threading

BASE = r"C:\Users\break\Projects\TotalRecalls\Marketing\Jasper\YouTube\yt-api"
TOKEN = f"{BASE}/token.json"
URL_FILE = f"{BASE}/url.txt"
STATUS = f"{BASE}/status.txt"

def status(msg):
    open(STATUS, "w").write(msg)
    print(msg, flush=True)

from google_auth_oauthlib.flow import InstalledAppFlow
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
flow = InstalledAppFlow.from_client_secrets_file(f"{BASE}/credentials.json", SCOPES)
auth_url = flow.authorization_url(
    access_type="offline", include_granted_scopes="true", prompt="consent"
)
open(URL_FILE, "w").write(auth_url)
status("WAITING_FOR_CONSENT")
print("AUTH_URL=" + auth_url, flush=True)

t = threading.Thread(target=flow.fetch_token, daemon=True)
t.start()
t.join()  # fetch_token runs the local callback server until redirect arrives
json.dump(flow.credentials, open(TOKEN, "w"))
status("TOKEN_SAVED")

from googleapiclient.discovery import build
youtube = build("youtube", "v3", credentials=flow.credentials)
resp = youtube.channels().list(part="snippet,contentDetails,statistics", mine=True).execute()
items = resp.get("items", [])
out = {
    "channels": [
        {
            "title": ch["snippet"]["title"],
            "id": ch["id"],
            "handle": ch["snippet"].get("customUrl"),
            "subscribers": ch["statistics"].get("subscriberCount"),
            "videoCount": ch["statistics"].get("videoCount"),
            "uploads_playlist": ch["contentDetails"]["relatedPlaylists"]["uploads"],
        }
        for ch in items
    ]
}
if items:
    pl = youtube.playlists().list(part="snippet", channelId=items[0]["id"], maxResults=50).execute()
    out["playlists"] = [p["snippet"]["title"] for p in pl.get("items", [])]
json.dump(out, open(f"{BASE}/result.json", "w"), indent=2)
status("DONE")
print("RESULT=" + json.dumps(out, indent=2), flush=True)
