# -*- coding: utf-8 -*-
"""Coverage proof: every indexed Jasper canvas doc has a local copy in the topic tree.
Matching: distinctive-title-token overlap (>=70%) against local filenames + first
headings, with char-count sanity within +/-20%."""
import json, re, os, glob

M = os.path.abspath("../../../..")
idx = json.load(open("canvas_index_stale_pre_consolidation.json", encoding="utf-8"))
docs = idx if isinstance(idx, list) else idx.get("docs", idx.get("documents", []))

GENERIC = {"the","a","an","of","to","for","and","or","in","on","with","at","your","you","is","it","be","from","by","this","that","totalrecalls","app","tr"}

def tokens(s):
    return {t for t in re.findall(r"[a-z0-9$]+", s.lower()) if t not in GENERIC and len(t) > 2}

local = []
for p in glob.glob(M + "/**/*.md", recursive=True):
    if "Jasper" in os.path.relpath(p, M).split(os.sep):
        continue
    txt = open(p, encoding="utf-8", errors="replace").read()
    first = ""
    for l in txt.splitlines():
        if l.strip():
            first = l.strip().lstrip("# ").strip()
            break
    local.append((p, os.path.basename(p), first, len(txt)))

print(f"local topic-tree .md files: {len(local)}")

def overlap(a, b):
    A, B = tokens(a), tokens(b)
    if not A:
        return 0.0
    return len(A & B) / len(A)

unmatched, matched = [], []
for d in docs:
    title, chars = d.get("title", ""), d.get("chars", 0)
    best = None
    for p, base, first, n in local:
        ov = max(overlap(title, base), overlap(title, first))
        if ov >= 0.70 and (best is None or ov > best[0]):
            best = (ov, p, chars, n)
    if best is None:
        unmatched.append((d.get("file"), title, chars))
    else:
        ov, p, chars, n = best
        flag = "" if 0.8 <= n / max(chars, 1) <= 1.25 else f"  <-- size {n} vs index {chars}"
        matched.append((title, os.path.relpath(p, M), flag))

print(f"indexed canvas docs: {len(docs)}")
print(f"matched: {len(matched)}   unmatched: {len(unmatched)}")
print("\n-- UNMATCHED --")
for f, t, c in unmatched:
    print(f"  ?? {t!r} ({c} chars)")
print("\n-- size-mismatch flags --")
for t, p, flag in matched:
    if flag:
        print(f"  {t!r} -> {p}{flag}")
