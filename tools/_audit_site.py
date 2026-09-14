"""Website audit: SEO meta (title/description/og), a11y basics, pricing consistency."""
import os, re, glob

dist = r"C:\Users\break\Projects\TotalRecalls\site\dist"
pages = sorted(glob.glob(os.path.join(dist, "**", "index.html"), recursive=True))
if not os.path.join(dist, "404.html") in pages:
    pages.append(os.path.join(dist, "404.html"))

no_title, no_desc, no_og = [], [], []
img_no_alt, empty_links, small_text = [], [], []
for f in pages:
    t = open(f, encoding="utf-8", errors="ignore").read()
    rel = os.path.relpath(f, dist)
    if not re.search(r"<title[^>]*>\s*\S", t):
        no_title.append(rel)
    if 'name="description"' not in t and 'name=\'description\'' not in t:
        no_desc.append(rel)
    if "og:title" not in t:
        no_og.append(rel)
    # imgs without alt
    for m in re.finditer(r"<img\b[^>]*>", t):
        tag = m.group(0)
        if "alt=" not in tag:
            img_no_alt.append((rel, tag[:60]))
    # links with empty text
    for m in re.finditer(r'<a\b[^>]*>\s*</a>', t):
        empty_links.append(rel)

print(f"pages checked: {len(pages)}")
print("missing <title>:", no_title or "NONE")
print("missing meta description:", no_desc or "NONE")
print("missing og:title:", len(no_og), no_og[:10] if no_og else "NONE")
print("imgs missing alt:", len(img_no_alt))
for r, x in img_no_alt[:8]:
    print("   ", r, x)
print("empty <a></a>:", len(empty_links), set(empty_links) if empty_links else "")

# Pricing consistency across all pages: $24, 8 providers, 3 free, 5 convs
print("\n=== pricing/limit consistency (source) ===")
src = r"C:\Users\break\Projects\TotalRecalls\site\src"
allsrc = ""
for root, _, files in os.walk(src):
    for fn in files:
        if fn.endswith((".astro", ".jsx", ".json", ".md")):
            allsrc += open(os.path.join(root, fn), encoding="utf-8", errors="ignore").read()
pub = r"C:\Users\break\Projects\TotalRecalls\site\public"
for root, _, files in os.walk(pub):
    if "downloads" in root or "demo" in root:
        continue
    for fn in files:
        if fn.endswith((".txt", ".md", ".html")):
            allsrc += open(os.path.join(root, fn), encoding="utf-8", errors="ignore").read()

def count(pat):
    return len(re.findall(pat, allsrc))
print("mentions of '$24' / '24 USD' / '24$':", count(r"\$24|24 ?USD|24\$"))
print("mentions of 'one-time' (should be consistent):", count(r"one.?time"))
print("'8 providers'/'eight providers'/'all 8':", count(r"8 providers|eight providers|all 8"))
print("'3 providers'/'three providers' (free):", count(r"3 providers|three providers"))
print("'5 conversations'/'5 convs' (free):", count(r"5 conversations|5 convs|five conversations"))
# any conflicting numbers
for bad in ["$19", "$29", "$49", "$99", "subscription", "per month", "monthly", "annual"]:
    hits = re.findall(rf".{{20}}{bad}.{{20}}", allsrc, flags=re.I)
    if hits:
        print(f"  WARNING '{bad}': {len(hits)} hits")
        for h in hits[:3]:
            print("     ...", h.replace("\n", " "))
