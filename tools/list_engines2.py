import os, json
import google.auth
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from google.auth.compute_engine import Credentials as CECredentials
from google.auth.impersonated_credentials import Credentials as ImpersonatedCredentials
import google.auth.transport.requests as tr_requests
from googleapiclient.discovery import build

# We need to call the API AS the target project. Ambient creds are for
# tmtwebsite-501119. To reach cs-poc..., we impersonate the cloudbuild/
# compute service account OR just set quota_project + re-run the listing.
# Easiest: use google-auth's "with_quota_project".

TARGET_PROJECT = "cs-poc-gw89wethbilefc1wrhgq7d7"
LOCATION = "us"

# Load ambient creds and force them to bill/talk to the right project.
base_creds, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
if hasattr(base_creds, "with_quota_project"):
    creds = base_creds.with_quota_project(TARGET_PROJECT)
else:
    creds = base_creds

# Discovery Engine is a regional gRPC endpoint tied to the data-store/engine project.
client_options = {"api_endpoint": f"{LOCATION}-discoveryengine.googleapis.com"}

from google.cloud import discoveryengine_v1 as de
engine_client = de.EngineServiceClient(client_info=None, client_options=client_options, credentials=creds)
ds_client = de.DataStoreServiceClient(client_options=client_options, credentials=creds)

parent = f"projects/{TARGET_PROJECT}/locations/{LOCATION}/collections/default_collection"

print("=== Listing Engines (target project:", TARGET_PROJECT, ") ===")
try:
    engines = list(engine_client.list_engines(parent=parent))
    print(f"Found {len(engines)} engine(s):")
    for e in engines:
        eid = e.name.split("/")[-1]
        print(f"  Engine ID: {eid!r}")
        print(f"  Full name: {e.name}")
        print(f"  Display name: {e.display_name}")
        print(f"  Serving config path: {e.name}/servingConfigs/default_search")
        print()
except Exception as ex:
    print("engine listing failed:", ex)

# Also try fetching the data store to read its connected_engines field.
ds_name = f"{parent}/dataStores/totalrecalls-content-ds_1786555440982"
print("=== Fetching Data Store details ===")
try:
    ds = ds_client.get_data_store(name=ds_name)
    print("data store name:", ds.name)
    print("display name:", ds.display_name)
    print("solution types:", ds.solution_types)
    print("connected_engines:", ds.connected_engines)  # this field tells us the linked engine
except Exception as ex:
    print("data store fetch failed:", ex)
