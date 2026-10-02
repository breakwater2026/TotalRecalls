
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
BASE = r"C:\Users\break\Projects\TotalRecalls\Marketing\Jasper\YouTube\yt-api"
API_KEY = open(BASE + "/api_key.txt").read().strip()
yt = build("youtube", "v3", developerKey=API_KEY)

for h in ["@totalrecalls", "@TotalRecalls", "@totalrecallsapp"]:
    try:
        r = yt.channels().list(part="snippet,statistics", handle=h).execute()
        items = r.get("items", [])
        print("handle", h, len(items), "item(s)", [(i['snippet']['title'], i['id']) for i in items])
    except HttpError as e:
        print("handle", h, "HTTP", e.resp.status)

r = yt.channels().list(part="snippet,statistics", id="UCjO3ZyrGqRtBfHRuQx2qX1w").execute()
print("by id:", len(r.get("items", [])), "item(s)")
