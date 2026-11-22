# -*- coding: utf-8 -*-
import os, re
from collections import Counter

def norm(p):
    return re.sub(r"\W+", "", open(p, encoding="utf-8", errors="replace").read()).lower()

M = os.path.abspath(os.path.join(os.getcwd(), ".."))
refs = {
 "Google_Ads_Display_PMax.txt": ["ads/google/Google Ads - Display PMax.md", "ads/google/Google Ads - Display PMax (variant 2).md"],
 "Google_Ads_Search.txt": ["ads/google/Google Ads - Search.md", "ads/google/Google Ads - Search (variant 2).md"],
 "Google_Ads_Video.txt": ["ads/google/Google Ads - Video.md", "ads/google/Google Ads - Video (variant 2).md"],
 "Launch_Day_Social_Posting_Checklist_TotalRecalls.txt": ["ops/Launch-Day Social Posting Checklist.md"],
 "Part_1_Page_by_Page_Website_Optimization_Brief.txt": ["website/Part 1 Page-by-Page Website Optimization Brief.md"],
 "Short_Form_Video_Strategy.txt": ["website/Short-Form Video Strategy.md"],
 "TotalRecalls YT Video 3 Script V2.md": ["youtube/scripts/YT Video 3 Script V2.md"],
 "TotalRecalls_YouTube_Video_1_Save_AI_Chats_from_8_Providers_.txt": ["youtube/scripts/YT Video 1 Script.md"],
 "TotalRecalls YT Video 6 Script.md": ["youtube/scripts/YT Video 6 Script (WIP truncated \u2014 needs re-download).md"],
}
for txt, cands in refs.items():
    txt_path = os.path.join("jasper_docs", txt)
    n1 = norm(txt_path)
    for rel in cands:
        ref = os.path.join(M, rel)
        if not os.path.exists(ref):
            print(f"  {rel}: MISSING")
            continue
        n2 = norm(ref)
        prefix = n2.startswith(n1)
        c1, c2 = Counter(n1), Counter(n2)
        contained = sum((c1 & c2).values()) / len(n1)
        print(f"{txt} vs {rel}: prefix_of_ref={prefix} charbag_contained={contained:.3f} (txt {len(n1)} vs ref {len(n2)})")
