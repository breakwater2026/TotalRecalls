"""Audit item: ZIP EXE staleness + placeholder/TODO sweep."""
import zipfile, hashlib, os, re

z = zipfile.ZipFile(r"C:\Users\break\Projects\TotalRecalls\site\public\downloads\TotalRecalls-1.0.0-free-tier.zip")
data = z.read("TotalRecalls.exe")
sha = hashlib.sha256(data).hexdigest()
print("ZIP TotalRecalls.exe SHA-256:", sha)
print("  new dist free EXE          = f93ef897d6b48330ca0c3d6dd97c964af9d1814e450cb428e61e1f7d28f64774")
print("  verdict:", "STALE (old build)" if sha != "f93ef897d6b48330ca0c3d6dd97c964af9d1814e450cb428e61e1f7d28f64774" else "matches new build")

# placeholder sweep
SITE = r"C:\Users\break\Projects\TotalRecalls\site"
roots = [os.path.join(SITE, "src"), os.path.join(SITE, "public")]
hits = []
for root in roots:
    for dirpath, _, files in os.walk(root):
        if "node_modules" in dirpath:
            continue
        for fn in files:
            if fn.endswith((".astro", ".jsx", ".md", ".txt")):
                p = os.path.join(dirpath, fn)
                for i, line in enumerate(open(p, encoding="utf-8", errors="ignore"), 1):
                    if re.search(r"lorem ipsum|TODO|FIXME|XXX|under construction|\[insert|TBD|coming soon", line, re.I):
                        rel = os.path.relpath(p, SITE)
                        hits.append(f"{rel}:{i}: {line.strip()[:90]}")
print(f"\nplaceholder/TODO hits: {len(hits)}")
for h in hits[:20]:
    print("  ", h)
