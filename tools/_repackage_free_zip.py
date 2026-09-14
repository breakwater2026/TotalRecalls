"""Repackage the free-tier ZIP with the new dist/TotalRecalls.exe (level-9 deflate),
then report SHA-256 + size MB for the /download page update."""
import zipfile, hashlib, os

SITE = r"C:\Users\break\Projects\TotalRecalls\site"
exesrc = r"C:\Users\break\Projects\TotalRecalls\dist\TotalRecalls.exe"
readme = os.path.join(SITE, "public", "downloads", "README.txt")
outzip = os.path.join(SITE, "public", "downloads", "TotalRecalls-1.0.0-free-tier.zip")

assert os.path.isfile(exesrc), exesrc
assert os.path.isfile(readme), readme

# keep a backup of the old ZIP (working tree; user can discard)
backup = outzip + ".bak-2026-09-08"
if not os.path.exists(backup):
    os.replace(outzip, backup)
    print("old ZIP backed up ->", os.path.basename(backup))

with zipfile.ZipFile(outzip, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    z.write(exesrc, "TotalRecalls.exe")
    z.write(readme, "README.txt")

data = open(outzip, "rb").read()
sha = hashlib.sha256(data).hexdigest()
size_mb = len(data) / (1024 * 1024)
print(f"NEW ZIP: {outzip}")
print(f"SHA-256: {sha}")
print(f"SIZE: {len(data)} bytes = {size_mb:.1f} MB")
with zipfile.ZipFile(outzip) as z:
    for n in z.namelist():
        print("  entry:", n, z.getinfo(n).file_size, "bytes")
