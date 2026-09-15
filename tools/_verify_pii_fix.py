"""Verify the rebuilt EXE's PYZ actually contains the PII-fix placeholder
strings in the three touched modules, plus the correct edition constant.

Per the build recipe: CArchiveReader(exe) -> extract('PYZ.pyz') -> write to
temp -> ZlibArchiveReader(path). Module names DOT-separated. Check co_consts
(literals) of the target modules.
"""
import os, sys, tempfile

EXE = sys.argv[1]
EXPECTED_EDITION = sys.argv[2] if len(sys.argv) > 2 else "pro"  # "pro" or "free"

from PyInstaller.archive.readers import CArchiveReader, ZlibArchiveReader

ca = CArchiveReader(EXE)
pyz_bytes = ca.extract("PYZ.pyz")
tmp = os.path.join(tempfile.gettempdir(), "tr_verify_pyz_%d.pyz" % os.getpid())
with open(tmp, "wb") as f:
    f.write(pyz_bytes)
zr = ZlibArchiveReader(tmp)

def module_consts(name):
    """Return the top-level co_consts string set of a module (incl. nested code objects)."""
    try:
        code = zr.extract(name)
    except Exception as e:
        return None
    consts = []
    stack = [code]
    while stack:
        c = stack.pop()
        for o in c.co_consts:
            if isinstance(o, str):
                consts.append(o)
            elif hasattr(o, "co_consts"):
                stack.append(o)
    return set(consts)

checks = {
    "totalrecalls.adapters.perplexity.adapter": ["perplexity-session@local"],
    "totalrecalls.adapters.chatgpt.auth": ["chatgpt-session@local"],
    "totalrecalls.adapters.claude.auth": ["claude-session@local"],
    "totalrecalls.edition": [EXPECTED_EDITION],
}

ok = True
for mod, needles in checks.items():
    cs = module_consts(mod)
    if cs is None:
        print(f"  MISSING MODULE: {mod}")
        ok = False
        continue
    if not cs:
        print(f"  EMPTY CONSTS (collector bug): {mod}")
        ok = False
        continue
    for n in needles:
        present = n in cs
        print(f"  {mod}: {'OK ' if present else 'FAIL'} '{n}'")
        if not present:
            ok = False

# edition: top-level const must contain the expected edition and NOT the other
ed = module_consts("totalrecalls.edition")
if ed:
    other = "free" if EXPECTED_EDITION == "pro" else "pro"
    print(f"  edition top-consts check: '{EXPECTED_EDITION}' in {EXPECTED_EDITION!r}={EXPECTED_EDITION in ed}, other '{other}' present={other in ed}")
    if EXPECTED_EDITION not in ed:
        ok = False

os.unlink(tmp)
print("VERIFY:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
