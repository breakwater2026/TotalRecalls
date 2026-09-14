"""Full link/asset audit of the V9 built site (site/dist).

Walks every built .html, extracts href/src, checks:
  - internal links exist in dist (page or file)
  - relative asset refs (css/js/img) exist on disk
  - external URLs -> probed with GET (HEAD rejected by some servers)
Also lists sitemap/robots presence. Prints a structured report.
"""
import os, re, sys, ssl, json
import urllib.request
import concurrent.futures

DIST = r"C:\Users\break\Projects\TotalRecalls\site\dist"
DEV = "http://localhost:4321"

pages = []
for root, _dirs, files in os.walk(DIST):
    for f in files:
        if f.endswith(".html"):
            pages.append(os.path.join(root, f))
print(f"built pages found: {len(pages)}")

internal_missing = []   # (page, url)
external = {}           # url -> first page that references it
asset_missing = []      # (page, url)

ASSET_EXT = (".css", ".js", ".png", ".jpg", ".jpeg", ".svg", ".ico", ".webp",
             ".gif", ".mp4", ".webm", ".woff", ".woff2", ".ttf", ".avif")

for p in sorted(pages):
    try:
        html = open(p, encoding="utf-8", errors="replace").read()
    except Exception as e:
        print(f"READ FAIL {p}: {e}")
        continue
    pdir = os.path.dirname(p)
    for val in re.findall(r'(?:href|src)="([^"]+)"', html):
        url = val.strip()
        if not url or url.startswith(("data:", "#", "mailto:", "javascript:")):
            continue
        if re.match(r'^[a-z]+://', url):
            external.setdefault(url, os.path.relpath(p, DIST))
            continue
        if url.startswith("//"):
            external.setdefault("https:" + url, os.path.relpath(p, DIST))
            continue
        # internal
        path = url.split("#")[0].split("?")[0]
        if not path:
            continue
        if path.startswith("/"):
            cand = os.path.join(DIST, path.lstrip("/"))
        else:
            cand = os.path.join(pdir, path)
        cand = os.path.normpath(cand)
        ok = os.path.isfile(cand) or os.path.isdir(cand)
        if not ok:
            # page route: try /path/index.html
            ok = os.path.isfile(os.path.join(cand, "index.html"))
        if not ok:
            if any(path.lower().endswith(e) for e in ASSET_EXT):
                asset_missing.append((os.path.relpath(p, DIST), url))
            else:
                internal_missing.append((os.path.relpath(p, DIST), url))

print(f"\n=== INTERNAL LINKS MISSING in dist: {len(internal_missing)} ===")
for pg, u in sorted(set(internal_missing)):
    print(f"  {pg}  ->  {u}")

print(f"\n=== ASSET REFS MISSING on disk: {len(asset_missing)} ===")
for pg, u in sorted(set(asset_missing)):
    print(f"  {pg}  ->  {u}")

# dev-server 404 check on every page + missing internal links
def probe(url):
    try:
        req = urllib.request.Request(url, method="GET",
                                     headers={"User-Agent": "Mozilla/5.0 (TotalRecallsAudit)"})
        r = urllib.request.urlopen(req, timeout=15)
        return r.status, url
    except urllib.error.HTTPError as e:
        return e.code, url
    except Exception as e:
        return f"ERR:{type(e).__name__}", url

print(f"\n=== DEV SERVER: probing {len(pages)} pages + external URLs ===")
page_paths = [DEV + "/" + os.path.relpath(p, DIST).replace("\\", "/").rsplit(".html", 1)[0]
              + ("/" if not p.endswith("index.html") else "") for p in pages]
# normalize: relpath already includes index.html -> strip to route
page_paths = []
for p in pages:
    rel = os.path.relpath(p, DIST).replace("\\", "/")
    route = "/" + rel
    if route.endswith("index.html"):
        route = route[: -len("index.html")]
        if not route.endswith("/"):
            route += "/"
    page_paths.append(route)

targets = [(DEV + r, "page") for r in sorted(set(page_paths))]
ext_urls = sorted(external.keys())
targets += [(u, "external") for u in ext_urls]

bad = []
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
    futs = {ex.submit(probe, u): (u, kind) for u, kind in targets}
    for fut in concurrent.futures.as_completed(futs):
        status, url = fut.result()
        u, kind = futs[fut]
        if status != 200:
            bad.append((kind, u, status, external.get(u, "")))

print(f"total probed: {len(targets)}; non-200: {len(bad)}")
for kind, u, status, src in sorted(bad, key=lambda x: (x[0], str(x[2]))):
    extra = f"  (referenced by {src})" if kind == "external" else ""
    print(f"  [{kind}] HTTP {status}  {u}{extra}")

print(f"\n=== sitemap / robots ===")
for name in ("sitemap.xml", "robots.txt"):
    fp = os.path.join(DIST, name)
    print(f"  {name}: {'present' if os.path.isfile(fp) else 'ABSENT'}")
