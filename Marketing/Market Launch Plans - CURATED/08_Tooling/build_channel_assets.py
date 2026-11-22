"""TotalRecalls YouTube channel assets per Jasper cookbook.

Palette (Channel Style doc): Obsidian #111315, Graphite #1A1D21,
Paper #F3EFE7, Steel Blue #7A8FA6, Slate #2A2F36.
Banner: 2560x1440, all text in 1546x423 safe area (Style 2.2/2.3).
Icon: 800x800, mark 50-55% of diameter, 80px circle margin (Style 3.1/3.2).
Watermark: 150x150, solid Obsidian circle (Style 6.1).
Mark source: app.ico (256x87 frame, 87x87 icon square) — the real brand mark.
"""
from PIL import Image, ImageDraw, ImageFont
import os

OUT = os.path.dirname(os.path.abspath(__file__))
FONT_BOLD = "C:/Windows/Fonts/bahnschrift.ttf"
FONT_MONO = "C:/Windows/Fonts/consola.ttf"

OBSIDIAN = (17, 19, 21, 255)
GRAPHITE = (26, 29, 33, 255)
PAPER = (243, 239, 231, 255)
STEEL = (122, 143, 166, 255)
SLATE = (42, 47, 54, 255)

def F(path, size):
    return ImageFont.truetype(path, size)

def get_mark(size):
    """Extract the 87x87 icon square from app.ico, upscale cleanly."""
    im = Image.open("C:/Users/break/Projects/TotalRecalls/app.ico").copy()
    icon = im.crop((0, 0, 87, 87)).convert("RGBA")
    return icon.resize((size, size), Image.LANCZOS)

def make_icon():
    W = 800
    im = Image.new("RGBA", (W, W), OBSIDIAN)
    mark = get_mark(416)  # 52% of diameter
    # circle-safe: centered, 416 + margin keeps it clear of the 80px edge ring
    im.paste(mark, ((W - 416) // 2, (W - 416) // 2), mark)
    p = os.path.join(OUT, "channel_icon_800.png")
    im.save(p)
    im.resize((98, 98), Image.LANCZOS).save(os.path.join(OUT, "qc_icon_98.png"))
    im.resize((48, 48), Image.LANCZOS).save(os.path.join(OUT, "qc_icon_48.png"))
    print("icon:", p, f"{os.path.getsize(p)/1024:.0f} KB")

def folder(d, x, y, s, color, w):
    d.rounded_rectangle([x, y + s * 0.18, x + s, y + s], radius=s * 0.1, outline=color, width=w)
    d.line([(x, y + s * 0.30), (x + s * 0.35, y + s * 0.30)], fill=color, width=w)
    d.line([(x, y + s * 0.18), (x + s * 0.30, y + s * 0.18), (x + s * 0.42, y + s * 0.30)], fill=color, width=w)

def make_banner():
    W, H = 2560, 1440
    im = Image.new("RGBA", (W, H), OBSIDIAN)
    d = ImageDraw.Draw(im)
    top = (H - 423) // 2
    d.rectangle([0, top, W, top + 423], fill=GRAPHITE)
    # faint folder-grid texture OUTSIDE the safe strip (Style 2.3: 4-6% opacity)
    tex = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    td = ImageDraw.Draw(tex)
    for i in range(22):
        for j in range(11):
            x, y = 40 + i * 116, 40 + j * 132
            if top - 30 < y < top + 423 + 30:
                continue
            folder(td, x, y, 56, SLATE, 2)
    tex.putalpha(tex.getchannel("A").point(lambda a: min(a, 14)))
    im = Image.alpha_composite(im, tex)
    d = ImageDraw.Draw(im)
    # safe area 1546 wide, centered; text left-aligned with 80px inner padding
    L = (W - 1546) // 2 + 80
    # wordmark ~64px cap height -> font 92
    d.text((L, top + 40), "TotalRecalls", font=F(FONT_BOLD, 92), fill=PAPER)
    # headline (Strategy §Banner: one line, Paper)
    d.text((L, top + 168), "Save your AI conversations as local files.", font=F(FONT_BOLD, 92), fill=PAPER)
    # detail line, mono, Steel Blue
    d.text((L, top + 312), "MARKDOWN · JSON · WINDOWS 10/11", font=F(FONT_MONO, 40), fill=STEEL)
    p = os.path.join(OUT, "channel_banner_2560x1440.png")
    im.convert("RGB").save(p, optimize=True)
    print("banner:", p, f"{os.path.getsize(p)/1e6:.2f} MB")
    im.crop((0, top, W, top + 423)).save(os.path.join(OUT, "qc_banner_desktop_strip.png"))
    cx = (W - 1855) // 2
    im.crop((cx, top, cx + 1855, top + 423)).save(os.path.join(OUT, "qc_banner_tablet_strip.png"))

def make_watermark():
    W = 300
    im = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse([0, 0, W, W], fill=OBSIDIAN)
    mark = get_mark(165)  # 55% of 300
    im.paste(mark, ((W - 165) // 2, (W - 165) // 2), mark)
    im = im.resize((150, 150), Image.LANCZOS)
    p = os.path.join(OUT, "channel_watermark_150.png")
    im.save(p)
    print("watermark:", p, f"{os.path.getsize(p)/1024:.0f} KB")

if __name__ == "__main__":
    make_icon()
    make_banner()
    make_watermark()
