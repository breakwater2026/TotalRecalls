"""End-to-end test of _kill_orphan_webviews.

Launch two fake msedgewebview2.exe processes (renamed wscript.exe idling in a
VBS loop): one whose command line references OUR profile folder, one
referencing a foreign one. Run the sweep; assert ONLY the ours was killed.
Proves the sweep targets our profile and leaves other apps alone.
"""
import os, subprocess, sys, time, shutil

TMP = r"C:\Users\break\AppData\Local\Temp\tr_sweep_test"
os.makedirs(TMP, exist_ok=True)
FAKE = os.path.join(TMP, "msedgewebview2.exe")
shutil.copy(r"C:\Windows\System32\wscript.exe", FAKE)
VBS = os.path.join(TMP, "_idle.vbs")
open(VBS, "w").write("do while true\n  wscript.sleep 600000\ndowhile false\n")

def alive(pid):
    r = subprocess.run(["tasklist", "/FI", f"PID eq {pid}"], capture_output=True, text=True)
    return str(pid) in r.stdout

OUR = r"C:\Users\break\AppData\Roaming\PerplexityExporter"
procs = []
# wscript: first arg = script; extra args land in the command line (ignored by
# wscript) — which is exactly what the sweep reads from wmic.
procs.append(subprocess.Popen(
    [FAKE, VBS, "--user-data-dir", os.path.join(OUR, "login-webview-chatgpt"), "--type=renderer"],
    creationflags=0x08000000))
procs.append(subprocess.Popen(
    [FAKE, VBS, "--user-data-dir", r"C:\Users\break\AppData\Local\OtherApp\webview", "--type=renderer"],
    creationflags=0x08000000))
time.sleep(4)
orphan_pid, foreign_pid = procs[0].pid, procs[1].pid
print("fake orphan pid:", orphan_pid, " foreign pid:", foreign_pid)
print("  alive pre-sweep  -> orphan:", alive(orphan_pid), " foreign:", alive(foreign_pid))

sys.path.insert(0, r"C:\Users\break\Projects\TotalRecalls")
from totalrecalls.desktop.bridge import _kill_orphan_webviews
_kill_orphan_webviews()
time.sleep(1.5)

o, f = alive(orphan_pid), alive(foreign_pid)
print("  alive post-sweep -> orphan:", o, " foreign:", f)
print("RESULT:", "PASS" if (not o and f) else "FAIL")
for p in procs:
    try:
        p.kill()
    except Exception:
        pass
