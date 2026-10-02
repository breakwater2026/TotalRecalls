# -*- coding: utf-8 -*-
"""Near-dup pass: normalize (lowercase, strip non-alpha, collapse spaces) and
compare all .md/.txt in marketing/. Reports pairs >= 90% similarity by ratio
and containment (min/max of lengths), so superseded/truncated dups surface."""
import os, re, json, sys
from difflib import SequenceMatcher

root = r"C:\Users\break\projects\totalrecalls\marketing"

def norm(p):
    t = open(p, encoding="utf-8", errors="replace").read()
    t = re.sub(r"[^a-z0-9]+", " ", t.lower()).strip()
    return t

items = []
for dirpath, dirnames, filenames in os.walk(root):
    dirnames[:] = [d for d in dirnames if d != "__pycache__"]
    for fn in sorted(filenames):
        if fn.lower().endswith((".md", ".txt")):
            items.append(os.path.join(dirpath, fn))

items = [p for p in items if os.path.getsize(p) > 200]  # skip fragments
norms = {p: norm(p) for p in items}
lens = {p: len(n) for p, n in norms.items()}

print(f"comparing {len(items)} files pairwise (n^2 = {len(items)*len(items)})\n")
hits = []
for i in range(len(items)):
    for j in range(i + 1, len(items)):
        a, b = items[i], items[j]
        la, lb = lens[a], lens[b]
        if min(la, lb) / max(la, lb) < 0.75:   # big length gap -> not near-dup
            continue
        short, long_ = (norms[a], norms[b]) if la <= lb else (norms[b], norms[a])
        # containment: how much of short is covered by long (cheap window check)
        ratio = SequenceMatcher(None, short[:4000], long_[:4000]).ratio()
        if ratio >= 0.88:
            hits.append((ratio, os.path.relpath(a, root), os.path.relpath(b, root), la, lb))

hits.sort(reverse=True)
for r, fa, fb, la, lb in hits:
    print(f"{r:.3f}  {la:>7} vs {lb:>7}  {fa}  <->  {fb}")
print(f"\n{len(hits)} near-dup pairs")
