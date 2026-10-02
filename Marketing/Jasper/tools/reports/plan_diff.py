# -*- coding: utf-8 -*-
import re, difflib, os
M = "C:/Users/break/projects/totalrecalls/marketing"
f = open(os.path.join(M, "strategy", "TotalRecalls Launch Marketing Plan (Revised) — 2 variants.md"), encoding="utf-8").read()
i1 = f.find("## TotalRecalls Launch Marketing Plan (Revised) (alt)")
h1 = "## TotalRecalls Launch Marketing Plan (Revised)\n"
h2 = "## TotalRecalls Launch Marketing Plan (Revised) (alt)\n"
i0 = f.find(h1)
v1 = f[i0+len(h1):i1]
v2 = f[i1+len(h2):]
v1, v2 = v1.strip(), v2.strip()
print("v1 chars:", len(v1), "| v2 chars:", len(v2))
def norm(s): return re.sub(r"\W+", "", s).lower()
a, b = norm(v1), norm(v2)
print("v2 fully in v1:", b in a, "| v1 fully in v2:", a in b)

def sents(s):
    return [x.strip() for x in re.split(r"(?<=[.:])\s+|\n", s) if len(x.strip()) > 25]
s1, s2 = sents(v1), sents(v2)
n1, n2 = set(norm(x) for x in s1), set(norm(x) for x in s2)
shared = n1 & n2
print(f"sentence units: v1={len(n1)} v2={len(n2)} shared={len(shared)} ({len(shared)/max(1,min(len(n1),len(n2))):.0%} of smaller)")

only1 = [x for x in s1 if norm(x) not in n2]
only2 = [x for x in s2 if norm(x) not in n1]
print(f"\n-- only in v1 ({len(only1)}) --")
for x in only1[:10]: print(" *", x[:140])
print(f"\n-- only in v2 ({len(only2)}) --")
for x in only2[:10]: print(" *", x[:140])

# structural comparison: which sections each has
def heads(s):
    out = []
    for line in s.splitlines():
        line = line.strip()
        if line and not line[0].isdigit() and len(line) < 40 and not line.startswith(("[", '"')):
            if line.lower().replace(" ", "") in [h.replace(" ","") for h in ["Overview","Objectives","Target Audience","Key Messages","Deliverables","Timeline","Channel Mix","Channel Roles","Short-Form Video Strategy","Content Pillars","Posting Cadence","Video Scripts"]]:
                out.append(line)
    return out
print("\nv1 structure:", heads(v1))
print("v2 structure:", heads(v2))
