# -*- coding: utf-8 -*-
"""Batch-convert flat Jasper exports to formatted .docx (same style as convert.py).

Usage:
    python batch_convert.py INPUT_FOLDER [OUTPUT_FOLDER] [--force] [--txt] [--docx]

  INPUT_FOLDER    folder holding the downloaded .md files (required)
  OUTPUT_FOLDER   where .docx files go (default: same as INPUT_FOLDER)
  --force         overwrite .docx files that already exist
  --txt           also convert .txt files
  --docx          also REFORMAT flat Jasper .docx dumps (output: "<name> - formatted.docx",
                  so your downloaded file is left untouched)

Naming: "My Doc.md" -> "My Doc.docx". Jasper sometimes names a file "My Doc.md.md"
(document titled 'My Doc.md'); the trailing '.md' is stripped so you get "My Doc.docx".

A summary is printed at the end; anything that errored is listed with the reason.
"""
import argparse, os, sys, time, traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from convert import convert_md

def clean_stem(path):
    stem = os.path.splitext(os.path.basename(path))[0]
    if stem.lower().endswith(".md"):          # Jasper artifact: "Title.md.md"
        stem = stem[:-3]
    return stem

def flatten_docx(docx_path):
    """Recover the flat text of a Jasper .docx dump (paragraphs, in order)."""
    from docx import Document
    doc = Document(docx_path)
    lines = []
    for p in doc.paragraphs:
        t = p.text
        lines.append(t if t else "")
    # Jasper dumps are one paragraph per line with no blank-line separators;
    # re-insert a blank line between every non-empty paragraph so convert_md
    # sees the same block structure as an .md export.
    out, prev_empty = [], True
    for t in lines:
        if t.strip() == "":
            out.append("")
        else:
            if prev_empty:
                out.append("")
            out.append(t)
            prev_empty = False
    return "\n".join(out)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output", nargs="?", default=None)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--txt", action="store_true")
    ap.add_argument("--docx", action="store_true")
    a = ap.parse_args()

    src_dir = os.path.abspath(a.input)
    out_dir = os.path.abspath(a.output) if a.output else src_dir
    os.makedirs(out_dir, exist_ok=True)

    jobs = []   # (src_path, out_path, kind)
    for fn in sorted(os.listdir(src_dir)):
        p = os.path.join(src_dir, fn)
        if not os.path.isfile(p): continue
        ext = os.path.splitext(fn)[1].lower()
        if ext in (".md", ".markdown") or (a.txt and ext == ".txt"):
            out = os.path.join(out_dir, clean_stem(p) + ".docx")
            if os.path.abspath(p) == os.path.abspath(out): continue
            jobs.append((p, out, "md"))
        elif a.docx and ext == ".docx":
            out = os.path.join(out_dir, clean_stem(p) + " - formatted.docx")
            if os.path.abspath(p) == os.path.abspath(out): continue
            jobs.append((p, out, "docx"))

    ok, skipped, errors = [], [], []
    t0 = time.time()
    for idx, (p, out, kind) in enumerate(jobs, 1):
        name = os.path.basename(out)
        if os.path.exists(out) and not a.force:
            skipped.append(name); print(f"[{idx}/{len(jobs)}] SKIP (exists) {name}")
            continue
        try:
            if kind == "docx":
                import tempfile
                flat = flatten_docx(p)
                tmp = os.path.join(out_dir, "._flat_tmp.md")
                open(tmp, "w", encoding="utf-8").write(flat)
                try:
                    convert_md(tmp, out)
                finally:
                    os.remove(tmp)
            else:
                convert_md(p, out)
            ok.append(name)
            print(f"[{idx}/{len(jobs)}] OK  {name}")
        except Exception as e:
            errors.append((name, repr(e)))
            print(f"[{idx}/{len(jobs)}] ERR {name}  {e!r}")
            traceback.print_exc()
    dt = time.time() - t0
    print(f"\nDone in {dt:.1f}s — {len(ok)} converted, {len(skipped)} skipped, {len(errors)} errors.")
    if errors:
        print("Errors:")
        for n, r in errors: print(f"  {n}: {r}")

if __name__ == "__main__":
    main()
