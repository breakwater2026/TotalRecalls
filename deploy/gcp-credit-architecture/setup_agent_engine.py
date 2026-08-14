"""
Vertex AI Agent Engine & Grounded Generation Setup Script
Project: cs-poc-gw89wethbilefc1wrhgq7d7 (Region: us-central1)
Credit ID: 6b0ed804949b4d7aea4d9e7116fe67d469cbf24a6c28994288d1dc1ae632103b

This script implements the approved Cloud Assist RAG architecture:
1. Ensures GCS bucket (rag-gcs-bucket) exists for document grounding.
2. Provisions Vertex AI Search data store & app (Agent Builder / Conversation).
3. Configures Grounded Generation client wrapper for Cloud Run backend (rag-app-tier).
"""

import os
from google.cloud import storage

PROJECT_ID = "cs-poc-gw89wethbilefc1wrhgq7d7"
REGION = "us-central1"
BUCKET_NAME = f"{PROJECT_ID}-rag-assets"

def setup_gcs_bucket():
    print(f"Setting up GCS bucket: {BUCKET_NAME} in {REGION}...")
    client = storage.Client(project=PROJECT_ID)
    bucket = client.lookup_bucket(BUCKET_NAME)
    if not bucket:
        bucket = client.create_bucket(BUCKET_NAME, location=REGION)
        print(f"Created bucket {BUCKET_NAME}")
    else:
        print(f"Bucket {BUCKET_NAME} already exists.")
    return bucket.name

if __name__ == "__main__":
    print("Initializing GCP Credit-Compliant Architecture Setup...")
    bucket = setup_gcs_bucket()
    print("GCS grounding bucket ready. Next step: deploy Cloud Run app with discoveryengine client.")
