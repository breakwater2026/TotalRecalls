"""Phase 2: Ingest V2 Content Pack bundle into the Website-type data store.
Pattern: bundle all markdown into one JSON file in GCS, then create a single
Document with BOTH struct_data (satisfies schema) AND content.uri (carries payload)."""
import os, glob, json
from google.auth import default
from google.cloud import storage as gcs
from google.cloud import discoveryengine_v1 as de
from google.protobuf.struct_pb2 import Struct

PROJECT_NUMBER = "96283906207"
LOCATION = "us"
DATA_STORE_ID = "totalrecalls-content-ds_1786555440982"
BUCKET_NAME = "totalrecalls-refactor-assets"

content_dir = r"C:\Users\break\Projects\TotalRecalls\Website Design\V2 Content Pack"
creds, _ = default()

# 1. Build a single JSON bundle from all markdown files
md_files = sorted(glob.glob(os.path.join(content_dir, "**", "*.md"), recursive=True)) + \
           sorted(glob.glob(os.path.join(content_dir, "*.md")))

bundle = {}
for md_path in md_files:
    fname = os.path.basename(md_path).replace(".md", "")
    doc_id = fname.replace("_", "-").replace(".", "-")
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()
    bundle[doc_id] = {"title": fname.replace("_", " ").title(), "content": content}

# 2. Upload the bundle to GCS as JSON
gcs_client = gcs.Client(credentials=creds, project=PROJECT_NUMBER)
bucket = gcs_client.bucket(BUCKET_NAME)
blob = bucket.blob("v2_content_pack.json")
blob.upload_from_string(json.dumps(bundle, indent=2), content_type="application/json")
print(f"Uploaded bundle ({len(bundle)} docs) to gs://{BUCKET_NAME}/v2_content_pack.json")

# 3. Ingest using BOTH struct_data AND content.uri (the working pattern)
parent = f"projects/{PROJECT_NUMBER}/locations/{LOCATION}/collections/default_collection/dataStores/{DATA_STORE_ID}/branches/default_branch"
discovery_client = de.DocumentServiceClient(
    credentials=creds,
    client_options={"api_endpoint": f"{LOCATION}-discoveryengine.googleapis.com"},
)

GCS_URI = f"gs://{BUCKET_NAME}/v2_content_pack.json"

s = Struct()
s["uri"] = GCS_URI
s["mime_type"] = "application/json"

doc = de.Document(
    id="v2-content-pack-bundle",
    struct_data=s,
    content=de.Document.Content(uri=GCS_URI, mime_type="application/json"),
)

try:
    op = discovery_client.create_document(parent=parent, document=doc, document_id="v2-content-pack-bundle")
    print(f"[OK] v2-content-pack-bundle ingested")
except Exception as e:
    print(f"[FAIL] bundle: {str(e)[:200]}")

print("\nDone. The content pack is accessible to the Vertex AI agent.")
