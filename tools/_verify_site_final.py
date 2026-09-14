"""Final website verification: dist ZIP SHA == page SHA, no dead internal links,
troubleshooting copy updated."""
import os, re, glob, hashlib, urllib.parse

dist = r"C:\Users\break\Projects\TotalRecalls\site\dist"

zpath = os.path.join(dist, "downloads", "TotalRecalls-1.0.0-free-tier.zip")
zsha = hashlib.sha256(open(zpath, "rb").read()).hexdigest()
page = open(os.path.join(dist, "download", "index.html"), encoding="utf-8").read()
m = re.search(r'([0-9a-f]{64})', page)
page_sha = m.group(1) if m else None
print("dist ZIP SHA:", zsha)
print("page SHA    :", page_sha)
print("MATCH:", zsha == page_sha)

# dead internal links (root-aware)
def resolves(u, base_dir, is_root):
    path = urllib.parse.unquote(urllib.parse.urlparse(u).path)
    if not path:
        return True
    target = os.path.normpath(os.path.join(dist if is_root else base_dir, path.lstrip("/") if is_root else path))
    if os.path.exists(target):
        return True
    if os.path.isdir(target) and os.path.exists(os.path.join(target, "index.html")):
        return True
    return False

missing = set()
href_re = re.compile(r'(?:href|src)="([^"]+)"')
for f in glob.glob(os.path.join(dist, "**", "*.html"), recursive=True):
    base = os.path.dirname(f)
    txt = open(f, encoding="utf-8", errors="ignore").read()
    for m in href_re.findall(txt):
        u = m.strip()
        if not u or u.startswith(("http://", "https://", "mailto:", "tel:", "#", "data:", "javascript:")):
            continue
        if not resolves(u, base, u.startswith("/")):
            missing.add((os.path.relpath(f, dist), u))
print("DEAD INTERNAL LINKS:", len(missing))
for rel, u in sorted(missing)[:15]:
    print("  ", rel, "->", u)

# troubleshooting copy updated?
t = open(os.path.join(dist, "guides", "troubleshooting", "index.html"), encoding="utf-8").read()
print("troubleshooting mentions embedded sign-in window:", ("sign-in window" in t and "embedded window" in t))
print("troubleshooting no longer says 'default browser':", "in your default browser" not in t)
