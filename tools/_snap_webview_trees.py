"""Live snapshot: which webview trees exist, who hosts them, are their parents alive."""
import subprocess, ctypes, re, sys

out2 = subprocess.run(
    ["wmic", "process", "where", "name='msedgewebview2.exe'", "/format:list"],
    capture_output=True, text=True).stdout
blocks = re.split(r"\r?\n\r?\n", out2.strip())
procs = []
for b in blocks:
    if not b.strip():
        continue
    d = {}
    for l in b.splitlines():
        if "=" in l:
            k, v = l.split("=", 1)
            d[k.strip()] = v.strip()
    if "ProcessId" in d:
        procs.append(d)

def alive(pid):
    if not pid or pid == "0":
        return None
    h = ctypes.windll.kernel32.OpenProcess(0x1000, False, int(pid))
    if h:
        ctypes.windll.kernel32.CloseHandle(h)
        return True
    return False

# also grab all python.exe + TotalRecalls procs for cross-ref
out3 = subprocess.run(
    ["wmic", "process", "where", "name='python.exe' or name='TotalRecalls.exe' or name='TotalRecalls-Pro.exe'",
     "/format:list"], capture_output=True, text=True).stdout
hosts = []
for b in re.split(r"\r?\n\r?\n", out3.strip()):
    if not b.strip():
        continue
    d = {}
    for l in b.splitlines():
        if "=" in l:
            k, v = l.split("=", 1)
            d[k.strip()] = v.strip()
    if "ProcessId" in d:
        hosts.append(d)
print("=== LIVE python.exe / TotalRecalls hosts ===")
for h in hosts:
    cl = h.get("CommandLine", "")[:90]
    print(f"  pid={h.get('ProcessId'):<7} name={h.get('Name','?'):<22} cl={cl}")
print(f"\n=== WebView2 trees (total procs: {len(procs)}) ===")
trees = {}
for p in procs:
    cl = p.get("CommandLine", "")
    m = re.search(r"--user-data-dir=\"?([^\s\"]+)", cl)
    profile = m.group(1) if m else "?"
    role = re.search(r"--type=([a-z.]+)", cl)
    host = re.search(r"--webview-exe-name=([^\s]+)", cl)
    pid = p.get("ProcessId"); pp = p.get("ParentProcessId", "")
    key = profile
    trees.setdefault(key, []).append((pid, pp, role.group(1) if role else "BROWSER-HOST",
                                       host.group(1) if host else "?"))
for profile, members in trees.items():
    browser = [m for m in members if m[2] == "BROWSER-HOST"]
    hostexe = browser[0][3] if browser else "?"
    parent = browser[0][1] if browser else "?"
    print(f"\n  PROFILE: {profile}")
    print(f"    browser-host pid={browser[0][0] if browser else '?'} "
          f"parent={parent} parent_alive={alive(parent)} host_exe={hostexe}")
    if not browser:
        print("    (no browser-host process — fully orphaned children)")
