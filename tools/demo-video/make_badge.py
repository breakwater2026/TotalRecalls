#!/usr/bin/env python3
"""Render the "1.5x speed" badge chip (223x64 PNG) for demo overlays.

Usage: make_badge.py [text] [out.png]
Defaults: "1.5x" (bold) + "speed" (regular), 223x64, at 34px Segoe UI.
"""
import sys
from PIL import Image, ImageDraw, ImageFont

BOLD = r"C:\Windows\Fonts\segoeuib.ttf"
REG = r"C:\Windows\Fonts\segoeui.ttf"


def make(t1: str = "1.5x", t2: str = " speed", size: int = 34,
         out: str = "badge_1.5x_speed.png") -> tuple[int, int]:
    f_bold = ImageFont.truetype(BOLD, size)
    f_reg = ImageFont.truetype(REG, size)
    w1 = f_bold.getlength(t1)
    w2 = f_reg.getlength(t2)
    pad_x, pad_y, radius = 28, 15, 20
    W = int(w1 + w2 + pad_x * 2)
    H = size + pad_y * 2
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([2, 2, W - 3, H - 3], radius=radius,
                        fill=(8, 12, 20, 225), outline=(47, 123, 255, 255), width=2)
    d.text((pad_x, pad_y - 2), t1, font=f_bold, fill=(248, 250, 252, 255))
    d.text((pad_x + w1, pad_y - 2), t2, font=f_reg, fill=(160, 170, 185, 255))
    im.save(out)
    return W, H


if __name__ == "__main__":
    out = sys.argv[2] if len(sys.argv) > 2 else "badge_1.5x_speed.png"
    w, h = make(sys.argv[1] if len(sys.argv) > 1 else "1.5x", out=out)
    print(f"badge {w}x{h} -> {out}")
