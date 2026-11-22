# -*- coding: utf-8 -*-
"""Classify small-doc clusters: exact dup / truncated capture / genuine variant.
Output: for each pair in a topic group, containment + first-diff summary."""
import os, re, difflib, glob

M = os.path.abspath(os.path.join(os.getcwd(), "..", "..", ".."))  # marketing root
print("M =", M)

def norm(s): return re.sub(r"\W+", "", s).lower()
def body(p): return open(p, encoding="utf-8", errors="replace").read()

groups = {
 "ads/generic":  ["Ad variation 1", "Ad variation 2", "Ad variation 3", "Search Ads"],
 "ads/google":   ["Google Ads - Display PMax", "Google Ads - Display PMax (variant 2)",
                  "Google Ads - Search", "Google Ads - Search (variant 2)",
                  "Google Ads - Video", "Google Ads - Video (variant 2)"],
 "ads/linkedin": ["LinkedIn Ad", "LinkedIn Ads", "LinkedIn Ads (variant 2)"],
 "ads/meta":     ["Meta Ads", "Meta Ads (variant 2)"],
 "ads/x":        ["X Ad", "X Ads", "X Ads (variant 2)"],
 "email-root":   ["Email Sequence (fragment)", "TotalRecalls Welcome Email Sequence (fragment)"],
 "email/sequences": ["Sequence 1 Core Welcome Onboarding",
                     "Sequence 2 Free-Tier to Pro Upgrade", "Sequence 2 Free-Tier to Pro Upgrade (variant 2)",
                     "Sequence 3 Launch Urgency", "Sequence 3 Launch Urgency (variant 2)"],
 "email/slot-2": ["Email 2 48 hours left at $24", "Email 2 48 hours left at $24 (variant 2)",
                  "Email 2 Feature Spotlight",
                  "Email 2 One app, eight providers, one library",
                  "Email 2 One app, eight providers, zero chaos",
                  "Email 2 Why $24 once beats $10 a month, forever",
                  "Email 2 Why $24 once beats $10 a month"],
 "email/slot-3": ["Email 3 Last call — pricing ends tonight", "Email 3 Last call — pricing ends tonight (variant 2)",
                  "Email 3 No cloud. No account. Just your files",
                  "Email 3 Ownership",
                  "Email 3 Still on the fence–", "Email 3 Still on the fence– (variant 2)",
                  "Email 3 Your chats. Your machine. Nobody else's"],
 "email/slot-4": ["Email 4 Unlock all 8 providers for one $24 payment",
                  "Email 4 Unlock every provider — one time, $24",
                  "Email 4 Upgrade Offer"],
 "messaging-campaign": ["Campaign Abstract", "Launch Pricing Ends Soon",
                        "TotalRecalls Launch Campaign", "TotalRecalls Launch Campaign (variant 2)",
                        "Recall every AI conversation", "Recall every AI conversation, before it's gone for good",
                        "Recall every AI conversation you've ever had"],
 "messaging-founder": ["Why I Built TotalRecalls", "Why I Built TotalRecalls (variant 2)",
                       "Andre Denis — founder profile"],
 "social/facebook": ["Facebook post", "Facebook post (variant 2)", "Facebook post (variant 3)",
                     "Facebook post (variant 4)", "Facebook post (variant 5)"],
 "social/instagram": ["Instagram caption", "Instagram caption (variant 2)", "Instagram caption (variant 3)",
                      "Instagram caption (variant 4)"],
 "social/linkedin": ["LinkedIn post", "LinkedIn post (variant 2)", "LinkedIn post (variant 3)",
                     "LinkedIn post (variant 4)"],
 "social/x": ["Tweet", "Tweet (variant 2)", "X post", "X post (variant 2)", "X post (variant 3)"],
 "strategy": ["TotalRecalls Master Implementation Plan", "TotalRecalls Master Implementation Plan (variant 2)",
              "TotalRecalls Master Implementation Plan (draft capture)",
              "TotalRecalls Launch Marketing Plan (Revised)", "TotalRecalls Launch Marketing Plan (Revised) (variant 2)",
              "TotalRecalls Launch Marketing Organization", "TotalRecalls Launch Readiness Plan",
              "TotalRecalls Launch Gap Checklist", "TotalRecalls Missing Items Checklist",
              "TotalRecalls 60-Day Launch Content Calendar"],
 "youtube": ["YouTube Playlist Structure & Naming", "YouTube Playlist Structure & Naming (variant 2)",
             "Main Product Explainer Video Outline", "Short-Form Video Strategy", "Thumbnail Concepts",
             "Video Shot List", "YouTube Channel Description", "YouTube Content Plan — First 10 Videos",
             "YouTube Upload Checklist & Template"],
 "youtube/scripts": ["YT Video 3 Script", "YT Video 3 Script V2",
                     "YT Video 5 Script V2", "YT Video 5 Script V2 (variant 2)",
                     "YT Video 6 Script (WIP truncated — needs re-download)"],
 "website": ["Landing Page (Trust, Built Differently)", "Landing Page — Homepage Hero Section",
             "Part 1 Page-by-Page Website Optimization Brief", "Part 2 Homepage Rewrite"],
}

def resolve(dirname, stem):
    """Find file in marketing/<dirname>/<stem>.md"""
    d = os.path.join(M, dirname)
    if not os.path.isdir(d):
        return None
    for f in os.listdir(d):
        if f == stem + ".md":
            return os.path.join(d, f)
    return None

for gname, stems in groups.items():
    dirname = stems[0].split("/")[0] if "/" in stems[0] else None
    files = []
    for s in stems:
        # figure out actual dir from the original listing
        pass
    # map stems to real paths via a global index
    allmd = {}
    for root, dirs, files_ in os.walk(M):
        rel = os.path.relpath(root, M)
        if "Jasper" in rel.split(os.sep) or rel == "Jasper":
            continue
        for f in files_:
            if f.endswith(".md"):
                allmd[os.path.splitext(f)[0]] = os.path.join(root, f)
    print(f"\n===== {gname} =====")
    paths = []
    for s in stems:
        p = allmd.get(s)
        if p is None:
            # try basename match
            for k, v in allmd.items():
                if k == s or k.startswith(s[:40]):
                    p = v
                    break
        if p:
            paths.append((s, p))
        else:
            print(f"  MISSING: {s}")
    for i in range(len(paths)):
        for j in range(i + 1, len(paths)):
            s1, p1 = paths[i]; s2, p2 = paths[j]
            t1, t2 = body(p1), body(p2)
            n1, n2 = norm(t1), norm(t2)
            if n1 == n2:
                print(f"  EXACT    {s1} == {s2}  ({len(t1)} vs {len(t2)})")
                continue
            a, b = (n1, n2) if len(n1) <= len(n2) else (n2, n1)
            # containment: longest-common-prefix ratio of shorter within longer
            # use difflib on chunks
            shorter, longer = ((s1, t1), (s2, t2)) if len(t1) <= len(t2) else ((s2, t2), (s1, t1))
            sm, lm = norm(shorter[1]), norm(longer[1])
            ratio = difflib.SequenceMatcher(None, sm, lm).ratio()
            # prefix containment: does shorter's normalized body appear as substring?
            sub = sm in lm
            # how much of shorter is present in longer (chunk match)
            matcher = difflib.SequenceMatcher(None, sm, lm)
            blocks = sum(b.size for b in matcher.get_matching_blocks())
            cover = blocks / max(len(sm), 1)
            tag = "CONTAINED" if sub else ("~truncated?" if cover > 0.85 else "distinct")
            print(f"  {tag:11} {shorter[0][:38]:38} vs {longer[0][:38]:38}  ratio={ratio:.2f} cover={cover:.2f}  ({len(shorter[1])} vs {len(longer[1])})")
