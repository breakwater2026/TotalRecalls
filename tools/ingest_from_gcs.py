"""Ingest the JSON bundle from Cloud Storage into the Website-type data store.
Websites stores require BOTH content (raw_bytes OR uri) AND a struct_data that
satisfies the data store's schema. We attach a minimal struct referencing the
source and let the GCS URI carry the actual payload."""
import json, time
import google.auth
from google.cloud import discoveryengine_v1 as de
from google.protobuf.struct_pb2 import Struct

PROJECT_NUMBER = "96283906207"
LOCATION = "us"
DATA_STORE_ID = "totalrecalls-content-ds_1786555440982"

base, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
creds = base.with_quota_project("cs-poc-gw89wethbilefc1wrhgq7d7") if hasattr(base, "with_quota_project") else base

doc_client = de.DocumentServiceClient(
    client_options={"api_endpoint": f"{LOCATION}-discoveryengine.googleapis.com"},
    credentials=creds,
)

branch = f"projects/{PROJECT_NUMBER}/locations/{LOCATION}/collections/default_collection/dataStores/{DATA_STORE_ID}/branches/default_branch"

s = Struct()
s["uri"] = "gs://totalrecalls-refactor-assets/tr_refactor_background.json"
s["mime_type"] = "application/json"

doc = de.Document(
    id="tr_refactor_background",
    struct_data=s,  # satisfies the website schema's "data" requirement
    content=de.Document.Content(
        uri="gs://totalrecalls-refactor-assets/tr_refactor_background.json",
        mime_type="application/json",
    ),
)
try:
    op = doc_client.create_document(parent=branch, document=doc, document_id="tr_refactor_background")
    print("OK: ingested background bundle from GCS URI")
    print("operation name:", op.operation.name)
except Exception as e:
    print("FAIL:", e)
