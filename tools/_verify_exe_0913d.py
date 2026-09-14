"""Verify today's (2026-09-13) fixes are INSIDE the built EXEs via PYZ.

Checks:
  1. edition consts
  2. bridge.openBuyPage -> lemonsqueezy.com URL (NOT totalrecalls.app/buy)
  3. export_fs -> provider-aware readme + tool=TotalRecalls (no 'Perplexity Exporter')
  4. chatgpt conversations -> NO 'order=created' (deep pass removed)
  5. chatgpt adapter -> count_conversations limit=100 (int const present)
"""
import os, sys, tempfile
sys.path.insert(0, os.path.expandvars(r"%LOCALAPPDATA%\tr-build-venv\Scripts"))
from PyInstaller.archive.readers import CArchiveReader, ZlibArchiveReader

def consts_of(code):
    out = set()
    stack = [code]
    while stack:
        c = stack.pop()
        for k in c.co_consts:
            if isinstance(k, str):
                out.add(k)
            elif isinstance(k, (int, float)) and not isinstance(k, bool):
                out.add(k)
            elif hasattr(k, "co_consts"):
                stack.append(k)
    return out

def check(exe, edition_expected, label):
    ca = CArchiveReader(exe)
    pyz = tempfile.NamedTemporaryFile(delete=False, suffix=".pyz")
    pyz.write(ca.extract("PYZ.pyz"))
    pyz.close()
    zr = ZlibArchiveReader(pyz.name)
    results = []

    ed = consts_of(zr.extract("totalrecalls.edition"))
    results.append(("edition consts", ed, {edition_expected} <= ed))

    br = consts_of(zr.extract("totalrecalls.desktop.bridge"))
    buy_ok = "https://totalrecalls.lemonsqueezy.com" in br and "https://totalrecalls.app/buy" not in br
    results.append(("openBuyPage -> LS store, no .app/buy", buy_ok, buy_ok))

    ef = consts_of(zr.extract("totalrecalls.core.export_fs"))
    ef_ok = "Perplexity Exporter" not in ef and "# Your " in ef and "TotalRecalls" in ef
    results.append(("export_fs provider-aware, no Perplexity Exporter", ef_ok, ef_ok))

    cg = consts_of(zr.extract("totalrecalls.adapters.chatgpt.conversations"))
    cg_code = zr.extract("totalrecalls.adapters.chatgpt.conversations")
    cg_names = set()
    stack = [cg_code]
    while stack:
        c = stack.pop()
        cg_names |= set(c.co_names)
        for k in c.co_consts:
            if hasattr(k, "co_consts"):
                stack.append(k)
    cg_ok = "created" not in cg_names and "order=created" not in cg
    results.append(("chatgpt conversations: no order='created' call site", cg_ok, cg_ok))

    ca2 = consts_of(zr.extract("totalrecalls.adapters.chatgpt.adapter"))
    ca_ok = 100 in ca2
    results.append(("chatgpt adapter: limit=100 const present", ca_ok, ca_ok))

    print(f"\n=== {label} ({os.path.basename(exe)}) ===")
    all_ok = True
    for name, _val, ok in results:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
        all_ok = all_ok and ok
    return all_ok

ok1 = check(r"C:\Users\break\Projects\TotalRecalls\dist\TotalRecalls.exe", "free", "FREE build")
ok2 = check(r"C:\Users\break\Projects\TotalRecalls\dist\TotalRecalls-Pro.exe", "pro", "PRO build")
print(f"\nOVERALL: {'ALL PASS' if ok1 and ok2 else 'FAILURES PRESENT'}")
sys.exit(0 if ok1 and ok2 else 1)
