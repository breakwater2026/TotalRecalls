import os
import google.auth
from googleapiclient.discovery import build

TARGET_PROJECT = "cs-poc-gw89wethbilefc1wrhgq7d7"
base, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
creds = base.with_quota_project(TARGET_PROJECT) if hasattr(base, "with_quota_project") else base
svc = build("serviceusage", "v1", credentials=creds, cache_discovery=False)

# List ALL services to find the generative AI add-on one.
try:
    info = svc.services().list(parent=f"projects/{TARGET_PROJECT}", filter="state:ENABLED", pageSize=200).execute()
    all_svcs = [s["serviceName"] for s in info.get("service", [])]
    for s in sorted(all_svcs):
        print(s)
except Exception as e:
    print("list failed:", str(e)[:300])
