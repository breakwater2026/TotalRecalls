"""TotalRecalls YouTube thumbnails — Jasper Channel Style, Template 2 (Product Proof).

1280x720, 40px safe margin, bottom-right keep-clear for the length stamp.
Chip top-left (mono, Steel on Slate) | headline left half (Bahnschrift Bold,
Paper, one Archive Amber word) | Graphite card right 45% with a blurred product
frame + 1px Slate border | evidence chip bottom-left (mono, Steel).
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

OUT = os.path.dirname(os.path.abspath(__file__))
F_HEAD = "C:/Windows/Fonts/bahnschrift.ttf"
F_MONO = "C:/Windows/Fonts/consolab.ttf"

OBSIDIAN = (17, 19, 21)
GRAPHITE = (26, 29, 33)
AMBER = (200, 138, 43)
PAPER = (243, 239, 231)
SLATE = (42, 47, 54)
STEEL = (122, 143, 166)
GREEN = (94, 138, 104)


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


def build(out, chip_text, headline, evidence, frame, saved=False):
    """headline: list of lines; each line is list of (text, color) segments."""
    W, H = 1280, 720
    img = Image.new("RGB", (W, H), OBSIDIAN)
    d = ImageDraw.Draw(img)
    f_chip = ImageFont.truetype(F_MONO, 34)
    f_ev = ImageFont.truetype(F_MONO, 30)

    # 1. series chip top-left
    chip(d, 40, 40, chip_text, f_chip, STEEL)

    # 4. focal card FIRST (right side) so headline can measure against it
    frame = Image.open(os.path.join(OUT, "frames", frame))
    # The TotalRecalls window sits centered at x 770-1570 in the 2292-wide frames;
    # crop that region so the card shows the app, not the black monitor margin.
    frame = frame.crop((770, 10, 1570, 1430))
    card_w = 460
    card_h = 560
    fw, fh = frame.size
    # fill the 460x560 card with a center crop of the app region
    scale = max(card_w / fw, card_h / fh)
    frame = frame.resize((int(fw * scale), int(fh * scale)), Image.LANCZOS)
    fw, fh = frame.size
    frame = frame.crop(((fw - card_w) // 2, (fh - card_h) // 2,
                        (fw - card_w) // 2 + card_w, (fh - card_h) // 2 + card_h))
    frame = frame.filter(ImageFilter.GaussianBlur(1.5))
    card = rounded_crop(frame, (0, 0, card_w, card_h), 14, SLATE)
    card_x, card_y = 780, 80
    img.paste(card, (card_x, card_y))
    d = ImageDraw.Draw(img)  # redraw over pasted card

    # 3. headline — left half, vertically centered, auto-fit so it never hits the card
    max_w = card_x - 48 - 20
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

    # 2. evidence chip bottom-left (below headline zone, no overlap with card)
    ev_y = H - 92
    if saved:
        w_chip = d.textlength("● SAVED LOCALLY", font=f_ev)
        chip(d, 40, ev_y, "● SAVED LOCALLY", f_ev, GREEN, bg=GRAPHITE)
        if evidence:
            d.text((40 + w_chip + 60, ev_y + 8), evidence, font=f_ev, fill=STEEL)
    elif evidence:
        chip(d, 40, ev_y, evidence, f_ev, STEEL, bg=GRAPHITE)

    img.save(os.path.join(OUT, "thumbnails", out), quality=90)
    print(f"  {out} (headline {size}px)")


P = (lambda t: (t, PAPER))
A = (lambda t: (t, AMBER))

VIDEOS = [
    # (filename, chip, headline lines, evidence, frame, saved)
    ("tr_thumb_master.jpg", "MASTER DEMO",
     [[P("EVERY AI "), A("CHAT.")], [P("ONE FOLDER.")]],
     ".MD · .JSON · OFFLINE", "thumb_master.jpg", False),
    ("tr_thumb_chatgpt.jpg", "GUIDE · CHATGPT",
     [[P("EVERY CHAT.")], [A("SAVED.")]],
     "C:\\TotalRecalls\\Library\\chatgpt\\", "thumb_chatgpt.jpg", True),
    ("tr_thumb_claude.jpg", "GUIDE · CLAUDE",
     [[P("EVERY CHAT.")], [A("SAVED.")]],
     "C:\\TotalRecalls\\Library\\claude\\", "thumb_claude.jpg", True),
    ("tr_thumb_perplexity.jpg", "GUIDE · PERPLEXITY",
     [[P("EVERY CHAT.")], [A("SAVED.")]],
     "C:\\TotalRecalls\\Library\\perplexity\\", "thumb_perplexity.jpg", True),
    ("tr_thumb_gemini.jpg", "GUIDE · GEMINI",
     [[P("EVERY CHAT.")], [A("SAVED.")]],
     "C:\\TotalRecalls\\Library\\gemini\\", "thumb_gemini.jpg", True),
    ("tr_thumb_grok.jpg", "GUIDE · GROK",
     [[P("EVERY CHAT.")], [A("SAVED.")]],
     "C:\\TotalRecalls\\Library\\grok\\", "thumb_grok.jpg", True),
    ("tr_thumb_mistral.jpg", "GUIDE · MISTRAL",
     [[P("EVERY CHAT.")], [A("SAVED.")]],
     "C:\\TotalRecalls\\Library\\mistral\\", "thumb_mistral.jpg", True),
    ("tr_thumb_qwen.jpg", "GUIDE · QWEN",
     [[P("EVERY CHAT.")], [A("SAVED.")]],
     "C:\\TotalRecalls\\Library\\qwen\\", "thumb_qwen.jpg", True),
    ("tr_thumb_deepseek.jpg", "GUIDE · DEEPSEEK",
     [[P("EVERY CHAT.")], [A("SAVED.")]],
     "C:\\TotalRecalls\\Library\\deepseek\\", "thumb_deepseek.jpg", True),
]

os.makedirs(os.path.join(OUT, "thumbnails"), exist_ok=True)
for v in VIDEOS:
    build(*v)
print(f"{len(VIDEOS)} thumbnails written to {OUT}/thumbnails/")
