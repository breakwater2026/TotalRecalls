#!/usr/bin/env python3
"""Generate the Microsoft Store / MSIX image assets from the brand logo.

Source: Marketing/brand/logo_Final.png — an 821x278 wide lockup containing a square
app icon on the left and the TotalRecalls wordmark on the right.

Outputs into msix/Assets/:
  Square tile assets   - the extracted square app icon, on a matching navy background
  Wide310x150Logo.png  - the wordmark
  StoreLogo.png        - 50x50 square
  SplashScreen620x300  - the full lockup on white

These are functional placeholders built from the existing brand asset. Replace them
with final Store artwork before submission if you want a bespoke treatment.

NOTE: run with a Python that has a working Pillow. The repo venv's Pillow is currently
broken (its _imaging extension will not import); the system Python has Pillow 13.0.0.

    python tools/generate_msix_assets.py
"""
import os

from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGO = os.path.join(REPO, "Marketing", "brand", "logo_Final.png")
OUT = os.path.join(REPO, "msix", "Assets")

# (filename, size) — the standard MSIX tile asset set.
SQUARE_ASSETS = [
    ("Square44x44Logo.png", 44),
    ("Square71x71Logo.png", 71),
    ("Square107x107Logo.png", 107),
    ("Square142x142Logo.png", 142),
    ("Square150x150Logo.png", 150),
    ("Square210x210Logo.png", 210),
    ("Square256x256Logo.png", 256),
    ("Square310x310Logo.png", 310),
    ("StoreLogo.png", 50),
]


def find_icon_bbox(im, scan_limit=320):
    """Bounding box of the dark app-icon square on the left of the lockup."""
    px = im.load()
    _, h = im.size
    xs, ys = [], []
    for x in range(0, min(scan_limit, im.size[0])):
        for y in range(h):
            r, g, b, a = px[x, y]
            if a > 200 and (r + g + b) < 250:
                xs.append(x)
                ys.append(y)
    if not xs:
        raise SystemExit("could not locate the app icon in the logo")
    return (min(xs), min(ys), max(xs) + 1, max(ys) + 1)


def dominant_colour(im) -> tuple:
    colours = im.convert("RGB").getcolors(maxcolors=1_000_000)
    colours.sort(reverse=True)
    r, g, b = colours[0][1]
    return (r, g, b)


def save_square(icon, bg, size, path):
    canvas = Image.new("RGBA", (size, size), bg + (255,))
    pad = max(1, int(size * 0.06))
    inner = size - 2 * pad
    tile = icon.resize((inner, inner), Image.Resampling.LANCZOS)
    canvas.paste(tile, (pad, pad), tile)
    canvas.save(path)


def save_wide(source, size, path, bg=(255, 255, 255)):
    canvas = Image.new("RGBA", size, bg + (255,))
    max_w, max_h = int(size[0] * 0.86), int(size[1] * 0.70)
    src = source
    scale = min(max_w / src.size[0], max_h / src.size[1])
    resized = src.resize((max(1, int(src.size[0] * scale)),
                          max(1, int(src.size[1] * scale))), Image.Resampling.LANCZOS)
    x = (size[0] - resized.size[0]) // 2
    y = (size[1] - resized.size[1]) // 2
    canvas.paste(resized, (x, y), resized)
    canvas.save(path)


def main():
    os.makedirs(OUT, exist_ok=True)
    logo = Image.open(LOGO).convert("RGBA")
    bbox = find_icon_bbox(logo)
    icon = logo.crop(bbox)
    bg = dominant_colour(icon)
    print(f"logo {logo.size} | icon bbox {bbox} -> {icon.size} | bg #{bg[0]:02X}{bg[1]:02X}{bg[2]:02X}")

    for name, size in SQUARE_ASSETS:
        path = os.path.join(OUT, name)
        save_square(icon, bg, size, path)
        print(f"  wrote {name} ({size}x{size})")

    wordmark = logo.crop((bbox[2] + 8, 0, logo.size[0], logo.size[1]))
    wide = os.path.join(OUT, "Wide310x150Logo.png")
    save_wide(wordmark, (310, 150), wide)
    print(f"  wrote Wide310x150Logo.png (310x150)")

    splash = os.path.join(OUT, "SplashScreen620x300.png")
    save_wide(logo, (620, 300), splash)
    print(f"  wrote SplashScreen620x300.png (620x300)")

    print(f"\nDone -> {OUT}")


if __name__ == "__main__":
    main()
