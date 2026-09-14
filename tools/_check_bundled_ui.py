import difflib
import inspect
from PyInstaller.archive import readers

r = readers.CArchiveReader(r"C:\Users\break\Projects\TotalRecalls\dist\TotalRecalls-Pro.exe")
print([m for m in dir(r) if not m.startswith("__")])
names = [n for n in r.toc if "app_ui" in n.lower()]
print("entries:", names)
data = None
for n in names:
    try:
        data = r.extract(n)
        if isinstance(data, tuple):
            data = data[0]
        print("extracted", n, type(data), len(data))
        break
    except Exception as e:
        print("extract failed:", e)
if data:
    lines = data.decode("utf-8", "replace").splitlines()
    joined = "\n".join(lines)
    print("bundled app_ui.html lines:", len(lines))
    print("has tier-badge:", "tier-badge" in joined)
    print("has selection-card:", "selection-card" in joined)
    print("has 'Download my conversations':", "Download my conversations" in joined)
    print("has 'Export my conversations':", "Export my conversations" in joined)
    open(r"C:\Users\break\AppData\Local\Temp\bundled_pro_app_ui.html", "w", encoding="utf-8").write(joined)
    repo = open(r"C:\Users\break\Projects\TotalRecalls\app_ui.html", encoding="utf-8").read().splitlines()
    d = list(difflib.unified_diff(repo, lines, "repo", "bundled", lineterm=""))
    print("diff lines:", len(d))
    for l in d[:50]:
        print(l[:200])
else:
    print("NOT FOUND")
