cat <<'EOF' > test_ds.py
from google.cloud import discoveryengine_v1 as de

def verify_connection():
    project_id = "cs-poc-gw89wethbilefc1wrhgq7d7"
    location = "us"
    data_store_id = "totalrecalls-content-ds_1786555440982"

    client = de.DocumentServiceClient()
    name = f"projects/{project_id}/locations/{location}/collections/default_collection/dataStores/{data_store_id}"

    try:
        print(f"Attempting to verify Data Store: {data_store_id}...")
        # List documents to check connection
        response = client.list_documents(parent=f"{name}/branches/default_branch")
        print("Success! Connection established. Data Store is accessible.")
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    verify_connection()
EOF