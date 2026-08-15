import google.auth
from googleapiclient.discovery import build

TARGET_PROJECT = "cs-poc-gw89wethbilefc1wrhgq7d7"
base, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
creds = base.with_quota_project(TARGET_PROJECT) if hasattr(base, "with_quota_project") else base
svc = build("serviceusage", "v1", credentials=creds, cache_discovery=False)

# Try the specific toggle names Google exposes for Vertex AI "add-ons"
targets = [
    "generativeaipreview.googleapis.com",
    "generativelanguage.googleapis.com",
    "aiplatform.googleapis.com",
    "discoveryengine.googleapis.com",
    "cloudaicompanion.googleapis.com",
    "cloudtrace.googleapis.com",
    "cloudprofiler.googleapis.com",
    "securitycenter.googleapis.com",
]
print("=== Current state of candidate services ===")
for t in targets:
    name = f"projects/{TARGET_PROJECT}/services/{t}"
    try:
        s = svc.services().get(name=name).execute()
        print(f"  {t}: {s.get('state')}")
    except Exception as e:
        print(f"  {t}: ERROR {str(e)[:150]}")

# Also check if there's a "feature" toggle exposed via billingbudgets / config
print("\n=== Trying to detect GenAI add-on via catalog/v1 ===")
try:
    pub = svc.services()
    # The undocumented endpoint that powers "Generative AI" add-on toggles:
    # services: testIamPermissions or a special "feature" resource.
    # Instead, let's list services that mention "generative" in their title.
    info = svc.services().list(
        parent=f"projects/{TARGET_PROJECT}",
        filter="state:ENABLED",
        pageSize=200,
    ).execute()
    for s in info.get("service", []):
        full = svc.services().get(name=s["name"], expand="CONSENT_INFO,CONTROL_PLANE").execute()
        st = full.get("state")
        title = full.get("title", "")
        if title and ("Generative" in title or "AI" in title or "Vertex" in title or "Companion" in title):
            print(f"  {s['serviceName']}: {st}  -- {title}")
    print("(if nothing printed above, none of the enabled services have a Generative/AI title)")
except Exception as e:
    print("catalog query failed:", str(e)[:400])
