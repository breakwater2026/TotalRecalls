"""Jump-cut trims for a demo take (frame-accurate, re-encoded).

Usage:
    python cut_takes.py input.mkv output.mp4 cuts.json

cuts.json format (seconds):
    [
      {"keep": [0.0, 12.5]},
      {"keep": [180.0, 195.2]}
    ]
Keeps are concatenated in the order given.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 4:
        print(__doc__)
        return 2
    src, dst, cuts_path = sys.argv[1], sys.argv[2], sys.argv[3]
    cuts = json.loads(Path(cuts_path).read_text(encoding="utf-8"))
    keeps = [c["keep"] for c in cuts]
    if not keeps:
        print("no keep segments")
        return 2

    # Probe source duration for sanity warnings
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", src],
        capture_output=True, text=True)
    try:
        total = float(probe.stdout.strip())
    except ValueError:
        total = None
    if total:
        covered = sum(b - a for a, b in keeps)
        print(f"source {total:.1f}s -> keeping {covered:.1f}s across {len(keeps)} segment(s)")
        for a, b in keeps:
            if b > total:
                print(f"WARN: segment end {b} beyond source duration {total:.1f}")

    with tempfile.TemporaryDirectory() as td:
        parts = []
        for i, (a, b) in enumerate(keeps):
            part = Path(td) / f"part{i:02d}.mp4"
            cmd = [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                "-ss", f"{a:.3f}", "-to", f"{b:.3f}", "-i", src,
                "-c:v", "libx264", "-crf", "18", "-preset", "medium",
                "-pix_fmt", "yuv420p", "-an",          # silent deliverable: drop audio now
                "-video_track_timescale", "90000",     # common timescale = clean concat
                str(part),
            ]
            subprocess.run(cmd, check=True)
            parts.append(str(part))
        lst = Path(td) / "list.txt"
        lst.write_text("".join(f"file '{p}'\n" for p in parts), encoding="utf-8")
        subprocess.run(
            ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
             "-f", "concat", "-safe", "0", "-i", str(lst),
             "-c", "copy", "-movflags", "+faststart", dst],
            check=True)
    print(f"wrote {dst}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
