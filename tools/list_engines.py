import os, json
from google.cloud import discoveryengine_v1 as de

PROJECT_ID = "cs-poc-gw89wethbilefc1wrhgq7d7"
LOCATION = "us"

client_options = {"api_endpoint": f"{LOCATION}-discoveryengine.googleapis.com"}
client = de.EngineServiceClient(client_options=client_options)

parent = f"projects/{PROJECT_ID}/locations/{LOCATION}/collections/default_collection"

print("=== Listing Engines for project/data store ===")
try:
    ops = client.list_engines(parent=parent)
    engines = list(ops)
    print(f"Found {len(engines)} engine(s):")
    for e in engines:
        # Engine resource name format: projects/.../engines/{ENGINE_ID}
        print(f"  Engine ID: {e.name.split('/')[-1]!r}")
        print(f"  Full name: {e.name}")
        print(f"  Display name: {e.display_name}")
        print(f"  Solution type: {e.solution_types}")
        # The serving config is auto-generated per engine:
        sc_parent = e.name
        print(f"  Serving config would be: {sc_parent}/servingConfigs/default_search")
        print()
except Exception as ex:
    print("Engine listing failed:", ex)
    # Try fetching via the Data Store as fallback
    ds_client = de.DataStoreServiceClient(client_options=client_options)
    ds_name = f"{parent}/dataStores/totalrecalls-content-ds_1786555440982"
    try:
        ds = ds_client.get_data_store(name=ds_name)
        print("DataStore connected_engines:", ds.connected_engines)
    except Exception as ex2:
        print("Fallback data store fetch also failed:", ex2)
