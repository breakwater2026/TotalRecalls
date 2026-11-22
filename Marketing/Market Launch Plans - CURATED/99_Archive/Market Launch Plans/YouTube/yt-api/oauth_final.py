"""OAuth capture, FINAL: one process does consent-url -> poll file -> exchange -> checks.
Same flow object exchanges its own code, so PKCE verifier always matches.
"""
import json, os, time
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

BASE = r"C:\Users\break\Projects\TotalRecalls\Marketing\Jasper\YouTube\yt-api"
IN = f"{BASE}/capture_in.txt"
SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"


def status(msg):
    print(msg, flush=True)


flow = InstalledAppFlow.from_client_secrets_file(
    f"{BASE}/credentials.json", [SCOPE], redirect_uri="http://localhost:9/"
)
auth_url, _ = flow.authorization_url(
    access_type="offline", prompt="consent", include_granted_scopes="true"
)
status("READY")
print("AUTH_URL=" + auth_url, flush=True)

status("POLLING")
deadline = time.time() + 1800
line = ""
while time.time() < deadline:
    if os.path.exists(IN):
        with open(IN) as f:
            data = f.read().strip()
        if data:
            line = data
            break
    time.sleep(2)
if not line:
    status("TIMEOUT_NO_INPUT")
    raise SystemExit(1)

code = line.split("code=", 1)[1].split("&", 1)[0]
status(f"CODE_RECEIVED len={len(code)}")

flow.fetch_token(code=code)
with open(f"{BASE}/token.json", "w") as f:
    f.write(flow.credentials.to_json())
status("TOKEN_SAVED")

youtube = build("youtube", "v3", credentials=flow.credentials)
items = youtube.channels().list(part="snippet,contentDetails,statistics", mine=True).execute().get("items", [])
result = {"channels": [{"title": c["snippet"]["title"], "id": c["id"], "handle": c["snippet"].get("customUrl")} for c in items]}
if items:
    pls = youtube.playlists().list(part="snippet", channelId=items[0]["id"]).execute().get("items", [])
    result["playlists"] = [{"id": p["id"], "title": p["snippet"]["title"]} for p in pls]
with open(f"{BASE}/result.json", "w") as f:
    json.dump(result, f, indent=2)
status("DONE")
print(json.dumps(result, indent=2), flush=True)
