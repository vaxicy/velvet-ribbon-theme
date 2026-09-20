"""Trim the picked AI logo: drop the coral outer border, keep the beige
rounded rectangle + bow, make outside transparent, crop tight, export 128.

Usage: python make_logo.py <source.png>
"""
import os
import sys
from PIL import Image, ImageChops, ImageDraw

SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..",
    "store-assets", "icon-candidates", "ai-2.png")
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT_LOGO = os.path.join(ROOT, "logo")
OUT_CAND = os.path.join(ROOT, "store-assets", "icon-candidates")
os.makedirs(OUT_LOGO, exist_ok=True)


def is_coral(p):
    return p[0] > 200 and 70 < p[1] < 185 and 70 < p[2] < 185 and (p[0] - p[1]) > 45


def scan(im, pts, forward=True):
    """First index in pts where the pixel is cream."""
    rng = pts if forward else list(reversed(pts))
    for i, (x, y) in enumerate(rng):
        if is_cream(im.getpixel((x, y))):
            return i
    return None


def main():
    im = Image.open(SRC).convert("RGB")
    W, H = im.size
    ip = im.load()
    cor = Image.new("L", (W, H), 0)
    cp = cor.load()
    for y in range(H):
        for x in range(W):
            if is_coral(ip[x, y]):
                cp[x, y] = 255
    ob = cor.getbbox()
    cx, cy = (ob[0] + ob[2]) // 2, (ob[1] + ob[3]) // 2

    def is_c(x, y):
        return is_coral(ip[x, y])

    left = ob[0]
    while left < ob[2] and is_c(left, cy):
        left += 1
    right = ob[2] - 1
    while right > ob[0] and is_c(right, cy):
        right -= 1
    top = ob[1]
    while top < ob[3] and is_c(cx, top):
        top += 1
    bot = ob[3] - 1
    while bot > ob[1] and is_c(cx, bot):
        bot -= 1
    print("coral outer:", ob, "-> inner:", (left, top, right, bot))

    # step inside past the coral edge / antialias halo
    inset = 10
    left, top, right, bot = left + inset, top + inset, right - inset, bot - inset

    # keep it square, centered on the cream rect
    side = min(right - left, bot - top)
    ccx, ccy = (left + right) // 2, (top + bot) // 2
    box = (ccx - side // 2, ccy - side // 2, ccx + side // 2, ccy + side // 2)
    crop = im.crop(box)

    SS = 4  # supersample for smooth corners
    n = crop.size[0] * SS
    big = crop.resize((n, n), Image.LANCZOS).convert("RGBA")
    radius = int(n * 0.115)
    mask = Image.new("L", (n, n), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, n - 1, n - 1], radius=radius, fill=255)
    big.putalpha(mask)

    master = big.resize((512, 512), Image.LANCZOS)
    master.save(os.path.join(OUT_CAND, "picked-bow-512.png"))
    master.resize((128, 128), Image.LANCZOS).save(os.path.join(OUT_LOGO, "logo128.png"))
    print("inner rect:", (left, top, right, bot), "side", side)
    print("saved logo128.png + picked-bow-512.png")


if __name__ == "__main__":
    main()
