"""Verify the document ingestion and then query it."""
import google.auth
from google.cloud import discoveryengine_v1 as de

PROJECT_NUMBER = "96283906207"
LOCATION = "us"
DATA_STORE_ID = "totalrecalls-content-ds_1786555440982"

base, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
creds = base.with_quota_project("cs-poc-gw89wethbilefc1wrhgq7d7") if hasattr(base, "with_quota_project") else base

doc_client = de.DocumentServiceClient(
    client_options={"api_endpoint": f"{LOCATION}-discoveryengine.googleapis.com"},
    credentials=creds,
)

doc_name = f"projects/{PROJECT_NUMBER}/locations/{LOCATION}/collections/default_collection/dataStores/{DATA_STORE_ID}/branches/default_branch/documents/tr_refactor_background"

# Attempt to fetch the document
print("=== Verifying Document ===")
try:
    doc = doc_client.get_document(name=doc_name)
    print("OK: document exists")
    print("name:", doc.name)
    print("id:", doc.id)
    # The content source is in the 'content' oneof
    if doc.content:
        print("content.uri:", doc.content.uri if hasattr(doc.content, 'uri') else "n/a")
except Exception as e:
    print("Verification failed:", e)

# Count documents in the data store to confirm ingestion
print("\n=== Counting Documents ===")
parent = f"projects/{PROJECT_NUMBER}/locations/{LOCATION}/collections/default_collection/dataStores/{DATA_STORE_ID}/branches/default_branch"
try:
    docs = list(doc_client.list_documents(parent=parent))
    print(f"Found {len(docs)} document(s):")
    for d in docs:
        print(f"  - {d.id}")
except Exception as e:
    print("List failed:", e)
