"""Release gate — one command, every assertion that has bitten us.

Run from the repo root. Exits non-zero on any mismatch, printing PASS/FAIL per
check so a failure names itself.

Checks:
  1. dist/TotalRecalls.exe exists and the PYZ verifier passes (edition, strings)
  2. the free-tier ZIP matches the EXE it was built from, and its SHA-256 matches
     the constant on /download
  3. every shipped render is High / yuv420p / 30 fps / expected duration / faststart
  4. the R2 objects serve the exact byte counts we expect
"""
from __future__ import annotations

import hashlib
import io
import os
import subprocess
import sys
import urllib.request
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD_VENV = os.path.join(os.environ.get("LOCALAPPDATA", ""), "tr-build-venv", "Scripts", "python.exe")
SHOOT = r"C:\Users\break\demo-shoot\renders"
ZIP = os.path.join(ROOT, "site", "public", "downloads", "TotalRecalls-1.0.0-free-tier.zip")
PAGE = os.path.join(ROOT, "site", "src", "pages", "download", "index.astro")

# provider -> (local render, R2 key, expected duration s, expected bytes)
RENDERS = {
    "chatgpt":    (r"chatgpt_v12\totalrecalls_demo_chatgpt_v12.mp4", "TR_website_chatgpt.mp4",    277.333333, 49548676),
    "claude":     (r"claude2_final\totalrecalls_demo_claude_v3.mp4", "TR_website_claude.mp4",     189.300000, 50178508),
    "perplexity": (r"perplexity_p2\totalrecalls_demo_perplexity.mp4", "TR_website_perplexity.mp4", 185.033333, 46433339),
    "deepseek":   (r"deepseek_p2\totalrecalls_demo_deepseek.mp4",   "TR_website_deepseek.mp4",   160.000000, 29206402),
    "gemini":     (r"gemini_v3\totalrecalls_demo_gemini.mp4",       "TR_website_gemini.mp4",     178.600000, 30689395),
    "mistral":    (r"mistral_v2\totalrecalls_demo_mistral.mp4",     "TR_website_mistral.mp4",    178.600000, 29045623),
    "grok":       (r"grok_v1\totalrecalls_demo_grok.mp4",           "TR_website_grok.mp4",       234.033333, 36681712),
    "qwen":       (r"qwen_v1\totalrecalls_demo_qwen.mp4",           "TR_website_qwen.mp4",       239.200000, 36166587),
}

fails: list[str] = []


def ok(name: str, cond: bool, detail: str = "") -> None:
    print(f"{'PASS' if cond else 'FAIL'}  {name}" + (f"  [{detail}]" if detail else ""))
    if not cond:
        fails.append(name)

def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def ffprobe(path: str) -> dict:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "format=duration,size:stream=pix_fmt,profile,width,height,r_frame_rate",
         "-of", "default=nw=1", path],
        capture_output=True, text=True,
    ).stdout
    d = {}
    for line in out.splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            d[k.strip()] = v.strip()
    return d


def main() -> int:
    exe = os.path.join(ROOT, "dist", "TotalRecalls.exe")
    ok("exe exists", os.path.isfile(exe), f"{os.path.getsize(exe) if os.path.isfile(exe) else 0} B")

    verifier = os.path.join(ROOT, "tools", "_verify_paddle_build.py")
    if os.path.isfile(verifier) and os.path.isfile(BUILD_VENV):
        r = subprocess.run([BUILD_VENV, verifier], capture_output=True, text=True)
        ok("PYZ verifier", r.returncode == 0, (r.stdout.strip().splitlines() or [""])[-1][:90])

    if os.path.isfile(ZIP):
        with zipfile.ZipFile(ZIP) as z:
            names = sorted(z.namelist())
            exe_size = z.getinfo("TotalRecalls.exe").file_size
        ok("zip entries", names == ["README.txt", "TotalRecalls.exe"], str(names))
        ok("zip exe == dist exe", exe_size == os.path.getsize(exe), f"{exe_size}")
        digest = sha256(ZIP)
        page = io.open(PAGE, encoding="utf-8", errors="replace").read()
        ok("page SHA == zip SHA", digest in page, digest[:16])

    for prov, (rel, key, want_dur, want_bytes) in RENDERS.items():
        path = os.path.join(SHOOT, rel)
        if not os.path.isfile(path):
            ok(f"{prov}: render present", False, path)
            continue
        info = ffprobe(path)
        ok(f"{prov}: yuv420p/High", info.get("pix_fmt") == "yuv420p" and info.get("profile") == "High",
           f"{info.get('pix_fmt')}/{info.get('profile')}")
        ok(f"{prov}: 30 fps 3440x1440", info.get("r_frame_rate") == "30/1" and info.get("width") == "3440",
           f"{info.get('r_frame_rate')} {info.get('width')}x{info.get('height')}")
        ok(f"{prov}: duration", abs(float(info.get("duration", 0)) - want_dur) < 0.1,
           f"{info.get('duration')} vs {want_dur}")
        head = open(path, "rb").read(4096)
        ok(f"{prov}: faststart", head.find(b"moov") >= 0 and (head.find(b"mdat") < 0 or head.find(b"moov") < head.find(b"mdat")))
        try:
            req = urllib.request.Request(
                f"https://video.totalrecalls.app/{key}", method="HEAD",
                headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                served = int(resp.headers.get("Content-Length", "0"))
            ok(f"{prov}: R2 bytes", served == want_bytes, f"{served} vs {want_bytes}")
        except Exception as e:
            ok(f"{prov}: R2 reachable", False, f"{type(e).__name__}")

    print()
    print("GATE PASSED" if not fails else f"GATE FAILED ({len(fails)}): " + ", ".join(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
