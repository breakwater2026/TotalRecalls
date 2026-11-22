"""OAuth test 2, manual-URL variant (threaded).
Background thread runs the local callback server with open_browser=False.
The auth URL is written to url.txt as soon as it's available.
User opens it in Chrome and clicks Allow; the thread completes on callback.
"""
import json, os, time, threading

BASE = r"C:\Users\break\Projects\TotalRecalls\Marketing\Jasper\YouTube\yt-api"
TOKEN = f"{BASE}/token.json"
URL_FILE = f"{BASE}/url.txt"
STATUS = f"{BASE}/status.txt"

def status(msg):
    open(STATUS, "w").write(msg)
    print(msg, flush=True)

state = {}

def run_flow():
    from google_auth_oauthlib.flow import InstalledAppFlow
    SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
    flow = InstalledAppFlow.from_client_secrets_file(f"{BASE}/credentials.json", SCOPES)
    auth_url, _redirect = flow.run_local_server(port=0, open_browser=False, timeout_seconds=3600)
    open(URL_FILE, "w").write(auth_url)
    status("WAITING_FOR_CONSENT url written")
    json.dump(flow.credentials, open(TOKEN, "w"))
    state["flow"] = flow
    status("TOKEN_SAVED")

t = threading.Thread(target=run_flow, daemon=True)
t.start()

# wait for the URL to appear
for _ in range(60):
    if os.path.exists(URL_FILE):
        break
    time.sleep(0.5)
print("AUTH_URL=" + (open(URL_FILE).read() if os.path.exists(URL_FILE) else "(not ready)"), flush=True)

t.join()
creds = json.load(open(TOKEN))

from googleapiclient.discovery import build
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
