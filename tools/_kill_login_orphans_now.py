"""Kill ONLY msedgewebview2.exe whose command line references our
login-webview-* profile folders (never the main window's webview/EBWebView,
never other apps' webviews). Then test the profile lock."""
import subprocess, os, time

D = r"C:\Users\break\AppData\Roaming\PerplexityExporter"

out = subprocess.run(
    ["wmic", "process", "where", "name='msedgewebview2.exe'",
     "get", "ProcessId,ParentProcessId,CommandLine"],
    capture_output=True, text=True).stdout

# wmic table: header line, dash line, then "PID,PARENT,CMDLINE" per row (cmdline has no commas
# in our case except inside quoted paths? no — paths use backslashes, fine)
rows = []
for line in out.splitlines()[2:]:
    line = line.strip()
    if not line:
        continue
    parts = line.split(",", 2)
    if len(parts) < 3 or not parts[0].isdigit():
        continue
    rows.append((parts[0], parts[1], parts[2]))

killed, spared = [], 0
for pid, pp, cl in rows:
    if "login-webview-" in cl and "perplexityexporter" in cl.lower():
        r = subprocess.run(["taskkill", "/PID", pid, "/F"],
                           capture_output=True, text=True)
        print(f"KILL pid={pid} parent={pp}: {r.stdout.strip() or r.stderr.strip()}")
        killed.append(pid)
    else:
        spared += 1

print(f"\nkilled={len(killed)} ({killed})  spared={spared} other webview procs")
time.sleep(3)

# verify lock cleared
ok = os.rename(os.path.join(D, "login-webview-chatgpt"),
               os.path.join(D, "login-webview-chatgpt-T"))
if ok:
    os.rename(os.path.join(D, "login-webview-chatgpt-T"),
              os.path.join(D, "login-webview-chatgpt"))
print("profile lock:", "UNLOCKED ✓" if ok else "STILL LOCKED ✗")

# also check for any login-webview-* folders with leftover locks (per-provider)
for name in os.listdir(D):
    if name.startswith("login-webview-"):
        p = os.path.join(D, name)
        ok = os.rename(p, p + "-T")
        if ok:
            os.rename(p + "-T", p)
        print(f"  {name}: {'unlocked' if ok else 'LOCKED'}")
