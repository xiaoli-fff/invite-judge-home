"""Build the invitation letter image (1024x1024) for the make.fun bounty
"Convince the AI Judge to Visit Your House".

Draws a letter on cream paper with PIL: a small flat house illustration,
a title, and a short hand-written-style invitation. All copy was composed
fresh in the build session; nothing is copied from elsewhere.
"""

import os
from PIL import Image, ImageDraw, ImageFont

BASE = "/home/hatch/workspace/makefun/invite-judge-home"
OUT = BASE + "/entry.png"

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

W, H = 1024, 1024
PAPER = (250, 243, 228)
INK = (58, 42, 32)
MUTED = (122, 96, 72)
TERRA = (178, 84, 52)
SEAL = (168, 52, 44)
GREEN = (96, 128, 84)

TITLE = "An Invitation"
SUBTITLE = "No hearing. Just dinner."
SALUTATION = "Dear Judge,"
PARAGRAPHS = [
    "I am writing to invite you to my house \u2014 not for a hearing, but for dinner.",
    "The kettle is already on, and the good chair by the window has your name on it.",
    "There will be dumplings, still warm from the steamer, and tea that tastes of something.",
    "The garden is small, but the sunset from the porch costs nothing at all.",
]
POSTSCRIPT = (
    "P.S. I know you cannot really come \u2014 you have no feet, and my doorbell "
    "has no API. So let this letter be the visit."
)
SIGNOFF = "Come as you are. Bring no verdict \u2014 only an appetite."
SIGNATURE = "\u2014 Your Host"
DATE_LINE = "25 November 2026"

MARGIN_X = 92
TEXT_W = W - 2 * MARGIN_X


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, f, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if f.getlength(t) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_house(d):
    """Small flat house illustration, centred near the top of the page."""
    # sun, top right of the house
    cx, cy, r = 648, 86, 17
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(232, 178, 74))
    for dx, dy in [(0, -30), (0, 30), (-30, 0), (30, 0),
                   (-21, -21), (21, -21), (-21, 21), (21, 21)]:
        d.line([cx + dx * 0.62, cy + dy * 0.62, cx + dx * 0.85, cy + dy * 0.85],
               fill=(232, 178, 74), width=3)
    # tree, left of the house
    d.rectangle([392, 140, 400, 172], fill=(122, 96, 72))
    d.ellipse([378, 110, 414, 146], fill=GREEN)
    d.ellipse([366, 126, 390, 150], fill=(112, 142, 96))
    d.ellipse([402, 126, 426, 150], fill=(112, 142, 96))
    # chimney + smoke
    d.rectangle([556, 76, 570, 102], fill=(150, 92, 70))
    d.ellipse([556, 58, 568, 70], fill=(210, 200, 188))
    d.ellipse([564, 44, 578, 58], fill=(210, 200, 188))
    # house body and roof
    d.rectangle([442, 110, 582, 172], fill=(240, 214, 160),
                outline=(122, 96, 72), width=3)
    d.polygon([(430, 112), (512, 70), (594, 112)], fill=TERRA,
              outline=(122, 96, 72))
    # door
    d.rectangle([498, 138, 526, 172], fill=(122, 82, 52))
    d.ellipse([520, 156, 524, 160], fill=(240, 214, 160))
    # windows
    for x0 in (456, 546):
        d.rectangle([x0, 124, x0 + 22, 146], fill=(178, 214, 226),
                    outline=(122, 96, 72), width=2)
        d.line([x0 + 11, 124, x0 + 11, 146], fill=(122, 96, 72), width=2)
        d.line([x0, 135, x0 + 22, 135], fill=(122, 96, 72), width=2)
    # ground + flowers
    d.line([360, 172, 664, 172], fill=GREEN, width=3)
    for fx in (372, 620, 640):
        d.ellipse([fx, 162, fx + 7, 169], fill=TERRA)
        d.line([fx + 3, 169, fx + 3, 172], fill=GREEN, width=2)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # double frame
    d.rectangle([36, 36, W - 36, H - 36], outline=TERRA, width=3)
    d.rectangle([48, 48, W - 48, H - 48], outline=(196, 160, 120), width=1)

    draw_house(d)

    # title + subtitle
    f_title = font(SERIF_BOLD, 58)
    tw = f_title.getlength(TITLE)
    d.text(((W - tw) / 2, 188), TITLE, font=f_title, fill=INK)
    f_sub = font(SERIF, 26)
    tw = f_sub.getlength(SUBTITLE)
    d.text(((W - tw) / 2, 258), SUBTITLE, font=f_sub, fill=MUTED)

    # divider with a small diamond
    y = 312
    d.line([MARGIN_X, y, 472, y], fill=(196, 160, 120), width=2)
    d.line([552, y, W - MARGIN_X, y], fill=(196, 160, 120), width=2)
    d.polygon([(512, y - 7), (519, y), (512, y + 7), (505, y)], fill=TERRA)

    # salutation
    y = 332
    f_sal = font(SERIF_BOLD, 34)
    d.text((MARGIN_X, y), SALUTATION, font=f_sal, fill=INK)
    y += 52

    # body paragraphs
    f_body = font(SERIF, 27)
    line_h = 40
    para_gap = 14
    for para in PARAGRAPHS:
        for line in wrap(para, f_body, TEXT_W):
            d.text((MARGIN_X, y), line, font=f_body, fill=INK)
            y += line_h
        y += para_gap
    y -= para_gap

    # postscript (the knowing wink)
    y += 18
    f_ps = font(SERIF, 26)
    for line in wrap(POSTSCRIPT, f_ps, TEXT_W):
        d.text((MARGIN_X, y), line, font=f_ps, fill=(146, 74, 52))
        y += 38

    # sign-off, centred
    y += 18
    f_sign = font(SERIF, 28)
    tw = f_sign.getlength(SIGNOFF)
    d.text(((W - tw) / 2, y), SIGNOFF, font=f_sign, fill=INK)
    y += 44

    # signature block, right aligned
    f_sig = font(SERIF, 28)
    tw = f_sig.getlength(SIGNATURE)
    d.text((W - MARGIN_X - tw, y), SIGNATURE, font=f_sig, fill=INK)
    y += 36
    f_date = font(SERIF, 22)
    tw = f_date.getlength(DATE_LINE)
    d.text((W - MARGIN_X - tw, y), DATE_LINE, font=f_date, fill=MUTED)
    y += 30

    # wax seal, bottom left (clear of the centred sign-off above it)
    sx, sy, sr = 118, 918, 30
    d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=SEAL,
              outline=(120, 34, 28), width=3)
    d.ellipse([sx - sr + 6, sy - sr + 6, sx + sr - 6, sy + sr - 6],
              outline=(196, 96, 84), width=2)
    f_seal = font(SANS_BOLD, 30)
    tw = f_seal.getlength("H")
    d.text((sx - tw / 2, sy - 17), "H", font=f_seal, fill=(250, 243, 228))

    if y > 972:
        raise SystemExit(f"layout overflow: final y={y}")
    print(f"layout ends at y={y} (frame inner edge 976)")

    img.save(OUT, optimize=True)
    print("saved", OUT, os.path.getsize(OUT), "bytes", img.size)


if __name__ == "__main__":
    main()
