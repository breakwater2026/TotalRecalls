from google.cloud import discoveryengine_v1 as de

def ingest_file_to_datastore(file_path, file_content):
    """
    Ingests a raw file string (like your Perplexity export) 
    directly into your Vertex AI Data Store.
    """
    project_id = "cs-poc-gw89wethbilefc1wrhgq7d7"
    location = "us"
    data_store_id = "totalrecalls-content-ds_1786555440982"
    
    client_options = {"api_endpoint": f"{location}-discoveryengine.googleapis.com"}
    client = de.DocumentServiceClient(client_options=client_options)
    
    # Path: projects/PROJECT/locations/LOCATION/collections/default_collection/dataStores/DATASTORE/branches/default_branch
    parent = f"projects/{project_id}/locations/{location}/collections/default_collection/dataStores/{data_store_id}/branches/default_branch"
    
    # Document definition
    doc = de.Document(
        id=os.path.basename(file_path).replace(".", "_"), # Must be unique
        struct_data={"text": file_content}, # Or use 'content' for raw bytes
    )
    
    request = de.CreateDocumentRequest(parent=parent, document=doc, document_id=doc.id)
    response = client.create_document(request=request)
    print(f"Ingested {file_path} successfully.")

if __name__ == "__main__":
    import os
    # Example: Ingest one of your export files
    path = r"C:\Users\break\TotalRecalls-export\sample_chat.json"
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            ingest_file_to_datastore(path, f.read())
    else:
        print("File not found - check the path for your chat exports.")
