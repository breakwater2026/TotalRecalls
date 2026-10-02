"""Recreate the landing-page ConvergenceDiagram as an animated MP4 for the YT channel.

Faithful to site/src/components/landing/ConvergenceDiagram.jsx:
  - 8 provider tiles (real logo paths from RiskMatrix.LOGOS, brand-color tiles)
  - curved data-flow paths converging on the C:\\TotalRecalls library folder
  - animated dash offset + moving packet rects (staggered 0.4s, 2.4s loop)
  - top scanline, CONVERGENCE · LIVE / 8 SOURCES → 1 FOLDER labels
Site dark theme: bg #101113, card #16181B, primary #2F7BFF, border #26292E, muted #9AA3AF.
Output: videos/tr_convergence_loop.mp4 (30 fps, ~12 s loop, silent AAC).
"""
import json, math, os
from PIL import Image, ImageDraw, ImageFont
from svgpathtools import parse_path, Path

OUT = os.path.dirname(os.path.abspath(__file__))
VIDEO = os.path.join(OUT, "videos", "tr_convergence_loop.mp4")
FRAME = 1280
HEIGHT = 720
FPS = 30
DUR = 12.0
N = int(FPS * DUR)
SCALE = 2.4          # 400x300 viewBox -> 960x720
OX = (FRAME - 400 * SCALE) / 2   # center: 160

BG = (16, 17, 19)        # #101113
CARD = (22, 24, 27)      # #16181B
PRIMARY = (47, 123, 255) # #2F7BFF
BORDER = (38, 41, 46)    # #26292E
MUTED = (154, 163, 175)  # #9AA3AF
FOREGROUND = (232, 234, 237)  # #E8EAED

PROVIDERS = [
    ("ChatGPT", "OAI-001", "ChatGPT", "#FFFFFF", "#10A37F"),
    ("Claude", "ANT-002", "Claude", "#FFFFFF", "#D97757"),
    ("Perplexity", "PPL-003", "Perplexity", "#FFFFFF", "#20B8CD"),
    ("Gemini", "GEM-004", "Gemini", "#4285F4", "#000000"),
    ("Grok", "GRK-005", "Grok", "#FFFFFF", "#0F172A"),
    ("DeepSeek", "DSK-006", "DeepSeek", "#4F8CFF", "#1E40AF"),
    ("Mistral", "MST-007", "Mistral", "#FF7000", "#FFF3E8"),
    ("Qwen Chat", "QWN-008", "Qwen", "#615CED", "#F0EFFF"),
]
YS = [20, 58, 96, 134, 172, 210, 248, 286]  # viewBox units


def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def U(x, y):
    """viewBox units -> canvas px."""
    return (OX + x * SCALE, y * SCALE)


def cubic(p0, p1, p2, p3, n=120):
    pts = []
    for i in range(n + 1):
        t = i / n
        a = (1 - t) ** 3
        b = 3 * (1 - t) ** 2 * t
        c = 3 * (1 - t) * t ** 2
        d = t ** 3
        x = a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0]
        y = a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]
        pts.append((x, y))
    return pts


# --- flow geometry (viewBox units), precompute pixel polylines + arc lengths ---
FLOWS = []
for y in YS:
    pts = cubic((90, y), (170, y), (185, 150), (232, 150), n=160)
    pix = [U(*p) for p in pts]
    # cumulative arc length
    cum = [0.0]
    for i in range(1, len(pix)):
        cum.append(cum[-1] + math.hypot(pix[i][0] - pix[i - 1][0], pix[i][1] - pix[i - 1][1]))
    FLOWS.append((pix, cum))
    # assert endpoint lands on folder left edge (~232,150 units)


def point_at(pix, cum, dist):
    """pixel point at arc-length dist along the polyline (clamped)."""
    total = cum[-1]
    dist = dist % total  # loop
    for i in range(1, len(cum)):
        if cum[i] >= dist:
            seg = cum[i] - cum[i - 1] or 1
            f = (dist - cum[i - 1]) / seg
            return (pix[i][0] - (pix[i][0] - pix[i - 1][0]) * (1 - f),
                    pix[i][1] - (pix[i][1] - pix[i - 1][1]) * (1 - f))
    return pix[-1]


# --- logos: rasterize each SVG path into a small mask ---
def sample_path(d, n=200):
    """Sample an SVG path string into a list of (real, imag) points.
    Iterates each element and samples it by its local t in [0,1] (robust for
    multi-subpath paths with arcs/beziers where Path.point(l) can fail)."""
    try:
        p = parse_path(d)
        total = max(p.length(), 1e-9)
    except Exception:
        return []
    pts = []
    for el in list(p):
        try:
            L = el.length()
        except Exception:
            continue
        k = max(2, int(n * (L / total)))
        for i in range(k):
            try:
                pts.append(el.point(i / (k - 1)))
            except Exception:
                pass
    return pts


def evenodd_fill(size, polygons):
    """Even-odd rule polygon fill -> PIL 'L' image (255 inside, 0 outside).
    Handles holes (rings) correctly regardless of winding direction."""
    img = Image.new("L", (size, size), 0)
    px = img.load()
    for y in range(size):
        # find x-intervals where a horizontal ray crosses an odd number of edges
        xs = []
        for poly in polygons:
            n = len(poly)
            for i in range(n):
                x1, y1 = poly[i]
                x2, y2 = poly[(i + 1) % n]
                if (y1 <= y < y2) or (y2 <= y < y1):
                    if abs(y2 - y1) > 1e-9:
                        t = (y - y1) / (y2 - y1)
                        xs.append(x1 + t * (x2 - x1))
        xs.sort()
        for j in range(0, len(xs) - 1, 2):
            for x in range(int(xs[j]), int(xs[j + 1]) + 1):
                if 0 <= x < size:
                    px[x, y] = 255
    return img


def build_logo_mask(d, vb, size=44):
    """Render an SVG path (possibly multi-subpath) into a 1-bit mask of `size` px,
    fitted to its own bbox. Splits the raw path string on Move commands so
    multi-subpath logos (rings) fill correctly with even-odd."""
    allpts = sample_path(d, 400)
    if not allpts:
        return Image.new("L", (size, size), 0)
    xs = [p.real for p in allpts]
    ys = [p.imag for p in allpts]
    x0, x1 = min(xs), max(xs)
    y0, y1 = min(ys), max(ys)
    w, h = max(x1 - x0, 1e-6), max(y1 - y0, 1e-6)
    pad = 0.06
    s = (size * (1 - 2 * pad)) / max(w, h)
    ox, oy = (size - w * s) / 2, (size - h * s) / 2

    def X(p):
        return ((p.real - x0) * s + ox, (p.imag - y0) * s + oy)

    import re as _re
    subs = [s2 for s2 in _re.split(r'(?<=[Mm])', d) if s2.strip()]
    polys = []
    for sub in subs:
        pts = [X(p) for p in sample_path(sub, 120)]
        if len(pts) > 2:
            polys.append(pts)
    if not polys:
        polys = [[X(p) for p in allpts]]
    return evenodd_fill(size, polys)


logos = json.load(open(os.path.join(OUT, "logos.json")))
LOGO_MASKS = {}
for name, (d, vb) in logos.items():
    try:
        LOGO_MASKS[name] = build_logo_mask(d, vb)
    except Exception as e:
        print(f"logo {name}: {e}")

FONT_DIR = "C:/Windows/Fonts"
F_HEAD = ImageFont.truetype(f"{FONT_DIR}/segoeui.ttf", 24)
F_MONO_S = ImageFont.truetype(f"{FONT_DIR}/consola.ttf", 17)
F_MONO = ImageFont.truetype(f"{FONT_DIR}/consola.ttf", 20)
F_FOLDER = ImageFont.truetype(f"{FONT_DIR}/consola.ttf", 21)


def draw_base():
    base = Image.new("RGB", (FRAME, HEIGHT), BG)
    d = ImageDraw.Draw(base)
    # outer hairline
    d.rectangle([8, 8, FRAME - 9, HEIGHT - 9], outline=BORDER, width=1)
    # header labels
    d.text((FRAME / 2, 22), "CONVERGENCE · LIVE", font=F_MONO_S, fill=MUTED, anchor="ma")
    d.text((FRAME - 40, 22), "8 SOURCES → 1 FOLDER", font=F_MONO_S, fill=PRIMARY, anchor="ra")
    # provider rows
    for i, (name, code, logo_key, glyph, tile) in enumerate(PROVIDERS):
        y = U(0, YS[i])[1]
        # row card
        x0 = U(10, 0)[0]
        x1 = x0 + 140 * SCALE
        h = 64
        d.rounded_rectangle([x0, y - h / 2, x1, y + h / 2], radius=4,
                            fill=CARD, outline=BORDER, width=1)
        # tile
        tx0 = x0 + 10
        t = 44
        tx0 = int(tx0)
        d.rounded_rectangle([tx0, y - t / 2, tx0 + t, y + t / 2], radius=4, fill=hex2rgb(tile))
        if logo_key in LOGO_MASKS:
            mask = LOGO_MASKS[logo_key].convert("L")
            base.paste(hex2rgb(glyph), (tx0, int(y - t / 2)), mask)
        # labels
        d.text((tx0 + t + 12, y - 13), name, font=F_HEAD, fill=FOREGROUND)
        d.text((tx0 + t + 12, y + 13), code, font=F_MONO_S, fill=MUTED)
    # folder box
    fx0 = U(232, 0)[0]
    fx1 = fx0 + 136 * SCALE
    fy0 = U(0, 99)[1]
    fy1 = U(0, 214.8)[1]
    d.rounded_rectangle([fx0, fy0, fx1, fy1], radius=6, fill=BG,
                        outline=(*PRIMARY, ), width=2)
    # folder glyph (simple)
    cx = (fx0 + fx1) / 2
    gy = fy0 + 42
    gw, gh = 64, 48
    d.rounded_rectangle([cx - gw / 2, gy, cx + gw / 2, gy + gh], radius=5,
                        outline=PRIMARY, width=3)
    d.polygon([(cx - gw / 2, gy), (cx - gw / 2 + 22, gy), (cx - gw / 2 + 30, gy - 12),
               (cx - 18, gy - 12)], outline=PRIMARY)
    d.line([(cx - gw / 2 + 30, gy - 12), (cx - gw / 2 + 30, gy)], fill=PRIMARY, width=3)
    d.text((cx, fy1 - 66), "C:\\TotalRecalls", font=F_FOLDER, fill=FOREGROUND, anchor="ma")
    d.text((cx, fy1 - 40), "Library\\", font=F_FOLDER, fill=MUTED, anchor="ma")
    d.text((cx, fy1 - 20), "797 files · secured", font=F_MONO_S, fill=PRIMARY, anchor="ma")
    return base


def draw_frame(base, t):
    d = ImageDraw.Draw(base, "RGB")
    # top scanline: sweeps top->bottom over 3s
    sy = int((t % 3.0) / 3.0 * HEIGHT)
    d.line([(10, sy), (FRAME - 10, sy)], fill=(*PRIMARY,), width=1)
    # flows: static hairline + animated dash
    dash_on, dash_off = 4 * SCALE, 6 * SCALE
    period = dash_on + dash_off
    offset = (t * (20 * SCALE / 2.0)) % period   # 20 units / 2 s
    for i, (pix, cum) in enumerate(FLOWS):
        d.line(pix, fill=BORDER, width=1)
        # animated dash: pattern phase slides along the path over time
        total = cum[-1]
        for j in range(1, len(pix)):
            a, b = cum[j - 1], cum[j]
            if b - a <= 0:
                continue
            # does this segment contain any "on" portion?
            seg_start = (a + offset) % period
            # check overlap of [0,seg] with on-windows
            draw = False
            nwin = int((b + offset) / period) + 1
            for k in range(nwin):
                on0, on1 = k * period, k * period + dash_on
                lo = max(a, on0)
                hi = min(b, on1)
                if lo < hi:
                    draw = True
                    break
            if draw:
                d.line([pix[j - 1], pix[j]], fill=PRIMARY, width=2)
        # moving packet (staggered 0.4 s, 2.4 s loop)
        frac = ((t - i * 0.4) % 2.4) / 2.4
        px, py = point_at(pix, cum, frac * total)
        d.rounded_rectangle([px - 5, py - 3.5, px + 5, py + 3.5], radius=2, fill=PRIMARY)
    return base


def main():
    base = draw_base()
    seq = os.path.join(OUT, "frames_convergence")
    os.makedirs(seq, exist_ok=True)
    for n in range(N):
        img = base.copy()
        draw_frame(img, n / FPS)
        img.save(os.path.join(seq, f"f{n:04d}.png"))
        if n % 60 == 0:
            print(f"frame {n}/{N}")
    print("frames done")
    out_mp4 = os.path.join(OUT, "videos", "TR_yt_convergence.mp4")
    os.makedirs(os.path.dirname(out_mp4), exist_ok=True)
    cmd = [
        "ffmpeg", "-y", "-framerate", "30", "-i",
        os.path.join(seq, "f%04d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "slow",
        "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
        "-map", "0:v:0", "-map", "1:a:0", "-c:a", "aac", "-b:a", "128k",
        "-shortest", "-movflags", "+faststart", out_mp4,
    ]
    import subprocess
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("ffmpeg FAILED:\n", r.stderr[-2000:])
    else:
        print("encoded", out_mp4)


if __name__ == "__main__":
    main()
