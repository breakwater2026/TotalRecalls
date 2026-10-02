# -*- coding: utf-8 -*-
"""SHA256 audit of all .md/.txt in marketing/ — finds exact-duplicate groups."""
import hashlib, os, json, sys

root = r"C:\Users\break\projects\totalrecalls\marketing"
out = {"files": [], "dup_groups": [], "total_files": 0, "unique_hashes": 0}
hashes = {}
for dirpath, dirnames, filenames in os.walk(root):
    dirnames[:] = [d for d in dirnames if d != "__pycache__"]
    for fn in sorted(filenames):
        if not fn.lower().endswith((".md", ".txt")):
            continue
        p = os.path.join(dirpath, fn)
        h = hashlib.sha256(open(p, "rb").read()).hexdigest()
        rel = os.path.relpath(p, root)
        hashes.setdefault(h, []).append((rel, os.path.getsize(p)))

for h, v in sorted(hashes.items(), key=lambda kv: (-len(kv[1]), kv[1][0][0])):
    entry = {"sha256": h, "count": len(v), "size": v[0][1], "files": [r for r, _ in v]}
    out["files"].append({"path": v[0][0], "sha256": h, "size": v[0][1]})
    if len(v) > 1:
        out["dup_groups"].append(entry)

out["total_files"] = sum(len(v) for v in hashes.values())
out["unique_hashes"] = len(hashes)

if len(sys.argv) > 1:
    json.dump(out, open(sys.argv[1], "w", encoding="utf-8"), indent=1)
    print("saved", sys.argv[1])
else:
    print(f"total text files: {out['total_files']}, unique hashes: {out['unique_hashes']}, dup groups: {len(out['dup_groups'])}\n")
    for g in out["dup_groups"]:
        print(f"SHA {g['sha256'][:16]}  x{g['count']}  ({g['size']} bytes)")
        for f in g["files"]:
            print(f"   {f}")
        print()
