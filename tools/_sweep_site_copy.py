"""Copy/consistency sweep of the V9 site source (site/src) + built dist.

Flags stale strings per the project conventions:
  - 'Perplexity Exporter' (old product name)
  - refund/money-back/guarantee/14-day (free-trial policy forbids refund language)
  - 'subscription' (one-time purchase, not subscription)
  - 'beta' (product is v1.0.0)
  - 'opens your browser' (login model is an EMBEDDED window)
  - version drift: 1.3.0 / 1.2.x (current = 1.0.0)
  - provider-count drift: 'five'/'5 providers'/'4 providers'/'three providers' claims
  - stale dates: 2025, 'September [1-8]' (release = September 12)
  - price drift: anything other than $24 for Pro
Also checks sitemap.xml covers all 52 pages.
"""
import os, re, glob

SRC = r"C:\Users\break\Projects\TotalRecalls\site\src"
DIST = r"C:\Users\break\Projects\TotalRecalls\site\dist"

CHECKS = [
    ("old product name", re.compile(r"Perplexity Exporter", re.I)),
    ("refund/guarantee", re.compile(r"refund|money-back|money back|guarantee", re.I)),
    ("14-day", re.compile(r"14[- ]day", re.I)),
    ("subscription", re.compile(r"subscription|monthly|per month|/mo\b", re.I)),
    ("beta", re.compile(r"\bbeta\b", re.I)),
    ("browser-login (should be embedded)", re.compile(r"opens your browser|open your browser|your browser to (sign|log)", re.I)),
    ("version drift 1.3/1.2", re.compile(r"1\.[23]\.\d")),
    ("provider-count drift", re.compile(r"\bfive providers?\b|\b5 providers?\b|\b4 providers?\b|\bfour providers?\b|\bthree providers?\b|\b3 providers?\b", re.I)),
    ("stale year 2025", re.compile(r"2025")),
    ("stale release month", re.compile(r"September [1-9]\b|August \d+|July \d+", re.I)),
    ("price drift", re.compile(r"\$\s?(?:2[0-35-9]|[3-9]\d|\d{3,})(?!\s?\d)")),
]

def scan(base, exts):
    hits = []
    for root, _d, files in os.walk(base):
        if "node_modules" in root or "_astro" in root:
            continue
        for f in files:
            if not any(f.endswith(e) for e in exts):
                continue
            fp = os.path.join(root, f)
            try:
                text = open(fp, encoding="utf-8", errors="replace").read()
            except Exception:
                continue
            for i, line in enumerate(text.splitlines(), 1):
                for label, pat in CHECKS:
                    for m in pat.finditer(line):
                        hits.append((label, os.path.relpath(fp, base), i, line.strip()[:110]))
    return hits

print("=== SRC (site/src) ===")
src_hits = scan(SRC, (".astro", ".jsx", ".js", ".json", ".md"))
for label, fp, i, line in src_hits:
    print(f"  [{label}] {fp}:{i}: {line}")
print(f"  total: {len(src_hits)}")

print("\n=== BUILT DIST (site/dist, excluding _astro chunks) ===")
dist_hits = scan(DIST, (".html",))
for label, fp, i, line in dist_hits:
    print(f"  [{label}] {fp}:{i}: {line}")
print(f"  total: {len(dist_hits)}")

# sitemap coverage
sm = os.path.join(DIST, "sitemap.xml")
if os.path.isfile(sm):
    urls = re.findall(r"<loc>([^<]+)</loc>", open(sm, encoding="utf-8").read())
    pages = {os.path.relpath(p, DIST).replace("\\", "/").rsplit(".html", 1)[0]
             for p in glob.glob(os.path.join(DIST, "**", "*.html"), recursive=True)
             if p.replace("\\", "/").find("_astro") == -1}
    print(f"\n=== sitemap === urls: {len(urls)}")
    for u in urls:
        print(f"  {u}")
