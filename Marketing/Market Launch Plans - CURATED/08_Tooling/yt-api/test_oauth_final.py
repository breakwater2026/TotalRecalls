"""OAuth test 2, final.
run_local_server(open_browser=False): the localhost callback server starts
immediately, prints the auth URL, then completes when the user's browser
redirects back with the code.
"""
import json, os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

BASE = r"C:\Users\break\Projects\TotalRecalls\Marketing\Jasper\YouTube\yt-api"
TOKEN = f"{BASE}/token.json"
URL_FILE = f"{BASE}/url.txt"
STATUS = f"{BASE}/status.txt"

def status(msg):
    open(STATUS, "w").write(msg)
    print(msg, flush=True)

if os.path.exists(TOKEN):
    creds = json.load(open(TOKEN))
    status("reusing cached token (no browser needed)")
else:
    flow = InstalledAppFlow.from_client_secrets_file(f"{BASE}/credentials.json",
                                                    ["https://www.googleapis.com/auth/youtube.force-ssl"])
    auth_url, _redirect_uri = flow.run_local_server(port=0, open_browser=False, timeout_seconds=3600)
    open(URL_FILE, "w").write(auth_url)
    status("WAITING_FOR_CONSENT")
    print("AUTH_URL=" + auth_url, flush=True)
    json.dump(flow.credentials, open(TOKEN, "w"))
    status("TOKEN_SAVED")
    creds = flow.credentials

youtube = build("youtube", "v3", credentials=creds)
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
