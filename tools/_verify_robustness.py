"""Verify rebuilt EXE PYZ contains the Perplexity-robustness code + PII
placeholders + correct edition constant.

Usage: python _verify_robustness.py <exe> <pro|free>

Per the build recipe: CArchiveReader(exe) -> extract('PYZ.pyz') -> temp file
-> ZlibArchiveReader(path). Module names DOT-separated. Checks co_consts
(string literals) of the target modules — a literal present in the frozen
module means the code path is in the binary.
"""
import os, sys, tempfile

EXE = sys.argv[1]
EXPECTED_EDITION = sys.argv[2] if len(sys.argv) > 2 else "pro"

from PyInstaller.archive.readers import CArchiveReader, ZlibArchiveReader

ca = CArchiveReader(EXE)
pyz_bytes = ca.extract("PYZ.pyz")
tmp = os.path.join(tempfile.gettempdir(), "tr_verify_rob_%d.pyz" % os.getpid())
with open(tmp, "wb") as f:
    f.write(pyz_bytes)
zr = ZlibArchiveReader(tmp)

def module_consts(name):
    try:
        code = zr.extract(name)
    except Exception:
        return None
    consts = []
    stack = [code]
    while stack:
        c = stack.pop()
        if isinstance(c, str):
            consts.append(c)
            continue
        elif not hasattr(c, "co_code"):
            continue  # None/int/float/bool consts — nothing to collect
        for o in c.co_consts:
            if isinstance(o, str):
                consts.append(o)
            elif isinstance(o, (tuple, list)):
                stack.extend(o)  # tuple members (e.g. ("cf_clearance", "__cf_bm"))
            elif hasattr(o, "co_code"):
                stack.append(o)
        consts.extend(c.co_names)  # method/attr names live here, not co_consts
    return set(consts)

checks = {
    # PII placeholders (09-15 fix)
    "totalrecalls.adapters.perplexity.adapter": ["perplexity-session@local"],
    "totalrecalls.adapters.chatgpt.auth": ["chatgpt-session@local"],
    "totalrecalls.adapters.claude.auth": ["claude-session@local"],
    # Perplexity robustness (09-15 follow-up)
    "totalrecalls.adapters.perplexity.auth": ["save_cf_cookies_from_header", "__cf_bm"],
    "totalrecalls.adapters.perplexity.http": ["cancelled", "set_retry_sink"],
    "totalrecalls.adapters.perplexity.discover": ["cancelled"],
    "totalrecalls.adapters.perplexity.adapter": ["count_conversations"],
    "totalrecalls.desktop.bridge": ["save_cf_cookies_from_header"],
    "totalrecalls.edition": [EXPECTED_EDITION],
}

ok = True
for mod, needles in checks.items():
    cs = module_consts(mod)
    if cs is None:
        print(f"  MISSING MODULE: {mod}")
        ok = False
        continue
    for n in needles:
        present = n in cs
        print(f"  {mod}: {'OK ' if present else 'FAIL'} '{n}'")
        if not present:
            ok = False

ed = module_consts("totalrecalls.edition")
if ed:
    other = "free" if EXPECTED_EDITION == "pro" else "pro"
    # Exact-constant check: the literal line `EDITION = "<other>"` must be
    # absent (the module's docstring/comment legitimately mentions both words).
    stray = f'EDITION = "{other}"' in ed
    print(f"  edition: '{EXPECTED_EDITION}' present={EXPECTED_EDITION in ed}, stray EDITION={other!r} const={stray}")
    if EXPECTED_EDITION not in ed or stray:
        ok = False

os.unlink(tmp)
print("VERIFY:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
