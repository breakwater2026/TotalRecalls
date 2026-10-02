# -*- coding: utf-8 -*-
"""Prove every doc in the Jasper canvas index has a local copy in the topic tree.
Match strategy per indexed doc: normalized-title match against each local file's
first heading line, plus char-count sanity. Reports unmatched index entries."""
import json, re, os, glob, difflib

M = os.path.abspath("../../../..")
idx = json.load(open("canvas_index_stale_pre_consolidation.json", encoding="utf-8"))
docs = idx if isinstance(idx, list) else idx.get("docs", idx.get("documents", []))

def norm(s):
    return re.sub(r"\W+", "", s).lower()

local_files = []
for pat in (M + "/*.md", M + "/*/*.md", M + "/*/*/*.md"):
    for p in glob.glob(pat):
        if os.path.relpath(p, M).startswith("Jasper"):
            continue
        local_files.append(p)

local_info = []
for p in local_files:
    txt = open(p, encoding="utf-8", errors="replace").read()
    lines = [l.strip() for l in txt.splitlines() if l.strip()]
    first = lines[0].lstrip("# ").strip() if lines else ""
    local_info.append((p, first, len(txt)))

# also collect normalized-content of every local file (for a fallback content check)
local_norm = {norm(open(p, encoding="utf-8", errors="replace").read()): p for p in local_files}

unmatched = []
for d in docs:
    title = d.get("title", "")
    chars = d.get("chars", 0)
    nt = norm(title)
    best = None
    for p, first, n in local_info:
        nf = norm(first)
        if not nf:
            continue
        # title match: exact, prefix, or close ratio
        if nt == nf or nt.startswith(nf) or nf.startswith(nt):
            best = (p, "title-exact")
            break
        r = difflib.SequenceMatcher(None, nt, nf).ratio()
        if r >= 0.82 and (best is None or r > best[2]):
            best = (p, f"title-ratio={r:.2f}", r)
    if best is None:
        unmatched.append((d.get("file"), title, chars))
    else:
        pass

print(f"indexed canvas docs : {len(docs)}")
print(f"local topic-tree md : {len(local_info)}")
print(f"matched             : {len(docs) - len(unmatched)}")
print(f"UNMATCHED           : {len(unmatched)}")
for f, t, c in unmatched:
    print(f"  ?? {t!r}  (chars={c}, index file={f})")

# duplicate check in the tree itself
from collections import Counter
c = Counter(local_norm.keys())
dups = [k for k, v in c.items() if v > 1]
print(f"\ntree internal duplicate content groups: {len(dups)}")
