# -*- coding: utf-8 -*-
"""Clean merged files: drop empty/dupe sections, renumber colliding headings.
Run AFTER merge_docs.py --apply. Idempotent. Regenerates paired docx.
"""
import os, re, difflib, hashlib

M = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
MANIFEST = os.path.join(M, "Jasper", "tools", "reports", "deleted-manifest.txt")
MERGED = [
 "ads/generic/Paid Ad Copy — Ad Variations & Search.md",
 "ads/google/Google Ads Copy — Search, Display & Video.md",
 "ads/linkedin/LinkedIn Ad Copy.md",
 "ads/meta/Meta Ad Copy.md",
 "ads/x/X Ad Copy.md",
 "email/sequences/Email Sequences 1-3 — Welcome, Upgrade, Urgency.md",
 "email/slot-2/Email 2 — all variants.md",
 "email/slot-3/Email 3 — all variants.md",
 "email/slot-4/Email 4 — all variants.md",
 "messaging/TotalRecalls Launch Campaign.md",
 "messaging/Landing Page Copy — 3 variants.md",
 "messaging/Press & Announcement Copy.md",
 "messaging/founder/Founder Story — Why I Built TotalRecalls (2 variants + profile).md",
 "social/facebook/Facebook Posts — all variants.md",
 "social/instagram/Instagram Captions — all variants.md",
 "social/linkedin/LinkedIn Posts — all variants.md",
 "social/x/X (Twitter) Posts — all variants.md",
 "strategy/TotalRecalls Launch Marketing Plan (Revised) — 2 variants.md",
 "youtube/YouTube Playlist Structure — 2 frameworks.md",
 "youtube/Main Explainer Video — Outline & Shot List.md",
 "website/Landing Page Copy — Hero & Trust.md",
]

def norm(s): return re.sub(r"\W+", "", s).lower()

def parse_sections(t):
    """Return (preamble, [(heading, [body lines]), ...])."""
    pre, secs, cur, body = [], [], None, []
    for line in t.splitlines():
        if line.startswith("## "):
            if cur is not None:
                secs.append((cur, body))
            cur, body = line[3:], []
        elif cur is None:
            pre.append(line)
        else:
            body.append(line)
    if cur is not None:
        secs.append((cur, body))
    return pre, secs

def main():
    man = []
    for f in MERGED:
        p = os.path.join(M, f)
        t = open(p, encoding="utf-8").read()
        pre, secs = parse_sections(t)
        # 1) drop sections whose body is empty or whitespace-only
        kept = []
        dropped = []
        for h, b in secs:
            if norm("\n".join(b)):
                kept.append((h, b))
            else:
                dropped.append(h)
        # 2) drop exact body duplicates (keep first)
        seen_body, kept2 = {}, []
        for h, b in kept:
            k = norm("\n".join(b))
            if k in seen_body:
                dropped.append(h + "  [body dup of %s]" % seen_body[k])
            else:
                seen_body[k] = h
                kept2.append((h, b))
        kept = kept2
        # 3) renumber heading collisions (distinct bodies, same heading)
        seen_h = {}
        final = []
        for h, b in kept:
            if h in seen_h:
                stem = os.path.splitext(os.path.basename(f))[0]
                h2 = f"{h} (alt)"
                n = 2
                while h2 in seen_h:
                    h2 = f"{h} (alt{n})"; n += 1
                man.append(f"REHEADED in {f}: '{h}' -> '{h2}'")
                h = h2
            seen_h[h] = 1
            final.append((h, b))
        if not dropped and len(final) == len(secs):
            continue
        # rewrite
        out = []
        for line in pre:
            out.append(line)
        while out and out[-1] == "":
            out.pop()
        out += ["", ""]
        for h, b in final:
            out += [f"## {h}", ""]
            out += b
            while out and out[-1] == "":
                out.pop()
            out += ["", ""]
        content = "\n".join(out).rstrip() + "\n"
        open(p, "w", encoding="utf-8").write(content)
        for d in dropped:
            man.append(f"DROPPED section in {f}: '{d}'")
        print(f"{f}: {len(secs)} -> {len(final)} sections"
              + (f"  (dropped: {dropped})" if dropped else ""))
        # regenerate docx
        from convert import convert_md
        os.chdir(M)
        convert_md(p, f[:-3] + ".docx")
        man.append(f"DOCX regenerated {f[:-3] + '.docx'}")
    if man:
        with open(MANIFEST, "a", encoding="utf-8") as fh:
            fh.write("\n".join(man) + "\n")
        print(f"manifest: +{len(man)} lines")

if __name__ == "__main__":
    main()
