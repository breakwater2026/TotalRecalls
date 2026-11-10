#!/usr/bin/env python3
"""Package TotalRecalls Smart Search Engine (SSE) add-on into a distributable ZIP.

Output:
  site/public/downloads/TotalRecalls-Smart-Search-Engine-1.0.0.zip
"""

import os
import zipfile
import hashlib

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SSE_DIR = os.path.join(REPO_ROOT, "Modules", "smart-search-engine")
OUT_ZIP = os.path.join(REPO_ROOT, "site", "public", "downloads", "TotalRecalls-Smart-Search-Engine-1.0.0.zip")

EXCLUDE_DIRS = {
    "node_modules",
    ".git",
    "scripts",
    "__pycache__",
    ".wrangler"
}

EXCLUDE_FILES = {
    ".gitignore",
    "package.json",
    "package-lock.json",
    "tsconfig.json",
    "metadata.json"
}

def main():
    print(f"Packaging SSE from {SSE_DIR}...")
    if not os.path.isdir(SSE_DIR):
        raise SystemExit(f"ERROR: SSE directory not found: {SSE_DIR}")

    os.makedirs(os.path.dirname(OUT_ZIP), exist_ok=True)
    
    with zipfile.ZipFile(OUT_ZIP, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        # Walk SSE directory
        for root, dirs, files in os.walk(SSE_DIR):
            # Prune excluded directories
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith(".")]
            
            for file in files:
                if file in EXCLUDE_FILES or file.startswith("."):
                    continue
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, SSE_DIR)
                # Store under root directory TotalRecalls-Smart-Search-Engine/
                archive_name = os.path.join("TotalRecalls-Smart-Search-Engine", rel_path)
                z.write(full_path, archive_name)

    data = open(OUT_ZIP, "rb").read()
    sha = hashlib.sha256(data).hexdigest()
    size_mb = len(data) / (1024 * 1024)
    print(f"\nSUCCESS! Package created at:")
    print(f"  {OUT_ZIP}")
    print(f"  Size: {size_mb:.2f} MB ({len(data):,} bytes)")
    print(f"  SHA-256: {sha}")

if __name__ == "__main__":
    main()
