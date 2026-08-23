"""Burn a lower-third title card onto a clip (TotalRecalls brand style).

Usage:
    python card.py input.mp4 output.mp4 "1/5 — Perplexity · exports to Library/perplexity" [start] [dur]

Card: electric-blue #2F7BFF band, white Segoe UI Semibold text, fades in/out.
Defaults: start=0.8s after clip start, duration=4s. Output is silent H.264.

Implementation notes (verified 2026-08-23):
- This ffmpeg build rejects absolute Windows font paths in drawtext (colon
  escaping ambiguity) and has no working fontconfig — so we copy the TTF into
  a temp dir and run ffmpeg with THAT as its cwd, letting the relative
  fontfile=seguisb.ttf resolve.
- drawbox runs FIRST, drawtext second, so the text renders on top of the band.
- Text is centered inside the 96px band: y = ih-96 + (96-text_h)/2.
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

FONT_SRC = Path(r"C:\Windows\Fonts\seguisb.ttf")
FONT_NAME = "seguisb.ttf"
BAND = "0x2F7BFF@0.92"
BAND_H = 96


def esc(text: str) -> str:
    # drawtext text= value: escape apostrophes and backslashes.
    return text.replace("\\", "\\\\").replace("'", "\\'")


def main() -> int:
    if len(sys.argv) not in (5, 6):
        print(__doc__)
        return 2
    src, dst, text = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
    start = float(sys.argv[4]) if len(sys.argv) == 6 else 0.8
    dur = float(sys.argv[5]) if len(sys.argv) == 6 else 4.0
    end = start + dur
    fade = 0.4

    alpha = (
        f"if(lt(t,{start + fade:.2f}),(t-{start:.2f})/{fade},"
        f"if(lt(t,{end - fade:.2f}),1,"
        f"if(lt(t,{end:.2f}),({end:.2f}-t)/{fade},0)))"
    )
    vf = (
        f"drawbox=x=0:y=ih-{BAND_H}:w=iw:h={BAND_H}:color={BAND}:t=fill:"
        f"enable='between(t,{start:.2f},{end:.2f})',"
        f"drawtext=fontfile={FONT_NAME}:text='{esc(text)}':"
        f"fontsize=40:fontcolor=white:"
        # drawtext in this ffmpeg build segfaults on the `ih` constant
        # (verified 2026-08-23) — use `h`, which equals ih here.
        f"x=(w-text_w)/2:y=h-{BAND_H}+({BAND_H}-th)/2:"
        f"alpha='{alpha}'"
    )
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        shutil.copy2(FONT_SRC, td_path / FONT_NAME)
        cmd = [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(src.resolve()),
            "-vf", vf,
            "-c:v", "libx264", "-crf", "18", "-preset", "medium",
            "-pix_fmt", "yuv420p", "-an",
            "-movflags", "+faststart",
            str(dst.resolve()),
        ]
        proc = subprocess.run(cmd, cwd=str(td_path))
        if proc.returncode != 0:
            print(f"ffmpeg failed rc={proc.returncode}")
            return 1
    print(f"wrote {dst}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
