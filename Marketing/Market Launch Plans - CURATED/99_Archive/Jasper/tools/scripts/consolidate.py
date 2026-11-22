# -*- coding: utf-8 -*-
"""Topical consolidation of marketing/Jasper artifacts. (v2)

- Groups all .md/.txt under marketing/Jasper by normalized content
  (strip non-alnum) -> finds stale duplicates across canvas_docs / jasper_docs / top level.
- For each document keeps ONE canonical .md (canvas preferred) + its paired .docx,
  moves them into a topical structure under marketing/<topic>/...
- Deletes stale copies; every move/delete logged to tools/reports/deleted-manifest.txt.
- Cross-capture near-dup collisions: LONGEST normalized content wins (truncation = stale).

Usage:  python consolidate.py --dry-run | --apply
"""
import hashlib, os, re, sys

ROOT = r"C:\Users\break\projects\totalrecalls\marketing"
J = os.path.join(ROOT, "Jasper")
CANVAS = os.path.join(J, "canvas_docs")
JASPER = os.path.join(J, "jasper_docs")
TOOLS = os.path.join(J, "tools")
MANIFEST = os.path.join(TOOLS, "reports", "deleted-manifest.txt")

# key -> "topic/subdir/canonical-name"  (final path = ROOT/<value>.md)
DOC = {
 # ---------- strategy / plans / calendars
 "TotalRecalls_Master_Implementation_Plan": "strategy/TotalRecalls Master Implementation Plan",
 "TotalRecalls_Launch_Marketing_Plan_Revised": "strategy/TotalRecalls Launch Marketing Plan (Revised)",
 "TotalRecalls_Launch_Marketing_Organization": "strategy/TotalRecalls Launch Marketing Organization",
 "TotalRecalls_Launch_Readiness_Plan": "strategy/TotalRecalls Launch Readiness Plan",
 "TotalRecalls_Launch_Gap_Checklist": "strategy/TotalRecalls Launch Gap Checklist",
 "TotalRecalls_Missing_Items_Checklist": "strategy/TotalRecalls Missing Items Checklist",
 "Missing_Items_Checklist": "strategy/TotalRecalls Missing Items Checklist",
 "TotalRecalls_60-Day_Launch_Content_Calendar_Blog_Guides": "strategy/TotalRecalls 60-Day Launch Content Calendar",
 "Content Calendar": "strategy/TotalRecalls 60-Day Launch Content Calendar",
 "Select_a_Brand_Voice": "strategy/TotalRecalls Master Implementation Plan (draft capture)",
 # ---------- emails
 "Sequence_1_Core_Welcome_Onboarding": "email/sequences/Sequence 1 Core Welcome Onboarding",
 "Sequence_2_Free-Tier_to_Pro_Upgrade": "email/sequences/Sequence 2 Free-Tier to Pro Upgrade",
 "Sequence_3_Launch_Urgency": "email/sequences/Sequence 3 Launch Urgency",
 "Free-Tier to Pro Upgrade Email": "email/sequences/Sequence 2 Free-Tier to Pro Upgrade",
 "Free-to-Pro Upgrade Email Sequence": "email/sequences/Sequence 2 Free-Tier to Pro Upgrade",
 "Email_2_48_hours_left_at_24": "email/slot-2/Email 2 48 hours left at $24",
 "Email_2_Feature_Spotlight": "email/slot-2/Email 2 Feature Spotlight",
 "Email_2_One_app_Eight_providers_One_library": "email/slot-2/Email 2 One app, eight providers, one library",
 "Email_2_One_app_eight_providers_zero_chaos": "email/slot-2/Email 2 One app, eight providers, zero chaos",
 "Email_2_Why_24_once_beats_10_a_month": "email/slot-2/Email 2 Why $24 once beats $10 a month",
 "Email_2_Why_24_once_beats_10_a_month_forever": "email/slot-2/Email 2 Why $24 once beats $10 a month, forever",
 "Email_3_Last_call_launch_pricing_ends_tonight": "email/slot-3/Email 3 Last call — pricing ends tonight",
 "Email_3_Last_call_pricing_ends_tonight": "email/slot-3/Email 3 Last call — pricing ends tonight",
 "Email_3_No_cloud_No_account_Just_your_files": "email/slot-3/Email 3 No cloud. No account. Just your files.",
 "Email_3_Ownership": "email/slot-3/Email 3 Ownership",
 "Email_3_Still_on_the_fence": "email/slot-3/Email 3 Still on the fence?",
 "Email_3_Your_chats_Your_machine_Nobody_else_s": "email/slot-3/Email 3 Your chats. Your machine. Nobody else's.",
 "Email_4_Unlock_all_8_providers_for_one_24_payment": "email/slot-4/Email 4 Unlock all 8 providers for one $24 payment",
 "Email_4_Unlock_every_provider_one_time_24": "email/slot-4/Email 4 Unlock every provider — one time, $24",
 "Email_4_Upgrade_Offer": "email/slot-4/Email 4 Upgrade Offer",
 "Email_Sequence": "email/Email Sequence (fragment)",
 "TotalRecalls Welcome Email Sequence": "email/TotalRecalls Welcome Email Sequence (fragment)",
 # ---------- paid ads
 "Ad_variation_1": "ads/generic/Ad variation 1",
 "Ad_variation_2": "ads/generic/Ad variation 2",
 "Ad_variation_3": "ads/generic/Ad variation 3",
 "Search_Ads": "ads/generic/Search Ads",
 "Google_Ads_-_Search": "ads/google/Google Ads - Search",
 "Google_Ads_-_Display/PMax": "ads/google/Google Ads - Display PMax",
 "Google_Ads_-_Display_PMax": "ads/google/Google Ads - Display PMax",
 "Google_Ads_-_Video": "ads/google/Google Ads - Video",
 "Meta_Ads": "ads/meta/Meta Ads",
 "LinkedIn_Ads": "ads/linkedin/LinkedIn Ads",
 "LinkedIn_Ad": "ads/linkedin/LinkedIn Ad",
 "X_Ads": "ads/x/X Ads",
 "X_Ad": "ads/x/X Ad",
 # ---------- youtube
 "TotalRecalls_YouTube_Channel_Description": "youtube/YouTube Channel Description",
 "TotalRecalls_YouTube_Content_Plan_Your_First_10_Videos": "youtube/YouTube Content Plan — First 10 Videos",
 "TotalRecalls_YouTube_Playlist_Structure_and_Naming_System": "youtube/YouTube Playlist Structure & Naming",
 "YouTube_Playlist_Structure_System_for_TotalRecalls": "youtube/YouTube Playlist Structure & Naming",
 "The_TotalRecalls_YouTube_Upload_Checklist_and_Template": "youtube/YouTube Upload Checklist & Template",
 "TotalRecalls_YouTube_Video_1_Save_AI_Chats_from_8_Providers": "youtube/scripts/YT Video 1 Script",
 "TotalRecalls_YouTube_Video_2_Why_I_Built_TotalRecalls": "youtube/scripts/YT Video 2 Script",
 "YT_Video_3_Script_V2": "youtube/scripts/YT Video 3 Script V2",
 "YT_Video_3_Script": "youtube/scripts/YT Video 3 Script",
 "YT_Video_4_Script": "youtube/scripts/YT Video 4 Script",
 "TotalRecalls YT Video 5 Script V2": "youtube/scripts/YT Video 5 Script V2",
 "YT_Video_6_SCRIPT_WIP_TRUNCATED": "youtube/scripts/YT Video 6 Script (WIP truncated — needs re-download)",
 "TotalRecalls YT Video 7 Script V3": "youtube/scripts/YT Video 7 Script V3",
 "TotalRecalls YT Video 8 Script V2": "youtube/scripts/YT Video 8 Script V2",
 "TotalRecalls YT Video 9 Script": "youtube/scripts/YT Video 9 Script",
 "TotalRecalls YT Video 10 Script": "youtube/scripts/YT Video 10 Script",
 "TotalRecalls_Video_Storyboard": "youtube/Video Storyboard",
 "TotalRecalls_Video_Shot_List": "youtube/Video Shot List",
 "TotalRecalls_Main_Product_Explainer_Video_Outline": "youtube/Main Product Explainer Video Outline",
 "TotalRecalls_Thumbnail_Concepts": "youtube/Thumbnail Concepts",
 "Short-Form_Video_Strategy": "youtube/Short-Form Video Strategy",
 # ---------- organic social
 "Instagram_caption": "social/instagram/Instagram caption",
 "Instagram_Caption": "social/instagram/Instagram caption",
 "Facebook_Post": "social/facebook/Facebook post",
 "Facebook_post": "social/facebook/Facebook post",
 "LinkedIn_post": "social/linkedin/LinkedIn post",
 "LinkedIn_Post": "social/linkedin/LinkedIn post",
 "X_Post": "social/x/X post",
 "X_Twitter": "social/x/X post",
 "Tweet": "social/x/Tweet",
 # ---------- website
 "Landing_Page_Homepage_Hero_Section": "website/Landing Page — Homepage Hero Section",
 "Part_1_Page-by-Page_Website_Optimization_Brief": "website/Part 1 Page-by-Page Website Optimization Brief",
 "Part_2_Homepage_Rewrite": "website/Part 2 Homepage Rewrite",
 "Landing Page": "website/Landing Page (Trust, Built Differently)",
 "Trust_Built_Differently": "website/Landing Page (Trust, Built Differently)",
 # ---------- messaging / copy assets
 "Campaign_Abstract": "messaging/Campaign Abstract",
 "TotalRecalls_Launch_Campaign": "messaging/TotalRecalls Launch Campaign",
 "Campaign Brief": "messaging/TotalRecalls Launch Campaign",
 "Introducing_TotalRecalls_Never_Lose_an_AI_Conversation_Again": "messaging/Introducing TotalRecalls",
 "Is_TotalRecalls_safe_to_use_and_why_does_Windows_show_a_warn": "messaging/FAQ — Is TotalRecalls safe, Windows warning",
 "FAQ (Frequently Asked Questions)": "messaging/FAQ — Is TotalRecalls safe, Windows warning",
 "Recall_every_AI_conversation": "messaging/Recall every AI conversation",
 "Recall_every_AI_conversation_before_it_s_gone_for_good": "messaging/Recall every AI conversation, before it's gone for good",
 "Recall_every_AI_conversation_you_ve_ever_had": "messaging/Recall every AI conversation you've ever had",
 "Headlines": "messaging/Headlines",
 "Blog_Post": "messaging/blog/Blog Post — Why Your AI Conversations Deserve a Permanent Home",
 "Launch_Pricing_Ends_Soon": "messaging/Launch Pricing Ends Soon",
 "ANDRE_DENIS": "messaging/founder/Andre Denis — founder profile",
 "Why_I_Built_TotalRecalls": "messaging/founder/Why I Built TotalRecalls",
 # ---------- ops
 "Launch-Day_Social_Posting_Checklist_TotalRecalls": "ops/Launch-Day Social Posting Checklist",
 # ---------- raw dumps (provenance)
 "Conversation Jasper ai-Day2": "raw_dumps/Conversation Jasper ai — Day2",
 "Jasper Plan 1": "raw_dumps/Jasper Plan 1 (full canvas export)",
 # ---------- meta (our own audit docs)
 "REORGANIZATION": "meta/REORGANIZATION (2026-09-28 canvas capture)",
 "TOPICS_AND_GAPS": "meta/TOPICS_AND_GAPS (2026-09-29 gap analysis)",
}

# stale content groups to drop entirely (superseded captures)
STALE_KEYS = {
    "TotalRecalls YT Video 8 Script": "superseded by V2 (V1 was truncated mid-generation)",
    "TotalRecalls YT Video 8 Script.dropped": "superseded by V2 (V1 was truncated mid-generation)",
    "TR Videos": "byte-identical duplicate of Video Storyboard (canvas 702707c6)",
    "Missing_Items_Checklist": "no-prefix re-capture of 9bb2daab — clean copy kept (has duplicated title line)",
}

HASH8 = re.compile(r"_[0-9a-f]{8}$")

def norm(p):
    t = open(p, encoding="utf-8", errors="replace").read()
    return re.sub(r"[^a-z0-9]+", " ", t.lower()).strip()

def doc_key(p):
    s = os.path.splitext(os.path.basename(p))[0]
    s = HASH8.sub("", s)
    return s

def main():
    apply_ = "--apply" in sys.argv
    text_files = []
    for dirpath, dirnames, filenames in os.walk(J):
        dirnames[:] = [d for d in dirnames if d not in ("__pycache__", "tools")]
        for fn in sorted(filenames):
            if fn.lower().endswith((".md", ".txt")) and fn not in ("audit_report.txt", "near_dup_report.txt"):
                text_files.append(os.path.join(dirpath, fn))

    groups = {}
    for p in text_files:
        n = norm(p)
        if not n:
            continue
        groups.setdefault(hashlib.sha256(n.encode()).hexdigest(), []).append(p)

    def rank(p):
        ext = 0 if p.lower().endswith(".md") else 1
        loc = 0 if os.path.dirname(p) == CANVAS else (1 if os.path.dirname(p) == JASPER else 3)
        return (ext, loc, p)

    keep, delete = {}, []
    for h, paths in groups.items():
        key = doc_key(paths[0])
        if key in STALE_KEYS:
            for p in sorted(paths):
                delete.append((p, STALE_KEYS[key]))
            continue
        keep[h] = sorted(paths, key=rank)[0]
        for p in sorted(paths, key=rank)[1:]:
            delete.append((p, "content-duplicate of " + os.path.basename(paths[0])))

    moves, unmapped = [], []
    for h, kp in keep.items():
        key = doc_key(kp)
        if key not in DOC:
            unmapped.append((kp, key))
            continue
        base = DOC[key]
        # Win32: '?' is a wildcard, ':' reserved — sanitize the final path.
        parts = base.split("/")
        parts[-1] = (parts[-1].replace("?", "–").replace(":", "–")
                     .replace("*", "–").replace("|", "–").strip(" ."))
        dst = os.path.join(ROOT, *parts) + ".md"
        docx = os.path.splitext(kp)[0] + ".docx"
        if not os.path.exists(docx):
            docx = None
        moves.append((kp, dst, docx))

    # cross-capture collisions on the same canonical name:
    #   identical-content groups already collapsed upstream; a collision here means
    #   DISTINCT variants sharing one canonical name -> keep all, suffix losers with
    #   " (variant N)". The longest/cleanest file becomes the base name.
    seen = {}
    for src, dst, docx in moves:
        seen.setdefault(dst, []).append((src, dst, docx))
    for dst, srcs in sorted(seen.items()):
        if len(srcs) > 1:
            srcs.sort(key=lambda sd: (len(norm(sd[0])), -rank(sd[0])[0]), reverse=True)
            winner, losers = srcs[0], srcs[1:]
            new_moves = []
            for i, (s, d, dx) in enumerate([winner] + losers, start=1):
                if i == 1:
                    new_moves.append((s, d, dx))
                else:
                    base, ext = os.path.splitext(d)
                    new_moves.append((s, f"{base} (variant {i})", dx))
            moves = [m for m in moves if m not in srcs] + new_moves
            print(f"VARIANTS -> {os.path.basename(dst)}: {len(srcs)} distinct versions kept (variant 1 = longest)")
            for i, (s, _, _) in enumerate([winner] + losers, start=1):
                print(f"    v{i}: {os.path.relpath(s, ROOT)} ({len(norm(s))} norm chars)")

    extra_del = []
    for p, why in delete:
        dx = os.path.splitext(p)[0] + ".docx"
        if os.path.exists(dx):
            extra_del.append((dx, why + " (paired docx)"))
    yt = os.path.join(J, "YouTube")
    if os.path.isdir(yt):
        for dirpath, _, filenames in os.walk(yt):
            for fn in filenames:
                extra_del.append((os.path.join(dirpath, fn),
                                  "old YouTube/ raw exports — superseded by canvas version"))

    print(f"text files scanned : {len(text_files)}")
    print(f"unique documents   : {len(groups)}")
    print(f"to keep & move     : {len(moves)}")
    print(f"to delete (md/txt) : {len(delete)}")
    print(f"to delete (docx)   : {len(extra_del)}")
    print(f"unmapped           : {len(unmapped)}")
    for u in unmapped:
        print("  UNMAPPED", u[0], "key=", u[1])

    if apply_:
        os.makedirs(os.path.dirname(MANIFEST), exist_ok=True)
        os.makedirs(os.path.join(TOOLS, "scripts"), exist_ok=True)
        lines = []
        for src, dst, docx in moves:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            os.replace(src, dst)
            if docx:
                os.replace(docx, os.path.splitext(dst)[0] + ".docx")
            lines.append(f"MOVED   {os.path.relpath(src, ROOT)}  ->  {os.path.relpath(dst, ROOT)}")
        for p, why in delete + extra_del:
            if os.path.exists(p):
                os.remove(p)
                lines.append(f"DELETED {os.path.relpath(p, ROOT)}  ({why})")
        # housekeeping: scripts + index + reports into tools/
        for fn in ("consolidate.py", "convert.py", "batch_convert.py", "sha_audit.py", "near_dup.py"):
            p = os.path.join(J, fn)
            if os.path.exists(p):
                os.replace(p, os.path.join(TOOLS, "scripts", fn))
                lines.append(f"MOVED   Jasper\\{fn}  ->  Jasper\\tools\\scripts\\{fn}")
        idx = os.path.join(CANVAS, "_index.json")
        if os.path.exists(idx):
            os.replace(idx, os.path.join(TOOLS, "reports", "canvas_index.json (stale — pre-consolidation)"))
            lines.append("MOVED   canvas_docs\\_index.json  ->  tools/reports/")
        for fn in ("audit_report.txt", "near_dup_report.txt"):
            p = os.path.join(J, fn)
            if os.path.exists(p):
                os.replace(p, os.path.join(TOOLS, "reports", fn))
                lines.append(f"MOVED   Jasper\\{fn}  ->  tools/reports/{fn}")
        open(MANIFEST, "w", encoding="utf-8").write("\n".join(lines) + "\n")
        print("\nAPPLIED. Manifest:", MANIFEST)
    else:
        print("\nDRY RUN — no changes.")

if __name__ == "__main__":
    main()
