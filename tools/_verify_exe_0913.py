"""Verify the freshly built EXE contains BOTH 2026-09-13 fixes + edition.
Reuses the proven CArchiveReader('PYZ.pyz') + temp-file ZlibArchiveReader pattern."""
import sys, os, types, tempfile
from PyInstaller.archive.readers import CArchiveReader, ZlibArchiveReader

EXE = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\break\Projects\TotalRecalls\dist\TotalRecalls.exe"
print("EXE:", EXE, os.path.getsize(EXE), "bytes")

def walk(co, acc_consts, acc_names, acc_nums):
    for c in co.co_consts:
        if isinstance(c, str):
            acc_consts.append(c)
        elif isinstance(c, (int, float)) and not isinstance(c, bool):
            acc_nums.append(c)
        elif isinstance(c, types.CodeType):
            walk(c, acc_consts, acc_names, acc_nums)
    acc_names.extend(co.co_names)

ca = CArchiveReader(EXE)
pyz = ca.extract("PYZ.pyz")
tmp = os.path.join(tempfile.gettempdir(), "tr_verify_pyz_0913.pyz")
with open(tmp, "wb") as f:
    f.write(pyz)
zr = ZlibArchiveReader(tmp)

def mod(name):
    code = zr.extract(name)
    consts, names, nums = [], [], []
    walk(code, consts, names, nums)
    return set(consts), set(names), set(nums)

ok = True
def check(label, cond):
    global ok
    print(("PASS" if cond else "FAIL"), label)
    ok = ok and cond

ec, _, _ = mod("totalrecalls.edition")
check("EDITION = pro ('pro' in consts, 'free' absent)", "pro" in ec and "free" not in ec)

cc, cn, cnum = mod("totalrecalls.adapters.chatgpt.conversations")
check("F1: order=created deep pass REMOVED (no 'created' const in conversations)",
      "created" not in cc)
check("F1: deep list still has order=updated pass", "updated" in cc)

ac, an, anums = mod("totalrecalls.adapters.chatgpt.adapter")
check("F2: count_conversations paginates real items (100 page-size const present)", 100 in anums)
check("F2: count_conversations 50-page safety cap present", 50 in anums)

# earlier 7 fixes still present
bc, bn, _ = mod("totalrecalls.desktop.bridge")
check("bridge: orphan sweep present (const)", any("orphan" in c for c in bc))
check("bridge: retry UI 'servers are busy' present", any("servers are busy" in c for c in bc))
check("bridge: call_with_stop imported (co_names)", "call_with_stop" in bn)
hc, hn, _ = mod("totalrecalls.adapters.chatgpt.http")
check("http: set_retry_sink present (co_names)", "set_retry_sink" in hn)

print("\nRESULT:", "ALL CHECKS PASS" if ok else "FAILURES PRESENT")
sys.exit(0 if ok else 1)
