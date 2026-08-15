"""Upload the refactor background bundle to Cloud Storage for ingestion into the website-type data store."""
import os, json
from google.auth import default
from google.cloud import storage

PROJECT_ID = "cs-poc-gw89wethbilefc1wrhgq7d7"
LOCATION = "us"
DATA_STORE_ID = "totalrecalls-content-ds_1786555440982"
BUCKET_NAME = "totalrecalls-refactor-assets"

# Load ambient creds, pin to project
base, _ = default(scopes=["https://www.googleapis.com/auth/cloud-platform", "https://www.googleapis.com/auth/devstorage.full_control"])
if hasattr(base, "with_quota_project"):
    creds = base.with_quota_project(PROJECT_ID)
else:
    creds = base

# 1. Create the bucket (ignore if it exists)
storage_client = storage.Client(project=PROJECT_ID, credentials=creds)
try:
    storage_client.create_bucket(BUCKET_NAME, location=LOCATION)
    print(f"OK: created bucket {BUCKET_NAME}")
except Exception as e:
    # Likely already exists (409)
    print(f"bucket create returned: {str(e)[:80]}")
bucket = storage_client.bucket(BUCKET_NAME)

# 2. Build the JSON bundle
bundle = {}
plan_path = r"C:\Users\break\Projects\TotalRecalls\Website Design\TR V2 Implementation Plan.md"
with open(plan_path, 'r', encoding='utf-8') as f:
    bundle["tr_v2_plan"] = f.read()

pack_dir = r"C:\Users\break\Projects\TotalRecalls\Website Design\V2 Content Pack"
for filename in os.listdir(pack_dir):
    if filename.endswith(".md"):
        doc_id = filename.replace(".md", "")
        path = os.path.join(pack_dir, filename)
        with open(path, 'r', encoding='utf-8') as f:
            bundle[doc_id] = f.read()

bundle_json = json.dumps(bundle, indent=2, ensure_ascii=False)

gcs_uri = f"gs://{BUCKET_NAME}/tr_refactor_background.json"

# 3. Upload
blob = bucket.blob("tr_refactor_background.json")
blob.upload_from_string(bundle_json, content_type="application/json")
print(f"OK: uploaded bundle ({len(bundle_json)} bytes) to {gcs_uri}")
