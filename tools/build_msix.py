#!/usr/bin/env python3
"""Pack and sign the Microsoft Store MSIX from the onedir build.

Usage:
    python tools/build_exe.py --edition free --mode onedir
    python tools/build_msix.py

    # unsigned package (inspect only; the Store submission must be signed)
    python tools/build_msix.py --no-sign

What it does:
  1. reads Identity (Publisher, Version) from msix/Package.appxmanifest
  2. stages dist/TotalRecalls/ + the manifest + Assets in a temp directory
  3. runs makeappx.exe pack
  4. signs with the code-signing certificate whose subject matches Publisher
  5. verifies the signature

Tool discovery: makeappx/signtool are taken from $MSIX_SDK_BIN, PATH, a Windows
Kits install, or the NuGet package cache (Microsoft.Windows.SDK.BuildTools).
The NuGet package can be fetched without Visual Studio:

    curl -L -o bt.nupkg https://api.nuget.org/v3-flatcontainer/\\
microsoft.windows.sdk.buildtools/10.0.28000.2957/\\
microsoft.windows.sdk.buildtools.10.0.28000.2957.nupkg
    unzip bt.nupkg -d "%LOCALAPPDATA%\\Microsoft\\Windows Kits\\BuildTools"
"""
from __future__ import annotations

import argparse
import glob
import os
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MANIFEST = REPO / "msix" / "Package.appxmanifest"
ASSETS = REPO / "msix" / "Assets"
ONEDIR = REPO / "dist" / "TotalRecalls"
NS = {"f": "http://schemas.microsoft.com/appx/manifest/foundation/windows10"}
SDK_NAMES = ("makeappx.exe", "signtool.exe")


def identity() -> tuple[str, str]:
    root = ET.parse(MANIFEST).getroot()
    node = root.find("f:Identity", NS)
    if node is None:
        raise SystemExit(f"ERROR: Identity element missing from {MANIFEST}")
    publisher = node.get("Publisher") or ""
    version = node.get("Version") or "1.0.0.0"
    if not publisher:
        raise SystemExit("ERROR: Identity/@Publisher is empty")
    return publisher, version


def find_tool(name: str) -> str:
    candidates: list[str] = []
    env = os.environ.get("MSIX_SDK_BIN")
    if env:
        candidates.append(os.path.join(env, name))
    found = shutil.which(name)
    if found:
        candidates.append(found)
    patterns = [
        r"C:/Program Files (x86)/Windows Kits/10/bin/*/x64/" + name,
        os.path.join(os.environ.get("USERPROFILE", ""), ".nuget", "packages",
                     "microsoft.windows.sdk.buildtools", "*", "bin", "*", "x64", name),
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "Windows Kits",
                     "BuildTools", "bin", "*", "x64", name),
    ]
    for pattern in patterns:
        candidates.extend(sorted(glob.glob(pattern), reverse=True))
    for candidate in candidates:
        if candidate and os.path.isfile(candidate):
            return candidate
    raise SystemExit(
        f"ERROR: {name} not found. Set MSIX_SDK_BIN to the SDK BuildTools x64 folder "
        "(see the module docstring for the NuGet download)."
    )


def cert_thumbprint(publisher: str) -> str | None:
    ps = (
        "$c = Get-ChildItem Cert:\\CurrentUser\\My | Where-Object { "
        f"$_.Subject -eq '{publisher}' -and $_.HasPrivateKey }} | "
        "Sort-Object NotAfter -Descending | Select-Object -First 1; "
        "if ($c) { $c.Thumbprint }"
    )
    result = subprocess.run(["powershell", "-NoProfile", "-Command", ps],
                            capture_output=True, text=True, timeout=60)
    thumb = (result.stdout or "").strip()
    return thumb or None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--arch", default="x64", help="architecture label (default: x64)")
    ap.add_argument("--out", default=None,
                    help="output .msix (default: dist/TotalRecalls-<version>-<arch>.msix)")
    ap.add_argument("--no-sign", action="store_true", help="skip signing")
    ap.add_argument("--keep-staging", action="store_true")
    args = ap.parse_args()

    if not (ONEDIR / "TotalRecalls.exe").is_file():
        raise SystemExit("ERROR: dist/TotalRecalls/TotalRecalls.exe missing — run "
                         "`python tools/build_exe.py --edition free --mode onedir` first.")

    publisher, version = identity()
    out = Path(args.out) if args.out else REPO / "dist" / f"TotalRecalls-{version}-{args.arch}.msix"

    staging = Path(tempfile.mkdtemp(prefix="tr-msix-"))
    try:
        shutil.copytree(ONEDIR, staging, dirs_exist_ok=True)
        shutil.copy2(MANIFEST, staging / "AppxManifest.xml")
        shutil.copytree(ASSETS, staging / "Assets", dirs_exist_ok=True)

        makeappx = find_tool("makeappx.exe")
        pack = subprocess.run([makeappx, "pack", "/d", str(staging), "/p", str(out), "/o"],
                              capture_output=True, text=True)
        if pack.returncode != 0:
            print(pack.stdout, pack.stderr, sep="\n")
            raise SystemExit(f"ERROR: makeappx failed ({pack.returncode})")
        print(f"[msix] packed {out} ({out.stat().st_size:,} bytes)  v{version}  {publisher}")

        if args.no_sign:
            print("[msix] unsigned (--no-sign)")
            return 0

        thumb = cert_thumbprint(publisher)
        if not thumb:
            raise SystemExit(
                "ERROR: no code-signing certificate in Cert:\\CurrentUser\\My with "
                f"subject {publisher!r}. Create one for local testing or pass --no-sign."
            )
        signtool = find_tool("signtool.exe")
        sign = subprocess.run([signtool, "sign", "/fd", "SHA256", "/sha1", thumb,
                               "/a", str(out)], capture_output=True, text=True)
        if sign.returncode != 0:
            print(sign.stdout, sign.stderr, sep="\n")
            raise SystemExit(f"ERROR: signtool sign failed ({sign.returncode})")
        verify = subprocess.run([signtool, "verify", "/pa", str(out)],
                                capture_output=True, text=True)
        if verify.returncode != 0:
            print(verify.stdout, verify.stderr, sep="\n")
            raise SystemExit("ERROR: signature verification failed")
        print(f"[msix] signed with {thumb} and verified")
        return 0
    finally:
        if args.keep_staging:
            print(f"[msix] staging kept: {staging}")
        else:
            shutil.rmtree(staging, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
