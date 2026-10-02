"""OAuth code-capture mode.

Instead of run_local_server (which needs the browser to reach localhost),
use a registered-but-dummy redirect (http://localhost:9/). After the user
clicks Allow, the code is in the BROWSER ADDRESS BAR (page may error).
User pastes the code to Hermes; Hermes feeds it to the stdin of this
process, which completes the token exchange and runs the API checks.

Usage:
  python oauth_code_capture.py > capture_out.txt 2> capture_err.txt
  (background / detached; Hermes reads capture_out.txt and writes capture_in.txt)
"""
import json, os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

BASE = r"C:\Users\break\Projects\TotalRecalls\Marketing\Jasper\YouTube\yt-api"
TOKEN = f"{BASE}/token.json"
SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"


def status(msg):
    print(msg, flush=True)


# Print auth URL FIRST so Hermes can grab it before the user acts.
flow = InstalledAppFlow.from_client_secrets_file(
    f"{BASE}/credentials.json", [SCOPE], redirect_uri="http://localhost:9/"
)
auth_url, _ = flow.authorization_url(
    access_type="offline",
    prompt="consent",
    include_granted_scopes="true",
)
status("READY")
print("AUTH_URL=" + auth_url, flush=True)

status("WAITING_FOR_CODE_FROM_USER")
line = input().strip()  # Hermes writes the pasted code here
status(f"CODE_RECEIVED len={len(line)}")

# Accept either the bare code or a full callback URL containing ?code=
if line.startswith("http"):
    if "code=" in line:
        line = line.split("code=", 1)[1].split("&", 1)[0]
    else:
        status("NO_CODE_PARAM_FOUND")
        raise SystemExit(2)

flow.fetch_token(auth_response=line)
with open(TOKEN, "w") as f:
    json.dump(flow.credentials, f)
status("TOKEN_SAVED")

youtube = build("youtube", "v3", credentials=flow.credentials)
items = youtube.channels().list(
    part="snippet,contentDetails,statistics", mine=True
).execute().get("items", [])
result = {
    "channels": [
        {
            "title": c["snippet"]["title"],
            "id": c["id"],
            "handle": c["snippet"].get("customUrl"),
        }
        for c in items
    ]
}
pls = youtube.playlists().list(
    part="snippet", channelId=items[0]["id"]
).execute().get("items", [])
result["playlists"] = [
    {"id": p["id"], "title": p["snippet"]["title"]} for p in pls
]
with open(f"{BASE}/result.json", "w") as f:
    json.dump(result, f, indent=2)
status("DONE")
print(json.dumps(result, indent=2), flush=True)
