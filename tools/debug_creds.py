import os, json
import google.auth
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Debug: discover which creds/projects are visible
try:
    creds, project = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    print("default() project:", project)
    print("creds type:", type(creds).__name__)
    svc = build("serviceusage", "v1", credentials=creds)
    # List enabled services on the ACTUAL authenticated project (whatever that is)
    try:
        info = svc.services().list(parent=f"projects/{project}", filter="state:ENABLED", pageSize=5).execute()
        enabled = [s["serviceName"] for s in info.get("service", [])]
        print("enabled on default project:", [e for e in enabled if "discoveryengine" in e])
    except Exception as e:
        print("list enabled failed:", e)
except Exception as e:
    print("default() failed:", e)

# Now explicitly enable on both projects
for pid in ["cs-poc-gw89wethbilefc1wrhgq7d7", "tmtwebsite-501119"]:
    try:
        c2, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
        # Force the quota_project / target
        if hasattr(c2, "with_quota_project"):
            c2 = c2.with_quota_project(pid)
        svc2 = build("serviceusage", "v1", credentials=c2)
        res = svc2.services().enable(name=f"projects/{pid}/services/discoveryengine.googleapis.com").execute()
        print(f"enable {pid}: accepted, op={res.get('operation')}")
    except Exception as ex:
        print(f"enable {pid} failed:", ex)
