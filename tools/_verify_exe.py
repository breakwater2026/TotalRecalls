"""Verify the freshly built EXE (v2): edition consts, fix markers via co_names
+ co_consts, and bundled-UI diff."""
import sys, types, tempfile, os
from PyInstaller.archive.readers import CArchiveReader, ZlibArchiveReader

EXE = sys.argv[1]
REPO = r"C:\Users\break\Projects\TotalRecalls"

def walk(co, acc_consts, acc_names):
    for c in co.co_consts:
        if isinstance(c, str):
            acc_consts.append(c)
        elif isinstance(c, types.CodeType):
            walk(c, acc_consts, acc_names)
    acc_names.extend(co.co_names)

def mod(zr, name):
    code = zr.extract(name)
    consts, names = [], []
    walk(code, consts, names)
    return set(consts), set(names)

ca = CArchiveReader(EXE)
pyz = ca.extract("PYZ.pyz")
tmp = os.path.join(tempfile.gettempdir(), "tr_verify_pyz2.pyz")
with open(tmp, "wb") as f:
    f.write(pyz)
zr = ZlibArchiveReader(tmp)

ok = True
def check(label, cond):
    global ok
    print(("PASS" if cond else "FAIL"), label)
    ok = ok and cond

ec, _ = mod(zr, "totalrecalls.edition")
check("edition consts non-trivial", len(ec) > 3)
check("edition = pro ('pro' in consts, 'free' absent)", "pro" in ec and "free" not in ec)

bc, bn = mod(zr, "totalrecalls.desktop.bridge")
check("bridge consts non-trivial", len(bc) > 400)
check("bridge imports call_with_stop (co_names)", "call_with_stop" in bn)
check("bridge imports load_session (co_names)", "load_session" in bn)
check("bridge lazy-imports chatgpt http sink (co_names)",
      "totalrecalls.adapters.chatgpt.http" in bn or "totalrecalls.adapters.chatgpt" in bn)
check("bridge has 'servers are busy' UI msg (consts)",
      any("servers are busy" in c for c in bc))
check("bridge pushes status type (consts)", "status" in bc)

hc, hn = mod(zr, "totalrecalls.adapters.chatgpt.http")
check("http defines set_retry_sink (co_names)", "set_retry_sink" in hn)
check("http defines reset_retry_sink (co_names)", "reset_retry_sink" in hn)
check("http has chatgpt_retry_sink var name (consts)", "chatgpt_retry_sink" in hc)

# bundled UI — repo file read with newline="" (no CRLF translation) so a
# byte-exact comparison is meaningful; the spec bundles app_ui.html verbatim.
ui = ca.extract("app_ui.html").decode("utf-8")
repo_ui = open(os.path.join(REPO, "app_ui.html"), encoding="utf-8", newline="").read()
if ui == repo_ui:
    check("bundled app_ui == repo app_ui", True)
else:
    check("bundled app_ui == repo app_ui", False)
    # find first difference (and whether it's just line endings)
    n = min(len(ui), len(repo_ui))
    print("   len bundled=%d repo=%d; equal up to first diff:" % (len(ui), len(repo_ui)))
    for i in range(n):
        if ui[i] != repo_ui[i]:
            print("   first diff at char %d: bundled=%r repo=%r" % (i, ui[i-20:i+20], repo_ui[i-20:i+20]))
            break
    # line-ending-insensitive comparison
    ui_n = ui.replace("\r\n", "\n"); repo_n = repo_ui.replace("\r\n", "\n")
    print("   equal after normalizing CRLF:", ui_n == repo_n)
check("UI has status handler", "p.type === 'status'" in ui)
check("UI has WIP provider-sync hunk", "updateProviderUI(s.provider)" in ui)

print("\nRESULT:", "ALL CHECKS PASS" if ok else "FAILURES PRESENT")
sys.exit(0 if ok else 1)
