"""Flat rounded-rectangle logo candidates for velvet-ribbon-theme.

Clean bow shape: two rounded triangles (loops) + knot + two short tails.
No gradients. Transparent bg, 512px.
"""
import os
import math
from PIL import Image, ImageDraw

S = 512
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                   "store-assets", "icon-candidates")
os.makedirs(OUT, exist_ok=True)

CORAL = (255, 149, 165)
CORAL_D = (233, 112, 134)
LAV = (206, 162, 211)
LAV_D = (176, 124, 184)
BLUE = (86, 111, 174)
PLUM = (120, 60, 122)
WHITE = (255, 255, 255)


def rpoly(d, pts, r, fill):
    """Convex polygon with visibly rounded corners."""
    d.polygon(pts, fill=fill)
    for (x, y) in pts:
        d.ellipse([x - r, y - r, x + r, y + r], fill=fill)


def tail(img, x0, y0, x1, y1, w, col):
    """Short ribbon tail with a clean rounded tip."""
    d = ImageDraw.Draw(img)
    d.line([(x0, y0), (x1, y1)], fill=col, width=w)
    d.ellipse([x1 - w / 2, y1 - w / 2, x1 + w / 2, y1 + w / 2], fill=col)


def bow(img, cx, cy, c1, c2, knot, tails=True):
    d = ImageDraw.Draw(img)
    LW, LH, KR = 146, 82, 30
    if tails:
        tail(img, cx - 14, cy + 26, cx - 68, cy + 150, 42, c1)
        tail(img, cx + 14, cy + 26, cx + 68, cy + 150, 42, c2)
    rpoly(d, [(cx - 4, cy), (cx - LW, cy - LH), (cx - LW, cy + LH)], 22, c1)
    rpoly(d, [(cx + 4, cy), (cx + LW, cy - LH), (cx + LW, cy + LH)], 22, c2)
    d.rounded_rectangle([cx - KR, cy - 36, cx + KR, cy + 36], radius=20, fill=knot)


def frame(img, style):
    d = ImageDraw.Draw(img)
    box = [46, 46, S - 46, S - 46]
    if style == "outline":
        d.rounded_rectangle(box, radius=92, outline=CORAL, width=26)
    elif style == "lav":
        d.rounded_rectangle(box, radius=92, fill=LAV)
    elif style == "coral":
        d.rounded_rectangle(box, radius=92, fill=CORAL)
    elif style == "white":
        d.rounded_rectangle(box, radius=92, fill=WHITE, outline=CORAL, width=20)
    elif style == "blue":
        d.rounded_rectangle(box, radius=92, outline=BLUE, width=26)


def make(style, c1, c2, knot, tails=True):
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    frame(img, style)
    bow(img, S / 2, S / 2 - 12, c1, c2, knot, tails)
    return img


def sheet(vs, names):
    pad = 22
    cols = 2
    rows = (len(vs) + cols - 1) // cols
    W = cols * S + (cols + 1) * pad
    H = rows * S + (rows + 1) * pad
    sh = Image.new("RGBA", (W, H), (246, 241, 246, 255))
    d = ImageDraw.Draw(sh)
    for i, v in enumerate(vs):
        r, c = divmod(i, cols)
        x = pad + c * (S + pad)
        y = pad + r * (S + pad)
        d.rounded_rectangle([x, y, x + S, y + S], radius=22, fill=WHITE)
        sh.alpha_composite(v, (x, y))
    return sh.convert("RGB")


def main():
    vs = [
        make("outline", CORAL, CORAL, CORAL_D),
        make("lav", WHITE, WHITE, PLUM),
        make("white", CORAL, CORAL, PLUM),
        make("coral", WHITE, WHITE, PLUM),
        make("blue", CORAL, CORAL, CORAL_D),
        make("outline", CORAL, LAV, PLUM),
    ]
    names = "abcdef"
    for v, n in zip(vs, names):
        v.save(os.path.join(OUT, "flat-%s.png" % n))
    sheet(vs, names).save(os.path.join(OUT, "preview-sheet.png"))
    print("saved", os.path.abspath(OUT))


if __name__ == "__main__":
    main()
