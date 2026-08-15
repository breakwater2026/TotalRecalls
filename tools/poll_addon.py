import os, time
import google.auth
from googleapiclient.discovery import build

TARGET_PROJECT = "cs-poc-gw89wethbilefc1wrhgq7d7"
base, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
creds = base.with_quota_project(TARGET_PROJECT) if hasattr(base, "with_quota_project") else base
svc = build("serviceusage", "v1", credentials=creds, cache_discovery=False)

targets = ["cloudaicompanion.googleapis.com", "generativelanguage.googleapis.com"]
for t in targets:
    name = f"projects/{TARGET_PROJECT}/services/{t}"
    print(f"Waiting for {t} to become ACTIVE...")
    for _ in range(12):  # poll up to ~5 minutes
        try:
            s = svc.services().get(name=name).execute()
            state = s.get("state")
            print(f"  state: {state}")
            if state == "ACTIVE":
                print(f"  -> {t} is ACTIVE")
                break
        except Exception as e:
            print(f"  get failed: {e}")
        time.sleep(25)
