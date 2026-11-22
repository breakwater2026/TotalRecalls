"""One-shot token exchange: re-build the identical flow (same client, PKCE)
and fetch the token with the authorization_response captured from the
browser address bar.
"""
import json, sys
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

BASE = r"C:\Users\break\Projects\TotalRecalls\Marketing\Jasper\YouTube\yt-api"
SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
AUTH_RESPONSE = "http://localhost:9/?state=gxMAsJlLqQQSW3dGPstwtITSV79ipr&iss=https://accounts.google.com&code=4/0AXlqoi5kflgtqQCeFhU91hMQLHy_bBbPUbtdSkUgrc3Rltaorr-6e5tbPRKxNUWV84VUmw&scope=https://www.googleapis.com/auth/youtube.force-ssl"

flow = InstalledAppFlow.from_client_secrets_file(
    f"{BASE}/credentials.json", [SCOPE], redirect_uri="http://localhost:9/"
)
# Build the exact same authorization request the browser used (PKCE code_verifier must match).
auth_url, _ = flow.authorization_url(
    access_type="offline", prompt="consent", include_granted_scopes="true"
)
code = AUTH_RESPONSE.split("code=", 1)[1].split("&", 1)[0]
flow.fetch_token(code=code)
with open(f"{BASE}/token.json", "w") as f:
    json.dump(flow.credentials, f)
print("TOKEN_SAVED")

youtube = build("youtube", "v3", credentials=flow.credentials)
items = youtube.channels().list(part="snippet,contentDetails,statistics", mine=True).execute().get("items", [])
result = {"channels": [{"title": c["snippet"]["title"], "id": c["id"], "handle": c["snippet"].get("customUrl")} for c in items]}
if items:
    pls = youtube.playlists().list(part="snippet", channelId=items[0]["id"]).execute().get("items", [])
    result["playlists"] = [{"id": p["id"], "title": p["snippet"]["title"]} for p in pls]
with open(f"{BASE}/result.json", "w") as f:
    json.dump(result, f, indent=2)
print("DONE")
print(json.dumps(result, indent=2))
