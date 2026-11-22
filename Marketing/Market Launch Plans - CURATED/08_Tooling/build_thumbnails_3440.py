"""TotalRecalls YouTube thumbnails — 3440x1440 masters, Template 2 (Product Proof).

Rebuilds the 9 channel thumbnails (master + 8 provider walkthroughs) at 1280x720
from the current 3440x1440 CRF-10 narrated masters.

Fixes vs. the old `build_thumbnails.py`:
  * Panel 3 (the TotalRecalls app window) is cropped at x 1656..2516, y 20..1380
    of the 3440x1440 frame — the old crop assumed 2292-wide frames.
  * The app card is kept CRISP. The old script applied GaussianBlur(1.5) to the
    whole card; the only masking left is whatever the source video already burned
    in (account line + conversation titles in the _pro_sse masters).

Frames are extracted from a mid-download / connected moment of each video where
the app is actively writing files and no personal email is on screen.

The master thumbnail uses the 12s convergence animation
(`TR_yt_convergence.mp4`, 8 sources -> 1 folder) rather than an app panel.
"""
from PIL import Image, ImageDraw, ImageFont
import os
import subprocess

TOOLING = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(TOOLING, "..", "07_Assets", "thumbnails_3440"))
FRAMES = os.path.join(OUT, "frames")
VIDEOS = r"C:\Users\break\Projects\TotalRecalls-Source Code\Videos\TR-demo-shoot"
CONVERGENCE = (
    r"C:\Users\break\Projects\TotalRecalls-Source Code\Marketing"
    r"\Market Launch Plans\YouTube\videos\TR_yt_convergence.mp4"
)
FFMPEG = "ffmpeg"

F_HEAD = "C:/Windows/Fonts/bahnschrift.ttf"
F_MONO = "C:/Windows/Fonts/consolab.ttf"

OBSIDIAN = (17, 19, 21)
GRAPHITE = (26, 29, 33)
AMBER = (200, 138, 43)
PAPER = (243, 239, 231)
SLATE = (42, 47, 54)
STEEL = (122, 143, 166)
GREEN = (94, 138, 104)

# Panel 3 of the 3440x1440 canvas: the TotalRecalls app window.
PANEL = (1656, 20, 2516, 1380)  # x0, y0, x1, y1

# provider -> (video filename, timestamp in seconds)
PROVIDERS = [
    ("chatgpt", "TR_website_chatgpt_pro_sse.mp4", 180),
    ("claude", "TR_website_claude_pro_sse.mp4", 140),
    ("perplexity", "TR_website_perplexity_pro_sse.mp4", 150),
    ("deepseek", "TR_website_deepseek_pro_sse.mp4", 120),
    ("gemini", "TR_website_gemini_pro_sse.mp4", 130),
    ("grok", "TR_website_grok_pro_sse.mp4", 150),
    ("mistral", "TR_website_mistral_pro_sse.mp4", 115),
    ("qwen", "TR_website_qwen_pro_sse.mp4", 120),
]


def extract_frame(video, t, out_path, crop=None):
    vf = []
    if crop:
        x0, y0, x1, y1 = crop
        vf.append(f"crop={x1 - x0}:{y1 - y0}:{x0}:{y0}")
    cmd = [FFMPEG, "-v", "error", "-ss", str(t), "-i", video, "-frames:v", "1"]
    if vf:
        cmd += ["-vf", ",".join(vf)]
    cmd += ["-q:v", "2", out_path, "-y"]
    subprocess.run(cmd, check=True)
    return out_path


def chip(draw, x, y, text, fnt, fg, bg=SLATE, radius=12):
    w = draw.textlength(text, font=fnt)
    h = fnt.size
    draw.rounded_rectangle([x, y, x + w + 40, y + h + 24], radius=radius, fill=bg)
    draw.text((x + 20, y + 10), text, font=fnt, fill=fg)


def rounded_crop(img, box, radius, border):
    x, y, w, h = box
    crop = img.crop((x, y, x + w, y + h))
    mask = Image.new("L", crop.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, crop.size[0], crop.size[1]], radius=radius, fill=255)
    out = Image.new("RGB", crop.size, OBSIDIAN)
    out.paste(crop, (0, 0), mask)
    ImageDraw.Draw(out).rounded_rectangle([0, 0, crop.size[0] - 1, crop.size[1] - 1],
                                          radius=radius, outline=border, width=2)
    return out


def fit_cover(img, card_w, card_h):
    """Scale to cover the card, then centre-crop. No blur."""
    fw, fh = img.size
    scale = max(card_w / fw, card_h / fh)
    img = img.resize((max(1, int(fw * scale)), max(1, int(fh * scale))), Image.LANCZOS)
    fw, fh = img.size
    return img.crop(((fw - card_w) // 2, (fh - card_h) // 2,
                     (fw - card_w) // 2 + card_w, (fh - card_h) // 2 + card_h))


def build(out, chip_text, headline, evidence, frame_path, saved=False,
          card=(780, 60, 460, 560), fit=fit_cover):
    """headline: list of lines; each line is list of (text, color) segments."""
    W, H = 1280, 720
    img = Image.new("RGB", (W, H), OBSIDIAN)
    d = ImageDraw.Draw(img)
    f_chip = ImageFont.truetype(F_MONO, 34)
    f_ev = ImageFont.truetype(F_MONO, 28)

    chip_x, chip_y, card_w, card_h = card

    # focal card first (right side) so the headline can measure against it
    frame = fit(Image.open(frame_path).convert("RGB"), card_w, card_h)
    card_img = rounded_crop(frame, (0, 0, card_w, card_h), 14, SLATE)
    img.paste(card_img, (chip_x, chip_y))
    d = ImageDraw.Draw(img)

    # series chip top-left
    chip(d, 40, 40, chip_text, f_chip, STEEL)

    # headline — left half, vertically centred, auto-fit so it never hits the card
    max_w = chip_x - 48 - 20
    size = 140
    while size > 72:
        f = ImageFont.truetype(F_HEAD, size)
        longest = max(d.textlength("".join(t for t, _ in line), font=f) for line in headline)
        if longest <= max_w:
            break
        size -= 4
    f_head = ImageFont.truetype(F_HEAD, size)
    asc, desc = f_head.getmetrics()
    line_h = int(asc + desc + 6)
    total = line_h * len(headline)
    y = (H - total) // 2 + 6
    for line in headline:
        x = 48
        for text, color in line:
            d.text((x, y), text, font=f_head, fill=color)
            x += d.textlength(text, font=f_head)
        y += line_h

    # evidence chip bottom-left
    ev_y = H - 92
    if saved:
        w_chip = d.textlength("● SAVED LOCALLY", font=f_ev)
        chip(d, 40, ev_y, "● SAVED LOCALLY", f_ev, GREEN, bg=GRAPHITE)
        if evidence:
            d.text((40 + w_chip + 44, ev_y + 8), evidence, font=f_ev, fill=STEEL)
    elif evidence:
        chip(d, 40, ev_y, evidence, f_ev, STEEL, bg=GRAPHITE)

    img.save(os.path.join(OUT, out), quality=92)
    print(f"  {out} (headline {size}px)")


P = (lambda t: (t, PAPER))
A = (lambda t: (t, AMBER))


VIDEOS_SPEC = [
    ("tr_thumb_master.jpg", "MASTER DEMO",
     [[P("EVERY AI "), A("CHAT.")], [P("ONE FOLDER.")]],
     ".MD · .JSON · OFFLINE", "master.jpg", False),
    ("tr_thumb_chatgpt.jpg", "GUIDE · CHATGPT",
     [[P("EVERY CHAT.")], [A("SAVED.")]],
     "C:\\TotalRecalls\\Library\\chatgpt\\", "chatgpt.jpg", True),
    ("tr_thumb_claude.jpg", "GUIDE · CLAUDE",
     [[P("EVERY CHAT.")], [A("SAVED.")]],
     "C:\\TotalRecalls\\Library\\claude\\", "claude.jpg", True),
    ("tr_thumb_perplexity.jpg", "GUIDE · PERPLEXITY",
     [[P("EVERY CHAT.")], [A("SAVED.")]],
     "C:\\TotalRecalls\\Library\\perplexity\\", "perplexity.jpg", True),
    ("tr_thumb_gemini.jpg", "GUIDE · GEMINI",
     [[P("EVERY CHAT.")], [A("SAVED.")]],
     "C:\\TotalRecalls\\Library\\gemini\\", "gemini.jpg", True),
    ("tr_thumb_grok.jpg", "GUIDE · GROK",
     [[P("EVERY CHAT.")], [A("SAVED.")]],
     "C:\\TotalRecalls\\Library\\grok\\", "grok.jpg", True),
    ("tr_thumb_mistral.jpg", "GUIDE · MISTRAL",
     [[P("EVERY CHAT.")], [A("SAVED.")]],
     "C:\\TotalRecalls\\Library\\mistral\\", "mistral.jpg", True),
    ("tr_thumb_qwen.jpg", "GUIDE · QWEN",
     [[P("EVERY CHAT.")], [A("SAVED.")]],
     "C:\\TotalRecalls\\Library\\qwen\\", "qwen.jpg", True),
    ("tr_thumb_deepseek.jpg", "GUIDE · DEEPSEEK",
     [[P("EVERY CHAT.")], [A("SAVED.")]],
     "C:\\TotalRecalls\\Library\\deepseek\\", "deepseek.jpg", True),
]


def main():
    os.makedirs(FRAMES, exist_ok=True)

    # 1. extract the 8 provider panels
    for provider, filename, t in PROVIDERS:
        dst = os.path.join(FRAMES, f"{provider}.jpg")
        if not os.path.exists(dst):
            extract_frame(os.path.join(VIDEOS, filename), t, dst, crop=PANEL)
        print(f"frame {provider}.jpg  <- {filename} @ {t}s")

    # 2. master card frame from the convergence animation (8 sources -> 1 folder).
    #    Crop to the converging lines + destination folder; the animation is
    #    16:9, so a portrait card can't hold the source column and the folder.
    master_frame = os.path.join(FRAMES, "master.jpg")
    if not os.path.exists(master_frame):
        raw = extract_frame(CONVERGENCE, 6.0, os.path.join(FRAMES, "_master_raw.jpg"))
        Image.open(raw).convert("RGB").crop((560, 0, 1060, 720)).save(master_frame, quality=95)
        os.remove(raw)
    print("frame master.jpg  <- TR_yt_convergence.mp4 @ 6s (crop 560..1060)")

    # 3. render all 9 thumbnails
    for out, chip_text, headline, evidence, frame, saved in VIDEOS_SPEC:
        build(out, chip_text, headline, evidence, os.path.join(FRAMES, frame),
              saved=saved, fit=fit_cover)

    print(f"\n{len(VIDEOS_SPEC)} thumbnails written to {OUT}")


if __name__ == "__main__":
    main()
