# -*- coding: utf-8 -*-
"""Merge small same-topic docs into consolidated review files (2026-09-29).

Usage:
    python merge_docs.py            # dry-run: prints plan + resulting counts
    python merge_docs.py --apply    # executes

Each merged file: one H1 title, a provenance note, then one "## <title>" section
per source. Source headings are demoted one level; a bare first-line title that
matches the section title is dropped. Consumed sources + their .docx are
deleted and logged to deleted-manifest.txt; new .docx are generated via
convert.py::convert_md.
"""
import os, sys, re

HERE = os.path.dirname(os.path.abspath(__file__))
M = os.path.abspath(os.path.join(HERE, "..", "..", ".."))   # marketing root
sys.path.insert(0, HERE)

MANIFEST = os.path.join(M, "Jasper", "tools", "reports", "deleted-manifest.txt")

# ---------------------------------------------------------------- spec ----
# (output_rel, [ (source_rel, section_title_or_None=auto) , ... ])
MERGES = [
 ("ads/generic/Paid Ad Copy — Ad Variations & Search.md", [
    "ads/generic/Ad variation 1.md",
    "ads/generic/Ad variation 2.md",
    "ads/generic/Ad variation 3.md",
    "ads/generic/Search Ads.md",
 ]),
 ("ads/google/Google Ads Copy — Search, Display & Video.md", [
    "ads/google/Google Ads - Search.md",
    "ads/google/Google Ads - Search (variant 2).md",
    "ads/google/Google Ads - Display PMax.md",
    "ads/google/Google Ads - Display PMax (variant 2).md",
    "ads/google/Google Ads - Video.md",
    "ads/google/Google Ads - Video (variant 2).md",
 ]),
 ("ads/linkedin/LinkedIn Ad Copy.md", [
    "ads/linkedin/LinkedIn Ad.md",
    "ads/linkedin/LinkedIn Ads.md",
    "ads/linkedin/LinkedIn Ads (variant 2).md",
 ]),
 ("ads/meta/Meta Ad Copy.md", [
    "ads/meta/Meta Ads.md",
    "ads/meta/Meta Ads (variant 2).md",
 ]),
 ("ads/x/X Ad Copy.md", [
    "ads/x/X Ad.md",
    "ads/x/X Ads.md",
    "ads/x/X Ads (variant 2).md",
 ]),
 ("email/sequences/Email Sequences 1-3 — Welcome, Upgrade, Urgency.md", [
    "email/sequences/Sequence 1 Core Welcome Onboarding.md",
    "email/sequences/Sequence 2 Free-Tier to Pro Upgrade.md",
    "email/sequences/Sequence 2 Free-Tier to Pro Upgrade (variant 2).md",
    "email/sequences/Sequence 3 Launch Urgency.md",
    "email/sequences/Sequence 3 Launch Urgency (variant 2).md",
 ]),
 ("email/slot-2/Email 2 — all variants.md", [
    "email/slot-2/Email 2 One app, eight providers, one library.md",
    "email/slot-2/Email 2 One app, eight providers, zero chaos.md",
    "email/slot-2/Email 2 Why $24 once beats $10 a month, forever.md",
    "email/slot-2/Email 2 Why $24 once beats $10 a month.md",
    "email/slot-2/Email 2 48 hours left at $24.md",
    "email/slot-2/Email 2 48 hours left at $24 (variant 2).md",
    "email/slot-2/Email 2 Feature Spotlight.md",
 ]),
 ("email/slot-3/Email 3 — all variants.md", [
    "email/slot-3/Email 3 Still on the fence–.md",
    "email/slot-3/Email 3 Still on the fence– (variant 2).md",
    "email/slot-3/Email 3 Your chats. Your machine. Nobody else's.md",
    "email/slot-3/Email 3 No cloud. No account. Just your files.md",
    "email/slot-3/Email 3 Ownership.md",
    "email/slot-3/Email 3 Last call — pricing ends tonight.md",
    "email/slot-3/Email 3 Last call — pricing ends tonight (variant 2).md",
 ]),
 ("email/slot-4/Email 4 — all variants.md", [
    "email/slot-4/Email 4 Unlock all 8 providers for one $24 payment.md",
    "email/slot-4/Email 4 Unlock every provider — one time, $24.md",
    "email/slot-4/Email 4 Upgrade Offer.md",
 ]),
 ("messaging/TotalRecalls Launch Campaign.md", [
    "messaging/Campaign Abstract.md",
    "messaging/TotalRecalls Launch Campaign.md",
    "messaging/TotalRecalls Launch Campaign (variant 2).md",
 ]),
 ("messaging/Landing Page Copy — 3 variants.md", [
    "messaging/Recall every AI conversation you've ever had.md",
    "messaging/Recall every AI conversation, before it's gone for good.md",
    "messaging/Recall every AI conversation.md",
 ]),
 ("messaging/Press & Announcement Copy.md", [
    "messaging/Introducing TotalRecalls.md",
    "messaging/Launch Pricing Ends Soon.md",
    "messaging/blog/Blog Post — Why Your AI Conversations Deserve a Permanent Home.md",
    "messaging/Headlines.md",
 ]),
 ("messaging/founder/Founder Story — Why I Built TotalRecalls (2 variants + profile).md", [
    "messaging/founder/Why I Built TotalRecalls.md",
    "messaging/founder/Why I Built TotalRecalls (variant 2).md",
    "messaging/founder/Andre Denis — founder profile.md",
 ]),
 ("social/facebook/Facebook Posts — all variants.md", [
    "social/facebook/Facebook post.md",
    "social/facebook/Facebook post (variant 2).md",
    "social/facebook/Facebook post (variant 3).md",
    "social/facebook/Facebook post (variant 4).md",
    "social/facebook/Facebook post (variant 5).md",
 ]),
 ("social/instagram/Instagram Captions — all variants.md", [
    "social/instagram/Instagram caption.md",
    "social/instagram/Instagram caption (variant 2).md",
    "social/instagram/Instagram caption (variant 3).md",
    "social/instagram/Instagram caption (variant 4).md",
 ]),
 ("social/linkedin/LinkedIn Posts — all variants.md", [
    "social/linkedin/LinkedIn post.md",
    "social/linkedin/LinkedIn post (variant 2).md",
    "social/linkedin/LinkedIn post (variant 3).md",
    "social/linkedin/LinkedIn post (variant 4).md",
 ]),
 ("social/x/X (Twitter) Posts — all variants.md", [
    "social/x/X post.md",
    "social/x/X post (variant 2).md",
    "social/x/X post (variant 3).md",
    "social/x/Tweet.md",
    "social/x/Tweet (variant 2).md",
 ]),
 ("strategy/TotalRecalls Launch Marketing Plan (Revised) — 2 variants.md", [
    "strategy/TotalRecalls Launch Marketing Plan (Revised).md",
    "strategy/TotalRecalls Launch Marketing Plan (Revised) (variant 2).md",
 ]),
 ("youtube/YouTube Playlist Structure — 2 frameworks.md", [
    "youtube/YouTube Playlist Structure & Naming.md",
    "youtube/YouTube Playlist Structure & Naming (variant 2).md",
 ]),
 ("youtube/Main Explainer Video — Outline & Shot List.md", [
    "youtube/Main Product Explainer Video Outline.md",
    "youtube/Video Shot List.md",
 ]),
 ("website/Landing Page Copy — Hero & Trust.md", [
    "website/Landing Page — Homepage Hero Section.md",
    "website/Landing Page (Trust, Built Differently).md",
 ]),
]

# sources deleted outright (no merge): (rel, reason)
DELETE = [
 ("email/TotalRecalls Welcome Email Sequence (fragment).md",
  "byte-identical duplicate of Email Sequence (fragment).md (renamed to Email 1 Welcome — early draft.md)"),
 ("strategy/TotalRecalls Master Implementation Plan (draft capture).md",
  "42-char capture of the clean Master Implementation Plan with UI-artifact header (Select a Brand Voice)"),
 ("strategy/TotalRecalls Master Implementation Plan (variant 2).md",
  "partial capture — 100% of its content contained in the full Master Implementation Plan"),
 ("messaging/TotalRecalls Launch Campaign (variant 2).md",
  "truncated capture — 97% contained in the full Launch Campaign"),
 ("youtube/scripts/YT Video 5 Script V2 (variant 2).md",
  "fully contained in YT Video 5 Script V2 (V2 kept)"),
]

# renames: (rel, new_rel)
RENAMES = [
 ("email/Email Sequence (fragment).md",
  "email/sequences/Email 1 Welcome — early draft.md"),
 ("youtube/scripts/YT Video 6 Script (WIP truncated — needs re-download).md",
  "youtube/scripts/YT Video 6 Script (v2).md"),
]

# ---------------------------------------------------------------- utils ----
def norm(s): return re.sub(r"\W+", "", s).lower()

def read(rel): return open(os.path.join(M, rel), encoding="utf-8").read()

def section_title(rel, explicit):
    if explicit:
        return explicit
    first = next((l.strip() for l in read(rel).splitlines() if l.strip()), "")
    if first.startswith("#"):
        first = first.lstrip("# ").strip()
    return first[:80] or os.path.splitext(os.path.basename(rel))[0]

def unique_titles(srcs):
    """Content-based titles where unique within the merge; filename stems otherwise."""
    titles = [section_title(s, None) for s in srcs]
    first_at = {}
    for i, t in enumerate(titles):
        if t in first_at:
            titles[i] = os.path.splitext(os.path.basename(srcs[i]))[0]
        else:
            first_at[t] = i
    return titles

def demote(text, drop_title):
    """Demote markdown headings one level; optionally drop the first title line."""
    out = []
    for line in text.splitlines():
        m = re.match(r"^(#{1,5})(\s)", line)
        if m:
            out.append("#" + line)
        else:
            out.append(line)
    text = "\n".join(out)
    if drop_title:
        lines = text.splitlines()
        for i, l in enumerate(lines):
            if not l.strip():
                continue
            if l.strip().lstrip("# ") == drop_title or norm(l) == norm(drop_title):
                del lines[i]
                break
        text = "\n".join(lines)
    return text.strip()

def build_merged(out_rel, sources):
    title = os.path.splitext(os.path.basename(out_rel))[0]
    titles = unique_titles(sources)
    parts = [f"# {title}", "",
             f"> Merged 2026-09-29 from {len(sources)} documents for review — "
             f"each section is one original document, unedited.", ""]
    for src, st in zip(sources, titles):
        body = demote(read(src), drop_title=st)
        parts += [f"## {st}", "", body, ""]
    return "\n".join(parts).rstrip() + "\n"

def docx_path(md_rel):
    d, f = os.path.split(md_rel)
    return os.path.join(d, os.path.splitext(f)[0] + ".docx")

def main():
    apply = "--apply" in sys.argv
    # sanity
    problems = []
    for out, srcs in MERGES:
        if any(os.path.join(M, s) == os.path.join(M, out) for s in srcs) and \
           out != "messaging/TotalRecalls Launch Campaign.md":
            problems.append(f"in-place merge needs temp: {out}")
    for rel, _ in DELETE:
        if not os.path.isfile(os.path.join(M, rel)):
            problems.append(f"missing: {rel}")
    for s in [s for _, ss in MERGES for s in ss]:
        if not os.path.isfile(os.path.join(M, s)):
            problems.append(f"missing source: {s}")
    if problems:
        print("PROBLEMS:"); [print("  ", p) for p in problems]; return 1

    n_consumed = sum(len(s) for _, s in MERGES)
    print(f"plan: {len(MERGES)} merged files, {n_consumed} sources consumed, "
          f"{len(DELETE)} standalone deletions, {len(RENAMES)} renames")

    if apply:
        man = []
        # 1) renames first (so merges see final names)
        for old, new in RENAMES:
            po, pn = os.path.join(M, old), os.path.join(M, new)
            if os.path.abspath(pn) in [os.path.abspath(os.path.join(M, s)) for _, ss in MERGES for s in ss] + \
               [os.path.join(M, d) for d, _ in MERGES] :
                pass
            if os.path.exists(os.path.join(M, new)):
                print(f"RENAMED (already) {old} -> {new}"); continue
            if not os.path.exists(po):
                print(f"RENAMED (missing, already done) {old} -> {new}"); continue
            os.rename(po, pn)
            do, dn = docx_path(old), docx_path(new)
            if os.path.exists(do): os.rename(do, dn)
            man.append(f"RENAMED {old}  ->  {new}")
            print(f"RENAMED {old} -> {new}")
        # 2) read all sources, then write merged files
        for out, srcs in MERGES:
            po = os.path.join(M, out)
            have = [s for s in srcs if os.path.exists(os.path.join(M, s))]
            if po in [os.path.join(M, s) for s in srcs]:
                # in-place merge: read the pre-existing file FIRST (it's one of the sources)
                if os.path.exists(po) and os.path.abspath(po) not in \
                   [os.path.abspath(os.path.join(M, s)) for s in have if s == out]:
                    pass
                pre = open(po, encoding="utf-8").read() if os.path.exists(po) else ""
            else:
                pre = ""
            # rebuild from whatever sources still exist + pre-existing output content
            parts = [f"# {os.path.splitext(os.path.basename(out))[0]}", "",
                     "> Merged 2026-09-29 from documents for review — each section is one original document, unedited.", ""]
            seen_titles = {}
            for src in srcs:
                ps = os.path.join(M, src)
                if os.path.abspath(ps) == os.path.abspath(po):
                    if pre:
                        text = pre
                    else:
                        continue
                elif os.path.exists(ps):
                    text = read(src)
                else:
                    continue
                st = section_title(src, None)
                if st in seen_titles:
                    st = os.path.splitext(os.path.basename(src))[0]
                seen_titles[st] = 1
                body = demote(text, drop_title=st)
                parts += [f"## {st}", "", body, ""]
            content = "\n".join(parts).rstrip() + "\n"
            tmp = po + ".tmp"
            open(tmp, "w", encoding="utf-8").write(content)
            os.replace(tmp, po)
            # 3) docx for the new file
            from convert import convert_md
            os.chdir(M)
            convert_md(po, docx_path(out))
            # 4) consume sources (skip if == output)
            for s in srcs:
                ps = os.path.join(M, s)
                if os.path.abspath(ps) != os.path.abspath(po) and os.path.exists(ps):
                    os.remove(ps)
                    man.append(f"MERGED  {s}  ->  {out}")
                    pd = docx_path(s)
                    if os.path.exists(os.path.join(M, pd)):
                        os.remove(os.path.join(M, pd))
                        man.append(f"MERGED  {pd}  ->  {docx_path(out)}  (paired docx)")
        # 5) standalone deletions
        for rel, reason in DELETE:
            p = os.path.join(M, rel)
            if os.path.exists(p):
                os.remove(p)
                man.append(f"DELETED {rel}  ({reason})")
                pd = docx_path(rel)
                if os.path.exists(os.path.join(M, pd)):
                    os.remove(os.path.join(M, pd))
                    man.append(f"DELETED {docx_path(rel)}  (paired docx)")
        # 6) manifest
        with open(MANIFEST, "a", encoding="utf-8") as f:
            f.write("\n".join(man) + "\n")
        print(f"manifest: +{len(man)} lines")
    else:
        for out, srcs in MERGES:
            print(f"\n  {out}  ({len(srcs)} sources)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
