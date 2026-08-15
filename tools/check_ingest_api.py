"""Ad-hoc ingestion check — Website data store accepts struct_data for content-less docs."""
import os, time, json
import google.auth
from google.cloud import discoveryengine_v1 as de
from google.protobuf.struct_pb2 import Struct

PROJECT_NUMBER = "96283906207"
LOCATION = "us"
DATA_STORE_ID = "totalrecalls-content-ds_1786555440982"

base, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
creds = base.with_quota_project("cs-poc-gw89wethbilefc1wrhgq7d7")
client_options = {"api_endpoint": f"{LOCATION}-discoveryengine.googleapis.com"}
doc_client = de.DocumentServiceClient(client_options=client_options, credentials=creds)

branch = f"projects/{PROJECT_NUMBER}/locations/{LOCATION}/collections/default_collection/dataStores/{DATA_STORE_ID}/branches/default_branch"

print("=== Ingestion with struct_data payload ===")
content = "Ad-hoc verification document for TotalRecalls."
doc_id = f"hermes_verify_int_{int(time.time())}"

s = Struct()
s["content"] = content

doc = de.Document(id=doc_id, struct_data=s)
try:
    op = doc_client.create_document(parent=branch, document=doc, document_id=doc_id)
    print(f"  OK: ingested doc id={doc_id}")
except Exception as e:
    err = str(e).lower()
    if "already exists" in err:
        print(f"  OK (already exists): doc id={doc_id}")
    else:
        print(f"  INGEST FAIL: {e}")
print("=== DONE ===")
