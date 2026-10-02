# -*- coding: utf-8 -*-
"""Merge a per-video 'Alternative Hooks' doc into its script file.

Usage:
    python merge_hooks.py 6            # Video 6
    python merge_hooks.py 1 2 3 4 5 7 8 9 10   # batch

Rules:
  - Hooks doc:  youtube/hooks/YT Video N — Alternative Hooks.md
                (fallback: "Video N Alternative Hooks.md" in youtube/hooks/ or Jasper/)
  - Script:     youtube/scripts/YT Video N Script*.md — prefers (Final), else highest
                version (V3 > V2 > bare), skips .superseded/.
  - Appends the hooks doc as a trailing "## Alternative Hooks" section with the
    doc's own ## headings demoted to ###. Re-run replaces the section (idempotent).
  - Pair .docx regeneration is left to batch_convert.py (folder mode).
"""
import os, re, sys

ROOT = "C:/Users/break/projects/totalrecalls/marketing"
HOOKS_DIR = os.path.join(ROOT, "youtube", "hooks")
SCRIPTS_DIR = os.path.join(ROOT, "youtube", "scripts")

def find_hooks(n):
    cands = [f"YT Video {n} — Alternative Hooks.md",
             f"Video {n} Alternative Hooks.md"]
    for d in (HOOKS_DIR, os.path.join(ROOT, "Jasper")):
        for c in cands:
            p = os.path.join(d, c)
            if os.path.isfile(p):
                return p
    return None

def find_script(n):
    pat = re.compile(rf"^YT Video {n} Script( (.+))?\.md$")
    found = []
    for fn in os.listdir(SCRIPTS_DIR):
        m = pat.match(fn)
        if m and os.path.isfile(os.path.join(SCRIPTS_DIR, fn)):
            suffix = (m.group(2) or "").lower()
            score = 3 if "final" in suffix else (1 + len(re.findall(r"v\d+", suffix)))
            found.append((score, fn))
    if not found:
        return None
    found.sort(reverse=True)
    return os.path.join(SCRIPTS_DIR, found[0][1])

def demote(text):
    # drop the doc's own H1 title line; demote ## -> ###
    out, dropped_h1 = [], False
    for line in text.splitlines():
        if not dropped_h1 and line.startswith("# ") and not line.startswith("##"):
            dropped_h1 = True
            continue
        if line.startswith("## "):
            out.append("### " + line[3:])
        else:
            out.append(line)
    return "\n".join(out).strip()

def merge(n, apply=True):
    hooks = find_hooks(n)
    if not hooks:
        print(f"[{n}] SKIP — no hooks doc found")
        return False
    script = find_script(n)
    if not script:
        print(f"[{n}] SKIP — no script found")
        return False
    htext = open(hooks, encoding="utf-8").read()
    stext = open(script, encoding="utf-8").read()
    marker = "## Alternative Hooks"
    if marker in stext:  # idempotent: replace existing section
        stext = stext[:stext.find(marker)].rstrip() + "\n"
    section = stext.rstrip() + "\n\n---\n\n## Alternative Hooks (Jasper, 2026-09-29)\n\n" \
              + demote(htext) + "\n"
    if not apply:
        print(f"[{n}] dry-run: would append hooks section to {os.path.basename(script)}")
        return True
    open(script, "w", encoding="utf-8", newline="\r\n").write(section)
    print(f"[{n}] OK  {os.path.basename(hooks)} -> {os.path.basename(script)}")
    return True

if __name__ == "__main__":
    args = sys.argv[1:] or ["6"]
    apply = not any(a == "--dry-run" for a in args)
    nums = [int(a) for a in args if a.isdigit()]
    ok = all(merge(n, apply) for n in nums)
    print("\n" + ("all merged" if ok else "some skipped — see above"))
