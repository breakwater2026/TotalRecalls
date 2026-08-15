import os, json
import google.auth
from googleapiclient.discovery import build

PROJECT_ID = "cs-poc-gw89wethbilefc1wrhgq7d7"

creds, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
svc = build("serviceusage", "v1", credentials=creds)

name = f"projects/{PROJECT_ID}/services/discoveryengine.googleapis.com"
print("=== Enabling Discovery Engine API ===")
try:
    res = svc.services().enable(name=name).execute()
    print("Enable request accepted; state:", res.get("state"))
    print("Service name:", res.get("serviceName"))
except Exception as e:
    print("enable failed:", e)
