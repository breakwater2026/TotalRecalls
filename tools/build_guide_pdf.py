#!/usr/bin/env python3
"""Render markdown user guides and README to professional PDF files via headless Edge."""

import os
import subprocess
import markdown

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(REPO_ROOT, "docs")
SSE_DIR = os.path.join(REPO_ROOT, "Modules", "smart-search-engine")
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

CSS = """
@page {
  size: letter;
  margin: 0.8in;
}
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  color: #1e293b;
  line-height: 1.6;
  font-size: 10pt;
}
h1 {
  font-size: 19pt;
  font-weight: 700;
  color: #0f172a;
  border-bottom: 2px solid #2f7bff;
  padding-bottom: 6px;
  margin-top: 0;
  margin-bottom: 16px;
}
h2 {
  font-size: 13.5pt;
  font-weight: 600;
  color: #0f172a;
  border-bottom: 1px solid #e2e8f0;
  padding-bottom: 4px;
  margin-top: 22px;
  margin-bottom: 10px;
}
h3 {
  font-size: 11pt;
  font-weight: 600;
  color: #1e293b;
  margin-top: 16px;
  margin-bottom: 8px;
}
p, li {
  color: #334155;
  margin-bottom: 6px;
}
ul, ol {
  padding-left: 22px;
  margin-bottom: 10px;
}
li {
  margin-bottom: 3px;
}
code {
  font-family: 'Consolas', 'Courier New', monospace;
  font-size: 9pt;
  background-color: #f1f5f9;
  color: #0f172a;
  padding: 2px 4px;
  border-radius: 3px;
  border: 1px solid #e2e8f0;
}
pre {
  background-color: #f8fafc;
  border: 1px solid #e2e8f0;
  border-left: 4px solid #2f7bff;
  padding: 10px 12px;
  border-radius: 4px;
  overflow-x: auto;
  margin: 10px 0;
}
pre code {
  background: transparent;
  padding: 0;
  border: none;
  font-size: 8.5pt;
  color: #0f172a;
}
blockquote {
  border-left: 4px solid #f59e0b;
  background: #fffbeb;
  margin: 10px 0;
  padding: 8px 12px;
  color: #92400e;
  border-radius: 0 4px 4px 0;
}
blockquote p {
  color: #92400e;
  margin: 0;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin: 12px 0;
  font-size: 9pt;
}
th, td {
  border: 1px solid #cbd5e1;
  padding: 5px 8px;
  text-align: left;
}
th {
  background-color: #f1f5f9;
  font-weight: 600;
  color: #0f172a;
}
tr:nth-child(even) {
  background-color: #f8fafc;
}
hr {
  border: none;
  border-top: 1px solid #e2e8f0;
  margin: 16px 0;
}
.brand-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 18px;
  border-bottom: 1px solid #e2e8f0;
  padding-bottom: 6px;
  font-size: 8.5pt;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
"""

def render_md_to_pdf(md_path, pdf_path, subtitle="Official Documentation"):
    text = open(md_path, "r", encoding="utf-8").read()
    html_content = markdown.markdown(text, extensions=["fenced_code", "tables"])
    full_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset='utf-8'>
<style>{CSS}</style>
</head>
<body>
<div class='brand-header'>
  <span>TotalRecalls · Smart Search Engine</span>
  <span>{subtitle}</span>
</div>
{html_content}
</body>
</html>"""
    temp_html = pdf_path.replace(".pdf", "_temp.html")
    open(temp_html, "w", encoding="utf-8").write(full_html)
    cmd = [
        EDGE_PATH,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={os.path.abspath(pdf_path)}",
        os.path.abspath(temp_html)
    ]
    subprocess.run(cmd, check=True)
    if os.path.exists(temp_html):
        os.remove(temp_html)
    print(f"   Generated {os.path.basename(pdf_path)} ({os.path.getsize(pdf_path):,} bytes)")

def main():
    print("Generating PDF documentation...")
    render_md_to_pdf(
        os.path.join(DOCS_DIR, "TOTALRECALLS_SSE_QUICK_START_GUIDE.md"),
        os.path.join(DOCS_DIR, "Quick-Start Guide (TotalRecalls SSE).pdf"),
        subtitle="Quick-Start Guide"
    )
    render_md_to_pdf(
        os.path.join(DOCS_DIR, "TOTALRECALLS_POWER_USER_MANUAL.md"),
        os.path.join(DOCS_DIR, "Power User Guide (TotalRecalls SSE).pdf"),
        subtitle="Power User Manual"
    )
    render_md_to_pdf(
        os.path.join(SSE_DIR, "README-SSE.md"),
        os.path.join(SSE_DIR, "README.pdf"),
        subtitle="Technical Documentation"
    )

if __name__ == "__main__":
    main()
