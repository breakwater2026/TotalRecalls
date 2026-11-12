#!/usr/bin/env python3
"""Package TotalRecalls Smart Search Engine (SSE) add-on into a distributable ZIP.

Includes:
  - TotalRecalls Smart Search Engine standalone application (index.html, dist/bundle.js, run-smart-search.bat)
  - Quick-Start Guide (.docx & .md)
  - Power User Guide (.docx & .md)

Output:
  site/public/downloads/TotalRecalls-Smart-Search-Engine-1.0.0.zip
"""

import os
import zipfile
import hashlib
import subprocess

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SSE_DIR = os.path.join(REPO_ROOT, "Modules", "smart-search-engine")
DOCS_DIR = os.path.join(REPO_ROOT, "docs")
OUT_ZIP = os.path.join(REPO_ROOT, "site", "public", "downloads", "TotalRecalls-Smart-Search-Engine-1.0.0.zip")

def main():
    print(f"1. Building bundle.js with esbuild...")
    esbuild_bin = os.path.join(SSE_DIR, "node_modules", ".bin", "esbuild.cmd")
    if not os.path.exists(esbuild_bin):
        esbuild_bin = os.path.join(SSE_DIR, "node_modules", ".bin", "esbuild")
        
    cmd = [
        esbuild_bin,
        "index.tsx",
        "--bundle",
        "--outfile=dist/bundle.js",
        "--format=iife",
        "--jsx=automatic",
        "--target=chrome100,edge100",
        '--define:process.env.NODE_ENV="production"',
    ]
    subprocess.run(cmd, cwd=SSE_DIR, check=True)
    bundle_path = os.path.join(SSE_DIR, "dist", "bundle.js")
    print(f"   Compiled {bundle_path} ({os.path.getsize(bundle_path):,} bytes)")

    print(f"2. Generating User Guides and README .pdf files...")
    builder_script = os.path.join(REPO_ROOT, "tools", "build_guide_pdf.py")
    subprocess.run(["python", builder_script], check=True)

    print(f"3. Packaging SSE into {OUT_ZIP}...")
    os.makedirs(os.path.dirname(OUT_ZIP), exist_ok=True)
    
    ROOT_PREFIX = "TotalRecalls-Smart-Search-Engine"
    
    with zipfile.ZipFile(OUT_ZIP, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        # Core runtime files
        z.write(os.path.join(SSE_DIR, "index.html"), f"{ROOT_PREFIX}/index.html")
        z.write(os.path.join(SSE_DIR, "dist", "bundle.js"), f"{ROOT_PREFIX}/dist/bundle.js")
        if os.path.exists(os.path.join(SSE_DIR, "dist", "tailwind.css")):
            z.write(os.path.join(SSE_DIR, "dist", "tailwind.css"), f"{ROOT_PREFIX}/dist/tailwind.css")
        z.write(os.path.join(SSE_DIR, "run-smart-search.bat"), f"{ROOT_PREFIX}/run-smart-search.bat")
        
        # README files at root (.md + .pdf)
        z.write(os.path.join(SSE_DIR, "README-SSE.md"), f"{ROOT_PREFIX}/README.md")
        readme_pdf = os.path.join(SSE_DIR, "README.pdf")
        if os.path.exists(readme_pdf):
            z.write(readme_pdf, f"{ROOT_PREFIX}/README.pdf")
        
        # User Guides strictly in User Guides/ subfolder (.pdf and .md only, zero .docx)
        guides = [
            ("Quick-Start Guide (TotalRecalls SSE).pdf", "Quick-Start Guide (TotalRecalls SSE).pdf"),
            ("TOTALRECALLS_SSE_QUICK_START_GUIDE.md", "Quick-Start Guide (TotalRecalls SSE).md"),
            ("Power User Guide (TotalRecalls SSE).pdf", "Power User Guide (TotalRecalls SSE).pdf"),
            ("TOTALRECALLS_POWER_USER_MANUAL.md", "Power User Guide (TotalRecalls SSE).md"),
        ]
        
        for src_name, dest_name in guides:
            src_file = os.path.join(DOCS_DIR, src_name)
            if os.path.exists(src_file):
                z.write(src_file, f"{ROOT_PREFIX}/User Guides/{dest_name}")

    data = open(OUT_ZIP, "rb").read()
    sha = hashlib.sha256(data).hexdigest()
    size_mb = len(data) / (1024 * 1024)
    print(f"\nSUCCESS! Package created at:")
    print(f"  {OUT_ZIP}")
    print(f"  Size: {size_mb:.2f} MB ({len(data):,} bytes)")
    print(f"  SHA-256: {sha}")
    
    print("\nPackage Contents:")
    with zipfile.ZipFile(OUT_ZIP, "r") as z:
        for info in z.infolist():
            print(f"  {info.filename:55s} {info.file_size:>10,} bytes")

if __name__ == "__main__":
    main()
